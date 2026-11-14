#!/usr/bin/env python3
"""Independent operator replay in four faithful Q sectors, with formal bodies."""
import argparse,collections,copy,hashlib,json
from pathlib import Path
from fractions import Fraction as F
import sympy as s
def need(v,msg):
    if not v:raise ValueError(msg)
def replay(program,Q,D):
    m=Q.rows;eye=s.eye(4*m);rows=[eye[i*m:(i+1)*m,:]for i in range(4)]
    lam={a:((1+a*s.I)*s.eye(m)+(1-a*s.I)*Q**2)/2 for a in [-1,1]}
    for op in program:
        tag=op[0]
        if tag=='LAMBDA':rows[op[1]]=lam[op[2]]*rows[op[1]]
        elif tag=='SCALE':rows[op[1]]=s.sympify(op[2])*rows[op[1]]
        elif tag=='SWAP':rows[op[1]],rows[op[2]]=rows[op[2]],rows[op[1]]
        elif tag=='QUERY':
            _,dst,src,power=op;need(dst!=src,'nonself query');rows[dst]+=Q**power*rows[src]
        elif tag=='HOST2':
            _,stage,indices=op;need(len(set(indices))==4,'four independent roles');x,y,u,v=indices;old=[r.copy()for r in rows];body=D[stage]
            rows[x]=body*old[x];rows[y]=body*(old[y]+Q**-1*old[x]);rows[u]=body*(old[u]-Q*old[v]);rows[v]=body*old[v]
        else:raise ValueError(tag)
        rows=[r.applyfunc(s.expand)for r in rows]
    return s.Matrix.vstack(*rows)
def equal(a,b):return all(s.expand(x-y)==0 for x,y in zip(a,b))
def bound(x):
    scale=10**28;target=x**199*scale**200;lo,hi=0,x*scale+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=target:lo=mid
        else:hi=mid
    return F(lo,scale),F(hi,scale)
def invoice(n,queries,rank):
    terms=[(448,rank),(-112*queries,1)]+[(-224*n,r)for r in [2,3,5,6]];lo=hi=F(0)
    for c,r in terms:
        a,b=bound(r)
        if c<0:a,b=b,a
        lo+=c*a;hi+=c*b
    need(lo>0,'conditional margin');return[str(lo),str(hi)]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    proof='effcfc36589a2f977922f9dceb98cdcf3bb538bab583592e06fdedd12ad46de1';manifest='16ffa4019dde4b75c2310db74c1af9184fca7ada9f6c1ee589dd0946471fb7bf'
    for p,pin in [('PROOF.md',proof),('MANIFEST.json',manifest)]:need(hashlib.sha256((a.author/p).read_bytes()).hexdigest()==pin,p+' pin')
    D=s.symbols('D1 D2 D3');bodies={i+1:s.Matrix([[d]])for i,d in enumerate(D)};receipts=[]
    for name,n,queries in [('two_native_two_query',2,2),('three_native_zero_query',3,0)]:
        p=a.author/(name+'.json');w=json.loads(p.read_text());sectors=[]
        for q in [s.Integer(1),s.Integer(-1),s.I,-s.I]:
            out=replay(w['program'],s.Matrix([[q]]),bodies);target=s.eye(4)*q**-1*s.prod(D[:n]);need(equal(out,target),'faithful Q sector '+str(q))
            sectors.append({'q':str(q),'diagonal':str(s.expand(q**-1*s.prod(D[:n]))),'off_diagonal_zero':True})
        census=dict(collections.Counter(x[0]for x in w['program']));need(census.get('HOST2',0)==n and census.get('QUERY',0)==queries,'paid census')
        receipts.append({'word':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'events':len(w['program']),'census':census,'sectors':sectors,'conditional_R0_profile_margin':invoice(n,queries,1+8*n)})
    w=json.loads((a.author/'two_native_two_query.json').read_text())['program'];Q=s.diag(1,s.I);db={1:s.Matrix([[0,1],[1,0]]),2:s.eye(2),3:s.eye(2)}
    need(not equal(replay(w,Q,db),s.diag(*([Q**-1*db[1]*db[2]]*4))),'noncommuting-body counterexample')
    mutants=[]
    for name in ['missing_query','repeat_body']:
        p=copy.deepcopy(w)
        if name=='missing_query':p.pop(next(i for i,x in enumerate(p)if x[0]=='QUERY'))
        else:p[next(i for i,x in enumerate(p)if x[0]=='HOST2' and x[1]==2)][1]=1
        need(not equal(replay(p,s.Matrix([[s.I]]),bodies),s.eye(4)*(-s.I)*D[0]*D[1]),name);mutants.append(name)
    out={'status':'PASS_ROOT_INDEPENDENT_COMMON_Q_CALLER_REVIEW','reviewed_proof':proof,'author_manifest':manifest,'implementation':'SymPy1.14 exact Gaussian algebra; formal D exponents; no author imports','faithfulness':'q^4-1 has four distinct roots; exact identities in all four sectors prove the commuting operator polynomial identity','words':receipts,'controls':{'noncommuting_body_counterexample_rejected':True,'mutants':mutants},'scope':'Common-Q controls only. Actual R0 replacement and every physical expense remain open. Conditional prices are not supplier certificates. No new kappa.'}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'conditional_margins':[float(F(x['conditional_R0_profile_margin'][0]))for x in receipts],'noncentral_countercontrol':True}))
if __name__=='__main__':main()
