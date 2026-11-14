#!/usr/bin/env python3
"""Independent exact Fourier-polynomial inverse-placement and hybrid review.
No author route/builder/replay imported. @CubeJerry/OpenAI assistance.
"""
import argparse,copy,gzip,hashlib,importlib.util,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parents[2];AUTHOR=BASE/'worker-b/inverse-caller-embedding'
N=25;ID=tuple(1<<i for i in range(N));PAIRS={(i,j):1<<k for k,(i,j)in enumerate((i,j)for i in range(N)for j in range(i+1,N))}
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def bits(x):
    while x:
        z=x&-x;yield z.bit_length()-1;x^=z
def dot(x,y):return(x&y).bit_count()%2
def apply(cols,x):
    r=0
    for i in bits(x):r^=cols[i]
    return r
def pull(cols,v):return sum(dot(c,v)<<i for i,c in enumerate(cols))
def phase(forms):
    lin=[0]*N;quad=0
    for v,c in forms:
        ii=list(bits(v))
        for i in ii:lin[i]=(lin[i]+c)%4
        if c%2:
            for a,i in enumerate(ii):
                for j in ii[a+1:]:quad^=PAIRS[i,j]
    return tuple(lin),quad

def op(cols=ID,forms=()):
    d=defaultdict(int)
    for v,c in forms:d[v]=(d[v]+c)%4
    return(tuple(cols),tuple(sorted((v,c)for v,c in d.items()if v and c)))
def compose(A,B):
    fa,pa=A;fb,pb=B
    return op(tuple(apply(fb,c)for c in fa),pa+tuple((pull(fa,v),c)for v,c in pb))
def product(*args):
    r=op()
    for A in args:r=compose(r,A)
    return r
def key(A):return A[0],phase(A[1])
def eq(A,B,label):need(key(A)==key(B),label)
def diag(forms):return op(forms=forms)
def Q(q,p=1):return diag(((q,p%4),))
def D(s,p=1):return diag(tuple((1<<(9+8*(s-1)+i),p%4)for i in range(8)))
def H(p=1):return diag(tuple((1<<i,p%4)for i in range(9)))
def route(B,s):
    def P(x):
        y=x
        for i,b in enumerate(B):
            v=b^(1<<(9+8*(s-1)+i))
            if dot(v,x):y^=v
        return y
    cols=tuple(P(1<<i)for i in range(N));need(all(apply(cols,c)==1<<i for i,c in enumerate(cols)),'literal route involution')
    return cols

def routes(w,records):
    d=w['logical_involution'];P=d['ports'];q={int(h):v for h,v in d['normals'].items()};R={int(h):{int(j):F(c)for j,c in row.items()}for h,row in d['R_rows'].items()};rec={(r['stage'],r['port']):r for r in records['route_records']}
    M={};Mi={};O={};Oi={};L={};Li={}
    for s in (1,2):
        for h in P:
            r=rec[s,h];B=r['orthogonal_complement'];cols=route(B,s);tau=r['input_translation'];sigma=r['output_translation']
            need(all(dot(a,b)==int(i==j)for i,a in enumerate([q[h]]+B)for j,b in enumerate([q[h]]+B)),'actual head orthonormal completion')
            need(apply(cols,q[h])==q[h],'route fixes its actual normal')
            M[s,h]=op(cols,((tau,2),));Mi[s,h]=op(cols,((apply(cols,tau),2),));O[s,h]=op(cols,((sigma,2),));Oi[s,h]=op(cols,((apply(cols,sigma),2),))
            eq(product(M[s,h],Mi[s,h]),op(),'input route and inverse including translation');eq(product(O[s,h],Oi[s,h]),op(),'output route and inverse including translation')
            eq(product(O[s,h],H(),Q(q[h],-1),M[s,h]),D(s),'actual forward body placement')
            eq(product(Mi[s,h],Q(q[h]),H(-1),Oi[s,h]),D(s,-1),'actual inverse diagonal')
            eq(product(M[s,h],Q(q[h],2),D(s,2),Mi[s,h]),H(2),'literal head characteristic square transport')
            L[s,h]=product(O[s,h],M[s,h]);Li[s,h]=product(Mi[s,h],Oi[s,h]);need(L[s,h][0]==ID,'O_s M_s is a pure translation');eq(product(L[s,h],D(s)),product(D(s),L[s,h]),'translation commutes with body')
    count=0;wrong=[];Dtot=product(D(1),D(2))
    for s in (1,2):
        for h in P:
            for j,c in R[h].items():
                Ap=product(Q(q[h]),Mi[s,h],M[s,j]);Api=product(Mi[s,h],Q(q[j],-1),M[s,j]);Am=product(O[s,h],Oi[s,j],Q(q[j]));Ami=product(Q(q[h],-1),O[s,h],Oi[s,j])
                rawY=product(Mi[s,h],H(-1),Oi[s,j]);rawU=product(Mi[s,h],Q(q[h]),Q(q[j]),H(-1),Oi[s,j])
                eq(rawY,product(Api,D(s,-1)),'actual inverse Y cross coefficient');eq(rawU,product(Ap,D(s,-1)),'actual inverse U cross coefficient')
                eq(product(rawY,D(s,2)),product(Api,D(s)),'pre-square inverse Y placement');eq(product(rawU,D(s,2)),product(Ap,D(s)),'pre-square inverse U placement')
                eq(product(D(s,2),rawY),product(D(s),Ami),'post-square inverse Y placement');eq(product(D(s,2),rawU),product(D(s),Am),'post-square inverse U placement')
                Rs=product(Mi[s,h],M[s,j]);Rp=product(O[s,h],Oi[s,j]);Kh=product(Q(q[h]),D(s));Kj=product(Q(q[j]),D(s))
                eq(product(Kh,Rs),product(Rp,Kj),'first actual K exchange');eq(product(Kh,Rp),product(Rs,Kj),'second actual K exchange')
                eq(product(Dtot,Ap),product(Rp,Q(q[j]),Dtot),'complete endpoint A+ transport')
                eq(product(Dtot,Ami),product(Q(q[h],2),Rs,Q(q[j]),Dtot),'complete endpoint inverse A- transport')
                other=3-s;eq(product(D(other),Ap),product(Ap,D(other)),'other fresh body commutes with A+');eq(product(D(other),Am),product(Am,D(other)),'other fresh body commutes with A-')
                eq(product(L[s,h],Api,Q(q[j],2),Li[s,j]),Am,'additional translation relation between A- and inverse A+')
                eq(product(Q(q[h],2),Li[s,h],Ami,L[s,j]),Ap,'preferred hybrid translation gauge gives common A+ coefficient')
                count+=1
                if key(Ami)!=key(Api):wrong.append([s,h,j])
    need(len(wrong)==896,'same-A replacement fails at every actual nonzero block')
    return P,q,R,M,Mi,O,Oi,{'diagonal_ports':224,'actual_nonzero_blocks':count,'cross_and_endpoint_identities':12*count,'additional_translation_gauge_identities':2*count,'same_A_replacement_failures':len(wrong),'first_wrong_same_A':wrong[0],'method':'Exact binary linear maps and canonical degree-two Z4 phase polynomials; no author route routine imported.'}

def ordinary_products(P,q,R,M,Mi,O,Oi):
    actual=defaultdict(lambda:defaultdict(F));expected=defaultdict(lambda:defaultdict(F));n=0
    for h in P:
        for k,a in R[h].items():
            for j,b in R[k].items():
                lhs=product(O[2,h],Oi[2,k],Q(q[k]),Q(q[k]),Mi[1,k],M[1,j])
                rhs=product(O[2,h],Oi[2,k],Q(q[k],2),Mi[1,k],M[1,j])
                eq(lhs,rhs,'complete actual A_t- A_s+ path with Q factors retained')
                actual[h,j][key(lhs)]+=a*b;expected[h,j][key(rhs)]+=a*b;n+=1
    a={p:{k:c for k,c in terms.items()if c}for p,terms in actual.items()};b={p:{k:c for k,c in terms.items()if c}for p,terms in expected.items()}
    need(a==b and n==1792,'sum all actual intermediate paths and scalar coefficients')
    return {'intermediate_paths':n,'summed_blocks':len(a),'retained_scalar_coefficients':True,'all_ordered_products_ordinary':True}
def span(B):
    S={0}
    for b in B:
        need(b not in S,'independent chart basis');S|={x^b for x in tuple(S)}
    return frozenset(S)
def add(a,b,c):
    r=a.copy()
    for k,v in b.items():
        z=r.get(k,F(0))+c*v
        if z:r[k]=z
        else:r.pop(k,None)
    return r

def hybrid_replay(w,reverse):
    need(w['public']==448 and w['owned_fields']==0,'448 arbitrary public inputs and no owner');S=list(map(span,w['frames']));rows={i:{i:F(1)}for i in range(448)};loc=list(w['initial']);counts=Counter();bill=Counter();orient=Counter();pairs=set()
    for o in w['program']:
        tag,i=o[:2];need(0<=i<448,'literal public role');counts[tag]+=1
        if tag=='MOVE':
            _,_,a,b,owned=o;need(owned is False and loc[i]==a,'actual raw departure chart');need(S[b]<S[a]if i in reverse else S[a]<S[b],'actual two-plane orientation');loc[i]=b;bill[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1;orient['descending'if i in reverse else'ascending']+=1;pairs.add((a,b))
        elif tag=='ADD':
            _,_,j,c,at=o;need(i!=j and 0<=j<448 and loc[i]==loc[j]==at and (i in reverse)==(j in reverse),'cocharted distinct arbitrary field in same plane');need(F(c)in(F(1,2),F(-1,2)),'original dyadic source coefficients');rows[i]=add(rows[i],rows[j],F(c))
        else:raise ValueError('nonreversible or unaccounted instruction '+tag)
    need(loc==w['final'],'all448 actual final charts')
    return rows,dict(bill),dict(counts),dict(orient),pairs

def hybrid_review(f,iv,P,R):
    role={k:{int(h):i for h,i in row.items()}for k,row in f['logical_involution']['role_map'].items()};xy=set(role['X'].values())|set(role['Y'].values());uv=set(role['B'].values())|set(role['D'].values());need(xy.isdisjoint(uv)and xy|uv==set(range(448)),'disjoint complete224-field planes')
    known={}
    for variant in ['FORWARD','INVERSE']:
        word=f if variant=='FORWARD'else iv
        for z in load(AUTHOR/f'source/{variant}-PHASES.json')['recipes']:
            a,b=z['source'],z['target'];need(z['source_frame']==word['frames'][a]and z['target_frame']==word['frames'][b],'inherited signed recipe actual frames');known[a,b]=z
    need(len(known)==560,'complete two-orientation signed map union')
    out=[]
    for name,reverse in [('inverse-XY',xy),('inverse-UV',uv)]:
        w=load(AUTHOR/f'output/{name}/WORD.json.gz');need(w['frames']==f['frames'],'all original chart frames retained')
        wantprog=[o for o in iv['program']if o[1]in reverse]+[o for o in f['program']if o[1]not in reverse];need(w['program']==wantprog,'exact original chronology retained within each plane')
        need(w['initial']==[f['final'][i]if i in reverse else f['initial'][i]for i in range(448)]and w['final']==[f['initial'][i]if i in reverse else f['final'][i]for i in range(448)],'literal mixed boundaries')
        rows,bill,counts,orient,pairs=hybrid_replay(w,reverse);want={i:{i:F(1)}for i in range(448)};sign=-1 if name=='inverse-XY'else 1
        for h in P:
            for j,c in R[h].items():
                want[role['Y'][h]]=add(want[role['Y'][h]],{role['X'][j]:F(1)},sign*c);want[role['B'][j]]=add(want[role['B'][j]],{role['D'][h]:F(1)},sign*c)
        need(rows==want,'all448 arbitrary hybrid inputs and exact outputs');need(all(rows[role['Y'][h]].get(role['X'][j],F(0))==rows[role['B'][j]].get(role['D'][h],F(0))for h in P for j in P),'all12544 same-sign hybrid coefficients')
        need(any(rows[role['Y'][h]].get(role['X'][j],F(0))+rows[role['B'][j]].get(role['D'][h],F(0))for h in P for j in P),'old opposite-adjoint contract actually fails')
        need(bill=={2:224,3:224,5:224,6:224}and counts=={'MOVE':896,'ADD':896}and orient=={'descending':448,'ascending':448},'full actual hybrid invoice and orientation')
        need(pairs==set(known),'all560 used signed ordered pairs covered');need(all(known[a,b]['rank']==abs(len(w['frames'][a])-len(w['frames'][b]))for a,b in pairs),'all exact ranks match invoice')
        bad=copy.deepcopy(w);o=next(o for o in bad['program']if o[0]=='ADD');o[3]=str(-F(o[3]));need(hybrid_replay(bad,reverse)[0]!=want,'wrong actual hybrid sign rejected')
        out.append({'variant':name,'all_input_columns':448,'coefficient_entries':12544,'counts':counts,'profile':bill,'orientations':orient,'signed_pairs':len(pairs),'wrong_sign_rejected':True,'opposite_adjoint_contract_rejected':True,'owners':0})
    return out

def phase_review(f,iv):
    path=AUTHOR/'source/native_verify.py';need(hashlib.sha256(path.read_bytes()).hexdigest()=='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38','retained signed interpreter pin')
    spec=importlib.util.spec_from_file_location('independent_embedding_retained_phase',path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    old={z['port']:z for z in load(AUTHOR/'source/NORMALIZERS.json')['records']};new=load(AUTHOR/'output/BOUNDARIES.json')['recipes'];need(len(new)==112 and {z['port']for z in new}==set(old),'all actual inverse boundary ports')
    n=0
    for z in new:
        for a,b in [('line_inverse','line_normalizer'),('facet_inverse','facet_normalizer')]:
            need(z[a]['rank']==0 and z[a]['right']is None,'actual boundary inverse has no Gaussian child')
            v.equal(v.recipe(z[a]),v.adjoint(v.recipe(old[z['port']][b])),'exact inverse ordinary boundary including global phase');n+=1
    p=0
    for variant,w in [('FORWARD',f),('INVERSE',iv)]:
        for z in load(AUTHOR/f'source/{variant}-PHASES.json')['recipes']:
            a,b=z['source'],z['target'];v.equal(v.recipe(z['recipe']),v.adjoint(v.frame(w['frames'][a],9))+v.frame(w['frames'][b],9),'every used forward or inverse signed physical map');p+=1
    bad=copy.deepcopy(new[0]['line_inverse']);bad['left']['phase']=(bad['left']['phase']+1)%4
    try:v.equal(v.recipe(bad),v.adjoint(v.recipe(old[new[0]['port']]['line_normalizer'])),'wrong global phase');rejected=False
    except ValueError:rejected=True
    need(rejected,'wrong inverse boundary phase rejected')
    return {'new_rank_zero_boundary_recipes':n,'all_inherited_forward_inverse_pairs_reproduced':p,'wrong_global_phase_rejected':True,'scope':'Pinned retained exact signed-interpreter reproduction, distinct from the independently written Z4 route algebra and arbitrary-input source replay.'}

PIN='97d6beb6e5759e331ea08eadbca60f982f417f6608e5393520cf25a8d27aa6ca'
def main():
    global AUTHOR
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();AUTHOR=a.author
    need(hashlib.sha256((AUTHOR/'MANIFEST.json').read_bytes()).hexdigest()==PIN,'frozen author manifest')
    manifest=load(AUTHOR/'MANIFEST.json')
    for name,pin in manifest['files'].items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'author file pin '+name)
    f=load(AUTHOR/'source/FORWARD.json.gz');iv=load(AUTHOR/'source/INVERSE.json.gz');records=load(AUTHOR/'source/ROUTES.json')
    P,q,R,M,Mi,O,Oi,rr=routes(f,records);products=ordinary_products(P,q,R,M,Mi,O,Oi);hybrids=hybrid_review(f,iv,P,R);phases=phase_review(f,iv)
    out={'status':'PASS_INDEPENDENT_INVERSE_PLACEMENT_AND_MIXED_BOUNDARY_REVIEW','author_manifest':PIN,'author_proof':manifest['files']['PROOF.md'],'source_pins':load(AUTHOR/'SOURCES.json')['pins'],'route_algebra':rr,'ordinary_ordered_products':products,'hybrid_sources':hybrids,'signed_phases':phases,'ordinary_inverse_inventory':{'input_O_inverse':448,'input_NY_inverse':224,'output_NX_inverse':224,'output_M_inverse':448,'extra_signs':448,'body_square_translations':448},'ordinary_hybrid_inventory':{'boundary_monomials':1344,'extra_signs':224,'body_square_translations':224},'additional_translation_gauge':{'L':'O_s M_s is a pure coordinate translation commuting with D_s,Q','relation':'A_s^- = L_s (A_s^+)^-1 Q^2 L_s^-1','preferred_XY_output_gauge':['L^-1','Q^2 L^-1'],'preferred_both_shear_coefficients':'A_s^+','complementary_XY_output_gauge':['L Q^2','L'],'complementary_both_shear_coefficients':'A_s^-','extra_monomial_applications':448,'input_gauges':'inverse of stated output gauges','status':'Additional independently derived source-bound lemma, proved separately in TRANSLATION-GAUGE.md; not a complete caller.'},'scope':'Actual arbitrary-input mixed-boundary sources, correct body placement, exact K_s endpoint transport. Original ascent-only schema and same-A HOST2 admission remain absent. No complete caller or new kappa. Grouped-one-call gate is separately scoped.'}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'routes':rr,'products':products,'hybrids':[{k:v for k,v in z.items()if k in('variant','all_input_columns','profile','orientations')}for z in hybrids],'phases':phases}))
if __name__=='__main__':main()
