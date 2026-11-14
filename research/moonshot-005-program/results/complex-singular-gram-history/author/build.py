#!/usr/bin/env python3
"""Paid singular X capture with the displaced full Gram mode cached in place.

The source is rebuilt from the pinned omitted-line interface, not composed with
the proper-born-clique word. Dirty owned retirement is explicitly retained.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PINS={
 'native':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
 'seed':'6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc',
 'replay':'045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e',
 'codec':'4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297'}
FRAMES={'hybrid':[7,25,42,52,268,274,289,319]}
# The all-native variant uses authenticated port indices; its normal list is
# recovered from the pinned source.
NATIVE_PORT_FRAME=[26,33,40,47,52,57,72,82]

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path,name):
    raw=path.read_bytes();need(sha(raw)==PINS[name],name+' pin');return json.loads(gzip.decompress(raw))
def module(path,name):
    need(sha(path.read_bytes())==PINS[name],name+' pin')
    spec=importlib.util.spec_from_file_location('singular_gram_'+name,path)
    obj=importlib.util.module_from_spec(spec);sys.modules[spec.name]=obj;spec.loader.exec_module(obj);return obj
def clean(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):clean(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v)for v in value]
    return value
def determinant(rows):
    a=[[F(v)for v in row]for row in rows];answer=F(1)
    for i in range(len(a)):
        k=next((k for k in range(i,len(a))if a[k][i]),None)
        if k is None:return F(0)
        if k!=i:a[k],a[i]=a[i],a[k];answer=-answer
        pivot=a[i][i];answer*=pivot
        for j in range(i+1,len(a)):
            c=a[j][i]/pivot;a[j]=[x-c*y for x,y in zip(a[j],a[i])]
    return answer

def main(args):
    n=read(args.native,'native');seed=read(args.seed,'seed')
    e=module(args.engine,'replay');codec=module(args.codec,'codec')
    ports=n['live'];roles={int(k):v for k,v in seed['source_role_map'].items()}
    host={ports[i]:(roles[b],roles[d])for i,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2'])}
    X={h:roles[h]for h in ports};Y={h:roles[h+112]for h in ports};U=sorted(set(ports)-set(host))
    normals={h:n['frames'][n['initial'][h]][0]for h in ports};by_normal={v:h for h,v in normals.items()}
    roots={h:codec.root(normals[h])for h in ports}
    Z=FRAMES['hybrid']if args.variant=='hybrid'else[normals[h]for h in NATIVE_PORT_FRAME]
    rz=[codec.root(z)for z in Z]
    need(all(sum(x*y for x,y in zip(rz[i],rz[j]))==18*int(i==j)for i in range(8)for j in range(8)),'orthogonal real root basis')
    actual={i:by_normal[z]for i,z in enumerate(Z)if z in by_normal};J=sorted(actual.values());selected=set(J)
    g={h:[sum(x*y for x,y in zip(roots[h],r))/18 for r in rz]for h in ports}
    G={(h,j):sum(g[h][i]*g[j][i]for i in range(8))for h in ports for j in ports}
    need(all(g[h]==[F(i==k)for i in range(8)]for k,h in actual.items()),'each held native source enters exactly one mode')
    frames=copy.deepcopy(seed['frames']);where={frozenset(e.span(f)):i for i,f in enumerate(frames)}
    def chart(vectors):
        basis=codec.basis(vectors);space=frozenset(e.span(basis))
        if space not in where:where[space]=len(frames);frames.append(basis)
        return where[space]
    O=3;Hub=127;lines=[chart([z])for z in Z]
    facets={h:where[frozenset(e.span(n['frames'][n['final'][h+112]]))]for h in ports}
    need(all(lines[i]==seed['initial'][X[h]]for i,h in actual.items()),'actual native capture station is original X line')
    patterns={}
    for h in ports:
        if h in selected:continue
        pat=tuple(i for i,z in enumerate(g[h])if z);need(len(pat)==4,'all other ports use exactly four modes')
        patterns.setdefault(pat,[]).append(h)
    need(len(patterns)==14,'fourteen remaining actual mode classes')
    groups=[];codec_receipts=[]
    for pat,allh in sorted(patterns.items()):
        hs=sorted(h for h in allh if h in host);us=sorted(h for h in allh if h not in host);ys=hs+us
        A=[[g[h][i]for h in hs]for i in pat]
        _,piv=e.select([[x.numerator*pow(x.denominator,-1,e.PRIME)%e.PRIME for x in row]for row in A])
        need(len(piv)==4,'authentic hosted class has four independent codec pivots')
        MD=[[F(i==j)for j in range(len(hs))]for i in range(len(hs))]
        MY=[[F(i==j)for j in range(len(ys))]for i in range(len(ys))]
        for mode,p in zip(pat,piv):
            MD[p]=[g[h][mode]for h in hs]
            MY[p]=[g[h][mode]*(1 if h in host else F(1,2))for h in ys]
        C=chart(Z[i]for i in pat);need(len(frames[C])==3,'real class chart has binary dimension three')
        need(all(e.span(frames[C])<e.span(frames[facets[h]])for h in ys),'class chart lies properly in every receiver facet')
        groups.append({'modes':list(pat),'ports':ys,'hosted':hs,'coupled':us,'D_roles':[host[h][1]for h in hs],
                       'Y_roles':[Y[h]for h in ys],'pivots':piv,'C':C,'M_D':MD,'M_Y':MY,
                       'D_encoder':codec.encoder(MD),'Y_encoder':codec.encoder(MY),'markers':{}})
        codec_receipts.append({'ports':ys,'pivot_ports':[hs[i]for i in piv],
                               'D_determinant':determinant(MD),'Y_determinant':determinant(MY)})
    out=[];markers={};events={};captures_at={};q=408
    cache={i:408+k for k,i in enumerate(actual)}
    def emit(op):out.append(op);return len(out)-1
    def add(d,s,c,C):return emit(['ADD',d,s,str(c),C])
    def move(d,A,B,owned=False):
        if A!=B:return emit(['MOVE',d,A,B,owned])
        return None
    def bop(bank,operations,C):
        for ty,i,j,c in operations:
            emit(['ADD',bank[i],bank[j],str(c),C]if ty=='ADD'else['SCALE',bank[i],str(c),C])
    def mark(name):markers[name]=len(out);return len(out)

    # Exactly the retained coupled a=x-y entry; these eight transfers are paid.
    for h in U:
        emit(['INIT',400,O]);add(400,Y[h],1,O);move(400,O,seed['initial'][X[h]],True)
        add(X[h],400,-1,seed['initial'][X[h]]);emit(['CLEAR',400,seed['initial'][X[h]]])
    mark('entry_end')
    for i,L in enumerate(lines):emit(['INIT',400+i,L])
    for z in groups:
        bank=z['D_roles'];C=z['C'];enc=z['D_encoder'];bop(bank,enc,O)
        piv={p:mode for p,mode in zip(z['pivots'],z['modes'])}
        for j,d in enumerate(bank):
            if j in piv:
                i=piv[j];move(d,O,lines[i]);add(400+i,d,1,lines[i]);move(d,lines[i],C)
            else:move(d,O,C)
        bop(bank,[codec.inverse_op(o)for o in reversed(enc)],C);z['markers']['D_restored_at_C3']=len(out)
        for h,d in zip(z['hosted'],bank):move(d,C,facets[h])
    mark('old_reverse_modes_exclude_native_basis_D')
    events['new_reverse_reads']=[];events['new_reverse_sources']=[]
    for i,h in actual.items():
        if h not in host:continue
        b,d=host[h];L=lines[i]
        emit(['INIT',q,O]);events['new_reverse_sources'].append(add(q,d,1,O));move(q,O,L,True)
        events['new_reverse_reads'].append(add(b,q,-1,L));emit(['CLEAR',q,L]);move(d,O,facets[h])
    mark('all_D_original_at_final_facets')
    for h in ports:
        if h not in selected:move(X[h],seed['initial'][X[h]],Hub)
    for h,(b,d)in host.items():move(b,seed['initial'][b],Hub)
    mark('nonbasis_X_and_all_B_at_Hub')
    events['old_reverse_consumers']=[]
    for i,L in enumerate(lines):
        move(400+i,L,Hub,True)
        for h,(b,d)in host.items():
            if g[h][i]:events['old_reverse_consumers'].append(add(b,400+i,-g[h][i],Hub))
        emit(['CLEAR',400+i,Hub])
    mark('reverse_consumed')
    events['captures']=[];events['cache_copies']=[];events['X_restoration']=[];events['native_ground_reads']=[]
    for i,L in enumerate(lines):
        p=400+i;emit(['INIT',p,Hub])
        for h in ports:
            if h not in selected and g[h][i]:add(p,X[h],g[h][i],Hub)
        move(p,Hub,L,True)
        captures_at[i]={'before':len(out)}
        if i not in actual:continue
        h=actual[i]
        events['captures'].append(add(X[h],p,1,L))
        emit(['INIT',cache[i],L]);events['cache_copies'].append(add(cache[i],X[h],1,L))
        events['captures'].append(add(p,X[h],-1,L));captures_at[i]['after']=len(out)
        move(X[h],L,Hub)
        for j in ports:
            if j not in selected and g[j][i]:events['X_restoration'].append(add(X[h],X[j],-g[j][i],Hub))
        captures_at[i]['restored']=len(out)
        move(p,L,O,True);captures_at[i]['at_ground']=len(out)
        events['native_ground_reads'].append(add(Y[h],p,-1 if h in host else F(-1,2),O))
        emit(['CLEAR',p,O]);move(Y[h],O,facets[h])
    mark('all_full_Gram_modes_at_actual_lines_and_basis_Y_complete')
    events['old_forward_reads']=[]
    for z in groups:
        bank=z['Y_roles'];C=z['C'];enc=[codec.dual_op(o)for o in z['Y_encoder']];bop(bank,enc,O)
        piv={p:mode for p,mode in zip(z['pivots'],z['modes'])}
        for j,y in enumerate(bank):
            if j in piv:
                i=piv[j];move(y,O,lines[i]);source=cache[i]if i in actual else 400+i
                events['old_forward_reads'].append(add(y,source,1,lines[i]));move(y,lines[i],C)
            else:move(y,O,C)
        bop(bank,[codec.inverse_op(o)for o in reversed(enc)],C)
        for h,y in zip(z['ports'],bank):move(y,C,facets[h])
    for i,L in enumerate(lines):emit(['CLEAR',cache[i]if i in actual else 400+i,L])
    word={'schema':'moonshot-S012-singular-full-Gram-duty-history-v1','public':400,'owned_fields':8+len(J),
          'initial':seed['initial'],'frames':frames,'source_role_map':seed['source_role_map'],'program':out,
          'source_pins':PINS,'singular_history':{'variant':args.variant,'orthogonal_frame_normals':Z,
          'native_basis_by_mode':actual,'native_basis_ports':J,'hosted_native_basis':sorted(selected&set(host)),
          'coupled_native_basis':sorted(selected&set(U)),'lines':lines,'cache_roles':cache,'reverse_self_role':q,
          'groups':clean(groups),'codec_determinants':clean(codec_receipts),'markers':markers,'events':events,
          'capture_boundaries':captures_at,'dirty_owned_retirement_assumption_retained':True}}

    boundaries=set(markers.values())|{z['markers']['D_restored_at_C3']for z in groups}
    boundaries.update(t for phases in captures_at.values()for t in phases.values())
    observations={};retired=[]
    def capture(t,op,rows,locations):
        if t+1 in boundaries:observations[t+1]=(copy.deepcopy(rows),dict(locations))
        if t+1<len(out)and out[t+1][0]=='CLEAR':
            role=out[t+1][1];retired.append({'operation':t+1,'role':role,'chart':locations[role],
                                           'nonzero':bool(rows[role]),'input_support':len(rows[role])})
    rows,locations,bill=e.replay(word,out,capture)
    aa={h:{X[h]:F(1)}if h in host else{X[h]:F(1),Y[h]:F(-1)}for h in ports}
    full=[];partial=[]
    for i in range(8):
        f={};p={}
        for h in ports:
            f=e.add(f,aa[h],g[h][i])
            if h not in selected:p=e.add(p,aa[h],g[h][i])
        full.append(f);partial.append(p)
    want={j:{j:F(1)}for j in range(400)};wantloc={}
    L={(h,j):F(h==j)if h in selected else G[h,j]for h in ports for j in ports}
    for h in ports:
        want[X[h]]=aa[h];wantloc[X[h]]=Hub;wantloc[Y[h]]=facets[h]
        for j in ports:want[Y[h]]=e.add(want[Y[h]],aa[j],L[h,j]*(1 if h in host else F(1,2)))
    for h,(b,d)in host.items():
        wantloc[b]=Hub;wantloc[d]=facets[h]
        for j,(bj,dj)in host.items():want[b]=e.add(want[b],{dj:F(1)},-L[j,h])
    need(rows==want and locations==wantloc,'all400 exact public output rows and endpoint chart identifiers')
    need(e.exact_rank(rows.values())==400,'all400 independent public inputs retained')
    for z in groups:
        obs,_=observations[z['markers']['D_restored_at_C3']]
        need(all(obs[d]=={d:F(1)}for d in z['D_roles']),'actual original D restored at class C3')
    obs,loc=observations[markers['old_reverse_modes_exclude_native_basis_D']]
    for i in range(8):
        expect={d:g[h][i]for h,(b,d)in host.items()if h not in selected and g[h][i]}
        need(obs[400+i]==expect and loc[400+i]==lines[i],'old reverse duty exactly omits replaced rows at its actual line')
    obs,loc=observations[markers['all_D_original_at_final_facets']]
    need(all(obs[d]=={d:F(1)}and loc[d]==facets[h]for h,(b,d)in host.items()),'all96 original D restored at original endpoints')
    for i,phases in captures_at.items():
        obs,loc=observations[phases['before']]
        need(obs[400+i]==partial[i]and loc[400+i]==lines[i],'actual chronological partial source at line')
        if i not in actual:continue
        h=actual[i];obs,loc=observations[phases['after']]
        need(obs[X[h]]==full[i]and obs[cache[i]]==full[i]and obs[400+i]==e.add({},aa[h],-1),'singular cell old duty and new payload')
        need(loc[X[h]]==loc[cache[i]]==loc[400+i]==lines[i],'all singular cell fields genuinely cocharted')
        obs,loc=observations[phases['restored']]
        need(obs[X[h]]==aa[h]and loc[X[h]]==Hub,'original X restored by actual available nonbasis sources')
        obs,loc=observations[phases['at_ground']]
        need(obs[400+i]==e.add({},aa[h],-1)and loc[400+i]==O,'new payload really transported to ground')
    obs,loc=observations[markers['all_full_Gram_modes_at_actual_lines_and_basis_Y_complete']]
    for i in range(8):
        role=cache[i]if i in actual else 400+i
        need(obs[role]==full[i]and loc[role]==lines[i],'every displaced old Gram duty preserved at its decoder station')
    need(all(obs[Y[h]]==e.add({Y[h]:F(1)},aa[h],1 if h in host else F(1,2))and loc[Y[h]]==facets[h]for h in J),'native basis receiver targets completed')
    need(all(rows[b].get(dj,F(0))+rows[Y[j]].get(X[h],F(0))==0
             for h,(b,d)in host.items()for j,(bj,dj)in host.items()),'all9216 hosted transpose entries')
    reverse=e.exact_rank([e.add(rows[b],{b:F(1),d:F(-1)},F(-1))for h,(b,d)in host.items()])
    s=len(J);u=len(selected&set(U));d=2*s-u
    need(reverse==96-s+u,'exact hosted residual rank drop')
    history=e.exact_rank(partial+[aa[h]for h in J]);need(history==8+s,'actual global forward history rank')
    need(e.exact_rank(full)==8,'canonical full Gram mode rank remains eight')
    raw=Counter();owned=Counter()
    for op in out:
        if op[0]=='MOVE':(owned if op[4]else raw)[abs(len(frames[op[3]])-len(frames[op[2]]))]+=1
    need(raw==Counter({1:112,2:112,3:88-d,5:200-d,8:200+d}),'full private raw route histogram')
    need(owned==Counter({1:8+d,8:16}),'all entry, native capture, paired self and old mode movements')
    need(sum(r*c for r,c in raw.items())==3200 and sum(r*c for r,c in owned.items())==136+d,'unchanged raw rank mass and fully paid extra owned mass')
    scalars=[F(op[3]if op[0]=='ADD'else op[2])for op in out if op[0]in('ADD','SCALE')]
    need(all(x.denominator&(x.denominator-1)==0 for x in scalars),'every actual scalar is dyadic')
    det=determinant([[F(i==j)-sum(g[h][i]*g[h][j]for h in host)for j in range(8)]for i in range(8)])
    need(det==F(415068771,2),'basis-independent hosted I-Gram determinant')
    forward_current=sum(h!=j and bool(L[h,j])for h in ports for j in ports)
    need(forward_current==4992-48*s,'current-a forward offdiagonal debt')
    forward_original=sum(len(e.add(rows[Y[h]],{X[h]:F(1)if h in host else F(1,2),Y[h]:F(1)if h in host else F(1,2)},F(-1)))for h in ports)
    controls=[]
    choices={'omit_X_Hub_restoration':events['X_restoration'][0],
             'cache_partial_instead_of_full_Gram':events['cache_copies'][0],
             'wrong_singular_capture_sign':events['captures'][1],
             'wrong_native_ground_decoder':events['native_ground_reads'][0],
             'omit_paired_native_reverse_delivery':events['new_reverse_reads'][0],
             'wrong_old_reverse_consumer':events['old_reverse_consumers'][0]}
    for label,index in choices.items():
        bad=copy.deepcopy(word);op=bad['program'][index]
        if label=='cache_partial_instead_of_full_Gram':op[2]=400+next(iter(actual))
        elif label.startswith('omit_'):op[3]='0'
        else:op[3]=str(-F(op[3]))
        try:mr,ml,_=e.replay(bad,bad['program']);rejected=mr!=rows or ml!=locations
        except ValueError:rejected=True
        need(rejected,'negative control '+label);controls.append(label)
    payload=(json.dumps(clean(word),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    receipt={'status':'PASS_ACTUAL_SINGULAR_CAPTURE_WITH_PRESERVED_GRAM_DUTY','variant':args.variant,
             'orthogonal_frame_normals':Z,'native_basis_ports':J,'hosted_native_basis':sorted(selected&set(host)),
             'coupled_native_basis':sorted(selected&set(U)),'s':s,'u':u,'extra_owned_rank_one':d,
             'word_sha256':sha(blob),'payload_sha256':sha(payload),'source_pins':PINS,'source_bill':bill,
             'raw_histogram':dict(raw),'owned_histogram':dict(owned),'all400_input_rank':400,
             'all96_D_original_at_final_facets':True,'all_original_X_restored':True,
             'all_old_forward_Gram_modes_preserved_at_actual_lines':True,
             'old_reverse_modes_exactly_omit_native_basis_D':True,'selected_Y_completed':J,
             'hosted_transpose_entries_checked':9216,'forward_global_history_rank':history,
             'reverse_residual_rank':reverse,'hosted_I_minus_Gram_determinant':det,
             'current_a_forward_offdiagonal_coefficients':forward_current,'original_coordinate_forward_debt':forward_original,
             'owned_retirements':retired,'owned_erasure_assumption_retained':True,
             'codec_determinants':codec_receipts,'all_scalars_dyadic':True,'negative_controls':controls,
             'scope':'Actual partial paired source, extended by the stated linear identities to every field volume. No composition with the proper-born-clique word; no new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(clean(receipt),sort_keys=True,indent=2)+'\n')
    print(json.dumps(clean({key:receipt[key]for key in('status','variant','native_basis_ports','word_sha256','source_bill','raw_histogram','owned_histogram','forward_global_history_rank','reverse_residual_rank')}),sort_keys=True,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--codec',type=Path,required=True)
    p.add_argument('--variant',choices=('hybrid','native'),required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
