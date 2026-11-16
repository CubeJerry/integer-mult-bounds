#!/usr/bin/env python3
"""Independent source/endpoint/preparation audit; no C author code imported."""
import argparse,hashlib,json,copy,sys
from pathlib import Path
p=argparse.ArgumentParser()
for n in ['repo','word','raw','proof','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();sys.path.insert(0,str(a.repo/'research/moonshot-005-program/sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from price import invoice
w=json.loads(a.word.read_bytes());u=json.loads(a.raw.read_bytes());meta=w['ground_normalization'];k=meta['boundary'];prep=meta['preload_operations']+meta['inverse_operations'];N=111;mask=(1<<N)-1
assert w['operations']==u['operations'][:k]+prep+u['operations'][k:]
stats=independent_replay(w);ss,end=trace(u);ns,nend=trace(w);v,at=ss[k]
assert all(v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero'for i in range(N))
assert all(z>>N==0 for n,z in v.items()if not n.startswith('Y'))
G={n:v[n]for n in meta['source_owners']};assert all(at[n]=='zero'for n in G)
S=set(w['targets']);assert set(G.values())=={1<<s for s in S}and len(G)==46
M=[end[0][f'Y{i}']>>N for i in range(N)];F=[end[0][f'Y{i}']&mask for i in range(N)]
assert M==[int(x,16)for x in meta['homogeneous_Y_rows_hex']]
assert all(end[0][f'X{i}']==1<<i for i in range(N))
D=[(1<<i)if i in S else 0 for i in range(N)];available=sum(1<<s for s in S)
assert all((f^d)&~available==0 for f,d in zip(F,D))
preval,preloc=ns[k+len(prep)];A=[preval[f'Y{i}']>>N for i in range(N)];L=[preval[f'Y{i}']&mask for i in range(N)]
def product(B,C):
 rows=[]
 for b in B:
  r=0
  for j in range(N):
   if b>>j&1:r^=C[j]
  rows.append(r)
 return rows
assert product(M,A)==[1<<i for i in range(N)]
assert [x^y for x,y in zip(F,product(M,L))]==D
assert all(preloc[f'Y{i}']=='zero'for i in range(N))
feedback=['ADD','Y2','X0']in w['operations']
expected_inverse=2 if feedback else 5
assert len(prep)==50+expected_inverse and len(meta['preload_operations'])==50 and len(meta['inverse_operations'])==expected_inverse
if feedback:
 ix=w['operations'].index(['ADD','Y2','X0']);assert ns[ix+1][0]['X0']==(1<<0)^(1<<2)^(1<<3)^(1<<113)^(1<<114)
assert sorted(o for o in w['operations']if o[0]!='ADD')==sorted(o for o in u['operations']if o[0]!='ADD')
controls=[]
for op in [meta['inverse_operations'][0],['MOVE','KNOWN_RAW1','zero']]:
 bad=copy.deepcopy(w);bad['operations'].remove(op)
 try:independent_replay(bad)
 except(AssertionError,KeyError)as e:controls.append({'omitted':op,'rejected':True,'reason':str(e)})
 else:raise AssertionError('accepted mutated preparation')
assert [M[i]for i in [2,3,4]]==([(1<<2)^(1<<3),1<<3,(1<<3)^(1<<4)]if feedback else[1<<3,(1<<2)^(1<<3),(1<<2)^(1<<3)^(1<<4)])
result={'status':'PASS_ROOT_INDEPENDENT_GROUND_NORMALIZATION_REVIEW','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'raw_word_sha256':hashlib.sha256(a.raw.read_bytes()).hexdigest(),'actual_ground_source_rank':46,'boundary':k,'actual_preload_ADDs':50,'actual_inverse_ADDs':expected_inverse,'actual_Y_to_X_feedback':feedback,'homogeneous_Y_block_and_inverse_verified':True,'actual_known_column_correction_verified':True,'X_has_no_final_arbitrary_Y_contamination':True,'stats':stats,'price':invoice(stats['movement_profile']),'independent_controls':controls,'scope':'Written iff proof separately reviewed; reused independent predecessor geometry/all222-column engine. No C author module imported; no supplier or exponent.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
