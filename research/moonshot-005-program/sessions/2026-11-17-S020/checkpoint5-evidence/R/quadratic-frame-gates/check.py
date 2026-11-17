"""Independent all-source quadratic first-exit proofs for three actual cuts."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from itertools import combinations_with_replacement
from math import gcd,lcm
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json
GEO='983c931bc9907de160fa59fc2011cff434766d7e7384ce898df05574cc5c61fc'
ARITH='41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'
PINS={'ground':'4628d085fc99ea258f03c374926e1a97852497ff7fe0cec1206cb32bc0bb2c9f','proper':'bad2213d8bab1c61d08a97bff2e1e21f24bdff9d22be6f7de09c84853b2efe85','meet':'54fada571a96571697f3e87b50ee613a9042ee9577703f90ab13b2f7a172ff95'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def basis(rows):
    b={}
    for v in rows:
        while v:
            p=(v&-v).bit_length()-1
            if p in b:v^=b[p]
            else:b[p]=v;break
    return b
def reduce(v,b):
    for p in sorted(b):
        if v>>p&1:v^=b[p]
    return v
def dual(rows,target):
    b=basis(rows);v=reduce(target,b);assert v;p=(v&-v).bit_length()-1
    return sum(((reduce(1<<j,b)>>p)&1)<<j for j in range(111))
def rr(rows,width):
    a=[list(map(F,r))for r in rows];k=0;piv=[]
    for c in range(width):
        j=next((j for j in range(k,len(a))if a[j][c]),None)
        if j is None:continue
        a[k],a[j]=a[j],a[k];z=a[k][c];a[k]=[x/z for x in a[k]]
        for j in range(len(a)):
            if j!=k and a[j][c]:z=a[j][c];a[j]=[x-z*y for x,y in zip(a[j],a[k])]
        piv.append(c);k+=1
    return a[:k],piv
def kernel(rows,width):
    a,p=rr(rows,width);out=[]
    for c in range(width):
        if c in p:continue
        v=[F(0)]*width;v[c]=1
        for row,k in zip(a,p):v[k]=-row[c]
        d=lcm(*(x.denominator for x in v));z=[int(x*d)for x in v];d=gcd(*z);out.append([x//d for x in z])
    return out
def independent_indices(rows):
    prime=1031;b={};chosen=[]
    for i,row in enumerate(rows):
        v=[int(x)%prime for x in row]
        for p in sorted(b):
            if v[p]:z=v[p];v=[(x-z*y)%prime for x,y in zip(v,b[p])]
        if any(v):
            p=next(k for k,x in enumerate(v)if x);inv=pow(v[p],-1,prime);b[p]=[x*inv%prime for x in v];chosen.append(i)
    return chosen
def record(v):
    with localcontext()as c:
        c.prec=55;return {'rational':list(map(str,v)),'decimal':[str(Decimal(x.numerator)/Decimal(x.denominator))for x in v]}
def audit(name,path,g,m,R):
    assert digest(path)==PINS[name];w=json.loads(path.read_text());charts,V,P=g.replay_cut(w);cut=w['carrier_interface_before_operation'];xmask=(1<<111)-1
    assert cut=={'ground':794,'proper':806,'meet':804}[name]and len(V)==(341 if name=='ground'else 342)
    assert len(basis(V[f'X{i}']for i in range(111)))==111
    for i,r in enumerate(R):
        assert charts[f'L{i}']==g.rref([r])and charts[f'F{i}']==g.nullspace([r])
        assert V[f'NATIVE_{i}']==1<<i and P[f'NATIVE_{i}']==f'L{i}'
        assert V[f'X{i}']&~xmask==0 and V[f'Y{i}']&~xmask==1<<(111+i)
    N=[{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)]
    bank=[(1<<i)|sum(1<<j for j in N[i])for i in range(111)]+[1<<i for i in range(8)]+[V[f'Y{i}']&xmask for i in range(111)]
    if name!='ground':
        owner='FRAME_EXPORT'if name=='proper'else'MEET_FRAME_EXPORT';h=sum(1<<i for i in[73,78,81,86]);assert V[owner]==h;bank.append(h)
    bank_rank=len(basis(bank));assert bank_rank==(29 if name=='ground'else 30)
    native={charts[f'L{i}']:i for i in range(111)};other=[];active={j:[]for j in range(111)}
    for n,v in V.items():
        j=native.get(charts[P[n]])
        if j is None:other.append(n)
        else:
            assert v&xmask in[0,1<<j]
            if n.startswith(('X','Y')):active[j].append(n)
    inside={i:[n for n in V if g.contains(charts[f'F{i}'],charts[P[n]])]for i in range(111)};other_set=set(other)
    obs={i:bank+[V[n]&xmask for n in inside[i]if n in other_set]for i in range(111)};dem={j:[]for j in range(111)}
    for i in range(8,111):
        assert not reduce(1<<i,basis(obs[i]+[1<<k for k in N[i]]))
        for j in N[i]:
            if reduce(1<<i,basis(obs[i]+[1<<k for k in N[i]if k!=j])):dem[j].append(i)
    assert all(not dem[j]for j in range(8));pairs=list(combinations_with_replacement(range(7),2));rows=[];duals=0
    for j in range(8,111):
        D=dem[j];assert len(g.rref([R[i]for i in D]))==7
        skip=next(k for k,x in enumerate(R[j])if x);coords=[k for k in range(8)if k!=skip]
        ev=[[R[i][coords[u]]*R[i][coords[v]]for u,v in pairs]for i in D];K=kernel(ev,28);qrank=28-len(K);form=None;form_rank=None
        if qrank==27:
            selected=[D[k]for k in independent_indices(ev)];assert len(selected)==27
            assert len(rr([[R[i][coords[u]]*R[i][coords[v]]for u,v in pairs]for i in selected],28)[0])==27
            form=K[0];M=[[0]*7 for _ in range(7)]
            for (u,v),z in zip(pairs,form):M[u][v]=M[v][u]=z*(2 if u==v else 1)
            form_rank=len(rr(M,7)[0]);assert form_rank==6 and all(sum(x*y for x,y in zip(v,form))==0 for v in ev);minimum=3
        else:
            selected=[D[k]for k in independent_indices([R[i]for i in D])];assert len(selected)==7 and len(g.rref([R[i]for i in selected]))==7;minimum=2
        witnesses=[]
        for i in selected:
            d=dual(obs[i]+[1<<k for k in N[i]if k!=j],1<<i)
            assert d>>i&1 and d>>j&1 and all((d&z).bit_count()%2==0 for z in bank)and all(not(d>>k&1)for k in N[i]if k!=j)
            for n in inside[i]:
                v=V[n]
                if not(charts[P[n]]==charts[f'L{j}']and v&xmask==1<<j):assert(d&v&xmask).bit_count()%2==0
            witnesses.append({'receiver':i,'dual_hex':hex(d)})
        duals+=len(witnesses);assert bool(active[j])==(minimum==3)
        rows.append({'source_role':j,'all_forced_receivers':D,'selected_receivers':selected,'duals':witnesses,'quadratic_rank':qrank,'normal_coordinate_indices':coords,'quadratic_kernel':form,'symmetric_form_rank':form_rank,'minimum_native_departures':minimum,'native_public_fields':active[j]})
    return finish(name,w,charts,V,P,bank_rank,rows,duals,g,m)
def finish(name,w,charts,V,P,bank_rank,rows,duals,g,m):
    total=sum(x['minimum_native_departures']for x in rows);public=sum(len(x['native_public_fields'])for x in rows)
    ground=[n for n in V if n.startswith(('X','Y'))and not charts[P[n]]];assert len(ground)==95
    assert total==(277 if name=='ground'else 273)and public==(71 if name=='ground'else 67)
    owned=total-public-len(ground);assert owned==111
    final_word=dict(w,carrier_interface_before_operation=len(w['operations']));_,FV,FP=g.replay_cut(final_word)
    assert set(FV)=={f'{kind}{i}'for kind in['X','Y']for i in range(111)}
    for i in range(111):assert FV[f'X{i}']==1<<i and FV[f'Y{i}']==V[f'Y{i}']and FP[f'X{i}']=='Hub'and FP[f'Y{i}']==f'F{i}'
    places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};profile=Counter();suffix=set();cut=w['carrier_interface_before_operation']
    for step,(kind,n,*args)in enumerate(w['operations']):
        if kind=='INIT':places[n]=args[0]
        elif kind=='CLEAR':del places[n]
        elif kind=='MOVE':
            dest=args[0];profile[abs(len(charts[dest])-len(charts[places[n]]))]+=1
            if step>=cut:
                assert n.startswith(('X','Y'))and n not in suffix;suffix.add(n);assert dest==('Hub'if n.startswith('X')else'F'+n[1:])
            places[n]=dest
    assert len(suffix)==222 and all(1<=k<=7 for k in profile)
    expected={'ground':{1:72,2:16,4:16,5:16,6:16,7:174},'proper':{1:72,2:22,3:1,4:16,5:19,6:16,7:170},'meet':{1:72,2:21,4:16,5:20,6:16,7:170}}
    assert dict(profile)==expected[name];Q0=m.moment(profile);mandatory=dict(profile);mandatory[1]+=owned;lower=m.moment(mandatory)
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.moment(gate));excess=(lower[0]-ceiling[1],lower[1]-ceiling[0]);assert excess[0]>37
    return {'source':name,'word_sha256':PINS[name],'cut':cut,'live_fields':len(V),'all_original_columns':222,'bank_rank':bank_rank,'source_witnesses':rows,'verified_duals':duals,'native_departures':total,'native_public_credit':public,'ground_public_credit':len(ground),'minimum_future_owned_ascents':owned,'Q0_profile':dict(sorted(profile.items())),'mandatory_profile':dict(sorted(mandatory.items())),'Q0':record(Q0),'target_excess':record(excess),'public_closure_moves':222}
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--geometry',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    for name in PINS:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();assert digest(a.geometry)==GEO;g=module(a.geometry,'independent_source_geometry')
    base=a.repo/'research/moonshot-005-program';native=base/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert digest(native)==g.NATIVE;R=json.loads(native.read_text())['native_roots']
    ar=base/'sessions/2026-11-17-S020/checkpoint2-evidence/C/four-plane-review/check.py';assert digest(ar)==ARITH;m=module(ar,'separate_exact_tariffs')
    cases=[audit(name,getattr(a,name),g,m,R)for name in PINS]
    coordinate_normals=[[int(i==j)for j in range(7)]for i in range(7)];assert len(rr(coordinate_normals,7)[0])==7 and all(v[0]*v[1]==0 for v in coordinate_normals)
    assert all(not reduce(1<<i,basis([1<<j for j in range(111)]))for i in range(111))
    total=sum(x['verified_duals']for x in cases);assert total==6263
    result={'status':'PASS_INDEPENDENT_QUADRATIC_GROUND_AND_TWO_FRAME_BANK_GATES','native_sha256':digest(native),'geometry_sha256':GEO,'arithmetic_sha256':ARITH,'cases':cases,'verified_duals':total,'quadratic_monomials':[list(x)for x in combinations_with_replacement(range(7),2)],'controls':{'linear_rank7_does_not_preclude_two_hyperplanes':True,'full_raw_bank_removes_forcing':True},'scope':'All real nested destination charts; monotone public routes; arbitrary paid owned turns; characteristic-two linear block processing; every future descending X row lies in the exact29/30 bank. New modes, nonlinear processing or changed public routes are outside.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],total,'duals');print([(x['source'],x['minimum_future_owned_ascents'],x['target_excess']['decimal'][0])for x in cases])
if __name__=='__main__':main()
