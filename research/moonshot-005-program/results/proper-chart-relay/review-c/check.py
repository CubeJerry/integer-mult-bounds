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

BASE=Path(__file__).resolve().parents[2]
DEFAULT_AUTHOR=Path('/workspace/scratch/c962181f51c6/worker-b/proper-chart-relay-frozen')
PINS={'proof':'c5d9ae71061a3283959338f4a33351ecc64f60c1f4cbbf95e73a926619252b7c','native':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','parent':'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','full':'d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','20':'0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c','44':'f3bd538e056c501c156bd06669656e7f7c2b46fe66d02f481c340dc78e170892'}

def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def comb(coeff,rows):
    out={}
    for c,r in zip(coeff,rows):out=plus(out,r,F(c))
    return out

def prep(native,parent,w):
    role={int(k):v for k,v in w['source_role_map'].items()};live=native['live'];hp={live[i]:(b,d)for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    old=sorted(live+[h+112 for h in live]+[z for pair in hp.values()for z in pair]);need(role==dict(zip(old,range(400))),'all400 native original role IDs')
    need(w['initial']==[native['initial'][i]for i in old]and w['initial']==parent['initial'],'literal native/parent starting charts')
    need(w['frames'][:len(parent['frames'])]==parent['frames'],'literal retained interface frames')
    X={h:role[h]for h in live};Y={h:role[h+112]for h in live};H={h:(role[b],role[d])for h,(b,d)in hp.items()};U=sorted(set(live)-set(H))
    need(U==[17,19,30,38,40,47,52,60],'actual coupled zero-D set')
    aa={h:plus({X[h]:F(1)},{Y[h]:F(1)},-1)if h in U else{X[h]:F(1)}for h in live}
    vv={h:native['frames'][native['initial'][h]][0]for h in live};rr={h:root_vector(vv[h])for h in live};G={h:{j:F(dot(rr[h],rr[j]),18)for j in live}for h in live}
    meta=w['relay'];Z=meta['ground_Gram_frame'];need(Z==[7,25,42,52,76,82,97,127],'actual omitted frame')
    rz=[root_vector(z)for z in Z];need([[dot(x,y)for y in rz]for x in rz]==[[18*int(i==j)for j in range(8)]for i in range(8)],'real orthogonal omitted basis')
    g=[{h:F(dot(z,rr[h]),18)for h in live}for z in rz]
    need(all(x in[F(0),F(1,2),-F(1,2)]for row in g for x in row.values()),'actual dyadic mode coefficients')
    for h in live:
        for j in live:need(sum(g[i][h]*g[i][j]for i in range(8))==G[h][j],'entire actual Gram factorization')
    need([[sum(g[i][h]*g[j][h]for h in live)for j in range(8)]for i in range(8)]==[[13*int(i==j)for j in range(8)]for i in range(8)],'native tight frame13')
    q=[{H[h][1]:g[i][h]for h in H if g[i][h]}for i in range(8)]
    r={h:plus({H[h][1]:-F(1)}if h in H else{}, {H[j][1]:G[h][j]for j in H if G[h][j]},1)for h in live}
    M=meta['mode_ports'];need(M==[19,30,38,40,47,52,60],'seven actual bank rows')
    need(rank([{j:F(x)for j,x in enumerate(rr[u])if x}for u in M])==7,'independent seven-dimensional real bank')
    root448=root_vector(448);need(all(dot(rr[u],root448)==0 for u in M),'bank is orthogonal to rho448')
    need([rr[17][j]-rr[19][j]-rr[38][j]+rr[40][j]for j in range(9)]==[0]*9,'r17 is redundant, not the missing eighth mode')
    T=meta['restored_ports'];S=meta['unrestored_ports'];perm={int(k):v for k,v in meta['permutation'].items()};need(len(T)in[20,44]and set(T).isdisjoint(S)and set(T+S)==set(H),'complete public D partition')
    for cycle in[T,S]:need(all(perm[h]==cycle[(i+1)%len(cycle)]for i,h in enumerate(cycle)),'literal two-cycle permutation')
    spaces=[span(f)for f in w['frames']];bank=meta['bank'];need(w['frames'][bank]==meta['bank_frame'],'literal bank basis')
    if len(T)==20:
        bankspace={0}
        for u in U:bankspace|={x^vv[u]for x in tuple(bankspace)}
        need(spaces[bank]==frozenset(bankspace)and set(T)=={h for h in H if vv[h]in bankspace},'exact20 target bank')
    else:
        need(spaces[bank]==frozenset(v for v in range(512)if (v&63).bit_count()%2==0),'bank44 means binary normal63, not native port63')
        need(set(T)=={h for h in H if dot(rr[h],root448)==0},'exact44 real hyperplane targets')
    facets={h:native['final'][h+112]for h in live};facetspaces={spaces[facets[h]]for h in H}
    need(spaces[bank]not in facetspaces,'proper bank is not any hosted final facet')
    for h in H:need(vv[perm[h]]in spaces[facets[h]],'permuted original line lies in actual final facet')
    stops={int(k):v for k,v in meta['stops'].items()};exclusion=[]
    for h in T:
        st=stops[h];need(spaces[st]==spaces[bank]&spaces[facets[h]],'literal proper stop intersection')
        need(len(w['frames'][st])==len(w['frames'][bank])-1<8 and vv[h]not in spaces[st]and vv[perm[h]]in spaces[st],'proper successor stop')
        beta=list(map(F,meta['beta'][str(h)]));need([sum(beta[i]*rr[u][j]for i,u in enumerate(M))for j in range(9)]==rr[h],'exact original-D real root reconstruction')
        need(comb(beta,[r[u]for u in M])==plus(r[h],{H[h][1]:F(1)},1),'actual bank identity d_h=-r_h+beta modes')
        outside=[j for j in H if j!=h and vv[j]not in spaces[st]];er=rank([{i:g[i][j]for i in range(8)if g[i][j]}for j in outside]);need(er==8,'outside rows exclude initial-local recovery')
        exclusion.append({'port':h,'outside_hosted_count':len(outside),'Gram_rank':er})
    return dict(role=role,live=live,X=X,Y=Y,H=H,U=U,aa=aa,vv=vv,rr=rr,G=G,g=g,q=q,r=r,M=M,T=T,S=S,perm=perm,spaces=spaces,bank=bank,stops=stops,facets=facets,facetspaces=facetspaces,exclusion=exclusion)


def audit(native,w,c,complete=True):
    H=c['H'];X=c['X'];Y=c['Y'];aa=c['aa'];r=c['r'];q=c['q'];M=c['M'];T=c['T'];S=c['S'];perm=c['perm'];bank=c['bank'];stops=c['stops'];spaces=c['spaces'];meta=w['relay'];marks=meta['markers']
    expected={}
    for h in c['live']:expected[X[h]]=aa[h];expected[Y[h]]={Y[h]:F(1)}
    for h,(b,d)in H.items():expected[b]=plus({b:F(1)},r[h],1);expected[d]={d:F(1)}if h in T else r[perm[h]]
    decoder_steps={z['step']:z['port']for z in meta['events']['decoded_owner']};restored_steps={z['step']:(z['port'],z['next_payload'])for z in meta['events']['restored_public']};seen=[];Breads=[];trace=[]
    Droles=[d for b,d in H.values()];Ds=set(Droles);inverse_perm={v:k for k,v in perm.items()}
    def check_time(t,rows,loc):
        if t==marks['entry_end']:
            need(all(rows[X[h]]==aa[h]and rows[Y[h]]=={Y[h]:F(1)}for h in c['live']),'actual old coupled entry retained');seen.append('entry')
        if t==marks['ground_preload']:
            need(all(rows[400+i]==q[i]and loc[400+i]==3 for i in range(8)),'eight actual original-D Gram acquisitions')
            need(all(rows[d]==r[h]and loc[d]==3 for h,(b,d)in H.items()),'actual dyadic ground preload')
            need(all(rows[408+i]==r[u]and loc[408+i]==3 for i,u in enumerate(M)),'seven modes acquired before original Gram records retire');seen.append('preload')
        if t==marks['permuted_preload']:
            need(all(rows[d]==r[perm[h]]and loc[d]==3 for h,(b,d)in H.items()),'actual explicit ground permutation');seen.append('permutation')
        if t==marks['all_B_reads']:
            need(all(rows[b]==expected[b]and loc[b]==127 for b,d in H.values()),'all actual B row reads and original ascents');seen.append('B')
        if t==marks['relay_start']:
            need(rows[400]==r[T[0]]and loc[400]==bank,'actual initial active payload at bank')
            need(all(rows[408+i]==r[u]and loc[408+i]==bank for i,u in enumerate(M)),'paid actual seven-mode bank');seen.append('relay_start')
        if t in decoder_steps:
            h=decoder_steps[t];need(rows[400]=={H[h][1]:F(1)}and loc[400]==bank,'actual original D decoded on owner at bank');seen.append(('decode',h))
        if t in restored_steps:
            h,nxt=restored_steps[t];need(nxt==perm[h]and rows[H[h][1]]=={H[h][1]:F(1)}and rows[400]==r[nxt],'actual singular swap restores D and transfers next preload')
            need(loc[H[h][1]]==loc[400]==stops[h],'restoration occurs at proper stop');seen.append(('restore',h))
        if t==marks['relay_end']:
            need(all(rows[H[h][1]]=={H[h][1]:F(1)}and loc[H[h][1]]==c['facets'][h]for h in T),'exact target D fields restored before endpoint closure');seen.append('relay_end')
        if complete and marks['ground_preload']<=t<=marks['ground_preload']+8:
            data=[rows[d]for d in Droles]+[row for i,row in rows.items()if i>=400]
            need(all(set(row)<=Ds for row in data),'post-entry owned rows are genuinely D-only')
            matrix=[[row.get(d,F(0))for d in Droles]for row in data]
            trace.append({'step':t,'owned_alive':len(rows)-400,'full_input_rank_mod3':304+ff_data(matrix,3)['rank']})
    B_to_h={b:h for h,(b,d)in H.items()}
    def hook(t,phase,op,rows,loc):
        if phase=='before':
            if op[0]=='MOVE'and not op[-1]:need(spaces[op[2]]<spaces[op[3]],'every public route is monotone upward')
            if op[0]=='ADD'and op[1]in B_to_h:
                h=B_to_h[op[1]];need(F(op[3])==1 and op[2]==H[inverse_perm[h]][1]and rows[op[2]]==r[h],'genuine original B read of its own acquired r_h')
                need(rows[op[1]]=={op[1]:F(1)}and loc[op[1]]==w['initial'][X[h]],'unknown original B retained at its original line');Breads.append(h)
        else:
            need(all(spaces[chart]not in c['facetspaces']for i,chart in loc.items()if i>=400),'no owned visit to any actual hosted final facet')
            check_time(t,rows,loc)
    result=replay(w,mode='independent_proper_relay',hook=hook)
    rows,loc,raw,owned,counts,peak,lifetimes,trace_unused,retire=result
    need(rows==expected,'all400 exact endpoint rows')
    need(all(loc[new]==native['final'][old]for old,new in c['role'].items()),'all400 exact final chart identifiers')
    need(sorted(Breads)==sorted(H),'all96 original B acquisitions exactly once')
    need(len(seen)==6+2*len(T),'every literal chronology cut checked')
    need(lifetimes==24 and peak==15 and len(retire)==24 and all(payload for t,i,ch,payload in retire),'all24 actual owned retirements are dirty')
    size=len(T);want_raw={1:96,2:20,5:20,7:76,8:304}if size==20 else{1:140,6:44,7:52,8:304};want_owned={1:47,6:1,7:7}if size==20 else{1:95,7:1,8:7}
    need(raw==want_raw and owned==want_owned,'complete actual raw/owned movement profiles')
    need(sum(k*v for k,v in raw.items())==3200,'all400 raw paths retain rank mass3200')
    for op in w['program']:
        if op[0]in('ADD','SCALE'):
            z=F(op[3]if op[0]=='ADD'else op[2]);need(z.denominator&(z.denominator-1)==0,'every actual introduced scalar is dyadic')
    if not complete:return True
    need(rank(list(rows.values()))==400,'independent exact rational full input rank400')
    small=[[F(i==j)-sum(c['g'][i][h]*c['g'][j][h]for h in S)for j in range(8)]for i in range(8)];det=determinant(small)
    need(det==(24387048 if size==20 else 480000),'remaining D determinant, exact8x8 reduction')
    reverse=rank([plus(rows[b],{b:F(1),d:-F(1)},-1)for b,d in H.values()]);need(reverse==8,'actual reverse residual rank8')
    need(sum(rows[Y[h]]!={Y[h]:F(1)}for h in c['live'])==0,'no paired forward progress')
    Dmatrix=[[rows[d].get(e,F(0))for e in Droles]for d in Droles]
    return {'size':size,'public_rank_over_Q':400,'original_D_restored':size,'original_D_remaining':96-size,'forward_targets_unfinished':104,'reverse_residual_rank':reverse,'remaining_D_determinant_up_to_permutation_sign':str(det),'counts':counts,'peak':peak,'lifetimes':lifetimes,'dirty_retirements':len(retire),'raw_histogram':raw,'owned_histogram':owned,'Q':dict(Counter(raw)+Counter(owned)),'chronology_checks':len(seen),'initial_local_decoder_exclusions':c['exclusion'],'ground_retirement_mod3_trace':trace},rows,Dmatrix

def ff_data(matrix,p):
    """Fresh prime-field elimination; return an explicit right-kernel basis."""
    a=[[F(x).numerator*pow(F(x).denominator,-1,p)%p for x in row]for row in matrix]
    n=len(a[0])if a else 0;piv=[];k=0
    for j in range(n):
        z=next((i for i in range(k,len(a))if a[i][j]),None)
        if z is None:continue
        a[k],a[z]=a[z],a[k];s=pow(a[k][j],-1,p);a[k]=[s*v%p for v in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                t=a[i][j];a[i]=[(u-t*v)%p for u,v in zip(a[i],a[k])]
        piv.append(j);k+=1
        if k==len(a):break
    null=[]
    for j in range(n):
        if j in piv:continue
        x=[0]*n;x[j]=1
        for i,col in enumerate(piv):x[col]=-a[i][j]%p
        null.append(x)
    original=[[F(x).numerator*pow(F(x).denominator,-1,p)%p for x in row]for row in matrix]
    need(all(sum(x*y for x,y in zip(row,v))%p==0 for row in original for v in null),'explicit finite-field kernel certificate')
    return {'rank':k,'pivots':piv,'kernel':null}

def coefficient_ring(c,rows,Dmat):
    H=c['H'];T=c['T'];Ds=[d for b,d in H.values()];n=len(T)
    q=[[r.get(d,F(0))for d in Ds]for r in c['q']]
    bank=[[c['r'][u].get(d,F(0))for d in Ds]for u in c['M']]
    candidates={20:[3,7,127],44:[3,5]}[n];expected={20:{3:94,7:95,127:94},44:{3:95,5:92}}[n]
    data=[]
    for p in candidates:
        result=ff_data(Dmat,p);need(result['rank']==expected[p],'exact terminal D prime-field rank')
        full_witness=[]
        for v in result['kernel']:
            w={d:x for d,x in zip(Ds,v)if x}
            for h,(b,d)in H.items():
                z=-sum((x.numerator*pow(x.denominator,-1,p)%p)*w.get(j,0)for j,x in c['r'][h].items())%p
                if z:w[b]=z
            need(all(sum((x.numerator*pow(x.denominator,-1,p)%p)*w.get(j,0)for j,x in row.items())%p==0 for row in rows.values()),'explicit nonzero400-input kernel annihilates every actual public endpoint')
            full_witness.append({str(j):x for j,x in sorted(w.items())})
        rank8=ff_data(Dmat+q,p)['rank'];rank7=ff_data(Dmat+bank,p)['rank']
        need(rank8==96 and rank7==(95 if p==3 else 96),'eight Gram rows repair every residual rank; seven miss rho448 at3')
        data.append({'prime':p,'public_D_rank':result['rank'],'full_public_rank':304+result['rank'],'deficit':96-result['rank'],'D_pivots':result['pivots'],'full_input_kernel_basis':full_witness,'with_eight_ground_modes_rank':rank8,'with_seven_relay_modes_rank':rank7})
    rr448=root_vector(448);w={d:F(dot(c['rr'][h],rr448),18)for h,(b,d)in H.items()};need(any(w.values()),'missing direction nonzero')
    need(all(w[H[h][1]]==0 for h in T),'rho448 direction vanishes on every restored target')
    need(all(sum(c['G'][h][j]*w[d]for j,(b,d)in H.items())==13*w[H[h][1]]for h in H),'missing real mode has Gram eigenvalue13')
    need(all(sum(x*w[j]for j,x in c['r'][u].items())==0 for u in c['U']),'all eight coupled bank rows annihilate rho448')
    coeff=[-F(1,2)]*4+[F(0)]*4
    need(comb(coeff,c['q'])=={d:x for d,x in w.items()if x},'missing mode qstar uses exactly first four ground Gram directions')
    coords=[[c['g'][i][u]for i in range(8)]for u in c['M']]
    need(determinant(coords+[coeff])==-F(1,8),'bank plus missing root mode is a dyadic basis')
    e1=[F(i==1)for i in range(8)];need(determinant(coords+[e1])==F(1,16),'bank plus raw ground q1 is a dyadic basis')
    if n==20:retained=[q[1],q[4]];names=['q1','q4']
    else:retained=[[a+b for a,b in zip(q[4],q[1])],q[5],q[6],q[7]];names=['q4+q1','q5','q6','q7']
    retained_ranks={p:ff_data(Dmat+retained,p)['rank']for p in candidates}
    need(all(r==96 for r in retained_ranks.values()),'explicit minimal retained scalar rows repair every odd determinant factor')
    need(len(retained)==max(96-expected[p]for p in candidates),'arithmetic number of retained rows is sharp')
    return {'coefficient_ring':'Z[1/2] and Z[1/2,i] by odd-prime residue fields','prime_controls':data,'missing_mode':{'real_root_normal':448,'ground_Gram_coefficients':list(map(str,coeff)),'bank_plus_qstar_determinant':'-1/8','bank_plus_q1_determinant':'1/16','coupled_r17_is_redundant':True},'minimum_additional_scalar_records':len(retained),'abstract_minimal_retention':{'rows':names,'ranks_at_all_odd_determinant_factors':retained_ranks,'scope':'Arithmetic row-module recoverability only; no cochart decoder, closure or invoice is asserted.'}}

def negative_controls(native,w,c):
    p=w['program'];B={b for b,d in c['H'].values()};marks=w['relay']['markers']
    first_q=next(i for i,o in enumerate(p)if i>=marks['entry_end']and o[0]=='ADD'and o[1]==400)
    first_bank=next(i for i,o in enumerate(p)if o[0]=='ADD'and o[1]==408)
    first_B=next(i for i,o in enumerate(p)if o[0]=='ADD'and o[1]in B)
    decode=w['relay']['events']['decoded_owner'][0]['step']-1
    swap=w['relay']['events']['first_swap'][0]
    tests=[('omit_actual_Gram_input',first_q),('omit_actual_bank_acquisition',first_bank),('omit_original_B_duty',first_B),('omit_original_D_reconstruction',decode),('break_singular_swap',swap)]
    out=[]
    for name,t in tests:
        bad=copy.deepcopy(w);need(bad['program'][t][0]=='ADD','mutation targets an actual scalar read');bad['program'][t][3]='0'
        try:audit(native,bad,c,False)
        except (ValueError,KeyError)as exc:out.append({'mutation':name,'instruction':t,'rejected_by':str(exc)})
        else:raise ValueError('mutated source incorrectly accepted: '+name)
    return out

def invoices(full,receipts):
    def combine(*terms):
        out={}
        for c,d in terms:
            for k,v in d.items():out[int(k)]=out.get(int(k),F(0))+F(c)*F(v)
        return {k:v for k,v in out.items()if v}
    slope=combine((F(1,18),full['invoice']['T']),(-F(1,18),full['invoice']['P']));penalty=combine((-1,slope));B=10**35;cache={}
    def bound(n):
        if n not in cache:
            N=n**199*B**200;lo=0;hi=n*B+1
            while hi-lo>1:
                a=(lo+hi)//2
                if a**200<=N:lo=a
                else:hi=a
            need(lo**200<=N<hi**200,'exact200th-power signed invoice bounds');cache[n]=(F(lo,B),F(hi,B))
        return cache[n]
    def moment(profile):
        lo=hi=F(0)
        for n,c in profile.items():
            a,b=bound(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
        return lo,hi
    pe=moment(penalty);need(pe[0]>0,'retained finite-m penalty positive');data=[]
    for r in receipts:
        margin=moment(combine((1,slope),(1,full['native']['paid']),(-1,full['native']['helpers']),(-1,r['Q'])))
        if r['size']==20:need(margin[0]-pe[1]>0,'twenty-source remaining room positive already at fixedm2');first=2
        else:need(margin[1]<0,'fortyfour partial source exceeds limiting allowance');first=None
        data.append({'size':r['size'],'limiting_room':margin,'first_positive_fixed_m':first})
    return {'exponent':'199/200','inherited_native_calls':18,'formula':'remaining_room(m)=limiting_room-finite_m_penalty/(m-1), fixed integer m>=2','finite_m_penalty':pe,'variants':data,'scope':'Incomplete-source remaining allowance only. All unfinished forward, D and coefficient-ring repair duties remain open.'}

def phases(author,parent,w,size):
    old={(o[2],o[3])for o in parent['program']if o[0]=='MOVE'};new={(o[2],o[3])for o in w['program']if o[0]=='MOVE'}-old
    data=load(author/str(size)/'PHASES.json');recs=data['recipes'];need(len(recs)==len(new)and{(r['source'],r['target'])for r in recs}==new,'complete actual newly introduced ordered-map coverage')
    path=author/'dependencies/native_verify.py';pin='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38';need(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'retained exact phase interpreter')
    spec=importlib.util.spec_from_file_location('retained_phase',path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    for r in recs:
        a,b=r['source'],r['target'];need(r['source_frame']==w['frames'][a]and r['target_frame']==w['frames'][b],'actual literal ordered frames')
        need(r['rank']==r['recipe']['rank']==abs(len(w['frames'][a])-len(w['frames'][b])),'nested map true rank')
        v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(w['frames'][a],9))+v.frame(w['frames'][b],9),'exact phase-inclusive recipe')
    bad=copy.deepcopy(recs[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
    try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(bad['source_frame'],9))+v.frame(bad['target_frame'],9),'wrong phase')
    except ValueError:pass
    else:raise ValueError('wrong phase accepted')
    return {'new_maps':len(new),'interpreter_sha256':pin,'wrong_phase_rejected':True,'classification':'Pinned retained-interpreter certificate reproduction; not a fresh independent phase algorithm.'}

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v)for v in x]
    return x

def main():
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=DEFAULT_AUTHOR);p.add_argument('--repo',type=Path,default=BASE/'programme');p.add_argument('--source-deps',type=Path,default=BASE/'worker-b/singular-gram-history/dependencies');p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));p.add_argument('--skip-phases',action='store_true');a=p.parse_args()
    files={'proof':a.author/'PROOF.md','native':a.source_deps/'native.json.gz','full':a.source_deps/'FULL-RESULT.json','parent':a.repo/'research/moonshot-005-program/results/complex-compensated-ferries/general/author/source-evidence/rail-consumer.json.gz',**{str(z):a.author/str(z)/'WORD.json.gz'for z in[20,44]}}
    for key,path in files.items():need(hashlib.sha256(path.read_bytes()).hexdigest()==PINS[key],'exact source pin '+key)
    native=load(files['native']);parent=load(files['parent']);full=load(files['full']);receipts=[]
    for size in[20,44]:
        w=load(files[str(size)]);c=prep(native,parent,w);r,rows,Dmat=audit(native,w,c);r['coefficient_ring']=coefficient_ring(c,rows,Dmat);r['negative_controls']=negative_controls(native,w,c)
        if not a.skip_phases:r['phase_certificates']=phases(a.author,parent,w,size)
        receipts.append(r);print(json.dumps({'size':size,'status':'PASS','rational_rank':400,'minimum_extra_arithmetic_records':r['coefficient_ring']['minimum_additional_scalar_records'],'negative_controls':len(r['negative_controls'])}),flush=True)
    result={'status':'PASS_INDEPENDENT_PROPER_CHART_RELAY_REVIEW_WITH_NEW_COEFFICIENT_RING_GATE','source_pins':PINS,'variants':receipts,'invoice':invoices(full,receipts),'scope':'Universal relay lemma accepted and actual400-input source checked. Q input survival does not imply continuation over dyadic coefficients. No complete source or new kappa.'}
    a.output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n');print('PASS: exact source, chronology, complete prices, residue obstructions and sharp abstract retention controls')

if __name__=='__main__':main()
