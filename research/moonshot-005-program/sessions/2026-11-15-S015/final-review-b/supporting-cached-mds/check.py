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


LOCAL='831ac2f8ba647a50866af61461f9f378c76a443801f372154745520b4caa96fa'

def four_row(w,k):
 return sum(1<<(4*j+k)for j in range(111)if w>>j&1)

def replay(w,roots,canonical,strict=True):
 need(w['physical_binary_copies']==4,'physical copy count changed')
 charts={n:(rr(c['rows'])if c['kind']=='span'else nullspace(c['rows']))for n,c in w['charts'].items()}
 need(charts['zero']==()and len(charts['Hub'])==8,'endpoint chart dimensions')
 for j,r in enumerate(roots):
  need(charts[f'L{j}']==rr([r])and charts[f'F{j}']==nullspace([r]),'native chart altered')
 @lru_cache(None)
 def sub(a,b):return contained(charts[a],charts[b])
 co=lambda a,b:sub(a,b)and sub(b,a)
 need(w['chart_normal_native_indices']==[76,81,91,96],'MDS normal identities')
 for k,j in enumerate(w['chart_normal_native_indices']):
  need(charts[f'C{k}']==nullspace([roots[3],roots[j]])and len(charts[f'C{k}'])==6,'actual shared facet chart')
 need(charts['I']==nullspace([roots[3],roots[91],roots[96]])and len(charts['I'])==5,'common proper patch chart')
 need(sub('I','C2')and sub('I','C3'),'proper import intersection')
 X=[f'X{j}_{k}'for j in range(111)for k in range(4)];Y=[f'Y{j}_{k}'for j in range(111)for k in range(4)];P=[f'P{q}_{k}'for q in range(9)for k in range(4)];D=[f'D{k}'for k in range(4)];expected_held=['X1_2','X1_3','X2_2','X2_3'];held_index=[X.index(n)for n in expected_held]
 need(w['proper_import_originals']==expected_held,'proper imports do not name the actual four pivots')
 values={n:1<<j for j,n in enumerate(X+Y)};where={n:f'L{j//4}'for j,n in enumerate(X)}|{n:'zero'for n in Y};owners=set();ever=set(values);counts=Counter();moves=Counter();dirty=0;events={};seedrows=[];transport=[];allstates=[];seed_info={};milestones={v:k for k,v in w['milestones'].items()};fullC=[four_row(v,k)for v in canonical for k in range(4)];original_at_cut=None;held_at_cut=None;allXrestore=None
 for step,op in enumerate(w['operations'],1):
  t=op[0];counts[t]+=1
  if t=='INIT':
   _,n,c=op;need(n not in ever and c in charts,'invalid zero-owner birth');ever.add(n);owners.add(n);values[n]=0;where[n]=c
  elif t=='ADD':
   _,s,n=op;need(s in values and n in values and s!=n,'invalid live ADD');need(co(where[s],where[n]),f'noncocharted ADD {s}->{n}');values[n]^=values[s]
   if n in P:
    allstates.append(values[n])
    if not co(where[n],'Hub'):transport.append(values[n])
  elif t=='MOVE':
   _,n,dest=op;need(n in values and dest in charts,'MOVE missing live field');old=where[n];need(sub(dest,old)if n in owners else sub(old,dest),'MOVE direction/inclusion');r=abs(len(charts[old])-len(charts[dest]));need(r>0,'MOVE has zero charged rank');moves[r]+=1
   if n in P:
    transport.append(values[n]);allstates.append(values[n])
    if co(old,'Hub'):seedrows.append(values[n]);seed_info[n]=values[n]
   where[n]=dest
  elif t=='CLEAR':
   _,n=op;need(n in owners and n in values,'invalid owner retirement');dirty+=int(values[n]!=0);owners.remove(n);del values[n],where[n]
  else:raise Reject('unknown operation')
  if step in milestones:
   label=milestones[step];H=[values[n]for n in X if co(where[n],'Hub')];held=[n for n in X if not co(where[n],'Hub')];h_rank=len(binary_basis(H));intersection=h_rank+36-len(binary_basis(H+fullC));event={'step':step,'hub_rank':h_rank,'held_originals':held,'canonical_Hub_intersection_dimension':intersection}
   if label in ['cached_source_aggregate_cut','four_actual_proper_imports_at_I','actual_canonical36_at_ground_with_D4_retained_at_I']:
    need(held==expected_held and h_rank==440 and intersection==32,'incorrect early Hub/held cut');need(where['X1_2']=='C2'and where['X1_3']=='C2'and where['X2_2']=='C3'and where['X2_3']=='C3','pivots at wrong charts');need(all(values[n]==1<<(444+j)and co(where[n],'zero')for j,n in enumerate(Y)),'canonical preload chronology changed original Y early')
    G=[values[n]for n in held];need(len(binary_basis(H+G))==444 and len(binary_basis(G))==4,'Hub and pivot decomposition');need(len(binary_basis(G+fullC))==40,'canonical intersects held subspace')
   if label=='cached_source_aggregate_cut':
    original_at_cut=[values[n]for n in X];held_at_cut=[values[n]for n in held];inv=binary_inverse(original_at_cut);projected=[];held_parts=[]
    for item in w['canonical_seeds']:
     role=item['canonical_role'];k=item['copy'];c=four_row(canonical[role],k);alpha=0
     for j in range(444):
      if c>>j&1:alpha^=inv[j]
     actual_reads=[n for j,n in enumerate(X)if(alpha>>j&1)and j not in held_index];proper=[i for i,j in enumerate(held_index)if alpha>>j&1]
     need(item['Hub_reads']==actual_reads and item['proper_import_reads']==proper,'seed coefficients disagree with independent inverse');need(int(item['canonical_row_hex'],16)==c,'seed canonical row metadata wrong');dh=0
     for j in held_index:
      if alpha>>j&1:dh^=original_at_cut[j]
     projected.append(c^dh);held_parts.append(dh)
    need(len(projected)==36 and len(binary_basis(projected))==36,'Hub projection of canonical36 loses rank');need(len(binary_basis(held_parts))==4,'canonical patch does not use all four held directions');event['independently_reconstructed_Hub_projection_rank']=36;event['held_component_rank']=4
   if label=='four_actual_proper_imports_at_I':
    need(all(n in owners and co(where[n],'I')and values[n]==values[s]for n,s in zip(D,expected_held)),'proper copies not actually acquired/descended')
   if label=='actual_canonical36_at_ground_with_D4_retained_at_I':
    for q,role in enumerate(w['canonical_basis_roles']):
     for k in range(4):need(f'P{q}_{k}'in owners and co(where[f'P{q}_{k}'],'zero')and values[f'P{q}_{k}']==four_row(canonical[role],k),'literal canonical endpoint wrong or unavailable')
    need(all(n in owners and co(where[n],'I')and values[n]==values[s]for n,s in zip(D,expected_held)),'proper D copies not retained at canonical milestone');G=[values[n]for n in P];Dr=[values[n]for n in D];ranks={'terminal_ground_canonical':len(binary_basis(G)),'canonical_plus_proper_D':len(binary_basis(G+Dr)),'completed_Hub_seeds':len(binary_basis(seedrows)),'completed_seed_transport':len(binary_basis(transport)),'all_literal_principal_transients':len(binary_basis(allstates))};need(ranks=={'terminal_ground_canonical':36,'canonical_plus_proper_D':40,'completed_Hub_seeds':36,'completed_seed_transport':40,'all_literal_principal_transients':444},'canonical/history rank distinction fails');need(w['actual_ground_information_rank']==36 and w['completed_seed_and_transport_history_rank']==40 and w['literal_principal_history_including_partial_Hub_formation_rank']==444,'word understates actual information history');event.update(ranks)
    for item in w['canonical_seeds']:
     row=0
     for n in item['Hub_reads']:row^=original_at_cut[X.index(n)]
     need(seed_info[item['packet']]==row,'departing principal seed differs from authenticated source projection')
   if label=='original_local_correction_completed_sources_not_yet_restored':
    need(all(values[f'Y3_{k}']==((1<<(444+12+k))^(1<<(12+k)))and co(where[f'Y3_{k}'],'F3')for k in range(4)),'actual four-copy output not completed');event['all_four_native_Y3_outputs_complete']=True
   if label=='original_all_original_sources_restored':
    need(all(values[n]==1<<j and co(where[n],'Hub')for j,n in enumerate(X)),'all-source inverse restoration failed');allXrestore=step
   events[label]=event
 need(not owners,'unretired owner at closed word')
 need(all(values[n]==1<<j and co(where[n],'Hub')for j,n in enumerate(X)),'final original X map incorrect')
 for j in range(111):
  for k in range(4):
   n=f'Y{j}_{k}';target=(1<<(444+4*j+k))^((1<<(4*j+k))if j==3 else 0);need(values[n]==target and co(where[n],f'F{j}'),'final original Y map incorrect')
 if strict:need(dict(counts)=={'INIT':44,'ADD':4181,'MOVE':1204,'CLEAR':44}and dirty==44,'full ordinary/owner invoice');need(dict(moves)=={1:16,2:228,3:36,5:268,6:4,7:652},'full movement invoice')
 return {'counts':dict(counts),'movement_profile':dict(sorted(moves.items())),'dirty_retirements':dirty,'events':events,'all_888_independent_columns_checked':True,'completed_native_roles':[3],'physical_copies':4,'uncompleted_native_outputs':440}

def delete_operation(w,pred,last=False):
 z=copy.deepcopy(w);ids=[j for j,op in enumerate(z['operations'])if pred(op)];need(bool(ids),'negative-control target absent');q=ids[-1]if last else ids[0];z['operations'].pop(q)
 for k,v in z['milestones'].items():
  if v>q:z['milestones'][k]=v-1
 return z

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--local-word',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).with_name('RESULT.json'));a=ap.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();need(hashlib.sha256(raw).hexdigest()==NATIVE,'native SHA');roots=json.loads(raw)['native_roots'];need(len(roots)==111,'native count');dot=lambda u,v:sum(x*y for x,y in zip(u,v));C=[sum(1<<j for j in range(111)if i==j or dot(roots[i],roots[j])==0)for i in range(111)];need(len(binary_basis(C))==9 and C[3]==C[0]^C[1]^C[2],'canonical rank or native four-axis identity')
 manifest=json.loads((a.source/'MANIFEST.json').read_text())
 for n,h in manifest['files'].items():need(hashlib.sha256((a.source/n).read_bytes()).hexdigest()==h,'reviewed file changed: '+n)
 w=json.loads((a.source/'WORD.json').read_text());need(w['native_sha256']==NATIVE and w['local_word_sha256']==LOCAL,'word dependency pins');need(hashlib.sha256(a.local_word.read_bytes()).hexdigest()==LOCAL,'preceding local source changed');local=json.loads(a.local_word.read_text());foreign=[j for j in range(111)if j!=3 and dot(roots[j],roots[3])==0];need(w['foreign_indices']==foreign and len(foreign)==58,'all foreign inputs not authenticated');need(w['source_assignments']==local['source_assignments']and w['pivot_originals']==local['pivot_originals'],'local actual source assignment changed')
 r=replay(w,roots,C)
 canonical_cut=w['milestones']['actual_canonical36_at_ground_with_D4_retained_at_I']
 need(not any((op[0]=='ADD'and op[2].startswith('Y'))or(op[0]=='MOVE'and op[1].startswith('Y'))for op in w['operations'][:canonical_cut]),'an original Y was touched before actual canonical ground delivery')
 # Preserve all original-X source operations and all original movements from the earlier local word.
 def xops(word):return [op for op in word['operations']if(op[0]=='ADD'and op[1].startswith('X')and op[2].startswith('X'))or(op[0]=='MOVE'and op[1].startswith('X'))]
 need(xops(w)==xops(local),'original X transformation/routes differ from credited local word')
 oldmoves=Counter(tuple(op)for op in local['operations']if op[0]=='MOVE');originalmoves=Counter(tuple(op)for op in w['operations']if op[0]=='MOVE'and(op[1].startswith('X')or op[1].startswith('Y')));need(oldmoves==originalmoves,'ordinary original movement omitted during composition')
 p={rank:F(count,4)for rank,count in r['movement_profile'].items()};need(p=={1:4,2:57,3:9,5:67,6:1,7:163},'unjustified movement normalization');r['normalized_movement_profile']={str(k):str(v)for k,v in p.items()};r['price']=price_check(p,json.loads((a.source/'PRICE.json').read_text()))
 tests=[('missing_anchor_capture',lambda o:o[0]=='ADD'and o[2]=='A0_0',False),('missing_actual_D_capture',lambda o:o==['ADD','X1_2','D0'],False),('missing_D_descent',lambda o:o==['MOVE','D0','I'],False),('missing_canonical_patch',lambda o:o[0]=='ADD'and o[1]=='D0'and o[2].startswith('P'),False),('missing_ground_Y_preload',lambda o:o==['ADD','P0_0','Y3_0'],False),('missing_anchor_read',lambda o:o==['ADD','A0_0','Y3_0'],False),('missing_source_inverse',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X'),True),('missing_D_retirement',lambda o:o==['CLEAR','D0'],False)];controls=[]
 for name,pred,last in tests:
  bad=delete_operation(w,pred,last)
  try:replay(bad,roots,C,False)
  except Reject as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
  else:raise Reject('semantic control survived: '+name)
 for key,wrong in [('literal_principal_history_including_partial_Hub_formation_rank',40),('actual_ground_information_rank',32),('physical_binary_copies',1)]:
  bad=copy.deepcopy(w);bad[key]=wrong
  try:replay(bad,roots,C,False)
  except Reject as e:controls.append({'name':'understated_'+key,'rejected':True,'reason':str(e)})
  else:raise Reject('scope mutation survived: '+key)
 r.update(status='PASS_INDEPENDENT_CACHED_MDS_CANONICAL_SOURCE',negative_controls=controls,native_sha256=NATIVE,local_word_sha256=LOCAL,source_proof_sha256=hashlib.sha256((a.source/'PROOF.md').read_bytes()).hexdigest(),source_word_sha256=hashlib.sha256((a.source/'WORD.json').read_bytes()).hexdigest(),source_manifest_sha256=hashlib.sha256((a.source/'MANIFEST.json').read_bytes()).hexdigest(),classification='Literal chronological partial source; four physical copies of receiver3 completed; no full decoder or new kappa.',implementation='Independent rational RREF, low-pivot binary elimination, actual 444x444 inverse; no author imports.')
 a.out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:r[k]for k in['status','counts','movement_profile','dirty_retirements']}));print('semantic negative controls:',len(controls))
if __name__=='__main__':main()
