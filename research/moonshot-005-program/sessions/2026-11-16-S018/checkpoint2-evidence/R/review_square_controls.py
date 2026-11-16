#!/usr/bin/env python3
"""Independent exact conditional-swap recipe check over Q[h]/(h^2-1)."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
p=argparse.ArgumentParser()
for n in ['proof','classification-result','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();z=(F(0),F(0));one=(F(1),F(0));h=(F(0),F(1))
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def mul(x,y):return(x[0]*y[0]+x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,c):return(x[0]*c,x[1]*c)
def compose(A,B):return[[add(mul(A[i][0],B[0][j]),mul(A[i][1],B[1][j]))for j in range(2)]for i in range(2)]
I=[[one,z],[z,one]];M=I;prefix=[]
steps=[[[one,one],[z,one]],[[one,z],[z,(F(-2),F(0))]],[[one,z],[one,one]],[[one,z],[z,h]],[[one,one],[z,one]],[[(F(1,2),F(0)),z],[z,one]],[[one,z],[z,(F(-1),F(0))]],[[one,z],[one,one]]]
for step in steps:
 M=compose(step,M);prefix.append(max(sum(abs(c[0])+abs(c[1])for c in row)for row in M))
plus=(F(1,2),F(1,2));minus=(F(1,2),F(-1,2));assert M==[[plus,minus],[minus,plus]];assert compose(M,M)==I;assert max(prefix)<=32
# Dropping the literal quarter-turn-induced involution breaks the route.
wrong=I
for k,step in enumerate(steps):wrong=compose(I if k==3 else step,wrong)
assert wrong!=M
c=json.loads(a.classification_result.read_text());assert c['diagonal_sign_count']==4096 and c['diagonal_root_four_count']==65536 and c['fibre_admitted']==384
r={'status':'PASS_ROOT_BOOLEAN_SOURCE_SQUARE_AND_CONDITIONAL_BANK_REVIEW','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'independent_classification_result_sha256':hashlib.sha256(a.classification_result.read_bytes()).hexdigest(),'Boolean_class_count_from_independent_full_classification':4096,'universal_bank_recipe_identity':True,'conditional_swap_involution':True,'prefix_norm_upper_bounds':[str(x)for x in prefix],'claimed_32_bound_valid':True,'per_direction_counts':{'ADD':4,'SCALE':3,'H_service':1,'new_owner':0},'omitted_H_control_rejected':True,'scope':'Universal ring calculation and independently derived monomial class; fixed compiler and all source/precision/ordinary tariffs remain conditional and paid. No complete421 caller.'}
a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
