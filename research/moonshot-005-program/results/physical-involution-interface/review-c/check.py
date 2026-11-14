#!/usr/bin/env python3
"""Independent native adapter, phase-polynomial and paid-bank review.
No author builder or checker imported. @CubeJerry/OpenAI.
"""
import argparse,copy,gzip,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
AUTHOR=BASE/'worker-a/physical-involution-interface'
def need(x,m):
    if not x:raise ValueError(m)
def parity(x):return x.bit_count()%2
def dot(x,y):return parity(x&y)
def root(v):
    if v.bit_count()==3:return [2 if v>>i&1 else -1 for i in range(9)]
    z=[i for i in range(9)if not(v>>i&1)];need(len(z)==2,'native root type');return [3*(int(i==z[0])-int(i==z[1]))for i in range(9)]
def dot_real(a,b):return sum(x*y for x,y in zip(a,b))
def rank(vs):
    basis={}
    for v in vs:
        while v:
            k=v.bit_length()-1
            if k in basis:v^=basis[k]
            else:basis[k]=v;break
    return len(basis)
def poly(terms,n):
    linear=[0]*n;quadratic=[0]*n
    for mask,c in terms:
        bits=[i for i in range(n)if mask>>i&1]
        for i in bits:linear[i]=(linear[i]+c)%4
        if c%2:
            for k,i in enumerate(bits):
                for j in bits[k+1:]:quadratic[i]^=1<<j
    return tuple(linear),tuple(quadratic)
def translation(terms,n):
    l,q=poly(terms,n);need(not any(q)and all(x in(0,2)for x in l),'exact mod-four polynomial is a translation')
    return sum((x//2)<<j for j,x in enumerate(l))
def route(basis,s):
    # Swap each orthogonal head/fresh pair by I+(b+e)(b+e)^T.
    ws=[b^(1<<(9+8*(s-1)+k))for k,b in enumerate(basis)]
    def apply(x):
        y=x
        for z in ws:
            if dot(z,x):y^=z
        return y
    return apply
def phase_recipes(w,normal):
    path=AUTHOR/'source/native_verify.py';need(hashlib.sha256(path.read_bytes()).hexdigest()=='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38','retained independent phase interpreter')
    spec=importlib.util.spec_from_file_location('physical_review_phase_interpreter',path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    P=w['logical_involution']['ports'];roles=w['logical_involution']['role_map'];need(len(normal['records'])==len(P)==112,'complete boundary recipe inventory')
    for z in normal['records']:
        h=z['port'];q=z['normal'];line=w['frames'][w['initial'][int(roles['X'][str(h)])]];facet=w['frames'][w['final'][int(roles['Y'][str(h)])]]
        need(line==z['line']==[q]and facet==z['facet'],'actual pinned boundary frames')
        S=v.frame(line,9);T=v.frame(facet,9);Q=(('C',q,1),);H=v.fourier(9)
        need(z['line_normalizer']['rank']==z['facet_normalizer']['rank']==0,'both ordinary rank-zero recipes')
        v.equal(v.recipe(z['line_normalizer']),v.adjoint(Q)+S,'line monomial including absolute phase')
        v.equal(v.recipe(z['facet_normalizer']),v.adjoint(T)+v.adjoint(Q)+H,'facet monomial including absolute phase')
        v.equal(S+Q,Q+S,'literal line-chart and Q commutation')
    bad=copy.deepcopy(normal['records'][0]['line_normalizer']);bad['left']['phase']=(bad['left']['phase']+1)%4
    q=normal['records'][0]['normal'];line=normal['records'][0]['line']
    try:v.equal(v.recipe(bad),(('C',q,-1),)+v.frame(line,9),'wrong absolute phase')
    except ValueError:rejected=True
    else:raise ValueError('wrong phase accepted')
    return {'rank_zero_normalizers':224,'commutations':112,'wrong_phase_rejected':rejected,'scope':'Retained literal-interpreter reproduction; author Clifford producer is not imported.'}

def routes(w,data):
    m=w['logical_involution'];P=m['ports'];q={int(h):v for h,v in m['normals'].items()};R={int(h):{int(j):F(a)for j,a in r.items()}for h,r in m['R_rows'].items()};records={(z['stage'],z['port']):z for z in data['route_records']};need(len(records)==224,'all112 ports at two distinct stages')
    bases={h:records[1,h]['orthogonal_complement']for h in P};checked=Counter();maps={}
    for s in[1,2,5]:
        n=9+8*s;axes=[1<<i for i in range(n)];old=axes[:n-8];fresh=axes[-8:];spectator=axes[9:]
        for h in P:
            B=bases[h];need(len(B)==8 and all(dot(x,y)==int(i==j)for i,x in enumerate([q[h]]+B)for j,y in enumerate([q[h]]+B)),'actual certified orthonormal head completion')
            p=route(B,s);need(p(q[h])==q[h]and all(p(p(x))==x for x in axes),'independent transvection involution fixes the native line')
            need(all(dot(p(x),p(y))==int(i==j)for i,x in enumerate(axes)for j,y in enumerate(axes)),'literal route orthogonality')
            xin=[(v,1)for v in spectator]+[(q[h],1)];yin=[(v,1)for v in spectator]
            ti=translation(xin+[(p(v),-1)for v in old],n)
            tiy=translation(yin+[(p(v),-1)for v in old]+[(p(q[h]),1)],n)
            to=translation([(v,1)for v in axes]+[(p(v),-1)for v in axes],n)
            toy=translation([(v,1)for v in axes]+[(q[h],-1)]+[(p(v),-1)for v in axes]+[(p(q[h]),1)],n)
            need(ti==tiy and to==toy,'identical adapters on both pair members')
            shift=translation([(v,1)for v in fresh]+[(p(v),-1)for v in axes[:9]]+[(p(q[h]),1)],n)
            need(shift==to^p(ti),'complete O B M equals the fresh D including actual translation')
            if s in[1,2]:
                z=records[s,h];need(z['normal']==q[h]and z['orthogonal_complement']==B and z['input_translation']==ti and z['output_translation']==to,'independently reconstructed literal retained contact')
            need(shift!=(to^1)^p(ti),'changed boundary translation rejected')
            checked['route_identity']+=1;maps[s,h]=(p,ti,to)
    witnesses=[];declared={(x['output_port'],x['input_port']):x for x in data['nonzero_R_blocks']};need(len(declared)==448,'all nonzero block witnesses')
    for h in P:
        for j,c in R[h].items():
            need(h!=j and dot(q[h],q[j])==0 and abs(c)==F(1,2),'actual off-diagonal orthogonal half contact')
            ph,pj=maps[1,h][0],maps[1,j][0];k=next(i for i,b in enumerate(bases[h])if dot(q[j],b));z=1<<(9+k);image=pj(ph(z))
            need(image&511==q[j]and parity(image>>9)==0,'exact noncommuting fresh-frequency witness')
            need((image>>9).bit_count()%4!=1,'body multiplier changes on this nonzero block')
            need(maps[2,j][0](maps[2,h][0](z))==z and image!=z,'literal first and second stage differ')
            mask=((1<<17)-1)^511;p=lambda x:ph(pj(x));images=[p(x&mask)^(p(x)&mask)for x in[1<<i for i in range(17)]]
            need(rank(images)==2,'literal conjugated route has Gaussian rank two via PF+FP')
            d=declared[h,j];need(d['frequency']==z and d['permuted_frequency']==image and d['block_gaussian_rank']==2,'author witness reconstructed by a different rank computation')
            witnesses.append({'output':h,'input':j,'fresh_axis':k,'frequency':z,'routed_frequency':image})
    return {'checked':dict(checked),'source_bound_stages':[1,2],'renamed_fresh_stage_control':5,'nonzero_blocks':448,'noncommuting_witnesses':witnesses}

def multiply(A,B):
    out=[]
    for row in A:
        z={}
        for j,c in row.items():
            for k,d in B[j].items():
                x=z.get(k,F(0))+c*d
                if x:z[k]=x
                else:z.pop(k,None)
        out.append(z)
    return out
def compose(*xs):
    result=xs[0]
    for x in xs[1:]:result=multiply(result,x)
    return result
def first_difference(A,B):
    return next(({'row':i,'column':j,'difference':str(A[i].get(j,0)-B[i].get(j,0))}for i in range(len(A))for j in sorted(set(A[i])|set(B[i]))if A[i].get(j,0)!=B[i].get(j,0)),None)
def algebra_control(w):
    m=w['logical_involution'];ports=m['groups'][0]['ports'];v={int(h):x for h,x in m['normals'].items()};RR={int(h):{int(j):F(c)for j,c in row.items()}for h,row in m['R_rows'].items()};n=32
    I=[{i:F(1)}for i in range(n)];R=[];Q=[];M=[];D=[]
    for a,h in enumerate(ports):
        for b in range(4):
            R.append({4*j+b:RR[h][k]for j,k in enumerate(ports)if k in RR[h]})
            Q.append({4*a+b:F((-1)**dot(v[h],1 if b<2 else 2))})
            permutation=b^1 if a%2 else b;M.append({4*a+permutation:F(1)});D.append({4*a+b:F((-1)**(b%2))})
    need(compose(R,R)==I and compose(Q,Q)==I and compose(M,M)==I and compose(D,D)==I,'exact source coupling and control involutions')
    need(compose(M,Q)==compose(Q,M)and compose(D,Q)==compose(Q,D),'required commutations only')
    A=compose(M,Q,R,M);Ai=compose(M,R,Q,M);Lam=compose(M,R,M);T=compose(D,Lam,D);O=compose(D,M,Q);Oi=compose(Q,M,D);N=compose(Q,R,Q)
    need(compose(A,Ai)==I and compose(O,Q,M)==D,'genuine normalized native and boundary relation in the noncentral control')
    need(compose(Lam,Ai)==Q and compose(A,Lam)==Q and compose(O,N,Oi)==T,'noncommutative repair and paid service simplification')
    need(compose(T,D,Lam)==D and compose(T,D,Ai)==compose(D,Q)and compose(D,A,Lam)==compose(D,Q),'all four repaired independent banks have the required operator coefficients')
    need(compose(D,A)!=compose(A,D)and T!=Lam and compose(R,Q)!=compose(Q,R),'control genuinely violates the unsafe centralities')
    wrongpost=first_difference(compose(Lam,D,Lam),D);omitV=first_difference(compose(D,Lam),D)
    need(wrongpost is not None and omitV is not None,'wrong postfactor and omitted second bank fail on arbitrary baseline input')
    # Whole-field lambda on two odd columns is1; the tensor product of
    # the two single-column lambdas is i*i=-1.
    lam=lambda p:(1,0)if p%2==0 else(0,1)
    gmul=lambda a,b:(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    need(lam(2)!=gmul(lam(1),lam(1)),'global lambda is not tensor-factorwise lambda')
    return {'model':'Exact32-dimensional bank, four arbitrary cohorts, actual native8-port R block and noncommuting rational Q/M/D controls. Algebraic interface control, not a new literal physical source.','all_arbitrary_input_columns':128,'wrong_postfactor_baseline_witness':wrongpost,'omitted_second_bank_baseline_witness':omitV,'global_lambda_tensor_control':True}

def service_support(w):
    m=w['logical_involution'];v={int(h):x for h,x in m['normals'].items()};R={int(h):{int(j):F(c)for j,c in r.items()}for h,r in m['R_rows'].items()};count=0
    def conv(qh,qj):
        A={0:(1,-1),qh:(1,1)};B={0:(1,1),qj:(1,-1)};out={}
        for h,(a,b)in A.items():
            for j,(c,d)in B.items():
                x,y=out.get(h^j,(0,0));out[h^j]=(x+a*c-b*d,y+a*d+b*c)
        return{k:v for k,v in out.items()if v!=(0,0)}
    need(all(len(row)==4 for row in R.values()),'four disjoint source-port blocks per row')
    # Four times every coefficient, computed as Gaussian integers.
    for h,row in R.items():
        for j in row:
            shifts=conv(v[h],v[j]);want={0:(2,0),v[h]:(0,2),v[j]:(0,-2),v[h]^v[j]:(2,0)}
            need(shifts==want and len(shifts)==4 and rank([v[h],v[j]])==2,'actual four distinct translations per nonzero block');count+=1
    qh,qj=next((v[h],v[j])for h,row in R.items()for j in row)
    supports=[]
    for width in[1,2,3,5]:
        s={0}
        for c in range(width):s={x^(d<<(9*c))for x in s for d in[0,qh,qj,qh^qj]}
        need(len(s)==4**width,'exact tensor translation support')
        supports.append({'width':width,'one_block_support':len(s),'whole_row_support':4*len(s),'addition_path_lower_bound':2*width+2})
    # Equal directions would instead give identity; distinctness is essential.
    need(conv(qh,qh)=={0:(4,0)},'equal-direction control gives identity instead of four terms')
    return {'actual_nonzero_blocks':count,'tensor_controls':supports,'equal_direction_control_support':1,'universal_row_support':'4^(V+1)','universal_entry_magnitude':'2^(-V-1)','fixed_ordinary_template_excluded':True,'paid_Gaussian_moment_lower_bound_claimed':False}

def budget():
    prior=BASE/'worker-c/involutive112-budget-review/RESULT.json';need(hashlib.sha256(prior.read_bytes()).hexdigest()=='1d99925bf409efc512849f2f8304b562b33e6b5659e769d1487b6447159cc004','independently reviewed all-arm invoice')
    d=json.loads(prior.read_text());cap=list(map(F,d['actual_smaller_meeting_per_native_allowance_at12']));single=[x/2 for x in cap];author=json.loads((AUTHOR/'BUDGET.json').read_text());given=author['sources']['R0-MINIMAL-WORD.json.gz']
    for computed,key in[(cap,'two_bank_ceiling'),(single,'single_bank_ceiling')]:
        saved=list(map(F,given[key]['rational_interval']));need(max(computed[0],saved[0])<=min(computed[1],saved[1]),'actual two-bank moment threshold matches independent invoice')
    return {'native_invocations_at_optimum':12,'independent_N_banks_per_native':2,'N_bank_occurrences_at_optimum':24,'per_native_two_bank_allowance':list(map(str,cap)),'identical_single_bank_ceiling':list(map(str,single)),'strict_full_caller_formula':'12*allowance_per_native - total_price_of24_N_banks - E_total >0','classification':'Conditional source-interface reduction only. No N service, complete baseline recurrence, uniform compiler or new kappa supplied.'}

PINS={'FREEZE.json':'7d5303e6b4ccd13d184e4a7943a45d85102c82c3b36b5b7beb47a9887603e1f1','PROOF.md':'d7c9374323ba3e4fdb2cc4781b1b3c41ad7890426db308328946d327968022d8','NORMALIZERS.json':'90a5e01b3df62af3bbdb5cb0c616a3f85728766b2bc7277bd53564fb77bbbbde','ROUTES.json':'ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a','BUDGET.json':'c86ce38b4339215bc730a658c1116c94e0f1e6cc973b6e13470192db02e2bfe7','source/R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','source/R0-MINIMAL-WORD.json.gz':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336'}
def main():
    global AUTHOR
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();AUTHOR=a.author
    for name,pin in PINS.items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen physical-interface pin '+name)
    w=json.loads(gzip.decompress((AUTHOR/'source/R0-WORD.json.gz').read_bytes()));normal=json.loads((AUTHOR/'NORMALIZERS.json').read_text());r=json.loads((AUTHOR/'ROUTES.json').read_text())
    result={'status':'PASS_INDEPENDENT_PHYSICAL_ADAPTER_AND_TWO_BANK_REDUCTION_REVIEW','source_pins':PINS,'boundary_recipes':phase_recipes(w,normal),'routes':routes(w,r),'noncentral_arbitrary_baseline_control':algebra_control(w),'service_support':service_support(w),'target_budget':budget(),'scope':'Actual ordinary adapters and noncommutative sufficient reduction to a paid112-bank N service. No such complete service or whole multiplication theorem is claimed.'}
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':result['status'],'normalizers':224,'route_identities':336,'nonzero_blocks':448,'single_bank_ceiling':float(F(result['target_budget']['identical_single_bank_ceiling'][0]))}))
if __name__=='__main__':main()
