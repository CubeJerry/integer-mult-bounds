#!/usr/bin/env python3
"""Independent rational-geometry and 222-column replay. Imports no author code."""
import argparse,copy,hashlib,json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'

class Reject(Exception):pass

def need(ok,msg):
 if not ok:raise Reject(msg)

def rr(rows,n=8):
 A=[list(map(F,r))for r in rows];i=0
 for j in range(n):
  p=next((p for p in range(i,len(A))if A[p][j]),None)
  if p is None:continue
  A[i],A[p]=A[p],A[i];v=A[i][j];A[i]=[x/v for x in A[i]]
  for p in range(len(A)):
   if p!=i and A[p][j]:
    v=A[p][j];A[p]=[x-v*y for x,y in zip(A[p],A[i])]
  i+=1
  if i==len(A):break
 return tuple(tuple(r)for r in A[:i])

def nullspace(rows):
 A=rr(rows);piv=[next(j for j,x in enumerate(r)if x)for r in A];free=[j for j in range(8)if j not in piv];out=[]
 for j in free:
  v=[F(0)]*8;v[j]=1
  for p,row in zip(piv,A):v[p]=-row[j]
  out.append(v)
 return rr(out)

def contained(U,V):
 for u in U:
  w=list(u)
  for v in V:
   p=next(j for j,x in enumerate(v)if x);q=w[p]
   if q:w=[x-q*y for x,y in zip(w,v)]
  if any(w):return False
 return True

def binary_basis(rows):
 A=[];piv=[]
 for w in rows:
  for j,v in zip(piv,A):
   if w>>j&1:w^=v
  if not w:continue
  j=(w&-w).bit_length()-1
  for k,v in enumerate(A):
   if v>>j&1:A[k]^=w
  pos=sum(k<j for k in piv);piv.insert(pos,j);A.insert(pos,w)
 return A

def binary_inverse(rows):
 n=len(rows);A=[w|(1<<(n+i))for i,w in enumerate(rows)]
 for j in range(n):
  p=next((p for p in range(j,n)if A[p]>>j&1),None);need(p is not None,'original X matrix lost invertibility');A[j],A[p]=A[p],A[j]
  for p in range(n):
   if p!=j and A[p]>>j&1:A[p]^=A[j]
 need(all((v&((1<<n)-1))==1<<j for j,v in enumerate(A)),'inverse reduction')
 return [v>>n for v in A]

def column(rows,j):return sum(((r>>j)&1)<<i for i,r in enumerate(rows))

def replay(word,roots,canonical,kind,require_invoice=True):
 charts={}
 for name,c in word['charts'].items():
  need(c['kind']in['span','ann'],'unknown chart descriptor');need(all(len(r)==8 for r in c['rows']),'chart ambient dimension')
  charts[name]=rr(c['rows'])if c['kind']=='span'else nullspace(c['rows'])
 need(charts['zero']==()and charts['Hub']==rr([[int(i==j)for i in range(8)]for j in range(8)]),'endpoint charts')
 for j,r in enumerate(roots):
  need(charts[f'L{j}']==rr([r]),'wrong native source line');need(charts[f'F{j}']==nullspace([r]),'wrong native target facet')
 @lru_cache(None)
 def sub(a,b):return contained(charts[a],charts[b])
 co=lambda a,b:sub(a,b)and sub(b,a)
 held_ids=[0]if kind=='one'else[0,4];held_charts={0:'S'}if kind=='one'else{0:'S0',4:'S4'};cache_names={0:'A'}if kind=='one'else{0:'A0',4:'A4'};kernels={0:15,4:240}
 for j in held_ids:
  T='T'if kind=='one'else f'T{j}';S=held_charts[j]
  need(len(charts[T])==3 and len(charts[S])==4,'proper cache dimensions');need(sub(T,f'F{j}')and not sub(S,f'F{j}'),'early escape geometry')
 if kind=='two':
  need(charts['C04']==nullspace([roots[0],roots[4]])and len(charts['C04'])==6,'shared facet intersection');need(sub('T0','C04')and sub('T4','C04'),'cache access to shared chart')
 value={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};where={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};owned=set();ever=set(value);ops=Counter();moves=Counter();dirty=0;events={};last_capture={};birth={};retire={};milestones={v:k for k,v in word['milestones'].items()}
 for step,op in enumerate(word['operations'],1):
  t=op[0];ops[t]+=1
  if t=='INIT':
   _,name,chart=op;need(name not in ever and chart in charts,'invalid owner birth');ever.add(name);owned.add(name);value[name]=0;where[name]=chart;birth[name]=step
  elif t=='ADD':
   _,src,dst=op;need(src in value and dst in value and src!=dst,'nonlive or aliased ADD');need(co(where[src],where[dst]),f'noncocharted ADD {src}->{dst}');value[dst]^=value[src]
   if dst in owned:last_capture[dst]=step
  elif t=='MOVE':
   _,name,dest=op;need(name in value and dest in charts,'invalid MOVE');old=where[name]
   need(sub(dest,old)if name in owned else sub(old,dest),f'wrong directional MOVE {name}:{old}->{dest}');r=abs(len(charts[dest])-len(charts[old]));need(r>0,'zero-rank or same-chart MOVE');moves[r]+=1;where[name]=dest
  elif t=='CLEAR':
   _,name=op;need(name in owned and name in value,'clearing non-owner');dirty+=int(value[name]!=0);owned.remove(name);del value[name],where[name];retire[name]=step
  else:raise Reject('unknown opcode')
  if step in milestones:
   label=milestones[step];held=[j for j in range(111)if not co(where[f'X{j}'],'Hub')];H=[value[f'X{j}']for j in range(111)if co(where[f'X{j}'],'Hub')];xr=[value[f'X{j}']for j in range(111)];need(all(x>>111==0 for x in xr),'Y contamination at source milestone');inv=binary_inverse(xr);h_rank=len(binary_basis(H));h_c=len(binary_basis(H+canonical));event={'step':step,'held_originals':held,'hub_rank':h_rank,'canonical_hub_intersection_dimension':h_rank+9-h_c}
   if label!='all_X_restored':
    need(held==held_ids,'claimed early milestone has wrong held originals');need(h_rank==111-len(held_ids)and h_c==h_rank,'canonical space not actually in Hub');restr=[]
    for j in held_ids:
     need(where[f'X{j}']==held_charts[j],'wrong held chart');w=column(inv,j);need(w==kernels[j],'wrong actual inverse column');need(all((r&w).bit_count()%2==0 for r in H+canonical),'held kernel visible to Hub/canonical');cache=cache_names[j];need(cache in owned,'proper cache is not live');need((value[cache]&w).bit_count()%2==1,'proper cache fails kernel acquisition');need(last_capture.get(cache,0)<word['milestones']['early_Hub_canonical_cut'],'cache acquired too late');restr.append([(value[cache]&kernels[k]).bit_count()%2 for k in held_ids])
    need(len(binary_basis([sum(v<<k for k,v in enumerate(row))for row in restr]))==len(held_ids),'joint retained cache injection');event['actual_inverse_columns']=[hex(column(inv,j))for j in held_ids];event['cache_restriction_matrix']=restr
    if kind=='two':
     need(all((value[g]&kernels[j]).bit_count()%2==0 for g in['G0','G4']for j in held_ids),'quartet imports incorrectly carry private kernel')
   if 'delivered' in label:
    for q,j in enumerate(word['canonical_basis_roles']):need(f'P{q}'in owned and co(where[f'P{q}'],'zero')and value[f'P{q}']==canonical[j],'canonical field not physically at ground')
    ground=[value[n]&((1<<111)-1)for n in owned if co(where[n],'zero')];gr=len(binary_basis(ground));need(gr==(9 if kind=='one' else 11),'wrong actual ground information rank');event['ground_information_rank']=gr
    if kind=='two':need(word['actual_ground_information_dimension']==gr,'ground rank understated');need(all(co(where[g],'zero')for g in['G0','G4']),'proper imports missing ground')
   if 'completed' in label:
    for j in held_ids:need(value[f'Y{j}']==((1<<(111+j))^(1<<j))and co(where[f'Y{j}'],f'F{j}'),'native output not actually completed')
    event['actual_completed_outputs']=held_ids
   if label=='all_X_restored':need(all(value[f'X{j}']==1<<j and co(where[f'X{j}'],'Hub')for j in range(111)),'original restoration failed')
   events[label]=event
 need(not owned,'live owner remains at closed word')
 for j in range(111):
  need(value[f'X{j}']==1<<j and co(where[f'X{j}'],'Hub'),'wrong final original X');need(value[f'Y{j}']==((1<<(111+j))^((1<<j)if j in held_ids else 0))and co(where[f'Y{j}'],f'F{j}'),'wrong final original Y')
 expected={'one':({'INIT':11,'ADD':594,'MOVE':292,'CLEAR':11},{1:56,2:3,3:2,4:5,6:53,7:164,8:9},11),'two':({'INIT':16,'ADD':640,'MOVE':331,'CLEAR':16},{1:68,2:26,3:6,4:10,5:20,6:60,7:132,8:9},16)}[kind]
 if require_invoice:need(dict(ops)==expected[0]and dict(moves)==expected[1]and dirty==expected[2],'complete invoice mismatch')
 return {'counts':dict(ops),'movement_profile':dict(sorted(moves.items())),'dirty_retirements':dirty,'events':events,'closed_owners':len(retire),'all_222_columns_checked':True,'completed_targets':held_ids,'uncompleted_targets':111-len(held_ids)}

SCALE=10**55
@lru_cache(None)
def interval(r):
 n=pow(r,199)*pow(SCALE,200);lo=SCALE;hi=r*SCALE
 while lo+1<hi:
  m=(lo+hi)//2
  if pow(m,200)<=n:lo=m
  else:hi=m
 return F(lo,SCALE),F(lo if pow(lo,200)==n else lo+1,SCALE)

def linear_interval(profile):
 lo=hi=F(0)
 for r,c in profile.items():
  a,b=interval(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi

def profile_add(*parts):
 d=Counter()
 for c,p in parts:
  for r,n in p.items():d[r]+=c*n
 return {r:c for r,c in d.items()if c}

def price_check(profile,published):
 N={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10};H={2:1,4:25,6:1,8:410}
 P2=profile_add((36,N),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}));T2=profile_add((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
 cap={127:F(37,6),64:F(74,6),1:F(-74,6)}
 for j in range(1,9):cap[7*j+1]=cap.get(7*j+1,0)+F(74,6);cap[7*j]=cap.get(7*j,0)-F(74,6)
 need(profile_add((1,N),(-1,H),(F(1,36),T2),(F(-1,36),P2))==cap,'retained caller formula mismatch')
 checks={};first=None
 for name,p in [('moment',profile),('limiting_allowance',cap),('limiting_room',profile_add((1,cap),(-1,profile)))]:
  x=linear_interval(p);reported=published[name];need(F(reported['lower_fraction'])<=x[0]<=x[1]<=F(reported['upper_fraction']),'published directed interval fails independent tighter enclosure');checks[name]={'lower_fraction':str(x[0]),'upper_fraction':str(x[1])}
 for m in range(2,202,2):
  delta=profile_add((F(m,2),T2),(F(-m,2),P2),(18*(m-1),N),(-18*(m-1),H),(-18*(m-1),profile));x=linear_interval(delta)
  if first is None and x[0]>0:first=m
  row=next((r for r in published['finite_even_m_checks']if r['m']==m),None)
  if row:
   rep=row['target_minus_paid'];need(F(rep['lower_fraction'])<=x[0]<=x[1]<=F(rep['upper_fraction']),'finite caller invoice mismatch');need(row['strictly_positive']==(x[0]>0),'wrong finite sign')
 need(first==published['first_positive_even_m_in_2_to_200'],'wrong first feasible even m');checks['first_positive_even_m']=first;checks['positive_affine_slope_for_later_even_m']=linear_interval(profile_add((36,cap),(-36,profile)))[0]>0
 return checks

def delete_op(word,pred,last=False):
 w=copy.deepcopy(word);ids=[j for j,o in enumerate(w['operations'])if pred(o)];need(bool(ids),'mutation target missing');q=ids[-1]if last else ids[0];w['operations'].pop(q)
 for k,v in w['milestones'].items():
  if v>q:w['milestones'][k]=v-1
 return w

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--one',type=Path,required=True);ap.add_argument('--two',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).with_name('RESULT.json'));ar=ap.parse_args()
 source=ar.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==NATIVE,'native pin');roots=json.loads(raw)['native_roots'];need(len(roots)==111,'native root count');dot=lambda x,y:sum(a*b for a,b in zip(x,y));C=[sum(1<<j for j in range(111)if i==j or dot(roots[i],roots[j])==0)for i in range(111)];need(len(binary_basis(C))==9,'canonical rank');need(all((w&15).bit_count()%2==0 and(w&240).bit_count()%2==0 for w in C),'axis quartet identities');selected=[];r=[]
 for j,w in enumerate(C):
  if len(binary_basis(r+[w]))>len(r):selected.append(j);r.append(w)
 need(selected==[0,1,2,4,8,9,14,30,59],'canonical basis roles');out={}
 for kind,path in [('one',ar.one),('two',ar.two)]:
  manifest=json.loads((path/'MANIFEST.json').read_text())
  for n,h in manifest['files'].items():need(hashlib.sha256((path/n).read_bytes()).hexdigest()==h,'frozen package changed: '+n)
  word=json.loads((path/'WORD.json').read_text());need(word['native_sha256']==NATIVE,'word native pin');need(word['canonical_basis_roles']==selected,'word basis roles');r=replay(word,roots,C,kind);r['price']=price_check({int(k):v for k,v in r['movement_profile'].items()},json.loads((path/'PRICE.json').read_text()));mutants=[]
  cache='A'if kind=='one'else'A0';tests=[('missing_early_cache_capture',lambda o:o==['ADD','X1',cache],False),('missing_cache_read',lambda o:o==['ADD',cache,'Y0'],False),('missing_canonical_source_term',lambda o:o==['ADD','X1','P0'],False),('missing_inverse_restoration',lambda o:o==['ADD','X0','X1'],True),('missing_cache_retirement',lambda o:o==['CLEAR',cache],False)]
  if kind=='two':tests += [('missing_paid_G0_route',lambda o:o==['MOVE','G0','zero'],False),('missing_shared_correction_read',lambda o:o==['ADD','Z','Y0'],False)]
  else:tests += [('missing_full_facet_read',lambda o:o==['ADD','B','Y0'],False)]
  for name,pred,last in tests:
   bad=delete_op(word,pred,last)
   try:replay(bad,roots,C,kind,False)
   except Reject as e:mutants.append({'name':name,'rejected':True,'reason':str(e)})
   else:raise Reject('semantic mutant survived: '+name)
  bad=copy.deepcopy(word);ret=next(j for j,o in enumerate(bad['operations'])if o==['MOVE','X0','Hub']);before=next(v for k,v in bad['milestones'].items()if 'delivered'in k);op=bad['operations'].pop(ret);bad['operations'].insert(before,op)
  try:replay(bad,roots,C,kind,False)
  except Reject as e:mutants.append({'name':'premature_return_invalidates_early_claim','rejected':True,'reason':str(e)})
  else:raise Reject('early chronology mutant survived')
  if kind=='two':
   bad=copy.deepcopy(word);bad['actual_ground_information_dimension']=9
   try:replay(bad,roots,C,kind,False)
   except Reject as e:mutants.append({'name':'hiding_two_ground_directions','rejected':True,'reason':str(e)})
   else:raise Reject('ground rank understatement survived')
  r['negative_controls']=mutants;r['proof_sha256']=hashlib.sha256((path/'PROOF.md').read_bytes()).hexdigest();r['word_sha256']=hashlib.sha256((path/'WORD.json').read_bytes()).hexdigest();r['manifest_sha256']=hashlib.sha256((path/'MANIFEST.json').read_bytes()).hexdigest();out[kind]=r
 # Native-specific foreign split is derived afresh from the root coordinates.
 classes=Counter((roots[j][0]==0,roots[j][4]==0)for j in range(8,111));need(classes=={(True,True):20,(True,False):29,(False,True):31,(False,False):23},'nonaxis class census')
 result={'status':'PASS_INDEPENDENT_ACTUAL_CACHED_EARLY_HUB_REVIEW','native_sha256':NATIVE,'canonical_binary_rank':9,'canonical_basis_roles':selected,'source_chart_arithmetic':'independent rational RREF/nullspace; no author imports','formal_columns':222,'integer_root_scale':str(SCALE),'nonaxis_classes':{str(k):v for k,v in classes.items()},'packages':out,'classification':'Verified literal partial sources with actual retained-cache chronology repair; no complete decoder or new kappa.'}
 ar.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'completed_targets':{k:v['completed_targets']for k,v in out.items()},'counts':{k:v['counts']for k,v in out.items()},'negative_controls':{k:len(v['negative_controls'])for k,v in out.items()}}))
if __name__=='__main__':main()
