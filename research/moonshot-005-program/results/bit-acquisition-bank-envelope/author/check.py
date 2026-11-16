#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib
import sympy as sp
def rank(rows):
 B={}
 for r in rows:
  while r:
   k=r.bit_length()-1
   if k in B:r^=B[k]
   else:B[k]=r;break
 return len(B)

def dual(rows,i):
 B={}
 for r,t in [(r,0)for r in rows]+[(1<<i,1)]:
  while r:
   p=r.bit_length()-1
   if p in B:r^=B[p][0];t^=B[p][1]
   else:B[p]=(r,t);break
  assert r or t==0
 v=0
 for p,(r,t)in sorted(B.items()):
  if ((r&v).bit_count()&1)^t:v|=1<<p
 assert v>>i&1 and all((v&r).bit_count()%2==0 for r in rows);return v

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();w=json.loads(a.word.read_text());raw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['source_sha256'];R=json.loads(raw)['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y));C={};ann={};local={}
 for ch,c in w['charts'].items():
  M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);B=M.rowspace()if c['kind']=='span'else M.nullspace();C[ch]=[list(v)for v in B];N=sp.Matrix(C[ch]).nullspace()if C[ch]else sp.eye(8).columnspace();ann[ch]=[list(v)for v in N];local[ch]=sum(1<<j for j in range(111)if all(dot(v,R[j])==0 for v in ann[ch]))
 val={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};owners=set();snap=[];cut=None
 isp=lambda n:n.startswith('P')and n[1:].isdigit()
 def save(n,k,phase):snap.append({'index':len(snap),'step':k,'packet':n,'chart':loc[n],'phase':phase,'row_hex':hex(val[n])})
 for k,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':val[n]=0;loc[n]=q[0];owners.add(n)
  elif op=='ADD':
   d=q[0]
   if isp(d)and loc[d]!='Hub':save(d,k,'before')
   val[d]^=val[n]
   if isp(d)and loc[d]!='Hub':save(d,k,'after')
  elif op=='MOVE':
   loc[n]=q[0]
   if isp(n)and loc[n]!='Hub':save(n,k,'arrival')
  elif op=='CLEAR':owners.remove(n);del val[n],loc[n]
  if k==w['milestones']['seed8_before_Y']:cut={'values':val.copy(),'charts':loc.copy(),'owners':sorted(owners)}
 assert cut;v=cut['values'];at=cut['charts'];xmask=(1<<111)-1;pure={n:r for n,r in v.items()if r&~xmask==0};ground=[r for n,r in pure.items()if not C[at[n]]];nonlocal_rows=[{'field':n,'chart':at[n],'dimension':len(C[at[n]]),'row_hex':hex(r),'outside_local_support':[j for j in range(111)if r>>j&1 and not(local[at[n]]>>j&1)]}for n,r in pure.items()if C[at[n]]and r&~local[at[n]]];
 d0=[7,11,12];d1=[0,28,44];replaced={f'KEEP_M{q["b"]}'for q in w['multi_retention']}|{f'ZKEEP{q["b"]}'for q in w['m1_retention']};fixed={n:r for n,r in pure.items()if n not in replaced}
 same=lambda x,y:len(C[x])==len(C[y])and(sp.Matrix(C[x]+C[y]).rank()if C[x]+C[y]else 0)==len(C[x])
 bank0=[r for n,r in pure.items()if same(at[n],'C0')];bank1=[r for n,r in pure.items()if same(at[n],'M1')];c0=next(c['roles']for c in w['cache_metadata']if c['family']==0);c1=next(c['roles']for c in w['cache_metadata']if c['family']==1 and len(c['receivers'])==3)
 out={'word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'fixed_lines':[d0,d1],'retained_bank_ranks':[rank(bank0),rank(bank1)],'visitor_enlarged_bank_ranks':[rank(bank0+[1<<j for j in c0]),rank(bank1+[1<<j for j in c1])],'source_visitors':[c0,c1],'global_bank_rows_hex':[hex(r)for r in ground+bank0+bank1+[1<<j for j in c0+c1]],'cases':{}}
 for mode in ['retained','all_visitor_captures','global_visitor_captures','all_visitor_captures_plus_three_points','global_visitor_captures_plus_three_points']:
  BB0=bank0+([1<<j for j in c0]if mode!='retained'else[]);BB1=bank1+([1<<j for j in c1]if mode!='retained'else[]);fitted=[];bad=[];invisible=[];receiver_rows=[]
  for i in range(111):
   rows=[r for n,r in fixed.items()if all(dot(v,R[i])==0 for v in C[at[n]])]+[1<<j for j in range(111)if dot(R[i],R[j])==0];seen0=any(dot(R[d],R[i])==0 for d in d0);seen1=any(dot(R[d],R[i])==0 for d in d1)
   if mode.startswith('global_'):seen0=seen1=True
   if mode.endswith('_plus_three_points'):rows +=[1<<j for j in [8,9,20]]
   if seen0:rows+=BB0
   if seen1:rows+=BB1
   if not seen0 and not seen1:invisible.append(i)
   receiver_rows.append(rows)
   if rank(rows+[1<<i])==rank(rows):fitted.append(i)
   else:bad.append({'receiver':i,'dual_hex':hex(dual(rows,i)),'sees_h0_channel':seen0,'sees_h1_channel':seen1})
  known=set(fitted);waves=[]
  while True:
   add=[i for i,rows in enumerate(receiver_rows)if i not in known and rank(rows+[1<<j for j in known]+[1<<i])==rank(rows+[1<<j for j in known])]
   if not add:break
   known.update(add);waves.append(add)
  closure_duals=[{'receiver':i,'dual_hex':hex(dual(rows+[1<<j for j in known],i))}for i,rows in enumerate(receiver_rows)if i not in known]
  out['cases'][mode]={'feedback_closure':sorted(known),'feedback_waves':waves,'closure_duals':closure_duals,'fitting_upper_set':fitted,'fitting_upper_count':len(fitted),'excluded_receivers':bad,'invisible_to_all_six_lines':invisible}
 native0=[j for j in range(111)if local['C0']>>j&1];native1=[j for j in range(111)if local['M1']>>j&1]
 assert set(native0+native1)==set(c0+c1)
 out['geometric_native_points']=[native0,native1]
 common=[int(r,16)for r in out['global_bank_rows_hex']];K=[(1<<i)^sum(1<<j for j in range(111)if dot(R[i],R[j])==0)for i in range(111)]
 out['common_global_rank']=rank(common);out['canonical_rank']=rank(K);out['canonical_intersection_rank']=rank(common)+rank(K)-rank(common+K);out['canonical_completion_upper_bound']=rank(common+K)-rank(common)
 assert [out['common_global_rank'],out['canonical_rank'],out['canonical_intersection_rank'],out['canonical_completion_upper_bound']]==[47,9,5,4]
 for i in range(111):assert rank(K+[1<<j for j in range(111)if dot(R[i],R[j])==0]+[1<<i])==rank(K+[1<<j for j in range(111)if dot(R[i],R[j])==0])
 out['positive_control']='Adding canonical C9 fits all111 receivers'
 out['dual_checks']=sum(len(c['excluded_receivers'])+len(c['closure_duals'])for c in out['cases'].values())
 assert out['dual_checks']==576
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print('banks',out['retained_bank_ranks'],out['visitor_enlarged_bank_ranks']);print({k:(v['fitting_upper_count'],[x['receiver']for x in v['excluded_receivers']])for k,v in out['cases'].items()})
if __name__=='__main__':main()
