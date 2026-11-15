#!/usr/bin/env python3
"""Exact finite diagnostics for the universal written two-native theorem."""
import argparse,hashlib,importlib.util,json,sys,random
from pathlib import Path
import sympy as s

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ar=ap.parse_args();base=Path(__file__).parent
 deps=json.loads((base/'DEPENDENCIES.json').read_text());assert len(deps['programme_baseline_sha'])==40
 for dep in deps['sources']:assert hashlib.sha256((ar.repo/dep['path']).read_bytes()).hexdigest()==dep['sha256']
 hp=ar.repo/deps['sources'][-1]['path'];sp=importlib.util.spec_from_file_location('two_native_dyadic',hp);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 I=m.eye(8);X=[m.monomial([j^(1<<k) for j in range(8)],[0]*8) for k in range(3)];C=[m.M((I.scale((1,1))+x.scale((1,-1))).a,1).norm() for x in X];S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);A=C[1]@S
 source=[]
 for V in (1,2):
  a=A.tp(V);d=a.n;i=m.eye(d);z=m.zero(d)
  for sign in (1,-1):
   b=a if sign==1 else a.star();D1=m.diagonal([b,i]);D2=m.diagonal([i,b]);L=m.block([[b,i],[z,b]]);E=m.block([[i,i],[z,i]]);assert L==D2@E@D1
   for c in (1,-1):
    U=m.block([[b,b.power(2).scale((c,0))],[z,b]]);Ec=m.block([[i,i.scale((c,0))],[z,i]]);assert U==D1@Ec@D2
    Ui=m.block([[b.star(),i.scale((-c,0))],[z,b.star()]]);assert U@Ui==m.eye(2*d)
   source.append({'width':V,'head_inverse_sign':sign,'all_input_columns':2*d,'two_query_factorizations':3})
 # Physical rank inequalities are checked with exact rational blocks, allowing singular blocks.
 rng=random.Random(2026111508);checks=0;singular_cii=0
 for p in range(4):
  d=2;n=(2+p)*d;ad=2*d
  for trial in range(8):
   Q=s.eye(n)
   for _ in range(3*n):
    i,j=rng.sample(range(n),2);coef=rng.choice([-2,-1,1,2]);Q[i,:]=Q[i,:]+coef*Q[j,:]
   if trial%2 and p:Q.row_swap(0,ad)
   assert Q.det()!=0
   Cai=Q[:ad,ad:];Cia=Q[ad:,:ad];Cii=Q[ad:,ad:];ri=Cii.rank();rx=Cai.rank();ry=Cia.rank();assert rx>=p*d-ri and ry>=p*d-ri
   T=s.Matrix(ad,ad,[rng.randrange(-2,3) for _ in range(ad*ad)]);P1=T.row_join(Cai).col_join(Cia.row_join(s.zeros(p*d,p*d)))
   assert P1.rank()>=rx+ry;checks+=1;singular_cii+=ri<p*d
 # Explicit ordinary zero-divisor block: one coordinate swaps between active and idle spaces.
 Q=s.eye(6);Q.row_swap(0,4);Cii=Q[4:,4:];assert Cii.rank()==1 and Q[:4,4:].rank()==Q[4:,:4].rank()==1
 # The old no-rank-zero count cannot be used after simply discarding ordinary jobs.
 p=2;Q=s.eye(8);assert Q[:4,4:].rank()==0 and Q[4:,:4].rank()==0 and Q[4:,4:].rank()==4
 # Changed-square negative control: W is invertible F1 but an unrelated rank2 cross defeats pi2=>pi3.
 b=A.star();K=C[0]@C[2]@S;assert m.gaussian_rank(K)==2 and K!=A.power(2);G=K@b;assert m.gaussian_rank(G)==3 and A@b==I
 W=m.block([[m.zero(8),b],[b,m.zero(8)]]);fake=m.block([[A,K],[m.zero(8),A]]);M=fake@W;assert M==m.block([[G,I],[I,m.zero(8)]])
 # Same-input components are not independent endpoint jobs.
 bad=m.block([[A.power(3),A.power(2)],[m.zero(8),m.zero(8)]]);phys=s.Matrix([[s.Rational(x,2**bad.k)+s.I*s.Rational(y,2**bad.k) for x,y in row] for row in bad.a]);assert phys.rank()==8
 out={'status':'PASS_EXACT_TWO_NATIVE_TOTAL_HEAD_DIAGNOSTICS','source_factorizations':source,'rational_block_rank_cases':checks,'cases_with_singular_idle_block':singular_cii,'explicit_zero_divisor_idle_rank':1,'negative_controls':['rank-zero jobs cannot be deleted from the idle-block count','unrelated rank-two cross invalidates the missing-rank-two implication even with invertible F1 preword','two high components on one input row do not give two independent endpoint jobs'],'physical_changed_cross_example':'[[G_rank3,I],[I,0]], with no rank2 component, is not an actual square-cross native','scope':'Universal theorem is the written component proof, stable cancellation and pinned two-query gate; finite tests are diagnostics, not independent review','new_kappa':False}
 (base/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
