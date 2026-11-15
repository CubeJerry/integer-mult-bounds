#!/usr/bin/env python3
import argparse,json,hashlib
from pathlib import Path
import sympy as s
def basis(rows):
    b={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k in b:x^=b[k]
            else:b[k]=x;break
    return b
def has(b,x):
    while x:
        k=x.bit_length()-1
        if k not in b:return False
        x^=b[k]
    return True
p=argparse.ArgumentParser();p.add_argument('--prefix',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
raw=a.source.read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';roots=json.loads(raw)['native_roots'];prefix=json.loads(a.prefix.read_text());word=json.loads(a.word.read_text());n=len(prefix['operations'])
assert word['operations'][:n]==prefix['operations'];names=['DC1_1','DC1_2','DC2_1'];assert word['operations'][n:]==[['MOVE',x,'SHARED5']for x in names]
v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};chart={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
for op in prefix['operations']:
    if op[0]=='INIT':v[op[1]]=0;chart[op[1]]=op[2]
    elif op[0]=='ADD':v[op[2]]^=v[op[1]]
    elif op[0]=='MOVE':chart[op[1]]=op[2]
    elif op[0]=='CLEAR':del v[op[1]];del chart[op[1]]
M=word['charts']['SHARED5']['rows'];assert s.Matrix(M).rank()==3
drops=[]
for name in names:
    before=word['charts'][chart[name]];assert before['kind']=='ann';r=s.Matrix(before['rows']).rank();assert s.Matrix(M+before['rows']).rank()==3;drops.append(3-r)
assert drops==[2,1,2]
G=[v[f'P{i}']for i in range(8)]+[1<<j for j in [16,19,38,49,50,56,57]];Z=[v[x]for x in names];assert len(basis(G))==15 and len(basis(G+Z))==18
reached=[i for i,r in enumerate(roots)if s.Matrix(M+[r]).rank()==3];assert reached==[0,63]
def fits(rows,i):
    outside=sum(1<<j for j,r in enumerate(roots)if sum(x*y for x,y in zip(roots[i],r))!=0)
    return has(basis([x&outside for x in rows]),1<<i)
old=[i for i in range(111)if fits(G,i)];glob=[i for i in range(111)if fits(G+Z,i)];actual=[i for i in range(111)if fits(G+Z if i in reached else G,i)]
assert len(old)==10 and set(glob)-set(old)=={26} and actual==old
F=[0,15,31,35,40,41,106,110];F2=[0,22,23,30,32,60,61,107]
project=lambda rows,frame:[sum(((x>>j)&1)<<i for i,j in enumerate(frame))for x in rows]
assert len(basis(project(G,F)))==5 and len(basis(project(G+Z,F)))==8
assert len(basis(project(G+Z,F2)))==5
assert all((x&z).bit_count()%2==0 for x in project(G+Z,F2)for z in [7,9,19])
support=[i for i in range(111)if v['DC1_2']>>i&1];assert support==[5,15,26,41,57,89,110]
assert all(sum(x*y for x,y in zip(roots[26],roots[j]))==0 for j in support if j!=26)
result={'status':'PASS_ROOT_SHARED_RESERVOIR_AND_ACCESS_GATE','formal_prefix_inputs':222,'literal_descents':drops,'global_rank':18,'reachable_receiver_facets':reached,'global_feasible_roles':glob,'actual_chart_relaxation_feasible_roles':actual,'no_added_chart_feasible_role':True,'first_frame_rank':8,'second_frame_rank':5,'receiver26_single_cache_support':support,'new_kappa':False}
a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
