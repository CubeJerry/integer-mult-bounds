#!/usr/bin/env python3
"""Lead's independent scalar census on the authenticated literal word."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
def need(x,m):
    if not x:raise ValueError(m)
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin');w=json.loads(gzip.decompress(raw));blob=a.word.read_bytes();q=json.loads(gzip.decompress(blob));need(len(q['program'])==len(q['marks']),'one purpose per operation');native=[];added=collections.Counter();base=collections.Counter();maxbits=[0,0]
for e,mark in zip(q['program'],q['marks']):
    if mark=='original_common_word':
        f=list(e);f[1]-=400 if f[1]>=1880 else 0
        if f[0] in ('ADD','COPY'):f[2]-=400 if f[2]>=1880 else 0
        native.append(f)
    if e[0] in ('ADD','COPY','SCALE'):
        x=F(e[2] if e[0]=='SCALE' else e[3]);d=x.denominator
        while d%2==0:d//=2
        if mark=='original_common_word':base[d]+=1
        else:
            added[(mark,d)]+=1;maxbits=[max(maxbits[0],abs(x.numerator).bit_length()),max(maxbits[1],x.denominator.bit_length())]
need(native==w['program'],'complete native subsequence authenticates purpose tags')
non={str(k):v for k,v in added.items() if k[1]!=1};need(non=={"('common_hub_correction', 5)":3471,"('receiver_history_accumulation', 3)":1},'new odd denominator counts');need(sum(v for d,v in base.items() if d!=1)==4143,'original odd denominator count');need(maxbits==[29,23],'new scalar bit lengths')
r=dict(status='PASS_INDEPENDENT_UNIT17_SCALAR_CENSUS',word_sha256=hashlib.sha256(blob).hexdigest(),source_sha256=hashlib.sha256(raw).hexdigest(),authenticated_native_instructions=len(native),new_non_dyadic_occurrences=non,original_non_dyadic_occurrences=4143,new_max_numerator_denominator_bits=maxbits,scope='Exact scalar accounting only; no dyadic compiler or precision admission is supplied.')
a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
