#!/usr/bin/env python3
"""Independent direct-K signed-path and literal ordinary codec review."""
from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import argparse,gzip,hashlib,importlib.util,itertools,json
HERE=Path(__file__).resolve().parent;AUTHOR=HERE.parents[1]/'worker-a/signed-inverse-forward-runs';N=33
def need(x,m):
    if not x:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def main(output):
    need(sha(AUTHOR/'FREEZE.json')=='d84e6ea5d662c1fdf54e47955bbbb29fd4660053d784d038d2071df31dfc4203','author freeze')
    need(sha(AUTHOR/'PROOF.md')=='8878de72284ec4a02d928480f38e68a66e7768306885d2b86b557e11d6490937','author proof')
    need(sha(HERE/'matrix_review.py')=='81fa50e7f06db6a2dcc30d00e542acfdc7864c7ef45c85eeceb0216484b01849','credited earlier independent matrix engine')
    spec=importlib.util.spec_from_file_location('prior_direct_matrix_review',HERE/'matrix_review.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    for n,pin in [('R0-WORD.json.gz','d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c'),('ROUTES.json','ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a')]:need(sha(AUTHOR/'source'/n)==pin,'actual source pin')
    w=load(AUTHOR/'source/R0-WORD.json.gz');rt=load(AUTHOR/'source/ROUTES.json');receipt=load(AUTHOR/'RESULT.json')
    ports=w['logical_involution']['ports'];roles=w['logical_involution']['role_map'];X={int(h):i for h,i in roles['X'].items()};Y={int(h):i for h,i in roles['Y'].items()};R={h:{}for h in ports}
    for j in ports:
        state=[F(0)for _ in range(448)];state[X[j]]=F(1)
        for e in w['program']:
            if e[0]=='ADD':state[e[1]]+=F(e[3])*state[e[2]]
            else:need(e[0]=='MOVE','actual source alphabet')
        for h in ports:
            if state[Y[h]]:R[h][j]=state[Y[h]]
    rec={r['port']:r for r in rt['route_records']if r['stage']==1};q={h:rec[h]['normal']for h in ports};P={}
    for s,h in itertools.product((1,2,3),ports):
        bb=rec[h]['orthogonal_complement'];need(all(v.dot(a,b)==int(i==j)for i,a in enumerate([q[h]]+bb)for j,b in enumerate([q[h]]+bb)),'orthonormal head basis')
        vv=[b^(1<<(9+8*(s-1)+k))for k,b in enumerate(bb)];cols=[]
        for i in range(N):
            z=1<<i
            for a in vv:
                if v.dot(a,1<<i):z^=a
            cols.append(z)
        P[s,h]=tuple(cols)
    Fbody=tuple((1<<i)if i>=9 else 0 for i in range(N));counts=Counter();ranks={};full=0
    def visit(K,port,pattern):
        nonlocal full
        s=len(pattern)+1
        if s==4:return
        e=int(bool(pattern)and pattern[-1]=='+');need(v.apply(K,q[port])==e*q[port],'incoming current-port state')
        for h in R[port]:
            need(v.dot(q[h],q[port])==0 and R[h].get(port)==R[port][h],'authentic symmetric orthogonal edge')
            ph,pj=P[s,h],P[s,port];conj=[]
            for i in range(N):conj.append(v.apply(ph,v.apply(pj,v.apply(K,v.apply(pj,ph[i])))))
            need(v.apply(conj,q[h])==q[h],'new-stage removable normal')
            for sign in ('-','+'):
                update=q[h]if sign=='-'else v.apply(ph,q[port]);new=conj.copy()
                for i in v.bits(update):new[i]^=update
                p=pattern+sign;positive_runs=sum(c=='+'and(i==0 or p[i-1]=='-')for i,c in enumerate(p));want=24-len(p)+2*positive_runs
                need(v.rank(new)==want and all(v.apply(new,c)==c for c in new),'signed rank and projection')
                need(v.apply(new,q[h])==int(sign=='+')*q[h],'updated current-port state')
                counts[p]+=1;ranks[p]=want
                if p in ('+','+-','+-+'):
                    expected=list(Fbody)
                    if len(p)%2:
                        for i in v.bits(q[h]):expected[i]^=q[h]
                    need(new==expected,'full alternating kernel');full+=1
                visit(tuple(new),h,p)
    for h in ports:visit(Fbody,h,'')
    recipe=receipt['ordinary_R0_recipe'];census=Counter(op[0]for op in recipe)
    need(census=={'ADD':280,'SCALE':58,'SWAP':56},'literal ordinary invoice')
    scalars=set()
    def replay_column(j,ops):
        a=[F(i==j)for i in range(112)]
        for op in ops:
            if op[0]=='SWAP':need(op[1]!=op[2],'distinct swap');a[op[1]],a[op[2]]=a[op[2]],a[op[1]]
            elif op[0]=='SCALE':
                c=F(op[2]);need(c!=0,'nonzero scale');scalars.add(c);a[op[1]]*=c
            else:
                need(op[0]=='ADD'and op[1]!=op[2],'distinct additive register');c=F(op[3]);scalars.add(c);a[op[1]]+=c*a[op[2]]
            need(all(0<=i<112 for i in op[1:3]if isinstance(i,int)),'only original register indices')
        return a
    for j in range(112):need(replay_column(j,recipe)==[R[h].get(ports[j],F(0))for h in ports],'in-place recipe all independent columns')
    need(all(abs(c)<=2 and c.denominator&(c.denominator-1)==0 for c in scalars),'bounded dyadic scalar set')
    bad=[list(op)for op in recipe];z=next(op for op in bad if op[0]=='ADD');z[3]=str(-F(z[3]))
    need(any(replay_column(j,bad)!=[R[h].get(ports[j],F(0))for h in ports]for j in range(112)),'wrong codec sign is rejected')
    def reduce(word):
        stack=[]
        for x in word:
            if stack and((x=='Q'and stack[-1]=='q')or(x=='q'and stack[-1]=='Q')or(x.startswith('R')and stack[-1]==x)):stack.pop()
            else:stack.append(x)
        return stack
    word_checks=0
    for r in range(1,12):
        word=[]
        for s in range(1,r+1):word=reduce(([f'R{s}','Q']if s%2 else['q',f'R{s}'])+word)
        expected=([f'R{s}'for s in range(r,0,-1)]+['Q'])if r%2 else['q']+[f'R{s}'for s in range(r,0,-1)]+['Q']
        need(word==expected,'literal alternating product with Q order retained')
        if r%2:need(reduce([f'R{s}'for s in range(1,r+1)]+word)==['Q'],'ordered odd decoder')
        else:
            # The retained D conjugation sends R_s to q Rprime_s Q.
            expansion=[]
            for s in range(r,0,-1):expansion+=['q',f'R{s}','Q']
            need(reduce(expansion)==word,'even D-conjugation product')
            need(reduce([f'R{s}'for s in range(r,0,-1)]+[f'R{s}'for s in range(1,r+1)])==[],'ordered even preencoder')
        word_checks+=1
    need(reduce(['R3','R2','R1','R3','R2','R1'])!=[],'wrong decoder order not silently commuted')
    data={'status':'PASS_INDEPENDENT_SIGNED_RUN_TARGET_REVIEW','path_counts':dict(sorted(counts.items())),'path_ranks':dict(sorted(ranks.items())),'full_alternating_kernels_checked':full,'ordinary_recipe_columns':112,'ordinary_recipe_census':dict(census),'ordinary_scalar_set':sorted(map(str,scalars)),'exact_normal_form_prefix_controls':word_checks,'controls':['wrong codec sign','wrong decoder order'],'scope':'All-width signed-chain theorem and exact odd/even target interfaces. No complete caller or shared preencoding compatibility inferred.','new_kappa':False}
    output.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in data.items()if k not in ('path_counts','path_ranks')},sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--output',type=Path,default=HERE/'RESULT.json');a=p.parse_args();AUTHOR=a.author;main(a.output)
