"""Exact actual-frame downset certificate and literal eight-Gram reference."""
from pathlib import Path
from fractions import Fraction as F
import argparse,gzip,json,hashlib,collections,importlib.util
if not __debug__:raise SystemExit('Exact verifier requires assertions')
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
DEP='a28c7e8037ae99b6aecf21a62a4f784c906016d5e12f100826062cf3d602c5b1'
FRAMES=[[0,16,17,32,36,38,67,71],[0,16,17,32,36,39,68,72],[0,16,17,36,37,63,71,72],[0,16,17,36,38,39,62,63],[1,8,9,30,37,46,73,77],[1,8,9,30,37,47,74,78],[1,8,9,36,37,65,73,74],[1,8,9,37,46,47,64,65],[36,37,62,64,67,68,77,78]]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p not in b:b[p]=x;break
   x^=b[p]
 return len(b)
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;s=json.loads(gzip.decompress(raw));ch={int(k):v for k,v in s['frames'].items()};roots=[[F(x) for x in ch[s['start'][i]]['B'][0]] for i in range(111)];v=[]
 for r in roots:
  norm=dot(r,r);assert norm in [1,4];w=[x*(2 if norm==1 else 1) for x in r];assert all(x.denominator==1 for x in w);v.append([int(x) for x in w])
 B=[]
 for i in range(111):
  row=0
  for j in range(111):
   d=dot(v[i],v[j]);assert d%2==0;row|=((d//2)%2)<<j
   assert bool((d//2)%2)==(i!=j and d!=0)
  B.append(row)
 assert rank(B)==8
 enc=[];spanbasis={}
 for i,row in enumerate(B):
  r=row;mask=0
  while r:
   k=r.bit_length()-1
   if k not in spanbasis:
    n=len(enc);enc.append((i,row));spanbasis[k]=(r,mask^(1<<n));break
   z,m=spanbasis[k];r^=z;mask^=m
 assert len(enc)==8
 dec=[]
 for row in B:
  r=row;m=0
  while r:
   k=r.bit_length()-1;z,x=spanbasis[k];r^=z;m^=x
  assert row==__import__('functools').reduce(int.__xor__,(enc[k][1] for k in range(8) if m>>k&1),0);dec.append(m)
 def inside(c,S):return any(all(dot([F(x) for x in b],roots[i])==0 for b in ch[c]['B']) for i in S)
 cert=[]
 for S in FRAMES:
  assert len(set(S))==8 and all(dot(roots[i],roots[j])!=0 for i in S for j in S)
  assert all(not inside(s['start'][j],S) for j in S) and all(inside(s['final'][111+j],S) for j in S)
  cuts=[sum(((row>>j)&1)<<k for k,j in enumerate(S)) for _,row in enc];bf=[sum(((B[i]>>j)&1)<<k for k,j in enumerate(S)) for i in S];assert rank(cuts)==rank(bf)==8
  assert bf==[((1<<8)-1)^(1<<i) for i in range(8)]
  cert.append({'frame':S,'source_lines_outside':8,'target_facets_inside':8,'real_dot_matrix':[[str(dot(roots[i],roots[j])) for j in S] for i in S],'encoder_first_entry_restrictions':cuts,'cut_rank':8,'B_principal_rows':bf})
 # New reference word, preserving actual source/final charts and all222 inputs.
 hub=s['final'][0];zero=s['start'][111];ops=[['MOVE',i,s['start'][i],hub] for i in range(111)];packet=222
 for k,(_,row) in enumerate(enc):
  ops.append(['INIT',packet,hub]);ops += [['ADD',packet,j,hub] for j in range(111) if row>>j&1];ops.append(['MOVE',packet,hub,zero]);ops += [['ADD',111+i,packet,zero] for i,m in enumerate(dec) if m>>k&1];ops.append(['CLEAR',packet,zero])
 ops += [['MOVE',111+i,zero,s['final'][111+i]] for i in range(111)]
 word={'schema':'actual-BIT-eight-homogeneous-Gram-reference-v1','public':222,'owned_fields':1,'start':s['start'][:222],'final':s['final'][:222],'frames':ch,'program':ops,'scope':'Exact partial reference: X=x,Y=y+B*x; allframecuttests pass but every Ytarget fails. Eight lifetimes, not one descending trajectory.'}
 dep=a.repo/'research/moonshot-005-program/results/bit-rank-nine-shared-interface/build_bit_nine_rail.py';assert hashlib.sha256(dep.read_bytes()).hexdigest()==DEP;spec=importlib.util.spec_from_file_location('retained_bit_replay',dep);R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R);rows,bill=R.replay(word,ch)
 assert rows[:111]==[1<<i for i in range(111)] and rows[111:]==[(1<<(111+i))^B[i] for i in range(111)]
 failed=[i for i in range(111) if rows[111+i]!=((1<<(111+i))^(1<<i))];assert failed==list(range(111)) and bill['paid_profile']=={7:222,8:8} and bill['retired_lifetimes']==8 and bill['peak_owned']==1
 assert all(inside(s['start'][j],list(range(8))) for j in range(8)) # coordinate bus is outside theorem's separated-frame premise
 # Removing an encoder trajectory destroys each square8 crossing-map rank.
 assert all(rank(c['encoder_first_entry_restrictions'][:-1])<=7 for c in cert)
 a.output.mkdir(parents=True,exist_ok=True);rawword=json.dumps(word,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(rawword,mtime=0);(a.output/'WORD.json.gz').write_bytes(compressed)
 out={'status':'PASS_EIGHT_DOWNSET_CUT_SOURCE_AND_PARTIAL_GRAM_REFERENCE','native_sha256':PIN,'retained_replay_sha256':DEP,'word_sha256':hashlib.sha256(compressed).hexdigest(),'eight_frames':cert,'initial_encoder_source_rows':[i for i,_ in enc],'initial_encoder_rows_hex':[hex(r) for _,r in enc],'decoder_masks':dec,'rank_B':8,'all222_reference_inputs_replayed':True,'reference_bill':bill,'every_Y_target_incomplete':failed,'cut_bound':'q>=8 for physical monotone descending trajectories; allother recordsascending and no unlistedincomingservice','allfield_allV_statement':'Linear rank cut uses8V independent sources and atmostqV incoming dimensions. No canonicalcode or terminal assumption.','controls':{'coordinate_bus_inputs_are_inside_union':8,'all_frame_rank_tests_pass_but_full_endpoints_fail':True,'one_encoder_removed_rejected_by_cut_rank':True,'owned_label_count_is_not_trajectory_count':{'labels':1,'descending_lifetimes':8}},'scope':'Exact source certificate and partial source witness; universal downset proof is separate. No complete eightpacket algorithm, physical admission, supplier or kappa.'}
 (a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','rank_B','reference_bill','word_sha256','cut_bound']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
