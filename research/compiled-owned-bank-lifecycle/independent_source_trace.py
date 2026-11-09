"""Independent review: annotate the authenticated compiler's literal round loop.

No author flat-ownership checker or author expected trace is imported.
"""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import types
ROOT=Path(__file__).resolve().parents[2]
PACKAGE=ROOT/'research/compiled-owned-bank-lifecycle'


def need(ok,message):
    if not ok: raise ValueError(message)


def module(name,path,raw):
    obj=types.ModuleType(name);obj.__file__=str(path);sys.modules[name]=obj
    exec(compile(raw,str(path),'exec'),obj.__dict__)
    return obj


raw=(ROOT/'research/lockstep-completion-pass/executor.py').read_bytes()
need(hashlib.sha256(raw).hexdigest()=='0bda14a3e5f4da348cd5c89ebe29d717e7a5406ec31b164d5b9e1d25f7f38e0e','canonical executor SHA256')
original=module('c_review_original',ROOT/'research/lockstep-completion-pass/executor.py',raw)
tree=ast.parse(raw)
compiler=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='Compiler')
method=next(n for n in compiler.body if isinstance(n,ast.FunctionDef) and n.name=='run_class')
rounds=[n for n in method.body if isinstance(n,ast.For) and ast.unparse(n.target)=='(j, ((r, owner), kind))']
need(len(rounds)==1,'one literal authenticated source round loop')
loop=rounds[0]
loop.body.insert(0,ast.parse('self.review_fragment(units, j)').body[0])
method.body.insert(method.body.index(loop)+1,ast.parse('self.review_fragment(units, len(self.R.rounds))').body[0])
ast.fix_missing_locations(tree)
annotated=module('c_review_annotated',ROOT/'research/lockstep-completion-pass/executor.py',tree)
irbytes=(PACKAGE/'source_ir.py').read_bytes();IR=module('c_review_ir',PACKAGE/'source_ir.py',irbytes)


def source_trace(unit,rank):
    fragments,rounds=unit.pieces()
    rule=original.Rule(unit.name,unit.roles,tuple((e.rank,e.fields[0]) for e in rounds),unit.owned)
    class Reviewer(annotated.Compiler):
        def __init__(self):
            super().__init__(rule,owned_policy='unit')
            self.trace=[];self.ids={};self.frames=[];self.programs=0
            self.private_borrowed=0;self.batch_counts=Counter();self.round_now={};self.class_group={}
        def alloc_bank(self,*args):
            f=super().alloc_bank(*args)
            need(f not in self.ids,'fresh direct-source identity')
            self.ids[f]=len(self.ids)
            return f
        def review_fragment(self,units,j):
            for U in units:
                _,g,_,_,fmap,omap,_=U
                names=dict(fmap,**omap)
                self.round_now[g]=j
                self.class_group[g]=tuple(U[1] for U in units)
                for event in fragments[j]:
                    self.trace.append(('fragment',event.op,tuple(self.ids[names[f]] for f in event.fields),event.token))
        def sub(self,n,fields,tops):
            fids=tuple(self.ids[f] for f in fields)
            if tops and isinstance(tops[0],tuple) and type(tops[0][0]) is int:
                label=('deepest-exit',n,tuple(tops))
                self.batch_counts[(self.class_group[tops[0][0]],self.round_now[tops[0][0]])]+=1
            else:
                label=('source-complement',n,self.frames[-1][1]-n)
            self.trace.extend(('program-enter',label,fids,i,f) for i,f in enumerate(fids))
            if n<rule.m:
                self.blackbox(n,fields,tops)
            else:
                need(len(fields)==self.compile(n)[0],'complete direct-source smaller program')
                self.uniform(n,fields,tops)
            self.trace.extend(('program-return',label,fids,i,fids[i]) for i in reversed(range(len(fids))))
        def blackbox(self,n,fields,tops):
            need(n<rule.m,'direct source only elementary rank base')
            super().blackbox(n,fields,tops)
            for field in fields:
                for axis in range(n):
                    self.trace.append(('leaf',self.ids[field],axis,n))
        def uniform(self,n,fields,tops,top_level=False,copies=None):
            need(copies is None,'no partial direct source')
            self.programs+=1;self.frames.append((self.programs,n))
            super().uniform(n,fields,tops,top_level=top_level,copies=None)
            self.frames.pop()
        def push(self,f,entry,expect_top):
            if isinstance(entry,tuple) and type(entry[0]) is int and entry[1] in dict(unit.roles):
                self.private_borrowed+=int(isinstance(f,tuple) and f[0]=='own')
            super().push(f,entry,expect_top)
    subject=Reviewer();B,a,P,cost=subject.compile(rank)
    fields=[('array',i) for i in range(B)];subject.ids={f:i for i,f in enumerate(fields)}
    if rank<rule.m:subject.blackbox(rank,fields,[None]*B)
    else:subject.uniform(rank,fields,[None]*B,top_level=True)
    need(sum(e[0]=='leaf' for e in subject.trace)==P,'independent direct-source leaf invoice')
    return subject.trace,dict(width=B,replication=a,paid=P,programs=subject.programs,
                              private_borrowed=subject.private_borrowed,
                              deepest_batches=sum(subject.batch_counts.values()),deepest_rounds=len(subject.batch_counts),
                              max_batches_per_round=max(subject.batch_counts.values(),default=0),source_cost=cost)


def actual_trace(unit):
    output=[]
    for event in unit.events:
        token=event.token
        if token and token[0]=='unit-fragment':
            output.append(('fragment',event.op,event.fields,token[-1]))
        elif event.op=='PAID':
            need(token[0]=='ordinary-rank-one' and event.rank==1,'only true elementary leaves')
            output.append(('leaf',event.fields[0],token[-2],token[-1]))
        elif event.op=='SERVICE' and token and token[0] in ('program-enter','program-return'):
            binding,index=token[1:];_,kind,fields=binding
            if kind[0]=='source-complement':label=('source-complement',kind[2],kind[3])
            else:
                need(kind[0]=='deepest-exit','declared source subprogram category')
                label=('deepest-exit',kind[3],kind[4])
            need(event.fields==(fields[index],),'exact entered source field')
            output.append((token[0],label,fields,index,event.fields[0]))
    return output


E=IR.Event
unit=IR.Unit('independent-review',(('x',2),('y',3)),('scratch','spare'),(
 E('INIT',('scratch',),('init1',)),E('COPY',('scratch','x'),('copy1',)),
 E('SERVICE',('x','scratch'),('before-first',)),E('PAID',('scratch',),('first',),1),
 E('SERVICE',('y','scratch'),('after-first',)),E('CLEAR',('scratch',),('clear1',)),
 E('INIT',('spare',),('init2',)),E('COPY',('spare','y'),('copy2',)),E('PAID',('x',),('second',),1),
 E('SERVICE',('x','spare'),('after-second',)),E('PAID',('spare',),('third',),1),
 E('CLEAR',('spare',),('clear2',)),E('INIT',('scratch',),('init3',)),
 E('COPY',('scratch','y'),('copy3',)),E('PAID',('scratch',),('fourth',),1),
 E('SERVICE',('x','scratch'),('after-fourth',)),E('CLEAR',('scratch',),('clear3',)))).check()
rows=[];last=None;last_expected=None
for rank in (2,3,4,6,9,12):
 expected,stats=source_trace(unit,rank)
 lowered,report,_=IR.lower(unit,rank,original)
 actual=actual_trace(lowered)
 need(actual==expected,'literal source chronology at rank '+str(rank))
 need(stats['paid']==report['paid'] and stats['private_borrowed']==report['borrowed_private'],'direct-source count agreement')
 rows.append(dict(rank=rank,trace_events=len(actual),**stats))
 print(json.dumps(rows[-1],sort_keys=True),flush=True)
 last,last_expected=lowered,expected
need(any(row['private_borrowed'] for row in rows),'actual nested private borrow')
need(any(row['replication']>1 for row in rows),'complete replicated source execution')
need(any(row['max_batches_per_round']>1 for row in rows),'multiple deepest batches before parent continuation')
# Semantic corruption can preserve the paired ownership brackets.
events=[];changed=False
for event in last.events:
 token=event.token
 if event.op=='SERVICE' and token and token[0] in ('program-enter','program-return'):
  binding,index=token[1:];tag,kind,fields=binding
  if kind[0]=='source-complement':
   kind=kind[:-1]+(kind[-1]+1,)
   event=E(event.op,event.fields,(token[0],(tag,kind,fields),index),event.rank);changed=True
 events.append(event)
need(changed and actual_trace(IR.Unit('bad complement',last.roles,last.owned,tuple(events)))!=last_expected,'wrong complement support rejected independently')
filtered=actual_trace(last)
position=next(i for i,item in enumerate(filtered) if item[0]=='fragment' and item[1]=='SERVICE')
dropped=filtered[:position]+filtered[position+1:]
need(dropped!=last_expected,'omitted inter-round source service rejected independently')
print(json.dumps(dict(marker='PASS_INDEPENDENT_LITERAL_SOURCE_CHRONOLOGY',cases=rows,
 source_ir_sha256=hashlib.sha256(irbytes).hexdigest(),executor_sha256=hashlib.sha256(raw).hexdigest(),
 controls=['paired wrong complement offset','omitted source nonpaid service']),sort_keys=True))
