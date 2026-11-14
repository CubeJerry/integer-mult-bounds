#!/usr/bin/env python3
"""Exact source tariffs and a separately stipulated twelve-stage caller budget."""
import argparse,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
def need(c,m):
    if not c:raise ValueError(m)
def main(args):
    need(hashlib.sha256(args.engine.read_bytes()).hexdigest()==PIN,'exact interval engine')
    sp=importlib.util.spec_from_file_location('logical112_interval',args.engine)
    p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
    a=6;outside={}
    def put(r,c):outside[r]=outside.get(r,F(0))+c
    put(1+16*a,F(112*2,2*a));put(1,F(-112*4,2*a))
    for j in range(1,a+1):put(1+8*j,F(112*4,2*a))
    for j in range(1,a):put(8*j,F(-112*4,2*a))
    allowance=p.moment(outside);data={};profiles={}
    for variant in('R0','R0-minimal','R1'):
        raw=(args.results/variant/'WORD.json.gz').read_bytes();word=json.loads(gzip.decompress(raw))
        result=json.loads((args.results/variant/'RESULT.json').read_text())
        need(hashlib.sha256(raw).hexdigest()==result['word_sha256'],'actual word/result pin')
        q=Counter();frames=word['frames']
        for op in word['program']:
            if op[0]=='MOVE':q[abs(len(frames[op[3]])-len(frames[op[2]]))]+=1
        need(dict(q)=={int(k):v for k,v in result['source_bill']['moves'].items()},'literal full movement tariff')
        charge=p.moment(q);slack=p.moment(p.add((1,outside),(-1,q)))
        profiles[variant]=q
        data[variant]={'word_sha256':result['word_sha256'],'profile':q,'source_moment':charge,
            'conditional_twelve_stage_margin_per_native':slack,
            'conditional_twelve_stage_total_margin':tuple(12*z for z in slack),
            'display':{'source_moment':float(charge[0]),'conditional_margin_per_native':float(slack[0])}}
    saving=p.moment(p.add((1,profiles['R0']),(-1,profiles['R0-minimal'])))
    need(saving[0]>0,'actual minimal meeting saves a positive moment')
    answer={'status':'PASS_EXACT_FULL112_SOURCE_TARIFFS','kappa':'1/200','interval_engine_sha256':PIN,
      'sources':data,'minimal_meeting_saving':saving,'conditional_outside_profile_per_native':outside,
      'conditional_outside_allowance_per_native':allowance,
      'conditional_invoice':'12*(allowance-Q_t)-4*delta_q-26*delta_r-E',
      'new_physical_query_and_productive_target_admission_assumed_for_invoice':True,
      'old104_fixed_m_penalty_not_inherited':True,
      'scope':'Source moments are actual full MOVE counts. Caller allowance is conditional on its new physical operator, query and productive-target contracts; every new debit remains. R1 additionally needs coefficient7 service. No complete supplier or new kappa.'}
    args.output.write_text(json.dumps(p.enc(answer),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':answer['status'],'sources':{k:v['display']for k,v in data.items()},'minimal_saving':float(saving[0])},indent=2))
if __name__=='__main__':
    x=argparse.ArgumentParser();x.add_argument('--engine',type=Path,required=True);x.add_argument('--results',type=Path,required=True)
    x.add_argument('--output',type=Path,required=True);main(x.parse_args())
