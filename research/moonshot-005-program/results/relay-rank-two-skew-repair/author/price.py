#!/usr/bin/env python3
"""Exact limiting MOVE-profile screen; does not transfer the old caller proof."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
PIN='5f32aa66d62f5edeb3f3fcda3a1cacb9f5fc5269154a3a23cb178a1ee2fc48a0'
pa=argparse.ArgumentParser();pa.add_argument('--old-price',type=Path,required=True);pa.add_argument('--output',type=Path,required=True);a=pa.parse_args();raw=a.old_price.read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:raise ValueError('old price pin')
p=json.loads(raw);scale=10**32;target=9**199*scale**200;lo=8*scale;hi=9*scale
while hi-lo>1:
 mid=(lo+hi)//2
 if mid**200<=target:lo=mid
 else:hi=mid
assert lo**200<=target<hi**200
cost=(F(2*lo,scale),F(2*hi,scale));old=list(map(F,p['limiting_room']));room=(old[0]-cost[1],old[1]-cost[0]);out={'status':'PASS_LIMITING_MOVEMENT_PROFILE_SCREEN_ONLY','target_exponent':'199/200','old_price_sha256':PIN,'added_owned_rank9_moves':2,'added_limiting_movement_cost':list(map(str,cost)),'remaining_nominal_limiting_room':list(map(str,room)),'approximate_cost':float(sum(cost)/2),'approximate_remaining_room':float(sum(room)/2),'finite_m_old_penalty_transferred':False,'old_caller_compatibility_proved':False,'unpaid_duties':['restore76 original D outputs','complete old I-G forward matrix on current a','compatible residual helper and full caller','all added ordinary work, dirty erasures, grid guards and recursion'],'no_new_kappa':True};a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
