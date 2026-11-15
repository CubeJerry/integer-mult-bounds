#!/usr/bin/env python3
"""Root review using the prior independent replay and new source derivations."""
import argparse, hashlib, json, sys
from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--funnel-review',type=Path,required=True)
ap.add_argument('--quotient',type=Path,required=True)
ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args();sys.path.insert(0,str(a.funnel_review))
from check import rank, rr, replay, need
from budget import budget, combine, moment
src=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
raw=src.read_bytes();sha=hashlib.sha256(raw).hexdigest()
need(sha=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','source pin')
R=json.loads(raw)['native_roots'];dot=lambda x,y:sum(i*j for i,j in zip(x,y))
K=[sum(1<<j for j in range(111) if i==j or dot(R[i],R[j])==0) for i in range(111)]
reports={}
for name in ['six','late-control']:
    raw=(a.quotient/name/'WORD.json').read_bytes();w=json.loads(raw)
    r=replay(w,R,name=='six');r['word_sha256']=hashlib.sha256(raw).hexdigest()
    r['budget']=budget(r['movement_profile']);reports[name]=r
early=reports['six'];late=reports['late-control']
need(early['counts']=={'INIT':18,'ADD':594,'MOVE':344,'CLEAR':18},'word counts')
need(early['budget']['first_positive_even_m']==12,'exact caller threshold')
need(late['budget']['first_positive_even_m'] is None,'late control exceeds allowance')
need(combine((1,late['movement_profile']),(-1,early['movement_profile']))=={1:-2,7:2},'real timing price difference')
w=json.loads((a.quotient/'six/WORD.json').read_text());T=w['targets'];cohorts={}
for j,r in enumerate(R):
    s=tuple(i for i in T if not dot(r,R[i]));cohorts[s]=cohorts.get(s,0)|(1<<j)
triangles=[(3,76,80),(3,73,77),(1,76,77),(1,73,80)]
relation=0
for s in triangles:relation^=cohorts[s]
need(relation==K[1]^K[3]==K[73]^K[76]==K[77]^K[80],'triangle identity')
need(relation.bit_count()==58,'relation support')
controls=[]
predicates=[
 ('retained cache read',lambda x:x[0]=='ADD' and x[1].startswith('A') and x[2].startswith('Y')),
 ('changed ground preload',lambda x:x[0]=='ADD' and x[1].startswith('P') and x[2]=='Y3'),
 ('early source capture',lambda x:x[0]=='ADD' and x[2].startswith('E')),
 ('original restoration',lambda x:x[0]=='MOVE' and x[1]=='X1' and x[2]=='Hub'),
 ('owner retirement',lambda x:x[0]=='CLEAR')]
for name,pred in predicates:
    x=deepcopy(w);idx=next(i for i,v in enumerate(x['operations']) if pred(v));del x['operations'][idx]
    try:replay(x,R,False)
    except ValueError as e:controls.append({'name':name,'rejected':str(e)})
    else:raise AssertionError('accepted mutant '+name)
spanners=[R[i] for i in [1,3,4,76]];need(len(rr(spanners))==4,'D4 rank')
T=[i for i,r in enumerate(R) if len(rr(spanners+[r]))==4]
Z=[j for j,r in enumerate(R) if all(not dot(r,R[i]) for i in T)]
need(len(T)==len(Z)==12 and not(set(T)&set(Z)),'D4 source classes')
outside=set(range(111))-set(T)-set(Z);mask=sum(1<<j for j in outside)
need(rank([v&mask for v in K])==rank(K)==9,'outside rank preserves canonical code')
grant=K+[1<<j for j in Z]
need(rank(grant)==21 and rank(grant+[1<<j for j in T])==33,'quotient rank12')
# A separately selected odd minor certifies the all-field lift explicitly.
rows=[];row_ids=[]
for i,v in enumerate(K):
    if rank(rows+[v&mask])>len(rows):rows.append(v&mask);row_ids.append(i)
columns=[];col_ids=[]
for j in sorted(outside,reverse=True):
    v=sum(((r>>j)&1)<<i for i,r in enumerate(rows))
    if rank(columns+[v])>len(columns):columns.append(v);col_ids.append(j)
matrix=[[F((r>>j)&1) for j in col_ids] for r in rows];det=F(1)
for i in range(9):
    p=next(j for j in range(i,9) if matrix[j][i])
    if p!=i:matrix[i],matrix[p]=matrix[p],matrix[i];det=-det
    pivot=matrix[i][i];det*=pivot
    for j in range(i+1,9):
        c=matrix[j][i]/pivot
        matrix[j]=[v-c*z for v,z in zip(matrix[j],matrix[i])]
need(det.denominator==1 and int(det)%2,'odd exact rational determinant')
for i in T:need(rank(grant+[1<<j for j in T if j!=i])==32,'missing target remains missing')
profile={1:12,7:222,8:9};floor=budget(profile);relaxation=budget({1:11,7:222,8:9})
need(F(floor['limiting_room']['upper_fraction'])<0,'12 arrival target failure')
need(F(relaxation['limiting_room']['lower_fraction'])>0,'11 arrival optimistic control')
out={'status':'PASS_ROOT_QUOTIENT_AND_D4_REVIEW','source_sha256':sha,'quotient_word':reports,
 'triangle_relation_support':58,'independent_semantic_controls':controls,
 'D4':{'targets':T,'free_local_sources':Z,'canonical_basis_rows':row_ids,'minor_columns':col_ids,
 'minor_determinant':int(det),'canonical_grant_rank':21,'with_targets_rank':33,'target_omission_controls':12,
 'movement_floor':floor,'eleven_arrival_relaxation':relaxation},'new_complete_kappa':False}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'Q':early['budget']['moment']['display_lower'],'first_even_m':12,
 'D4_minor_determinant':int(det),'D4_upper_room':floor['limiting_room']['display_upper']}))
