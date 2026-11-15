#!/usr/bin/env python3
import argparse,json,hashlib
from pathlib import Path
from build import rank,independent,xor

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,default=Path(__file__).parent/'output/WORD.json');ap.add_argument('--out',type=Path,default=Path(__file__).parent/'CAPACITY.json');a=ap.parse_args();w=json.loads(a.word.read_text());W=[int(x,16) for x in w['W_rows_hex']];hm=int(w['W_pivot_h_hex'],16);M=(1<<111)-1;W0=independent([x&(M^hm) for x in W]);W1=independent([x&hm for x in W]);assert[len(W0),len(W1)]==[7,8]
 U0=[int(x,16) for x in w['reprogramming']['h0_target_rows_hex']];rows=[];details=[]
 for g in w['cohorts']:
  S=g['sources'];mask=sum(1<<i for i in S);R=[int(x,16) for x in g['run_rows_hex']];r=rank(R);rows+=R;private=[v for n,(c,v) in w['expected'].items() if n.startswith('C') and n.endswith('_g'+str(S[0]))]
  assert rank(R+private)==r==rank(private)
  if g['h_class']==0:assert rank(R+[x&mask for x in U0])==r
  details.append({'first_role':S[0],'h_class':g['h_class'],'run_count':len(g['runs']),'independent_run_capacity':r,'full_W_projection_rank':rank([x&mask for x in (W0 if not g['h_class'] else W1)]),'sources':S})
 assert rank(rows)==44 and rank(rows)+15-rank(rows+W)==10
 assert rank(rows)+7-rank(rows+W0)==6 and rank(rows)+8-rank(rows+W1)==4
 a30=next(g for g in w['cohorts'] if g['sources'][0]==30);a81=next(g for g in w['cohorts'] if g['sources'][0]==81)
 duals={}
 for g in [a30,a81]:
  assert len(g['runs'])==2
  cols=independent([sum(1<<j for j,row in enumerate(W0) if row>>i&1) for i in g['sources']]);assert len(cols)==3
  vectors=[xor(cols[j] for j in range(3) if v>>j&1) for v in range(8)];assert 88 in vectors;duals[str(g['sources'][0])]=sorted(vectors)
 assert set(duals['30'])&set(duals['81'])=={0,88}
 g52=next(g for g in w['cohorts'] if g['sources'][0]==52);g22=next(g for g in w['cohorts'] if g['sources'][0]==22);assert len(g52['runs'])==len(g22['runs'])==1
 sm=sum(1<<i for i in g52['sources']+g22['sources']);assert rank([x&sm for x in W1])==6
 out={'status':'PASS_PAIRED_FLAG_EXACT_CAPACITY_10V','source_word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'D_rank':44,'W0_rank':7,'W1_rank':8,'D_W0':6,'D_W1':4,'D_W_total':10,'total_run_visits':sum(g['run_count'] for g in details),'private_cache_owners':sum(n.startswith('C') for n in w['expected']),'class0_remaining_rank3_capacity2_duals':duals,'class0_annihilator_vector':88,'class1_one_run_union_projection_rank':6,'cohorts':details,'scope':'fixed new paired flags, cohort-local independent run capacities, two charged dependent axis helper copies; all characteristic-two fields and all whole-record widths'}
 a.out.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='cohorts'})
if __name__=='__main__':main()
