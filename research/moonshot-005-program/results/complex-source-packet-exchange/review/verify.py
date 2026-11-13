"""Independent full400 source/interface and structural m3 exchange review."""
import argparse,collections,copy,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from dense_engine import run,span,eqrow
if not __debug__:raise SystemExit("Exact checks require Python without -O")
PINS={'native': '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883', 'caller': 'd9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7', 'parent': 'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc', 'manifest': '380cbe7bf7658504495e99fa06793b22e5bb9544b10a7d4c819d8227564cb4e5', 'word': 'cb77301a8f402fcc0f8dc069faefa0f0b3c6dfaedb6122a5a7d65b04802e2514', 'm3': 'ff2d8c5ad32ea2d2cc7a6cd6c408eac517546009ef9c63e91970dd649dc73d27'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p,pin):
 b=p.read_bytes();assert sha(b)==pin,(str(p),sha(b));return json.loads(gzip.decompress(b))
def rank(rows):
 basis={}
 for row in rows:
  d={i:F(v) for i,v in enumerate(row) if v}
  while d:
   p=min(d)
   if p not in basis:
    c=d[p];basis[p]={i:v/c for i,v in d.items()};break
   c=d[p]
   for i,v in basis[p].items():
    w=d.get(i,F(0))-c*v
    if w:d[i]=w
    elif i in d:del d[i]
 return len(basis)
def integer_root(n,k):
 v=1<<((n.bit_length()+k-1)//k)
 while True:
  z=((k-1)*v+n//v**(k-1))//k
  if z>=v:break
  v=z
 while (v+1)**k<=n:v+=1
 while v**k>n:v-=1
 assert v**k<=n<(v+1)**k
 return v
def main(a):
 mb=(a.bundle/'MANIFEST.json').read_bytes();assert sha(mb)==PINS['manifest'];man=json.loads(mb)
 for e in man['files']:assert sha((a.bundle/e['path']).read_bytes())==e['sha256']
 s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',PINS['native']);q=load(a.bundle/'source-evidence/rail-consumer.json.gz',PINS['parent']);w=load(a.bundle/'output/rail-exchange.json.gz',PINS['word']);m3=load(a.bundle/'m3/WORD.json.gz',PINS['m3'])
 receipt=json.loads((a.bundle/'output/RESULT.json').read_text());mr=json.loads((a.bundle/'m3/RESULT.json').read_text());roles={int(k):v for k,v in q['source_role_map'].items()};rev={v:k for k,v in roles.items()}
 assert sorted(rev)==list(range(400)) and all(w[k]==q[k] for k in ['initial','frames','source_role_map']);spaces=list(map(span,w['frames']));live=s['live'];DP={live[k] for k in s['hosted']['Dports']};U=sorted(set(live)-DP)
 host={live[k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};dual={roles[j] for pair in host.values() for j in pair};assert len(dual)==192
 # Independent lifetime graph + breadth-first components, not author's union/find.
 graph=collections.defaultdict(set);current={i:i for i in range(400)};nodes=[];nn=400
 for e in q['program']:
  op,r=e[:2]
  if op=='INIT':assert r not in current;current[r]=nn;nn+=1
  node=current[r];nodes.append(node)
  if op in ('ADD','COPY'):other=current[e[2]];graph[node].add(other);graph[other].add(node)
  if op=='CLEAR':del current[r]
 tag={};components=[]
 for start in range(nn):
  if start in tag:continue
  seen={start};queue=collections.deque([start])
  while queue:
   for v in graph[queue.popleft()]:
    if v not in seen:seen.add(v);queue.append(v)
  colors={'D' if v in dual else 'P' for v in seen if v<400};assert len(colors)<=1;color=next(iter(colors),'P')
  for v in seen:tag[v]=color
  components.append({'nodes':len(seen),'public':len([v for v in seen if v<400]),'color':color})
 P=[(k,e) for k,e in enumerate(q['program']) if tag[nodes[k]]=='P'];D=[(k,e) for k,e in enumerate(q['program']) if tag[nodes[k]]=='D']
 begin=next(k for k,e in P if e==['INIT',451,127]);down=next(k for k,e in P if k>begin and e==['MOVE',451,127,3,True]);end=next(k for k,e in P if k>down and e==['CLEAR',451,3])
 bt,bo=next((k,e) for k,e in D if e[0]=='MOVE' and e[1]<400 and e[3]==127 and len(q['frames'][e[2]])==8);carrier,facet=bo[1],bo[2];assert (begin,down,end,bt,carrier,facet)==(3462,3528,3594,578,209,132)
 def rename(e):
  z=e.copy()
  if z[1]>=400:z[1]+=q['owned_fields']
  if z[0] in ('ADD','COPY') and z[2]>=400:z[2]+=q['owned_fields']
  return z
 cache=400+2*q['owned_fields'];expected=[e for k,e in P if k<begin]+[rename(e) for k,e in D if k<bt];encoder_begin=len(expected)
 expected += [e for k,e in P if begin<=k<down];expected += [['INIT',cache,127],['ADD',cache,451,'1',127]];exchange_begin=len(expected)
 expected += [['MOVE',451,127,facet,True],['ADD',carrier,451,'1',facet],['ADD',451,carrier,'-1',facet],bo];restore= len(expected)
 expected += [['ADD',carrier,cache,'-1',127],['CLEAR',cache,127],['MOVE',451,facet,3,True]]
 expected += [e for k,e in P if k>down]+[rename(e) for k,e in D if k>bt]
 assert w['program']==expected and w['owned_fields']==2*q['owned_fields']+1
 print('Independent full400 parent/exchange replay with causal snapshots',flush=True)
 old,do,lo,oldbill,_=run(q,spaces)
 new,dn,ln,bill,sn=run(w,spaces,capture_before={encoder_begin:('donors_ready',[roles[j] for j in live]+[carrier]),exchange_begin:('before_exchange',[451,carrier,cache])},capture_after={exchange_begin+2:('exchanged',[451,carrier]),restore:('restored_B',[carrier]),restore+2:('packet_at0',[451])})
 assert ln==lo=={i:s['final'][rev[i]] for i in range(400)}
 dd,rd,ld=sn['donors_ready']
 for j in live:assert ld[roles[j]]==127 and eqrow(rd[roles[j]],dd,old[roles[j]],do)
 assert ld[carrier]==facet
 ds,rs,ls=sn['before_exchange'];h=rs[carrier];p0=rs[451];assert ls=={451:127,carrier:facet,cache:127} and rs[cache]==p0 and any(h) and any(p0)
 assert eqrow(rd[carrier],dd,h,ds)
 # Reconstruct original funded encoder on the genuinely ready current donors.
 enc=[0]*400
 for e in q['program'][begin+1:down]:
  assert e[0]=='ADD' and e[1]==451 and e[2] in [roles[j] for j in live] and e[4]==127;c=F(e[3]);enc=[x+c*y for x,y in zip(enc,rd[e[2]])]
 assert all(F(v,dd)==F(t,ds) for v,t in zip(enc,p0))
 de,re,le=sn['exchanged'];assert le=={451:facet,carrier:facet}
 assert eqrow(re[451],de,[-v for v in h],ds) and eqrow(re[carrier],de,[x+y for x,y in zip(h,p0)],ds)
 dr,rr,lr=sn['restored_B'];assert lr[carrier]==127 and eqrow(rr[carrier],dr,h,ds)
 dz,rz,lz=sn['packet_at0'];assert lz[451]==3 and eqrow(rz[451],dz,[-v for v in h],ds)
 old={i:[F(v,do) for v in row] for i,row in old.items()};new={i:[F(v,dn) for v in row] for i,row in new.items()};hh=[F(v,ds) for v in h];pp=[F(v,ds) for v in p0];shift=[-x-y for x,y in zip(hh,pp)]
 beta=collections.defaultdict(F)
 for e in q['program'][down+1:end]:assert e[0]=='ADD' and e[2]==451 and e[4]==3;beta[e[1]]+=F(e[3])
 for i in range(400):assert new[i]==[x+beta[i]*d for x,d in zip(old[i],shift)]
 frozen={roles[j] for j in live}|dual
 assert all(new[i]==old[i] for i in frozen)
 # Verify the explicit inverse expression using independently replayed unchanged outputs.
 expr={int(k):F(v) for k,v in receipt['output_shear_inverse_expression_on_unchanged_outputs'].items()};assert set(expr)<=frozen
 assert [sum(c*new[i][j] for i,c in expr.items()) for j in range(400)]==shift
 assert {k:F(v,ds) for k,v in enumerate(h) if v}=={int(k):F(v) for k,v in receipt['actual_B_facet_row'].items()}
 assert {k:F(v,ds) for k,v in enumerate(p0) if v}=={int(k):F(v) for k,v in receipt['actual_old_P0'].items()}
 assert tuple(F(s['hosted'][k]) for k in ['alpha','beta','alpha2','beta2'])==(F(-1),F(1,2),F(-1),F(0))
 olderrs={};newerrs={};completed=[]
 for j in live:
  ideal=[F(0)]*400;ideal[roles[j]]=ideal[roles[j+112]]=F(1,2) if j in U else F(1)
  olderrs[j]=[x-y for x,y in zip(old[roles[j+112]],ideal)];newerrs[j]=[x-y for x,y in zip(new[roles[j+112]],ideal)]
  if not any(newerrs[j]):completed.append(j)
 counts=[sum(sum(bool(x) for x in r) for r in errors.values()) for errors in [olderrs,newerrs]];assert counts==[4920,7470]
 reverse=[];host_complete=[]
 for j,(b,d) in host.items():
  er=new[roles[b]].copy();er[roles[b]]-=1;er[roles[d]]+=1;reverse.append(er)
  if not any(er):host_complete.append(j)
 assert rank(reverse)==58 and len(host_complete)==24
 for j in U:assert new[roles[j]]==[F(int(k==roles[j])-int(k==roles[j+112])) for k in range(400)]
 for i in range(400):assert [e for e in expected if e[0]=='MOVE' and e[1]==i]==[e for e in q['program'] if e[0]=='MOVE' and e[1]==i]
 assert all(bill[k]==receipt['bill'][k] for k in ['instructions','counts','lifetimes','peak']) and {str(k):v for k,v in bill['moves'].items()}==receipt['bill']['moves']
 inc={k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in set(bill['counts'])|set(oldbill['counts'])};mi={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in set(bill['moves'])|set(oldbill['moves'])};mi={k:v for k,v in mi.items() if v};assert mi=={1:1,8:1,9:-1} and inc=={'ADD':4,'CLEAR':1,'INIT':1,'MOVE':1,'SCALE':0}
 oldpairs={(e[2],e[3]) for e in q['program'] if e[0]=='MOVE'};pairs={(e[2],e[3]) for e in expected if e[0]=='MOVE'}-oldpairs;assert pairs=={(127,132),(132,3)}
 import importlib.util,sys
 vp=a.repo/'research/shared-wire-split-composition/frozen/native_verify.py';assert sha(vp.read_bytes())=='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38';spec=importlib.util.spec_from_file_location('bridge_exchange_phase',vp);phase=importlib.util.module_from_spec(spec);sys.modules[spec.name]=phase;spec.loader.exec_module(phase)
 maps=json.loads((a.bundle/'CHART-MAPS.json').read_text());by_pair={(m['source'],m['target']):m for m in maps['maps']};assert set(by_pair)==pairs
 for aa,bb in pairs:
  m=by_pair[aa,bb];f,g=w['frames'][aa],w['frames'][bb];assert m['source_frame']==f and m['target_frame']==g and m['rank']==m['recipe']['rank']==abs(len(g)-len(f));phase.equal(phase.recipe(m['recipe']),phase.adjoint(phase.frame(f,9))+phase.frame(g,9),'independent complex exchange map')
 bad=copy.deepcopy(next(iter(by_pair.values())));bad['recipe']['right']['phase']=(bad['recipe']['right']['phase']+1)%4
 try:phase.equal(phase.recipe(bad['recipe']),phase.adjoint(phase.frame(bad['source_frame'],9))+phase.frame(bad['target_frame'],9),'wrong phase')
 except ValueError:pass
 else:raise AssertionError('wrong phase accepted')
 controls=[]
 for name,ix,value in [('wrong_complex_exchange_sign',exchange_begin+2,'1'),('missing_Hub_restore',restore,'0')]:
  bad=copy.deepcopy(w);bad['program'][ix][3]=value;br,bd,bl,bb,_=run(bad,spaces);assert any([F(v,bd) for v in br[i]]!=new[i] for i in range(400));controls.append({'name':name,'event':ix,'rejected_by':'complete400 original-input map'})
 # Stale old-P0 interpretation is directly rejected by the actual payload.
 assert [-x for x in hh]!=pp
 # Literal block composition: no claimed independent2280 coefficient replay.
 p=2280;expected=[];blocks=[]
 def mapped(e,public,mapfield):
  z=e.copy();z[1]=mapfield(z[1]) if z[1]<public else p+z[1]-public
  if z[0] in ('ADD','COPY'):z[2]=mapfield(z[2]) if z[2]<public else p+z[2]-public
  return z
 for j in range(2):
  bank=lambda i:1480+400*j+i
  start=len(expected);expected += [['ADD',bank(i),rev[i],'-1',q['initial'][i]] for i in range(400)]
  expected += [mapped(e,400,bank) for e in w['program']];blocks.append({'copy':j+1,'start':start,'stop':len(expected)})
 start=len(expected);expected += [mapped(e,1480,lambda i:i) for e in s['program']];common=[start,len(expected)]
 for j in range(2):expected += [['ADD',1480+400*j+i,rev[i],'1',s['final'][rev[i]]] for i in range(400)]
 assert m3['program']==expected and m3['public']==2280 and m3['owned_fields']==max(s['owned_fields'],w['owned_fields'])
 assert m3['initial']==s['initial']+w['initial']*2 and m3['frames']==w['frames'] and m3['private_blocks']==blocks and m3['common_block']==common
 # Separate schedule-only replay checks all2280 physical charts and lifetimes.
 loc=dict(enumerate(m3['initial']));mc=collections.Counter();mm=collections.Counter();life=peak=0
 for e in expected:
  op,i=e[:2];mc[op]+=1;assert 0<=i<2280+m3['owned_fields']
  if op=='INIT':assert i>=2280 and i not in loc;loc[i]=e[2];life+=1
  elif op=='CLEAR':assert i>=2280 and loc[i]==e[2];del loc[i]
  elif op=='MOVE':
   aa,bb,owned=e[2:];assert loc[i]==aa and owned==(i>=2280) and (spaces[aa]<spaces[bb] or owned and spaces[bb]<spaces[aa]);mm[abs(len(m3['frames'][bb])-len(m3['frames'][aa]))]+=1;loc[i]=bb
  elif op in ('ADD','COPY'):assert loc[i]==loc[e[2]]==e[4]
  elif op=='SCALE':assert loc[i]==e[3] and F(e[2])
  else:raise AssertionError(op)
  peak=max(peak,len(loc)-2280)
 assert set(loc)==set(range(2280)) and all(loc[i]==s['final'][i] for i in range(1480))
 assert all(loc[1480+400*j+i]==ln[i] for j in range(2) for i in range(400))
 mbill={'instructions':len(expected),'counts':dict(mc),'moves':dict(sorted(mm.items())),'lifetimes':life,'peak':peak}
 assert all(mbill[k]==mr['ordinary_bill'][k] for k in ['instructions','counts','lifetimes','peak']) and {str(k):v for k,v in mm.items()}==mr['ordinary_bill']['moves']
 fb=(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes();assert sha(fb)==PINS['caller'];full=json.loads(fb)
 T,P=[{int(k):v for k,v in full['invoice'][name].items()} for name in ['T','P']]
 raw=collections.Counter();Gh=collections.Counter();dims=list(map(len,s['frames']))
 for e in s['program']:
  if e[0]=='MOVE':(raw if e[1] in roles else Gh)[abs(dims[e[2]]-dims[e[3]])]+=1
 Hh=collections.Counter(dims[s['final'][i]]-dims[s['initial'][i]] for i in range(1480) if i not in roles)
 assert raw=={1:990,2:360,3:105,4:112,5:133,6:8,7:2}
 assert {str(k):v for k,v in (raw+Gh).items()}==full['native']['paid'] and {str(k):v for k,v in Hh.items()}==full['native']['helpers']
 rr=set(T)|set(P)|set(Gh)|set(Hh)|set(raw)|set(bill['moves'])
 tm={r:3*T.get(r,0)-36*Hh.get(r,0) for r in rr};pm={r:3*P.get(r,0)-36*Gh.get(r,0)+36*(bill['moves'].get(r,0)-raw.get(r,0)) for r in rr}
 for r in rr:assert pm[r]==3*(P.get(r,0)-18*(raw+Gh).get(r,0))+18*mm.get(r,0)
 assert all(tm.get(r,0)==int(mr['T'].get(str(r),0)) and pm.get(r,0)==int(mr['P'].get(str(r),0)) for r in rr)
 assert sum(tm.values())==31296 and sum(pm.values())==155952 and sum(r*(tm[r]-pm[r]) for r in rr)==4380
 grid=10**30;powers={}
 for r in rr:
  n=r**199*grid**200;v0=integer_root(n,200);powers[r]=(F(v0,grid),F(v0+int(v0**200!=n),grid))
 def bounds(profile):
  lo=hi=F(0)
  for r,c in profile.items():
   aa,bb=powers[r];lo+=c*(aa if c>=0 else bb);hi+=c*(bb if c>=0 else aa)
  return [lo,hi]
 margin=bounds({r:F(tm[r]-pm[r],36) for r in rr});assert margin[0]>0
 aa,bb=map(F,mr['per_rail_moment_bounds']);assert max(aa,margin[0])<=min(bb,margin[1])
 extra=bounds(mi);assert extra[0]>0 and extra[1]<F('0.015587213772120')
 out={'status':'PASS_INDEPENDENT_DENSE400_COMPLEX_EXCHANGE_AND_STRUCTURAL_M3','pins':PINS,'all400_original_coefficients_replayed':True,'full2280_coefficient_replay':False,'all2280_chart_schedule_checked':True,'independent_bank_partition':'Lifetime dependency graph, breadth-first connected components; no author union/find imported','bank_components':components,'original_boundaries':{'encoder_begin':begin,'packet_down':down,'packet_clear':end,'carrier_old_move':bt},'actual_events':{'encoder_begin':encoder_begin,'exchange_begin':exchange_begin,'carrier_restore':restore},'all104_current_X_donors_ready_atHub':True,'carrier':carrier,'facet':facet,'controller_cache':cache,'actual_facet_h':{j:str(v) for j,v in enumerate(hh) if v},'actual_old_P0':{j:str(v) for j,v in enumerate(pp) if v},'actual_ground_packet':'-h, not P0','local_scatter':[[1,1],[-1,0]],'local_determinant':1,'packet_through':0,'carrier_restored_before_dual_suffix':True,'all_X_B_D_rows_exact_parent':True,'output_change':'beta*(-h-P0) only on firstY rows','verified_inverse_expression_on_unchanged_outputs':{i:str(v) for i,v in expr.items()},'inverse_is_information_only':True,'forward_original_term_counts':{'old':4920,'new':7470},'completed_firstY_ports':completed,'hosted_reverse_rank':58,'hosted_completed_ports':host_complete,'coupled_reverse_completed_ports':U,'all_original_raw_MOVE_sequences_retained':True,'parent_bill':oldbill,'bill':bill,'ordinary_increment':inc,'move_increment':mi,'extra_movement_bounds':list(map(str,extra)),'new_chart_pairs':sorted(pairs),'both_phase_maps_pass':True,'wrong_phase_rejected':True,'negative_controls':controls,'m3_bill':mbill,'T_m3':tm,'P_m3':pm,'perrail_m3_margin_bounds':list(map(str,margin)),'perrail_m3_margin_decimal':float(margin[0]),'m3_symbolic_formula':'common=Wu; private_j=pi*Wu+L_exchange*(v_j-pi*u)','scope':'Actual funded singular handoff and changed forward map. Complete oldGram delivery, forward targets, new decoder/cross actions, compiler and strict suppliers remain open. Shared premises: pinned native endpoint/caller, fixed-m theorem, our independent dense engine and frozen phase checker.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','bill','move_increment','actual_facet_h','completed_firstY_ports','hosted_reverse_rank','perrail_m3_margin_decimal','extra_movement_bounds','negative_controls']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
