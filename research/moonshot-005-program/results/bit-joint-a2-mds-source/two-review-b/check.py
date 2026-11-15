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


def gm(a,b):
 z=0
 for i in range(2):
  for j in range(2):
   if(a>>i&1)and(b>>j&1):z^=1<<(i+j)
 if z&4:z^=7
 return z

def gi(a):
 need(a!=0,'GF4 inverse of zero');return next(b for b in range(1,4)if gm(a,b)==1)

def four_row(row,k):return sum(1<<(4*j+k)for j in range(111)if row>>j&1)

def gf_encode_rows(root,channels):
 p,q=channels;d=gi(p^q);matrix=[[gm(d,q),d],[gm(d,p),d]];out=[]
 for slot in range(2):
  for bit in range(2):
   row=0
   for inp in range(2):
    for b in range(2):
     if gm(matrix[slot][inp],1<<b)>>bit&1:row^=1<<(4*root+2*inp+b)
   out.append(row)
 return out

def canonical_line(v):
 if next(x for x in v if x)<0:return tuple(-x for x in v)
 return tuple(v)

def full_root_closure(roots):
 S={canonical_line(r)for r in roots}
 while True:
  new=set(S)
  for r in S:
   for s in S:
    d=sum(x*y for x,y in zip(r,s));need(d%2==0,'nonintegral root reflection');new.add(canonical_line([x-(d//2)*y for x,y in zip(r,s)]))
  if new==S:return S
  S=new

def validate_geometry(w,g,R):
 dot=lambda u,v:sum(x*y for x,y in zip(u,v));targets=[3,76];need(w['completed_native_roles']==targets and g['receivers']==targets,'joint target indices');common=[j for j in range(111)if dot(R[3],R[j])==0 and dot(R[76],R[j])==0];need(common==g['common_roles']==w['common_roles']and len(common)==36,'shared source partition');full=full_root_closure(R);need(len(full)==120,'full native root closure');priv={};enc={};expected_pivots={};expected_members={}
 for data in g['private_data']:
  i=data['receiver'];other=76 if i==3 else 3;roles=[j for j in range(111)if j!=i and dot(R[i],R[j])==0 and dot(R[other],R[j])!=0];priv[i]=roles;need(roles==data['private_roles']==w['private_roles'][str(i)],'private source partition');need(len(data['normals'])==4,'private chart count')
  for t,q in enumerate(data['normals']):
   need(canonical_line(q)in full and abs(dot(R[i],q))==2,'private normal not an actual A2 root');need(w['charts'][f'C{i}_{t}']=={'kind':'ann','rows':[R[i],q]},'private chart normal metadata');expected_members[i,t]=[]
  special=dict(zip(data['pivot_roles'],data['pivot_selected_pairs']))
  for j in roles:
   available=[t for t,q in enumerate(data['normals'])if dot(R[j],q)==0];need(len(available)>=2,'private source not double covered');receiver,chosen=w['private_assignments'][str(j)];need(receiver==i and len(chosen)==2 and len(set(chosen))==2 and set(chosen)<=set(available),'private source assignment unavailable');need(chosen==(special[j]if j in special else available[:2]),'source assignment differs from fixed declared choice');enc[j]=gf_encode_rows(j,chosen)
   for slot,t in enumerate(chosen):expected_members[i,t].append((j,slot))
  for t in range(4):
   candidates=[(j,s)for j,s in expected_members[i,t]if j in special];need(len(candidates)==1,'private pivot not uniquely assigned');expected_pivots[i,t]=candidates[0];need(list(candidates[0])==w['private_pivots'][f'{i}:{t}'],'actual private pivot mismatch')
 need(len(priv[3])==22 and len(priv[76])==24 and set(priv[3]).isdisjoint(priv[76]),'private family overlap');need(set(map(int,w['private_assignments']))==set(priv[3])|set(priv[76]),'extraneous or missing source encodings')
 expected_rows={}
 for (i,t),items in expected_members.items():
  pj,ps=expected_pivots[i,t]
  for bit in range(2):
   v=0
   for j,s in items:v^=enc[j][2*s+bit]
   expected_rows[f'X{pj}_{2*ps+bit}']=v
 return {'common':common,'private':priv,'encoders':enc,'aggregate_rows':expected_rows,'full_root_count':120}

def replay(w,R,C,g,strict=True):
 structure=validate_geometry(w,g,R);charts={n:(rr(c['rows'])if c['kind']=='span'else nullspace(c['rows']))for n,c in w['charts'].items()};need(charts['zero']==()and len(charts['Hub'])==8,'bad endpoint charts')
 for j,r in enumerate(R):need(charts[f'L{j}']==rr([r])and charts[f'F{j}']==nullspace([r]),'bad native source geometry')
 @lru_cache(None)
 def sub(a,b):return contained(charts[a],charts[b])
 co=lambda a,b:sub(a,b)and sub(b,a)
 need(charts['CC']==nullspace([R[3],R[76]])and len(charts['CC'])==6 and sub('CC','F3')and sub('CC','F76'),'actual common chart geometry')
 for i in [3,76]:
  for t in range(4):need(len(charts[f'C{i}_{t}'])==6 and sub(f'C{i}_{t}',f'F{i}'),'private chart dimension or target inclusion')
 X=[f'X{j}_{k}'for j in range(111)for k in range(4)];Y=[f'Y{j}_{k}'for j in range(111)for k in range(4)];P=[f'P{q}'for q in range(36)];A=[f'A{k}'for k in range(4)];held_expected=[f'X{j}_{k}'for j in [1,4,60,64]for k in range(4)];need(w['direct_query_originals']==held_expected,'held pivot set')
 value={n:1<<j for j,n in enumerate(X+Y)};where={n:f'L{j//4}'for j,n in enumerate(X)}|{n:'zero'for n in Y};owners=set();ever=set(value);counts=Counter();moves=Counter();dirty=0;events={};milestones={v:k for k,v in w['milestones'].items()};C4=[four_row(v,k)for v in C for k in range(4)];seeds=[];seed_values={};transport=[];allhistory=[];X_cut=None;basis_rows=[];Y_preloads={};trajectory={n:[where[n]]for n in X};cache_capture={n:[]for n in A};cache_reads={n:[]for n in A};seed_read_count=0;direct_reads=[];first_Y_touch=None
 for step,op in enumerate(w['operations'],1):
  t=op[0];counts[t]+=1
  if t=='INIT':
   _,n,c=op;need(n not in ever and c in charts,'invalid owner birth');ever.add(n);owners.add(n);value[n]=0;where[n]=c
  elif t=='ADD':
   _,s,n=op;need(s in value and n in value and s!=n,'invalid live ADD');need(co(where[s],where[n]),f'noncocharted ADD {s}->{n}');value[n]^=value[s]
   if n in A:cache_capture[n].append((step,s))
   if s in A:cache_reads[s].append((step,n))
   if n in P:
    allhistory.append(value[n])
    if co(where[n],'Hub'):seed_read_count+=1
    else:transport.append(value[n]);direct_reads.append((step,s,n,where[n]))
   if n in Y:
    if first_Y_touch is None:first_Y_touch=step
    if co(where[n],'zero')and s in P:Y_preloads.setdefault(n,[]).append(s)
  elif t=='MOVE':
   _,n,dest=op;need(n in value and dest in charts,'MOVE without live record');old=where[n];need(sub(dest,old)if n in owners else sub(old,dest),f'wrong directional MOVE {n}:{old}->{dest}');rank=abs(len(charts[dest])-len(charts[old]));need(rank>0,'zero charged MOVE');moves[rank]+=1
   if n in X:trajectory[n].append(dest)
   if n in P:
    transport.append(value[n]);allhistory.append(value[n])
    if co(old,'Hub'):seeds.append(value[n]);seed_values[n]=value[n]
   if n in Y and first_Y_touch is None:first_Y_touch=step
   where[n]=dest
  elif t=='CLEAR':
   _,n=op;need(n in owners and n in value,'invalid retirement');dirty+=int(value[n]!=0);owners.remove(n);del value[n],where[n]
  else:raise Reject('unknown opcode')
  if step in milestones:
   label=milestones[step];H=[value[n]for n in X if co(where[n],'Hub')];held=[n for n in X if not co(where[n],'Hub')];hr=len(binary_basis(H));event={'step':step,'Hub_rank':hr,'held_originals':held,'canonical_Hub_intersection':hr+36-len(binary_basis(H+C4))}
   if label in ['joint_source_aggregate_cut','canonical36_at_ground_before_all_Y_moves']:
    need(held==held_expected and hr==428 and event['canonical_Hub_intersection']==20,'joint source cut rank/chronology');Dr=[value[n]for n in held];need(len(binary_basis(Dr))==16 and len(binary_basis(H+Dr))==444 and len(binary_basis(Dr+C4))==52,'joint source quotient');need(all(value[n]==1<<(444+j)and co(where[n],'zero')for j,n in enumerate(Y)),'Y modified before canonical preload availability');need(first_Y_touch is None,'an original Y was touched too early')
    for k,n in enumerate(A):need(n in owners and co(where[n],'CC')and value[n]==sum(1<<(4*j+k)for j in structure['common']),'shared cache not actual common sum')
   if label=='joint_source_aggregate_cut':
    for n,v in structure['aggregate_rows'].items():need(value[n]==v,'actual private MDS aggregate incorrect')
    X_cut=[value[n]for n in X];inv=binary_inverse(X_cut);need(all(v>>444==0 for v in X_cut),'Y contamination in source transform');bi={n:j for j,n in enumerate(X)};held_ids=[bi[n]for n in held];projection=[];hs=[]
    for q,item in enumerate(w['canonical_seeds']):
     c=int(item['canonical_row_hex'],16);basis_rows.append(c);need(item['packet']==f'P{q}'and len(binary_basis(C4+[c]))==36,'adapted field is not canonical');alpha=0
     for j in range(444):
      if c>>j&1:alpha^=inv[j]
     hub=[n for j,n in enumerate(X)if alpha>>j&1 and j not in held_ids];missing=[n for j,n in enumerate(X)if alpha>>j&1 and j in held_ids];proj=sum(((alpha>>j)&1)<<k for k,j in enumerate(held_ids));need(item['Hub_reads']==hub and item['direct_original_reads']==missing,'canonical source coefficients disagree with independent inverse');need(len(missing)<=1 and int(item['held_projection_hex'],16)==proj,'canonical field needs unrecorded proper source');projection.append(proj);h=0
     for n in hub:h^=X_cut[bi[n]]
     hs.append(h)
    need(len(basis_rows)==36 and len(binary_basis(basis_rows))==36,'adapted canonical basis rank');need(projection==[1<<j for j in range(16)]+[0]*20,'adapted source projection is not unit-pivot normal form');need(len(binary_basis(hs))==36,'completed projected Hub basis rank');event['canonical_held_projection_rank']=len(binary_basis(projection));event['independent_inverse_columns_checked']=444
    ev=[sum(((row>>j)&1)<<k for k,j in enumerate([1,4,60,64]))for row in C];need(len(binary_basis(ev))==4,'scalar canonical pivot evaluations lose rank')
    for row in basis_rows:
     patterns={(row>>(4*j))&15 for j in range(111)}-{0};need(len(patterns)==1,'selected canonical row outside the declared tensor family');scalar=sum(1<<j for j in range(111)if(row>>(4*j))&15);need(len(binary_basis(C+[scalar]))==9,'selected scalar tensor factor not canonical')
    event['scalar_pivot_evaluation_rank']=4;event['declared_tensor_candidates']=511*15;event['zero_projection_tensor_candidates']=(2**(9-4)-1)*15
    meta=w['canonical_basis_selection'];need(meta['candidate_count']==7665 and meta['zero_projection_candidates']==465 and meta['Hub_basis_dimension']==20,'finite candidate family counts incorrect')
   if label=='canonical36_at_ground_before_all_Y_moves':
    for q,n in enumerate(P):need(n in owners and co(where[n],'zero')and value[n]==basis_rows[q],'actual canonical ground field missing')
    actual_ground=[value[n]&((1<<444)-1)for n in owners if co(where[n],'zero')];ranks={'terminal_canonical_ground':len(binary_basis(actual_ground)),'completed_Hub_seed':len(binary_basis(seeds)),'completed_seed_transport':len(binary_basis(transport)),'all_principal_transients':len(binary_basis(allhistory)),'all_live_owned_source_rank':len(binary_basis([value[n]&((1<<444)-1)for n in owners]))};need(ranks['terminal_canonical_ground']==36 and ranks['completed_Hub_seed']==36 and ranks['completed_seed_transport']==52 and ranks['all_principal_transients']==444,'joint canonical/history ranks');need(w['actual_ground_information_rank']==36,'understated/incorrect ground rank');event.update(ranks)
    for item in w['canonical_seeds']:
     h=0
     for n in item['Hub_reads']:h^=X_cut[X.index(n)]
     need(seed_values[item['packet']]==h,'departing canonical seed wrong');need(sorted(s for _,s,n,_ in direct_reads if n==item['packet'])==sorted(item['direct_original_reads']),'proper query different from coefficient witness')
   if label in ['actual_receiver_3_completed','actual_receiver_76_completed']:
    i=int(label.split('_')[2]);need(all(value[f'Y{i}_{k}']==((1<<(444+4*i+k))^(1<<(4*i+k)))and co(where[f'Y{i}_{k}'],f'F{i}')for k in range(4)),'joint native output incomplete');event['actual_completed_receiver']=i
   if label=='all_X_restored':need(all(value[n]==1<<j and co(where[n],'Hub')for j,n in enumerate(X)),'original source inverse/restoration failed')
   events[label]=event
 need(not owners,'live owner remains')
 for j,n in enumerate(X):need(value[n]==1<<j and co(where[n],'Hub'),'final original X changed')
 for i in range(111):
  for k in range(4):need(value[f'Y{i}_{k}']==((1<<(444+4*i+k))^((1<<(4*i+k))if i in [3,76]else 0))and co(where[f'Y{i}_{k}'],f'F{i}'),'final original Y changed')
 for k,n in enumerate(A):
  need([s for _,s in cache_capture[n]]==[f'X{j}_{k}'for j in structure['common']],'shared capture is not exactly once per real source');need([s for _,s in cache_reads[n]]==[f'Y3_{k}',f'Y76_{k}'],'shared cache not actually reused by both receivers')
 for n,path in trajectory.items():need(path[-1]=='Hub'and path.count('Hub')==1,'original trajectory reset or duplicated Hub arrival')
 for witness in w['canonical_preload_witnesses']:
  i=witness['receiver'];k=witness['copy'];names=[f'P{q}'for q in witness['principal_indices']];need(Y_preloads[f'Y{i}_{k}']==names,'actual canonical Y read list wrong');row=0
  for q in witness['principal_indices']:row^=basis_rows[q]
  need(row==four_row(C[i],k),'canonical Y preload combination not exact')
 if strict:need(dict(counts)=={'INIT':40,'ADD':3936,'MOVE':1292,'CLEAR':40},'full operation invoice differs');need(dict(moves)=={1:40,2:328,5:328,6:24,7:552,8:20}and dirty==40,'complete physical movement/dirty invoice differs')
 return {'counts':dict(counts),'movement_profile':dict(sorted(moves.items())),'dirty_retirements':dirty,'events':events,'shared_capture_source_rows':36,'actual_shared_cache_owners':4,'same_cache_read_by_both_groups':True,'single_original_X_trajectories':444,'original_X_and_Y_columns':888,'private_family_sizes':[22,24],'completed_native_roles':[3,76],'physical_binary_copies':4,'actual_completed_outputs':8,'uncompleted_outputs':436,'actual_completed_Hub_seed_ADD_count':seed_read_count,'proper_original_reads':len(direct_reads),'Y_preload_ADD_count':sum(map(len,Y_preloads.values())),'first_original_Y_touch':first_Y_touch}

def delete_operation(w,pred,last=False):
 z=copy.deepcopy(w);ids=[j for j,op in enumerate(z['operations'])if pred(op)];need(ids,'mutation target absent');q=ids[-1]if last else ids[0];z['operations'].pop(q)
 for k,v in z['milestones'].items():
  if v>q:z['milestones'][k]=v-1
 return z

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--preliminary',action='store_true');ap.add_argument('--out',type=Path,default=Path(__file__).with_name('RESULT.json'));a=ap.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==NATIVE,'native pin');R=json.loads(raw)['native_roots'];dot=lambda r,s:sum(x*y for x,y in zip(r,s));C=[sum(1<<j for j in range(111)if j==i or dot(R[i],R[j])==0)for i in range(111)];need(len(binary_basis(C))==9,'canonical native rank');w=json.loads((a.source/'WORD.json').read_text());g=json.loads((a.source/'GEOMETRY.json').read_text());need(w['native_sha256']==NATIVE and w['geometry_sha256']==hashlib.sha256((a.source/'GEOMETRY.json').read_bytes()).hexdigest(),'actual source pins');need(w['physical_binary_copies']==4,'copy normalization')
 if not a.preliminary:
  m=json.loads((a.source/'MANIFEST.json').read_text())
  for n,h in m['files'].items():need(hashlib.sha256((a.source/n).read_bytes()).hexdigest()==h,'frozen author bytes changed: '+n)
 result=replay(w,R,C,g,not a.preliminary)
 if not a.preliminary:
  result['price']=price_check({int(k):F(v,4)for k,v in result['movement_profile'].items()},json.loads((a.source/'PRICE.json').read_text()))
  tests=[('omit_shared_capture',lambda o:o==['ADD','X0_0','A0'],False),('omit_second_receiver_shared_read',lambda o:o==['ADD','A0','Y76_0'],False),('omit_private_source_encoding',lambda o:o[0]=='ADD'and o[1].startswith('X1_')and o[2].startswith('X1_'),False),('omit_direct_canonical_pivot_read',lambda o:o[0]=='ADD'and o[1]=='X1_0'and o[2].startswith('P'),False),('omit_second_canonical_preload',lambda o:o[0]=='ADD'and o[1].startswith('P')and o[2]=='Y76_0',False),('omit_second_private_decoder_term',lambda o:o[0]=='ADD'and o[1].startswith('X60_')and o[2].startswith('Y76_'),False),('omit_first_receiver_private_decoder_term',lambda o:o[0]=='ADD'and o[1].startswith('X1_')and o[2].startswith('Y3_'),False),('omit_source_inverse',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'),True),('omit_shared_cache_retirement',lambda o:o==['CLEAR','A0'],False)];controls=[]
  for name,pred,last in tests:
   bad=delete_operation(w,pred,last)
   try:replay(bad,R,C,g,False)
   except Reject as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
   else:raise Reject('joint semantic mutant survived: '+name)
  bad=copy.deepcopy(w);cut=bad['milestones']['canonical36_at_ground_before_all_Y_moves'];idx=next(j for j,op in enumerate(bad['operations'])if op==['MOVE','Y76_0','CC']);op=bad['operations'].pop(idx);bad['operations'].insert(cut-1,op)
  try:replay(bad,R,C,g,False)
  except Reject as e:controls.append({'name':'Y76_leaves_before_canonical_preload','rejected':True,'reason':str(e)})
  else:raise Reject('chronology mutant survived')
  bad=copy.deepcopy(w);q=next(j for j,op in enumerate(bad['operations'])if op==['MOVE','X0_0','Hub']);bad['operations'].insert(q+1,['MOVE','X0_0','CC'])
  for k,v in bad['milestones'].items():
   if v>q:bad['milestones'][k]=v+1
  try:replay(bad,R,C,g,False)
  except Reject as e:controls.append({'name':'reset_shared_source_for_a_second_visit','rejected':True,'reason':str(e)})
  else:raise Reject('shared reset mutant survived')
  result['negative_controls']=controls
 result.update(status='PRELIMINARY_INDEPENDENT_JOINT_WORD'if a.preliminary else'PASS_INDEPENDENT_JOINT_TWO_RECEIVER_MDS',native_sha256=NATIVE,source_word_sha256=hashlib.sha256((a.source/'WORD.json').read_bytes()).hexdigest(),source_geometry_sha256=hashlib.sha256((a.source/'GEOMETRY.json').read_bytes()).hexdigest(),source_proof_sha256=None if a.preliminary else hashlib.sha256((a.source/'PROOF.md').read_bytes()).hexdigest(),classification='Actual joint two-port/four-copy source; no complete111-port decoder or new kappa.',independent_implementation='No author imports; rational chart RREF, explicit GF4 arithmetic, all888 columns, independent444 inverse and native root reflection closure.')
 a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k]for k in['status','counts','movement_profile','dirty_retirements','actual_completed_outputs','actual_completed_Hub_seed_ADD_count','proper_original_reads','Y_preload_ADD_count']}))
if __name__=='__main__':main()
