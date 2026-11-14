#!/usr/bin/env python3
"""Actual canonical core prefix and static code certificate; no decoder claim."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PIN="51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78"
def need(ok,s):
 if not ok:raise ValueError(s)

def basis(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return list(b.values())

def combine(m,rows):
 s=0
 while m:
  z=m&-m;s^=rows[z.bit_length()-1];m^=z
 return s

def solve(rows,rhs,n):
 rr=[x|(int(y)<<n) for x,y in zip(rows,rhs)];piv=[]
 for col in range(n):
  k=next((j for j in range(len(piv),len(rr)) if rr[j]>>col&1),None)
  if k is None:continue
  at=len(piv);rr[at],rr[k]=rr[k],rr[at]
  for j in range(len(rr)):
   if j!=at and rr[j]>>col&1:rr[j]^=rr[at]
  piv.append(col)
 if any((x&((1<<n)-1))==0 and x>>n for x in rr):return None
 part=sum((rr[j]>>n&1)<<p for j,p in enumerate(piv));ker=[]
 for f in range(n):
  if f not in piv:ker.append((1<<f)|sum((rr[j]>>f&1)<<p for j,p in enumerate(piv)))
 return part,ker

def source(native):
 roots=[list(map(F,native['frames'][str(native['start'][i])]['B'][0])) for i in range(111)]
 K=[sum(int(i==j or sum(a*b for a,b in zip(x,y))==0)<<j for j,y in enumerate(roots)) for i,x in enumerate(roots)]
 G=[];chosen=[]
 for i,row in enumerate(K):
  if len(basis(G+[row]))>len(G):G.append(row);chosen.append(i)
 need(len(G)==9,'canonical rank9')
 equations=[sum((g>>j&1)<<a for a,g in enumerate(G)) for j in range(111)]
 coeff=[]
 for row in K:
  sol=solve(equations,[row>>j&1 for j in range(111)],9)
  need(sol is not None and not sol[1],'unique canonical basis coefficients');coeff.append(sol[0])
 R=[combine(c&7,G[:3]) for c in coeff]
 need(len(basis(R))==3 and all(r^combine(c>>3,G[3:])==k for r,c,k in zip(R,coeff,K)),
      'three-plus-six exact static decomposition')
 groups={}
 for i,r in enumerate(roots):
  support=tuple(j for j,x in enumerate(r) if x);sgn=1 if r[support[0]]>0 else-1
  groups.setdefault((support,sum(x*sgn<0 for x in r)%2),[]).append(i)
 groups=list(groups.values());D=[sum(1<<j for j in group) for group in groups]
 zero=solve(equations[:8],[0]*8,9)[1]
 need(len(zero)==5,'zero-coordinate canonical kernel dimension5')
 for v in zero:
  row=combine(v,G)
  need(all(len({row>>j&1 for j in group})==1 for group in groups),
       'zero-coordinate canonical rows are group-constant')
 need(len(basis(K+D))==39,'canonical/halfclass intersection dimension6')
 return roots,K,G,chosen,coeff,R,groups,zero

def emit(native,G,coeff):
 hub=native['final'][0];ground=native['start'][111]
 ops=[]
 for i in range(111):
  line=native['start'][i]
  ops += [['INIT',222+i,line],['ADD',222+i,i,line],['MOVE',i,line,hub]]
 for a,row in enumerate(G[:3]):
  packet=333+a;cache=336+a
  ops.append(['INIT',packet,hub])
  for j in range(111):
   if row>>j&1:ops.append(['ADD',packet,j,hub])
  ops += [['MOVE',packet,hub,ground],['INIT',cache,ground],['ADD',cache,packet,ground]]
  for i,c in enumerate(coeff):
   if c>>a&1:ops.append(['ADD',111+i,packet,ground])
  ops.append(['CLEAR',packet,ground])
 prefix={'schema':'native_nested_linear_partial_word','public':222,'hub':hub,
         'start':native['start'][:222],'final':[hub]*111+[ground]*111,
         'frames':native['frames'],'owned_fields':list(range(222,339)),
         'program':ops[:],'end_owned':list(range(222,333))+list(range(336,339)),
         'scope':'111 actual line copies, three canonical ground modes, projected canonical Y preloads; no complete decoder.'}
 for i in range(111):ops.append(['MOVE',111+i,ground,native['final'][111+i]])
 for i in range(111):ops.append(['CLEAR',222+i,native['start'][i]])
 for a in range(3):ops.append(['CLEAR',336+a,ground])
 closed={**prefix,'program':ops,'final':native['final'][:222],'end_owned':[],
         'scope':'Closed partial canonical preconditioner only; Y_i=y_i+R_i x, not the completed translation.'}
 return prefix,closed

def replay(word,native,R,G,closed):
 frames=word['frames'];loc=dict(enumerate(word['start']));rows={i:1<<i for i in range(222)}
 born=set(loc);counts=Counter();profile=Counter();peak=0;clears=[]
 for event,op in enumerate(word['program']):
  t,i=op[:2];counts[t]+=1
  if t=='INIT':
   need(i>=222 and i not in born,'actual fresh zero INIT');born.add(i);loc[i]=op[2];rows[i]=0
   peak=max(peak,len(loc)-222)
  elif t=='ADD':
   _,i,j,c=op;need(i!=j and loc.get(i)==loc.get(j)==c,'actual cochart ADD');rows[i]^=rows[j]
  elif t=='MOVE':
   _,i,u,v=op;need(loc.get(i)==u,'actual MOVE source')
   fu,fv=frames[str(u)],frames[str(v)];d=fv['dim']-fu['dim'];need(d!=0,'positive rank MOVE')
   low,high=(fu,fv) if d>0 else(fv,fu)
   need(all(sum(F(a)*F(b) for a,b in zip(row,normal))==0 for row in low['B'] for normal in high['A']),
        'actual native nested charts')
   if i<222:need(d>0,'public paths monotone')
   loc[i]=v;profile[abs(d)]+=1
  elif t=='CLEAR':
   need(i>=222 and loc.get(i)==op[2],'actual paid owned CLEAR')
   clears.append({'event':event,'record':i,'chart':op[2],'value_hex':hex(rows[i])})
   del rows[i];del loc[i]
  else:raise ValueError(t)
 for i in range(111):
  need(rows[i]==1<<i and loc[i]==native['final'][i],'original X restored at Hub')
  need(rows[111+i]==(1<<(111+i))^R[i],'exact arbitrary-Y preconditioner')
  need(loc[111+i]==(native['final'][111+i] if closed else native['start'][111+i]),'actual Y endpoint')
 if closed:need(len(loc)==222,'all owned records closed')
 else:
  need(len(loc)==336,'114 retained records')
  for i in range(111):need(rows[222+i]==1<<i and loc[222+i]==native['start'][i],'actual stationary point copy')
  for a in range(3):need(rows[336+a]==G[a] and loc[336+a]==native['start'][111],'actual canonical ground cache')
 need(any(rows[111+i]!=(1<<(111+i))^(1<<i) for i in range(111)),'partial word must not be advertised as full source')
 return {'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
         'owned_peak':peak,'owned_live':len(loc)-222,'clear_rows':clears},loc,rows

def cut_census(K,E):
 allmask=(1<<111)-1;adj=[allmask^k for k in K];closed=[x|(1<<i) for i,x in enumerate(adj)]
 best=-1;witness=None;hist=Counter();frames=Counter();cliques=Counter()
 def visit(S,sm,cand,U):
  nonlocal best,witness
  k=len(S)
  if k:cliques[k]+=1
  if k>=6:
   noise=U&~sm;ru=len(basis([e&U for e in E]));rn=len(basis([e&noise for e in E]));delta=k+rn-ru
   hist[delta]+=1
   if k==8:frames[ru]+=1
   if delta>best:
    best=delta;witness={'receivers':S,'unknown':[i for i in range(111) if U>>i&1],
                       'nuisance':[i for i in range(111) if noise>>i&1],
                       'core_unknown_rank':ru,'core_nuisance_rank':rn,'deficit':delta}
  while cand:
   bit=cand&-cand;cand^=bit;i=bit.bit_length()-1
   visit(S+[i],sm|bit,cand&adj[i],U&closed[i])
 visit([],0,allmask,allmask)
 need(sum(cliques.values())==485330 and cliques[8]==4373 and best==6,'complete actual clique census')
 need(frames=={3:4373},'all eight-frame core restrictions full rank3')
 return {'maximum_deficit':best,'witness':witness,'cliques_by_size':dict(sorted(cliques.items())),
         'deficits_for_cliques_size_at_least6':dict(sorted(hist.items())),
         'eight_frame_core_ranks':dict(frames),'scope':'Exact fixed native source; full conditional cuts, not a decoder.'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True)
 p.add_argument('--outdir',type=Path,required=True);a=p.parse_args();a.outdir.mkdir(parents=True,exist_ok=True)
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin')
 native=json.loads(gzip.decompress(raw));roots,K,G,chosen,coeff,R,groups,zero=source(native)
 prefix,closed=emit(native,G,coeff)
 rp,loc,rows=replay(prefix,native,R,G,False);rc,_,_=replay(closed,native,R,G,True)
 need(rp['movement_profile']=={7:111,8:3} and rc['movement_profile']=={7:222,8:3},'exact complete movement profiles')
 need(rp['owned_peak']==115 and rp['owned_live']==114,'actual ownership invoice')
 census=cut_census(K,G[:3]);S=census['witness']['receivers']
 inside=lambda chart:any(all(sum(F(x)*y for x,y in zip(row,roots[i]))==0 for row in native['frames'][str(chart)]['B']) for i in S)
 O=[rows[i] for i,c in loc.items() if inside(c)];T=[(1<<i)^(1<<(111+i)) for i in S]
 r0=len(basis(O));r1=len(basis(O+T));need((r0,r1)==(216,222),'literal full222-column six-demand witness')
 census['literal_witness_observation_rank']=r0;census['literal_witness_augmented_rank']=r1
 controls=[]
 selected=[('omit actual point-copy ADD',lambda o:o[:3]==['ADD',222,0]),
           ('omit actual Hub seed ADD',lambda o:o[0]=='ADD' and o[1]==333),
           ('omit Hub-to-ground MOVE',lambda o:o[0]=='MOVE' and o[1]==333),
           ('omit pure-core cache ADD',lambda o:o[:3]==['ADD',336,333]),
           ('omit projected Y preload',lambda o:o[0]=='ADD' and 111<=o[1]<222)]
 for name,predicate in selected:
  at=next(i for i,o in enumerate(prefix['program']) if predicate(o));mutant={**prefix,'program':prefix['program'][:at]+prefix['program'][at+1:]}
  try:replay(mutant,native,R,G,False)
  except (ValueError,KeyError):controls.append(name)
  else:raise ValueError('mutant accepted '+name)
 need(census['maximum_deficit']==6 and census['eight_frame_core_ranks']=={3:4373},'full-frame screen alone is insufficient')
 code={'native_sha256':PIN,'canonical_basis_indices':chosen,
       'canonical_basis_hex':[hex(g) for g in G],'core_basis_hex':[hex(g) for g in G[:3]],
       'six_complementary_modes_hex':[hex(g) for g in G[3:]],
       'receiver_coefficients_9':coeff,'receiver_core_coefficients':[c&7 for c in coeff],
       'receiver_preload_rows_hex':[hex(r) for r in R],
       'canonical_rows_hex':[hex(k) for k in K],
       'halfclass_groups':groups,'zero_coordinate_canonical_kernel_coefficients':zero,
       'zero_coordinate_kernel_rows_hex':[hex(combine(v,G)) for v in zero],
       'dimensions':{'canonical':9,'core':3,'complement':6,'halfclass_indicator':36,
                     'canonical_plus_halfclass':39,'zero_coordinate_canonical_kernel':5},
       'qualification':'Six-mode completion is an algebraic side-information code, not six physically delivered packets.'}
 pins={}
 for name,word in [('PREFIX.json.gz',prefix),('CLOSED-PARTIAL.json.gz',closed)]:
  payload=json.dumps(word,sort_keys=True,separators=(',',':')).encode()
  data=gzip.compress(payload,mtime=0);(a.outdir/name).write_bytes(data)
  pins[name]={'gzip_sha256':hashlib.sha256(data).hexdigest(),'canonical_json_sha256':hashlib.sha256(payload).hexdigest()}
 result={'status':'PASS_ACTUAL_CANONICAL_CORE_PREFIX_AND_STATIC_COMPLETION',
         'native_sha256':PIN,'canonical_basis_indices':chosen,'prefix':rp,'closed_partial':rc,
         'negative_controls':controls+['eight-frame full rank does not prove five future modes suffice',
                                        'closed partial word is not the desired multiplication source'],
         'cut_census':census,'word_pins':pins,'complete_source':False,'new_kappa':None,
         'scope':'Actual fixed-source prefix and universal static-code/cut lemmas; physical joint decoder remains unresolved.'}
 for name,data in [('CODE.json',code),('CUT-CENSUS.json',census),('RESULT.json',result)]:
  (a.outdir/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':result['status'],'basis_indices':chosen,
                   'prefix_counts':rp['counts'],'closed_counts':rc['counts'],
                   'cut_maximum':census['maximum_deficit']}))

if __name__=='__main__':main()

