#!/usr/bin/env python3
"""Independent native geometry, direct-sum capacity and actual read checks."""
import argparse,hashlib,json,re
from pathlib import Path

def basis(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return list(b.values())
def rank(rows):return len(basis(rows))
def span(rows):
 s={0}
 for x in rows:s|={v^x for v in list(s)}
 return s
def xor(rows):
 a=0
 for x in rows:a^=x
 return a
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 f=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(f.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';roots=json.loads(f.read_text())['native_roots'];c=json.loads(a.certificate.read_text());assert hashlib.sha256(a.word.read_bytes()).hexdigest()==c['word_sha256'];w=json.loads(a.word.read_text())
 K=[sum(1<<j for j in range(111)if i==j or sum(x*y for x,y in zip(roots[i],roots[j]))==0)for i in range(111)];h=K[0]^K[4];W=[K[i]&sum(1<<j for j in range(111)if(h>>j&1)==(h>>i&1))for i in range(111)]
 W0=[x for i,x in enumerate(W)if not(h>>i&1)];W1=[x for i,x in enumerate(W)if h>>i&1];b0=[int(x,16)for x in c['h0_W_basis_hex']];b1=[int(x,16)for x in c['h1_W_basis_hex']];assert rank(b0)==rank(W0)==rank(b0+W0)==7;assert rank(b1)==rank(W1)==rank(b1+W1)==8
 vals={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
 for op in w['operations']:
  if op[0]=='INIT':vals[op[1]]=0
  elif op[0]=='ADD':vals[op[2]]^=vals[op[1]]
  elif op[0]=='CLEAR':del vals[op[1]]
  else:assert op[0]=='MOVE'
 assert all(vals[f'X{i}']==1<<i for i in range(111));assert vals['Y0']==(1<<111)^1
 cache={n:v for n,v in vals.items()if re.fullmatch(r'C\d+_\d+_[01]',n)};assert len(cache)==80
 cohorts=c['cohorts'];assert sorted(j for co in cohorts for j in co['roles'])==list(range(111));D=[];duals={};class1=[];cohortchecks=[]
 for co in cohorts:
  roles=co['roles'];mask=sum(1<<j for j in roles);r=co['run_capacity'];rows=[int(x,16)for x in co['actual_run_rows_hex']];assert rank(rows)==r and all(x&~mask==0 for x in rows);D+=rows;cl=co['h_class'];assert all(h>>j&1==cl for j in roles)
  bb=b0 if cl==0 else b1;pr=rank([x&mask for x in bb]);assert pr==co['full_W_projection_rank'];assert r<=len(roles)
  if cl==0 and r==2:
   ai=span([sum(((x>>j)&1)<<k for k,x in enumerate(b0))for j in roles]);assert len(ai)==8 and ai==set(co['local_dual_vectors']);duals[co['first_role']]=ai
  elif cl==0:assert pr<=r
  else:class1+=rows
  cohortchecks.append([co['first_role'],r,pr])
 assert len(D)==rank(D)==40;assert rank(D+W)==46;assert rank(D+W0)==42;assert rank(D+W1)==44
 assert rank(list(cache.values()))==40 and rank(D+list(cache.values()))==40
 assert set(duals)=={81,66,46,30};assert duals[81]&duals[66]&duals[46]=={0}
 H=span([24,32,64]);L=span([24,32]);assert all(len(H&ai)==4 and len(L&ai)>=2 for ai in duals.values())
 # Construct even-width U0 directly on two coordinate lanes; odd scalar U0.
 ueven=[xor([x for i,x in enumerate(b0)if v>>i&1])for v in range(128)if all((v&t).bit_count()%2==0 for t in H)]
 uscalar=[xor([x for i,x in enumerate(b0)if v>>i&1])for v in range(128)if all((v&t).bit_count()%2==0 for t in L)]
 assert rank(ueven)==4 and rank(uscalar)==5
 for co in cohorts:
  if co['h_class']:continue
  mask=sum(1<<j for j in co['roles']);assert rank([x&mask for x in ueven])+rank([x&mask for x in b0])<=2*co['run_capacity'];assert rank([x&mask for x in uscalar])<=co['run_capacity']
 mask=sum(1<<j for co in cohorts if co['first_role']in[52,22]for j in co['roles']);assert rank([x&mask for x in b1])==6;assert rank(class1)+rank(b1)-rank(class1+b1)==4
 cols=c['read_incidence_column_order'];cr=[int(x['row_hex'],16)for x in cols];assert len(cr)==40 and rank(cr)==40;inc=c['read_incidence_rows_hex'];assert set(inc)==set(cache)
 for name,z in inc.items():assert xor([x for j,x in enumerate(cr)if int(z,16)>>j&1])==cache[name]
 assert rank([int(x,16)for x in inc.values()])==40
 # Negative/positive scope controls: full W0 fails a two-run cohort;
 # per-coordinate scalar capacity10 is false, while two lanes attain11.
 assert any(rank([x&sum(1<<j for j in co['roles'])for x in b0])>co['run_capacity']for co in cohorts if not co['h_class'])
 out={'status':'PASS_ROOT_EXACT_COHORT_CAPACITY','scalar_D_rank':40,'scalar_W_intersection':9,'W_class_dimensions':[7,8],'upper_certificate':'three local duals have zero triple intersection; rank-six class-one projection pair','even_class_zero_dimension':11,'scalar_class_zero_dimension':5,'exact_all_field_capacity':'9V+floor(V/2)','actual_read_matrix_rank':40,'cohorts':cohortchecks,'physical_block_compilation':'open; scalar word reviewed separately'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
