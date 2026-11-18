#!/usr/bin/env python3
"""Exact rational brackets for the frozen d^(199/200) movement moments."""
from argparse import ArgumentParser
from fractions import Fraction
from pathlib import Path
import json

PROFILES={'direct':{1:126,5:315,7:210},'shared_D4':{1:126,2:189,3:441,7:210},'merged_K6':{1:252,2:315,3:189,7:210}}

def bracket(d):
    scale=10**24;power=d**199*scale**200;low=0;high=d*scale+1
    while high-low>1:
        m=(low+high)//2
        if m**200<=power:low=m
        else:high=m
    return Fraction(low,scale),Fraction(low+(low**200!=power),scale)

def moment(profile):
    low=high=Fraction(0)
    for d,n in profile.items():
        a,b=bracket(d);low+=n*a;high+=n*b
    return low,high

def main():
    p=ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    values={name:moment(prof)for name,prof in PROFILES.items()}
    lo=values['direct'][0]-values['merged_K6'][1];hi=values['direct'][1]-values['merged_K6'][0]
    assert lo>0
    out={'status':'PASS_STRICT_FROZEN_MOVEMENT_GAIN_FOR_SAME_SEVEN_SOURCE_TARGET','exponent':'199/200','profiles':PROFILES,'moment_intervals':{name:[str(x)for x in value]for name,value in values.items()},'moment_decimals':{name:float(value[0])for name,value in values.items()},'direct_minus_merged_interval':[str(lo),str(hi)],'direct_minus_merged_decimal':float(lo),'normalized_by_fifteen_binary_bank_lanes_interval':[str(lo/15),str(hi/15)],'ordinary_ADD_and_helper_costs_separately_charged':True,'full_supplier_or_kappa_claim':False}
    a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['moment_decimals'],'gain',out['direct_minus_merged_decimal'])

if __name__=='__main__':main()
