#!/usr/bin/env python3
"""Build a literal paid eight-row target tile through the bank480 D12 chart."""
import argparse,gzip,json
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
from field import INV,reduce,mm,linear_word,add_field,swap_field
B=480;N=111;PUBLIC=2*N*B
PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','phase':'a806cc80a7bc7955fa07e04384707deb38200bac682424682e997f742dc5e278'}
def fid(kind,j,c):return (0 if kind=='X'else N*B)+j*B+c
def target_rows(neighbors,j):
 a=[[int(r==c)for c in range(B)]for r in range(8)];pos=neighbors.index(j)
 if pos==0:
  for r in range(7):a[r][r+1]^=1
 elif pos==1:a[7][0]^=1
 elif pos<=60:
  for r in range(8):a[r][8*(pos-1)+r]^=1
 return a
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 base=args.repo/'research/moonshot-005-program/results';atlas=base/'bit-asymmetric-balanced-atlas/author'
 paths={'layout':base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','routes':atlas/'output/ROUTES.jsonl.gz','phase':atlas/'PHASE-CERTIFICATE.json'}
 raw={k:gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes()for k,p in paths.items()}
 assert all(sha256(v).hexdigest()==PINS[k]for k,v in raw.items())
 lay=json.loads(raw['layout']);phase=json.loads(raw['phase']);routes=[json.loads(line)for line in raw['routes'].splitlines()]
 roots=lay['root_table'];H=list(map(set,lay['A2']));D=list(map(set,lay['D4']));dual=lay['dual_D4'];d=12;i=80
 hs=[h for h,W in enumerate(H)if W<=D[d]];ks=[k for k,W in enumerate(H)if W<=D[dual[d]]];donors=sorted(D[d]);receivers=sorted(D[dual[d]])
 neighbors=[j for j in range(N)if sum(a*b for a,b in zip(roots[i],roots[j]))==0]
 assert len(hs)==len(ks)==16 and max(donors+receivers)<111 and i in receivers
 assert not set(phase['full_early_planes']).intersection(hs+ks)
 selected_k=[k for k in ks if i in H[k]];assert selected_k==[370,371,372,373];R=[ks.index(k)for k in selected_k]
 rx={};ry={};XH=defaultdict(list);XK=defaultdict(list);YK=defaultdict(list);route={}
 for rr in routes:
  kind,j,c,h,dd,k,lj,ri=rr;f=fid(kind,j,c);assert f not in route;route[f]=rr
  if kind=='X':
   XH[j,h].append(f)
   if k is not None:XK[k,ri].append(f)
  else:YK[k,j].append(f)
  if dd==d:(rx if kind=='X'else ry)[h]=f
 assert len(rx)==len(ry)==16 and set(rx)==set(ry)==set(hs)
 xout={route[f][5]:f for f in rx.values()};yout={route[f][5]:f for f in ry.values()};assert set(xout)==set(yout)==set(ks)
 A=[[INV[r^(16+c)]for c in range(16)]for r in range(16)];assert reduce(A)==16
 actions=[];caches=[];early=[];latepure=[];source_u={};source_v={};Fs={};slots_all={};transfers=[]
 def action(stage,chart,word,tag):
  if word:actions.append({'stage':stage,'chart':chart,'word':word,'tag':tag})
 def cache(stage,chart,src,tag):
  dst=PUBLIC+len(caches);caches.append({'field':dst,'chart':chart,'source':src,'tag':tag})
  action(stage,chart,[['INIT',5*dst+b]for b in range(5)]+add_field(dst,src),tag);return dst
 def clear(stage,chart,f,tag):action(stage,chart,[['CLEAR',5*f+b]for b in range(5)],tag)
 for j in donors:
  jhs=[h for h in hs if j in H[h]];assert len(jhs)==4;cols=[hs.index(h)for h in jhs]
  aa=[[A[r][c]for c in cols]for r in R];cc=[[int(r==c)for c in cols]for r in R]
  assert reduce(aa)==4;S=[row+[0]*4 for row in aa]+[c+a for c,a in zip(cc,aa)];assert reduce(S)==8
  target=target_rows(neighbors,j);F=mm(reduce(S,True),target);assert mm(S,F)==target and reduce(F)==8
  Fs[j]=F;transfers.append({'donor':j,'left_planes':jhs,'transfer':S,'target':target})
  for h in jhs:
   available=sorted(XH[j,h]);assert len(available)==15
   u=rx[h]if route[rx[h]][1]==j else available[0];v=next(f for f in available if f!=u)
   source_u[j,h]=u;source_v[j,h]=v
  slots=[source_u[j,h]%B for h in jhs]+[source_v[j,h]%B for h in jhs];assert len(set(slots))==8;slots_all[j]=slots
  active=sorted(set(range(8))|{c for row in F for c,x in enumerate(row)if x})
  E=[[F[r][c]if r<8 else int(r==c)for c in active]for r in active];assert reduce(E)==len(active)
  word=linear_word(E,[fid('X',j,c)for c in active]);order=list(range(B));pos=list(range(B))
  for t,dst in enumerate(slots):
   src=pos[t]
   if src!=dst:
    word+=swap_field(fid('X',j,src),fid('X',j,dst));old=order[dst];order[src],order[dst]=old,t;pos[old],pos[t]=src,dst
  assert all(order[slots[t]]==t for t in range(8))
  action('X_NATIVE',['L',j],word,f'source-{j}');early.append(word)
 hc={}
 for h in hs:
  us=[source_u[j,h]for j in sorted(H[h])];vs=[source_v[j,h]for j in sorted(H[h])];assert rx[h]in us
  word=[op for u in us if u!=rx[h]for op in add_field(rx[h],u)]
  action('X_H',['H',h],word,f'early-H-{h}');early.append(word)
  hc[h]=[cache('X_H',['H',h],v,f'H-cache-{h}-{t}')for t,v in enumerate(vs)]
 dc=[cache('X_D',['D',d],rx[h],f'D-cache-{h}')for h in hs]
 xf=[rx[h]for h in hs];px={f:t for t,f in enumerate(xf)};E=[[0]*16 for _ in range(16)]
 for r,k in enumerate(ks):E[px[xout[k]]]=A[r][:]
 dx=linear_word(E,xf);action('X_D',['D',d],dx,'D-early-Cauchy');early.append(dx)
 kx={};ky={}
 for k in selected_k:
  sx=xout[k];tx=sx if route[sx][7]==i else min(XK[k,i]);kx[k]=tx
  word=swap_field(sx,tx);action('X_K',['K',k],word,f'route-X-{k}');early.append(word)
  sy=yout[k];ky[k]=sy if route[sy][1]==i else min(YK[k,i])
 fc=[cache('X_F',['F',i],kx[k],f'F-cache-{k}')for k in selected_k]
 action('HUB_RESTORE',['Hub'],[op for word in reversed(early)for op in reversed(word)],'restore-all-X')
 yf=[ry[h]for h in hs];py={f:t for t,f in enumerate(yf)};G=[[0]*16 for _ in range(16)]
 for r,k in enumerate(ks):G[py[yout[k]]]=A[r][:]
 dy=linear_word(G,yf);latepure.append(dy);kywords=[]
 for k in selected_k:
  word=swap_field(yout[k],ky[k]);kywords.append((k,word));latepure.append(word)
 fy=[];order=list(range(B));pos=list(range(B))
 for t,k in enumerate(selected_k):
  val=ky[k]%B;dst=4+t;src=pos[val]
  if src!=dst:
   fy+=swap_field(fid('Y',i,src),fid('Y',i,dst));old=order[dst];order[src],order[dst]=old,val;pos[old],pos[val]=src,dst
 assert all(order[4+t]==ky[k]%B for t,k in enumerate(selected_k));latepure.append(fy)
 action('GROUND_PRELOAD',['Ground'],[op for word in reversed(latepure)for op in reversed(word)],'inverse-arbitrary-Y-baseline')
 for h in hs:
  for t,c in enumerate(hc[h]):
   action('Y_H',['H',h],add_field(ry[h],c),f'late-H-{h}-{t}');clear('Y_H',['H',h],c,f'clear-H-{h}-{t}')
 action('Y_D',['D',d],dy,'D-late-Cauchy')
 for r,k in enumerate(ks):
  action('Y_D',['D',d],add_field(yout[k],dc[r]),f'D-cross-{r}');clear('Y_D',['D',d],dc[r],f'clear-D-{r}')
 for k,word in kywords:action('Y_K',['K',k],word,f'route-Y-{k}')
 action('Y_F',['F',i],fy,'final-Y-coordinate-order')
 for t,c in enumerate(fc):
  action('Y_F',['F',i],add_field(fid('Y',i,t),c),f'final-early-add-{t}');clear('Y_F',['F',i],c,f'clear-F-{t}')
 assert len(caches)==68
 stages=['X_NATIVE','X_H','X_D','X_K','X_F','HUB_RESTORE','GROUND_PRELOAD','Y_H','Y_D','Y_K','Y_F']
 def location(stage,f):
  if f>=PUBLIC:return caches[f-PUBLIC]['chart']
  kind,j,c,h,dd,k,lj,ri=route[f]
  if kind=='X':
   if stage=='X_NATIVE':return ['L',j]
   if stage=='X_H':return ['H',h]
   if stage=='X_D':return ['D',dd]
   if stage=='X_K':return ['K',k]if k is not None else ['Hub']
   if stage=='X_F':return ['F',ri]if ri is not None else ['Hub']
   return ['Hub']
  if stage in stages[:7]:return ['Ground']
  if stage=='Y_H':return ['H',h]if h is not None else ['D',dd]
  if stage=='Y_D':return ['D',dd]
  if stage=='Y_K':return ['K',k]
  return ['F',j]
 actions.sort(key=lambda a:stages.index(a['stage']))
 symbolic={};owned=set();counts=Counter();peak=0;dirty=0
 def get(bit):return symbolic.get(bit,1<<bit)if bit<5*PUBLIC else symbolic[bit]
 for act in actions:
  for op in act['word']:
   for bit in op[1:]:assert location(act['stage'],bit//5)==act['chart'],(act['tag'],op,location(act['stage'],bit//5),act['chart'])
   counts[op[0]]+=1
   if op[0]=='ADD':symbolic[op[1]]=get(op[1])^get(op[2])
   elif op[0]=='INIT':assert op[1]not in owned;symbolic[op[1]]=0;owned.add(op[1]);peak=max(peak,len(owned))
   elif op[0]=='CLEAR':
    assert op[1]in owned;dirty+=bool(symbolic[op[1]]);owned.remove(op[1]);del symbolic[op[1]]
   else:raise AssertionError(op)
 assert not owned
 affectedX=[b for b in symbolic if b<5*N*B];assert all(symbolic[b]==1<<b for b in affectedX)
 ymask=((1<<(5*PUBLIC))-1)^((1<<(5*N*B))-1)
 affectedY=[b for b in symbolic if 5*N*B<=b<5*PUBLIC];assert all(symbolic[b]&ymask==1<<b for b in affectedY)
 targets=[]
 for t in range(8):
  support=[fid('X',j,c)for j in donors for c,x in enumerate(target_rows(neighbors,j)[t])if x]
  for bit in range(5):
   output=5*fid('Y',i,t)+bit;expected=1<<output
   for f in support:expected^=1<<(5*f+bit)
   assert get(output)==expected,(t,bit)
   targets.append({'output_bit':output,'source_bit_indices':[5*f+bit for f in support]})
 assert counts['INIT']==counts['CLEAR']==peak==340 and dirty==340
 invoice={'ADD':counts['ADD'],'INIT':counts['INIT'],'dirty_CLEAR':dirty,'extra_peak_binary_owners':peak,'public_binary_owners':5*PUBLIC,'peak_total_binary_owners':5*PUBLIC+peak,'proper_MOVE_binary_counts':{'1':5*267060,'2':5*216390,'4':5*11520},'added_MOVE':0,'canonical_return_included':False}
 word={'schema':'native-bank480-target-tile-v1','field_modulus':0x25,'field_bits':5,'bank_fields':B,'receiver':i,'middle':d,'source_donors':donors,'selected_target_rows':list(range(8)),'public_route_pin':PINS['routes'],'actions':actions,'caches':caches,'invoice':invoice,'owner_label_rule':'X fields0..53279; Y fields53280..106559; field bit5*f+r; owned fields>=106560'}
 args.out.mkdir(parents=True,exist_ok=True);raw=json.dumps(word,sort_keys=True,separators=(',',':')).encode();(args.out/'WORD.json.gz').write_bytes(gzip.compress(raw,mtime=0))
 matrices={'Cauchy':A,'D':d,'dual_D':dual[d],'H':hs,'K':ks,'selected_K':selected_k,'target_row80_neighbor_order':neighbors,'source_maps':Fs,'source_slots':slots_all,'pair_transfers':transfers,'target_bit_supports':targets}
 data=json.dumps(matrices,sort_keys=True,separators=(',',':')).encode();(args.out/'MATRICES.json.gz').write_bytes(gzip.compress(data,mtime=0))
 result={'status':'PASS_LITERAL_NATIVE_D4_TARGET_TILE','source_pins':PINS,'middle':d,'dual_middle':dual[d],'receiver':i,'native_donors':donors,'early_and_late_fields_each':16,'fixed_target_field_rows':8,'original_input_field_columns_in_scope':PUBLIC,'binary_original_input_columns_in_scope':5*PUBLIC,'exact_target_binary_rows':len(targets),'invertible_source_8row_lifts':len(donors),'all_original_X_restored':True,'arbitrary_original_Y_baseline_restored':True,'word_decompressed_sha256':sha256(raw).hexdigest(),'matrices_decompressed_sha256':sha256(data).hexdigest(),'invoice':invoice,'actions':len(actions),'affected_original_X_bits':len(affectedX),'affected_original_Y_bits':len(affectedY),'complete_native_endpoint':False,'global_irreducible_target_realized':False,'new_complete_kappa':False}
 (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
