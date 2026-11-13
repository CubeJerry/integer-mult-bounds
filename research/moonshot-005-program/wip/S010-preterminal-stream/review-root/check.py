from pathlib import Path
from fractions import Fraction as F
import argparse,copy,gzip,hashlib,json
from dense_engine import run,span
from source_review import rank
from verify_general import interval,read
if not __debug__:raise SystemExit('Assertions required')
M='d52a97c02f008eb4ec82c1cc92950f51bb0612795c9084981984ee518a303e59'
def main(a):
 man=read(a.bundle/'MANIFEST.json',M)
 for z in man['files']:assert hashlib.sha256((a.bundle/z['path']).read_bytes()).hexdigest()==z['sha256']
 source=read(a.repo/'research/shared-wire-split-composition/data/final.json.gz','2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',True)
 full=read(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json','d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7')
 parent=read(a.bundle/'source-evidence/rail-consumer.json.gz','a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc',True)
 four=read(a.bundle/'source-evidence/rail-cross-four.json.gz','20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f',True)
 start=parent['consumer']['begin'];assert start==4779 and len(parent['consumer']['lifetimes'])==31
 p=copy.deepcopy(parent);p['program']=p['program'][:start]
 w=copy.deepcopy(four);w['program']=[op for op,old in zip(w['program'],w['parent_event_of_output']) if old is None or old<start]
 r0,d0,l0,b0,_=run(p,list(map(span,p['frames'])));r4,d4,l4,b4,_=run(w,list(map(span,w['frames'])))
 roles={int(k):v for k,v in parent['source_role_map'].items()};host={source['live'][k]:(roles[x],roles[y]) for k,x,y in zip(source['hosted']['Dports'],source['hosted']['X2'],source['hosted']['Y2'])}
 matrices=[[[rows[b][host[j][1]]+den*int(i==j) for j in host] for i,(b,d) in host.items()] for rows,den in [(r0,d0),(r4,d4)]]
 assert list(map(rank,matrices))==[82,82]
 assert all(mat[i][i]==den for mat,den in zip(matrices,[d0,d4]) for i in range(96))
 expected={i:row.copy() for i,row in r0.items()}
 for i,j,c in [(1,106,-1),(2,4,1),(11,15,1),(23,24,1)]:
  for u,v in [(i,j),(j,i)]:expected[host[u][0]][host[v][1]]+=c*d0
 assert l0==l4 and all([v*d4 for v in expected[i]]==[v*d0 for v in r4[i]] for i in range(400))
 ferry={r:b4['moves'].get(r,0)-b0['moves'].get(r,0) for r in set(b4['moves'])|set(b0['moves'])};ferry={r:c for r,c in ferry.items() if c};assert ferry=={1:16,7:8,9:-8}
 cv=lambda x:{int(k):F(v) for k,v in x.items()}
 T,P=cv(full['invoice']['T']),cv(full['invoice']['P']);N,H=cv(full['native']['paid']),cv(full['native']['helpers']);Q=cv(b0['moves']);keys=set(T)|set(P)|set(N)|set(H)|set(Q)|{7,9}
 slope={r:(T.get(r,0)-P.get(r,0))/18 for r in keys};base={r:slope[r]+N.get(r,0)-H.get(r,0)-Q.get(r,0) for r in keys};assert interval(slope)[1]<0
 variants={}
 for label,debit,first in [('without_ferry',{},21),('with_four_ferry',ferry,24)]:
  limit={r:base[r]-8*int(r==7)-debit.get(r,0) for r in keys};tests=[]
  for m in [first-1,first]:
   bounds=interval({r:limit[r]+slope[r]/(m-1) for r in keys})
   if m==first-1:assert bounds[1]<0
   else:assert bounds[0]>0
   tests.append({'m':m,'bounds':list(map(str,bounds))})
  variants[label]={'first_fixed_m':first,'limiting_bounds':list(map(str,interval(limit))),'adjacent_tests':tests}
 gap={r:-base[r]+96*int(r==1) for r in keys};assert interval(gap)[0]>F(389,10)
 out={'status':'PASS_INDEPENDENT_STRIPPED_SOURCE_AND_CONDITIONAL_TARIFF','author_manifest_sha256':M,'all400_maps_compared':True,'stripped_ranks':[82,82],'all96_diagonals_one':True,'only_eight_advertised_B_changes':True,'stripped_bills':[b0,b4],'variants':variants,'coordinate_return_invariant_gap_bounds':list(map(str,interval(gap))),'scope':'Conditional tariff and literal stripping only. No rank8 source or C2 observation/decoder. All previous source costs and restoration constraints retained.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','stripped_ranks','variants','coordinate_return_invariant_gap_bounds']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
