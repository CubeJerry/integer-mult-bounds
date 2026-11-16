"""Five genuine unknown modes with native shared proper correction caches."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
PIN='27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd'
PLAN=[['P0','KEEP_C0',35,'D3_21',[3,21]],['P1','KEEP_C1',110,'D76_64',[76,64]],['P2','KEEP_C2',93,'D80_65',[80,65]],['P3','ZFIRST3',96,'F4',[4]],['P5','ZFIRST5',97,'F78',[78]]]
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(p,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();p.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--bits',default='11111');a=ap.parse_args();path=a.repo/'research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json';raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','shared_proper_engine');t=load(Path(__file__).with_name('build_d4_cohort.py'),'shared_proper_trace');pr=load(Path(__file__).with_name('price_d4_cohort.py'),'shared_proper_price');C,_,before=e.replay(w,R);bt=t.trace(w['operations']);assert len(a.bits)==5 and set(a.bits)<={'0','1'};bits=list(map(int,a.bits));D={z[2]for z in PLAN};names={f'X{i}'for i in D};mask=sum(1<<i for i in D);assert D.isdisjoint(w['targets']);assert not any(o[0]=='ADD'and o[2]in names for o in w['operations']);assert not any(o[0]=='ADD'and o[1].startswith('Y')for o in w['operations']);ops=[];caches=[]
 def add(*rows):ops.extend([list(o)for o in rows])
 for j,(p,f,i,loc,ys)in enumerate(PLAN):
  assert e.sub(C[f'L{i}'],C[loc]);assert all(e.sub(C[loc],C[f'F{k}'])for k in ys);cache=f'SHARED_PROPER_RAW_{i}';caches.append(cache);add(('MOVE',f'X{i}',loc),('INIT',cache,loc),('ADD',f'X{i}',cache),('MOVE',f'X{i}','Hub'))
 prelude=len(ops);mapping={};programs=[];corrections=[];clear=[];closure=[]
 firstfields={z[1]for z in PLAN};resets={p:w['operations'].index(['ADD',f,p])for p,f,i,l,ys in PLAN}
 for p,f,i,loc,ys in PLAN:
  readers=[o[2]for o in w['operations']if o[0]=='ADD'and o[1]==f and o[2]!=p];assert readers==[f'Y{k}'for k in ys],(f,readers)
  assert[o for o in w['operations'][:resets[p]]if o[0]=='ADD'and o[1]==p]==[['ADD',p,f]],(p,'unrepaired pre-reset packet observer')
 for k,o in enumerate(w['operations']):
  typ,n,*q=o
  if typ=='CLEAR':clear.append(o);mapping[k]=len(ops);continue
  if typ=='MOVE'and n.startswith('Y')and int(n[1:])not in w['targets']:closure.append(o);mapping[k]=len(ops);continue
  if(typ=='MOVE'and n in names)or(typ=='ADD'and n in names):mapping[k]=len(ops);continue
  oo=o.copy()
  for j,(p,f,i,loc,ys)in enumerate(PLAN):
   if typ=='MOVE'and n==p and bt[k][1][p]=='Hub':
    if bits[j]:programs.append(len(ops));add(('ADD',f'X{i}',p))
   if typ=='MOVE'and n in{f'Y{k}'for k in ys}and q[0]==f'F{n[1:]}':
    if loc!=q[0]:add(('MOVE',n,loc));assert e.sub(C[bt[k][1][n]],C[loc])
    if bits[j]and loc!=q[0]:corrections.append(len(ops));add(('ADD',caches[j],n))
  add(oo)
  for j,(p,f,i,loc,ys)in enumerate(PLAN):
   if typ=='MOVE'and n in{f'Y{k}'for k in ys}and q[0]==f'F{n[1:]}'and loc==q[0]and bits[j]:corrections.append(len(ops));add(('ADD',caches[j],n))
  mapping[k]=len(ops)
 cut=len(ops);add(*closure,*clear,*[('CLEAR',n)for n in caches]);nw=copy.deepcopy(w);nw.update(schema='five-shared-native-proper-corrections-v1',base_word_sha256=PIN,operations=ops,carrier_interface_before_operation=cut,released_carriers=[],shared_proper_masks={'plan':PLAN,'bits':bits,'prelude_end':prelude,'source_add_indices':programs,'correction_add_indices':corrections,'continuation_before_operation':cut},scope='Same46 completed outputs; five independent unknown directions on an unfinished nonorthogonal seven-clique are retained nonlocally using actual native original routes and five shared proper raw caches. Six old receivers share three rank6 correction caches. No added owned MOVE. All65 unfinished Y stay rawground. No all111 supplier or kappa.')
 CC,_,after=e.replay(nw,R);nt=t.trace(ops);v,at=nt[cut]
 for i in range(111):
  assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
  if i not in w['targets']:assert v[f'Y{i}']==1<<(111+i)and at[f'Y{i}']=='zero'
 for j,(p,f,i,loc,ys)in enumerate(PLAN):
  oldlast=next(z for z in reversed(bt)if f in z[0]);expected=(oldlast[0][f]&~mask)^((1<<i)if bits[j]else 0);assert v[f]==expected and v[caches[j]]==1<<i
 # Covariance outside the five changing packet segments, their retentions and corrected outputs.
 affectedY={f'Y{i}'for z in PLAN for i in z[4]};comp=0
 for k,o in enumerate(w['operations']):
  if o[0]=='CLEAR':continue
  ov,oa=bt[k+1];vv,aa=nt[mapping[k]]
  for n,z in ov.items():
   if n in names|firstfields|affectedY or(n in resets and k<resets[n]):continue
   if n.startswith('Y')and int(n[1:])not in w['targets']:continue
   assert n in vv and vv[n]==z&~mask,(k,o,n,hex(vv.get(n,0)),hex(z&~mask));assert CC[aa[n]]==C[oa[n]],(k,n,'chart');comp+=1
 born={o[1]for o in ops if o[0]=='INIT'};owned={n:z for n,z in v.items()if n in born};J=[5,35,93,96,97,109,110];jm=sum(1<<i for i in J);assert all(sum(x*y for x,y in zip(R[i],R[k]))!=0 for i in J for k in J if i!=k);nonlocal_rows=[];certificate=[]
 for n,z in owned.items():
  local=sum(1<<i for i in J if e.sub(C[f'L{i}'],CC[at[n]]));row=z&jm&~local
  if row:nonlocal_rows.append(row);certificate.append({'owner':n,'chart':at[n],'row_hex':hex(row),'clique_support':[i for i in J if row>>i&1]})
 if all(bits):assert len(e.bb(nonlocal_rows))==5
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 lim=tuple(z/6 for z in pr.moment(gate));q=pr.moment(after['movement_profile']);qo=pr.moment(before['movement_profile']);a.out.mkdir(parents=True,exist_ok=True);sha=write(a.out/'WORD.json',nw);res={'status':'PASS_FIVE_ACTUAL_SHARED_PROPER_UNKNOWN_MODES','word_sha256':sha,'base_word_sha256':PIN,'before':before,'after':after,'all_targets':nw['targets'],'interface':cut,'plan':PLAN,'parameter_bits':bits,'clique':J,'clique_nonlocal_projection_rank':len(e.bb(nonlocal_rows)),'clique_nonlocal_certificate':certificate,'unaffected_projected_states':comp,'owned_move_increment':sum(o[0]=='MOVE'and o[1]in born for o in ops)-sum(o[0]=='MOVE'and o[1]in{p[1]for p in w['operations']if p[0]=='INIT'}for o in w['operations']),'whole_moment':pr.record(q),'moment_increment':pr.record((q[0]-qo[1],q[1]-qo[0])),'necessary_limiting_room':pr.record((lim[0]-q[1],lim[1]-q[0])),'scope':nw['scope']};write(a.out/'RESULT.json',res);print(json.dumps({k:res[k]for k in['status','word_sha256','after','clique_nonlocal_projection_rank','owned_move_increment','whole_moment','necessary_limiting_room']}))
if __name__=='__main__':main()
