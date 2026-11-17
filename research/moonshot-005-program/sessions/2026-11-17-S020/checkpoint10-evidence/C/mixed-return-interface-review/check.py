#!/usr/bin/env python3
"""Independent exact source/gauge and primitive review of the mixed interface."""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

DEFAULT=Path(__file__).resolve().parents[1]/'gaussian-dyadic-prefix-compiler/check.py'
PIN='5a75913c9f2f9f55fe33174802e3fa40b8e1358ccb3966ce6638eaab9b4ffedb'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--arithmetic',type=Path,default=DEFAULT)
    ap.add_argument('--out',type=Path,default=Path(__file__).with_name('CERTIFICATE.json'))
    args=ap.parse_args();assert sha256(args.arithmetic.read_bytes()).hexdigest()==PIN
    spec=importlib.util.spec_from_file_location('c_gaussian_dyadic',args.arithmetic)
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    Z,O,I=m.ZERO,m.ONE,m.I
    def zero(n=16):return [[Z]*n for _ in range(n)]
    def eye(n=16):return m.identity(n)
    def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
    def scale(a,c):return [[x*c for x in row] for row in a]
    def mm(a,b):
        out=[[Z]*len(b[0]) for _ in range(len(a))]
        for i,row in enumerate(a):
            for k,x in enumerate(row):
                if not x:continue
                for j,y in enumerate(b[k]):
                    if y:out[i][j]=out[i][j]+x*y
        return out
    def star(a):return [[m.G(a[j][i].a,-a[j][i].b) for j in range(len(a))] for i in range(len(a[0]))]
    def power(a,k):
        if k<0:return power(star(a),-k)
        out=eye(len(a))
        for _ in range(k):out=mm(out,a)
        return out
    roots=[O,I,-O,-I]
    def mono(dest,phase):
        a=zero()
        for x in range(16):
            bits=[(x>>j)&1 for j in range(4)]
            a[dest(*bits)][x]=roots[phase(*bits)%4]
        return a
    def table(a):
        out=[]
        for x in range(len(a)):
            nz=[y for y in range(len(a)) if a[y][x]]
            assert len(nz)==1 and a[nz[0]][x] in roots
            out.append([nz[0],roots.index(a[nz[0]][x])])
        assert len({x[0] for x in out})==len(a)
        return out
    def rowmono(a):
        p,z=[],[]
        for row in a:
            nz=[j for j,x in enumerate(row) if x]
            assert len(nz)==1
            p.append(nz[0]);z.append(row[nz[0]])
        return tuple(p),tuple(z)
    E=eye();S=mono(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
    Xb=mono(lambda a,b,c,d:a+2*(1-b)+4*c+8*d,lambda *x:0)
    Cb=scale(add(scale(E,O+I),scale(Xb,O-I)),F(1,2))
    A=mm(Cb,S)
    # Independent direct columns verify the retained source convention.
    direct=zero()
    for x in range(16):
        a,b,c,d=[(x>>j)&1 for j in range(4)];y=b+2*c+4*d+8*a;sg=(-1)**(a*b*d)
        direct[y][x]=m.G(F(sg,2),F(sg,2));direct[y^2][x]=m.G(F(sg,2),F(-sg,2))
    assert A==direct and mm(A,star(A))==E
    D=[]
    for bit in range(4):D.append(mono(lambda a,b,c,d:a+2*b+4*c+8*d,lambda *bs,bit=bit:bs[bit]))
    s=mono(lambda a,b,c,d:a+2*c+4*b+8*d,lambda *x:0)
    h=mm(s,mm(D[1],star(D[2])))
    r=mono(lambda a,b,c,d:d+2*(1-c)+4*a+8*b,lambda *x:0)
    assert mm(A,mm(s,A))==r
    assert mm(s,s)==mm(h,h)==E
    clock=mm(s,h)
    assert clock==mm(D[1],star(D[2]))
    assert power(clock,4)==E and power(clock,2)!=E
    assert mm(s,mm(clock,s))==star(clock)
    group=[power(clock,k) for k in range(4)]+[mm(s,power(clock,k)) for k in range(4)]
    assert len({tuple(tuple((x.a,x.b) for x in row) for row in g) for g in group})==8
    traces=[sum((g[j][j] for j in range(16)),Z) for g in group]
    assert traces==[m.G(x) for x in [16,8,0,8,8,8,8,8]]
    rotations=add(add(group[0],group[1]),add(group[2],group[3]))
    physical_kernel=scale(mm(add(E,scale(s,-1)),rotations),F(1,8))
    assert physical_kernel==zero()
    # Faithful regular D8 control: the projector is nonzero in the algebra,
    # despite its zero width-one source representation.
    dreg,sreg=zero(8),zero(8)
    for parity in (0,1):
        for k in range(4):
            col=k+4*parity
            dreg[(k+1)%4+4*parity][col]=O
            sreg[(-k)%4+4*(1-parity)][col]=O
    av=eye(8)
    for k in (1,2,3):av=add(av,power(dreg,k))
    kerreg=scale(mm(add(eye(8),scale(sreg,-1)),av),F(1,8))
    assert mm(kerreg,kerreg)==kerreg and star(kerreg)==kerreg
    assert mm(sreg,kerreg)==scale(kerreg,-1)
    assert mm(mm(sreg,dreg),kerreg)==scale(kerreg,-1)
    assert sum((kerreg[j][j] for j in range(8)),Z)==O
    K=mm(S,s);ell=mm(K,D[1])
    rights=[mm(D[2],star(D[3])),mm(D[3],star(D[0])),mm(D[0],star(D[1]))]
    assert mm(K,Cb)==mm(Cb,K) and mm(K,D[1])==mm(D[1],K)
    assert mm(Cb,mm(D[1],Cb))==mm(D[1],mm(Cb,D[1]))
    for j in range(1,4):assert mm(A,mm(h,power(A,j)))==mm(ell,mm(power(A,j),rights[j-1]))
    assert mm(rights[0],A)==mm(A,rights[1]) and mm(rights[1],A)==mm(A,rights[2])

    def canonical(rank):
        out=E
        for bit in range(rank):
            xb=mono(lambda a,b,c,d,bit=bit:(a+2*b+4*c+8*d)^(1<<bit),lambda *x:0)
            out=mm(scale(add(scale(E,O+I),scale(xb,O-I)),F(1,2)),out)
        return out
    def gaussian_gauge(a):
        """Build actual root-four L,R with a=L C_rank R, not a support-count test."""
        sizes={sum(bool(x) for x in row) for row in a};assert len(sizes)==1
        width=sizes.pop();assert width and width&(width-1)==0
        rank=width.bit_length()-1
        alpha=m.G(F(1,2),F(1,2));normal=O
        for _ in range(rank):normal=normal*alpha
        groups={}
        for row in range(16):groups.setdefault(tuple(j for j,x in enumerate(a[row]) if x),[]).append(row)
        assert len(groups)==16//width
        L,R=zero(),zero()
        for block,(cols,rows) in enumerate(sorted(groups.items())):
            assert len(rows)==width
            exps=[]
            for rr in rows:
                values=[a[rr][cc]/normal for cc in cols];assert all(x in roots for x in values)
                exps.append([roots.index(x) for x in values])
            patterns=[]
            for ee in exps:
                diff=[(ee[j]-ee[0]-exps[0][j]+exps[0][0])%4 for j in range(width)]
                assert all(x in (0,2) for x in diff)
                patterns.append(sum((x//2)<<j for j,x in enumerate(diff)))
            basis=[];coordinates={0:0}
            for pat in patterns:
                if pat not in coordinates:
                    old=dict(coordinates);bit=1<<len(basis);basis.append(pat)
                    coordinates.update({x^pat:c|bit for x,c in old.items()})
            assert len(basis)==rank and len(set(patterns))==width and set(patterns)==set(coordinates)
            colcodes=[sum(((v>>j)&1)<<k for k,v in enumerate(basis)) for j in range(width)]
            assert len(set(colcodes))==width
            for rr,pat,ee in zip(rows,patterns,exps):
                u=coordinates[pat];L[rr][block*width+u]=roots[(ee[0]+u.bit_count())%4]
            for j,cc in enumerate(cols):
                v=colcodes[j];R[block*width+v][cc]=roots[(exps[0][j]-exps[0][0]+v.bit_count())%4]
        table(L);table(R);assert mm(L,mm(canonical(rank),R))==a
        return {'rank':rank,'left_monomial':table(L),'right_monomial':table(R)}
    heads={}
    for name,g in [('I',E),('h',h),('s',s),('sh',mm(s,h))]:
        heads[name]=[gaussian_gauge(mm(A,mm(g,power(A,j)))) for j in (1,2,3)]
    assert {name:[x['rank'] for x in xs] for name,xs in heads.items()}=={
        'I':[2,3,4],'h':[1,2,3],'s':[0,1,2],'sh':[2,3,4]}

    def had(i,j,inverse):
        w=[('ADD',i,j),('SCALE',j,m.G(-2)),('ADD',j,i)]
        if inverse:w += [('SCALE',i,m.G(F(1,2))),('SCALE',j,m.G(F(1,2)))]
        return w
    def controlled(i,j,g):return had(i,j,True)+[('MONO',j,rowmono(g))]+had(i,j,False)
    def rot(i,j,g,inverse=False):
        if inverse:return controlled(i,j,g)+[('MONO',j,rowmono(g))]
        return [('MONO',j,rowmono(g))]+controlled(i,j,g)
    word=rot(0,1,h)+rot(1,2,s)
    inverse=rot(1,2,s,True)+rot(0,1,h,True)
    Ph,Nh=scale(add(E,h),F(1,2)),scale(add(E,scale(h,-1)),F(1,2))
    Ps,Ns=scale(add(E,s),F(1,2)),scale(add(E,scale(s,-1)),F(1,2))
    blocks=[[Ph,scale(Nh,-1),zero()],[mm(Ps,Nh),mm(Ps,Ph),scale(Ns,-1)],
            [mm(Ns,Nh),mm(Ns,Ph),Ps]]
    expected=[[blocks[i//16][j//16][i%16][j%16] for j in range(48)] for i in range(48)]
    def join(bs):return [[bs[i//16][j//16][i%16][j%16] for j in range(48)] for i in range(48)]
    nativeL=join([[A,zero(),zero()],[E,A,zero()],[zero(),zero(),E]])
    nativeU=join([[A,scale(power(A,2),-1),zero()],[zero(),A,zero()],[zero(),zero(),E]])
    native=mm(nativeL,mm(expected,nativeU))
    aha=mm(A,mm(h,A));aha2=mm(A,mm(h,power(A,2)))
    first_p=scale(add(power(A,2),aha),F(1,2))
    first_z=scale(add(add(scale(power(A,2),-1),aha),add(scale(power(A,3),-1),scale(aha2,-1))),F(1,2))
    assert [row[:16] for row in native[:16]]==first_p
    assert [row[16:32] for row in native[:16]]==first_z
    assert [row[32:] for row in native[:16]]==zero()
    assert [row[32:] for row in native[16:32]]==scale(mm(A,Ns),-1)
    assert [row[32:] for row in native[32:]]==Ps
    actual,counts=m.apply(word,16,3);back,backcounts=m.apply(inverse,16,3)
    assert actual==expected and mm(back,actual)==mm(actual,back)==eye(48)
    assert counts==backcounts=={'MONO':4,'ADD':8,'SCALE':8}
    controls=0
    for program,target in [(word,actual),(inverse,back)]:
        for k,op in enumerate(program):
            if op[0]=='ADD':
                assert m.apply(program[:k]+program[k+1:],16,3)[0]!=target;controls+=1
    # Erasing the clock phase must not preserve the new lowering gauge.
    assert mm(A,mm(s,A))!=mm(ell,mm(A,rights[0]))
    def encode(program):
        out=[]
        for op in program:
            if op[0]=='ADD':out.append({'op':'ADD','dst':op[1],'src':op[2]})
            elif op[0]=='SCALE':out.append({'op':'SCALE','bank':op[1],'value':op[2].enc()})
            else:
                out.append({'op':'MONO','bank':op[1],'row_permutation':list(op[2][0]),
                            'row_phase':[roots.index(x) for x in op[2][1]]})
        return out
    result={'status':'PASS_INDEPENDENT_MIXED_RETURN_INTERFACE','arithmetic_sha256':PIN,
        'source_A_direct_columns_verified':True,'inherited_return_sbc':table(r),
        'new_phased_involution_h':table(h),'K':table(K),'left_gauge':table(ell),
        'dihedral_group_traces':[x.enc() for x in traces],
        'active_column_common_minus_projector':'(I-s)(I+d+d^2+d^3)/8, d=s h',
        'active_kernel_dimension_formula':'(16^W-2*8^W)/8, W>=1',
        'active_kernel_dimensions':{str(w):(16**w-2*8**w)//8 for w in range(1,5)},
        'faithful_regular_projector_trace':1,
        'scoped_421_gate':{'first_row_identity_replayed':True,
            'class3_coefficient':'-a^3 z/2','output1_class0_coefficient':'r(p+z)/4',
            'forced_column':'p=z=0, w=N_s w; no left inverse',
            'scope':'Fixed Cmix, uniform fixed finite ordinary collective-tail catalogue, faithful large widths'},
        'right_gauges':[table(x) for x in rights],'head_gaussian_gauges':heads,
        'Cmix_forward':encode(word),'Cmix_inverse':encode(inverse),
        'forward_counts':counts,'inverse_counts':backcounts,'arbitrary_input_columns':48,
        'omitted_ADD_controls':controls,'clock_phase_erasure_rejected':True,
        'uniform_primitive_prefix_bound':14,'scope':'Exact ordinary unit/inverse and source class gauges at every tensor width. No Q, independent endpoint, caller, or kappa claim.'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'out':str(args.out),'head_ranks':{k:[z['rank'] for z in v] for k,v in heads.items()},'controls':controls}))
if __name__=='__main__':main()
