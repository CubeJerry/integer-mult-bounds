"""Bounded observational trace of actual selected single-leaf divmod call6."""
from pathlib import Path
import sys, types, json, math

ROOT=Path(__file__).resolve().parents[1]/'wave9/literal-leaf-headers'
def load(path,name):
 m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
 exec(compile(path.read_bytes(),str(path),'exec'),m.__dict__);return m
v=load(ROOT/'inputs/keypass/verify.py','b10_prev')
_,previous,base,m,*_=v.modules()
trace=[];current={'invocation':0,'call':0}
old_produce=m.numeric.produce;old_div=m.w.Unsigned.divmod
def produce(*args,**kwargs):
 current['invocation']+=1;current['call']=0
 return old_produce(*args,**kwargs)
def div(self,n,d):
 current['call']+=1
 capture=current['call']==6
 if capture:
  before={'invocation':current['invocation'],'N':n.slot,'D':d.slot,
          'available':list(self.arena.available),'live':sorted(self.arena.live),
          'n_bits':list(n.cells[1:]),'d_bits':list(d.cells[1:])}
 q,r=old_div(self,n,d)
 if capture:
  before.update(Q=q.slot,R=r.slot,available_after=list(self.arena.available),live_after=sorted(self.arena.live))
  trace.append(before)
 return q,r
m.numeric.produce=produce;m.w.Unsigned.divmod=div
cases=[]
for left,right in((2,3),(3,2),(3,5),(5,3),(4,9),(9,4),(8,11),(11,8),(13,16),(16,13)):
 for value in(0,1,left-1,left):
  start=len(trace);current['invocation']=0
  source=m.e.Port(m.w)
  for modulus,coordinate in zip((17,19,left,right),(1,2,value,1)):
   width=max(modulus.bit_length(),coordinate.bit_length())
   for token in [m.r.ROOT]+[m.w.ONE]*width+[m.r.WORD_END]+[(modulus>>i)&1 for i in range(width)]+[m.r.WORD_END]+[(coordinate>>i)&1 for i in range(width)]+[m.r.RECORD_END]:
    source.append(token)
  source.append(m.w.RIGHT);source.rewind()
  endpoint=m.writer.Endpoint(m.f,m.w,m.r,m.e,m.numeric,m.owner,m.bridge,source)
  iterator=endpoint.iterator
  with base.seal_numerical_roles(m):
   lease=iterator.next()
   while not m.route.selected_leaf(iterator,lease):
    lease.close();lease=iterator.next()
   selected=[x for x in trace[start:] if x['invocation']==current['invocation']]
   if len(selected)!=1:raise ValueError('one selected sixth call')
   row=selected[0];row.update(left=left,right=right,value=value)
   cases.append(row)
   lease.close()
   if not iterator.closed:iterator.close()
out={'status':'OBSERVED_BOUNDARIES_ONLY','cases':cases}
(Path(__file__).resolve().parent/'CALL-TRACE.json').write_text(json.dumps(out,indent=2)+'\n')
states={tuple([x['N'],x['D'],*x['available'][-5:]]) for x in cases}
print(json.dumps({'cases':len(cases),'distinct_entry_fingerprints':len(states),'fingerprints':sorted(states)},indent=2))
