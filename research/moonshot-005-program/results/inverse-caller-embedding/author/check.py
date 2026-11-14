#!/usr/bin/env python3
"""Independent inverse placements using actual Fourier monomial routes."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def parity(v):return v.bit_count()%2
def main(output):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for f,pin in pins.items():need(sha(HERE/f)==pin,'source pin '+f)
    f=json.loads(gzip.decompress((HERE/'source/FORWARD.json.gz').read_bytes()))
    inv=json.loads(gzip.decompress((HERE/'source/INVERSE.json.gz').read_bytes()))
    need(inv['initial']==f['final']and inv['final']==f['initial'],'actual reverse boundaries')
    expected=[]
    for op in reversed(f['program']):
        expected.append(['MOVE',op[1],op[3],op[2],False]if op[0]=='MOVE'else['ADD',op[1],op[2],str(-F(op[3])),op[4]])
    need(inv['program']==expected,'all1792 literal reversed instructions')
    paid=Counter(abs(len(inv['frames'][op[2]])-len(inv['frames'][op[3]]))for op in inv['program']if op[0]=='MOVE')
    need(paid==Counter({2:224,3:224,5:224,6:224})and Counter(op[0]for op in inv['program'])==Counter({'MOVE':896,'ADD':896}),'complete literal source invoice')
    price=json.loads((HERE/'source/INVERSE-PRICE.json').read_text());need(price['word_sha256']==pins['source/INVERSE.json.gz'],'actual inverse price pin')
    data=f['logical_involution'];P=data['ports'];R={int(h):{int(j):F(v)for j,v in row.items()}for h,row in data['R_rows'].items()}
    routes=json.loads((HERE/'source/ROUTES.json').read_text());rr={(x['stage'],x['port']):x for x in routes['route_records']}
    need(len(rr)==224 and set(s for s,h in rr)=={1,2},'two genuine fresh stages')
    n=25;tests=[0]+[1<<i for i in range(n)]+[(1<<i)^(1<<j)for i in range(n)for j in range(i)]
    counts=Counter();digests={}
    def perm(s,h,z):
        row=rr[s,h];start=9+8*(s-1);ans=z
        for k,b in enumerate(row['orthogonal_complement']):
            if parity(b&z)^((z>>(start+k))&1):ans^=b^(1<<(start+k))
        return ans
    def act(ops,z):
        ph=0
        for op in ops:
            tag=op[0]
            if tag in('M','O'):
                _,s,h,sign=op;row=rr[s,h];tr=row['input_translation'if tag=='M'else'output_translation']
                if sign==1:z=perm(s,h,z);ph+=2*parity(tr&z)
                else:ph+=2*parity(tr&z);z=perm(s,h,z)
            elif tag=='Q':_,h,exp=op;ph+=exp*parity(rr[1,h]['normal']&z)
            elif tag=='H':ph+=op[1]*(z&511).bit_count()
            elif tag=='D':_,s,exp=op;ph+=exp*((z>>(9+8*(s-1)))&255).bit_count()
            else:raise ValueError(tag)
        return z,ph%4
    def eq(label,a,b):
        values=[]
        for z in tests:
            aa=act(a,z);bb=act(b,z)
            need(aa==bb,label+' at '+str(z));values.append(aa)
        counts[label]+=1
        if label not in digests:digests[label]=hashlib.sha256()
        digests[label].update(json.dumps(values,separators=(',',':')).encode())
    def M(s,h,k=1):return('M',s,h,k)
    def O(s,h,k=1):return('O',s,h,k)
    def Q(h,k=1):return('Q',h,k)
    def D(s,k=1):return('D',s,k)
    for s in(1,2):
        for h in P:
            row=rr[s,h];q=row['normal'];basis=[q]+row['orthogonal_complement']
            need(len(basis)==9 and all(parity(x&y)==int(i==j)for i,x in enumerate(basis)for j,y in enumerate(basis)),'actual orthonormal head basis')
            need(q==int(data['normals'][str(h)]),'authentic normal')
            eq('M_inverse',[M(s,h),M(s,h,-1)],[]);eq('O_inverse',[O(s,h),O(s,h,-1)],[])
            eq('actual_O_B_M',[M(s,h),Q(h,-1),('H',1),O(s,h)],[D(s)])
            eq('inverse_all_role_diagonal',[O(s,h,-1),('H',-1),Q(h),M(s,h,-1)],[D(s,-1)])
            eq('pre_square_diagonal',[D(s,2),O(s,h,-1),('H',-1),Q(h),M(s,h,-1)],[D(s)])
            eq('post_square_diagonal',[O(s,h,-1),('H',-1),Q(h),M(s,h,-1),D(s,2)],[D(s)])
            eq('M_body_square_M_inverse',[M(s,h,-1),D(s,2),M(s,h)],[('H',2),Q(h,2)])
            eq('K_square_to_common_head_square',[M(s,h,-1),D(s,2),Q(h,2),M(s,h)],[('H',2)])
        for h in P:
            for j,c in R[h].items():
                need(c in(F(1,2),F(-1,2)),'actual source block coefficient')
                directY=[O(s,j,-1),('H',-1),M(s,h,-1)]
                directU=[O(s,j,-1),('H',-1),Q(j),Q(h),M(s,h,-1)]
                Ai=[M(s,j),Q(j,-1),M(s,h,-1)]
                A=[M(s,j),Q(h),M(s,h,-1)]
                Ar=[Q(j),O(s,j,-1),O(s,h)]
                Ari=[O(s,j,-1),O(s,h),Q(h,-1)]
                Rs=[M(s,j),M(s,h,-1)];Rt=[O(s,j,-1),O(s,h)]
                eq('actual_forward_Y_block',[M(s,j),Q(j,-1),Q(h,-1),('H',1),O(s,h)],Ai+[D(s)])
                eq('actual_forward_U_block',[M(s,j),('H',1),O(s,h)],A+[D(s)])
                eq('inverse_Y_block',directY,[D(s,-1)]+Ai)
                eq('inverse_U_block',directU,[D(s,-1)]+A)
                eq('pre_square_Y_block',[D(s,2)]+directY,[D(s)]+Ai)
                eq('pre_square_U_block',[D(s,2)]+directU,[D(s)]+A)
                eq('post_square_Y_block',directY+[D(s,2)],Ari+[D(s)])
                eq('post_square_U_block',directU+[D(s,2)],Ar+[D(s)])
                eq('reverse_coupling_transport',[D(s,-1)]+A+[D(s)],Ar)
                eq('K_Rs_equals_Rprime_K',Rs+[D(s),Q(h)],[D(s),Q(j)]+Rt)
                eq('K_Rprime_equals_Rs_K',Rt+[D(s),Q(h)],[D(s),Q(j)]+Rs)
                other=3-s;total=[D(1),D(2)]
                eq('Dtotal_forward_endpoint',A+total,total+Ar)
                eq('Dtotal_inverse_reverse_endpoint',Ari+total,total+[Q(j)]+Rs+[Q(h,2)])
                eq('cross_stage_body_commutes',[D(other)]+A,A+[D(other)])
    paths=0
    for h in P:
        for j,c in R[h].items():
            for k,b in R[j].items():
                a=[M(1,k),Q(j),M(1,j,-1),Q(j),O(2,j,-1),O(2,h)]
                ordinary=[M(1,k),M(1,j,-1),Q(j,2),O(2,j,-1),O(2,h)]
                eq('ordinary_reverse_forward_path',a,ordinary);paths+=1
    h=P[0];j=next(iter(R[h]));controls={}
    pairs={'omit_pre_Dsquare':([O(1,j,-1),('H',-1),M(1,h,-1)],[D(1),M(1,j),Q(j,-1),M(1,h,-1)]),
      'replace_reverse_by_forward':([D(1,-1),M(1,j),Q(h),M(1,h,-1),D(1)],[M(1,j),Q(h),M(1,h,-1)]),
      'wrong_inverse_U_Q_sign':([O(1,j,-1),('H',-1),Q(j,-1),Q(h),M(1,h,-1)],[D(1,-1),M(1,j),Q(h),M(1,h,-1)])}
    pairs['wrong_same_A_hybrid_target']=([O(1,j,-1),O(1,h),Q(h,-1),D(1)],[M(1,j),Q(j,-1),M(1,h,-1),D(1)])
    for name,(aa,bb)in pairs.items():
        z=next((z for z in tests if act(aa,z)!=act(bb,z)),None);need(z is not None,'negative phase control '+name)
        controls[name]={'frequency':z,'actual':act(aa,z),'wrong_target':act(bb,z)}
    result={'status':'PASS_ACTUAL_INVERSE_PLACEMENTS_AND_ENDPOINT_TRANSPORT','source_pins':pins,
      'ambient_bits_checked':n,'phase_polynomial_test_frequencies':len(tests),'quadratic_phase_identity_not_sampling':True,
      'exact_identity_counts':dict(counts),'identity_sha256':{k:v.hexdigest()for k,v in digests.items()},
      'ordinary_reverse_forward_paths':paths,'negative_controls':controls,'K_definition':'K_s=Q D_s',
      'source_gaussian_profile':dict(paid),'exact_source_moment':price['exact_moment'],
      'ordinary_inventory_per_inverse_embedded_call':{'input_O_inverse_port_monomials':448,'input_YV_NY_inverse_monomials':224,
       'output_XU_NX_inverse_monomials':224,'output_M_inverse_port_monomials':448,
       'destination_sign_conjugation_scalar_negations':448,'one_pre_or_post_body_square_translations':448},
      'ordinary_inventory_per_hybrid_embedded_call':{'all_forward_or_inverse_port_monomial_applications':1344,
       'inverse_plane_destination_scalar_negations':224,'inverse_plane_post_body_square_translations':224},
      'whole_caller_or_new_kappa':False,'scope':'Actual signed boundary/route identities for both inverse placements. Ordinary work remains paid by the retained tape model; no extra Gaussian job, owned field or erased information. Complete mixed caller endpoint and invoice remain separate.'}
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':result['status'],'counts':dict(counts),'paths':paths},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output/ROUTES.json');a=p.parse_args();main(a.output)
