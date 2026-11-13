#!/usr/bin/env python3
"""Independent exact review of the frozen cotangent-packet source words.

No worker-a builder, replay helper, or author verifier is imported. The
interpreter is a small Fraction row engine; the chart-pair phase check uses a
direct exact Pauli tableau plus Gaussian-dyadic |0> state computation.
"""
import argparse, gzip, hashlib, itertools, json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PINS = {
    "native": "2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883",
    "full": "d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7",
    "rail": "a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc",
    "cyclic": "ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2",
    "clifford": "2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962",
    "native_map": "3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38",
}

def need(ok, why):
    if not ok:
        raise ValueError(why)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read_gz(path):
    return json.loads(gzip.decompress(path.read_bytes()))

def q(x):
    return F(str(x))

def plus(x, y, coeff=F(1)):
    out = x.copy()
    for k,v in y.items():
        w = out.get(k,F(0)) + coeff*v
        if w:
            out[k] = w
        else:
            out.pop(k,None)
    return out

def span(frame):
    values={0}
    for v in frame:
        values |= {z ^ v for z in tuple(values)}
    return frozenset(values)

def rank(matrix):
    if not matrix:
        return 0
    a=[list(map(F,row)) for row in matrix]
    nr,nc=len(a),len(a[0]); p=0
    for c in range(nc):
        ix=next((r for r in range(p,nr) if a[r][c]),None)
        if ix is None: continue
        a[p],a[ix]=a[ix],a[p]
        z=a[p][c];a[p]=[v/z for v in a[p]]
        for r in range(nr):
            if r!=p and a[r][c]:
                z=a[r][c];a[r]=[v-z*w for v,w in zip(a[r],a[p])]
        p+=1
        if p==nr: break
    return p

def inverse(matrix):
    n=len(matrix)
    a=[list(map(F,row))+[F(i==j) for j in range(n)] for i,row in enumerate(matrix)]
    for c in range(n):
        ix=next((r for r in range(c,n) if a[r][c]),None)
        need(ix is not None,"singular exact matrix inverse")
        a[c],a[ix]=a[ix],a[c]
        z=a[c][c];a[c]=[v/z for v in a[c]]
        for r in range(n):
            if r!=c and a[r][c]:
                z=a[r][c];a[r]=[v-z*w for v,w in zip(a[r],a[c])]
    return [row[n:] for row in a]

def replay(word, n, limit=None, allow_open=False, watch_before=None):
    frames=word["frames"]; spaces=[span(f) for f in frames]
    own=word["owned_fields"]; rows=[{i:F(1)} for i in range(n)]+[{} for _ in range(own)]
    loc=list(word["initial"])+[None]*own
    live=set(range(n));counts=Counter();moves=Counter();om=Counter();rm=Counter()
    peak=now=lifetimes=0; snapshots={}
    stop=len(word["program"]) if limit is None else limit
    for t,op in enumerate(word["program"][:stop]):
        if watch_before and t in watch_before:
            snapshots[t]=({k:v.copy() for k,v in enumerate(rows) if v},loc.copy(),live.copy())
        typ,d=op[:2];counts[typ]+=1
        if typ=="INIT":
            need(d>=n and d not in live and loc[d] is None,f"INIT owner at {t}")
            loc[d]=op[2];rows[d]={};live.add(d);now+=1;lifetimes+=1;peak=max(peak,now)
        elif typ=="CLEAR":
            need(d>=n and d in live and loc[d]==op[2],f"CLEAR owner/chart at {t}")
            live.remove(d);loc[d]=None;rows[d]={};now-=1
        elif typ=="MOVE":
            src,dst,owned=op[2:]
            need(d in live and loc[d]==src and type(owned) is bool and owned==(d>=n),f"MOVE source/owner at {t}")
            need(src!=dst and (spaces[src] < spaces[dst] or spaces[dst] < spaces[src]),f"MOVE charts not strictly nested at {t}")
            r=abs(len(frames[src])-len(frames[dst]));need(r>0,f"zero-rank MOVE at {t}")
            moves[r]+=1;(om if owned else rm)[r]+=1;loc[d]=dst
        elif typ=="SCALE":
            c=q(op[2]);need(c and d in live and loc[d]==op[3],f"SCALE chart at {t}")
            rows[d]={i:c*v for i,v in rows[d].items() if c*v}
        else:
            need(typ in ("ADD","COPY"),f"unexpected opcode at {t}: {typ}")
            s,c,ch=op[2],q(op[3]),op[4]
            need(s in live and d in live and d!=s and loc[d]==loc[s]==ch,f"ADD/COPY cochart at {t}")
            if typ=="COPY": need(not rows[d],f"COPY target nonzero at {t}")
            rows[d]=plus(rows[d],rows[s],c)
    if limit is None:
        need(live==set(range(n)) and now==0 and all(loc[i] is not None for i in range(n)),"terminal public/owned state")
    elif not allow_open:
        need(live==set(range(n)) and now==0,"prefix owned state")
    return rows,loc,counts,moves,om,rm,peak,lifetimes,live,snapshots

def union_find_partition(parent, dual_inputs):
    n=parent["public"]; program=parent["program"]
    uf=list(range(n));current={i:i for i in range(n)};event_nodes=[]
    def find(x):
        while uf[x]!=x:
            uf[x]=uf[uf[x]];x=uf[x]
        return x
    def join(x,y):
        x,y=find(x),find(y)
        if x!=y: uf[y]=x
    for t,op in enumerate(program):
        typ,d=op[:2]
        if typ=="INIT":
            need(d not in current,f"lifetime overlap at {t}")
            node=len(uf);uf.append(node);current[d]=node
        node=current[d];event_nodes.append(node)
        if typ in ("ADD","COPY"): join(node,current[op[2]])
        if typ=="CLEAR": del current[d]
    tags={}
    for i in range(n):tags.setdefault(find(i),set()).add("D" if i in dual_inputs else "P")
    need(all(len(v)<=1 for v in tags.values()),"one owned component mixes primal and dual inputs")
    colors=[]
    for node in event_nodes:
        ts=tags.get(find(node),set())
        need(len(ts)<=1,"event component mixes banks")
        colors.append(next(iter(ts),"P"))
    return [i for i,c in enumerate(colors) if c=="P"],[i for i,c in enumerate(colors) if c=="D"]

def root9(n):
    bits=[i for i in range(9) if n>>i&1]
    if len(bits)==3:return tuple(2 if i in bits else -1 for i in range(9))
    need(len(bits)==7,f"unexpected E8 normal {n}")
    p,r=[i for i in range(9) if not n>>i&1]
    return tuple(3*(int(i==p)-int(i==r)) for i in range(9))

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def source_data(native):
    host={native["live"][k]:(x,y) for k,x,y in zip(native["hosted"]["Dports"],native["hosted"]["X2"],native["hosted"]["Y2"])}
    H=list(host)
    roots={i:root9(native["frames"][native["initial"][i]][0]) for i in native["live"]}
    gram=lambda i,j:F(dot(roots[i],roots[j]),18)
    return host,H,roots,gram

def mode_rows(word, roles, host, H, gram):
    pc=word["packet_cycles"];m=pc["modes"]
    modes=[];expected_json=[]
    J=set(pc["selected_coordinate_strip_ports"])
    for mode in pc["upward_mode_basis"][:m]:
        a=mode["root"];b=mode["reference_root"];c=q(mode["coefficient"])
        row={j:gram(a,j)-(c*gram(b,j) if b is not None else 0) for j in H}
        modes.append(row)
        expected={str(roles[host[j][1]]):str(v) for j,v in row.items() if j not in J and v}
        expected_json.append(expected)
    return modes, expected_json

def reconstruct_cycle(parent, word, native, base_rows, base_loc, roles, host, H, gram):
    pc=word["packet_cycles"];m=pc["modes"]
    primal,dual=union_find_partition(parent,{roles[r] for pair in host.values() for r in pair})
    need(primal==pc["primal_parent_events"] and dual==pc["dual_parent_events"],"independent bank chronology partition")
    need(len(primal)==3061 and len(dual)==2181 and len(parent["program"])==5242,"parent bank event census")
    need(all(a<b for a,b in zip(primal,primal[1:])) and all(a<b for a,b in zip(dual,dual[1:])),"retimed subword order")
    modes,expected_observations=mode_rows(word,roles,host,H,gram)
    need(pc["observations"]==expected_observations,"published observation coefficients differ from root-derived rows")
    events={e["old_clear"]:e for e in pc["events"]}
    need(len(events)==m and len(set(events))==m,"one replaced clear per cycle")
    caches=[e["cache"] for e in pc["events"]]
    need(len(set(caches))==m and caches==list(range(400+parent["owned_fields"],400+parent["owned_fields"]+m)),"fresh cache lifetime IDs")
    by_clear={}
    encoders={}
    for old,e in events.items():
        op=parent["program"][old]
        need(op[0]=="CLEAR" and op[2]==3,"cycle replaces the actual forward packet clear")
        field=op[1]
        init=max(t for t in range(old) if parent["program"][t][:2]==["INIT",field])
        down=next(t for t in range(init+1,old) if parent["program"][t][0]=="MOVE" and parent["program"][t][1]==field and parent["program"][t][2:4]==[127,3])
        encoder=parent["program"][init+1:down]
        need(all(z[0]=="ADD" and z[1]==field and z[4]==127 for z in encoder),"original forward encoder is literal Hub arithmetic")
        need(encoder==e["true_original_forward_encoder"],"retimed packet uses authentic original forward coefficients")
        encoders[old]=(field,encoder,down)
        by_clear[old]=e

    consumer=parent["consumer"]
    clear_to_port={life["end"]-1:life["port"] for life in consumer["lifetimes"]}
    need(len(clear_to_port)==31 and set(clear_to_port.values())==set(consumer["selected_return_ports"]),"all31 old D returns identified")
    primal_by_old=set(primal);dual_by_old=set(dual)
    need(set(events)<=primal_by_old,"only primal forward packet clears are replaced")
    core=[];event_bounds={};clear_positions={};trace_pre=[]
    for old in primal:
        op=parent["program"][old]
        if old not in by_clear:
            core.append(list(op));continue
        e=by_clear[old];mode=e["mode"];packet,encoder,down=encoders[old]
        begin=len(core)
        # Re-evaluate the already-emitted prefix to check genuine source access
        # and original input chronology at this packet's actual birth chart.
        pref=dict(word);pref["program"]=core;pref["owned_fields"]=word["owned_fields"]
        rows,loc,*_=replay(pref,400,limit=len(core),allow_open=True)
        need(loc[packet]==3,"forward packet remains at its real source chart before return")
        for j in H:
            dinput=roles[host[j][1]]
            need(loc[dinput]==3 and rows[dinput]=={dinput:F(1)},"unmodified D input has not reached the real chart-3 packet read")
        need(all(loc[i]==127 for i in range(104)),"all104 authentic first-X current inputs are at Hub before packet reuse")
        for z in encoder:
            need(loc[z[2]]==127,"authentic current first-X encoder source is at Hub when read")
        for j in H:
            v=modes[mode][j]
            if v:core.append(["ADD",packet,roles[host[j][1]],str(v),3])
        core.append(["MOVE",packet,3,127,True])
        for z in encoder:core.append(["ADD",packet,z[2],str(-q(z[3])),127])
        core.extend([["INIT",e["cache"],127],["ADD",e["cache"],packet,"1",127],["CLEAR",packet,127]])
        event_bounds[mode] = {"begin":begin,"end":len(core)}
    need([event_bounds[k] for k in range(m)]==[{"begin":e["begin"],"end":e["end"]} for e in pc["events"]],"retimed packet insertion locations")

    for old in dual:
        op=parent["program"][old]
        if old in clear_to_port:
            j=clear_to_port[old]
            need(op==["CLEAR",400,127],"real D return temporary clears at Hub")
            # Check exact source and chart just before this return is consumed.
            pref=dict(word);pref["program"]=core;pref["owned_fields"]=word["owned_fields"]
            rows,loc,*_=replay(pref,400,limit=len(core),allow_open=True)
            need(rows[400]=={roles[host[j][1]]:F(1)} and loc[400]==127,"actual returned D_j temporary is present at Hub before strip")
            for k in range(m):
                v=modes[k][j]
                if v:core.append(["ADD",caches[k],400,str(-v),127])
        clear_positions[old]=len(core)
        core.append(list(op))
    need(len(core)==pc["consumer_begin"],"cycle core boundary")

    # The mixed caches have exactly the root-derived gamma*(I-E_J E_J^T)d rows.
    prefix=dict(word);prefix["program"]=core
    rows,loc,counts,moves,om,rm,peak,lives,active,_=replay(prefix,400,limit=len(core),allow_open=True)
    need(active==set(range(400))|set(caches),"only new packet caches remain live at consumer boundary")
    for k,cache in enumerate(caches):
        need(loc[cache]==127,"mixed packet cache retained at Hub")
        expected={roles[host[j][1]]:v for j,v in modes[k].items() if j not in set(pc["selected_coordinate_strip_ports"]) and v}
        need(rows[cache]==expected,f"actual cache row {k} equals selected-coordinate-stripped Gamma*d")
    need(all(rows[i]==base_rows[i] and loc[i]==base_loc[i] for i in range(400)),"400 public current Q rows are unchanged before the new consumer")

    # Recompute the consumer C=M[:,T]*(N_T)^-1 from actual current rows.
    bidx={j:roles[host[j][0]] for j in H};didx={j:roles[host[j][1]] for j in H}
    M=[[F(i==j)+base_rows[bidx[i]].get(didx[j],F(0)) for j in H] for i in H]
    N=[ [rows[c].get(didx[j],F(0)) for j in H] for c in caches]
    need(rank(M)==58,"actual parent current residual rank58")
    need(rank(N)==m,"actual independent packet observation rows")
    useful=min(m,7);Nuse=N[:useful]
    need(rank(M+Nuse)==58 and rank(M+N)==(59 if m==8 else 58),"correct useful/nuisance observation quotient rank")
    pivots=pc["pivot_ports"];tidx=[H.index(j) for j in pivots]
    need(len(tidx)==useful and len(set(tidx))==useful,"consumer pivot ports")
    NT=[[Nuse[k][j] for j in tidx] for k in range(useful)]
    NTi=inverse(NT)
    C=[[sum(M[i][tidx[z]]*NTi[z][k] for z in range(useful)) for k in range(useful)] for i in range(len(H))]
    published=[[q(x) for x in row] for row in pc["consumer_coefficients"]]
    need(C==published,"consumer shear equals exact pivot solution")
    residual=[[M[i][j]-sum(C[i][k]*Nuse[k][j] for k in range(useful)) for j in range(len(H))] for i in range(len(H))]
    need(rank(residual)==58-useful,"exact B residual rank drop")
    old_complete={i for i,row in enumerate(M) if not any(row)}
    new_complete={i for i,row in enumerate(residual) if not any(row)}
    need(old_complete<=new_complete,"previously completed B rows remain completed")

    finish=[]
    for i,port in enumerate(H):
        for k,c in enumerate(C[i]):
            if c:finish.append(["ADD",bidx[port],caches[k],str(-c),127])
    finish.extend([["CLEAR",c,127] for c in caches])
    expected_program=core+finish
    need(word["program"]==expected_program,"entire cycle word equals independently reconstructed timed program")
    need(pc["consumer_begin"]==len(core),"reported consumer starts after all old D returns")
    need(word["source_role_map"]==parent["source_role_map"] and word["initial"]==parent["initial"] and word["frames"]==parent["frames"],"cycle preserves 400-source interface")
    return {"core":core,"M":M,"N":N,"C":C,"residual":residual,"expected_observations":expected_observations,
            "cache_ids":caches,"event_bounds":event_bounds,"useful":useful,"rank_before":rank(M),
            "rank_after":rank(residual),"stack_rank":rank(M+N),"clear_to_port":clear_to_port,
            "old_complete_count":len(old_complete),"new_complete_count":len(new_complete),"newly_completed":sorted(new_complete-old_complete)}

def exact_power_bounds(r, precision=100):
    den=1<<precision;target=r**199*den**200;lo=0;hi=r*den+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=target:lo=mid
        else:hi=mid
    need(lo**200<=target<(lo+1)**200,"integer 200th root bracket")
    up=lo if lo**200==target else lo+1
    return F(lo,den),F(up,den)

def signed_moment(profile):
    lo=hi=F(0)
    for r,c in profile.items():
        a,b=exact_power_bounds(int(r))
        if c>=0:lo+=c*a;hi+=c*b
        else:lo+=c*b;hi+=c*a
    return lo,hi

def verify_map(root, parent, maps, cycle_words):
    recipe=maps["recipe"]
    need(maps["source"]==3 and maps["target"]==127 and maps["rank"]==9,"3-to-127 map metadata")
    need(parent["frames"][3]==[] and parent["frames"][127]==[1<<i for i in range(9)],"3 and 127 are the empty and full charts")
    oldpairs={(o[2],o[3]) for o in parent["program"] if o[0]=="MOVE"}
    for w in cycle_words:
        newpairs={(o[2],o[3]) for o in w["program"] if o[0]=="MOVE"}-oldpairs
        need(newpairs=={(3,127)},"only chart pair introduced is 3->127")
    # Direct local implementation of monomial, C-gate and full-frame operators.
    def parity(x):return x.bit_count()&1
    def transpose(rows,n=9):return tuple(sum(((rows[j]>>i)&1)<<j for j in range(n)) for i in range(n))
    def binary_inverse(rows,n=9):
        a=[rows[i]|(1<<(n+i)) for i in range(n)]
        for j in range(n):
            z=next((i for i in range(j,n) if a[i]>>j&1),None);need(z is not None,"map invertible permutation")
            a[j],a[z]=a[z],a[j]
            for i in range(n):
                if i!=j and a[i]>>j&1:a[i]^=a[j]
        return tuple(r>>n for r in a)
    def mv(rows,x):return sum(parity(r&x)<<i for i,r in enumerate(rows))
    def mono(record):
        return [("D",tuple(record["quadratic_rows"]),tuple(record["linear_Z4"])),
                ("P",tuple(record["matrix_rows"])),("X",record["offset"]),("phase",record["phase"])]
    def circuit(rec):
        out=mono(rec["right"])
        out += [("C",1<<i,1) for i in range(rec["rank"])]
        out += mono(rec["left"])
        return out
    def tableau(gates):
        out=[(1<<i,0,0) for i in range(9)]+[(0,1<<i,0) for i in range(9)]
        for gate in gates:
            new=[]
            for x,z,ph in out:
                tag=gate[0]
                if tag=="P":
                    G=gate[1];Gi=binary_inverse(G);GinvT=transpose(Gi)
                    x,z=mv(G,x),mv(GinvT,z)
                elif tag=="X":ph+=2*parity(z&gate[1])
                elif tag=="C":
                    _,qv,sgn=gate
                    if parity(z&qv):x^=qv;ph+=3*sgn
                elif tag=="D":
                    _,Q,a=gate
                    ph+=sum(a[i] for i in range(9) if x>>i&1)
                    ph+=2*sum(parity((Q[i]>>(i+1))&(x>>(i+1))) for i in range(9) if x>>i&1)
                    z^=mv(Q,x)
                else:need(tag=="phase","map tableau tag")
                new.append((x,z,ph%4))
            out=new
        return tuple(out)
    def mul_i(pair,power):
        a,b=pair
        return [(a,b),(-b,a),(-a,-b),(b,-a)][power%4]
    def zero_state(gates):
        state={0:(F(1),F(0))}
        for gate in gates:
            tag=gate[0];out={}
            if tag=="C":
                _,direction,sign=gate
                for x,(a,b) in state.items():
                    for dest,pair in ((x,(a-sign*b,b+sign*a)),(x^direction,(a+sign*b,b-sign*a))):
                        old=out.get(dest,(F(0),F(0)))
                        out[dest]=(old[0]+pair[0]/2,old[1]+pair[1]/2)
            else:
                for x,pair in state.items():
                    if tag=="P":dest=mv(gate[1],x)
                    elif tag=="X":dest=x^gate[1]
                    else:dest=x
                    if tag=="D":
                        Q,a=gate[1:];power=(sum(a[i] for i in range(9) if x>>i&1)+2*sum(parity((Q[i]>>(i+1))&(x>>(i+1))) for i in range(9) if x>>i&1))%4
                        pair=mul_i(pair,power)
                    elif tag=="phase":pair=mul_i(pair,gate[1])
                    need(dest not in out,"monomial map injective");out[dest]=pair
            state={x:v for x,v in out.items() if v!=(0,0)}
        return state
    actual=circuit(recipe)
    # Source chart 3 is the empty frame; target chart 127 is the full rank-nine
    # frame, whose exact canonical transport is nine commuting C gates.
    expected=[("C",1<<i,1) for i in range(9)]
    need(tableau(actual)==tableau(expected),"map Pauli generator action")
    need(zero_state(actual)==zero_state(expected),"map exact global phase on |0>")
    bad=json.loads(json.dumps(recipe));bad["right"]["phase"]=(bad["right"]["phase"]+1)%4
    badc=circuit(bad)
    need(tableau(badc)==tableau(expected) and zero_state(badc)!=zero_state(expected),"wrong global phase control is rejected")
    return {"new_pair": [3,127],"rank":9,"pauli_generators_checked":18,"exact_zero_state_support":len(zero_state(actual)),
            "global_phase_match":True,"wrong_phase_control_rejected":True}

def main(args):
    package=args.package;repo=args.repo
    manifest_path=package/"MANIFEST.json";manifest_bytes=manifest_path.read_bytes()
    need(sha(manifest_bytes)=="1acafa8b51766dafff868959026829e41b4c1682c1f0b98fe0366ae719d8caea","author manifest pin")
    manifest=json.loads(manifest_bytes)
    for rel,expected in manifest["artifacts"].items():
        need(sha((package/rel).read_bytes())==expected,f"frozen artifact hash {rel}")
    native_path=repo/"research/shared-wire-split-composition/data/final.json.gz"
    full_path=repo/"research/shared-wire-split-composition/FULL-RESULT.json"
    need(sha(native_path.read_bytes())==PINS["native"] and sha(full_path.read_bytes())==PINS["full"],"native/full pins")
    native=read_gz(native_path);full=json.loads(full_path.read_bytes())
    parent=read_gz(package/"source-evidence/rail-consumer.json.gz")
    need(sha((package/"source-evidence/rail-consumer.json.gz").read_bytes())==PINS["rail"],"parent Q pin")
    need(parent["public"]==400 and parent["source_role_map"],"parent 400-source rail")
    roles={int(k):int(v) for k,v in parent["source_role_map"].items()};reverse={v:k for k,v in roles.items()}
    need(len(roles)==400 and set(reverse)==set(range(400)),"400-source role bijection")
    host,H,roots,gram=source_data(native)
    need(len(H)==96,"hosted 96-port set")
    dinputs={j:roles[host[j][1]] for j in H};binputs={j:roles[host[j][0]] for j in H}
    # The 192 dual inputs are exactly actual hosted X2/Y2 coordinates.
    dual_inputs={roles[v] for pair in host.values() for v in pair}
    need(len(dual_inputs)==192,"192 actual hosted dual inputs")

    base_rows,base_loc,base_counts,base_moves,base_om,base_rm,base_peak,base_lives,_,_=replay(parent,400)
    for j in H:
        di=dinputs[j];bi=binputs[j]
        need(base_rows[di]=={di:F(1)} and base_loc[di]==native["final"][host[j][1]],"all hosted D fields restored unchanged")
        need(base_loc[bi]==127,"all current B rows at actual Hub")
    need(all(base_rows[binputs[j]].get(binputs[k],F(0))==F(j==k) for j in H for k in H),"current B identity block")

    results={};cycle_words=[];one_matrix=None
    for name,modes in (("one",1),("eight",8)):
        word=read_gz(package/name/"rail-cycle.json.gz");receipt=json.loads((package/name/"RESULT.json").read_bytes())
        need(sha((package/name/"rail-cycle.json.gz").read_bytes())==receipt["word_sha256"],f"{name} word hash")
        need(receipt["status"]=="PASS_ACTUAL_COTANGENT_PACKET_CYCLE" and receipt["cycles"]==modes,"cycle receipt")
        need(word["packet_cycles"]["modes"]==modes and word["owned_fields"]==parent["owned_fields"]+modes,"cycle count/owned space")
        need(word["packet_cycles"]["source_rail_sha256"]==PINS["rail"],"cycle parent source pin")
        constructed=reconstruct_cycle(parent,word,native,base_rows,base_loc,roles,host,H,gram)
        if name=="one":one_matrix=constructed["M"]
        rows,loc,counts,moves,om,rm,peak,lives,_,_=replay(word,400)
        need(loc[:400]==base_loc[:400] and len(rows)==400+word["owned_fields"],"all 400 final charts retained")
        # Verify exact all-400 map: only hosted B rows shear by C times actual caches.
        for i in range(400):
            expected=base_rows[i].copy()
            if i in binputs.values():
                j=next(j for j in H if binputs[j]==i)
                for k,c in enumerate(constructed["C"][H.index(j)]):
                    expected=plus(expected,{idx:v for idx,v in zip([dinputs[h] for h in H],constructed["N"][k]) if v},-c)
            need(rows[i]==expected,f"{name} exact400-input public row {i}")
        expected_counts=Counter(receipt["bill"]["counts"])
        need(counts==expected_counts,f"{name} opcode count receipt")
        expected_moves=Counter({int(k):v for k,v in receipt["bill"]["moves"].items()})
        need(moves==expected_moves,f"{name} rank MOVE receipt")
        delta_counts={k:counts.get(k,0)-base_counts.get(k,0) for k in set(counts)|set(base_counts)}
        delta_counts={k:v for k,v in delta_counts.items() if v}
        need(delta_counts=={k:int(v) for k,v in receipt["ordinary_increment"].items() if v},f"{name} ordinary increment")
        delta_moves={r:moves.get(r,0)-base_moves.get(r,0) for r in set(moves)|set(base_moves)}
        delta_moves={r:v for r,v in delta_moves.items() if v}
        need(delta_moves=={int(k):v for k,v in receipt["new_paid_move_profile"].items() if v},f"{name} new paid route profile")
        denominators=sorted({q(op[3] if op[0] in ("ADD","COPY") else op[2]).denominator
                             for op in word["program"] if op[0] in ("ADD","COPY","SCALE")})
        need(denominators==receipt["scalar_denominators"],f"{name} exact scalar denominator census")
        need(peak==receipt["bill"]["peak"] and lives==receipt["bill"]["lifetimes"],f"{name} owned lifetimes/peak")
        need(receipt["hosted_reverse_residual_rank"]==constructed["rank_after"],f"{name} rank receipt")
        need(receipt["forward_rows_unchanged"] and receipt["eight_coupled_entry_calls_retained"],f"{name} stated retained duties")
        need(receipt["upward_Gram_ports"]==word["packet_cycles"]["upward_Gram_ports"],f"{name} gamma ports")
        cycle_words.append(word)
        results[name]={"status":"PASS","cycles":modes,"operations":len(word["program"]),"moves":sum(moves.values()),
                       "rank_before":constructed["rank_before"],"rank_after":constructed["rank_after"],
                       "previously_completed_rows":constructed["old_complete_count"],"completed_rows_after":constructed["new_complete_count"],
                       "newly_completed_rows":constructed["newly_completed"],
                       "observation_rank":rank(constructed["N"]),"stack_rank":constructed["stack_rank"],
                       "new_return_calls":dict(Counter({int(k):v for k,v in receipt["new_paid_move_profile"].items()})),
                       "owned_lifetimes":lives,"peak":peak,"forward_rows_unchanged":True,
                       "bank_retiming_events":{"primal":3061,"dual":2181},"cache_formula_verified":True}

    # Negative control: without bank retiming, the first real gamma source is
    # already at a different chart when the old packet would be re-used.
    first_word=cycle_words[0];first_pc=first_word["packet_cycles"]
    first_mode_rows,_=mode_rows(first_word,roles,host,H,gram)
    first_event=first_pc["events"][0];old_clear=first_event["old_clear"]
    old_packet=parent["program"][old_clear][1]
    strips=set(first_pc["selected_coordinate_strip_ports"])
    departed=next(j for j in H if first_mode_rows[0][j] and j not in strips)
    original_prefix=dict(parent);original_prefix["program"]=parent["program"][:old_clear]
    pre_rows,pre_loc,*_=replay(original_prefix,400,limit=old_clear,allow_open=True)
    source_d=roles[host[departed][1]]
    need(pre_loc[source_d]!=3,"unretimed chronology control has already departed chart 3")
    illegal=dict(parent);illegal["program"]=parent["program"][:old_clear]+[["ADD",old_packet,source_d,str(first_mode_rows[0][departed]),3]]
    rejected=False
    try:
        replay(illegal,400,limit=len(illegal["program"]),allow_open=True)
    except ValueError:
        rejected=True
    need(rejected,"unretimed first packet reuse fails actual D cochart access")

    # Local movement-price negative control: seven real original-coordinate
    # returns remove seven successive coloops of the actual M at rank one.
    # All seven facet->Hub chart pairs are already present in the cyclic source.
    cyclic_path=repo/"research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz"
    need(sha(cyclic_path.read_bytes())==PINS["cyclic"],"cyclic route source pin")
    cyclic=read_gz(cyclic_path);cyclic_pairs={(op[2],op[3]) for op in cyclic["program"] if op[0]=="MOVE"}
    cheap_ports=[84,91,92,94,95,98,99];cheap_ranks=[]
    cheap_matrix=[row.copy() for row in one_matrix]
    for port in cheap_ports:
        col=H.index(port)
        facet=native["final"][host[port][1]]
        need((facet,127) in cyclic_pairs,"dominating rank-one D return has inherited real chart map")
        for i in range(len(H)):cheap_matrix[i][col]=F(0)
        cheap_ranks.append(rank(cheap_matrix))
    need(cheap_ranks==[57,56,55,54,53,52,51],"seven actual rank-one coordinate returns match eight-cycle rank gain")

    # Independently construct the one-cycle fixed-m=3 word and replay all 2280
    # input basis columns against its separately composed common/private map.
    qword=cycle_words[0];copies=3;public=1480+400*(copies-1)
    need(public==2280,"m3 public arity")
    ops=[];blocks=[]
    for bankidx in range(copies-1):
        bank={i:1480+400*bankidx+i for i in range(400)};start=len(ops)
        ops += [["ADD",bank[i],reverse[i],"-1",qword["initial"][i]] for i in range(400)]
        for op in qword["program"]:
            z=list(op);z[1]=bank[z[1]] if z[1]<400 else public+z[1]-400
            if z[0] in ("ADD","COPY"):z[2]=bank[z[2]] if z[2]<400 else public+z[2]-400
            ops.append(z)
        blocks.append({"copy":bankidx+1,"start":start,"stop":len(ops)})
    common_start=len(ops)
    for op in native["program"]:
        z=list(op);z[1]=z[1] if z[1]<1480 else public+z[1]-1480
        if z[0] in ("ADD","COPY"):z[2]=z[2] if z[2]<1480 else public+z[2]-1480
        ops.append(z)
    common_end=len(ops)
    for bankidx in range(copies-1):
        for i in range(400):ops.append(["ADD",1480+400*bankidx+i,reverse[i],"1",native["final"][reverse[i]]])
    composed=read_gz(package/"one-m3/WORD.json.gz");m3receipt=json.loads((package/"one-m3/RESULT.json").read_bytes())
    need(composed["program"]==ops and composed["private_blocks"]==blocks and composed["common_block"]==[common_start,common_end],"literal one-cycle m3 composition")
    need(composed["initial"]==native["initial"]+qword["initial"]*(copies-1),"m3 common/private initial chart interface")
    need(composed["copies"]==3 and composed["public"]==public and composed["source_sha256"]==PINS["native"],"m3 metadata")
    need(composed["rail_sha256"]==sha((package/"one/rail-cycle.json.gz").read_bytes()),"m3 exact one-cycle parent pin")
    full_rows,full_loc,full_counts,full_moves,full_om,full_rm,full_peak,full_lives,_,_=replay(composed,public)
    native_rows,native_loc,native_counts,native_moves,_,_,native_peak,native_lives,_,_=replay(native,1480)
    qrows,qloc,*_=replay(qword,400)
    need(all(full_rows[i]==native_rows[i] and full_loc[i]==native_loc[i] for i in range(1480)),"m3 all common rows equal native W")
    for bankidx in range(copies-1):
        off=1480+400*bankidx
        for i in range(400):
            target=native_rows[reverse[i]].copy()
            for k,c in qrows[i].items():
                target=plus(target,{off+k:F(1)},c)
                target=plus(target,{reverse[k]:F(1)},-c)
            need(full_rows[off+i]==target,f"m3 all2280 exact private row bank{bankidx}, output{i}")
            need(full_loc[off+i]==qloc[i]==native["final"][reverse[i]],"m3 private endpoint chart")
    need(len(ops)==83635 and full_counts["ADD"]==70256 and full_moves[9]==18 and sum(full_moves.values())==7992,"m3 full operation invoice")
    need(full_lives==860 and full_peak==43 and full_counts["INIT"]==full_counts["CLEAR"]==860,"m3 owned lifetime invoice")
    need(full_counts["SCALE"]==3666 and full_counts["COPY"]==1,"m3 nonmovement counts")

    # Recompute complete fixed-m=3 caller profiles from the actual one-cycle Q.
    T={int(k):int(v) for k,v in full["invoice"]["T"].items()}
    P={int(k):int(v) for k,v in full["invoice"]["P"].items()}
    Nprof={int(k):int(v) for k,v in full["native"]["paid"].items()}
    Hprof={int(k):int(v) for k,v in full["native"]["helpers"].items()}
    R={1:990,2:360,3:105,4:112,5:133,6:8,7:2}
    _,_,_,Qprof,_,_,_,_,_,_=replay(qword,400)
    Qprof=dict(Qprof)
    ranks=set(T)|set(P)|set(Nprof)|set(Hprof)|set(R)|set(Qprof)
    G={r:Nprof.get(r,0)-R.get(r,0) for r in ranks}
    Tm={r:3*T.get(r,0)-36*Hprof.get(r,0) for r in ranks}
    Pm={r:3*P.get(r,0)-36*G.get(r,0)+36*(Qprof.get(r,0)-R.get(r,0)) for r in ranks}
    need({r:v for r,v in Tm.items() if v}=={int(k):v for k,v in m3receipt["T"].items()},"independent full m3 target profile")
    need({r:v for r,v in Pm.items() if v}=={int(k):v for k,v in m3receipt["P"].items()},"independent full m3 paid profile")
    signed={r:Tm[r]-Pm[r] for r in ranks}
    mlo,mhi=signed_moment(signed);perlo,perhi=mlo/36,mhi/36
    rlo,rhi=map(F,m3receipt["per_rail_moment_bounds"])
    need(rlo<=perlo<=perhi<=rhi and perlo>0,"exact m3 complete caller moment bracket positive")
    need(sum(Tm.values())==31296 and sum(Pm.values())==155952,"m3 caller target/paid position totals")
    need(sum(r*signed[r] for r in ranks)==4056,"m3 moment rank surplus")

    maps=json.loads((package/"CHART-MAPS.json").read_bytes())
    map_result=verify_map(repo,parent,maps,cycle_words)
    output={"status":"PASS_INDEPENDENT_COTANGENT_PACKET_REVIEW","author_manifest_sha256":sha(manifest_bytes),
            "native_sha256":PINS["native"],"full_caller_sha256":PINS["full"],"parent_rail_sha256":PINS["rail"],
            "cycles":results,"one_cycle_m3":{"status":"PASS","input_directions":2280,"operations":len(ops),
                "moves":sum(full_moves.values()),"owned_lifetimes":full_lives,"peak":full_peak,
                "rank_surplus":sum(r*signed[r] for r in ranks),"target_positions":sum(Tm.values()),"paid_positions":sum(Pm.values()),
                "per_rail_moment_bounds":[str(perlo),str(perhi)],"all2280_rows_checked":True},
            "new_chart_map":map_result,
            "unretimed_negative_control":{"first_old_clear":old_clear,"first_required_D_source":source_d,
                "actual_source_chart":pre_loc[source_d],"required_source_chart":3,"rejected":rejected},
            "locally_dominated_coordinate_returns":{"ports":cheap_ports,"rank_sequence":cheap_ranks,
                "all_facet_to_hub_pairs_inherited":True,"movement_price":7},
            "scope":"Actual source packet reuse and mixed current-row consumption only. No full forward off-diagonal acquisition, no absorption of coupled eight entry calls, and no supplier or kappa. Condensed-gate source rank/general algebra not re-reviewed here."}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--repo",type=Path,required=True);p.add_argument("--package",type=Path,required=True);p.add_argument("--output",type=Path,required=True);main(p.parse_args())
