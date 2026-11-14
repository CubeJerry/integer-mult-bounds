#!/usr/bin/env python3
"""Exact source/positive/boundary controls for the unitary entropy theorem.
No author builder or checker imported. @CubeJerry with OpenAI assistance.
"""
import argparse,gzip,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parents[3]
SOURCE=BASE/'worker-b/logical-involution-112/output/R0-minimal/WORD.json.gz'
BUDGET=BASE/'worker-a/physical-involution-interface/BUDGET.json'
INTERFACE=BASE/'worker-a/physical-involution-interface/PROOF.md'
PINS={'source':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336','budget':'c86ce38b4339215bc730a658c1116c94e0f1e6cc973b6e13470192db02e2bfe7','interface':'d7c9374323ba3e4fdb2cc4781b1b3c41ad7890426db308328946d327968022d8'}
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def cadd(a,b):return(a[0]+b[0],a[1]+b[1])
def cmul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cscale(a,c):return(a[0]*c,a[1]*c)
def conj(a):return(a[0],-a[1])
Z=(F(0),F(0));ONE=(F(1),F(0));I=(F(0),F(1))
def mm(A,B):return[[sumc([cmul(A[i][k],B[k][j])for k in range(len(B))])for j in range(len(B[0]))]for i in range(len(A))]
def sumc(vals):
    out=Z
    for v in vals:out=cadd(out,v)
    return out
def eye(n):return[[ONE if i==j else Z for j in range(n)]for i in range(n)]
def adj(A):return[[conj(A[j][i])for j in range(len(A))]for i in range(len(A[0]))]
def kron(A,B):return[[cmul(a,b)for a in rowa for b in rowb]for rowa in A for rowb in B]

def native_controls(w):
    d=w['logical_involution'];P=d['ports'];q={int(h):x for h,x in d['normals'].items()};R={int(h):{int(j):F(x)for j,x in row.items()}for h,row in d['R_rows'].items()}
    need(len(P)==112 and len(set(q.values()))==112 and all(q.values()),'112 distinct nonzero actual normals')
    need(all(len(R[h])==4 and all(abs(c)==F(1,2)and j!=h for j,c in R[h].items())for h in P),'four true half-coefficient neighbors per row')
    need(all(sum(R[h].get(j,F(0))*R[k].get(j,F(0))for j in set(R[h])|set(R[k]))==int(h==k)for h in P for k in P),'actual whole-port R0 is orthogonal')
    half=d['halves'];need(len(half)==28,'actual28 halfclass unitary blocks')
    need(sorted(h for z in half for h in z['ports'])==sorted(P)and sorted(h for z in half for h in z['sources'])==sorted(P),'both halfclass partitions cover all ports exactly')
    for z in half:
        T,S=z['ports'],z['sources'];need(len(T)==len(S)==4,'true four-port blocks')
        need(all(set(R[h])==set(S)for h in T),'literal block support')
        need(all(sum(R[h][j]*R[k][j]for j in S)==int(h==k)for h in T for k in T),'each signed four-port block is orthogonal')
    rows=[]
    for V in (1,2,3):
        for h in P:
            out={}
            for j,c in R[h].items():
                base={0:(F(1,2),F(0)),q[h]:(F(0),F(1,2)),q[j]:(F(0),F(-1,2)),q[h]^q[j]:(F(1,2),F(0))}
                need(len(base)==4,'independent normal pair and true four translations')
                for t in itertools.product(base,repeat=V):
                    coef=ONE
                    for x in t:coef=cmul(coef,base[x])
                    out[(j,t)]=cscale(coef,c)
            need(len(out)==4**(V+1),'exact full bank tensor row support')
            norms=[a*a+b*b for a,b in out.values()]
            need(all(x==F(1,4**(V+1))for x in norms)and sum(norms)==1,'uniform exact Gaussian rational row and norm')
            if V==2:need(sum((a*a+b*b)*R[h][j]**2 for (j,t),(a,b)in out.items())==F(1,4),'actual wrong tensor-powered bank coefficients lose row norm')
        rows.append({'V':V,'all_rows':112,'entries_per_row':4**(V+1),'row_entropy_bits':2*V+2,'normalized_main_entropy_bits':224*(V+1)})
    return {'R0_orthogonal':True,'all112_distinct_normals':True,'all448_neighbor_pairs_independent':True,'four_port_unitary_blocks':28,'ordinary_R0_entropy_allowance':224,'sharp_positive_rank_mass':224,'sharp_positive_moment':224,'finite_width_rows':rows,'wrong_tensor_scalar_norm_at_V2':'1/4'}

def clean_ancilla_control():
    a=(F(1,2),F(1,2));J=[[a,a],[a,cscale(a,-1)]];need(mm(adj(J),J)==eye(2),'dyadic two-port J is exactly unitary')
    A=kron(J,eye(2));P=eye(4);P[2],P[3]=P[3],P[2]
    W=mm(mm(adj(A),P),A);need(mm(W,W)==eye(4),'coherent parity W is involutive')
    S=eye(4);S[2][2]=I;S[3][3]=I
    U=mm(mm(W,S),W);C=[[(F(1,2),F(1,2)),(F(1,2),F(-1,2))],[(F(1,2),F(-1,2)),(F(1,2),F(1,2))]]
    need([row[:2]for row in U[:2]]==C and all(U[i][j]==Z for i in (2,3)for j in (0,1)),'actual C_q with a clean restored zero field')
    need(mm(adj(U),U)==eye(4),'complete direct-sum operator remains unitary')
    wrong=mm(S,W);need(any(wrong[i][j]!=Z for i in (2,3)for j in (0,1)),'omitting final W leaves data in ancilla')
    return {'exact_clean_ancilla_one_column_Cq':True,'two_port_unitary_occurrences_per_column':4,'port_entropy_allowance_per_column':8,'Gaussian_calls':0,'all_width_N_countercontrol_C_port':'1792*V+224','omitted_final_W_rejected':True,'scope':'Countercontrol only when linear-in-V ordinary port work is allowed; violates the theorem\'s o(V) hypothesis.'}

def root_bracket(n,power=199):
    D=10**36;target=n**power*D**200;lo,hi=0,n*D+1
    while hi-lo>1:
        x=(hi+lo)//2
        if x**200<=target:lo=x
        else:hi=x
    need(lo**200<=target<hi**200,'exact rational200th-root enclosure')
    return F(lo,D),F(hi,D)
def bounds(budget):
    z=budget['sources']['R0-MINIMAL-WORD.json.gz'];out=[]
    rt=root_bracket(9,1)
    for b,key in [(1,'single_bank_ceiling'),(2,'two_bank_ceiling')]:
        mass=224*b;capfree=root_bracket(mass);capped=(F(mass)/rt[1],F(mass)/rt[0]);allowance=tuple(map(F,z[key]['rational_interval']))
        need(capfree[0]>allowance[1]and capped[0]>capfree[1],'both exact paid-moment bounds exceed conditional service allowance')
        out.append({'independent_N_banks':b,'asymptotic_rank_mass':mass,'cap_free_moment_interval':list(map(str,capfree)),'cap_free_display':float(capfree[0]),'rank_at_most9_moment_interval':list(map(str,capped)),'rank_at_most9_display':float(capped[0]),'conditional_allowance_interval':list(map(str,allowance)),'conditional_allowance_display':float(allowance[1]),'exact_comparison_passed':True})
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=SOURCE);p.add_argument('--budget',type=Path,default=BUDGET);p.add_argument('--interface',type=Path,default=INTERFACE);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args()
    for key,path in [('source',a.source),('budget',a.budget),('interface',a.interface)]:need(hashlib.sha256(path.read_bytes()).hexdigest()==PINS[key],'authenticated source pin '+key)
    w=load(a.source);budget=load(a.budget)
    out={'status':'PASS_EXACT_UNITARY_NORMALIZER_ENTROPY_PREMISES_AND_CONTROLS','source_pins':PINS,'source_controls':native_controls(w),'ordinary_budget_boundary_control':clean_ancilla_control(),'moment_bounds':bounds(budget),'universal_inequality':'V*S_V+C_port(V)>=224*b*(V+1)','cap_free_asymptotic_moment':'liminf sum r^t >= (224*b)^t when C_port=o(V)','proof_status':'Universal entropy and clean-ancilla argument in PROOF.md; this checker authenticates finite source premises, exact controls and rational comparisons.','scope':'Unitary Gaussian/monomial/port gates, zero restored direct-sum ancillas, absolute paid moment, no productive helper credits. Arbitrary nonunitary arithmetic and redesigned caller endpoints are not excluded. No new kappa.'}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'normalizer_rows':out['source_controls']['finite_width_rows'],'bounds':[{k:v for k,v in r.items()if 'display'in k or k=='independent_N_banks'}for r in out['moment_bounds']],'clean_ancilla_control':True}))
if __name__=='__main__':main()
