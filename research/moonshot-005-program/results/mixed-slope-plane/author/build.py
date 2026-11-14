#!/usr/bin/env python3
"""Actual independent fields meeting with opposite public directions."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import gzip,json,hashlib,argparse,copy
HERE=Path(__file__).resolve().parent
SHA='c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336'
PHASE_PINS={'FORWARD-PHASES.json': '465a759e6e4e14d29d9b8cda8fed51c8e6440926d699f3a088c0507b2ec9ae55', 'INVERSE-PHASES.json': 'c2b9e20782d6aa0cdddd9d11e64ec5b03bd14188aebe9cbc2068a918863f8300'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def span(vs):
 a={0}
 for v in vs:a|={x^v for x in list(a)}
 return a
def add(a,b,c):
 r=dict(a)
 for j,v in b.items():
  r[j]=r.get(j,F(0))+c*v
  if not r[j]:del r[j]
 return r
def replay(w):
 rows=[{i:F(1)}for i in range(w['public'])];loc=w['initial'][:];counts=Counter();ups=downs=0
 for e in w['program']:
  if e[0]=='MOVE':
   _,h,a,b,owned=e;need(not owned and loc[h]==a,'actual independent raw location')
   A=span(w['frames'][a]);B=span(w['frames'][b]);need(A<B or B<A,'nested actual move')
   r=abs(len(w['frames'][a])-len(w['frames'][b]));counts[r]+=1;loc[h]=b
   if A<B:ups+=1
   else:downs+=1
  elif e[0]=='ADD':
   _,d,s,c,f=e;need(loc[d]==loc[s]==f,'actual source/receiver cochart');rows[d]=add(rows[d],rows[s],F(c))
  else:raise ValueError('unexpected opcode')
 need(loc==w['final'],'every original field final frame')
 return rows,dict(sorted(counts.items())),ups,downs
def main(out):
 raw=(HERE/'source/R0-MINIMAL-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==SHA,'literal parent pin');old=json.loads(gzip.decompress(raw))
 P=old['logical_involution']['ports'];roles=old['logical_involution']['role_map'];oldrows,_,_,_=replay(old)
 X={h:i for i,h in enumerate(P)};Y={h:112+i for i,h in enumerate(P)};R={}
 for h in P:
  y=roles['Y'][str(h)];r=dict(oldrows[y]);need(r.pop(y)==1,'old arbitrary Y baseline')
  R[h]={j:r[roles['X'][str(j)]]for j in P if roles['X'][str(j)]in r};need(len(R[h])==4,'four actual R0 contacts')
 expected=[{i:F(1)}for i in range(224)]
 for h in P:expected[Y[h]]=add(expected[Y[h]],{X[j]:v for j,v in R[h].items()},1)
 phase={}
 for name in ['FORWARD-PHASES.json','INVERSE-PHASES.json']:
  b=(HERE/'source'/name).read_bytes();need(hashlib.sha256(b).hexdigest()==PHASE_PINS[name],'exact signed phase receipt pin');z=json.loads(b)
  for r in z['recipes']:phase[r['source'],r['target']]=r
 out.mkdir(parents=True,exist_ok=True);results={}
 for x_up in [True,False]:
  name='X-up-Y-down'if x_up else'X-down-Y-up';initial=[None]*224;final=[None]*224
  for h in P:
   ox=roles['X'][str(h)];oy=roles['Y'][str(h)]
   initial[X[h]]=old['initial'][ox]if x_up else old['final'][ox];final[X[h]]=old['final'][ox]if x_up else old['initial'][ox]
   initial[Y[h]]=old['final'][oy]if x_up else old['initial'][oy];final[Y[h]]=old['initial'][oy]if x_up else old['final'][oy]
  ops=[]
  for z in old['logical_involution']['halves']:
   C=z['source_C3'];S=z['sources'];T=z['ports'];need(len(old['frames'][C])==3,'actual rank3 meeting')
   for j in S:ops.append(['MOVE',X[j],initial[X[j]],C,False])
   for h in T:ops.append(['MOVE',Y[h],initial[Y[h]],C,False])
   for h in T:
    for j in S:ops.append(['ADD',Y[h],X[j],str(R[h][j]),C])
   for j in S:ops.append(['MOVE',X[j],C,final[X[j]],False])
   for h in T:ops.append(['MOVE',Y[h],C,final[Y[h]],False])
  w={'schema':'S012-mixed-slope-independent-half-v1','public':224,'owned_fields':0,'frames':old['frames'],'initial':initial,'final':final,'program':ops,
   'mixed_slope':{'variant':name,'ports':P,'normals':old['logical_involution']['normals'],'role_map':{'X':X,'Y':Y},'source_parent_sha256':SHA,
   'abstract_endpoint':'X=x; Y=y+R0 x; all224 original inputs arbitrary','new_public_directions':'X strictly ascends and Y strictly descends'if x_up else'X strictly descends and Y strictly ascends'}}
  rows,H,ups,downs=replay(w);need(rows==expected,'all224 original scalar columns and complete endpoints')
  need(H=={2:112,3:112,5:112,6:112}and ups==downs==224,'complete actual half tariff and slopes')
  used={tuple(e[2:4])for e in ops if e[0]=='MOVE'}
  for a,b in used:
   r=phase[a,b];need(r['source_frame']==w['frames'][a]and r['target_frame']==w['frames'][b],'retained exact signed ordered map')
   need(r['rank']==abs(len(w['frames'][a])-len(w['frames'][b])),'retained signed map rank')
  bad=copy.deepcopy(w);k=next(k for k,e in enumerate(bad['program'])if e[0]=='ADD');del bad['program'][k]
  need(replay(bad)[0]!=expected,'deleted contact changes an actual original column')
  bad=copy.deepcopy(w);e=next(e for e in bad['program']if e[0]=='MOVE');e[2],e[3]=e[3],e[2]
  try:replay(bad);rejected=False
  except ValueError:rejected=True
  need(rejected,'wrong entering public direction rejected')
  data=(json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(data,mtime=0);folder=out/name;folder.mkdir(exist_ok=True);(folder/'WORD.json.gz').write_bytes(blob)
  result={'status':'PASS_ACTUAL_MIXED_SLOPE_224_INPUT_SOURCE','word_sha256':hashlib.sha256(blob).hexdigest(),'profile':H,'ascents':ups,'descents':downs,
   'public':224,'independent_source_columns':224,'ADD':448,'MOVE':448,'owned_fields':0,'ordered_signed_maps':len(used),
   'all_existing_signed_recipes_matched':True,'source_parent_sha256':SHA,'negative_controls':['deleted_actual_contact_changes_endpoint','wrong_entering_move_rejected'],
   'scope':'Exact source and opposite public directions. These were not admitted by the old ascent-only public grammar. A complete new caller/target interface and all foundational assumptions remain; no new kappa.'}
  (folder/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');results[name]=result
 final={'status':'PASS_BOTH_ACTUAL_MIXED_SLOPE_SOURCES','variants':results,'phase_receipt_pins':{name:hashlib.sha256((HERE/'source'/name).read_bytes()).hexdigest()for name in ['FORWARD-PHASES.json','INVERSE-PHASES.json']}}
 (out/'RESULT.json').write_text(json.dumps(final,indent=2,sort_keys=True)+'\n');print(json.dumps({name:r['word_sha256']for name,r in results.items()},indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=HERE/'output');main(a.parse_args().out)
