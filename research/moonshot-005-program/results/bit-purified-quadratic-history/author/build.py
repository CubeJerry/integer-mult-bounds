#!/usr/bin/env python3
"""One actual rank-one canonical purification and an all-union seven-cut certificate."""
import argparse,gzip,hashlib,json,itertools
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
RIGIDITY_PIN='86ce82a4a716419d366a69ec2d1a28baeb1e4eab50b9fc2d562988cb4971b417'
PARITY_PIN='977eedcdd197d36967f646385fe07f32bae06b37a08f06dd986d8fbccccba001'
PIVOT_PIN='763ef1dafa697d814d28807f247cd5382540e3a8109bff346a897f2b7ef99fd4'
def need(b,m):
 if not b:raise ValueError(m)
def dot(a,b):return sum(F(x)*F(y) for x,y in zip(a,b))
def rank(rows):
 p={}
 for r in rows:
  while r:
   b=r.bit_length()-1
   if b in p:r^=p[b]
   else:p[b]=r;break
 return len(p)
def replay(w,n,closed):
 loc=dict(enumerate(w['start']));rows={k:1<<k for k in range(222)};born=set(loc);counts=Counter();profile=Counter();peak=0;clears=[]
 for op in w['program']:
  tag,k=op[:2];counts[tag]+=1
  if tag=='INIT':need(k>=222 and k not in born,'fresh lifetime');born.add(k);loc[k]=op[2];rows[k]=0;peak=max(peak,len(loc)-222)
  elif tag=='ADD':
   _,k,l,C=op;need(k!=l and loc.get(k)==loc.get(l)==C,'actual same-chart ADD');rows[k]^=rows[l]
  elif tag=='MOVE':
   _,k,a,b=op;need(loc.get(k)==a,'actual MOVE source');fa,fb=w['frames'][str(a)],w['frames'][str(b)];d=fb['dim']-fa['dim'];need(d!=0,'positive actual movement');small,large=(fa,fb) if d>0 else(fb,fa);need(all(dot(x,y)==0 for x in small['B'] for y in large['A']),'exact real nesting');need((d>0) if k<222 else(k in(334,335) and d<0),'monotone physical paths');loc[k]=b;profile[abs(d)]+=1
  elif tag=='CLEAR':need(k>=222 and loc.get(k)==op[2],'actual owned CLEAR');clears.append({'record':k,'chart':op[2],'value_hex':hex(rows[k])});del loc[k];del rows[k]
  else:raise ValueError(tag)
 for k in range(111):
  need(rows[k]==1<<k and loc[k]==n['final'][k],'all111 original X restored')
  need(rows[111+k]==((1<<(111+k))^((1<<k) if k==92 else 0)),'full222-column public map')
  need(loc[111+k]==(n['final'][111+k] if closed or k==92 else n['start'][111+k]),'actual original Y endpoint')
 if closed:need(set(loc)==set(range(222)),'all owners retired')
 else:
  need(set(loc)==set(range(335)),'only helper335 retired')
  for k in range(111):need(rows[222+k]==1<<k and loc[222+k]==n['start'][k],'actual point copy')
  R=[list(map(F,n['frames'][str(n['start'][k])]['B'][0])) for k in range(111)]
  K=[sum(int(k==l or dot(R[k],R[l])==0)<<l for l in range(111)) for k in range(111)]
  need(rows[333]==K[92] and loc[333]==636,'pure canonical row at actual common chart')
  need(rows[334]==(K[92]&K[54]) and loc[334]==n['start'][111],'quadratic row retained at ground')
 return {'counts':dict(counts),'profile':dict(sorted(profile.items())),'rank_length':sum(d*c for d,c in profile.items()),'peak_owned':peak,'live_owned':len(loc)-222,'clears':clears},loc,rows

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--pivot',type=Path,required=True);ap.add_argument('--rank-certificate',type=Path,required=True);ap.add_argument('--rigidity-certificate',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True);a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw));pr=a.pivot.read_bytes();need(hashlib.sha256(pr).hexdigest()==PIVOT_PIN,'literal predecessor pivot pin');p=json.loads(gzip.decompress(pr));need(p['public']==222 and p['end_owned']==list(range(222,335)),'retained pivot interface')
 Fi=n['final'][203];C=636;ground=n['start'][111];helper=[['INIT',335,Fi],['ADD',335,203,Fi],['MOVE',335,Fi,C],['ADD',333,335,C],['CLEAR',335,C]]
 p={**p,'owned_fields':p['owned_fields']+[335],'program':p['program']+helper,'scope':'One original target complete, pure canonical K92 at rank6C and pure quadratic at ground. Partial source.'}
 c={**p,'program':p['program']+[['MOVE',111+k,ground,n['final'][111+k]] for k in range(111) if k!=92]+[['CLEAR',222+k,n['start'][k]] for k in range(111)]+[['CLEAR',333,C],['CLEAR',334,ground]],'final':n['final'][:222],'end_owned':[],'scope':'Closed partial source; onlyY92 updated; all114owned lifetimes retired.'}
 rp,loc,rows=replay(p,n,False);rc,_,_=replay(c,n,True);need(rc['profile']=={1:29,2:32,5:32,6:27,7:164},'exact helper invoice');need(rc['rank_length']==1563,'one extra rank unit')
 R=[list(map(F,n['frames'][str(n['start'][k])]['B'][0])) for k in range(111)];K=[sum(int(k==l or dot(R[k],R[l])==0)<<l for l in range(111)) for k in range(111)];B=[2,8,14,21,46,48,81,84]
 need(all(dot(R[u],R[v])!=0 for u,v in itertools.combinations(B,2)),'source eight-clique basis')
 labels=[]
 for row in K:
  v=sum(((row>>b)&1)<<j for j,b in enumerate(B));labels.append(v^(255 if v.bit_count()%2==0 else 0))
 def q(v):t=v.bit_count();return t*(t+1)//2%2
 def beta(u,v):return ((u&v).bit_count()+(u.bit_count()%2)*(v.bit_count()%2))%2
 need(len(set(labels))==111 and all(q(v)==1 for v in labels),'injective native nonsingular quadric representation')
 need(all(((K[i]>>j)&1)==1-beta(labels[i],labels[j]) for i in range(111) for j in range(111)),'complete native orthogonality is the quadric polar form')
 need(labels[92]^labels[54]==labels[84],'A2 binary triangle');need(K[92]^K[54]^K[84]==(1<<111)-1,'actual A2 canonical partition identity')
 need(all(dot(v,R[k])==0 for v in p['frames'][str(C)]['B'] for k in(92,54,84)),'actual common chart belongs to all three A2 facets')
 possible=[r for r in range(9) if ((r if r%2 else 8-r)*((r if r%2 else 8-r)+1)//2)%2==1];need(possible==[1,2,5,6],'universal eight-clique weight identity')
 need(not any(x+y+z==8 for x in(2,5,6) for y in(2,5,6) for z in(2,5,6)),'three outside-root supports cannot partition8')
 cuts=[]
 for S in(B,[2,8,9,14,15,60,93]):
  def inside(A):return any(all(dot(v,R[t])==0 for v in p['frames'][str(A)]['B']) for t in S)
  O=[rows[k] for k,A in loc.items() if inside(A)];T=[(1<<t)^(1<<(111+t)) for t in S];r0=rank(O);r1=rank(O+T);cuts.append({'receivers':S,'observation_rank':r0,'target_augmented_rank':r1,'deficit':r1-r0,'canonical_cache_inside':inside(C),'canonical_own_support':[t for t in S if K[92]>>t&1],'quadratic_own_support':[t for t in S if (K[92]&K[54])>>t&1]})
 need(cuts[0]['deficit']==7 and cuts[1]['deficit']==7,'two exact seven-deficit cuts')
 cert_raw=a.rank_certificate.read_bytes();need(hashlib.sha256(cert_raw).hexdigest()==PARITY_PIN,'rank-nine parity certificate pin');cert=json.loads(cert_raw);frames=cert['frames_pairwise_REAL_NONorthogonal'];need(len(frames)==9 and all(len(set(T))==8 for T in frames),'nine8frames');used=Counter(t for T in frames for t in T);need(all(c%2==0 for c in used.values()),'even incidence');need(all(dot(R[u],R[v])!=0 for T in frames for u,v in itertools.combinations(T,2)),'actual nonorthogonal parity witness');W=sorted(used);need(len(W)==26 and set(W).isdisjoint({92,54,84}),'unaffected26role source');need(all(not all(dot(v,R[t])==0 for v in p['frames'][str(C)]['B']) for t in W),'proper canonical cache cannot reach any parity receiver');need(any((K[92]&K[54])>>t&1 for t in W),'nonzero restricted quadratic mode')
 rig_raw=a.rigidity_certificate.read_bytes();need(hashlib.sha256(rig_raw).hexdigest()==RIGIDITY_PIN,'rigidity seed/anchor pin');rig=json.loads(rig_raw);T=[t for t in range(111) if t not in{92,54,84}];factors=rig['canonical_factor_rows_9bit'];need(all(((factors[u]&factors[v]).bit_count()%2)==(K[u]>>v&1) for u in range(111) for v in range(111)),'all canonical factor products');F0=rig['identity_frame_roles'];need(all(factors[t]==1<<a for a,t in enumerate(F0)),'canonical point frame');seed=set(rig['seed_roles']);need(seed.issubset(T),'all35star seed roles survive');edges=rig['sparse_edge_roles'];pairs={tuple(e['endpoints']) for e in edges};need(pairs==set(itertools.combinations(range(8),2))-{(0,4)},'actual saturated high-degree star');need(all(factors[e['role']]==((1<<e['endpoints'][0])^(1<<e['endpoints'][1])^256) for e in edges),'actual sparse edge factors');checked=0
 for anchor in rig['extension_anchors']:
  t=anchor['role']
  if t not in T:continue
  A=anchor['eight_noncontact_seed_roles'];need(set(A).issubset(seed) and len(A)==8 and rank([factors[k] for k in A])==8,'unchanged eight-anchor rank');need(all(not(K[t]>>k&1) for k in A),'actual noncontact anchors');checked+=1
 need(checked==73,'all73remaining punctured roles anchored');need(all(not all(dot(v,R[t])==0 for v in p['frames'][str(C)]['B']) for t in T),'proper cache reaches no punctured receiver')
 CB=[];CB_roles=[]
 for t in T:
  rr=sum((K[t]>>u&1)<<j for j,u in enumerate(T))
  if rank(CB+[rr])>len(CB):CB.append(rr);CB_roles.append(t)
 need(len(CB)==9,'punctured canonical dimension9');spectrum=Counter();witness=None
 for mask in range(1,512):
  v=0
  for bit_index,row in enumerate(CB):
   if mask>>bit_index&1:v^=row
  wt=v.bit_count();spectrum[wt]+=1
  if witness is None or wt<witness['weight']:witness={'weight':wt,'basis_mask':mask,'word_hex':hex(v)}
 ell=sum(((K[92]&K[54])>>u&1)<<j for j,u in enumerate(T));need(witness['weight']==46 and ell.bit_count()==32,'strict sparse retained mode gap32<46');need(rank(CB+[ell])==10,'retained mode outside actual canonical code')
 controls=[]
 for omitted in range(5):
  m={**p,'program':p['program'][:len(p['program'])-5]+[o for z,o in enumerate(helper) if z!=omitted]}
  try:replay(m,n,False)
  except(KeyError,ValueError):controls.append('delete helper '+str(omitted))
  else:raise ValueError('accepted helper deletion')
 a.outdir.mkdir(parents=True,exist_ok=True);pins={}
 for name,w in [('PREFIX.json.gz',p),('CLOSED-PARTIAL.json.gz',c)]:
  payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();raw=gzip.compress(payload,mtime=0);(a.outdir/name).write_bytes(raw);pins[name]={'gzip_sha256':hashlib.sha256(raw).hexdigest(),'canonical_json_sha256':hashlib.sha256(payload).hexdigest()}
 out={'status':'PASS_PURIFIED_QUADRATIC_PREFIX_AND_SEVEN_CUT_CERTIFICATE','native_sha256':PIN,'input_pivot_sha256':hashlib.sha256(pr).hexdigest(),'prefix':rp,'closed_partial':rc,'quadric':{'basis_clique':B,'labels':labels,'dimension':8,'polar_formula':'dot(u,v)+parity(u)*parity(v)','quadratic_formula':'weight(v)*(weight(v)+1)/2 mod2','maximum_nonorthogonal_clique':8,'outside_clique_canonical_weights':[2,5,6],'A2_triangle':[92,54,84]},'chronological_rank':{'parity_certificate_sha256':PARITY_PIN,'frames':frames,'receiver_roles':W,'initial_nonlocal_width_bound':1,'minimum_fitting_width':9,'minimum_future_transfer_width':8},'strict_future_capacity':{'rigidity_certificate_sha256':RIGIDITY_PIN,'receiver_roles':T,'surviving_seed_roles':sorted(seed),'surviving_anchor_count':checked,'canonical_basis_roles':CB_roles,'canonical_basis_rows':[hex(v) for v in CB],'canonical_weight_spectrum':dict(sorted(spectrum.items())),'distance_witness':witness,'retained_mode_weight':32,'capacity_strictly_greater_than_V_multiple':8,'whole_V_transfer_events_at_least':9},'cuts':cuts,'all_receiver_union_deficit_upper_bound':7,'attained_cut_deficit':7,'negative_controls':controls,'word_pins':pins,'complete_source':False,'new_kappa':None,'qualification':'Universal all-union upper bound uses written quadric proof; no seven-packet sufficiency or physical continuation.'}
 (a.outdir/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'prefix_counts':rp['counts'],'closed_profile':rc['profile'],'cuts':cuts}))
if __name__=='__main__':main()
