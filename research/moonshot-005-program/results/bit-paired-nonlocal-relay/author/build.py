#!/usr/bin/env python3
"""Actual nonlocal ground-to-cell Y import on the frozen paired source."""
import argparse,copy,hashlib,json
from pathlib import Path
BASE_SHA='3aaabaf76bbfabccce40fe2dc56c2dfaf7242061de698d19098d64ef8821a8e5'

def xor(xs):
 a=0
 for x in xs:a^=x
 return a

def build(base):
 w=copy.deepcopy(base);ops=w['operations'];exp=w['expected'];W=[int(x,16) for x in w['W_rows_hex']]
 # The P1 incoming value at A15 is its target plus all later raw reads.
 raw={n:v for n,(c,v) in exp.items() if n.startswith('C')}
 tail=xor(v for n,v in raw.items() if n.startswith('C1_') and int(n.split('_')[1])>=4)
 assert tail==sum(1<<i for i in [4,5,6,7]+list(range(52,59)))
 j=59;g1=W[j]^tail;u=g1^(1<<j)
 oldtargets=[exp[f'P{q}'][1] for q in range(8)];targets=oldtargets[:]
 targets[1]=W[j];targets[5]=W[8];targets[6]=u
 seed={q:w['seeds'][q]^oldtargets[q]^targets[q] for q in [1,5,6]}
 # Change only explicit Hub seed ADDs; their costs remain in the literal word.
 rew=[]
 for op in ops:
  if op[0]=='INIT' and op[1] in {f'P{q}' for q in seed}:
   q=int(op[1][1:]);rew.append(op);rew.extend([['ADD',f'X{i}',f'P{q}'] for i in range(111) if seed[q]>>i&1]);continue
  if op[0]=='ADD' and op[1].startswith('X') and op[2] in {f'P{q}' for q in seed}:continue
  rew.append(op)
 # Finish the already paid P6 path before either paired trajectory starts.
 p6=[op for op in rew if (op[0]=='MOVE' and op[1]=='P6') or (op[0]=='ADD' and op[2]=='P6' and op[1].startswith('C'))]
 assert sum(o[0]=='MOVE' for o in p6)==8
 rew=[op for op in rew if not ((op[0]=='MOVE' and op[1]=='P6') or (op[0]=='ADD' and op[2]=='P6' and op[1].startswith('C')))]
 start=next(i for i,op in enumerate(rew) if op[0]=='MOVE' and op[1]=='P0')
 preload=[['INIT','YM59','zero'],['ADD','Y59','YM59'],['ADD','P6','Y59'],['MOVE','Y59','A15']]
 rew[start:start]=p6+preload
 # Two independent singular exchanges at one actual shared cell. P0's is retained.
 pos=next(i for i,op in enumerate(rew) if op[0]=='ADD' and op[2]=='P1' and op[1].startswith('C1_4_'))
 rew[pos:pos]=[['ADD','P1','Y59'],['ADD','Y59','P1'],['MOVE','Y59','F59']]
 pos=next(i for i,op in enumerate(rew) if op==['MOVE','P1','zero'])
 # There is no raw depth-eight cache; the Y mask is cancelled at actual ground.
 assert not any(n.startswith('C1_8_') for n in raw)
 rew.insert(pos+1,['ADD','YM59','P1'])
 exp['P1']=['zero',W[j]^(1<<j)];exp['P5']=['zero',W[8]];exp['P6']=['zero',u];exp['YM59']=['zero',1<<(111+j)]
 # P1+P6+P0 is the common axis bank x4+x5+x6+x7. Every correction below
 # is read from an actual private cache on an ascending receiver trajectory.
 routes={4:[('L7',7),('A63',6),('A31',5)],5:[('L4',4),('A96',7),('F5',6)],6:[('L5',5),('A207',4),('F6',7)],7:[('L6',6),('A159',5),('A143',4)]}
 route_meta={}
 for i,steps in routes.items():
  rew.extend([['ADD','P1',f'Y{i}'],['ADD','P6',f'Y{i}'],['ADD','P0',f'Y{i}']]);route_meta[i]=[];current='zero'
  for chart,axis in steps:
   hits=sorted(n for n,(c,v) in exp.items() if n.startswith('C') and c==chart and v==1<<axis)
   assert hits,('missing-axis-cache',i,chart,axis)
   n=hits[0]
   if chart!=current:rew.append(['MOVE',f'Y{i}',chart]);current=chart
   rew.append(['ADD',n,f'Y{i}']);route_meta[i].append({'chart':chart,'axis':axis,'cache':n})
  if current!=f'F{i}':rew.append(['MOVE',f'Y{i}',f'F{i}'])
 w['operations']=rew;w['handoff']=len(rew);w['completed_targets']=[0,4,5,6,7,j];w['terminal_W_roles']=[None,None,14,22,38,8,None,None]
 for q in seed:w['seeds'][q]=seed[q]
 w['schema']='paired-nonlocal-y-relay-v1';w['relay']={'recipient':j,'chart':'A15','raw_tail_hex':hex(tail),'P1_incoming_kernel_hex':hex(g1),'P6_actual_ground_preload_hex':hex(u),'P1_final_hex':hex(W[j]^(1<<j)),'completed_axis_routes':route_meta,'principal_through_matrix_2x2':[[0,0],[0,0]],'through_matrix_scope':'Actual boundary map from the two principal arrivals to their outgoing records, holding actual incoming Y records as separate boundary inputs.'}
 w['base_word_sha256']=BASE_SHA
 closed=copy.deepcopy(w);closed['closed']=True;closed['operations'] += [['CLEAR',n] for n in sorted(exp)]+[['MOVE',f'Y{i}',f'F{i}'] for i in range(111) if i not in w['completed_targets']]
 return w,closed

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();b=a.base.read_bytes();assert hashlib.sha256(b).hexdigest()==BASE_SHA;a.out.mkdir(parents=True,exist_ok=True)
 for n,w in zip(['WORD','CLOSED-WORD'],build(json.loads(b))):(a.out/f'{n}.json').write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
 print('BUILT_PAIRED_NONLOCAL_Y_RELAY')
if __name__=='__main__':main()
