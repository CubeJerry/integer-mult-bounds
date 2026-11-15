#!/usr/bin/env python3
"""Author check of conditional two-lane semantics, not retained compiler admission."""
import argparse,hashlib,json,copy
from pathlib import Path
from collections import Counter
from functools import lru_cache
import sympy as sp
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def basis(rows):
 B={}
 for j,r in enumerate(rows):
  tag=1<<j
  while r:
   p=r.bit_length()-1
   if p in B:r^=B[p][0];tag^=B[p][1]
   else:B[p]=(r,tag);break
 return B
def solve(B,r):
 tag=0
 while r:
  p=r.bit_length()-1
  if p not in B:return None
  r^=B[p][0];tag^=B[p][1]
 return tag
def chart(c):
 M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);rows=M.rowspace()if c['kind']=='span'else M.nullspace()
 return tuple(tuple(v)for v in rows)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def collapsed(r):return sum(1<<i for i in range(222)if ((r>>(2*i))&3).bit_count()%2)
def replay(w,R):
 need(w['record_lanes']==2 and w['retained_compiler_admitted']is False,'compiler status or lane width misrepresented')
 charts={n:chart(c)for n,c in w['charts'].items()};dims={n:len(c)for n,c in charts.items()}
 @lru_cache(None)
 def sub(a,b):return(sp.Matrix(charts[a]+charts[b]).rank()if charts[a]+charts[b]else 0)==dims[b]
 for i,r in enumerate(R):
  need(charts[f'L{i}']==chart({'kind':'span','rows':[r]}),'native line changed')
  need(charts[f'F{i}']==chart({'kind':'ann','rows':[r]}),'native facet changed')
 vals={f'X{i}':[1<<(2*i),1<<(2*i+1)]for i in range(111)}|{f'Y{i}':[1<<(222+2*i),1<<(223+2*i)]for i in range(111)}
 places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 owned=set();born=set();packets={f'P{q}'for q in range(8)};counts=Counter();moves=Counter();hist=[];events=[];handoff=None;dirty=0;peak=0;escape=None;source_lane=seed_lane=0
 def restored():need(all(vals[f'X{i}']==[1<<(2*i),1<<(2*i+1)]and places[f'X{i}']=='Hub'for i in range(111)),'original source not restored at Hub')
 for step,op in enumerate(w['operations']):
  kind,n,*args=op;counts[kind]+=1;changed=None
  if kind=='INIT':
   need(n not in vals and n not in born,'owner rebirth');vals[n]=[0,0];places[n]=args[0];owned.add(n);born.add(n);peak=max(peak,len(owned))
   if n in packets:restored();need(args[0]=='Hub','packet birth is not at Hub')
  elif kind=='ADD':
   t=args[0];need(n in vals and t in vals and n!=t,'invalid full ADD');need(sub(places[n],places[t])and sub(places[t],places[n]),'noncochart full ADD')
   vals[t]=[a^b for a,b in zip(vals[t],vals[n])];changed=t
  elif kind=='ADD_LANE':
   a,t,b=args;need(n in vals and t in vals and a in [0,1]and b in [0,1]and(n!=t or a!=b),'invalid selected-lane XOR')
   need(sub(places[n],places[t])and sub(places[t],places[n]),'noncochart lane XOR')
   need((n.startswith('X')and t.startswith('X'))or(n.startswith('X')and t in packets and places[t]=='Hub'),'unlisted conditional lane-service use')
   if t in packets:restored();seed_lane+=1
   else:source_lane+=1
   vals[t][b]^=vals[n][a];changed=t
   if escape is None and collapsed(vals[t][0])!=collapsed(vals[t][1]):escape={'operation_index':step,'operation':op,'chart':places[t],'repeated_input_lane_rows_hex':[hex(collapsed(v))for v in vals[t]]}
  elif kind=='MOVE':
   dest=args[0];need(n in vals and dims[dest]!=dims[places[n]],'invalid MOVE')
   need(n not in owned or n in packets,'extra owner moves')
   need(sub(dest,places[n])if n in owned else sub(places[n],dest),'wrong direction or incomparable MOVE')
   moves[abs(dims[dest]-dims[places[n]])]+=1;places[n]=dest;changed=n
  elif kind=='CLEAR':
   need(n in owned,'invalid retirement');dirty+=any(vals[n]);owned.remove(n);del vals[n],places[n]
  else:raise ValueError('unknown conditional opcode')
  if changed in packets and places[changed]!='Hub':
   for lane,row in enumerate(vals[changed]):hist.append(row);events.append({'operation_index':step,'packet':changed,'lane':lane,'chart':places[changed],'row_hex':hex(row)})
  if step+1==w['handoff']:
   handoff={n:[places[n],vals[n][:]]for n in sorted(owned)};need(handoff==w['expected'],'handoff chart or value mismatch')
 need(handoff is not None,'handoff missing');restored()
 for i in range(111):
  expected=[1<<(222+2*i+a)^((1<<(2*i+a))if i==0 else 0)for a in range(2)]
  need(vals[f'Y{i}']==expected,'wrong original Y value')
  need(places[f'Y{i}']==(f'F{i}'if w['closed']or i==0 else'zero'),'wrong original Y chart')
 need(len(owned)==(0 if w['closed']else len(born)),'owner endpoint mismatch')
 K=[sum(1<<j for j,r in enumerate(R)if i==j or dot(R[i],r)==0)for i in range(111)];hm=K[0]^K[4];ones=(1<<111)-1
 W=[]
 for i,k in enumerate(K):
  row=k&(hm if hm>>i&1 else ones^hm)
  for lane in range(2):W.append(sum(1<<(2*j+lane)for j in range(111)if row>>j&1))
 need([hex(v)for v in W]==[v for row in w['W_rows_lanes_hex']for v in row],'block W code changed')
 raw={n:v[1]for n,v in handoff.items()if n.startswith('C')};D=[r for rows in raw.values()for r in rows];DB=basis(D);HB=basis(hist)
 need(len(raw)==80 and len(DB)==80,'actual read capacity not80')
 need(len(DB)+30-len(basis(D+W))==19,'actual W intersection not19')
 witnesses=[]
 for i,row in enumerate(W):
  tag=solve(HB,row);need(tag is not None,'W row absent from actual history');witnesses.append({'role':i//2,'lane':i%2,'W_row_hex':hex(row),'history_coefficients_hex':hex(tag)})
 cachew=[]
 for n,rows in raw.items():
  for a,row in enumerate(rows):
   tag=solve(HB,row);need(tag is not None,'raw cache lane absent from actual histories');cachew.append({'cache':n,'lane':a,'history_coefficients_hex':hex(tag)})
 terminal=[r for q in range(8)for r in handoff[f'P{q}'][1]]
 need(not any(v>>222 for v in terminal),'terminal y contamination');need(len(basis(terminal))==13,'terminal rank13')
 need(handoff['P6'][1][1]==0 and handoff['P7'][1]==[0,0],'reserved three scalar slots not zero')
 need(escape is not None,'claimed noncoordinatewise packing has no constant-input escape')
 profile=dict(sorted(moves.items()));expected_profile={1:183,2:12,3:119,4:71,7:110}
 if w['closed']:need(profile==expected_profile,'whole-record movement profile changed')
 return {'status':'PASS_CONDITIONAL_LANE_SEMANTICS_ONLY','retained_compiler_admitted':False,'record_lanes':2,'independent_original_columns':444,
 'counts':dict(counts),'owned_peak':peak,'dirty_clears':dirty,'movement_profile':profile,'rank_length':sum(k*v for k,v in moves.items()),
 'actual_cache_increment_rank':len(DB),'actual_cache_W_intersection':19,'actual_history_rank':len(HB),'actual_history_y_rank':len(basis([v>>222 for v in hist])),
 'actual_history_W_intersection':30,'terminal_rank':13,'terminal_W_intersection':13+30-len(basis(terminal+W)),
 'conditional_source_lane_operations':source_lane,'conditional_seed_lane_operations':seed_lane,
 'bit_XOR_work_at_V_equals_2s':{'full_record_ADD_count':counts['ADD'],'lane_XOR_count':counts['ADD_LANE'],'coefficient_of_s':2*counts['ADD']+counts['ADD_LANE'],'selector_access_overhead':'Unadmitted and separately owed; no zero-cost masking claim.'},
 'first_escape_from_constant_record_invariant':escape,'new_complete_kappa':False,
 'evidence':{'history_events':events,'all222_W_lane_witnesses':witnesses,'all160_cache_lane_witnesses':cachew}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();rb=(a.repo/ROOT).read_bytes();need(hashlib.sha256(rb).hexdigest()==ROOT_SHA,'root pin');R=json.loads(rb)['native_roots'];raw=a.word.read_bytes();w=json.loads(raw);r=replay(w,R);e=r.pop('evidence');a.out.mkdir(parents=True,exist_ok=True);(a.out/'HISTORY.json').write_text(json.dumps(e,indent=2,sort_keys=True)+'\n')
 mutants={};lane=[i for i,op in enumerate(w['operations'])if op[0]=='ADD_LANE'and op[3].startswith('X')]
 cuts={'omit_lane_formation':lane[0],'omit_lane_restoration':lane[-1],'omit_actual_feedback':w['operations'].index(['ADD','Y0','P0'])}
 for label,i in cuts.items():
  bad=copy.deepcopy(w);del bad['operations'][i];bad['handoff']-=int(i<bad['handoff'])
  try:replay(bad,R)
  except(ValueError,KeyError)as exc:mutants[label]={'rejected':True,'reason':str(exc)}
  else:raise ValueError('accepted conditional-word mutant '+label)
 mutants['claim_retained_scalar_compiler_admission']={'rejected':True,'reason':'ADD_LANE is absent from the pinned scalar compiler grammar; the exhibited repeated-input state violates its constant-record invariant.'}
 out={'status':r['status'],'word_sha256':hashlib.sha256(raw).hexdigest(),'receipt':r,'negative_controls':mutants,'new_complete_kappa':False};(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'counts':r['counts'],'D_W':19,'history_W':30,'conditional_lane_count':r['counts']['ADD_LANE'],'compiler_admitted':False},sort_keys=True))
if __name__=='__main__':main()
