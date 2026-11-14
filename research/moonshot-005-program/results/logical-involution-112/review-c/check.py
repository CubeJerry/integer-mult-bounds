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

from engine import replay,span,plus
from itertools import combinations

BASE=Path(__file__).resolve().parents[2]
AUTHOR=BASE/'worker-b/logical-involution-112'
REPO=BASE/'programme'

def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def closure(vectors):
    s={0}
    for v in vectors:s|={x^v for x in tuple(s)}
    return frozenset(s)

def geometry(native,w):
    m=w['logical_involution'];P=m['ports'];v={int(h):a for h,a in m['normals'].items()};Z=m['omitted_frame'];need(P==sorted(v)and len(P)==112 and len(set(v.values()))==112,'112 distinct genuine root lines')
    need(Z==[7,25,42,52,76,82,97,127]and set(v.values())=={a for a in range(512)if a.bit_count()in(3,7)}-set(Z),'full120 normal domain minus exact orthogonal frame')
    need(all(v[h]==native['frames'][native['initial'][h]][0]for h in native['live']),'all old104 native normals embedded exactly')
    root={h:root_vector(v[h])for h in P};rz=[root_vector(z)for z in Z];need([[dot(a,b)for b in rz]for a in rz]==[[18*int(i==j)for j in range(8)]for i in range(8)],'orthogonal omitted real basis')
    g={h:[F(dot(root[h],r),18)for r in rz]for h in P};G={h:{j:F(dot(root[h],root[j]),18)for j in P}for h in P}
    need(all(G[h][j]==sum(g[h][i]*g[j][i]for i in range(8))for h in P for j in P),'all12544 Gram factorization entries')
    need([[sum(g[h][i]*g[h][j]for h in P)for j in range(8)]for i in range(8)]==[[14*int(i==j)for j in range(8)]for i in range(8)],'global tight-frame constant14')
    spaces=[span(f)for f in w['frames']];roles={tag:{int(h):r for h,r in d.items()}for tag,d in m['role_map'].items()}
    need(roles=={tag:{h:k*112+i for i,h in enumerate(P)}for k,tag in enumerate(['X','Y','B','D'])}and w['public']==448,'four distinct arbitrary main inputs per new port')
    for h in P:
        x,y,b,d=[roles[t][h]for t in['X','Y','B','D']]
        need(spaces[w['initial'][x]]==spaces[w['initial'][b]]==frozenset([0,v[h]])and spaces[w['initial'][y]]==spaces[w['initial'][d]]==frozenset([0]),'actual source boundary geometry')
        need(spaces[w['final'][x]]==spaces[w['final'][b]]==frozenset(range(512)),'actual Hub output geometry')
        need(spaces[w['final'][y]]==spaces[w['final'][d]]==frozenset(a for a in range(512)if (a&v[h]).bit_count()%2==0),'actual prescribed facet outputs')
    classes={}
    for h in P:
        key=tuple(i for i in range(8)if g[h][i]);need(len(key)==4,'four omitted modes per root');classes.setdefault(key,[]).append(h)
    need(len(classes)==14 and all(len(t)==8 for t in classes.values())and set(classes)=={tuple(z['modes'])for z in m['groups']},'complete fourteen full eight-port classes')
    co={};codecs=[];fourier=[];radicals=Counter()
    for z in m['groups']:
        ports=z['ports'];modes=z['modes'];need(ports==classes[tuple(modes)],'actual complete class membership')
        need([[sum(g[h][i]*g[h][j]for h in ports)for j in modes]for i in modes]==[[2*int(i==j)for j in modes]for i in modes],'each four-mode class has tight constant2')
        need(spaces[z['C3']]==closure(Z[i]for i in modes)and len(spaces[z['C3']])==8,'exact codec rank3 chart')
        for h in ports:co[h]=tuple(modes)
        M=[[F(i==j)for j in range(8)]for i in range(8)];need(len(z['pivots'])==len(set(z['pivots']))==4,'four actual independent pivots')
        for i,p in zip(modes,z['pivots']):M[p]=[g[h][i]for h in ports]
        det=determinant(M);need(det and M==[[F(a)for a in row]for row in z['M']],'exact full-eight class encoder')
        enc={i:{i:F(1)}for i in range(8)}
        for tag,a,b,c in z['encoder']:
            if tag=='ADD':enc[a]=plus(enc[a],enc[b],F(c))
            else:need(tag=='SCALE','codec scalar operation');enc[a]={j:F(c)*t for j,t in enc[a].items()if F(c)*t}
        need([[enc[i].get(j,F(0))for j in range(8)]for i in range(8)]==M,'literal elementary encoder')
        codecs.append({'modes':modes,'determinant':str(det)})
        parts={-1:[],1:[]}
        for h in ports:
            sign=1
            for i in modes:sign*=1 if g[h][i]>0 else -1
            parts[sign].append(h)
        T=parts[-1];S=parts[1];ST=closure(v[h]for h in T);SS=closure(v[h]for h in S);W=ST&SS
        need(len(T)==len(S)==4 and len(ST)==len(SS)==8 and len(W)==4 and len(closure(ST|SS))==16,'orthogonal half spans meet in rank2')
        need(all((a&b).bit_count()%2==0 for a in ST for b in SS),'two half spans orthogonal')
        need(W=={a for a in ST if all((a&b).bit_count()%2==0 for b in ST)}=={a for a in SS if all((a&b).bit_count()%2==0 for b in SS)},'intersection is the common radical')
        aa=sorted(W-{0});a=aa[0];b=aa[1];ww=[0,a,b,a^b];u=min(v[h]for h in T);vv=min(v[h]for h in S)
        need({u^x for x in W}=={v[h]for h in T}and{vv^x for x in W}=={v[h]for h in S},'actual halves are affine radical planes')
        signs=[[int(F(dot(root_vector(u^x),root_vector(vv^y)),9))for y in ww]for x in ww]
        need(all(abs(s)==1 for row in signs for s in row),'all cross coefficients exactly signed one-half')
        norm=[[signs[i][j]*signs[i][0]*signs[0][j]*signs[0][0]for j in range(4)]for i in range(4)]
        sym=[[(-1)**(((i&1)*((j>>1)&1)+((i>>1)&1)*(j&1))%2)for j in range(4)]for i in range(4)]
        need(norm==sym,'exact canonical symplectic Fourier kernel on common radical')
        radicals[tuple(sorted(W))]+=1;fourier.append({'modes':modes,'negative_half_ports':T,'positive_half_ports':S,'common_radical_basis':[a,b],'base_normals':[u,vv],'cross_twice_Gram':signs,'normalized_symplectic_signs':norm})
    E=closure([30,45,75]);need(len(E)==8 and len(radicals)==7 and set(radicals.values())=={2}and all(set(W)<=E for W in radicals),'seven planes of the same rank3 even space, each used twice')
    need(len(m['halves'])==28,'all oriented half meetings')
    seen=Counter();halfof={}
    for z in m['halves']:
        T=z['ports'];S=z['sources'];modes=m['groups'][z['class']]['modes'];C=z.get('source_C3',z.get('C4'))
        need(len(T)==len(S)==4 and set(T).isdisjoint(S)and set(T+S)==set(classes[tuple(modes)]),'oriented disjoint half partition')
        expected=closure(v[h]for h in S)
        if m['variant']!='R0-minimal':expected=closure(list(expected)+[Z[i]for i in modes])
        need(spaces[C]==expected and len(expected)==(8 if m['variant']=='R0-minimal'else 16),'literal meeting chart is the specified native span')
        need({h for h in P if v[h]in expected}==set(S),'exact source incidence of the meeting chart')
        need({h for h in P if all((a&v[h]).bit_count()%2==0 for a in expected)}==set(T),'exact receiver incidence of the meeting chart')
        need(all(abs(G[h][j])==F(1,2)for h in T for j in S),'all16 local contacts are genuine signed halves')
        for h in T:seen[h]+=1;halfof[h]=z
    need(seen==Counter({h:1 for h in P}),'each receiver has exactly one local meeting')
    alpha=F(m['alpha']);need(alpha==(F(1,7)if m['variant']=='R1'else 0),'stated coupling parameter')
    R={h:{j:F(h==j)-(G[h][j]if co[h]==co[j]else 0)+alpha*G[h][j]for j in P}for h in P}
    R={h:{j:a for j,a in row.items()if a}for h,row in R.items()}
    need(R=={int(h):{int(j):F(a)for j,a in row.items()}for h,row in m['R_rows'].items()},'every stored coupling coefficient reconstructed')
    need(all(R[h].get(j,0)==R[j].get(h,0)for h in P for j in P),'symmetric coupling')
    for h in P:
        square={}
        for j,a in R[h].items():square=plus(square,R[j],a)
        need(square=={h:F(1)},'every entry of the actual112 coupling square')
    d=rank([plus(R[h],{h:F(1)},-1)for h in P]);need(d==(48 if alpha else 56),'rank of R-I')
    old=native['live'];witness=None
    for h in old:
        square={}
        for j,a in R[h].items():
            if j in old:square=plus(square,{k:b for k,b in R[j].items()if k in old},a)
        error=plus(square,{h:F(1)},-1)
        if error:witness={'row':h,'square_minus_identity':error};break
    need(witness is not None,'old104 principal restriction really fails involution')
    return {'P':P,'v':v,'g':g,'G':G,'R':R,'roles':roles,'spaces':spaces,'halfof':halfof,'rank_R_minus_I':d,'codecs':codecs,'fourier':fourier,'radical_planes':list(radicals),'old104_counterexample':witness}

def audit(w,c):
    m=w['logical_involution'];P=c['P'];g=c['g'];G=c['G'];R=c['R'];roles=c['roles'];spaces=c['spaces'];X,Y,B,D=[roles[s]for s in['X','Y','B','D']];variant=m['variant'];active=variant=='R1';events=m['events'];checks=Counter()
    invX={r:h for h,r in X.items()};invY={r:h for h,r in Y.items()};invB={r:h for h,r in B.items()};invD={r:h for h,r in D.items()};cache={456+i:h for i,h in enumerate(P)}
    localF=set(events['local_forward']);localR=set(events['local_reverse']);need(len(localF)==len(localR)==448,'exact local event cardinalities')
    Dcuts={z['markers']['D_original']:z for z in m['groups']}if active else{}
    Ycuts={z['markers']['global_Y_decoded']:z for z in m['groups']}if active else{}
    Ccuts={z['markers']['cache_ready']:z for z in m['halves']}if active else{}
    def hook(t,when,o,rows,loc):
        if when=='before':
            if t in localF:
                need(o[0]=='ADD','local forward is a literal read');h=(cache if active else invY)[o[1]];j=invX[o[2]];z=c['halfof'][h];chart=z.get('source_C3',z.get('C4'))
                need(j in z['sources']and F(o[3])==-G[h][j]and o[4]==chart and rows[o[2]]=={X[j]:F(1)},'each real original-X cochart contact');checks['local_forward_original_X']+=1
            if t in localR:
                need(o[0]=='ADD','local reverse is a literal read');j=invB[o[1]];h=invD[o[2]];z=c['halfof'][h];chart=z.get('source_C3',z.get('C4'))
                need(j in z['sources']and F(o[3])==G[h][j]and o[4]==chart and rows[o[2]]=={D[h]:F(1)},'each paired original-D cochart contact');checks['local_reverse_original_D']+=1
        if when!='after':return
        if t in Dcuts:
            z=Dcuts[t]
            for h in z['ports']:need(rows[D[h]]=={D[h]:F(1)}and loc[D[h]]==z['C3'],'actual restored D before local consumers');checks['restored_D_at_C3']+=1
        if t in Ycuts:
            z=Ycuts[t]
            for h in z['ports']:
                want=plus({Y[h]:F(1)},{X[j]:G[h][j]/7 for j in P if G[h][j]},1)
                need(rows[Y[h]]==want and loc[Y[h]]==z['C3'],'complete global Gram contribution before cached local correction');checks['global_Y_at_C3']+=1
        if t in Ccuts:
            z=Ccuts[t]
            for i,h in cache.items():
                if h in z['ports']:need(rows[i]=={X[j]:-G[h][j]for j in z['sources']}and loc[i]==z['C4'],'genuine stationary local forward cache');checks['actual_local_cache']+=1
        for key,rr in [('reverse_modes_acquired',D),('forward_modes_acquired',X)]:
            if active and t==m['markers'][key]:
                for i in range(8):
                    need(rows[448+i]=={rr[h]:g[h][i]for h in P if g[h][i]}and spaces[loc[448+i]]==frozenset([0,m['omitted_frame'][i]]),'actual complete exported Gram mode at its true native line');checks[key]+=1
    rows,loc,raw,owned,counts,peak,lifetimes,trace,retire=replay(w,hook=hook)
    want={i:{i:F(1)}for i in range(448)}
    for h in P:
        want[Y[h]]=plus(want[Y[h]],{X[j]:a for j,a in R[h].items()},1)
        want[B[h]]=plus(want[B[h]],{D[j]:-R[j].get(h,F(0))for j in P if R[j].get(h,F(0))},1)
    need(rows==want and loc==dict(enumerate(w['final'])),'all448 arbitrary input columns and every final chart')
    need(rank(rows.values())==448 and all(rows[Y[h]].get(X[j],0)+rows[B[j]].get(D[h],0)==0 for h in P for j in P),'full rank and all12544 adjoint entries')
    expected={'R0':{3:224,4:448,5:224},'R0-minimal':{2:224,3:224,5:224,6:224},'R1':{1:336,2:112,3:336,4:224,5:224}}[variant]
    need(raw==expected and owned==({8:16}if active else{})and sum(k*v for k,v in raw.items())==3584,'complete independent movement and original-boundary rank mass')
    need(peak==(120 if active else 0)and lifetimes==len(retire)==(128 if active else 0)and all(r for _,_,_,r in retire),'all owned births, peak and dirty retirements counted')
    scalars=Counter();unsupported=[]
    for t,o in enumerate(w['program']):
        if o[0]in('ADD','SCALE'):
            a=F(o[3]if o[0]=='ADD'else o[2]);scalars[str(a)]+=1;n=a.denominator
            for p in[2,3,5]:
                while n%p==0:n//=p
            if n!=1:unsupported.append(t)
    need(len(unsupported)==(504 if active else 0),'exact unsupported denominator7 operations')
    if not active:need(set(scalars)=={'1/2','-1/2'}and counts=={'MOVE':896,'ADD':896},'actual direct R0 scalar and instruction budget')
    need(not active or all(R[h][h]==F(1,7)for h in P),'R1 target itself has an unadmitted1/7 diagonal')
    receipt={'variant':variant,'public':448,'all_input_rank':448,'adjoint_entries':12544,'rank_R_minus_I':c['rank_R_minus_I'],'raw':raw,'owned':owned,'Q':dict(Counter(raw)+Counter(owned)),'counts':counts,'lifetimes':lifetimes,'peak':peak,'dirty_retirements':len(retire),'chronology':dict(checks),'scalar_counts':dict(scalars),'unsupported_denominator7_operations':len(unsupported),'old104_counterexample':c['old104_counterexample']}
    return receipt,rows,loc

def controls(w,c,good,goodloc):
    ev=w['logical_involution']['events'];jobs=[]
    for key in['local_forward','local_reverse','forward_reads','reverse_reads','cache_delivery']:
        if ev.get(key):jobs.append(('corrupt_'+key,ev[key][0]))
    jobs.append(('skip_actual_X_stop',next(t for t,o in enumerate(w['program'])if o[0]=='MOVE'and o[1]in c['roles']['X'].values())))
    if w['logical_involution']['variant']=='R1':
        jobs.append(('erase_required_cache',next(t for t,o in enumerate(w['program'])if o[0]=='INIT'and o[1]>=456)))
    out=[]
    for label,t in jobs:
        bad=copy.deepcopy(w);o=bad['program'][t]
        if label.startswith('corrupt_'):o[3]=str(-F(o[3]))
        elif label=='skip_actual_X_stop':o[3]=127
        else:bad['program'][t]=['INIT',o[1]+112,o[2]]
        try:
            rr,ll,*_=replay(bad);rejected=(rr!=good or ll!=goodloc)
        except (ValueError,KeyError):rejected=True
        need(rejected,'semantic negative control '+label);out.append(label)
    # A source-field square is not the square of its coupling.  The actual
    # shear has nonzero doubled off-diagonal entries over characteristic zero.
    X,Y=[c['roles'][s]for s in['X','Y']];h=c['P'][0];j,a=next(iter(c['R'][h].items()))
    need(a and good[Y[h]].get(X[j])==a and 2*a!=0,'paired shear is not an involution')
    out.append('R_squared_identity_does_not_make_the_paired_shear_an_involution')
    return out

def phase_review(w,parent,path):
    need(w['frames'][:len(parent['frames'])]==parent['frames'],'phase parent exact chart prefix')
    inherited={(o[2],o[3])for o in parent['program']if o[0]=='MOVE'};used={(o[2],o[3])for o in w['program']if o[0]=='MOVE'};new=used-inherited
    data=load(path);recs=data['recipes'];need({(r['source'],r['target'])for r in recs}==new and len(recs)==len(new),'all and only introduced ordered maps certified')
    engine=REPO/'research/moonshot-005-program/results/complex-omitted-line-gram/author/dependencies/native_verify.py';pin='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38';need(hashlib.sha256(engine.read_bytes()).hexdigest()==pin,'retained phase interpreter')
    sp=importlib.util.spec_from_file_location('involution_review_phase',engine);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
    for r in recs:
        a,b=r['source'],r['target'];need((r['source_frame'],r['target_frame'])==(w['frames'][a],w['frames'][b]),'actual literal recipe frames')
        need(r['rank']==r['recipe']['rank']==abs(len(w['frames'][a])-len(w['frames'][b])),'true nested rank in recipe')
        v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(w['frames'][a],9))+v.frame(w['frames'][b],9),'exact signed map')
    r=copy.deepcopy(recs[0]);r['recipe']['left']['phase']=(r['recipe']['left']['phase']+1)%4
    try:v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(r['source_frame'],9))+v.frame(r['target_frame'],9),'wrong phase')
    except ValueError:rejected=True
    else:raise ValueError('wrong phase accepted')
    return {'introduced_maps':len(new),'inherited_used_maps':len(used&inherited),'phase_mutation_rejected':rejected,'scope':'Pinned retained-interpreter certificate reproduction, distinct from the independently implemented rational source replay.'}

def invoices(receipts):
    B=10**35;cache={}
    def power(n):
        if n not in cache:
            N=n**199*B**200;lo=0;hi=n*B+1
            while hi-lo>1:
                a=(lo+hi)//2
                if a**200<=N:lo=a
                else:hi=a
            need(lo**200<=N<hi**200,'exact integer root tariff bracket');cache[n]=(F(lo,B),F(hi,B))
        return cache[n]
    def moment(q):
        lo=hi=F(0)
        for n,c in q.items():
            a,b=power(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
        return [lo,hi]
    out=[]
    for r in receipts:
        z=moment(r['Q']);out.append({'variant':r['variant'],'movement_moment_interval':z,'display':float(z[0]),'instruction_counts':r['counts'],'owned_lifetimes':r['lifetimes'],'dirty_retirements':r['dirty_retirements']})
    d=moment({2:224,4:-448,6:224});need(d[1]<0,'source-half refinement strictly decreases the concave moment')
    outside={97:F(56,3),1:F(-112,3)}
    for j in range(1,7):outside[1+8*j]=F(112,3)
    for j in range(1,6):outside[8*j]=F(-112,3)
    price=load(AUTHOR/'output/PRICE.json')
    need({int(k):F(v)for k,v in price['conditional_outside_profile_per_native'].items()}==outside,'exact separately stipulated twelve-stage benchmark profile')
    allowance=moment(outside);margins=[]
    for r in receipts:
        q=dict(outside)
        for n,k in r['Q'].items():q[n]=q.get(n,F(0))-k
        z=moment(q);given=list(map(F,price['sources'][r['variant']]['conditional_twelve_stage_margin_per_native']))
        need(max(z[0],given[0])<=min(z[1],given[1]),'independent rational benchmark enclosure agrees')
        margins.append({'variant':r['variant'],'conditional_per_native_margin':z,'display':float(z[0])})
    return {'kappa':'1/200','profile_convention':'[r]=r^(199/200)','sources':out,'minimal_minus_C4_moment_interval':d,'conditional_twelve_stage_benchmark':{'outside_profile_per_native':outside,'allowance':allowance,'margins':margins,'assumed_complete_interface':True,'status':'Arithmetic implication only; physical operator/query/productive target hypotheses are not established.'},'complete_finite_m_invoice':False,'scope':'Exact finite source movement moments and ordinary operation/owner counts. Native/caller helpers, compiler, precision, erasure, recursive multiplicity and productive-head admission are not supplied by this new112-domain source.'}

PINS={'dependencies/native104.json.gz':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','dependencies/GEOMETRY.json':'e8e48d62be188293677d5c2f7c9a1b104e944bff8ac97669fbaa9a70b41613c6','output/R0/WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','output/R1/WORD.json.gz':'86b8a1098e8fd18959e9fbfbfcb84d9f4bd157838936aeb94d656be5ce8ed5c7','output/R0-minimal/WORD.json.gz':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336'}
PINS.update({'PROOF.md':'2cd7cfb5fb673ec0604fd6fb4774b998e65c94792ce21b069e59e6d320dc4792','MANIFEST.json':'e7b004e11618a472ac1f5e7567575e892b6981be83cc27898c26836f83ca2147','output/PRICE.json':'a9dea3704adb6e02b10d02d8cef550f74851620e1066bcfd8b265422f3d06151'})

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v)for v in x]
    return x

def main():
    global AUTHOR,REPO
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--repo',type=Path,default=REPO);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));p.add_argument('--skip-phases',action='store_true');a=p.parse_args();AUTHOR=a.author;REPO=a.repo
    for name,pin in PINS.items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen source pin '+name)
    native=load(AUTHOR/'dependencies/native104.json.gz');seedpath=REPO/'research/moonshot-005-program/results/complex-omitted-line-gram/author/output/WORD.json.gz';need(hashlib.sha256(seedpath.read_bytes()).hexdigest()=='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc','exact phase parent');seed=load(seedpath)
    receipts=[];first=None;fourier=None
    for name in['R0','R0-minimal','R1']:
        w=load(AUTHOR/'output'/name/'WORD.json.gz');c=geometry(native,w);r,rows,loc=audit(w,c);r['negative_controls']=controls(w,c,rows,loc)
        if name=='R0':first=rows;fourier=c['fourier']
        if name=='R0-minimal':need(rows==first,'minimal chart source has exactly the same448-column map')
        if not a.skip_phases:r['phase_recipes']=phase_review(w,seed,AUTHOR/'output'/name/'PHASES.json')
        receipts.append(r);print(json.dumps({'variant':name,'status':'PASS','public':448,'raw':r['raw'],'owned':r['owned'],'controls':len(r['negative_controls'])}),flush=True)
    result={'status':'PASS_INDEPENDENT_FULL112_LOGICAL_SOURCE_REVIEW','sources':receipts,'fourier_radical_geometry':fourier,'source_movement_invoices':invoices(receipts),'source_pins':PINS,'classification':'Proved finite exact paired sources and exact scalar/rational algebra; physical caller and productive-head admission remain open. R1 additionally fails the retained exact coefficient ring. No new kappa.'}
    a.output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n')

if __name__=='__main__':main()
