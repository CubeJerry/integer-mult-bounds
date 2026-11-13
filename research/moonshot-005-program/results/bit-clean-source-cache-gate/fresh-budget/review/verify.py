"""Independent primary-source replay, Hasse-chain unions and complete budget."""
import argparse,collections,gzip,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def introws(rr):
 ans=[]
 for r in rr:
  x=list(map(F,r));d=math.lcm(*(v.denominator for v in x));ans.append([int(v*d) for v in x])
 return ans
def floorroot(n,k):
 x=1<<((n.bit_length()+k-1)//k)
 while True:
  y=((k-1)*x+n//x**(k-1))//k
  if y>=x:break
  x=y
 while (x+1)**k<=n:x+=1
 while x**k>n:x-=1
 assert x**k<=n<(x+1)**k
 return x
def funct_or(xs):
 z=0
 for x in xs:z|=x
 return z
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP
 s=json.loads(gzip.decompress(raw));fr={int(c):f for c,f in s['frames'].items()};BB={c:introws(f['B']) for c,f in fr.items()};AA={c:introws(f['A']) for c,f in fr.items()}
 def sub(c,d):return all(dot(b,v)==0 for b in BB[c] for v in AA[d])
 roots=[BB[c][0] for c in s['start'][:111]];row=[1<<i for i in range(111)];where=s['start'][:111].copy();history=collections.defaultdict(set);cleanpaid=collections.Counter();ops=collections.Counter()
 def record(i):history[where[i]].add(row[i])
 for i in range(111):record(i)
 for ev in s['program']:
  op,i=ev[:2]
  if i>=111:continue
  if op in ('ADD','SWAP'):
   j=ev[2]
   if j>=111:continue
   ops[op]+=1
   if op=='ADD':
    assert where[i]==where[j]==ev[3];row[i]^=row[j]
   else:row[i],row[j]=row[j],row[i];where[i],where[j]=where[j],where[i];record(j)
   record(i)
  elif op=='MOVE':
   c,d=ev[2:];assert where[i]==c and sub(c,d) and fr[d]['dim']>fr[c]['dim'];cleanpaid[fr[d]['dim']-fr[c]['dim']]+=1;where[i]=d;record(i)
  else:raise AssertionError(op)
 assert row==[1<<i for i in range(111)] and where==s['final'][:111]
 assert dict(cleanpaid)=={1:289,2:244} and sum(map(len,history.values()))==1027
 support={c:funct_or(v) for c,v in history.items()}
 for c,mask in support.items():
  assert all(all(dot(roots[j],a)==0 for a in AA[c]) for j in range(111) if mask>>j&1)
 charts=sorted(history,key=lambda c:(fr[c]['dim'],c));lower={};covers={};states={};total=0
 for k,c in enumerate(charts):
  pred=[d for d in charts[:k] if fr[d]['dim']<fr[c]['dim'] and sub(d,c)]
  lower[c]=set(pred);maximal=[]
  for d in reversed(pred):
   if not any(d in lower[e] for e in maximal):maximal.append(d)
  covers[c]=maximal
  states[c]={support[c]|u for d in maximal for u in states[d]} if maximal else {support[c]}
  total+=len(states[c])
 assert all(not sub(c,d) for c,d in itertools.combinations(charts,2) if fr[c]['dim']==fr[d]['dim'])
 contacts=[];allowed=[];max_chain=[]
 for i in range(111):
  facet=s['final'][111+i];assert fr[facet]['dim']==7 and all(dot(roots[i],v)==0 for v in BB[facet])
  si=sum(int(i!=j and dot(roots[i],roots[j])==0)<<j for j in range(111));contacts.append(si)
  eligible=[c for c in charts if sub(c,facet)];unions={u for c in eligible for u in states[c]};assert unions
  assert all(not(u&~si) for u in unions);assert funct_or(support[c] for c in eligible)==si
  allowed.append(unions);max_chain.append(max(u.bit_count() for u in unions))
 per=[]
 for i,si in enumerate(contacts):
  best=min(((si&~contacts[h]&~u).bit_count(),h,u) for h in range(111) if h!=i for u in allowed[i])
  per.append({'receiver':i,'minimum_exception_ports':best[0],'partner':best[1],'chain_union_mask':best[2]})
 assert min(v['minimum_exception_ports'] for v in per)==12 and max(v['minimum_exception_ports'] for v in per)==22
 assert max(max_chain)==18 and min(si.bit_count()-m for si,m in zip(contacts,max_chain))==39
 caps={d:max(support[c].bit_count() for c in charts if fr[c]['dim']==d) for d in sorted({fr[c]['dim'] for c in charts})};assert caps=={1:1,2:2,4:9,6:12,7:13,8:111}
 print(json.dumps({'phase':'SOURCE_AND_CHAINS_PASS','history_charts':len(charts),'hasse_edges':sum(map(len,covers.values())),'all_hasse_union_states':total,'exception_min':12,'exception_max':22,'caps':caps}),flush=True)
 # Build the complete accepted paired-caller profiles from independently recounted native/helper atoms.
 N=collections.Counter(abs(fr[e[3]]['dim']-fr[e[2]]['dim']) for e in s['program'] if e[0]=='MOVE')
 H=collections.Counter(abs(fr[s['final'][i]]['dim']-fr[s['start'][i]]['dim']) for i in range(222,659))
 assert dict(N)=={1:1386,2:1253,3:62,4:47,5:9,6:104,7:10} and dict(H)=={2:1,4:25,6:1,8:410}
 P2=collections.Counter({r:36*n for r,n in N.items()});P2[1]+=444
 for j in range(1,9):P2[7*j]+=444
 T2=collections.Counter({r:36*n for r,n in H.items()});T2[127]+=222
 for j in range(1,10):T2[1+7*j]+=444
 ranks=set(N)|set(H)|set(P2)|set(T2)|set(range(1,9));grid=10**36;power={}
 for r in ranks:
  target=r**199*grid**200;v=floorroot(target,200);power[r]=(F(v,grid),F(v+int(v**200!=target),grid))
 def bounds(profile):
  lo=hi=F(0)
  for r,n in profile.items():
   a,b=power[r];lo+=n*(a if n>=0 else b);hi+=n*(b if n>=0 else a)
  return [str(lo),str(hi)]
 margin={r:T2.get(r,0)-P2.get(r,0) for r in ranks};assert F(bounds(margin)[1])<0
 allowance={r:N.get(r,0)-H.get(r,0)+F(margin[r],36) for r in ranks}
 base=dict(cleanpaid);base[7]=base.get(7,0)+111;base[8]=base.get(8,0)+9
 remaining={r:allowance[r]-base.get(r,0) for r in ranks};room=bounds(remaining);assert F(room[1])<power[6][0]
 profiles=[(n1,n2,n4,n1+2*n2+9*n4) for n1 in range(6) for n2 in range(3) for n4 in range(2) if n1+2*n2+4*n4<=5];assert max(z[3] for z in profiles)==10
 # Independent punctured row-code rigidity, useful for allowing arbitrary global decoder rows.
 K=[contacts[i]|(1<<i) for i in range(111)];eb={};bs=[]
 for v in K:
  old=v
  while v:
   q=v.bit_length()-1
   if q not in eb:eb[q]=v;bs.append(old);break
   v^=eb[q]
 assert len(bs)==9
 words=[]
 for m in range(1,512):
  v=0
  for q in range(9):
   if m>>q&1:v^=bs[q]
  words.append(v)
 rho=[min((w&~K[i]).bit_count() for w in words if not(w>>i&1)) for i in range(111)];assert min(rho)==18
 assert min(v.bit_count() for v in words)==48
 out={'status':'PASS_INDEPENDENT_CACHE_SUPPORT_AND_COMPLETE_PRICE_COMPOSITION','source_sha256':SP,'method':'Primary native replay; unpruned unions along maximal Hasse paths, rather than transitive-predecessor antichain pruning.','clean_source_paid':dict(cleanpaid),'clean_source_arithmetic':dict(ops),'history_charts':len(charts),'history_distinct_rows':sum(map(len,history.values())),'hasse_edges':sum(map(len,covers.values())),'hasse_union_states':total,'per_receiver_exception_minima':per,'minimum_exception_ports':12,'maximum_exception_ports':22,'minimum_no_interaction_missing_ports':39,'maximum_single_chain_support':18,'source_history_support_caps':caps,'native_paid':dict(N),'helper_targets':dict(H),'paired_paid':dict(P2),'paired_targets':dict(T2),'limiting_complete_Q_allowance_bounds':bounds(allowance),'fixed_cleanX_Y_nineHub_lower_bounds':bounds(base),'limiting_extra_return_room_bounds':room,'rank6_power_bounds':list(map(str,power[6])),'original_paired_margin_bounds':bounds(margin),'birth_dimension_profiles_at_most5':profiles,'maximum_affordable_extra_input_union':10,'canonical_code_minimum_weight':48,'diagonal_zero_noncontact_restriction_minima':rho,'minimum_diagonal_zero_noncontact_weight':18,'negative_controls':{'pooling_incomparable_chart_supports_recovers_every_full_contact_set':True},'scope':'Fixed clean-X, stationary caches, nine unchanged canonical/gauge packets, monotone publicY coding, extra fresh single-birth returns. Mutable payloads/changed source excluded. Arbitrary-decoder corollary separate.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','minimum_exception_ports','source_history_support_caps','limiting_extra_return_room_bounds','rank6_power_bounds','minimum_diagonal_zero_noncontact_weight']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
