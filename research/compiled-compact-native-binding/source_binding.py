"""Bind one exact emitted current compiler record to its physical owner.

All maps/tokens here are fixed template data. run() receives no address oracle
or payload callback. The current A execute_table interpreter is not invoked.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
from binding_sources import module,need
from provider import Provider

HERE=Path(__file__).resolve().parent

class Service:
    def __init__(self,event,rank,native_factory):
        t=event.token
        need(event.op=='SERVICE' and len(event.fields)==1 and len(t)==6
             and t[0]=='selected-bit-xor','exact current emitted XOR service')
        need(type(t[1]) is int and t[1]>=0 and t[2] in ('enter','return'),
             'fixed occurrence/return token')
        need(type(t[3]) is int and type(t[4]) is int,'fixed source/target block labels')
        need(t[5] and t[5][0] in ('program-enter','program-return','occurrence-enter',
                                 'occurrence-return','base-axis-enter','base-axis-return'),
             'retained source boundary token')
        self.token=t;self.owner=event.fields[0]
        self.record=('XROW',t[4],t[3]) # #5445 writes target before source.
        self.provider=Provider(rank,t[3],t[4],native_factory)
        self.field=self.context=None

    @property
    def port_count(self):return self.provider.port_count

    def bind(self,work,fields,context):
        need(self.owner in fields,'actual compiled owner is present')
        self.field=fields[self.owner];self.context=context
        self.provider.bind(work)

    def run(self):
        need(self.field is not None,'fixed field/context binding before input')
        self.provider.run(self.field,self.context)

def fixture_events():
    """Actual #5443 -> A.lower -> B.bind execution; no native algebra claim.

    The declared (2,3)-rank unit at final rank2 takes the compiler's elementary
    program branch, emitting both ordinary axes and their actual prefix routes.
    This is a compiler-control fixture, not a proposed Gaussian identity.
    """
    ir=module('binding_current_ir',HERE/'vendor/lifecycle/source_ir.py')
    compiler=module('binding_lockstep',HERE/'vendor/lockstep_executor.py')
    routes=module('binding_current_routes',HERE/'vendor/dispatch/compiler_routes.py')
    raw=ir.Unit('current-native-binding-fixture',(('x',2),('y',3)),('o',),
                (ir.Event('INIT',('o',)),ir.Event('COPY',('o','x')),
                 ir.Event('PAID',('o',),('fixture-paid',),1),ir.Event('CLEAR',('o',)))).check()
    unit,lowered,_=ir.lower(raw,2,compiler)
    events,routed,_=routes.bind(unit,2,3,dict(raw.roles))
    selected=tuple(e for e in events if e.op=='SERVICE' and e.token and e.token[0]=='selected-bit-xor')
    need(len(selected)==6,'actual complete entry and return triple')
    return selected,dict(lowered=lowered,routed=routed)
