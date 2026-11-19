#!/usr/bin/env python3
"""Stitch D12 and D99 by independent source masks and receiver cancellation."""
from common import *
DS=[12,99];RECEIVERS=[80,1]
def pivots(matrix):
 a=[r[:]for r in matrix];out=[];row=0
 for c in range(len(a[0])):
  k=next((k for k in range(row,len(a))if a[k][c]),None)
  if k is None:continue
  a[row],a[k]=a[k],a[row];a[row]=[T[INV[a[row][c]]][v]for v in a[row]]
  for k in range(len(a)):
   if k!=row and a[k][c]:a[k]=[x^T[a[k][c]][y]for x,y in zip(a[k],a[row])]
  out.append(c);row+=1
  if row==len(a):break
 assert row==len(matrix);return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--late-masks',action='store_true');args=ap.parse_args()
 base=args.repo/'research/moonshot-005-program/results';atlas=base/'bit-asymmetric-balanced-atlas/author'
 pp={'layout':base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','routes':atlas/'output/ROUTES.jsonl.gz','phase':atlas/'PHASE-CERTIFICATE.json'}
 raw={k:gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes()for k,p in pp.items()};assert all(sha256(v).hexdigest()==PINS[k]for k,v in raw.items())
 layout=json.loads(raw['layout']);phase=json.loads(raw['phase']);routes=[json.loads(s)for s in raw['routes'].splitlines()];route={fid(r[0],r[1],r[2]):r for r in routes};assert len(route)==PUBLIC
 H=list(map(set,layout['A2']));D=list(map(set,layout['D4']));roots=layout['root_table'];neighbors=[j for j in range(N)if sum(a*b for a,b in zip(roots[80],roots[j]))==0]
 hd={d:[h for h,W in enumerate(H)if W<=D[d]]for d in DS};kd={d:[k for k,W in enumerate(H)if W<=D[layout['dual_D4'][d]]]for d in DS};shared=sorted(D[12]&D[99]);donors=sorted(D[12]|D[99])
 assert shared==[5,7,42,43,44,45]and len(donors)==18 and set(hd[12])&set(hd[99])=={106,113,118,119}
 assert all({80,1}<=D[layout['dual_D4'][d]]and max(D[d]|D[layout['dual_D4'][d]])<111 for d in DS)
 assert not set(phase['full_early_planes']).intersection(set(sum(hd.values(),[])+sum(kd.values(),[])))
 XH=defaultdict(list);YL=defaultdict(list);XK=defaultdict(list);YK=defaultdict(list);rx={};ry={}
 for f,r in route.items():
  kind,j,c,h,d,k,line,term=r
  if kind=='X':XH[j,h].append(f);XK[k,term].append(f)
  else:YL[line,h].append(f);YK[k,j].append(f)
  if d in DS:(rx if kind=='X'else ry)[d,h]=f
 assert len(rx)==len(ry)==32
 xo={(d,route[f][5]):f for (d,h),f in rx.items()};yo={(d,route[f][5]):f for (d,h),f in ry.items()}
 A=[[INV[r^(16+c)]for c in range(16)]for r in range(16)]
 U={};V={};demands={};jhs={};ms=[]
 for d in DS:
  Ra=[kd[d].index(k)for k in kd[d]if 80 in H[k]];Rb=[kd[d].index(k)for k in kd[d]if 1 in H[k]]
  for j in sorted(D[d]):
   jhs[d,j]=[h for h in hd[d]if j in H[h]];C=[hd[d].index(h)for h in jhs[d,j]]
   u=rows80(neighbors,j);w=[[int(c==r)for c in range(B)]for r in range(4)];v=[[int(c==476+r)for c in range(B)]for r in range(4)]
   if j in shared:
    pu=[[x^y for x,y in zip(ur,vr)]for ur,vr in zip(u,v)]if d==12 else v
    if args.late_masks:qv=[[x^y for x,y in zip(wr,vr)]for wr,vr in zip(w,v)]if d==12 else v
    else:qv=w if d==12 else [[0]*B for _ in range(4)]
   else:pu=u;qv=w
   M=[[A[r][c]for c in C]for r in Ra];G=[[A[r][c]for c in C]for r in Rb]
   U[d,j]=mm(reduce(M,True),pu);V[d,j]=mm(reduce(G,True),qv);demands[d,j]=(pu,qv)
   assert mm(M,U[d,j])==pu and mm(G,V[d,j])==qv
   ms.append({'D':d,'donor':j,'H':jhs[d,j],'U':U[d,j],'V':V[d,j],'early_demand':pu,'late_demand':qv,'early_minor':M,'late_minor':G})
 for j in donors:
  ds=[d for d in DS if j in D[d]];assert reduce(sum([U[d,j]for d in ds],[]))==4*len(ds)
 sx={};sy={};usedx=defaultdict(set);usedy=defaultdict(set)
 for d in DS:
  for j in sorted(D[d]):
   for h in jhs[d,j]:
    reserve_x={f for (dd,hh),f in rx.items()if hh==h};reserve_y={f for (dd,hh),f in ry.items()if hh==h}
    x=rx[d,h]if route[rx[d,h]][1]==j else next(f for f in sorted(XH[j,h])if f not in reserve_x|usedx[j,h])
    y=ry[d,h]if route[ry[d,h]][6]==j else next(f for f in sorted(YL[j,h])if f not in reserve_y|usedy[j,h])
    assert x not in usedx[j,h]and y not in usedy[j,h];sx[d,j,h]=x;sy[d,j,h]=y;usedx[j,h].add(x);usedy[j,h].add(y)
 actions=[];caches=[];early=[];pure=[];source_bases=[]
 def act(stage,chart,word,tag,pure_y=False):
  if word:actions.append({'stage':stage,'chart':chart,'word':word,'tag':tag})
  if pure_y:pure.append((STAGES.index(stage),len(pure),word))
 def allocate(stage,chart,wordmaker,tag):
  f=PUBLIC+len(caches);caches.append({'field':f,'chart':chart,'tag':tag});act(stage,chart,[['INIT',5*f+b]for b in range(5)]+wordmaker(f),tag);return f
 for j in donors:
  ds=[d for d in DS if j in D[d]];stack=sum([U[d,j]for d in ds],[]);pv=pivots(stack)
  for d in ds:
   for t,h in enumerate(jhs[d,j]):
    if not any(V[d,j][t]):continue
    v=allocate('X_NATIVE',['L',j],lambda f,d=d,t=t:[op for c,alpha in enumerate(V[d,j][t])if alpha for op in coeff_add(f,fid('X',j,c),alpha)],f'capture-{d}-{j}-{h}')
    act('Y_LINE',['L',j],add_field(sy[d,j,h],v)+[['CLEAR',5*v+b]for b in range(5)],f'inject-{d}-{j}-{h}')
  active=sorted(set(pv)|{c for row in stack for c,x in enumerate(row)if x});rowmap={c:t for t,c in enumerate(pv)}
  E=[[stack[rowmap[r]][c]if r in rowmap else int(r==c)for c in active]for r in active];assert reduce(E)==len(active)
  fields=[fid('X',j,c)for c in active];word=linear_word(E,fields);slots=[sx[d,j,h]for d in ds for h in jhs[d,j]]
  word+=permutation(list(zip(slots,[fid('X',j,c)for c in pv])));act('X_NATIVE',['L',j],word,f'joint-source-{j}');early.append(word)
  source_bases.append({'donor':j,'tiles':ds,'rank':len(stack),'pivot_columns':pv,'active_columns':active,'output_owner_fields':slots})
 for d in DS:
  for h in hd[d]:
   us=[sx[d,j,h]for j in sorted(H[h])];vs=[sy[d,j,h]for j in sorted(H[h])];assert rx[d,h]in us and ry[d,h]in vs
   w=[op for f in us if f!=rx[d,h]for op in add_field(rx[d,h],f)];act('X_H',['H',h],w,f'early-H-{d}-{h}');early.append(w)
   act('Y_H',['H',h],[op for f in vs if f!=ry[d,h]for op in add_field(ry[d,h],f)],f'late-H-{d}-{h}',True)
  for kind,inputs,outputs,stage in [('X',rx,xo,'X_D'),('Y',ry,yo,'Y_D')]:
   fs=[inputs[d,h]for h in hd[d]];pos={f:t for t,f in enumerate(fs)};M=[[0]*16 for _ in range(16)]
   for r,k in enumerate(kd[d]):M[pos[outputs[d,k]]]=A[r][:]
   word=linear_word(M,fs);act(stage,['D',d],word,f'Cauchy-{kind}-{d}',kind=='Y')
   if kind=='X':early.append(word)
 def route_packets(receiver,outputs,bank,kind):
  groups=defaultdict(list)
  for d in DS:
   for k in kd[d]:
    if receiver in H[k]:groups[k].append((d,outputs[d,k]))
  dest={}
  for k,packets in sorted(groups.items()):
   taken=set();pairs=[]
   for d,src in packets:
    if src in bank[k,receiver]:dest[d,k]=src;taken.add(src)
   for d,src in packets:
    if (d,k)not in dest:dest[d,k]=next(f for f in sorted(bank[k,receiver])if f not in taken);taken.add(dest[d,k])
    pairs.append((dest[d,k],src))
   word=permutation(pairs);act(f'{kind}_K',['K',k],word,f'joint-{kind}-K-{k}',kind=='Y')
   if kind=='X':early.append(word)
  return dest
 xd=route_packets(80,xo,XK,'X');yd=route_packets(1,yo,YK,'Y')
 fc=[]
 for t in range(4):
  packets=[xd[d,[k for k in kd[d]if 80 in H[k]][t]]for d in DS]
  fc.append((t,allocate('X_F',['F',80],lambda f,packets=packets:[op for src in packets for op in add_field(f,src)],f'capture-F80-joint-{t}')))
 act('HUB_RESTORE',['Hub'],[op for word in reversed(early)for op in reversed(word)],'restore-all-X')
 pairs=[(fid('Y',1,4*z+t),yd[d,k])for z,d in enumerate(DS)for t,k in enumerate(k for k in kd[d]if 1 in H[k])]
 act('Y_F',['F',1],permutation(pairs),'F1-packet-order',True)
 act('Y_F',['F',1],[op for t in range(4)for op in add_field(fid('Y',1,t),fid('Y',1,4+t))],'F1-cancel-shared-masks',True)
 # Treat every native cache bit as independent to locate certainly clean Y80 slots.
 late={}
 for a in actions:
  if a['stage']=='Y_LINE':
   for op in a['word']:
    if op[0]=='ADD':late[op[1]]=late.get(op[1],0)^(1<<(op[2]-5*PUBLIC))
 for _,__,word in sorted(pure):
  for op,dst,src in word:late[dst]=late.get(dst,0)^late.get(src,0)
 bad={bit//5 for bit,x in late.items()if x};assert len(bad)<=100
 clean=[fid('Y',80,c)for c in range(B)if fid('Y',80,c)not in bad][:4];assert len(clean)==4
 act('Y_F',['F',80],permutation([(fid('Y',80,t),s)for t,s in enumerate(clean)]),'isolate-F80-target',True)
 for z,(t,c)in enumerate(fc):act('Y_F',['F',80],add_field(fid('Y',80,t),c)+[['CLEAR',5*c+b]for b in range(5)],f'F80-cancel-shared-masks-{z}')
 pure.sort();act('GROUND_PRELOAD',['Ground'],[op for _,__,word in reversed(pure)for op in reversed(word)],'inverse-arbitrary-Y')
 actions.sort(key=lambda a:STAGES.index(a['stage']))
 result=replay(actions,caches,route,neighbors,donors)
 assert result['all_original_X_restored']and result['arbitrary_original_Y_baseline_restored']and all(result['target_rows_correct'].values()),result
 extra=500 if args.late_masks else 380
 assert result['INIT']==result['CLEAR']==result['dirty_CLEAR']==result['extra_peak_binary_owners']==extra
 invoice={k:result[k]for k in ['ADD','INIT','dirty_CLEAR','extra_peak_binary_owners']};invoice.update({'public_binary_owners':5*PUBLIC,'peak_total_binary_owners':5*PUBLIC+extra,'proper_MOVE_binary_counts':{'1':5*267060,'2':5*216390,'4':5*11520},'added_MOVE':0,'canonical_return_included':False})
 word={'schema':'native-bank480-overlapping-D12-D99-stitch-v1','field_modulus':0x25,'field_bits':5,'bank_fields':B,'receivers':RECEIVERS,'selected_rows':list(range(4)),'middle_tiles':DS,'source_donors':donors,'shared_donors':shared,'mask_coordinates':list(range(476,480)),'late_masks':args.late_masks,'public_route_pin':PINS['routes'],'actions':actions,'caches':caches,'invoice':invoice}
 args.out.mkdir(parents=True,exist_ok=True);wr=json.dumps(word,sort_keys=True,separators=(',',':')).encode();(args.out/'WORD.json.gz').write_bytes(gzip.compress(wr,mtime=0))
 cert={'matrices':ms,'source_bases':source_bases,'H':hd,'K':kd,'source_X_owners':[[d,j,h,f]for (d,j,h),f in sx.items()],'source_Y_owners':[[d,j,h,f]for (d,j,h),f in sy.items()],'early_K_destinations':[[d,k,f]for (d,k),f in xd.items()],'late_K_destinations':[[d,k,f]for (d,k),f in yd.items()],'clean_Y80':clean,'neighbor80_order':neighbors,'target_supports':result.pop('target_supports')}
 cr=json.dumps(cert,sort_keys=True,separators=(',',':')).encode();(args.out/'CERTIFICATE.json.gz').write_bytes(gzip.compress(cr,mtime=0))
 result.update({'status':'PASS_LITERAL_OVERLAPPING_TWO_D_MASK_STITCH','source_pins':PINS,'word_decompressed_sha256':sha256(wr).hexdigest(),'certificate_decompressed_sha256':sha256(cr).hexdigest(),'invoice':invoice,'actions':len(actions),'native_donors':len(donors),'shared_donors':shared,'shared_H':sorted(set(hd[12])&set(hd[99])),'shared_K':sorted(set(kd[12])&set(kd[99])),'joint_source_ranks':{j:4*sum(j in D[d]for d in DS)for j in donors},'new_complete_kappa':False,'complete_receiver_endpoints':False})
 (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
