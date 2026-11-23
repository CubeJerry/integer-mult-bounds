"""Exact source replay and independent scalar oracle for the caller boundary."""
import argparse, ast, hashlib, json
from fractions import Fraction
from pathlib import Path
HERE = Path(__file__).resolve().parent
def require(test, message):
    if not test: raise ValueError(message)
def extract(file, names, ns):
    nodes=[x for x in ast.parse((HERE/'retained'/file).read_text()).body
           if isinstance(x,ast.FunctionDef) and x.name in names]
    require({x.name for x in nodes}==set(names),'source functions')
    exec(compile(ast.Module(body=nodes,type_ignores=[]),file,'exec'),ns)
def main():
    bindings=json.loads((HERE/'ORIGINS.json').read_text())['files']
    for name, record in bindings.items():
        b=(HERE/'retained'/name).read_bytes()
        require(hashlib.sha256(b).hexdigest()==record['sha256'],name+' SHA256')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==record['git_blob'],name+' blob')
    ns={'Fraction':Fraction,'require':require}
    extract('cover.py',{'residue','row_program'},ns)
    extract('quotient_route.py',{'positions','multiply_row','reduce_row','canonical_right','right_matrix'},ns)
    graph=json.loads((HERE/'retained/graph.json').read_text())
    caller=json.loads((HERE/'retained/caller.json').read_text())
    vectors=graph['frames'][str(graph['start'][17])]['B']+graph['frames'][str(graph['final'][caller['ports']+17])]['B']
    S=tuple(zip(*vectors,strict=True)); n=len(S)
    require(n==8,'dimension')
    word=ns['row_program'](S,3)
    require(ns['right_matrix'](n,word,27)==tuple(tuple(x%27 for x in row) for row in S),'source endpoint')
    I=tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
    low,_=ns['canonical_right'](I,S,3)
    fields=[(i,j) for i,cols in enumerate(ns['positions'](low)) for j in cols]
    require(fields[15]==(2,1),'field index')
    cases=0
    def value(a,b,w):
        nonlocal cases
        m=3**w; rows=[list(r) for r in I];rows[0][0]+=3*a;rows[0][2]+=3*b
        out,L=ns['canonical_right'](rows,S,m)
        require(tuple(tuple(x%3 for x in r) for r in out)==low,'fixed low')
        A=1+3*a; B=3*b; y=-A*pow(A+B,-1,m)%m
        require(out[2][1]==y,'independent scalar formula')
        for i in range(n):
            for j in range(n):
                require(sum(rows[i][k]*S[k][j] for k in range(n))%m==sum(L[i][k]*out[k][j] for k in range(n))%m,'gS=LY')
        cases+=1
        return (y-2)//3
    for a in range(9):
        for b in range(9):value(a,b,3)
    def corners(w):return [value(a,b,w) for a,b in ((0,0),(1,0),(0,1),(1,1))]
    c=corners(3);require(c==[8,8,6,3],'four corners')
    for w in range(3,21):
        t=corners(w);side=3**(w-1);delta=(t[3]-t[1]-t[2]+t[0])%side
        require(delta==-3*pow(28,-1,side)%side and delta!=0,'all-width formula')
    t=corners(2);require((t[3]-t[1]-t[2]+t[0])%3==0,'first-order control')
    require((c[1]+c[2]-c[0])%9!=c[3],'fixed affine counterfeit')
    receiver=(HERE/'retained/receiver-before-patch.py').read_text().replace('from same_order_body import SameOrderBody, same_order_line','from same_order_body import SameOrderBody\nfrom five_exchange import same_order_line')
    require(hashlib.sha256(receiver.encode()).hexdigest()=='5d9faeabe8ccc4a4ccf670f91322016cf33b2c2a497fd78b41f3750fbadae560','current patch')
    return {'status':'pass','canonical_cases':cases,'source_files':len(bindings),'source_word_length':len(word),'corner_values_mod9':c,'mixed_difference_mod9':6,'widths_checked':list(range(3,21)),'negative_control_families':2,'scope':'obstruction to fixed-affine quotient shortcut; no source correctness defect'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args()
    result=json.dumps(main(),indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(result)
    else:print(result,end='')
