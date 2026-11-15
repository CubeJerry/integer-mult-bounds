#!/usr/bin/env python3
"""Author scalar-word replay for two fully paid physical copies."""
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
def replay(w,R):
 need(w['physical_copies']==2 and w['scalar_word_grammar']and not w['single_wide_record_claim'],'physical copy accounting')
 C={n:chart(c)for n,c in w['charts'].items()};dim={n:len(c)for n,c in C.items()}
 @lru_cache(None)
 def sub(a,b):return(sp.Matrix(C[a]+C[b]).rank()if C[a]+C[b]else 0)==dim[b]
 for i,r in enumerate(R):
  need(C[f'L{i}']==chart({'kind':'span','rows':[r]}),'native source line changed');need(C[f'F{i}']==chart({'kind':'ann','rows':[r]}),'native facet changed')
 X={f'X{i}_b{a}':(i,a)for i in range(111)for a in range(2)};Y={f'Y{i}_b{a}':(i,a)for i in range(111)for a in range(2)}
 vals={n:1<<(2*i+a)for n,(i,a)in X.items()}|{n:1<<(222+2*i+a)for n,(i,a)in Y.items()}
 loc={n:f'L{i}'for n,(i,a)in X.items()}|{n:'zero'for n in Y}
 packets={f'P{q}_b{a}'for q in range(8)for a in range(2)};owned=set();born=set();counts=Counter();moves=Counter();hist=[];events=[];handoff=None;peak=dirty=0;ground={};paths={p:[8]for p in packets}
 def restored():need(all(vals[n]==1<<(2*i+a)and loc[n]=='Hub'for n,(i,a)in X.items()),'original source not restored at Hub')
 for step,op in enumerate(w['operations']):
  kind,n,*args=op;counts[kind]+=1;changed=None
  if kind=='INIT':
   need(n not in vals and n not in born and len(args)==1,'owner rebirth');vals[n]=0;loc[n]=args[0];owned.add(n);born.add(n);peak=max(peak,len(owned))
   if n in packets:restored();need(args[0]=='Hub','packet birth not at Hub')
  elif kind=='ADD':
   t=args[0];need(n in vals and t in vals and n!=t and len(args)==1,'invalid scalar ADD');need(sub(loc[n],loc[t])and sub(loc[t],loc[n]),'noncochart scalar ADD')
   if t in packets and loc[t]=='Hub':need(n in X,'unaccounted seed source');restored()
   vals[t]^=vals[n];changed=t
  elif kind=='MOVE':
   dest=args[0];need(n in vals and len(args)==1 and dim[dest]!=dim[loc[n]],'invalid MOVE');need(n not in owned or n in packets,'extra owned channel')
   need(sub(dest,loc[n])if n in owned else sub(loc[n],dest),'wrong direction or incomparable MOVE');moves[abs(dim[dest]-dim[loc[n]])]+=1;loc[n]=dest;changed=n
   if n in packets:
    paths[n].append(dim[dest])
    if dim[dest]==0:need(n not in ground,'repeated first ground arrival');ground[n]=vals[n]
  elif kind=='CLEAR':
   need(n in owned and not args,'invalid retirement');dirty+=bool(vals[n]);owned.remove(n);del vals[n],loc[n]
  else:raise ValueError('new instruction outside scalar grammar')
  if changed in packets and loc[changed]!='Hub':hist.append(vals[changed]);events.append({'operation_index':step,'packet':changed,'chart':loc[changed],'row_hex':hex(vals[changed])})
  if step+1==w['handoff']:
   handoff={n:[loc[n],vals[n]]for n in sorted(owned)};need(handoff==w['expected'],'actual scalar handoff mismatch')
 need(handoff is not None,'handoff missing');restored()
 for n,(i,a)in Y.items():
  need(vals[n]==(1<<(222+2*i+a))^((1<<(2*i+a))if i==0 else 0),'wrong original target value')
  need(loc[n]==(f'F{i}'if w['closed']or i==0 else'zero'),'wrong original target chart')
 need(len(owned)==(0 if w['closed']else len(born)),'owner endpoint mismatch')
 need(paths=={p:list(range(8,-1,-1))for p in packets},'one physical bank escaped its complete path')
 K=[sum(1<<j for j,r in enumerate(R)if i==j or dot(R[i],r)==0)for i in range(111)];hm=K[0]^K[4];ones=(1<<111)-1;W=[]
 for i,row in enumerate(K):
  row&=hm if hm>>i&1 else ones^hm
  W.extend(sum(1<<(2*j+a)for j in range(111)if row>>j&1)for a in range(2))
 need([hex(v)for v in W]==[v for row in w['W_rows_lanes_hex']for v in row],'two-copy W code changed')
 raw={n:v[1]for n,v in handoff.items()if n.startswith('C')};D=list(raw.values());HB=basis(hist)
 need(len(raw)==160 and len(basis(D))==80,'actual scalar cache/read rank');need(80+30-len(basis(D+W))==19,'acquired W19 changed')
 ww=[];cw=[]
 for i,row in enumerate(W):
  tag=solve(HB,row);need(tag is not None,'two-copy W row absent from actual history');ww.append({'role':i//2,'bank':i%2,'row_hex':hex(row),'history_coefficients_hex':hex(tag)})
 for n,row in raw.items():
  tag=solve(HB,row);need(tag is not None,'actual scalar cache absent from history');cw.append({'cache':n,'row_hex':hex(row),'history_coefficients_hex':hex(tag)})
 T=[handoff[f'P{q}_b{a}'][1]for q in range(8)for a in range(2)];need(len(basis(T))==13 and not any(v>>222 for v in T),'terminal fields changed')
 zero=[n for n in packets if handoff[n][1]==0];need(sorted(zero)==['P6_b1','P7_b0','P7_b1'],'three reserved zero fields changed')
 if w['closed']:
  need(dict(moves)=={1:366,2:24,3:238,4:142,7:220},'movement not exactly doubled')
  need(dict(counts)=={'INIT':400,'ADD':2126,'MOVE':990,'CLEAR':400}and dirty==397,'full physical invoice changed')
 return {'status':'PASS_TWO_COPY_SCALAR_SOURCE','physical_copies':2,'independent_original_columns':444,'original_X_records':222,'original_Y_records':222,'counts':dict(counts),'owned_peak':peak,'dirty_clears':dirty,
 'movement_profile':dict(sorted(moves.items())),'rank_length':sum(k*v for k,v in moves.items()),'physical_packet_lifetimes':16,
 'actual_cache_increment_rank':80,'actual_cache_W_intersection':19,'actual_history_rank':len(HB),'actual_history_y_rank':len(basis([v>>222 for v in hist])),'actual_history_W_intersection':30,'terminal_rank':13,'terminal_W_intersection':13+30-len(basis(T+W)),
 'zero_terminal_fields':sorted(zero),'actual_first_ground_rows_hex':{p:hex(v)for p,v in ground.items()},'new_complete_kappa':False,
 'evidence':{'history_events':events,'all222_W_witnesses':ww,'all160_actual_cache_witnesses':cw}}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--conditional',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 rb=(a.repo/ROOT).read_bytes();need(hashlib.sha256(rb).hexdigest()==ROOT_SHA,'native root pin');R=json.loads(rb)['native_roots'];wb=a.word.read_bytes();w=json.loads(wb);cb=a.conditional.read_bytes();c=json.loads(cb)
 need(hashlib.sha256(cb).hexdigest()==w['source_conditional_word_sha256'],'conditional source pin')
 expected=[];boundaries=[]
 for op in c['operations']:
  k,n,*v=op
  if k=='ADD_LANE':expected.append(['ADD',f'{n}_b{v[0]}',f'{v[1]}_b{v[2]}'])
  elif k=='ADD':expected.extend([['ADD',f'{n}_b{i}',f'{v[0]}_b{i}']for i in range(2)])
  elif k in ['INIT','MOVE']:expected.extend([[k,f'{n}_b{i}',v[0]]for i in range(2)])
  elif k=='CLEAR':expected.extend([['CLEAR',f'{n}_b{i}']for i in range(2)])
  else:raise ValueError('unknown predecessor opcode')
  boundaries.append(len(expected))
 need(expected==w['operations']and boundaries==w['conditional_to_scalar_operation_boundaries'],'literal bank expansion differs from specified paid translation')
 r=replay(w,R);e=r.pop('evidence');a.out.mkdir(parents=True,exist_ok=True);(a.out/'HISTORY.json').write_text(json.dumps(e,indent=2,sort_keys=True)+'\n')
 source_add=[i for i,op in enumerate(w['operations'])if op[0]=='ADD'and op[1].startswith('X')and op[2].startswith('X')]
 cross=next(i for i in source_add if w['operations'][i][1][-1]!=w['operations'][i][2][-1])
 cuts={'omit_cross_bank_source_ADD':cross,'omit_Hub_inverse':source_add[-1],
 'omit_second_bank_MOVE':next(i for i,op in enumerate(w['operations'])if op==['MOVE','P0_b1','F0']),
 'omit_second_bank_feedback':w['operations'].index(['ADD','Y0_b1','P0_b1'])}
 if w['closed']:cuts['omit_second_bank_retirement']=w['operations'].index(['CLEAR','P6_b1'])
 mutants={}
 for label,i in cuts.items():
  bad=copy.deepcopy(w);del bad['operations'][i];bad['handoff']-=int(i<bad['handoff'])
  try:replay(bad,R)
  except(ValueError,KeyError)as exc:mutants[label]={'rejected':True,'reason':str(exc)}
  else:raise ValueError('accepted scalar expansion mutant '+label)
 bad=copy.deepcopy(w);bad['physical_copies']=1
 try:replay(bad,R)
 except ValueError as exc:mutants['count_only_one_physical_copy']={'rejected':True,'reason':str(exc)}
 else:raise ValueError('accepted one-copy tariff')
 out={'status':r['status'],'word_sha256':hashlib.sha256(wb).hexdigest(),'conditional_source_sha256':hashlib.sha256(cb).hexdigest(),'scalar_expansion_boundaries_checked':len(boundaries),'receipt':r,'negative_controls':mutants,'new_complete_kappa':False}
 (a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'counts':r['counts'],'dirty':r['dirty_clears'],'history_W':30,'D_W':19,'mutants':len(mutants)},sort_keys=True))
if __name__=='__main__':main()
