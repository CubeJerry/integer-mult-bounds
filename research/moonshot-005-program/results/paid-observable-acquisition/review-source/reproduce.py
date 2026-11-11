"""Reproduce the completed independent forward source-row audit."""
import argparse,gzip,hashlib,importlib.util,json
from fractions import Fraction
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--interpreter',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
b=a.source.read_bytes()
if hashlib.sha256(b).hexdigest()!='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883':raise ValueError('native source pin')
if hashlib.sha256(a.interpreter.read_bytes()).hexdigest()!='4c0eb22f56d34054675d90ac02e77ac113fa45c742063508de34c5c0d81f63a4':raise ValueError('independent interpreter pin')
s=importlib.util.spec_from_file_location('independent_forward',a.interpreter);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);w=json.loads(gzip.decompress(b));M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);_,_,snap=v.replay(w,w['program'],M,{30823:130,30824:1481});r=snap[30824];m=snap[30823];entry={q for q in M if w['initial'][q]==3};union=set(r)|set(m)
result={'source_sha256':v.NATIVE,'r':{str(q):str(x) for q,x in sorted(r.items())},'Mnew':{str(q):str(x) for q,x in sorted(m.items())},'entry_union':sorted(union&entry),'nonentry_union':sorted(union-entry),'minor_entry':str(r.get(129,Fraction(0))*m.get(130,Fraction(0))-r.get(130,Fraction(0))*m.get(129,Fraction(0))),'minor_nonentry':str(r.get(2,Fraction(0))*m.get(4,Fraction(0))-r.get(4,Fraction(0))*m.get(2,Fraction(0)))}
a.output.write_text(json.dumps(result,indent=2)+'\n')
print('PASS_INDEPENDENT_FORWARD_SOURCE_SPLIT')
