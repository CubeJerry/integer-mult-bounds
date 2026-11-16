#!/usr/bin/env python3
"""Acquire two canonical directions while preserving active fitting rows and full W15 history."""
from pathlib import Path
from collections import Counter
import argparse,json,hashlib,copy

def rank(rows):
 B={}
 for v in rows:
  while v:
   q=v.bit_length()-1
   if q in B:v^=B[q]
   else:B[q]=v;break
 return len(B)
def solve(rows,v):
 B={}
 for j,r in enumerate(rows):
  c=1<<j
  while r:
   q=r.bit_length()-1
   if q in B:r^=B[q][0];c^=B[q][1]
   else:B[q]=(r,c);break
 c=0
 while v:
  q=v.bit_length()-1;assert q in B;v^=B[q][0];c^=B[q][1]
 return c
def combination(rows,c):
 v=0
 for j,r in enumerate(rows):
  if c>>j&1:v^=r
 return v

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);ap.add_argument('--filters',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();br=a.base.read_bytes();fr=a.filters.read_bytes();assert hashlib.sha256(br).hexdigest()=='ad5ee926df808054a05bff8b2db5f2eb4c70e6e4713f1419fcf02a211eb14f64';assert hashlib.sha256(fr).hexdigest()=='a82d3f9283fb770377981b9f20b384639aaf135dbdc0046db4852f7f0df6f46d';base=json.loads(br);old=json.loads(fr);charts=copy.deepcopy(base['charts']);R=json.loads((a.repo/base['source_path']).read_text())['native_roots'];design=json.loads(Path(__file__).with_name('DESIGN.json').read_text());charts['Extra6']={'kind':'span','rows':[R[j]for j in design['expanded_extra_group']]};fields=copy.deepcopy(old['history_cache_metadata']);groups=copy.deepcopy(old['history_groups']);qmask=sum(1<<f['new_receiver']for f in base['forks'])
 for g in groups:
  if g['h']==0 and len(g['receivers'])==1:g['chart']=next(f['chart']for f in base['forks']if f['old_receiver']==g['receivers'][0])
 groups[-1]['roles']=design['expanded_extra_group'];groups[-1]['chart']='Extra6'
 for c in fields:c['chart']=groups[c['group']]['chart'];assert int(c['row_hex'],16)&qmask==0
 for z,gg in enumerate(groups):
  basis=[int(c['row_hex'],16)for c in fields if c['group']==z]
  for k,vr in enumerate(design['displaced_rows_hex']):
   v=int(vr,16)&sum(1<<j for j in gg['roles'])
   if rank(basis+[v])>rank(basis):
    fields.append({'name':f'Hnew{z}_{k}','group':z,'chart':gg['chart'],'row_hex':hex(v),'roles':[j for j in gg['roles']if v>>j&1]});basis.append(v)
 assert len(fields)==52

 pair=lambda ii:next(q['chart']for q in base['cache_metadata']if q['family']==1 and q['receivers']==ii)
 routes=[[f"F{f['old_receiver']}",f['chart'],'M0','zero']for f in base['forks']]+[['F4',pair([4,74]),'M1','zero'],['F74',pair([74,78]),'M1','zero'],['F78',pair([4,78]),'M1','zero'],['Extra6','zero'],['zero']]
 import sympy as sp
 def equal(x,y):
  c,d=charts[x],charts[y];M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);N=sp.Matrix(d['rows'])if d['rows']else sp.zeros(0,8);B=M.rowspace()if c['kind']=='span'else M.nullspace();C=N.rowspace()if d['kind']=='span'else N.nullspace();return len(B)==len(C)and sp.Matrix([list(v)for v in B+C]).rank()==len(B)
 for c in fields:
  hits=[(p,ch)for p,route in enumerate(routes)for ch in route if equal(c['chart'],ch)];assert hits;c['packet'],c['read_chart']=hits[0]
 val={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j)for j in range(111)};loc={f'X{j}':f'L{j}'for j in range(111)}|{f'Y{j}':'zero'for j in range(111)};ops=[]
 def emit(o):
  ops.append(o);op,n,*q=o
  if op=='INIT':val[n]=0;loc[n]=q[0]
  elif op=='MOVE':loc[n]=q[0]
  elif op=='ADD':val[q[0]]^=val[n]
  elif op=='CLEAR':del val[n],loc[n]
 for c in fields:emit(['INIT',c['name'],c['chart']])
 extra=design['expanded_extra_group']
 for o in base['operations'][:base['milestones']['source_cut']]:
  if o[0]=='MOVE'and o[1].startswith('X'):
   j=int(o[1][1:])
   if j in extra and o[2]=='Hub':
    emit(['MOVE',o[1],'Extra6'])
    for c in fields:
     if j in c['roles']:emit(['ADD',o[1],c['name']])
    emit(o);continue
   emit(o)
   if o[2]!='Hub':
    for c in fields:
     if j in c['roles']and equal(o[2],c['chart']):emit(['ADD',o[1],c['name']])
  else:emit(o)
 for c in fields:assert val[c['name']]==int(c['row_hex'],16),c
 marks={'source_cut':len(ops)};names=base['source_basis_names'];B=[val[n]for n in names];assert rank(B)==111;original=[int(v,16)for v in design['active_rows_hex']]+[int(v,16)for v in design['best_candidates'][0]['g_hex']];allrows=[combination(original,c)for c in range(256)];project=lambda v:solve(B,v)>>(len(B)-3);S=[]
 for z in range(3):S.append(next(v for v in allrows if project(v)==1<<z))
 for v in allrows:
  if project(v)==0 and rank(S+[v])>rank(S):S.append(v)
 assert len(S)==8 and rank(S+original)==8;seed=[];reads=[]
 for z,s in enumerate(S):
  ff=[c for c in fields if c['packet']==z];q=0
  for c in ff:q^=int(c['row_hex'],16)
  co=solve(B,s^q);hub=[n for k,n in enumerate(names)if co>>k&1 and n.startswith('X')and loc[n]=='Hub'];early=[n for k,n in enumerate(names)if co>>k&1 and n.startswith('E')];query=[n for k,n in enumerate(names)if co>>k&1 and n.startswith('X')and loc[n]!='Hub'];assert query==([f"X{base['forks'][z]['new_receiver']}"]if z<3 else[]);emit(['INIT',f'P{z}','Hub'])
  for n in hub:emit(['ADD',n,f'P{z}'])
  for ch in routes[z]:
   emit(['MOVE',f'P{z}',ch])
   for n in query:
    if equal(loc[n],ch):emit(['ADD',n,f'P{z}'])
   for c in ff:
    if c['read_chart']==ch:emit(['ADD',c['name'],f'P{z}']);reads.append({'step':len(ops),'packet':f'P{z}','cache':c['name'],'chart':ch,'row_hex':c['row_hex']})
  for n in early:emit(['ADD',n,f'P{z}'])
  assert val[f'P{z}']==s;seed.append({'field':f'P{z}','row_hex':hex(s),'compensated_row_hex':hex(s^q),'query_sum_hex':hex(q),'Hub_reads':hub,'early_point_reads':early,'held_query':query,'route':routes[z]})
 marks['seed8_before_Y']=len(ops);done=set();dot=lambda x,y:sum(a*b for a,b in zip(x,y));h=base['singular_h'];A=[sum(1<<j for j in range(111)if h[i]==h[j]and(i==j or dot(R[i],R[j])==0))for i in range(111)]
 for step,o in enumerate(base['operations'][base['milestones']['seed8_before_Y']:],base['milestones']['seed8_before_Y']+1):
  if o[0]=='ADD'and o[1].startswith('P')and o[2].startswith('Y'):
   i=int(o[2][1:])
   if i not in done:
    cc=solve(S,A[i]);done.add(i)
    for z in range(8):
     if cc>>z&1:emit(['ADD',f'P{z}',f'Y{i}'])
  else:emit(o)
  for k,v in base['milestones'].items():
   if v==step:marks[k]=len(ops)
 for c in fields:emit(['CLEAR',c['name']])
 out=copy.deepcopy(base);out.update({'schema':'actual-canonical-history-fifteen-v1','base_fifteen_word_sha256':hashlib.sha256(br).hexdigest(),'filter_history_word_sha256':hashlib.sha256(fr).hexdigest(),'charts':charts,'operations':ops,'milestones':marks,'ground_code':'active S6 plus two canonical C9 rows','canonical_innovations_hex':design['best_candidates'][0]['g_hex'],'displaced_seed_rows_hex':design['displaced_rows_hex'],'seed_rows_hex':[hex(v)for v in S],'history_omitted_roles':[j for j in old['history_omitted_roles']if j!=8],'history_extra_query_roles':extra,'history_groups':groups,'history_cache_metadata':fields,'history_quotient_representatives_hex':old['history_quotient_representatives_hex'],'principal_query_reads':reads,'seed_metadata':seed,'principal_routes':routes,'history_claim':'Full W15 and canonical C9 are represented in actual non-Hub principal histories; active S6 and two canonical innovations are the eight final ground rows. Receiver access is separate.'});a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json').write_text(json.dumps(out,indent=2)+'\n');print('counts',dict(Counter(o[0]for o in ops)),'filtered owners',len(fields),'source basis rank',rank(B))
if __name__=='__main__':main()
