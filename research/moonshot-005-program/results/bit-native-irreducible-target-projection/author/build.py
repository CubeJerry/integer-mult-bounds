#!/usr/bin/env python3
"""Literal native receiver80 target projection using a paid tile plus exact flow."""
import argparse,gzip,json
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
from field import add_field,swap_field
from flow import construct
B=480;N=111;PUBLIC=2*N*B
TILE_PIN='42b701dfce05e108dfafc4db5dcf813f92c42d74f0416e6d37a1d7bb301459e1'
PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','phase':'a806cc80a7bc7955fa07e04384707deb38200bac682424682e997f742dc5e278'}
STAGES=['X_NATIVE','X_H','X_D','X_K','X_F','HUB_RESTORE','GROUND_PRELOAD','Y_LINE','Y_H','Y_D','Y_K','Y_F']
def fid(kind,j,c):return (0 if kind=='X'else N*B)+j*B+c
def targets(neighbors,j,t):
 p=neighbors.index(j);out=[t]
 if p==0 and t<7:out.append(t+1)
 elif p==1 and t==7:out.append(0)
 elif 2<=p<=60:out.append(8*(p-1)+t)
 return out
def permute(pairs):
 """Complete a partial bijection dst<-src; untouched complement is fixed."""
 assert len({d for d,s in pairs})==len(pairs)==len({s for d,s in pairs})
 fields=sorted({f for p in pairs for f in p});order={f:f for f in fields};pos=order.copy();word=[]
 for dst,val in pairs:
  src=pos[val]
  if src!=dst:
   word+=swap_field(dst,src);old=order[dst];order[src],order[dst]=old,val;pos[old],pos[val]=src,dst
 assert all(order[d]==s for d,s in pairs)
 return word
def location(stage,f,route,caches):
 if f>=PUBLIC:return caches[f-PUBLIC]['chart']
 kind,j,c,h,d,k,line,term=route[f]
 if kind=='X':
  if stage=='X_NATIVE':return ['L',j]
  if stage=='X_H':return ['H',h]
  if stage=='X_D':return ['D',d]
  if stage=='X_K':return ['K',k]if k is not None else ['Hub']
  if stage=='X_F':return ['F',term]if term is not None else ['Hub']
  return ['Hub']
 if stage in STAGES[:7]:return ['Ground']
 if stage=='Y_LINE':return ['L',line]if line is not None else ['D',d]
 if stage=='Y_H':return ['H',h]if h is not None else ['D',d]
 if stage=='Y_D':return ['D',d]
 if stage=='Y_K':return ['K',k]
 return ['F',j]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--tile',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 base=args.repo/'research/moonshot-005-program/results';atlas=base/'bit-asymmetric-balanced-atlas/author'
 pp={'layout':base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','routes':atlas/'output/ROUTES.jsonl.gz','phase':atlas/'PHASE-CERTIFICATE.json'}
 raw={k:gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes()for k,p in pp.items()}
 assert all(sha256(v).hexdigest()==PINS[k]for k,v in raw.items())
 layout=json.loads(raw['layout']);routes=[json.loads(s)for s in raw['routes'].splitlines()];route={fid(r[0],r[1],r[2]):r for r in routes}
 assert len(route)==PUBLIC
 tile_raw=gzip.decompress(args.tile.read_bytes());assert sha256(tile_raw).hexdigest()==TILE_PIN;tile=json.loads(tile_raw)
 roots=layout['root_table'];H=list(map(set,layout['A2']));neighbors=[j for j in range(N)if sum(x*y for x,y in zip(roots[80],roots[j]))==0]
 remaining=sorted(set(neighbors)-set(tile['source_donors']));assert len(remaining)==50
 yout={r[5]:f for f,r in route.items()if r[0]=='Y'and r[4]==12};ks=[k for k in sorted(yout)if 80 in H[k]]
 yd={k:(yout[k]if route[yout[k]][1]==80 else min(f for f,r in route.items()if r[0]=='Y'and r[1]==80 and r[5]==k))for k in ks}
 paths=construct(routes,layout,remaining,yout,yd)
 assert len(paths)==400 and all(p['D']!=12 for p in paths)
 assert Counter((p['donor'],p['coordinate'])for p in paths)==Counter((j,t)for j in remaining for t in range(8))
 tile_h={r[3]for r in route.values()if r[0]=='Y'and r[4]==12}
 for p in paths:
  j,h,d,k=p['donor'],p['H'],p['D'],p['K'];a,b,c,e=[route[f]for f in p['owners']]
  assert all(r[0]=='Y'for r in [a,b,c,e])
  assert a[6]==j and a[3]==h and b[3]==h and b[4]==d and c[4]==d and c[5]==k and e[5]==k and e[1]==80
  assert j in H[h]and H[h]<=set(layout['D4'][d])and 80 in H[k]and H[k]<=set(layout['D4'][layout['dual_D4'][d]])
  assert h not in tile_h and p['owners'][2]not in set(yout.values())|set(yd.values())and p['owners'][3]not in set(yd.values())
 actions=[];caches=tile['caches'][:];pure=[]
 def act(stage,chart,word,tag,is_pure=False):
  if word:actions.append({'stage':stage,'chart':chart,'word':word,'tag':tag})
  if is_pure:pure.append((STAGES.index(stage),len(pure),word))
 for a in tile['actions']:
  if a['stage']in STAGES[:6]or a['stage']=='Y_H'or a['stage']=='Y_D'and a['tag']!='D-late-Cauchy':actions.append(a)
 for p in paths:
  j,t=p['donor'],p['coordinate'];c=PUBLIC+len(caches);sources=[fid('X',j,s)for s in targets(neighbors,j,t)]
  caches.append({'field':c,'chart':['L',j],'source_fields':sources,'tag':f'native-parity-{j}-{t}'})
  act('X_NATIVE',['L',j],[['INIT',5*c+b]for b in range(5)]+[op for s in sources for op in add_field(c,s)],f'capture-native-{j}-{t}')
  act('Y_LINE',['L',j],add_field(p['owners'][0],c)+[['CLEAR',5*c+b]for b in range(5)],f'inject-native-{j}-{t}')
 for stage,index,chartkey in [('Y_H',1,'H'),('Y_D',2,'D')]:
  groups=defaultdict(list)
  for p in paths:groups[p[chartkey]].append((p['owners'][index],p['owners'][index-1]))
  for chart,pairs in sorted(groups.items()):act(stage,[chartkey,chart],permute(pairs),f'flow-{chartkey}-{chart}',True)
 # Put the D12 pure map before its retained cross-cache additions.
 old=next(a for a in tile['actions']if a['tag']=='D-late-Cauchy');actions.insert(0,old);pure.append((STAGES.index('Y_D'),len(pure),old['word']))
 kg=defaultdict(list)
 for p in paths:kg[p['K']].append((p['owners'][3],p['owners'][2]))
 for k in ks:kg[k].append((yd[k],yout[k]))
 for k,pairs in sorted(kg.items()):act('Y_K',['K',k],permute(pairs),f'joint-route-K-{k}',True)
 fpairs=[(fid('Y',80,4+t),yd[k])for t,k in enumerate(ks)]+[(fid('Y',80,8+z),p['owners'][3])for z,p in enumerate(paths)]
 act('Y_F',['F',80],permute(fpairs),'final-packet-placement',True)
 act('Y_F',['F',80],[op for z,p in enumerate(paths)for op in add_field(fid('Y',80,p['coordinate']),fid('Y',80,8+z))],'final-flow-accumulation',True)
 for a in tile['actions']:
  if a['stage']=='Y_F'and a['tag']!='final-Y-coordinate-order':actions.append(a)
 pure.sort();act('GROUND_PRELOAD',['Ground'],[op for _,__,word in reversed(pure)for op in reversed(word)],'inverse-arbitrary-Y-baseline')
 actions.sort(key=lambda a:STAGES.index(a['stage']))
 replay_and_save(args.out,actions,caches,route,neighbors,paths,tile['source_donors'])
def replay(actions,caches,route,neighbors):
 symbolic={};owned=set();counts=Counter();peak=0;dirty=0
 def get(bit):return symbolic.get(bit,1<<bit)if bit<5*PUBLIC else symbolic[bit]
 for act in actions:
  for op in act['word']:
   for bit in op[1:]:assert location(act['stage'],bit//5,route,caches)==act['chart'],(act['tag'],op,location(act['stage'],bit//5,route,caches),act['chart'])
   counts[op[0]]+=1
   if op[0]=='ADD':
    assert op[1]!=op[2];symbolic[op[1]]=get(op[1])^get(op[2])
   elif op[0]=='INIT':assert op[1]not in owned and op[1]>=5*PUBLIC;symbolic[op[1]]=0;owned.add(op[1]);peak=max(peak,len(owned))
   elif op[0]=='CLEAR':
    assert op[1]in owned;dirty+=bool(symbolic[op[1]]);owned.remove(op[1]);del symbolic[op[1]]
   else:raise AssertionError(op)
 assert not owned
 ax=[b for b in symbolic if b<5*N*B];allx=all(symbolic[b]==1<<b for b in ax)
 ymask=((1<<(5*PUBLIC))-1)^((1<<(5*N*B))-1)
 ay=[b for b in symbolic if 5*N*B<=b<5*PUBLIC];ally=all(symbolic[b]&ymask==1<<b for b in ay)
 tr=[];target_ok=True
 for t in range(8):
  support=[fid('X',j,c)for j in neighbors for c in targets(neighbors,j,t)]
  for bit in range(5):
   output=5*fid('Y',80,t)+bit;expected=1<<output
   for f in support:expected^=1<<(5*f+bit)
   target_ok &= get(output)==expected
   tr.append({'output_bit':output,'source_bit_indices':[5*f+bit for f in support]})
 xmask=(1<<(5*N*B))-1;nonzero_x_output_fields={b//5 for b in ay if symbolic[b]&xmask}
 return {'all_original_X_restored':allx,'arbitrary_original_Y_baseline_restored':ally,'all_62_donor_target_rows_exact':target_ok,'ADD':counts['ADD'],'INIT':counts['INIT'],'CLEAR':counts['CLEAR'],'dirty_CLEAR':dirty,'peak':peak,'affected_original_X_bits':len(ax),'affected_original_Y_bits':len(ay),'actual_X_dependent_output_fields':len(nonzero_x_output_fields),'partial_word_return_rank_lower_bound_fields':N*B-len(nonzero_x_output_fields),'target_supports':tr}
def replay_and_save(out,actions,caches,route,neighbors,paths,tile_donors):
 result=replay(actions,caches,route,neighbors)
 assert result['all_original_X_restored']and result['arbitrary_original_Y_baseline_restored']and result['all_62_donor_target_rows_exact'],result
 assert result['INIT']==result['CLEAR']==result['peak']==2340 and result['dirty_CLEAR']==2340
 invoice={'ADD':result['ADD'],'INIT':result['INIT'],'dirty_CLEAR':result['dirty_CLEAR'],'extra_peak_binary_owners':result['peak'],'public_binary_owners':5*PUBLIC,'peak_total_binary_owners':5*PUBLIC+result['peak'],'proper_MOVE_binary_counts':{'1':5*267060,'2':5*216390,'4':5*11520},'added_MOVE':0,'canonical_return_included':False}
 word={'schema':'native-bank480-target-row80-v1','field_modulus':0x25,'field_bits':5,'bank_fields':B,'receiver':80,'selected_target_rows':list(range(8)),'public_route_pin':PINS['routes'],'tile_word_pin':TILE_PIN,'actions':actions,'caches':caches,'invoice':invoice,'owner_label_rule':'X fields0..53279; Y fields53280..106559; field bit5*f+r; owned fields>=106560'}
 out.mkdir(parents=True,exist_ok=True);wr=json.dumps(word,sort_keys=True,separators=(',',':')).encode();(out/'WORD.json.gz').write_bytes(gzip.compress(wr,mtime=0))
 certificate={'paths':paths,'tile_donors':tile_donors,'all_neighbors':neighbors,'target_supports':result.pop('target_supports')}
 cr=json.dumps(certificate,sort_keys=True,separators=(',',':')).encode();(out/'ROUTING.json.gz').write_bytes(gzip.compress(cr,mtime=0))
 result.update({'status':'PASS_COMPLETE_EIGHT_FIELD_ROW_NATIVE_TARGET_PROJECTION','source_pins':PINS,'tile_word_pin':TILE_PIN,'word_decompressed_sha256':sha256(wr).hexdigest(),'routing_decompressed_sha256':sha256(cr).hexdigest(),'fixed_target_field_rows':8,'source_donors':len(neighbors),'tile_donors':len(tile_donors),'additional_exact_paths':len(paths),'native_captures':400,'path_distinct_H':len({p['H']for p in paths}),'path_distinct_D':len({p['D']for p in paths}),'path_distinct_K':len({p['K']for p in paths}),'binary_original_input_columns_in_scope':5*PUBLIC,'invoice':invoice,'actions':len(actions),'complete_receiver_480row_endpoint':False,'global_irreducible_target_realized':False,'new_complete_kappa':False})
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
