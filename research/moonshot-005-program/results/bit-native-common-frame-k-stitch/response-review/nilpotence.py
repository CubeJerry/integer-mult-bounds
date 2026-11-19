#!/usr/bin/env python3
"""Supplement to the independently evaluated full five-tile response."""
from argparse import ArgumentParser
from pathlib import Path
import json
import check as engine
p=ArgumentParser();p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
w=engine.load(a.word,'word');cols={z:i for i,z in enumerate(sorted(engine.public_bits(w)))}
b,_=engine.evaluate(w,cols);inverse={i:z for z,i in cols.items()};inputs=set()
for row in b.values():
 while row:
  low=row&-row;inputs.add(inverse[low.bit_length()-1]//5);row^=low
outputs={z//5 for z in b};assert outputs.isdisjoint(inputs)
o={'status':'PASS_FULL_RESPONSE_COORDINATE_NILPOTENCE','word_sha256':engine.PINS['word'],'proper_output_field_count':len(outputs),'proper_input_field_count':len(inputs),'intersection_count':0,'input_fields':sorted(inputs),'output_fields':sorted(outputs),'conclusion':'B squared is zero; I+B is its own inverse in characteristic two. This is coordinate support of the fixed word, not disjoint native donor/receiver roles.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(o,indent=2)+'\n');print(o['status'])
