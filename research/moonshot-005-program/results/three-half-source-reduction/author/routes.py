#!/usr/bin/env python3
"""Authenticate three fresh physical stages and emit the actual macro chronology."""
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def bit(x):return x.bit_count()%2
def main(out,codec_path):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for p,z in pins.items():need(hashlib.sha256((HERE/p).read_bytes()).hexdigest()==z,'source pin '+p)
    w=json.loads(gzip.decompress((HERE/'source/R0.json.gz').read_bytes()));data=w['logical_involution'];P=data['ports']
    R={int(h):{int(j):F(c)for j,c in row.items()}for h,row in data['R_rows'].items()}
    rr={(r['stage'],r['port']):r for r in json.loads((HERE/'source/ROUTES.json').read_text())['route_records']}
    for h in P:
        r=rr[1,h]
        for s in(2,3):
            q=copy.deepcopy(r);q['stage']=s
            for name in('input_translation','output_translation'):
                v=r[name];need(v<1<<17,'first route only head and first fresh block');q[name]=(v&511)|((v>>9)<<(9+8*(s-1)))
            if s==2:need(q==rr[s,h],'actual second stage is authentic fresh-block rename')
            else:rr[s,h]=q
    n=33;tests=[0]+[1<<i for i in range(n)]+[(1<<i)^(1<<j)for i in range(n)for j in range(i)]
    def perm(s,h,z):
        ans=z
        for k,b in enumerate(rr[s,h]['orthogonal_complement']):
            f=1<<(9+8*(s-1)+k)
            if bit(b&z)^bool(z&f):ans^=b^f
        return ans
    def act(ops,z):
        phase=0
        for op in ops:
            if op[0]in('M','O'):
                tag,s,h,sign=op;v=rr[s,h]['input_translation'if tag=='M'else'output_translation']
                if sign==1:z=perm(s,h,z);phase+=2*bit(v&z)
                else:phase+=2*bit(v&z);z=perm(s,h,z)
            elif op[0]=='Q':_,h,k=op;phase+=k*bit(rr[1,h]['normal']&z)
            elif op[0]=='H':phase+=op[1]*(z&511).bit_count()
            elif op[0]=='D':_,s,k=op;phase+=k*((z>>(9+8*(s-1)))&255).bit_count()
            else:raise ValueError(op[0])
        return z,phase%4
    counts=Counter();digest=hashlib.sha256()
    def eq(label,a,b):
        for z in tests:
            x=act(a,z);need(x==act(b,z),label);digest.update(str(x).encode())
        counts[label]+=1
    M=lambda s,h,k=1:('M',s,h,k);O=lambda s,h,k=1:('O',s,h,k);Q=lambda h,k=1:('Q',h,k);D=lambda s,k=1:('D',s,k)
    for s in(1,2,3):
        for h in P:
            r=rr[s,h];B=[r['normal']]+r['orthogonal_complement'];need(all(bit(x&y)==int(i==j)for i,x in enumerate(B)for j,y in enumerate(B)),'authentic head frame')
            eq('actual_O_B_M',[M(s,h),Q(h,-1),('H',1),O(s,h)],[D(s)])
            eq('M_Q_commute',[M(s,h),Q(h)],[Q(h),M(s,h)])
            eq('O_Q_commute',[O(s,h),Q(h)],[Q(h),O(s,h)])
            for t in(1,2,3):
                if t!=s:need(all(perm(s,h,1<<k)==1<<k for k in range(9+8*(t-1),9+8*t)),'other fresh body fixed')
            for j,c in R[h].items():
                need(c in(F(1,2),F(-1,2)),'authentic source coefficient')
                Fwd=[M(s,j),Q(h),M(s,h,-1)];Rev=[Q(j),O(s,j,-1),O(s,h)]
                Finv=[M(s,j),Q(j,-1),M(s,h,-1)];Ginv=[O(s,j,-1),O(s,h),Q(h,-1)]
                eq('own_body_forward_transport',[D(s,-1)]+Fwd+[D(s)],Rev)
                eq('own_body_inverse_reverse_transport',[D(s,-1)]+Ginv+[D(s)],[Q(j,2)]+Finv+[Q(h,2)])
    result={'status':'PASS_ACTUAL_THREE_STAGE_ROUTES','source_pins':pins,'route_records':[rr[s,h]for s in(1,2,3)for h in P],
       'ambient_bits':n,'complete_quadratic_phase_test_frequencies':len(tests),'exact_identity_counts':dict(counts),
       'identity_digest':digest.hexdigest(),'third_stage_constructed_by_actual_fresh_block_rename':True,
       'other_stage_body_commutation_from_disjoint_support':True,'uniform_lift_requires_retained_compiler':True}
    out.mkdir(parents=True,exist_ok=True);(out/'ROUTES3.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    program=[['SIGN_BANK',0,-1],['HALF_FORWARD_UV',1,0,1],['SIGN_BANK',0,-1],
      ['ORDINARY_BANK',0,['R2','Q_squared','Rprime1']],
      ['HALF_FORWARD_UV',2,1,0],['ORDINARY_BANK',1,['R3','Q_squared','Rprime2']],
      ['SIGN_BANK',0,-1],['HALF_FORWARD_UV',3,0,1],['SIGN_BANK',0,-1]]
    interface={'schema':'moonshot-S012-three-half-physical-interface-program-v1','public_banks':2,'ports_per_bank':112,
       'program':program,'ordinary_product_order':'written leftmost acts last','half_source_pin':pins['source/FORWARD-UV.json.gz'],
       'half_contract':'(U,V)->(D_s(U-F_s V),D_s V), F_s=Q R_s','ordinary_R_definition':'R_s=M_s^-1 R M_s; Rprime_s=O_s R O_s^-1',
       'R0_codec_sha256':hashlib.sha256(codec_path.read_bytes()).hexdigest(),
       'route_receipt_sha256':hashlib.sha256((out/'ROUTES3.json').read_bytes()).hexdigest(),
       'exact_target':['G2^-1 Dtot y','-G3^-1 G2^-1 G1^-1 Dtot x'],'G_definition':'G_s=Rprime_s Q','Dtot':'D1 D2 D3',
       'owned_or_zero_fields':0,'query_calls':0,'idle_calls':0,'gaussian_child_profile':{2:336,3:336,5:336,6:336},
       'old_native_caller_schema_admission':False,'productive_rank25_target_claimed':False,'new_kappa':False}
    (out/'INTERFACE-PROGRAM.json').write_text(json.dumps(interface,sort_keys=True,indent=2)+'\n');print(dict(counts))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE);p.add_argument('--codec',type=Path,default=HERE/'R0-CODEC.json');a=p.parse_args();main(a.output,a.codec)
