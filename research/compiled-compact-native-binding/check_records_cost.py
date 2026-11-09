"""Exact source-record convention and pre-absorption exponent checks."""
from pathlib import Path
from fractions import Fraction as F
from binding_sources import module,need
from source_binding import fixture_events

HERE=Path(__file__).resolve().parent

def run():
    lift=module('binding_record_lift',HERE/'vendor/record_lift/lift.py')
    events,report=fixture_events();checked=0
    for event in events:
        source,target=event.token[3:5];record=('XROW',target,source)
        for f in (1,2,3,4):
            for packed in range(1<<(2*f)):
                columns=[(packed>>(2*j))&3 for j in range(f)]
                want=[x^(((x>>source)&1)<<target) for x in columns]
                got=lift.execute([record],columns,f,0b101101)
                need(got==(want,0,0b101101),'exact retained XROW convention, all columns and spectators')
                checked+=1
    guard=[]
    for p in (2,3,7,32,257,1024):
        L=(p-1).bit_length();G=4*L+6;K=128*G
        need(K>=G+4*L+10,'actual K128G sufficient guard separation')
        delta=p*(2*F(1,1<<G)+8*F(1,1<<(K-G)))
        need(delta<=F(5,128*p**3),'complete two-source exceptional proportion')
        guard.append(dict(p=p,G=G,K=K,delta_upper=str(F(5,128*p**3))))
    kappa=F(781451,250000000);margin=F(1,1400000000)
    tau_node=1-kappa-4*margin;tau_B1=F(99830289,100000000)
    need(tau_B1>tau_node,'historical coarse tariff does not imply the selected node exponent')
    return dict(record_checks=checked,source_report=report,guards=guard,
                historical_tau=str(tau_B1),selected_node_tau=str(tau_node),
                exponent_gap=str(tau_B1-tau_node),
                conclusion='Upper-bound implication obstruction only; no algorithmic lower bound or kappa claim')
