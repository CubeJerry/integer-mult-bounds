#!/usr/bin/env python3
"""Shared D12: first four prescribed rows at receivers80 and1, paid word."""
import argparse,gzip,json
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
from field import INV,T,reduce,mm,linear_word,add_field,swap_field
B=480;N=111;PUBLIC=2*N*B
PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','phase':'a806cc80a7bc7955fa07e04384707deb38200bac682424682e997f742dc5e278'}
STAGES=['X_NATIVE','X_H','X_D','X_K','X_F','HUB_RESTORE','GROUND_PRELOAD','Y_LINE','Y_H','Y_D','Y_K','Y_F']
def fid(kind,j,c):return (0 if kind=='X'else N*B)+j*B+c
def rows80(neighbors,j):
 a=[[int(r==c)for c in range(B)]for r in range(4)];p=neighbors.index(j)
 if p==0:
  for r in range(4):a[r][r+1]^=1
 elif 2<=p<=60:
  for r in range(4):a[r][8*(p-1)+r]^=1
 return a
def coeff_add(dst,src,alpha):
 return [['ADD',5*dst+r,5*src+s]for s in range(5)for r in range(5)if T[alpha][1<<s]>>r&1]
def permutation(pairs):
 assert len(pairs)==len({d for d,s in pairs})==len({s for d,s in pairs})
 fields={f for pair in pairs for f in pair};order={f:f for f in fields};pos=order.copy();word=[]
 for dst,val in pairs:
  src=pos[val]
  if src!=dst:
   word+=swap_field(dst,src);old=order[dst];order[src],order[dst]=old,val;pos[old],pos[val]=src,dst
 assert all(order[d]==s for d,s in pairs);return word
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
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 base=args.repo/'research/moonshot-005-program/results';atlas=base/'bit-asymmetric-balanced-atlas/author'
 pp={'layout':base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','routes':atlas/'output/ROUTES.jsonl.gz','phase':atlas/'PHASE-CERTIFICATE.json'}
 raw={k:gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes()for k,p in pp.items()};assert all(sha256(v).hexdigest()==PINS[k]for k,v in raw.items())
 layout=json.loads(raw['layout']);phase=json.loads(raw['phase']);routes=[json.loads(s)for s in raw['routes'].splitlines()];route={fid(r[0],r[1],r[2]):r for r in routes};assert len(route)==PUBLIC
 H=list(map(set,layout['A2']));D=list(map(set,layout['D4']));roots=layout['root_table'];d=12;dual=layout['dual_D4'][d]
 hs=[h for h,W in enumerate(H)if W<=D[d]];ks=[k for k,W in enumerate(H)if W<=D[dual]];donors=sorted(D[d]);neighbors=[j for j in range(N)if sum(a*b for a,b in zip(roots[80],roots[j]))==0]
 k80=[k for k in ks if 80 in H[k]];k1=[k for k in ks if 1 in H[k]];r80=[ks.index(k)for k in k80];r1=[ks.index(k)for k in k1]
 assert len(hs)==len(ks)==16 and len(k80)==len(k1)==4 and set(k80)&set(k1)=={370}
 assert not set(phase['full_early_planes']).intersection(hs+ks)
 XH=defaultdict(list);YL=defaultdict(list);XK=defaultdict(list);YK=defaultdict(list);rx={};ry={}
 for f,r in route.items():
  kind,j,c,h,dd,k,line,term=r
  if kind=='X':XH[j,h].append(f);XK[k,term].append(f)
  else:YL[line,h].append(f);YK[k,j].append(f)
  if dd==12:(rx if kind=='X'else ry)[h]=f
 xo={route[f][5]:f for f in rx.values()};yo={route[f][5]:f for f in ry.values()}
 A=[[INV[r^(16+c)]for c in range(16)]for r in range(16)]
 actions=[];caches=[];early=[];pure=[];sources={};late_sources={};matrices=[]
 def action(stage,chart,word,tag,pure_y=False):
  if word:actions.append({'stage':stage,'chart':chart,'word':word,'tag':tag})
  if pure_y:pure.append((STAGES.index(stage),len(pure),word))
 def allocate(stage,chart,wordmaker,tag):
  f=PUBLIC+len(caches);caches.append({'field':f,'chart':chart,'tag':tag});action(stage,chart,[['INIT',5*f+b]for b in range(5)]+wordmaker(f),tag);return f
 for j in donors:
  jhs=[h for h in hs if j in H[h]];cols=[hs.index(h)for h in jhs]
  M=[[A[r][c]for c in cols]for r in r80];G=[[A[r][c]for c in cols]for r in r1]
  target=rows80(neighbors,j);U=mm(reduce(M,True),target);V=reduce(G,True)
  assert mm(M,U)==target and mm(G,V)==[[int(r==c)for c in range(4)]for r in range(4)]
  matrices.append({'donor':j,'H':jhs,'U':U,'V':V,'early_minor':M,'late_minor':G})
  # Native late captures precede the source chart change and may be dependent on U.
  for t,h in enumerate(jhs):
   v=allocate('X_NATIVE',['L',j],lambda f,t=t:[op for s,alpha in enumerate(V[t])for op in coeff_add(f,fid('X',j,s),alpha)],f'native-late-{j}-{h}')
   holder=ry[h]if route[ry[h]][6]==j else min(YL[j,h]);late_sources[j,h]=holder
   action('Y_LINE',['L',j],add_field(holder,v)+[['CLEAR',5*v+b]for b in range(5)],f'late-inject-{j}-{h}')
   sources[j,h]=rx[h]if route[rx[h]][1]==j else min(XH[j,h])
  active=sorted(set(range(4))|{c for row in U for c,x in enumerate(row)if x});E=[[U[r][c]if r<4 else int(r==c)for c in active]for r in active]
  assert reduce(E)==len(active)
  word=linear_word(E,[fid('X',j,c)for c in active]);word+=permutation([(sources[j,h],fid('X',j,t))for t,h in enumerate(jhs)])
  action('X_NATIVE',['L',j],word,f'early-source-{j}');early.append(word)
 for h in hs:
  us=[sources[j,h]for j in sorted(H[h])];vs=[late_sources[j,h]for j in sorted(H[h])]
  assert rx[h]in us and ry[h]in vs
  w=[op for u in us if u!=rx[h]for op in add_field(rx[h],u)];action('X_H',['H',h],w,f'sum-X-H-{h}');early.append(w)
  action('Y_H',['H',h],[op for v in vs if v!=ry[h]for op in add_field(ry[h],v)],f'sum-Y-H-{h}',True)
 for kind,inputs,outputs,stage in [('X',rx,xo,'X_D'),('Y',ry,yo,'Y_D')]:
  fs=[inputs[h]for h in hs];pos={f:t for t,f in enumerate(fs)};M=[[0]*16 for _ in range(16)]
  for r,k in enumerate(ks):M[pos[outputs[k]]]=A[r][:]
  word=linear_word(M,fs);action(stage,['D',12],word,f'D12-{kind}-Cauchy',kind=='Y')
  if kind=='X':early.append(word)
 kxd={};kyd={}
 for k in k80:
  src=xo[k];dst=src if route[src][7]==80 else min(XK[k,80]);kxd[k]=dst;w=swap_field(src,dst);action('X_K',['K',k],w,f'early-K-{k}');early.append(w)
 for k in k1:
  src=yo[k];dst=src if route[src][1]==1 else min(YK[k,1]);kyd[k]=dst;action('Y_K',['K',k],swap_field(src,dst),f'late-K-{k}',True)
 fc=[allocate('X_F',['F',80],lambda f,k=k:add_field(f,kxd[k]),f'early-F80-{k}')for k in k80]
 action('HUB_RESTORE',['Hub'],[op for word in reversed(early)for op in reversed(word)],'restore-all-X')
 action('Y_F',['F',1],permutation([(fid('Y',1,t),kyd[k])for t,k in enumerate(k1)]),'target-F1-order',True)
 # Conservatively track all late X contamination, including unused native taps.
 bad=set(late_sources.values())
 badbits={5*f+b for f in bad for b in range(5)}
 for _,__,word in sorted(pure):
  for op,dst,src in word:
   if src in badbits:badbits.add(dst)
 badfields={bit//5 for bit in badbits}
 clean=[fid('Y',80,c)for c in range(B)if fid('Y',80,c)not in badfields][:4];assert len(clean)==4
 action('Y_F',['F',80],permutation([(fid('Y',80,t),s)for t,s in enumerate(clean)]),'isolate-early-F80',True)
 for t,c in enumerate(fc):action('Y_F',['F',80],add_field(fid('Y',80,t),c)+[['CLEAR',5*c+b]for b in range(5)],f'early-target-add-{t}')
 pure.sort();action('GROUND_PRELOAD',['Ground'],[op for _,__,word in reversed(pure)for op in reversed(word)],'inverse-arbitrary-Y')
 actions.sort(key=lambda a:STAGES.index(a['stage']))
 replay_save(args.out,actions,caches,route,neighbors,donors,matrices,{'H':hs,'K':ks,'K80':k80,'K1':k1,'late_sources':[[j,h,f]for (j,h),f in late_sources.items()],'clean_Y80':clean})
def replay(actions,caches,route,neighbors,donors):
 symbolic={};owned=set();counts=Counter();peak=0;dirty=0
 def get(bit):return symbolic.get(bit,1<<bit)if bit<5*PUBLIC else symbolic[bit]
 for a in actions:
  for op in a['word']:
   for bit in op[1:]:assert location(a['stage'],bit//5,route,caches)==a['chart'],(a['tag'],op)
   counts[op[0]]+=1
   if op[0]=='ADD':assert op[1]!=op[2];symbolic[op[1]]=get(op[1])^get(op[2])
   elif op[0]=='INIT':assert op[1]>=5*PUBLIC and op[1]not in owned;owned.add(op[1]);symbolic[op[1]]=0;peak=max(peak,len(owned))
   elif op[0]=='CLEAR':assert op[1]in owned;dirty+=bool(get(op[1]));owned.remove(op[1]);del symbolic[op[1]]
   else:raise AssertionError(op)
 assert not owned
 ax=[b for b in symbolic if b<5*N*B];ay=[b for b in symbolic if 5*N*B<=b<5*PUBLIC];xmask=(1<<(5*N*B))-1;ymask=((1<<(5*PUBLIC))-1)^xmask
 allx=all(symbolic[b]==1<<b for b in ax);ally=all(symbolic[b]&ymask==1<<b for b in ay);targets=[];correct={}
 for i in [80,1]:
  correct[i]=True
  for t in range(4):
   fields=[fid('X',j,c)for j in donors for c,x in enumerate(rows80(neighbors,j)[t]if i==80 else [int(c==t)for c in range(B)])if x]
   for bit in range(5):
    output=5*fid('Y',i,t)+bit;expect=1<<output
    for f in fields:expect^=1<<(5*f+bit)
    correct[i]&=get(output)==expect;targets.append({'output_bit':output,'source_bit_indices':[5*f+bit for f in fields]})
 nonzero={b//5 for b in ay if symbolic[b]&xmask}
 return {'all_original_X_restored':allx,'arbitrary_original_Y_baseline_restored':ally,'target_rows_correct':correct,'ADD':counts['ADD'],'INIT':counts['INIT'],'CLEAR':counts['CLEAR'],'dirty_CLEAR':dirty,'extra_peak_binary_owners':peak,'affected_X_bits':len(ax),'affected_Y_bits':len(ay),'actual_X_dependent_output_fields':len(nonzero),'partial_word_return_rank_lower_bound_fields':N*B-len(nonzero),'target_supports':targets}
def replay_save(out,actions,caches,route,neighbors,donors,matrices,metadata):
 result=replay(actions,caches,route,neighbors,donors)
 assert result['all_original_X_restored']and result['arbitrary_original_Y_baseline_restored']and all(result['target_rows_correct'].values()),result
 assert result['INIT']==result['CLEAR']==result['dirty_CLEAR']==result['extra_peak_binary_owners']==260
 invoice={k:result[k]for k in ['ADD','INIT','dirty_CLEAR','extra_peak_binary_owners']};invoice.update({'public_binary_owners':5*PUBLIC,'peak_total_binary_owners':5*PUBLIC+260,'proper_MOVE_binary_counts':{'1':5*267060,'2':5*216390,'4':5*11520},'added_MOVE':0,'canonical_return_included':False})
 word={'schema':'native-bank480-shared-D12-pair-v1','field_modulus':0x25,'field_bits':5,'bank_fields':B,'receivers':[80,1],'selected_rows':list(range(4)),'source_donors':donors,'public_route_pin':PINS['routes'],'actions':actions,'caches':caches,'invoice':invoice}
 out.mkdir(parents=True,exist_ok=True);raw=json.dumps(word,sort_keys=True,separators=(',',':')).encode();(out/'WORD.json.gz').write_bytes(gzip.compress(raw,mtime=0))
 data=json.dumps({'matrices':matrices,'metadata':metadata,'neighbor80_order':neighbors,'target_supports':result.pop('target_supports')},sort_keys=True,separators=(',',':')).encode();(out/'MATRICES.json.gz').write_bytes(gzip.compress(data,mtime=0))
 result.update({'status':'PASS_LITERAL_SHARED_D12_TWO_RECEIVER_TILE','source_pins':PINS,'word_decompressed_sha256':sha256(raw).hexdigest(),'matrices_decompressed_sha256':sha256(data).hexdigest(),'invoice':invoice,'actions':len(actions),'new_complete_kappa':False,'complete_receiver_endpoints':False})
 (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
