#!/usr/bin/env python3
"""Exact half tariff and explicitly conditional three-half caller budget."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main(out):
    p=HERE/'source/interval.py';pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    if hashlib.sha256(p.read_bytes()).hexdigest()!=pins['source/interval.py']:raise ValueError('interval pin')
    s=importlib.util.spec_from_file_location('interval',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    half={2:112,3:112,5:112,6:112};T={25:224,24:224};P={1:112,2:336,3:336,5:336,6:336,8:672}
    gap=m.moment(m.add((1,T),(-1,P)));bad=m.moment(m.add((1,T),(-1,P),(-1,{1:112})))
    if not(gap[0]>0 and bad[1]<0):raise ValueError('conditional gap / extra query control')
    r={'status':'PASS_EXACT_HALF_TARIFF_AND_CONDITIONAL_BUDGET','t':'199/200','half_profile':half,'half_moment':m.moment(half),
       'conditional_three_half_caller':{'productive_targets':T,'paid':P,'gap':gap,'one_extra_head_bank_gap':bad,
       'assumptions':['three actual half-source embeddings in three fresh rank8 stages','six paid whole-body idles per port',
       'common P,P^-1,P coefficient and complete body/history alignment','one physical rank1 head bank closes the residual Pd',
       'two rank25 and two rank24 independent original-input productive targets with ordinary adapters'],
       'physical_caller_constructed':False,'uniform_precision_or_supplier_admission':False},'new_kappa':False}
    out.write_text(json.dumps(m.enc(r),sort_keys=True,indent=2)+'\n');print('conditional gap',float(gap[0]))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output/PRICE.json');a=p.parse_args();main(a.output)
