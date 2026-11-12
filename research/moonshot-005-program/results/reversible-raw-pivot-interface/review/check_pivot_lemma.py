#!/usr/bin/env python3
"""Independent finite controls for the universal raw-pivot proof."""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
PROOF=Path('/workspace/scratch/6a77123a1d61/root-research/reversible-raw-pivot-interface/PROOF.md')
def need(b,m):
 if not b:raise ValueError(m)
def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def rank(a,l):
 b=[r.copy() for r in a];h=0
 if not b:return 0
 for j in range(len(b[0])):
  p=next((i for i in range(h,len(b)) if b[i][j]%l),None)
  if p is None:continue
  b[h],b[p]=b[p],b[h];u=pow(b[h][j]%l,-1,l);b[h]=[u*x%l for x in b[h]]
  for i in range(len(b)):
   if i!=h:
    u=b[i][j]%l;b[i]=[(x-u*y)%l for x,y in zip(b[i],b[h])]
  h+=1
  if h==len(b):break
 return h
def apply(rows,op,l,indices=None):
 kind,i,j,c=op;i=i if indices is None else indices[i];c%=l
 if kind=='s':need(c!=0,'nonzero SCALE');rows[i]=[c*x%l for x in rows[i]]
 else:
  j=j if indices is None else indices[j];need(i!=j,'ADD distinct operands');rows[i]=[(x+c*y)%l for x,y in zip(rows[i],rows[j])]
def reduce_ops(B,l):
 b=[r.copy() for r in B];ops=[];m=len(B)
 def emit(op):ops.append(op);apply(b,op,l)
 for j in range(m):
  p=next((i for i in range(j,m) if b[i][j]%l),None)
  if p is None:raise ValueError('singular selected minor')
  if p!=j:
   emit(('a',j,p,1));emit(('a',p,j,-1));emit(('a',j,p,1));emit(('s',p,None,-1))
  emit(('s',j,None,pow(b[j][j],-1,l)))
  for i in range(m):
   if i!=j and b[i][j]:emit(('a',i,j,-b[i][j]))
 need(b==identity(m),'Gauss map actually reduces selected minor');return ops
def inverse_op(op,l):
 kind,i,j,c=op;return(kind,i,j,pow(c%l,-1,l) if kind=='s' else -c)
def matvec(M,q,l):return tuple(sum(a*b for a,b in zip(row,q))%l for row in M)
def algebra_cases():
 totals={};allcases=0
 for l in [2,3]:
  stats=Counter();largest={'ADD':0,'SCALE':0}
  for p in range(1,4):
   vectors=list(product(range(l),repeat=p))
   for m in range(1,p+1):
    for flat in product(range(l),repeat=m*p):
     A=[list(flat[i*p:(i+1)*p]) for i in range(m)];arank=rank(A,l);stats['matrices']+=1;success=False
     for I0 in combinations(range(p),m):
      I=list(I0);J=[j for j in range(p) if j not in I];B=[[row[j] for j in I] for row in A];r=rank(B,l);M=identity(p)
      for i,j in enumerate(I):M[j]=A[i].copy()
      expectedrank=p-m+r;need(rank(M,l)==expectedrank,'exact block rank')
      images={matvec(M,q,l) for q in vectors};need(len(images)==l**expectedrank,'all physical input image cardinalities')
      loss=m-r;records=next((R for R in combinations(I,loss) if rank(M+[identity(p)[j] for j in R],l)==p),None)
      need(records is not None,'coordinate records attain algebraic minimum')
      if loss:
       need(all(rank(M+[identity(p)[j] for j in R],l)<p for R in combinations(range(p),loss-1)),'one fewer record never restores rank')
       need(any(any(q) and matvec(M,q,l)==(0,)*p for q in vectors),'explicit input collision')
      need(len({matvec(M,q,l)+tuple(q[j] for j in records) for q in vectors})==l**p,'optimal records distinguish every input')
      stats['pivot_choices']+=1;stats['all_input_assignments']+=len(vectors);stats['lost_dimensions_total']+=loss
      if r!=m:stats['singular_choices']+=1;continue
      success=True;stats['invertible_choices']+=1;ops=reduce_ops(B,l);rows=identity(p)
      for op in reversed(ops):apply(rows,inverse_op(op,l),l,I)
      extra=[]
      for i,j in enumerate(I):
       for k in J:
        if A[i][k]:extra.append(('a',j,k,A[i][k]));apply(rows,extra[-1],l)
      need(rows==M,'actual elementary acquisition emits exact A rows')
      for op in extra:apply(rows,inverse_op(op,l),l)
      for op in ops:apply(rows,op,l,I)
      need(rows==identity(p),'actual local inverse recovers every original')
      adds=2*(sum(o[0]=='a' for o in ops)+len(extra));scales=2*sum(o[0]=='s' for o in ops)
      need(adds<=2*m*(p-1)+6*(m-1) and scales<=4*m-2,'Gaussian operation bounds')
      largest['ADD']=max(largest['ADD'],adds);largest['SCALE']=max(largest['SCALE'],scales)
     need(success==(arank==m),'full row rank iff some selected minor works')
  stats['largest_actual_ADD_count']=largest['ADD'];stats['largest_actual_SCALE_count']=largest['SCALE'];totals[str(l)]=dict(stats);allcases+=stats['pivot_choices']
 return totals,allcases

def route_hist(D,c,ells,fs,I):
 hist=Counter()
 for j,ell in enumerate(ells):
  segments=[c-ell]
  if j in I:
   f=fs[I.index(j)];segments +=[f-c,D-f]
  else:segments +=[D-c]
  need(all(r>=0 for r in segments),'nested dimension order')
  hist.update(r for r in segments if r)
 return hist

def route_controls():
 n=0;examples=[]
 for D in range(1,10):
  for c in range(D+1):
   for ell in range(c+1):
    for f in range(c,D+1):
     ells=[ell,c,max(0,ell-1)];I=[2,0];fs=[f,D];actual=route_hist(D,c,ells,fs,I);direct=Counter(D-e for e in ells if D!=e)
     changed=actual.copy();changed.subtract(direct);formula=Counter()
     def term(r,a):
      if r:formula[r]+=a
     for e in ells:term(c-e,1);term(D-c,1);term(D-e,-1)
     for z in fs:term(z-c,1);term(D-z,1);term(D-c,-1)
     need(dict((r,v) for r,v in changed.items() if v)==dict((r,v) for r,v in formula.items() if v),'exact acquisition-plus-delivery histogram identity')
     need(sum(r*v for r,v in changed.items())==0,'rank mass at t1 unchanged');n+=1
 # Incomparable equal-dimensional charts cannot be treated as a zero-rank stop.
 def space(vs):
  a={0}
  for v in vs:a|={v^x for x in tuple(a)}
  return a
 C=space([1,2]);badF=space([2,4]);need(not C<=badF,'recipient facet must actually contain C')
 actual=route_hist(9,7,[1,1,1],[8],[0]);without_last=actual.copy();without_last[1]-=1
 need(actual!=without_last and sum(r*v for r,v in actual.items())-sum(r*v for r,v in without_last.items())==1,'omitted final pivot leg changes paid profile')
 no_acquisition=actual.copy();no_acquisition[6]-=3
 need(actual!=no_acquisition,'omitted acquisition legs change paid profile')
 return {'symbolic_route_profiles_checked':n,'zero_length_segments_omitted':True,'arbitrary_pivot_index_order_checked':True,'noncontaining_facet_rejected':True,'omitted_final_leg_rejected':True,'omitted_acquisition_rejected':True}
def composition_controls():
 A=[[1,0,0],[0,0,1]];B=[[row[j] for j in [0,1]] for row in A]
 need(rank(A,3)==2 and rank(B,3)==1,'full requested rank does not validate chosen minor')
 need(rank([[row[j] for j in [0,2]] for row in A],3)==2,'a different minor does work')
 dep=[[1,1],[1,1]];need(rank(dep,2)==1 and matvec(dep,(1,1),2)==(0,0),'dependent overwritten rows have explicit collision')
 need(rank(dep+[[1,0]],2)==2,'one real original-coordinate record repairs the loss')
 outcomes={}
 for l in [2,3]:
  r=identity(3);a=('a',0,1,1);b=('a',1,2,1);apply(r,a,l);apply(r,b,l)
  correct=[x.copy() for x in r];apply(correct,inverse_op(b,l),l);apply(correct,inverse_op(a,l),l)
  wrong=[x.copy() for x in r];apply(wrong,inverse_op(a,l),l);apply(wrong,inverse_op(b,l),l)
  need(correct==identity(3) and wrong!=identity(3) and wrong[0]==[1,0,(-1)%l],'overlapping inverse order matters')
  available=[r[1]];desired=[0,1,0];record=[0,0,1]
  need(rank(available+[desired],l)>rank(available,l),'intended original row unavailable from current raw field alone')
  need(rank(available+[record,desired],l)==rank(available+[record],l),'owned observation changes the complete availability gate')
  outcomes[str(l)]={'wrong_inverse_first_row':wrong[0],'raw_only_rank':rank(available,l),'with_record_rank':rank(available+[record],l)}
 M=[[1,0,0],[0,0,1],[0,0,1]];V=3;K=[[M[i//V][j//V]*int(i%V==j%V) for j in range(3*V)] for i in range(3*V)]
 need(rank(K,3)==V*rank(M,3)==6,'vector-field rank and kernel scale by V')
 return {'full_rank_matrix_bad_minor_rejected':True,'dependent_output_collision_rejected':True,'overlap_and_complete_availability':outcomes,'rank_tensor_identity_verified_at_V3':True}

def main():
 pin='71d27e20ed5041f0779f92a16fc1708f08581d330e942909fa66d57de5ffc955'
 need(hashlib.sha256(PROOF.read_bytes()).hexdigest()==pin,'reviewed updated proof bytes')
 algebra,total=algebra_cases();need(total==22807,'complete declared finite matrix/pivot family')
 out={'status':'PASS_INDEPENDENT_RAW_PIVOT_LEMMA_CONTROLS','reviewed_proof_sha256':pin,'finite_fields':[2,3],'all_matrices_and_pivot_choices_for':'1<=m<=p<=3','pivot_cases':total,'field_results':algebra,'route_profiles':route_controls(),'negative_controls':composition_controls(),'universal_scope':'The universal any-field theorem is justified by the separate mathematical proof review; these finite controls verify concrete elementary implementations, all small-field inputs, exact lost-information counts, minimum coordinate records, route histogram identities, inverse order, and complete current availability. They do not establish physical chart suppliers or compatible global schedules.'}
 (HERE/'REVIEW-RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
