#!/usr/bin/env python3
"""Exhaust exact three-import injections into the three late M1 loads.

This is an information-envelope screen, not an endpoint-valid physical word.
The original source word is replayed, all changed record histories are propagated,
and arbitrary historical X parts and geometric raw locals are generously granted.
"""
from pathlib import Path
from itertools import product
import argparse, hashlib, importlib.util, json

IMPORTS = [8,9,36]
MARKERS = {'P3':'K46_PAIR','P4':'P4_K','P5':'P5_K'}

def load(path):
    spec=importlib.util.spec_from_file_location('e',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def add(b,x):
    while x:
        k=x.bit_length()-1
        if k in b:x^=b[k]
        else:b[k]=x;return

def contains(b,x):
    while x:
        k=x.bit_length()-1
        if k not in b:return False
        x^=b[k]
    return True

def basis(rows):
    b={}
    for x in rows:add(b,x)
    return b

def closure(initial,known):
    known=set(known);bases=[b.copy() for b in initial];todo=set(known);waves=[]
    while True:
        for b in bases:
            for j in todo:add(b,1<<j)
        newly={i for i,b in enumerate(bases) if i not in known and contains(b,1<<i)}
        if not newly:return sorted(known),waves
        waves.append(sorted(newly));known|=newly;todo=newly

def parametrized_history(w,C):
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':0 for i in range(111)}
    at={f'X{i}':f'L{i}' for i in range(111)}|{f'Y{i}':'zero' for i in range(111)}
    tags={n:0 for n in values};H=[(0,n,at[n],v,0) for n,v in values.items()];events=[]
    for step,op in enumerate(w['operations'],1):
        kind,n,*args=op
        if kind=='MOVE' and n in MARKERS and args==[MARKERS[n]]:
            assert at[n]=='M1'
            for i in IMPORTS:
                assert C[at[f'IMPORT_E{i}']]==C['M1'] and values[f'IMPORT_E{i}']==1<<i
                assert tags[f'IMPORT_E{i}']==0
            bit=1<<(['P3','P4','P5'].index(n));assert tags[n]==0
            tags[n]^=bit;H.append((step,n,at[n],values[n],tags[n]))
            events.append({'before_step':step,'principal':n,'at':'M1','next_chart':args[0],
                           'pre_injection_row_hex':hex(values[n]),'parameter_bit':bit})
        if kind=='INIT':values[n]=0;tags[n]=0;at[n]=args[0]
        elif kind=='ADD':values[args[0]]^=values[n];tags[args[0]]^=tags[n]
        elif kind=='MOVE':at[n]=args[0]
        elif kind=='CLEAR':del values[n],tags[n],at[n]
        if kind in ['INIT','ADD','MOVE']:
            changed=args[0] if kind=='ADD' else n
            H.append((step,changed,at[changed],values[changed],tags[changed]))
    assert len(events)==3
    return H,events

def main():
    p=argparse.ArgumentParser()
    for n in ['repo','word','engine','out']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--word-sha256',required=True)
    a=p.parse_args();raw=a.word.read_bytes();pin=hashlib.sha256(raw).hexdigest();assert pin==a.word_sha256
    w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes()
    assert hashlib.sha256(source).hexdigest()==w['source_sha256'];roots=json.loads(source)['native_roots']
    e=load(a.engine);C,_,replay=e.replay(w,roots);H,events=parametrized_history(w,C)
    source_rows=[];fixed=[];variable=[]
    for i in range(111):
        rows={(v,t) for _,_,c,v,t in H if e.sub(C[c],C[f'F{i}'])}
        rows|={(1<<j,0) for j in range(111) if sum(x*y for x,y in zip(roots[i],roots[j]))==0}
        source_rows.append(sorted(rows));fixed.append(basis(v for v,t in rows if t==0))
        variable.append(sorted((v,t) for v,t in rows if t))
    choices=[sum(1<<j for k,j in enumerate(IMPORTS) if m>>k&1) for m in range(8)]
    old=set(w['targets']);cases=[]
    for coeffs in product(range(8),repeat=3):
        payloads=[choices[c] for c in coeffs];tagvalue={t:0 for t in range(8)}
        for t in range(8):
            for k,x in enumerate(payloads):
                if t>>k&1:tagvalue[t]^=x
        bs=[]
        for i in range(111):
            b=fixed[i].copy()
            for row,tag in variable[i]:add(b,row^tagvalue[tag])
            bs.append(b)
        actual_closure,waves=closure(bs,set())
        free_closure,free_waves=closure(bs,old)
        lost=[]
        for i in old:
            b=bs[i].copy()
            for j in old-{i}:add(b,1<<j)
            if not contains(b,1<<i):lost.append(i)
        cases.append({'coefficient_masks_P3_P4_P5':list(coeffs),
                      'payload_rows_hex':[hex(x) for x in payloads],
                      'injection_rank':len(basis(payloads)),
                      'closure_from_no_global_points':actual_closure,'feedback_waves':waves,
                      'preserves_all_original_targets_in_information_envelope':old<=set(actual_closure),
                      'new_points_with_all_original_targets_granted':sorted(set(free_closure)-old),
                      'old_targets_impossible_even_with_all_other_original_targets_granted':sorted(lost)})
    survivors=[c for c in cases if c['preserves_all_original_targets_in_information_envelope']]
    gainers=[c for c in survivors if set(c['closure_from_no_global_points'])-old]
    necessary_survivors=[c for c in cases if not c['old_targets_impossible_even_with_all_other_original_targets_granted']]
    summary={'status':'COMPLETE_EXACT_BINARY_INJECTION_FAMILY_SCREEN','word_sha256':pin,
             'native_source_sha256':w['source_sha256'],'source_replay':replay,'injection_sites':events,
             'coefficient_field':'GF(2)','choice_count':len(cases),'original_targets':sorted(old),
             'information_envelope_preserving_count':len(survivors),'preserving_and_gaining_count':len(gainers),
             'necessary_old_point_feasibility_survivors':len(necessary_survivors),
             'maximum_closure_count_preserving_original_targets':max((len(c['closure_from_no_global_points']) for c in survivors),default=None),
             'best_gaining_cases':sorted(gainers,key=lambda c:-len(c['closure_from_no_global_points']))[:30],
             'scope':'Complete binary coefficient screen for injections into the three specified late M1 loads only; every actual changed history is propagated. All-history X-parts/raw-local/decoded-point feedback are optimistic information grants, not physical fitting words. Finite failure does not imply arbitrary-field or arbitrary-source impossibility.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(summary,indent=2)+'\n');(a.out/'ALL-512.json').write_text(json.dumps(cases,indent=2)+'\n')
    print(json.dumps(summary))

if __name__=='__main__':main()
