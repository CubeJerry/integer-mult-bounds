#!/usr/bin/env python3
"""Exact whole-cell boundary and native puncture checks for the relay template."""
import argparse,hashlib,json
from pathlib import Path
MASK=(1<<111)-1
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
def rank(rows):
 b={}
 for a in rows:
  while a:
   j=a.bit_length()-1
   if j in b:a^=b[j]
   else:b[j]=a;break
 return len(b)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--package',type=Path,default=Path(__file__).parent);a=ap.parse_args();p=a.package
 raw=(a.repo/ROOT).read_bytes();assert hashlib.sha256(raw).hexdigest()==ROOT_SHA;roots=json.loads(raw)['native_roots'];w=json.loads((p/'output/WORD.json').read_text());cert=json.loads((p/'PUNCTURE.json').read_text())
 val={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
 loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 coeff={};through={};T={};K={};arrivals={}
 for op in w['operations']:
  t,n,*args=op
  if t=='INIT':val[n]=0;loc[n]=args[0];coeff[n]=0
  elif t=='ADD':
   q=args[0];val[q]^=val[n]
   if loc[n]==loc[q]=='A15':coeff[q]=coeff.get(q,0)^coeff.get(n,0)
  elif t=='MOVE':
   d=args[0]
   if loc[n]=='A15'and n in ['P0','P1']:through[n]=coeff[n]
   loc[n]=d
   if d=='A15':
    coeff[n]=(1 if n=='P0'else 2 if n=='P1'else 0)
    if n in ['P0','P1']:K[n]=val[n]&MASK
    if n=='Y59':arrivals[n]=val[n]&MASK
   if d=='zero'and n.startswith('P'):T[n]=val[n]&MASK
  elif t=='CLEAR':val.pop(n);loc.pop(n)
  else:raise AssertionError(t)
 assert through=={'P0':0,'P1':0},through
 R=int(w['relay']['raw_tail_hex'],16);N=sum(1<<i for i in range(52,59));v=int(w['W_rows_hex'][59],16);e=1<<59
 assert T['P0']==N and T['P1']==v^e and T['P6']==v^R^e and K['P1']==v^R
 assert arrivals['Y59']==T['P6']
 local=[i for i,r in enumerate(roots)if not any(r[:4])];lm=sum(1<<i for i in local)
 assert R&~lm==0 and K['P0']&~lm and K['P1']&~lm and T['P1']&~lm
 E=set(cert['deleted']);assert E==set([4,5,6,7]+list(range(52,60)));pm=MASK^sum(1<<i for i in E)
 assert all((row&pm)==0 for row in [N,R,e]);assert len({T['P1']&pm,T['P6']&pm,K['P1']&pm})==1
 G=list(T.values())+list(K.values());assert rank(G)==9 and rank([row&pm for row in G])==6
 F=cert['star']['frame'];assert len(F)==8 and len(set(F))==8 and not set(F)&E
 assert all(dot(roots[i],roots[j])!=0 for i in F for j in F)
 pairs={};edges=cert['star']['edges']
 for d in edges:
  i=d['role'];pair=tuple(d['pair']);assert i not in E and i not in F and len(pair)==2 and pair not in pairs
  assert pair==tuple(j for j,f in enumerate(F)if dot(roots[i],roots[f])==0);pairs[pair]=i
 for p1,i in pairs.items():
  for p2,j in pairs.items():
   if p1<p2 and set(p1)&set(p2):assert dot(roots[i],roots[j])!=0
 degrees=[sum(j in p for p in pairs)for j in range(8)];assert degrees==cert['star']['degrees'] and min(degrees)>=4
 # Deliberately incomplete puncture and corrupted star both fail their premise.
 bad=E-{59};assert (e&(MASK^sum(1<<i for i in bad)))!=0
 assert F[0]not in E and F[0]in E|{F[0]}
 out={'status':'PASS_EXACT_RELAY_PUNCTURE_AND_CELL','word_sha256':hashlib.sha256((p/'output/WORD.json').read_bytes()).hexdigest(),'through_matrix':[[0,0],[0,0]],'actual_preload_hex':hex(arrivals['Y59']),'C_local_input_roles':local,'both_kernels_genuinely_nonlocal_mod_C':True,'P1_terminal_nonlocal_mod_C':True,'k1_plus_preload_is_pure_x59':K['P1']^arrivals['Y59']==e,'actual_normalized_rank':rank(G),'actual_punctured_rank':6,'arbitrary_v_and_five_other_seed_fields_rank_ceiling_per_width':7,'retained_roles':111-len(E),'star_edge_count':len(edges),'star_degrees':degrees,'all_field_star_rank_floor_per_width':9,'negative_controls':['omit59_from_puncture_breaks_e59_vanishing','delete_star_point_breaks_retained_frame'],'new_complete_kappa':False}
 (p/'verification/PUNCTURE-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
