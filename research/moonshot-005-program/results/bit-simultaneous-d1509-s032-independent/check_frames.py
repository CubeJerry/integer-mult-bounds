#!/usr/bin/env python3
"""Independent S032 physical reconstruction; only generic S031 review algebra reused."""
import argparse, gzip, hashlib, itertools, json, runpy
from collections import defaultdict
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=ROOT/'research/moonshot-005-program/results'
ALG=runpy.run_path(str(BASE/'bit-shared-h-s031-construction/native-d1509-all-native/review-c/check.py'))
mm,rank,inverse,image_echelon=ALG['mm'],ALG['rank'],ALG['inverse'],ALG['echelon']
def need(x,msg):
 if not x:raise AssertionError(msg)
def rd(p):
 raw=p.read_bytes()
 return json.loads(gzip.decompress(raw) if p.suffix=='.gz' else raw)
def wr(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);raw=(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n').encode()
 p.write_bytes(gzip.compress(raw,mtime=0) if p.suffix=='.gz' else raw)
def basis(A):return A[:,image_echelon(A)[1]]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--compare',type=Path);args=ap.parse_args()
 old=BASE/'bit-shared-h-s031-construction/native-d1509-all-native/output'
 pins=[old/n for n in ['SOURCES.json.gz','H-PHYSICAL.json.gz','D-WORD.json.gz']]
 pins += [BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',BASE/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz',BASE/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',BASE/'bit-shared-h-s031-construction/native-d1509-all-native/review-c/check.py']
 source,hp,dw,layout,allocation=[rd(p) for p in pins[:5]]
 roots=np.array(layout['root_table'],dtype=np.int64);dots=roots@roots.T
 need(roots.shape==(120,8) and np.all(np.diag(dots)==4),'literal root norms')
 adj=[set(np.flatnonzero(r==0).tolist()) for r in dots];need(all(len(a)==63 for a in adj),'Euclidean orthogonality')
 planes=[set(a) for a in layout['A2']];charts=[set(a) for a in layout['D4']]
 marked=set(allocation['selected_D'])
 routes=[json.loads(l) for l in gzip.decompress(pins[5].read_bytes()).splitlines()]
 X,Y,Xj,Yj=[defaultdict(list) for _ in range(4)]
 for r in routes:
  if r[3] is None:continue
  (X if r[0]=='X' else Y)[r[3]].append(r)
  if r[0]=='X':Xj[r[1],r[3]].append(r)
  elif r[6] is not None:Yj[r[6],r[3]].append(r)
 for table in [X,Y,Xj,Yj]:
  for k in table:table[k].sort(key=lambda r:(r[1],r[2]))
 paired={int(j):{int(h):np.array(a,dtype=np.uint8) for h,a in row.items()} for j,row in source['paired_maps'].items()}
 donors=sorted(paired);recvs=[i for i in range(120) if charts[1509]<=adj[i]]
 need(donors==sorted(j for j in charts[1509] if j<111) and len(recvs)==12,'all donors/receivers')
 prot=list(range(48))+list(range(240,288));local=[0,1,2,15,16,17];trans={}
 for j in donors:
  for h,f in paired[j].items():
   p=hp[str(h)];ne,nl=len(X[h]),len(Y[h]);need(p['X_owners']==X[h] and p['Y_owners']==Y[h],'actual H owners')
   E=np.array(p['early'],dtype=np.uint8).reshape(ne,ne);B=np.array(p['late'],dtype=np.uint8).reshape(nl,nl);G=np.array(p['cross'],dtype=np.uint8).reshape(nl,ne)
   q=np.array(source['frames'][f'{j}/{h}'],dtype=np.uint8);xe=np.zeros((ne,30),dtype=np.uint8);yl=np.zeros((nl,30),dtype=np.uint8)
   xi={(r[1],r[2]):t for t,r in enumerate(X[h])};yi={(r[1],r[2]):t for t,r in enumerate(Y[h])}
   for t,r in enumerate(Xj[j,h]):xe[xi[r[1],r[2]]]=q[t]
   for t,r in enumerate(Yj[j,h]):yl[yi[r[1],r[2]]]=q[len(Xj[j,h])+t]
   trans[j,h]=(mm(mm(E,xe),f[:,prot]),mm(mm(G,xe)^mm(B,yl),f[:,prot]))
 owners=sorted([r for r in routes if r[4]==1509 and r[0]=='X'],key=lambda r:(r[1],r[2]))+sorted([r for r in routes if r[4]==1509 and r[0]=='Y'],key=lambda r:(r[1],r[2]))
 need(owners==dw['owners'] and len(owners)==35,'D owners');D=np.array(dw['matrix'],dtype=np.uint8)
 frames,proper,sections={},{},{}
 for j in donors:
  frames[j],proper[j],sections[j]={},{},{}
  inputs=[t for t,r in enumerate(owners) if r[3] is not None and j in planes[r[3]]];need(len(inputs)==8,'D inputs')
  for rcv in recvs:
   rows,labels=[],[]
   for h in sorted(paired[j]):
    if not planes[h]<=adj[rcv]:continue
    for phase,hs,val in [('X',X[h],trans[j,h][0]),('Y',Y[h],trans[j,h][1])]:
     for t,r in enumerate(hs):
      if r[4] in marked and charts[r[4]]<=adj[rcv]:rows.append(val[t]);labels.append([phase,r[1],r[2]])
   A=np.array(rows,dtype=np.uint8);need(A.shape==(96,96),'entire protected left')
   outputs=[t for t,r in enumerate(owners) if r[5] is not None and rcv in planes[r[5]]];need(len(outputs)==8,'D outputs')
   C=D[np.ix_(outputs,inputs)];ci=inverse(C);rhs=np.zeros((96,8),dtype=np.uint8)
   for t,k in enumerate(inputs):
    r=owners[k];lab=[r[0],r[1],r[2]];need(labels.count(lab)==1,'unique owner')
    rhs[labels.index(lab)]=ci[t]
   U=mm(inverse(A),rhs);need(rank(U)==8 and np.array_equal(mm(A,U),rhs),'entire inverse fibre')
   frames[j][rcv]=U;proper[j][rcv]={'labels':labels,'matrix':A.tolist(),'target':rhs.tolist()};sections[j][rcv]={'D_inputs':inputs,'D_outputs':outputs,'section':C.tolist()}
  print('INDEPENDENT_FRAMES',j,len(recvs),flush=True)
 cores,hf,anchor={},{},[]
 for j in donors:
  pieces=[];hf[j]={}
  for centre in [263,642]:
   if j not in planes[centre]:continue
   vals=[]
   for rcv in range(120):
    if not planes[centre]<=adj[rcv]:continue
    hs=[h for h in sorted(paired[j]) if planes[h]<=adj[rcv]];need(len(hs)==16 and centre in hs,'complete H source view')
    for h in hs:
     f=paired[j][h]
     need(not np.any(f[np.ix_(local,[i for i in range(480) if i not in prot])]),'no complementary input')
     need(not np.any(f[np.ix_([i for i in range(30) if i not in local],prot)]),'protected direct summand')
    A=np.vstack([paired[j][h][np.ix_(local,prot)] for h in hs]);rhs=np.zeros((96,6),dtype=np.uint8);rhs[6*hs.index(centre):6*hs.index(centre)+6]=np.eye(6,dtype=np.uint8)
    U=mm(inverse(A),rhs);need(rank(U)==6,'whole protected H fibre');vals.append(U);hf[j][f'{centre}/{rcv}']=U.tolist()
   W=basis(np.hstack(vals));pieces.append(W);anchor.append({'donor':j,'H':centre,'receiver_fibres':len(vals),'protected_paired_span':W.shape[1]})
  W=basis(np.hstack(pieces)) if pieces else np.zeros((96,0),dtype=np.uint8)
  C=basis(np.hstack([W,frames[j][6]]));cores[j]={'H':W,'H_and_receiver6':C}
 checks=[]
 if args.compare:
  for name,mine in [('FRAMES.json.gz',{str(j):{str(r):a.tolist() for r,a in row.items()} for j,row in frames.items()}),('PROPER.json.gz',{str(j):{str(r):a for r,a in row.items()} for j,row in proper.items()}),('READOUTS.json.gz',{str(j):{str(r):a for r,a in row.items()} for j,row in sections.items()})]:
   actual=rd(args.compare/name)
   if name=='PROPER.json.gz':
    def canonical(row):return sorted((tuple(lab),a,b) for lab,a,b in zip(row['labels'],row['matrix'],row['target']))
    need(set(actual)==set(mine) and all(set(actual[j])==set(mine[j]) and all(canonical(actual[j][r])==canonical(mine[j][r]) for r in mine[j]) for j in mine),'independent labelled proper row agreement')
   else:need(actual==mine,'independent author agreement '+name)
   checks.append(name)
 wr(args.out/'FRAMES.json.gz',{j:{r:a.tolist() for r,a in row.items()} for j,row in frames.items()});wr(args.out/'H-FIBRES.json.gz',hf);wr(args.out/'CORES.json.gz',{j:{k:a.tolist() for k,a in row.items()} for j,row in cores.items()})
 result={'status':'PASS_INDEPENDENT_D1509_FRAMES_AND_H_CORES','donors':donors,'receivers':recvs,'entire_D_frame_dimension':8,'source_protected_dimension':96,'anchor_fibres':anchor,'constraint_dimensions':{j:{k:a.shape[1] for k,a in row.items()} for j,row in cores.items()},'author_output_agreement':checks,'new_author_executable_imports':False,'reused_generic_field_algebra':str(pins[-1].relative_to(ROOT)),'whole_global_word':False,'new_kappa':False}
 wr(args.out/'RESULT.json',result);wr(args.out/'SOURCE-PINS.json',{'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in pins}})
 print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':main()

