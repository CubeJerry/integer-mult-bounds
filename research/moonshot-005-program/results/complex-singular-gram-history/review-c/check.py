#!/usr/bin/env python3
"""Independent rational whole-source review; no author replay imported.

Reuses the previously independently authored root replay kernel, credited in
REVIEW.md. @CubeJerry with OpenAI assistance. Apache-2.0.
"""
import argparse, copy, gzip, hashlib, importlib.util, json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def rank(rows):
    basis = {}
    for original in rows:
        row = dict(original)
        for j in sorted(basis):
            if j in row:
                c = row[j]
                for k, value in basis[j].items():
                    v = row.get(k, F(0)) - c * value
                    if v: row[k] = v
                    else: row.pop(k, None)
        if row:
            j = min(row); c = row[j]
            basis[j] = {k: v / c for k, v in row.items()}
    return len(basis)

def determinant(matrix):
    a = [[F(v) for v in row] for row in matrix]; answer = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None: return F(0)
        if pivot != j: a[j], a[pivot] = a[pivot], a[j]; answer = -answer
        x = a[j][j]; answer *= x
        a[j] = [v/x for v in a[j]]
        for i in range(j+1, len(a)):
            c = a[i][j]
            a[i] = [v-c*w for v,w in zip(a[i], a[j])]
    return answer

def root_vector(bits):
    on = [i for i in range(9) if bits >> i & 1]
    if len(on) == 3: return [2 if i in on else -1 for i in range(9)]
    off = [i for i in range(9) if not (bits >> i & 1)]
    need(len(off) == 2, 'native real root type')
    return [3*(int(i == off[0])-int(i == off[1])) for i in range(9)]


from engine import replay, span, plus
from itertools import combinations

BASE = Path(__file__).resolve().parents[2]
AUTHOR = BASE/'worker-b/singular-gram-history'
REPO = BASE/'programme'
PINS = {
 'PROOF.md':'b444eb138ebeeffd1c46438012eca6f5038df88f555addad745e982df7475013',
 'dependencies/native.json.gz':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
 'dependencies/FULL-RESULT.json':'d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7',
 'output/hybrid/WORD.json.gz':'6a1bca25b99d5f13547a4132706219e4504ef202618027b64092cacf0a0848c9',
 'output/native/WORD.json.gz':'b19aee42a551500a9af5676f8daa78213c28e2f960ddea0197d0b4313ce9b176',
}

def load(path):
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes())

def lincomb(coeff,rows):
    ans={}
    for c,row in zip(coeff,rows):
        if c: ans=plus(ans,row,c)
    return ans

def dot(x,y): return sum(a*b for a,b in zip(x,y))
def scale(row,c): return {i:v*c for i,v in row.items() if v*c}
def dense_rank(a): return rank([{j:F(x)for j,x in enumerate(row)if x}for row in a])

def row_operations(ops,n):
    a=[{i:F(1)}for i in range(n)]
    for kind,i,j,c in ops:
        if kind=='ADD':a[i]=plus(a[i],a[j],F(c))
        elif kind=='SCALE':need(i==j,'scalar index format');a[i]=scale(a[i],F(c))
        else:raise ValueError('codec opcode')
    return [[r.get(j,F(0))for j in range(n)]for r in a]

def prepare(native,w):
    role={int(k):v for k,v in w['source_role_map'].items()}
    live=native['live'];host_original={live[k]:(b,d)for k,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    originals=sorted(live+[h+112 for h in live]+[j for pair in host_original.values()for j in pair])
    need(role==dict(zip(originals,range(400))),'native sorted400 role compression')
    need(w['public']==400 and len(role)==400,'400 distinct public fields')
    need(w['frames'][:len(native['frames'])]==native['frames'],'literal native chart prefix')
    need(w['initial']==[native['initial'][j]for j in originals],'literal original starting charts')
    X={h:role[h]for h in live};Y={h:role[h+112]for h in live}
    H={h:(role[b],role[d])for h,(b,d)in host_original.items()};U=set(live)-set(H)
    need(len(H)==96 and len(U)==8,'hosted/coupled split')
    aa={h:plus({X[h]:F(1)},{Y[h]:F(1)},-1)if h in U else{X[h]:F(1)}for h in live}
    vv={h:native['frames'][native['initial'][h]][0]for h in live}
    rr={h:root_vector(vv[h])for h in live}
    G={h:{j:F(dot(rr[h],rr[j]),18)for j in live}for h in live}
    spaces=[span(f)for f in w['frames']]
    for h in live:
        need(len(w['frames'][w['initial'][X[h]]])==1,'X initial line')
        fy=native['final'][h+112]
        need(spaces[fy]==frozenset(t for t in range(512)if (t&vv[h]).bit_count()%2==0),'actual final Y facet')
        need(vv[h]not in spaces[fy],'own line outside own facet')
        need(sum(bool(G[h][j])for j in live if j!=h)==48,'native48 Gram contacts')
        for j in live:
            if h!=j:need(bool(G[h][j])==(vv[j]in spaces[fy]),'real/binary contact compatibility')
    m=w['singular_history'];Z=m['orthogonal_frame_normals'];rz=[root_vector(z)for z in Z]
    need([[dot(x,y)for y in rz]for x in rz]==[[18*int(i==j)for j in range(8)]for i in range(8)],'orthogonal Gram basis')
    g=[{h:F(dot(z,rr[h]),18)for h in live}for z in rz]
    for h in live:
        for j in live:need(sum(g[i][h]*g[i][j]for i in range(8))==G[h][j],'basis Gram factorization')
    need([[sum(g[i][h]*g[j][h]for h in live)for j in range(8)]for i in range(8)]==[[13*int(i==j)for j in range(8)]for i in range(8)],'rank8 tight Gram frame')
    actual={i:next(h for h in live if vv[h]==z)for i,z in enumerate(Z)if z in vv.values()}
    need({str(i):h for i,h in actual.items()}==m['native_basis_by_mode'],'native mode identity')
    I=set(actual.values());s=len(I);u=len(I&U)
    need(sorted(I)==m['native_basis_ports'],'native basis list')
    full=[lincomb([g[i][h]for h in live],[aa[h]for h in live])for i in range(8)]
    partial=[lincomb([g[i][h]for h in live if h not in I],[aa[h]for h in live if h not in I])for i in range(8)]
    rev=[{H[h][1]:g[i][h]for h in H if h not in I and g[i][h]}for i in range(8)]
    need(dense_rank([[g[i][h]for h in live]for i in range(8)])==8,'Gram rank')
    need(rank(partial)==8 and rank(full+[aa[h]for h in I])==8+s,'direct-sum exported history')
    for i,h in actual.items():
        need(all(g[j][h]==int(i==j)for j in range(8)),'withheld basis port contributes only own mode')
        need(m['lines'][i]==w['initial'][X[h]],'capture at literal original line ID')
    for i,L in enumerate(m['lines']):need(spaces[L]==frozenset([0,Z[i]]),'mode source line')
    return role,live,X,Y,H,U,aa,G,g,actual,I,spaces,full,partial,rev

def codec_audit(native,w,ctx):
    role,live,X,Y,H,U,aa,G,g,actual,I,spaces,full,partial,rev=ctx
    m=w['singular_history'];classes={}
    for h in live:
        if h not in I:
            support=tuple(i for i in range(8)if g[i][h]);need(len(support)==4,'four-mode nonbasis support')
            classes.setdefault(support,[]).append(h)
    need(len(classes)==14 and set(classes)=={tuple(z['modes'])for z in m['groups']},'complete14-class partition')
    receipts=[]
    for z in m['groups']:
        modes=z['modes'];ports=z['ports'];host=z['hosted'];coupled=z['coupled'];piv=z['pivots'];C=z['C']
        need(set(ports)==set(classes[tuple(modes)]) and ports==host+coupled,'literal class bank')
        need(host==[h for h in ports if h in H]and coupled==[h for h in ports if h in U],'hosted/coupled ordering')
        need(z['D_roles']==[H[h][1]for h in host]and z['Y_roles']==[Y[h]for h in ports],'actual class roles')
        mode_span=set([0])
        for i in modes:mode_span|={v^m['orthogonal_frame_normals'][i]for v in tuple(mode_span)}
        need(mode_span==set(spaces[C])and len(mode_span)==8,'literal rank3 common source')
        for h in ports:need(spaces[C]<spaces[native['final'][h+112]],'proper class-to-final-facet inclusion')
        need(len(piv)==4 and len(set(piv))==4 and all(0<=p<len(host)for p in piv),'four actual hosted pivots')
        dh=len(host);dy=len(ports)
        MD=[[F(i==j)for j in range(dh)]for i in range(dh)]
        MY=[[F(i==j)for j in range(dy)]for i in range(dy)]
        for i,p in zip(modes,piv):
            MD[p]=[g[i][h]for h in host]
            MY[p]=[(F(1,2)if h in U else F(1))*g[i][h]for h in ports]
        need(MD==[[F(x)for x in row]for row in z['M_D']],'reconstructed D matrix')
        need(MY==[[F(x)for x in row]for row in z['M_Y']],'reconstructed Y matrix')
        dd=determinant(MD);dy0=determinant(MY)
        need(dd and dd==dy0,'invertible reciprocal codecs share determinant')
        need(row_operations(z['D_encoder'],dh)==MD,'literal D elementary encoder')
        need(row_operations(z['Y_encoder'],dy)==MY,'literal Y elementary encoder')
        receipts.append({'modes':modes,'hosted_count':dh,'coupled_count':dy-dh,'determinant':str(dd)})
    return receipts


def replay_audit(native,w,ctx,full_check=True):
    role,live,X,Y,H,U,aa,G,g,actual,I,spaces,full,partial,rev=ctx
    m=w['singular_history'];marks=m['markers'];events=m['events'];lines=m['lines'];cache={int(k):v for k,v in m['cache_roles'].items()}
    captures={int(k):v for k,v in m['capture_boundaries'].items()}
    c={h:F(1,2)if h in U else F(1)for h in live}
    L={h:{j:(F(h==j)if h in I else G[h][j])for j in live}for h in live}
    expected={}
    for h in live:
        expected[X[h]]=aa[h]
        expected[Y[h]]=plus({Y[h]:F(1)},lincomb([c[h]*L[h][j]for j in live],[aa[j]for j in live]),1)
    for j,(b,d)in H.items():
        expected[b]=plus({b:F(1)},{H[h][1]:-L[h][j]for h in H if L[h][j]},1)
        expected[d]={d:F(1)}
    bytime={}
    for name,t in marks.items():bytime.setdefault(t,[]).append(('mark',name))
    for z in m['groups']:bytime.setdefault(z['markers']['D_restored_at_C3'],[]).append(('group',z))
    for i,phases in captures.items():
        for name,t in phases.items():bytime.setdefault(t,[]).append(('capture',(i,name)))
    visited=[];exported=[];intermediate=[];hub_intermediate=[];last_old_read={}
    reverse_sources=set(events['new_reverse_sources']);reverse_reads=set(events['new_reverse_reads'])
    old_reads=set(events['old_forward_reads']);restores=set(events['X_restoration']);reverse_consumers=set(events['old_reverse_consumers'])
    line_mode={v:i for i,v in enumerate(lines)}
    def inspect_boundary(t,rows,loc):
        for kind,data in bytime.get(t,[]):
            visited.append((t,kind))
            if kind=='group':
                for d in data['D_roles']:need(rows[d]=={d:F(1)}and loc[d]==data['C'],'D restored before C3 departure')
            elif kind=='capture':
                i,name=data;p=400+i;h=actual.get(i)
                if name=='before':
                    need(rows[p]==partial[i]and loc[p]==lines[i],'actual exported partial at line')
                    if h is not None:need(rows[X[h]]==aa[h]and loc[X[h]]==lines[i],'untouched original basis X at capture')
                elif name=='after':
                    need(rows[p]==scale(aa[h],-1)and rows[X[h]]==full[i]and rows[cache[i]]==full[i],'singular cell preserves displaced full duty')
                    need(loc[p]==loc[X[h]]==loc[cache[i]]==lines[i],'actual singular cochart')
                elif name=='restored':need(rows[X[h]]==aa[h]and loc[X[h]]==127,'original X restored at Hub')
                elif name=='at_ground':need(rows[p]==scale(aa[h],-1)and loc[p]==3 and rows[Y[h]]=={Y[h]:F(1)}and loc[Y[h]]==3,'captured payload reaches untouched Y at ground')
            else:
                if data=='entry_end':
                    need(all(rows[X[h]]==aa[h]and rows[Y[h]]=={Y[h]:F(1)}for h in live),'genuine coupled entry and retained originals')
                elif data=='old_reverse_modes_exclude_native_basis_D':
                    need(all(rows[400+i]==rev[i]and loc[400+i]==lines[i]for i in range(8)),'actual reverse records omit native basis D')
                elif data=='all_D_original_at_final_facets':
                    need(all(rows[d]=={d:F(1)}and loc[d]==native['final'][next(k for k,v in role.items()if v==d)]for b,d in H.values()),'every original D restored at exact final chart')
                elif data=='nonbasis_X_and_all_B_at_Hub':
                    need(all(rows[X[h]]==aa[h]and loc[X[h]]==(lines[next(i for i,b in actual.items()if b==h)]if h in I else 127)for h in live),'only basis X withheld')
                    need(all(loc[b]==127 for b,d in H.values()),'all B actually at Hub')
                elif data=='reverse_consumed':need(all(rows[b]==expected[b]for b,d in H.values()),'complete actual reverse map before forward')
                elif data=='all_full_Gram_modes_at_actual_lines_and_basis_Y_complete':
                    need(all(rows[cache.get(i,400+i)]==full[i]and loc[cache.get(i,400+i)]==lines[i]for i in range(8)),'all displaced old duties at actual decoder lines')
                    need(all(rows[Y[h]]==expected[Y[h]]and loc[Y[h]]==native['final'][h+112]for h in I),'native basis Y fully delivered')
    def hook(t,phase,op,rows,loc):
        if phase=='after':
            inspect_boundary(t,rows,loc)
            if t>marks['reverse_consumed']and op[0]in('ADD','SCALE')and 400<=op[1]<408 and op[1]in rows:
                intermediate.append(dict(rows[op[1]]))
                if loc[op[1]]==127:hub_intermediate.append(dict(rows[op[1]]))
            return
        if t in restores:
            need(op[0]=='ADD'and op[2]in[X[h]for h in live if h not in I]and op[-1]==127,'restoration uses only causally prior nonbasis X')
            h=next(h for h in live if X[h]==op[2]);need(rows[op[2]]==aa[h]and loc[op[2]]==127,'restoration source already restored at Hub')
        if t in reverse_sources:
            need(op[0]=='ADD'and op[-1]==3 and op[2]in[H[h][1]for h in I if h in H],'genuine original D paired acquisition')
            need(rows[op[2]]=={op[2]:F(1)}and not rows[op[1]],'paired acquisition from intact D into zero owner')
        if t in reverse_reads:
            h=next(h for h in H if H[h][0]==op[1]);need(h in I and op[0]=='ADD'and F(op[3])==-1,'paired native B subtraction')
            need(rows[op[2]]=={H[h][1]:F(1)}and loc[op[1]]==loc[op[2]]==w['initial'][X[h]],'actual paired D at original B line')
        if t in reverse_consumers:
            i=op[2]-400;need(op[0]=='ADD'and 0<=i<8 and rows[op[2]]==rev[i]and loc[op[2]]==127,'old reverse uses exact delivered record')
        if t in old_reads:
            i=line_mode[op[-1]];need(op[0]=='ADD'and rows[op[2]]==full[i]and op[2]==cache.get(i,400+i),'old decoder reads full displaced Gram value')
            last_old_read[op[2]]=t
        if t>marks['reverse_consumed']and op[0]=='MOVE'and op[-1]and 400<=op[1]<408:
            i=op[1]-400
            if op[2]==127:need(op[3]==lines[i]and rows[op[1]]==partial[i],'forward exported partial');exported.append(dict(rows[op[1]]))
            elif i in actual:need(op[2]==lines[i]and op[3]==3 and rows[op[1]]==scale(aa[actual[i]],-1),'actual captured continuation');exported.append(dict(rows[op[1]]))
            else:raise ValueError('unexpected forward moving history')
    result=replay(w,mode='independent_singular',hook=hook)
    rows,loc,raw,owned,counts,peak,lifetimes,trace,retire=result
    need(rows==expected,'all400 exact independent input-column rows')
    need(all(loc[new]==native['final'][old]for old,new in role.items()),'all400 exact endpoint chart IDs')
    need(len(visited)==sum(len(v)for v in bytime.values()),'every source chronology boundary visited')
    need(len(last_old_read)==8,'all eight genuine old decoder modes consumed')
    for t,q,ch,payload in retire:
        if q in last_old_read and t>marks['reverse_consumed']:need(t>last_old_read[q],'old duty survives its last actual read')
    s=len(I);u=len(I&U);d=2*s-u
    need(raw=={1:112,2:112,3:88-d,5:200-d,8:200+d},'independent complete raw profile')
    need(owned=={1:8+d,8:16},'independent complete owned profile')
    need(sum(k*v for k,v in raw.items())==3200 and sum(k*v for k,v in owned.items())==136+d,'complete rank masses')
    need(rank(exported)==8+s and len(exported)==8+s,'actual MOVE-boundary history rank')
    for o in w['program']:
        if o[0]in('ADD','SCALE'):
            x=F(o[3]if o[0]=='ADD'else o[2]);need(x.denominator&(x.denominator-1)==0,'actual dyadic scalar')
    if not full_check:return True
    need(rank(list(rows.values()))==400,'independent full public rank')
    for h,(b,d0)in H.items():
        for j,(bj,dj)in H.items():need(rows[b].get(dj,F(0))+rows[Y[j]].get(X[h],F(0))==0,'full9216 hosted adjoint entries')
    residual=rank([plus(rows[b],{b:F(1),d0:F(-1)},-1)for b,d0 in H.values()])
    need(residual==96-s+u,'exact actual reverse residual rank')
    hostdet=determinant([[F(i==j)-sum(g[i][h]*g[j][h]for h in H)for j in range(8)]for i in range(8)])
    need(hostdet==F(415068771,2),'hosted determinant via exact8x8 reduction')
    current=sum(bool(L[h][j])for h in live for j in live if h!=j)
    debt=sum(len(plus(rows[Y[h]],{X[h]:c[h],Y[h]:c[h]if h in U else F(1)},-1))for h in live)
    need(current==4992-48*s,'uncorrected current-a contacts')
    Q=dict(Counter(raw)+Counter(owned))
    return {'variant':m['variant'],'s':s,'u':u,'d':d,'public_rank':400,'paired_entries':9216,'raw':raw,'owned':owned,'Q':Q,'counts':counts,'peak':peak,'lifetimes':lifetimes,'nonzero_owned_retirements':sum(bool(p)for _,_,_,p in retire),'exported_forward_history_rank':rank(exported),'all_forward_packet_arithmetic_state_rank':rank(intermediate),'Hub_formation_intermediate_rank':rank(hub_intermediate),'reverse_residual_rank':residual,'current_a_debt':current,'original_coordinate_debt':debt,'chronology_boundaries':len(visited),'actual_old_decoder_reads':len(old_reads),'restoration_reads':len(restores),'hosted_determinant':str(hostdet)}


def negative_controls(native,w,ctx):
    events=w['singular_history']['events'];out=[]
    jobs=[('cache_copied_from_partial',events['cache_copies'][0]),('capture_wrong_sign',events['captures'][1]),('omit_one_Hub_restoration_read',events['X_restoration'][0]),('omit_actual_paired_B_delivery',events['new_reverse_reads'][0]),('wrong_native_ground_sign',events['native_ground_reads'][0]),('omit_actual_D_acquisition',events['new_reverse_sources'][0])]
    for name,t in jobs:
        bad=copy.deepcopy(w)
        if name=='cache_copied_from_partial':
            i=next(i for i,v in enumerate(w['singular_history']['lines'])if v==bad['program'][t][-1]);bad['program'][t][2]=400+i
        elif name in('capture_wrong_sign','wrong_native_ground_sign'):bad['program'][t][3]=str(-F(bad['program'][t][3]))
        else:bad['program'][t][3]='0'
        try:replay_audit(native,bad,ctx,False)
        except (ValueError,KeyError)as exc:out.append({'mutation':name,'instruction':t,'rejected_by':str(exc)})
        else:raise ValueError('negative control accepted: '+name)
    return out


def frame_census(native):
    normals=[x for x in range(512)if x.bit_count()in(3,7)];roots=[root_vector(x)for x in normals];n=len(normals)
    need(n==120,'complete root-normal domain')
    adj=[sum(1<<j for j in range(i+1,n)if dot(roots[i],roots[j])==0)for i in range(n)]
    live=native['live'];h_by_v={native['frames'][native['initial'][h]][0]:h for h in live}
    H={live[i]for i in native['hosted']['Dports']};U=set(live)-H
    full_count=0;native_count=0;hist=Counter();native_examples=[]
    def dfs(chosen,cand):
        nonlocal full_count,native_count
        if len(chosen)==8:
            full_count+=1
            if all(normals[j]in h_by_v for j in chosen):
                native_count+=1;ports=[h_by_v[normals[j]]for j in chosen];u=len(set(ports)&U);hist[u]+=1
                if u==3:native_examples.append(sorted(ports))
            return
        while cand and len(chosen)+cand.bit_count()>=8:
            bit=cand&-cand;cand^=bit;j=bit.bit_length()-1;dfs(chosen+[j],cand&adj[j])
    dfs([], (1<<n)-1)
    need((full_count,native_count,dict(hist))==(2025,759,{0:369,1:308,2:80,3:2}),'independent exhaustive frame census')
    rr={h:root_vector(native['frames'][native['initial'][h]][0])for h in U};obstructions=[]
    for quartet in combinations(sorted(U),4):
        pair=next(((a,b)for a,b in combinations(quartet,2)if dot(rr[a],rr[b])),None)
        need(pair is not None,'coupled four-clique excluded');obstructions.append({'ports':list(quartet),'nonorthogonal_pair':list(pair),'dot':dot(rr[pair[0]],rr[pair[1]])})
    need(len(obstructions)==70,'all coupled four-subsets')
    return {'root_normals':120,'full_frames':full_count,'actual_native_frames':native_count,'coupled_intersections':dict(hist),'max_three_examples':native_examples,'coupled_ports':sorted(U),'four_subset_witnesses':obstructions}


def exact_invoices(results):
    f=load(AUTHOR/'dependencies/FULL-RESULT.json');T=f['invoice']['T'];P=f['invoice']['P']
    seed={1:120,2:112,3:88,5:200,8:216}
    def combine(*terms):
        out={}
        for c,d in terms:
            for k,v in d.items():out[int(k)]=out.get(int(k),F(0))+F(c)*F(v)
        return {k:v for k,v in out.items()if v}
    slope=combine((F(1,18),T),(-F(1,18),P))
    room=combine((1,slope),(1,f['native']['paid']),(-1,f['native']['helpers']),(-1,seed))
    penalty=combine((-1,slope));unit={1:1,3:-1,5:-1,8:1};B=10**35;cache={}
    def bound(n):
        if n not in cache:
            N=n**199*B**200;lo=0;hi=n*B+1
            while hi-lo>1:
                a=(hi+lo)//2
                if a**200<=N:lo=a
                else:hi=a
            need(lo**200<=N<hi**200,'exact200th-power endpoint inequalities')
            cache[n]=(F(lo,B),F(hi,B))
        return cache[n]
    def moment(profile):
        lo=hi=F(0)
        for n,c in profile.items():
            a,b=bound(n)
            lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
        return lo,hi
    ru=moment(room);pe=moment(penalty);un=moment(unit)
    need(un[0]>0 and pe[0]>0,'positive signed unit and finite-m penalty')
    variants=[]
    for z in results:
        d=z['d'];delta=combine((d,unit));Q=combine((1,seed),(1,delta))
        need(Q==z['Q'],'independent actual word versus complete source refund profile')
        inc=moment(delta);margin=moment(combine((1,room),(-1,delta)))
        if margin[0]>0:
            m=2
            while margin[0]-pe[1]/(m-1)<=0:m+=1
            need(m==2 or margin[1]-pe[0]/(m-2)<0,'exact minimal integer multiplicity')
        else:need(margin[1]<0,'decisive impossible limiting margin');m=None
        variants.append({'variant':z['variant'],'increment':inc,'limiting_margin':margin,'first_positive_fixed_m':m})
    need(variants[0]['first_positive_fixed_m']==9 and variants[1]['first_positive_fixed_m']is None,'hybrid9/native none')
    return {'exponent':'199/200','decimal_precision':35,'seed_Q':seed,'unit':un,'seed_room':ru,'finite_m_penalty':pe,'variants':variants,'formula':'margin - penalty/(m-1), fixed integer m>=2','inherited_full_caller_substitutions':18,'computed_nth_root_bounds':len(cache)}


def phases(w,variant):
    dep=REPO/'research/moonshot-005-program/results/complex-omitted-line-gram/author'
    seedpath=dep/'output/WORD.json.gz';need(hashlib.sha256(seedpath.read_bytes()).hexdigest()=='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc','retained seed pin')
    seed=load(seedpath);need(w['frames'][:len(seed['frames'])]==seed['frames'],'literal seed chart prefix')
    old={(o[2],o[3])for o in seed['program']if o[0]=='MOVE'};new={(o[2],o[3])for o in w['program']if o[0]=='MOVE'}-old
    data=load(AUTHOR/'output'/variant/'PHASES.json');recs=data['recipes']
    need(len(recs)==len(new)and{(r['source'],r['target'])for r in recs}==new,'complete introduced recipe pair coverage')
    engine=dep/'dependencies/native_verify.py';pin='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'
    need(hashlib.sha256(engine.read_bytes()).hexdigest()==pin,'retained exact phase interpreter pin')
    spec=importlib.util.spec_from_file_location('retained_phase_interpreter',engine);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    for r in recs:
        a,b=r['source'],r['target'];need(r['source_frame']==w['frames'][a]and r['target_frame']==w['frames'][b],'actual ordered recipe frames')
        need(r['rank']==r['recipe']['rank']==abs(len(w['frames'][a])-len(w['frames'][b])),'actual nested recipe rank')
        v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(w['frames'][a],9))+v.frame(w['frames'][b],9),'published phase-inclusive recipe')
    bad=copy.deepcopy(recs[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
    try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(bad['source_frame'],9))+v.frame(bad['target_frame'],9),'wrong phase')
    except ValueError:pass
    else:raise ValueError('wrong global phase accepted')
    return {'introduced_ordered_pairs':len(new),'retained_interpreter_sha256':pin,'wrong_phase_rejected':True,'classification':'retained independent-interpreter certificate reproduction, not a new independent phase algorithm'}


def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v)for v in x]
    return x

def main():
    global AUTHOR,REPO
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--repo',type=Path,default=REPO);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));p.add_argument('--skip-phases',action='store_true');args=p.parse_args();AUTHOR=args.author;REPO=args.repo
    for file,pin in PINS.items():need(hashlib.sha256((AUTHOR/file).read_bytes()).hexdigest()==pin,'authenticated '+file)
    native=load(AUTHOR/'dependencies/native.json.gz');variants=[]
    for variant in ('hybrid','native'):
        w=load(AUTHOR/'output'/variant/'WORD.json.gz');ctx=prepare(native,w);codecs=codec_audit(native,w,ctx);r=replay_audit(native,w,ctx)
        r['codecs']=codecs;r['negative_controls']=negative_controls(native,w,ctx)
        if not args.skip_phases:r['finite_phase_recipes']=phases(w,variant)
        variants.append(r);print(json.dumps({'variant':variant,'status':'PASS','history':r['exported_forward_history_rank'],'all_intermediate_rank':r['all_forward_packet_arithmetic_state_rank'],'residual':r['reverse_residual_rank'],'negative_controls':len(r['negative_controls'])}),flush=True)
    census=frame_census(native);invoice=exact_invoices(variants)
    result={'status':'PASS_INDEPENDENT_SINGULAR_GRAM_SOURCE_REVIEW','pins':PINS,'variants':variants,'census':census,'invoice':invoice,'classification':'Universal conditional compiler argument reviewed; pinned source and finite invoice independently checked. No new kappa. Exported history is not all intermediate arithmetic state history.'}
    args.output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n');print('PASS: all400 maps,18432 adjoint entries, chronology,12 source mutations, frame census and complete invoices')

if __name__=='__main__':main()
