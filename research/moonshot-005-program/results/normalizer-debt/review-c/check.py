#!/usr/bin/env python3
"""Independent sparse zero-character replay and completed-row gate review.
No author builder/replay imported. @CubeJerry/OpenAI.
"""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parents[2];AUTHOR=BASE/'worker-b/normalizer-debt'
def need(x,m):
    if not x:raise ValueError(m)
def add(a,b,c=1):
    z=dict(a)
    for j,v in b.items():
        x=z.get(j,0)+c*v
        if x:z[j]=x
        else:z.pop(j,None)
    return z
def eye(n):return[{i:1}for i in range(n)]
def literal(c,omitted):
    rows=eye(c['roles']);stages=[]
    for e in c['events']:
        op=e[0]
        if op in('ADD','QUERY'):rows[e[1]]=add(rows[e[1]],rows[e[2]],int(e[3])if op=='ADD'else 1)
        elif op=='SCALE':rows[e[1]]={j:int(e[2])*v for j,v in rows[e[1]].items()}
        elif op=='SWAP':rows[e[1]],rows[e[2]]=rows[e[2]],rows[e[1]]
        elif op=='HOST2':
            _,s,x,y,u,v=e;stages.append(s);rows[y]=add(rows[y],rows[x]);rows[u]=add(rows[u],rows[v],-1)
            for bit,r in[(2*(s-1),y),(2*(s-1)+1,v)]:
                if bit in omitted:rows[r]={j:-z for j,z in rows[r].items()}
        else:need(op in('LAMBDA','IDLE_ONE'),'literal zero-character opcode')
    need(stages==list(range(1,2*c['arms']+1)),'all actual chronological native invocations')
    return rows
def rankone(rows,x,y,coefficient):
    value={}
    for j,c in y.items():value=add(value,rows[j],c)
    out=[dict(r)for r in rows]
    for i,c in x.items():out[i]=add(out[i],value,coefficient*c)
    return out
def formulas(a,omitted):
    L=2*a+1;rows=eye(2*L)
    for side in[0,1]:
        for i in range(1,a+1):
            stage=side*a+i-1
            if 2*stage in omitted:
                if side==0:x={0:1,i:1,**{j:2 for j in range(1,i)}};y={0:1}
                else:x={0:-1,a+i:1,**{a+j:2 for j in range(i+1,a+1)}};y={0:1,a+i:2}
                rows=rankone(rows,x,y,-2)
            if 2*stage+1 in omitted:
                if side==0:x={L+i:1};y={L:1,L+i:-1}
                else:x={L:-2,L+a+i:1,**{L+a+j:4 for j in range(i+1,a+1)}};y={L:1,L+a+i:1}
                rows=rankone(rows,x,y,2)
    return rows
def witness(a,omitted,rows):
    L=2*a+1;out=[]
    for bit in sorted(omitted):
        stage,isV=divmod(bit,2);i=stage%a+1
        if stage<a and not isV:r=i;j=0;z=rows[r].get(j,0);need(z%4==2,'left-Y invariant modulo four')
        elif stage>=a and not isV:r=j=a+i;z=rows[r].get(j,0);need(z==-3,'right-Y diagonal invariant')
        elif stage<a:r=j=L+i;z=rows[r].get(j,0);need(z==-1,'left-V diagonal invariant')
        else:r=j=L+a+i;z=rows[r].get(j,0);need(z==3,'right-V diagonal invariant')
        out.append([bit,r,j,z])
    return out
def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def root(v):
    if v.bit_count()==3:return[2 if v>>i&1 else-1 for i in range(9)]
    off=[i for i in range(9)if not(v>>i&1)];need(len(off)==2,'native root');return[3*(int(i==off[0])-int(i==off[1]))for i in range(9)]
def span(vs):
    s={0}
    for v in vs:s|={x^v for x in tuple(s)}
    return s
def source(w):
    m=w['logical_involution'];P=m['ports'];v={int(h):x for h,x in m['normals'].items()};rho={h:root(v[h])for h in P};G={h:{j:F(sum(a*b for a,b in zip(rho[h],rho[j])),18)for j in P}for h in P}
    classes={h:k for k,z in enumerate(m['groups'])for h in z['ports']};R={h:{j:F(h==j)-(G[h][j]if classes[h]==classes[j]else 0)for j in P}for h in P}
    R={h:{j:c for j,c in row.items()if c}for h,row in R.items()};need(R=={int(h):{int(j):F(c)for j,c in row.items()}for h,row in m['R_rows'].items()},'coupling independently reconstructed from integer roots')
    h=P[0];eig={j:F(j==h)-R[j].get(h,0)for j in P};eig={j:c for j,c in eig.items()if c}
    need(eig and all(sum(c*eig.get(j,0)for j,c in R[i].items())==-eig.get(i,0)for i in P),'genuine112-dimensional negative eigenvector')
    halves={}
    for z in m['halves']:halves.setdefault(z['class'],[]).append(z['ports'])
    geometry=[]
    for cl,(A,B)in sorted(halves.items()):
        need(len(A)==len(B)==4 and all(((v[i]&v[j]).bit_count()%2)==int((i in A)==(j in A))for i in A+B for j in A+B),'exact binary pairing diag(J4,J4)')
        need(all(G[i][j]==int(i==j)for half in[A,B]for i in half for j in half),'two actual identity-four diagonal Gram blocks')
        W=span(v[h]for h in A+B);K={x for x in W if all((x&v[h]).bit_count()%2==0 for h in A+B)}
        need(len(W)==16 and len(K)==4 and all(K<span(v[h]for h in half)<W for half in[A,B]),'true W4 K2 and nested half charts')
        modes=m['groups'][cl]['modes'];coords={h:{i:F(sum(a*b for a,b in zip(rho[h],root(m['omitted_frame'][i]))),18)for i in modes}for h in A+B}
        need(len(modes)==4 and all(coords[h][i]for h in A+B for i in modes),'four genuine full-class scalar modes')
        need(all(sum(coords[h][i]*coords[j][i]for i in modes)==G[h][j]for h in A+B for j in A+B),'positive four-row factorization saturates both diagonal rank counts')
        geometry.append({'class':cl,'A':A,'B':B,'W':sorted(W),'K':sorted(K),'ideal_completed_row_control_modes':modes,'ideal_per_plane_profile':{2:4}})
    return eig,geometry
def tariffs():
    B=10**35;cache={}
    def power(n):
        if n not in cache:
            z=n**199*B**200;lo=0;hi=n*B+1
            while hi-lo>1:
                x=(lo+hi)//2
                if x**200<=z:lo=x
                else:hi=x
            need(lo**200<=z<hi**200,'exact rational tariff enclosure');cache[n]=(F(lo,B),F(hi,B))
        return cache[n]
    def moment(d):return[sum(c*power(n)[k]for n,c in d.items())for k in[0,1]]
    g=moment({2:112});codec=moment({1:448,2:560,5:448});old=load(AUTHOR/'source/R0-price.json');cap=list(map(F,old['sources']['R0-minimal']['conditional_twelve_stage_margin_per_native']));outside=list(map(F,old['conditional_outside_allowance_per_native']))
    need(g[0]>cap[1]and codec[0]>outside[1],'both separately scoped all-free-extra preflights fail')
    return {'completed_row_lower_moment':g,'available_repair_allowance':cap,'optimistic_codec_profile':{1:448,2:560,5:448},'optimistic_codec_moment':codec,'outside_allowance':outside}

PINS={'MANIFEST.json':'77329f4a27523f8bb2b840fd56114b9e3e76d37822c6ac1b14fee8a5b7a4e3e5','PROOF.md':'cd0ca7657362114cc966f76a631cb43c1ccf3a1941ff55c54099b77152622747','CLASS-GATE.md':'78c913ee67b1dd5bf4ce612b9708e2fa7ebad7e092e8e6c62772a3d99d449a34','source/R0-minimal.json.gz':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336','output/a1/CALLER.json.gz':'9afe985ad5788ffca2f4f533ad080c19d34b2d987e14f68dec3634a0f022c21a','output/a2/CALLER.json.gz':'b2ba96e30e1661e5e5df55d6177aeb89710c0fb73d2f42467ae1c3e5a01fbdb0','output/a6/CALLER.json.gz':'d5bf995d3994371463594df46b2ee167983f60a862feb0b3ddb706aaba7f95bc'}
def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return{str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(list,tuple)):return[enc(v)for v in x]
    return x
def main():
    global AUTHOR
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();AUTHOR=a.author
    for path,pin in PINS.items():need(hashlib.sha256((AUTHOR/path).read_bytes()).hexdigest()==pin,'frozen source pin '+path)
    w=load(AUTHOR/'source/R0-minimal.json.gz');eig,geometry=source(w);receipts=[]
    for arms in[1,2,6]:
        c=load(AUTHOR/f'output/a{arms}/CALLER.json.gz');need(c['arms']==arms and c['roles']==4*arms+2 and c['body_dimension']==8,'literal caller shape')
        need(literal(c,set())==eye(c['roles']),'all services present positive control')
        if arms<3:patterns=[{j for j in range(4*arms)if mask>>j&1}for mask in range(1,1<<(4*arms))]
        else:
            patterns=[{j}for j in range(4*arms)]+[set(range(4*arms)),set(range(0,4*arms,2)),set(range(1,4*arms,2)),set(range(2*arms)),set(range(2*arms,4*arms)),{j for j in range(4*arms)if j%3==0}]
        for omitted in patterns:
            rows=literal(c,omitted);need(rows==formulas(arms,omitted),'all four exact rank-one site formulas match the full literal caller')
            need(rows!=eye(c['roles']),'every nonempty tested omission fails');witness(arms,omitted,rows)
        allrows=literal(c,set(range(4*arms)));want={0:(4*(-1)**arms-5**arms)//3,**{arms+i:4*(-5)**(arms-i)for i in range(1,arms+1)}};need(allrows[0]==want,'exact all-omitted closed root formula')
        receipts.append({'arms':arms,'patterns':len(patterns),'all_patterns':arms<3,'all_omitted_root':allrows[0],'all_omitted_leaf_witnesses':witness(arms,set(range(4*arms)),allrows)})
    out={'status':'PASS_INDEPENDENT_UNCHANGED_CALLER_OMISSION_AND_CLASS_ROW_GATE','source_pins':PINS,'actual_negative_eigenvector':eig,'omission_checks':receipts,'class_geometry':geometry,'tariffs':tariffs(),'scope':'Universal omission proof reviewed directly; finite literal replays verify the four site formulas. Separate row tariff assumes completed separate chains, one class, no productive credits. Neither is a general lower bound on N or a new kappa.'}
    a.output.write_text(json.dumps(enc(out),sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'patterns':sum(r['patterns']for r in receipts),'class_gate':float(out['tariffs']['completed_row_lower_moment'][0])}))
if __name__=='__main__':main()
