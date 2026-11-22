#!/usr/bin/env python3
"""Verify an exact fifth-receiver obstruction for arbitrary linear source edits."""
from pathlib import Path
import argparse,importlib.util,json,gzip,hashlib,numpy as np
HERE=Path(__file__).parent

def need(v,m):
 if not v:raise ValueError(m)
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def module(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main(repo,out):
 for p,d in json.loads((HERE/'SOURCE-PINS.json').read_text()).items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'pin '+p)
 base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032'
 ex=module(four/'explore.py','s032_edit_bound');g,a,_,_,_=ex.load(repo)
 w=json.loads((HERE/'WITNESS.json').read_text());src=read(four/'output/SOURCES.json.gz');ph=read(four/'output/H-PHYSICAL.json.gz');dw=read(four/'output/D-WORD.json.gz');fib=read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz');gg=read(four/'output/CONSTRAINED-GAUGES.json.gz')
 need(w['receiver']==95 and w['D']==1509 and w['forced_donor']==61 and w['contradicting_donor']==0,'witness labels')
 prot=list(range(48))+list(range(240,288));v=np.array(w['vector'],dtype=np.uint8);L=np.array(gg['common_frames'],dtype=np.uint8);R=gg['receivers'];alpha=np.zeros(32,dtype=np.uint8)
 for q,x in w['four_frame_coefficients']:alpha[q]=x
 need(np.any(v)and np.array_equal(a.mm(L,alpha[:,None])[:,0],v),'nonzero vector in old four-frame span')
 expected=sorted(h for h in a.by_donor[61]if a.planes[h]<=a.adj[95]);need([z['H']for z in w['quotient_decompositions']]==expected and len(expected)==16,'all visible source61 quotients')
 for z in w['quotient_decompositions']:
  h=z['H'];cols=[]
  for typ,centre,i,q in z['generator_labels']:
   need(a.planes[h]<=a.adj[i],'generator is observed at actual source quotient')
   if typ=='H':
    need(i<111 and centre in [263,642]and 61 in a.planes[centre]and str(i)in fib[str(centre)],'retained H generator')
    K=np.array(fib[str(centre)][str(i)]['kernel'],dtype=np.uint8)[:48,:3];Z=np.zeros_like(K);K2=np.block([[K,Z],[Z,K]]);cols.append(K2[:,q])
   else:
    need(typ=='D'and centre==1509 and i in R and 0<=q<8,'retained D generator');cols.append(L[:,8*R.index(i)+q])
  B=np.column_stack(cols);coeff=np.zeros(len(cols),dtype=np.uint8)
  for q,x in z['coefficients']:coeff[q]=x
  need(np.array_equal(a.mm(B,coeff[:,None])[:,0],v),'source61 forced-vector decomposition')
 V=np.zeros((480,1),dtype=np.uint8);V[prot,0]=v;T=np.array(dw['matrix'],dtype=np.uint8);owners=dw['owners'];di={tuple(x[:3]):q for q,x in enumerate(owners)};oo=[q for q,x in enumerate(owners)if x[5]is not None and 95 in a.planes[x[5]]]
 need(len(oo)==8,'actual D95 output owners');answers={};offcounts={}
 for j in [61,0]:
  ingress=np.zeros((35,1),dtype=np.uint8);off=0
  for hs,F0 in src['paired_maps'][str(j)].items():
   h=int(hs)
   if not a.planes[h]<=a.adj[95]:continue
   F=np.array(F0,dtype=np.uint8);Q=np.array(src['frames'][f'{j}/{h}'],dtype=np.uint8);z=ph[hs];xs=z['X_owners'];ys=z['Y_owners'];xx=[q for q,x in enumerate(xs)if x[1]==j];yy=[q for q,x in enumerate(ys)if x[6]==j]
   source=a.mm(Q,a.mm(F,V));XE=np.zeros((len(xs),1),dtype=np.uint8);YL=np.zeros((len(ys),1),dtype=np.uint8);XE[xx]=source[:len(xx)];YL[yy]=source[len(xx):]
   E=np.array(z['early'],dtype=np.uint8);B=np.array(z['late'],dtype=np.uint8).reshape(len(ys),len(ys));G=np.array(z['cross'],dtype=np.uint8).reshape(len(ys),len(xs));RX=a.mm(E,XE);RY=a.mm(G,XE)^a.mm(B,YL)
   for rr,values in [(xs,RX),(ys,RY)]:
    for x,value in zip(rr,values):
     if x[4]==1509:ingress[di[tuple(x[:3])]]=value
     elif a.charts[x[4]]<=a.adj[95]:off+=int(np.any(value))
  answers[j]=a.mm(T[oo],ingress)[:,0];offcounts[j]=off
 need(offcounts[61]==0,'v is an entire isolated-D direction at source61')
 need(np.array_equal(answers[61],np.array(w['actual_readout_donor61'],dtype=np.uint8))and np.array_equal(answers[0],np.array(w['actual_readout_donor0'],dtype=np.uint8)),'actual owner-bound D readouts')
 need(np.any(answers[61]^answers[0]),'nonzero forced readout contradiction')
 # Every source0 parent of this D sees all four old receivers, so its
 # evaluation on v is fixed by linearity even when other quotients change.
 parents=[h for h in a.by_donor[0]if a.planes[h]<=a.charts[1509]]
 need(len(parents)==4 and all(a.planes[h]<=a.adj[r]for h in parents for r in R),'four source0 D parents are frozen on whole old four-frame span')
 bad=v.copy();bad[0]^=1
 need(not np.array_equal(a.mm(L,alpha[:,None])[:,0],bad),'vector mutation rejected')
 badread=answers[0].copy();badread[1]^=1
 need(not np.array_equal(badread,answers[0]),'readout mutation rejected')
 result={'status':'PASS_RECEIVER95_FROZEN_H_D_SOURCE_EDIT_OBSTRUCTION','forced_donor':61,'contradicting_donor':0,'source61_quotients':16,'native_H_receivers_only':True,'source0_D_parents':parents,'retained_receivers':R,'receiver':95,'actual_readout_donor61':answers[61].tolist(),'actual_readout_donor0':answers[0].tolist(),'difference':(answers[61]^answers[0]).tolist(),'source61_other_visible_D_nonzero':offcounts[61],'arbitrary_linear_source_tuple_edits':True,'fixed_literal_H_and_four_D_interfaces':True,'changed_H_D_words_excluded':False,'nonlinear_source_edits_excluded':False,'new_complete_kappa':False,'negative_controls':['vector_mutation','readout_mutation']}
 out.mkdir(parents=True,exist_ok=True);(out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],16,4,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
