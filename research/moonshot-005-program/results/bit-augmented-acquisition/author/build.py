#!/usr/bin/env python3
"""Two actual facet acquisitions free one W seed without owned descent."""
import argparse,copy,hashlib,json
from pathlib import Path
BASE_SHA='4cea047c9f28a17c3379d3073a88b3a5d00e6e749214661c9d330a289824d060'
GROUPS={0:[49,50,84,87,100,102],1:[18,20,70,72]}
def build(base,spare=False):
 w=copy.deepcopy(base);ops=[['INIT',f'EXTRA_A{q}',f'F{q}']for q in GROUPS]
 assignments={j:q for q,js in GROUPS.items()for j in js};rows={q:sum(1<<j for j in js)for q,js in GROUPS.items()}
 used=set();old=w['operations'];t=0;newseeds={}
 values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
 places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 # The old symbolic stream verifies that every diverted carrier is still pure.
 for op in old:
  kind,n,*a=op
  if kind=='INIT':values[n]=0;places[n]=a[0]
  elif kind=='ADD':values[a[0]]^=values[n]
  elif kind=='MOVE':
   if n.startswith('X')and int(n[1:])in assignments and a[0]=='Hub':
    j=int(n[1:]);assert values[n]==1<<j;used.add(j)
   places[n]=a[0]
  else:raise AssertionError('live base must have no clear')
 assert used==set(assignments)
 used=set()
 while t<len(old):
  op=old[t];kind,n,*a=op
  if kind=='INIT'and n.startswith('P'):
   q=int(n[1:]);ops.append(op);t+=1;seed=0
   while t<len(old)and old[t][0]=='ADD'and old[t][2]==n and old[t][1].startswith('X'):
    seed^=1<<int(old[t][1][1:]);t+=1
   seed^=rows.get(q,0)
   if spare and q==7:seed^=base['expected']['P7'][1]
   newseeds[n]=seed;ops.extend([['ADD',f'X{i}',n]for i in range(111)if seed>>i&1]);continue
  if kind=='MOVE'and n.startswith('X')and int(n[1:])in assignments and a[0]=='Hub':
   j=int(n[1:]);q=assignments[j];assert j not in used;used.add(j)
   ops.extend([['MOVE',n,f'F{q}'],['ADD',n,f'EXTRA_A{q}'],op])
  else:
   ops.append(op)
   if kind=='MOVE'and n in ('P0','P1')and a[0]==f'F{int(n[1:])}':ops.append(['ADD',f'EXTRA_A{int(n[1:])}',n])
  t+=1
 assert used==set(assignments)
 expected=copy.deepcopy(base['expected']);expected.update({f'EXTRA_A{q}':[f'F{q}',row]for q,row in rows.items()})
 if spare:expected['P7'][1]=0
 w.update(schema='augmented-colored-acquisition-h9-v1',operations=ops,expected=expected,handoff=len(ops),closed=False,
  spare_packet_terminal_zero=spare,extra_pure_acquisitions=[{'packet':f'P{q}','chart':f'F{q}','owner':f'EXTRA_A{q}','source_roles':js,'row_hex':hex(rows[q])}for q,js in GROUPS.items()],
  actual_seed_rows_hex={n:hex(r)for n,r in newseeds.items()},seeds=[newseeds[f'P{q}']for q in range(8)],increment_space_dimension=42,increment_W_intersection=9,new_complete_kappa=False,base_word_sha256=BASE_SHA)
 if spare:w['terminal_W_roles'][-1]=None
 closed=copy.deepcopy(w);closed['closed']=True;closed['operations'] += [['CLEAR',n]for n in sorted(expected)] + [['MOVE',f'Y{i}',f'F{i}']for i in range(111)if i not in w['completed_targets']]
 return w,closed

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args()
 raw=a.source.read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE_SHA;base=json.loads(raw);a.out.mkdir(parents=True,exist_ok=True)
 for spare,prefix in [(False,'PRESERVED'),(True,'SPARE')]:
  for suffix,w in zip(['WORD','CLOSED-WORD'],build(base,spare)):(a.out/f'{prefix}-{suffix}.json').write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
 print('BUILT_TWO_ACTUAL_FACET_ACQUISITIONS')
if __name__=='__main__':main()
