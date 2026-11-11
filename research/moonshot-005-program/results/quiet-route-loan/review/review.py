"""Independent decomposition/three-variable proof of the emitted quiet-loan word."""
import argparse,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as F
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,msg):
 if not x:raise ValueError(msg)
def main(source,transcript):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));t=json.loads(gzip.decompress(transcript.read_bytes()));M=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));C={r:1480+i for i,r in enumerate(M)};q=C[907];z=C[977];rows={'H':[F(1),F(0),F(0)],'Q':[F(0),F(1),F(0)],'Z':[F(0),F(0),F(1)]};macros=[('H','Q',1),('Q','H',-1),('H','Q',1),('Z','H',1),('H','Q',-1),('Q','H',1),('H','Q',-1)]
 for a,b,c in macros:rows[a]=[x+c*y for x,y in zip(rows[a],rows[b])]
 need(rows=={'H':[1,0,0],'Q':[0,1,0],'Z':[0,1,1]},'closed three-input matrix')
 # Derive the literal passive embedding without importing author construction.
 expected=[['ADD',C[r],r,'-1',w['initial'][r]] for r in M];extra=[];locations=w['initial'][:];donor_before=receiver_before=None
 for i,event in enumerate(w['program']):
  if i==28048:
   need(locations[449]==locations[907]==3 and locations[977]==594,'loan start charts');donor_before=locations[907];receiver_before=locations[977]
   extra.extend(range(len(expected),len(expected)+3));expected.extend([['ADD',449,q,'1',3],['ADD',q,449,'-1',3],['ADD',449,q,'1',3]])
  e=event[:];e[1]+=400*(e[1]>=1480)
  if e[0] in ('ADD','COPY'):e[2]+=400*(e[2]>=1480)
  expected.append(e)
  if event[0]=='MOVE':
   if event[1]<1480:locations[event[1]]=event[3]
   if event[1] in C:expected.append(['MOVE',C[event[1]],event[2],event[3],False])
  if i==28048:extra.append(len(expected));expected.append(['ADD',z,449,'1',594])
  if i==30653:
   need(locations[449]==locations[907]==594,'closure charts');extra.extend(range(len(expected),len(expected)+3));expected.extend([['ADD',449,q,'-1',594],['ADD',q,449,'1',594],['ADD',449,q,'-1',594]])
 need(expected==t['program'],'every emitted operation agrees with independent passive embedding plus macro')
 touches=[i for i,e in enumerate(w['program']) if e[1]==449 or e[0] in ('ADD','COPY') and e[2]==449];need(28048 in touches and next(i for i in touches if i>28048)==30837,'actual next helper access');need(w['program'][30653]==['MOVE',907,3,594,False],'borrowed carrier closure');need(len(extra)==7,'seven ADDs')
 return {'status':'PASS_INDEPENDENT_WORD_DECOMPOSITION_AND_EXACT_LOAN_MATRIX','source_sha256':PIN,'transcript_sha256':hashlib.sha256(transcript.read_bytes()).hexdigest(),'physical_events':len(expected),'physical_macro_indices':extra,'source_loan_events':[28048,30653],'next_helper_access':30837,'loan_matrix':{k:[str(x) for x in v] for k,v in rows.items()},'method':'Independent literal passive-word decomposition, actual source-touch and chart checks, exact three-independent-variable matrix; author scientific code not imported or rerun.','scope':'Closed common-helper loan implements q977+=q907 using seven ADDs and funded routes. Full second native E action and physical scalar tariffs are not established.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--transcript',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=main(a.source,a.transcript);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
