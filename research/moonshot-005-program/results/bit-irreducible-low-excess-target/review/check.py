import argparse,gzip,hashlib,json
from pathlib import Path
def rank(vectors):
    p={}
    for x in vectors:
        while x:
            k=(x&-x).bit_length()-1
            if k not in p:p[k]=x;break
            x^=p[k]
    return len(p)
def entries(k,w):
    if k==0:return [(r,r+1) for r in range(w-1)]
    if k==1:return [(w-1,0)]
    return [(r,(k-1)*w+r) for r in range(w)]
def action(pairs,x):
    y=0
    for r,c in pairs:
        if x>>c&1:y^=1<<r
    return y
def native(roots):
    nb=[{j for j,v in enumerate(roots) if j!=i and sum(a*b for a,b in zip(u,v))==0} for i,u in enumerate(roots)]
    cols=[sum(1<<i for i in range(111) if i==j or i in nb[j]) for j in range(111)]
    assert rank(cols)==9 and sum(map(len,nb))==6470 and 10 not in nb[80]
    assert (len(nb[80]),len(nb[10]))==(62,61)
    reached={0}
    while True:
        more=reached|set().union(*(nb[i] for i in reached))
        if more==reached:break
        reached=more
    assert len(reached)==111
    for s in [nb[80]|{10},nb[10]|{80}]:assert rank([v for j,v in enumerate(cols) if j not in s])==9
    return nb,cols
def full_columns(nb,K,w):
    b=60*w;n=111*b
    columns=[sum(1<<(i*b+k) for i in range(111) if K[j]>>i&1) for j in range(111) for k in range(b)]
    delta=[0]*n;changed={}
    for index,j in enumerate(sorted(nb[80])):
        if index<61:changed[80,j]=entries(index,w)
    for index,i in enumerate(sorted(nb[10])):changed[i,10]=[(c,r) for r,c in entries(index,w)]
    assert len(changed)==122 and all((j,i) not in changed for i,j in changed)
    for (i,j),pairs in changed.items():
        for r,c in pairs:delta[j*b+c]^=1<<(i*b+r)
        assert rank([(1<<c)^action(pairs,1<<c) for c in range(b)])==b
    q=rank([x^d for x,d in zip(columns,delta)]);rr=rank(columns+delta)-9*b
    assert rank(delta)==2*w and q==9*b+2*w and rr==2*w
    return {'w':w,'b':b,'matrix_dimension':n,'fitting_rank':q,'delta_rank':2*w,'retained_quotient_rank':rr,'nonidentity_blocks':len(changed)}
def algebra(w):
    b=60*w;J=entries(0,w);E=entries(1,w);checked=0
    for r in range(w):
        for s in range(w):
            for t in range(w):
                x=1<<t
                for _ in range(s):x=action(J,x)
                x=action(E,x)
                for _ in range(w-1-r):x=action(J,x)
                assert x==((1<<r) if t==s else 0);checked+=1
    for l in range(1,60):
        N=entries(l+1,w);Nt=[(c,r) for r,c in N]
        for t in range(w):assert action(N,1<<(l*w+t))==1<<t and action(Nt,1<<t)==1<<(l*w+t)
    rows=[];images=[]
    for k in range(61):
        pairs=entries(k,w);rows.extend(sum(1<<c for rr,c in pairs if rr==r) for r in range(b));images.extend(action(pairs,1<<c) for c in range(b))
    assert rank(rows)==b and rank(images)==w
    assert action(J,1)==0 and action(E,1)==1<<(w-1)
    return {'w':w,'central_basis_action_checks':checked,'full_right_kernel':0,'one_sided_image_dimension':w,'transport_coordinates':b}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
    p=a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';raw=gzip.decompress(p.read_bytes());layout=json.loads(raw)
    nb,K=native(layout['root_table'][:111]);full=full_columns(nb,K,4);alg=[algebra(w) for w in [4,5,8]]
    out={'status':'PASS_INDEPENDENT_IRREDUCIBLE_TARGET','layout_sha256':hashlib.sha256(raw).hexdigest(),'literal_native_control':full,'algebra_controls':alg,'author_code_imported':False,'physical_realization':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
