"""Independent400-input dense dyadic replay; no author interpreter imported."""
import argparse,collections,copy,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
FP='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
AP='7b0f31383391da6dcbeb938f8b2edf52155bf3bf86922e7ed8478ae0c8d56d3b'
PARENT='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc'
WORDS={'coded':'02abaeace9eccdd190aae71f7726f7a946106b1dc6674b4c72160d1bda986f5d','observer':'24fc1264c8d3b0345441a47dd2a50087fd416bb3e4b035a61edbbf89e02dc79e'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p,pin):
 b=p.read_bytes();assert sha(b)==pin;return json.loads(gzip.decompress(b))
def span(f):
 a={0}
 for x in f:
  assert 0<x<512;a|={z^x for z in tuple(a)}
 assert len(a)==1<<len(f);return frozenset(a)
def eqrow(a,da,b,db):
 d=max(da,db);return all((x<<(d-da))==(y<<(d-db)) for x,y in zip(a,b))
def run(w,spaces,capture_before=None,capture_after=None,purity=None):
 n=w['public'];assert n==400 and len(w['initial'])==n and all(0<=c<len(spaces) for c in w['initial']);loc=dict(enumerate(w['initial']));rows={i:[int(i==j) for j in range(n)] for i in range(n)};D=0
 cnt=collections.Counter();paid=collections.Counter();life=peak=cleared_nonzero=rescalings=0;snap={};capture_before=capture_before or {};capture_after=capture_after or {};purity=purity or [];expected={}
 def save(label,ids):snap[label]=(D,{i:rows[i].copy() for i in ids},{i:loc[i] for i in ids})
 def scale_all(k):
  nonlocal D,rescalings
  D+=k;rescalings+=1
  for i in rows:rows[i]=[v<<k for v in rows[i]]
 for t,e in enumerate(w['program']):
  if t in capture_before:
   label,ids=capture_before[t];save(label,ids)
  op,i=e[:2];assert 0<=i<n+w['owned_fields'];cnt[op]+=1
  if op=='INIT':
   assert i>=n and i not in loc and 0<=e[2]<len(spaces);loc[i]=e[2];rows[i]=[0]*n;life+=1
  elif op=='CLEAR':
   assert i>=n and i in loc and loc[i]==e[2];cleared_nonzero+=any(rows[i]);del rows[i];del loc[i]
  elif op=='MOVE':
   a,b,owned=e[2:];assert 0<=a<len(spaces) and 0<=b<len(spaces);assert type(owned)is bool and owned==(i>=n) and loc.get(i)==a
   assert spaces[a]<spaces[b] or owned and spaces[b]<spaces[a];paid[abs(len(spaces[a]).bit_length()-len(spaces[b]).bit_length())]+=1;loc[i]=b
  elif op in ('ADD','COPY'):
   j,c,at=e[2:];assert i!=j and loc.get(i)==loc.get(j)==at
   if op=='COPY':assert not any(rows[i])
   c=F(c);den=c.denominator;assert den&(den-1)==0
   if any((c.numerator*v)%den for v in rows[j]):scale_all(den.bit_length()-1)
   rows[i]=[x+c.numerator*y//den for x,y in zip(rows[i],rows[j])]
  elif op=='SCALE':
   c=F(e[2]);assert c and loc.get(i)==e[3];den=c.denominator;assert den&(den-1)==0
   if any((c.numerator*v)%den for v in rows[i]):scale_all(den.bit_length()-1)
   rows[i]=[c.numerator*v//den for v in rows[i]]
  else:raise AssertionError(op)
  peak=max(peak,len(loc)-n)
  for r,begin,end,chart,coeff in purity:
   if begin<=t<end:
    assert loc.get(r)==chart
    key=(D,tuple(sorted(coeff.items())))
    if key not in expected:expected[key]=[int(coeff.get(j,0))<<D for j in range(n)]
    assert rows[r]==expected[key],('pure-original functional',t,r)
  if t in capture_after:
   label,ids=capture_after[t];save(label,ids)
 assert set(loc)==set(rows)==set(range(n))
 return rows,D,loc,{'instructions':len(w['program']),'counts':dict(cnt),'moves':dict(sorted(paid.items())),'lifetimes':life,'peak':peak,'nonzero_owned_clears':cleared_nonzero,'common_dyadic_exponent':D,'global_rescalings':rescalings},snap
def main(a):
 mb=(a.bundle/'MANIFEST.json').read_bytes();assert sha(mb)==AP;man=json.loads(mb)
 reviewed=['KERNEL-LANE.md','CHART-MAPS.json','CONDITIONAL-BUDGET.json','kernel-coded/RESULT.json','kernel-observer/RESULT.json','source-evidence/rail-consumer.json.gz','kernel-coded/rail-kernel.json.gz','kernel-observer/rail-kernel.json.gz']
 for name in reviewed:assert sha((a.bundle/name).read_bytes())==man['artifacts'][name]
 s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',SP)
 q=load(a.bundle/'source-evidence/rail-consumer.json.gz',PARENT)
 ww={tag:load(a.bundle/f'kernel-{tag}/rail-kernel.json.gz',pin) for tag,pin in WORDS.items()}
 assert q['frames'][:len(s['frames'])]==s['frames']
 roles={int(k):v for k,v in q['source_role_map'].items()};assert sorted(roles.values())==list(range(400))
 for r,i in roles.items():assert q['initial'][i]==s['initial'][r]
 U=[17,19,30,38,40,47,52,60];R=[17,19,38,40];Y={j:roles[j+112] for j in R};pivot=Y[17];ids=list(Y.values());null={Y[17]:1,Y[19]:-1,Y[38]:-1,Y[40]:1}
 entry=[]
 for j in U:entry.extend([['INIT',400,3],['ADD',400,roles[j+112],'1',3],['MOVE',400,3,s['initial'][j],True],['ADD',roles[j],400,'-1',s['initial'][j]],['CLEAR',400,s['initial'][j]]])
 assert q['program'][:40]==entry
 oldspaces=list(map(span,q['frames']));C=frozenset.intersection(*(oldspaces[s['final'][j+112]] for j in R));assert len(C)==64
 ci=len(q['frames']);assert ci==1125 and oldspaces[3]=={0} and len(oldspaces[127])==512
 direct={}
 for j in R:
  moves=[t for t,e in enumerate(q['program']) if e[0]=='MOVE' and e[1]==Y[j]];assert len(moves)==1
  direct[j]=moves[0];assert q['program'][moves[0]]==['MOVE',Y[j],3,s['final'][j+112],False]
 packets=[];drop=set(direct.values())
 for t,e in enumerate(q['program']):
  if e[0]!='MOVE' or e[2:4]!=[127,3]:continue
  r=e[1];end=next(k for k in range(t+1,len(q['program'])) if q['program'][k][:2]==['CLEAR',r])
  assert not any(z[1]==r for z in q['program'][t+1:end]);beta={j:F(0) for j in R};hits=[]
  for k in range(t+1,end):
   z=q['program'][k]
   if z[0]=='ADD' and z[2]==r and z[1] in ids:
    j=next(j for j in R if Y[j]==z[1]);beta[j]+=F(z[3])
    if j==17:hits.append(k)
  assert len(hits)==1 and beta[17]-beta[19]-beta[38]+beta[40]==0;drop.update(hits)
  packets.append({'move':t,'clear':end,'field':r,'pivot_add':hits[0],'beta':{j:str(v) for j,v in beta.items()}})
 assert len(packets)==8 and min(direct.values())>max(p['clear'] for p in packets)
 uses={t for t,e in enumerate(q['program'][40:],40) if e[1]==pivot or e[0] in('ADD','COPY') and e[2]==pivot}
 assert uses=={direct[17]}|{p['pivot_add'] for p in packets}
 reunion=min(direct.values());early=[['ADD',pivot,Y[19],'-1',3],['ADD',pivot,Y[38],'-1',3],['ADD',pivot,Y[40],'1',3],['MOVE',pivot,3,ci,False]]
 late=[['MOVE',Y[j],3,ci,False] for j in R if j!=17]+[['ADD',pivot,Y[19],'1',ci],['ADD',pivot,Y[38],'1',ci],['ADD',pivot,Y[40],'-1',ci]]+[['MOVE',Y[j],ci,s['final'][j+112],False] for j in R]
 cap_after={p['clear']:(f'packet{k}',ids) for k,p in enumerate(packets)}
 before,db,bl,basebill,sn=run(q,oldspaces,{40:('prefix',ids),reunion:('parent_reunion',ids)},cap_after)
 for r,i in roles.items():assert bl[i]==s['final'][r]
 d,rr,ll=sn['prefix']
 for i in ids:assert eqrow(rr[i],d,[int(j==i) for j in range(400)],0)
 for k in range(8):
  d,rr,ll=sn[f'packet{k}'];combo=[rr[Y[17]][j]-rr[Y[19]][j]-rr[Y[38]][j]+rr[Y[40]][j] for j in range(400)];assert eqrow(combo,d,[null.get(j,0) for j in range(400)],0)
 results={};new_pairs={};mutant_results=[]
 for tag,w in ww.items():
  assert w['initial']==q['initial'] and w['source_role_map']==q['source_role_map'] and w['frames'][:-1]==q['frames'] and span(w['frames'][-1])==C
  observer=tag=='observer';temp=400+q['owned_fields'];en=early.copy()
  if observer:en +=[['INIT',temp,ci],['ADD',temp,pivot,'1',ci],['MOVE',temp,ci,127,True]]
  expected=[]
  for t,e in enumerate(q['program']):
   if t==40:expected.extend(en)
   if t==reunion:expected.extend(late)
   if t not in drop:expected.append(e)
  if observer:expected.append(['CLEAR',temp,127])
  assert w['program']==expected and w['owned_fields']==q['owned_fields']+int(observer)
  spaces=oldspaces+[C];em=next(t for t,e in enumerate(expected) if e==early[-1]);dec=[t for t,e in enumerate(expected) if e[0]=='ADD' and e[1]==pivot and e[4]==ci];assert len(dec)==3
  purity=[(pivot,em,dec[0],ci,null)];caps={em:('early_null',[pivot]),dec[-1]:('late_decoded',ids)}
  if observer:
   om=next(t for t,e in enumerate(expected) if e==['MOVE',temp,ci,127,True]);purity.append((temp,om,len(expected)-1,127,null));caps[om]=('observer_Hub',[temp])
   firstdown=next(t for t,e in enumerate(expected) if e[0]=='MOVE' and e[2:4]==[127,3]);pf=expected[firstdown][1];formation=max(t for t,e in enumerate(expected[:firstdown]) if e[:2]==['INIT',pf]);assert om<formation
  after,da,al,bill,ss=run(w,spaces,capture_after=caps,purity=purity)
  assert all(eqrow(before[i],db,after[i],da) for i in range(400)) and al==bl
  dl,rr,ll=ss['late_decoded'];dp,rp,lp=sn['parent_reunion'];assert all(eqrow(rr[i],dl,rp[i],dp) and ll[i]==ci for i in ids)
  inc={r:bill['moves'].get(r,0)-basebill['moves'].get(r,0) for r in set(bill['moves'])|set(basebill['moves'])};inc={r:v for r,v in inc.items() if v};want={2:4,6:4,8:-4}
  if observer:want[3]=1
  assert inc==want and bill['peak']==29+int(observer) and bill['lifetimes']==402+int(observer)
  receipt=json.loads((a.bundle/f'kernel-{tag}/RESULT.json').read_text());assert all(bill[k]==receipt['ordinary_bill'][k] for k in ['instructions','counts','lifetimes','peak']);assert {str(k):v for k,v in bill['moves'].items()}==receipt['ordinary_bill']['moves']
  new_pairs[tag]=sorted({(e[2],e[3]) for e in expected if e[0]=='MOVE'}-{(e[2],e[3]) for e in q['program'] if e[0]=='MOVE'})
  results[tag]={'word_sha256':WORDS[tag],'bill':bill,'movement_increment':inc,'all400_rows_and_native_exit_charts_preserved':True,'early_pivot_event':em,'late_decoder_events':dec,'pure_input_functional':null,'new_chart_pairs':new_pairs[tag]}
  if observer:
   probe=copy.deepcopy(w);probe_role=next(i for i in range(400) if al[i]==127);probe['program'].insert(len(probe['program'])-1,['ADD',probe_role,temp,'1',127])
   pr,dd,pl,pb,_=run(probe,spaces)
   for i in range(400):
    target=before[i].copy()
    if i==probe_role:target=[v+(null.get(j,0)<<db) for j,v in enumerate(target)]
    assert eqrow(pr[i],dd,target,db) and pl[i]==bl[i]
   results[tag]['actual_Hub_probe_role']=probe_role;results[tag]['observer_arrival_event']=om;results[tag]['first_primal_packet_formation_event']=formation;results[tag]['probe_output_delta_is_exact_original_null']=True
 # Independently derive access geometry; no route-search or Cayley conclusion is imported.
 eligible=[i for i in s['live'] if oldspaces[s['initial'][i]]<=C];assert eligible==[7,18,27,46,77,81,87,103,111] and not(set(U)&set(eligible))
 allnorm={0}
 for j in R:allnorm|={v^s['frames'][s['initial'][j]][0] for v in tuple(allnorm)}
 assert allnorm&set(C)=={0,51} and all(s['frames'][s['initial'][j]][0].bit_count()%2 for j in s['live'])
 # Shared frozen signed-Pauli checker only; geometry/pair discovery above is independent.
 vp=a.repo/'research/shared-wire-split-composition/frozen/native_verify.py';assert sha(vp.read_bytes())=='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'
 spec=importlib.util.spec_from_file_location('bridge_kernel_frozen_phase',vp);phase=importlib.util.module_from_spec(spec);sys.modules[spec.name]=phase;spec.loader.exec_module(phase)
 maps=json.loads((a.bundle/'CHART-MAPS.json').read_text());by_pair={(m['source'],m['target']):m for m in maps['maps']};pairs=set(new_pairs['coded'])|set(new_pairs['observer']);assert len(pairs)==6 and set(by_pair)==pairs
 for ab in pairs:
  m=by_pair[ab];f,g=ww['observer']['frames'][ab[0]],ww['observer']['frames'][ab[1]];assert m['source_frame']==f and m['target_frame']==g and m['rank']==m['recipe']['rank']==len(g)-len(f)
  phase.equal(phase.recipe(m['recipe']),phase.adjoint(phase.frame(f,9))+phase.frame(g,9),'independent kernel chart map')
 bad=copy.deepcopy(by_pair[ci,127]);bad['recipe']['right']['phase']=(bad['recipe']['right']['phase']+1)%4
 try:phase.equal(phase.recipe(bad['recipe']),phase.adjoint(phase.frame(bad['source_frame'],9))+phase.frame(bad['target_frame'],9),'wrong global phase')
 except ValueError:pass
 else:raise AssertionError('wrong global phase accepted')
 # Independent controls, including an observer mutation invisible at public endpoints.
 spaces=oldspaces+[C];coded=ww['coded'];em=next(t for t,e in enumerate(coded['program']) if e==early[-1]);dec=[t for t,e in enumerate(coded['program']) if e[0]=='ADD' and e[1]==pivot and e[4]==ci]
 for name,ix in [('missing_encoder_term',40),('missing_decoder_term',dec[0])]:
  w=copy.deepcopy(coded);w['program'][ix][3]='0';rr,dd,ll,bb,_=run(w,spaces);assert any(not eqrow(rr[i],dd,before[i],db) for i in range(400));mutant_results.append({'name':name,'rejected_by':'complete400-input map'})
 w=copy.deepcopy(coded);down=next(t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[2:4]==[127,3]);pf=w['program'][down][1];w['program'].insert(down+1,['ADD',pivot,pf,packets[0]['beta'][17],3])
 try:run(w,spaces)
 except AssertionError:mutant_results.append({'name':'stale_pivot_read_at0','rejected_by':'actual cochart'})
 else:raise AssertionError('stale pivot read accepted')
 w=copy.deepcopy(ww['observer']);temp=493;copy_ix=next(t for t,e in enumerate(w['program']) if e[:3]==['ADD',temp,pivot]);w['program'][copy_ix][3]='0';om=results['observer']['observer_arrival_event']
 rr,dd,ll,bb,_=run(w,spaces);assert all(eqrow(rr[i],dd,before[i],db) for i in range(400))
 try:run(w,spaces,purity=[(temp,om,len(w['program'])-1,127,null)])
 except AssertionError:mutant_results.append({'name':'zero_observer_copy','public_map_alone_passes':True,'rejected_by':'pure original null observation'})
 else:raise AssertionError('empty observer accepted')
 # Complete conditional m3 invoice, independently recomputed from the native/main partition.
 fb=(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes();assert sha(fb)==FP;full=json.loads(fb)
 T,P=[{int(k):v for k,v in full['invoice'][t].items()} for t in ('T','P')]
 raw=collections.Counter();G=collections.Counter();dims=list(map(len,s['frames']))
 for e in s['program']:
  if e[0]=='MOVE':(raw if e[1] in roles else G)[abs(dims[e[3]]-dims[e[2]])]+=1
 H=collections.Counter(dims[s['final'][i]]-dims[s['initial'][i]] for i in range(s['public']) if i not in roles)
 assert dict(G+raw)=={int(k):v for k,v in full['native']['paid'].items()} and dict(H)=={int(k):v for k,v in full['native']['helpers'].items()}
 assert dict(raw)=={1:990,2:360,3:105,4:112,5:133,6:8,7:2}
 def root(n,k):
  v=1<<((n.bit_length()+k-1)//k)
  while True:
   z=((k-1)*v+n//v**(k-1))//k
   if z>=v:break
   v=z
  while (v+1)**k<=n:v+=1
  while v**k>n:v-=1
  assert v**k<=n<(v+1)**k
  return v
 ranks=set(T)|set(P)|set(G)|set(H)|set(raw)|set(range(1,10));grid=10**30;power={}
 for r in ranks:
  n=r**199*grid**200;v=root(n,200);power[r]=(F(v,grid),F(v+int(v**200!=n),grid))
 def bounds(profile):
  lo=hi=F(0)
  for r,c in profile.items():
   v,w=power[r];lo+=c*(v if c>=0 else w);hi+=c*(w if c>=0 else v)
  return [lo,hi]
 budget=json.loads((a.bundle/'CONDITIONAL-BUDGET.json').read_text())
 for tag,z in results.items():
  inc=bounds(z['movement_increment']);Q=z['bill']['moves'];profile={r:G.get(r,0)-H.get(r,0)+F(T.get(r,0)-P.get(r,0),12)-Q.get(r,0)+raw.get(r,0) for r in ranks};margin=bounds(profile)
  z['extra_movement_per_native_bounds']=list(map(str,inc));z['conditional_m3_margin_bounds']=list(map(str,margin));assert inc[0]>0 and margin[0]>0
  receipt=budget['kernel-'+tag]
  for ours,key in [(inc,'extra_movement_per_native_bounds'),(margin,'conditional_m3_per_rail_remaining_bounds')]:
   aa,bb=map(F,receipt[key]);assert max(ours[0],aa)<=min(ours[1],bb)
 out={'status':'PASS_INDEPENDENT_DENSE400_KERNEL_LANE_REVIEW','native_sha256':SP,'caller_invoice_sha256':FP,'author_manifest_sha256':AP,'reviewed_kernel_files':reviewed,'parent_rail_sha256':PARENT,'all_independent_input_directions':400,'parent_bill':basebill,'words':results,'all8_entry_preconditions_exactly_retained':True,'literal_forward_packet_coefficients':packets,'all_forward_packet_payloads_immutable':True,'six_actual_new_chart_pairs':sorted(pairs),'shared_phase_engine_sha256':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38','six_global_phase_recipes_pass':True,'wrong_phase_rejected':True,'common_chart_binary_basis':ww['coded']['frames'][ci],'common_chart_dimension':6,'eligible_original_X_lines':eligible,'coupled_X_lines_at_common_chart':[],'kernel_X_normal_span_intersection_common_chart':[0,51],'negative_controls':mutant_results,'scope':'Kernel-only actual partial400-input timing interface and conditional m3 invoice. Preserves parent partial map; does not complete coupledS, remove8entry calls, admit Cayley/route leads, or discharge physical all-width/owned/compiler obligations.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','all_independent_input_directions','common_chart_dimension','eligible_original_X_lines','six_global_phase_recipes_pass','negative_controls']},indent=2));print(json.dumps({t:{k:z[k] for k in ['bill','movement_increment','extra_movement_per_native_bounds','conditional_m3_margin_bounds']} for t,z in results.items()},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
