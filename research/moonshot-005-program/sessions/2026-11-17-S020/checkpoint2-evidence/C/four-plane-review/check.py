#!/usr/bin/env python3
"""Independent all-222-column, real-geometry and tariff review.

No builder, native interpreter or author arithmetic is imported.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from functools import cache
import argparse,hashlib,json

NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD='6270dfd9df015e8573066afedc32e22adac8dec5da499c5b566f4bcbe539ad9d'


def require(ok,why):
    if not ok:raise ValueError(why)


@cache
def basis(rows):
    A=[list(map(F,row))for row in rows];r=0
    for j in range(8):
        p=next((k for k in range(r,len(A))if A[k][j]),None)
        if p is None:continue
        A[p],A[r]=A[r],A[p];v=A[r][j];A[r]=[x/v for x in A[r]]
        for k in range(len(A)):
            if k!=r and A[k][j]:
                v=A[k][j];A[k]=[x-v*y for x,y in zip(A[k],A[r])]
        r+=1
    return tuple(tuple(row)for row in A[:r])


def kernel(rows):
    A=basis(tuple(map(tuple,rows)));piv=[next(j for j,x in enumerate(row)if x)for row in A]
    out=[]
    for j in range(8):
        if j in piv:continue
        row=[F(0)]*8;row[j]=1
        for p,v in zip(piv,A):row[p]=-v[j]
        out.append(tuple(row))
    return basis(tuple(out))


def chart(spec):
    rows=tuple(map(tuple,spec['rows']))
    if spec['kind']=='span':return basis(rows)
    require(spec['kind']=='ann','known chart convention')
    return kernel(rows)


def contained(A,B):return len(basis(A+B))==len(B)


def derive(roots,word):
    support=[0,1,6,7];a,b,c,d=support
    signs=[i for i,r in enumerate(roots)if [j for j,x in enumerate(r)if x]==support]
    require(signs==list(range(22,30)),'literal eight-sign group')
    E=[tuple(int(i==j)for j in range(8))for i in range(8)]
    charts={n:chart(v)for n,v in word['charts'].items()}
    require(charts['G']==basis(tuple(E[i]for i in support)),'coordinate quartet G')
    groups={};expected={i:frozenset()for i in range(111)};pairs={}
    for s in (1,-1):
        for label,(x,y,u,v)in [('A',(a,b,c,d)),('B',(c,d,a,b))]:
            name=f'{label}{s}'
            plane_vector=tuple(E[x][j]+s*E[y][j]for j in range(8))
            require(charts[name]==basis((plane_vector,E[u],E[v])),'independent query plane '+name)
            local={i for i in signs if roots[i][x]==s*roots[i][y]}|{u,v}
            receivers=[i for i,r in enumerate(roots)if [j for j in support if r[j]]==[x,y] and r[x]==-s*r[y]]
            require(len(local)==6,'six distinct local summands')
            groups[name]={'receivers':receivers,'summands':sorted(local)}
            for i in receivers:
                require(not expected[i],'query groups disjoint')
                require(i not in local and all(sum(q*z for q,z in zip(roots[i],roots[k]))==0 for k in local),'all summands are foreign neighbors')
                require(contained(charts[name],charts[f'F{i}']),'receiver final facet contains actual query plane')
                expected[i]=frozenset(local)
        for t in (1,-1):
            name=f'PAIR_{s}_{t}'
            roles=[i for i in signs if roots[i][a]==s*roots[i][b] and roots[i][c]==t*roots[i][d]]
            require(len(roles)==2,'two roots per pair intersection')
            require(charts[name]==basis(tuple(tuple(roots[i])for i in roles)) and len(charts[name])==2,'actual pair chart')
            require(contained(charts[name],charts[f'A{s}'])and contained(charts[name],charts[f'B{t}']),'pair contained in both query planes')
            pairs[name]=roles
    served=sorted(i for i,S in expected.items()if S)
    require(len(served)==29,'29 independently derived receivers')
    require({q:len(v['receivers'])for q,v in groups.items()}=={'A1':8,'B1':7,'A-1':7,'B-1':7},'query populations')
    require(all(contained(charts['G'],charts[f'F{i}'])for i in(2,3)),'both couriers can continue from G')
    require(not(set(served)&{2,3}),'couriers are not served receivers')
    require(word['Y_correction_rows_hex']==[hex(sum(1<<j for j in expected[i]))for i in range(111)],'declared correction rows match independently derived native geometry')
    require(word['construction']['query_roles']=={q:v['receivers']for q,v in groups.items()},'query role record')
    require(set(word['construction']['served_receivers'])==set(served),'served inventory')
    incoming=Counter();outgoing=Counter()
    for q,info in word['construction']['oriented_pairs'].items():
        require(info['roles']==pairs[q],'pair input inventory')
        incoming[info['late']]+=1;outgoing[info['early']]+=1
        require(contained(charts[q],charts[info['early']])and contained(charts[q],charts[info['late']]),'oriented edge geometry')
    require(incoming==outgoing==Counter({q:1 for q in groups}),'one early and one late pair per query')
    return charts,groups,expected,served,sorted(support+signs)


def replay(word,charts,expected,served,sources,check_cut=True):
    val={f'X{i}':frozenset([i])for i in range(111)}|{f'Y{i}':frozenset([111+i])for i in range(111)}
    at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    owned=set();born=set();counts=Counter();profile=Counter();prefix=Counter();dirty=peak=0;cut=None
    for step,(kind,name,*arg)in enumerate(word['operations']):
        if step==word['carrier_interface_before_operation']:cut=(val.copy(),at.copy(),owned.copy())
        counts[kind]+=1
        if kind=='INIT':
            require(name not in val and name not in born,'fresh unique owned lifetime')
            require(arg[0]in charts,'birth chart exists');val[name]=frozenset();at[name]=arg[0];owned.add(name);born.add(name)
        elif kind=='ADD':
            target=arg[0];require(name in val and target in val and name!=target,'live distinct ADD operands')
            require(charts[at[name]]==charts[at[target]],f'actual cochart ADD at {step}')
            val[target]=val[target]^val[name]
            if target.startswith('X'):require(all(j<111 for j in val[target]),'no Y-dependent value enters an original X')
        elif kind=='MOVE':
            require(name in val and arg[0]in charts,'live movement')
            before,after=charts[at[name]],charts[arg[0]]
            require(contained(after,before)if name in owned else contained(before,after),f'legal chart direction at {step}')
            gap=abs(len(before)-len(after));require(gap>0,'strict positive rank movement')
            require(name not in owned,'gadget has no owned movement')
            profile[gap]+=1
            if step<word['carrier_interface_before_operation']:prefix[gap]+=1
            at[name]=arg[0]
        elif kind=='CLEAR':
            require(name in owned,'only owned fields may be retired');dirty+=bool(val[name]);owned.remove(name);del val[name],at[name]
        else:raise ValueError('unknown opcode')
        peak=max(peak,len(owned))
    require(cut is not None and not owned and len(val)==222,'closed all-input public endpoint')
    for i in range(111):
        require(val[f'X{i}']==frozenset([i])and at[f'X{i}']=='Hub',f'raw X{i} endpoint')
        require(val[f'Y{i}']==expected[i]|{111+i}and at[f'Y{i}']==f'F{i}',f'exact all-column Y{i} endpoint')
    cv,ca,co=cut
    if check_cut:
        require(len(cv)==333 and len(co)==111,'complete cut inventory')
        for i in range(111):
            require(cv[f'X{i}']==frozenset([i]),'all X restored by cut')
            require(ca[f'X{i}']==('G'if i in sources else f'L{i}'),'actual X cut location')
            require(cv[f'Y{i}']==expected[i]|{111+i},'all arbitrary Y coefficients restored at cut')
            require(cv[f'NATIVE_{i}']==frozenset([i])and ca[f'NATIVE_{i}']==f'L{i}','stationary native snapshot')
            if i in(2,3):require(ca[f'Y{i}']=='G','restored courier chart')
            elif i not in served:require(ca[f'Y{i}']=='zero','unused Y remains at ground')
            else:require(len(charts[ca[f'Y{i}']])==3 and contained(charts[ca[f'Y{i}']],charts[f'F{i}']),'served Y at its real proper query plane')
    return {'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'prefix_profile':dict(sorted(prefix.items())),'rank_length':sum(k*v for k,v in profile.items()),'dirty_CLEAR':dirty,'peak_owned':peak,'cut_live_fields':len(cv)},cv,ca


def root_interval(n,power=199,den=200,digits=31):
    scale=10**digits;target=n**power*scale**den;lo,hi=0,n*scale+1
    while hi-lo>1:
        mid=(hi+lo)//2
        if mid**den<=target:lo=mid
        else:hi=mid
    return F(lo,scale),F(hi,scale)


def moment(profile):
    lo=hi=F(0)
    for n,c in profile.items():
        a,b=root_interval(n)
        lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi


def main():
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    require(hashlib.sha256(a.native.read_bytes()).hexdigest()==NATIVE,'authenticated native source')
    require(hashlib.sha256(a.word.read_bytes()).hexdigest()==WORD,'authenticated gadget word')
    roots=json.loads(a.native.read_text())['native_roots'];word=json.loads(a.word.read_text())
    charts,groups,expected,served,sources=derive(roots,word)
    stats,cv,ca=replay(word,charts,expected,served,sources)
    require(stats['counts']=={'INIT':111,'ADD':230,'MOVE':316,'CLEAR':111},'complete primitive invoice')
    require(stats['movement_profile']=={1:57,2:37,3:2,4:41,7:179}and stats['prefix_profile']=={1:57,2:37},'independent movement invoice')
    require(stats['rank_length']==1554 and stats['dirty_CLEAR']==111 and stats['peak_owned']==111,'full length and lifetime charges')
    q=moment(stats['movement_profile']);baseline=moment({7:222});overhead=(q[0]-baseline[1],q[1]-baseline[0])
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in moment(gate));room=(ceiling[0]-q[1],ceiling[1]-q[0])
    controls={}
    for label in ['ground_Y_inverse','original_inverse','courier_actual_cleanup']:
        alt=json.loads(json.dumps(word));k=alt['semantic_operation_indices'][label][0];del alt['operations'][k];alt['carrier_interface_before_operation']-=1
        try:replay(alt,charts,expected,served,sources)
        except ValueError as e:controls[label]=str(e)
        else:raise ValueError('missing essential operation accepted')
    alt=json.loads(json.dumps(word));k=alt['semantic_operation_indices']['query_early_arrival'][0];alt['operations'][k][2]='A1'
    try:replay(alt,charts,expected,served,sources)
    except ValueError as e:controls['bypass_pair_chart']=str(e)
    else:raise ValueError('noncochart shortcut accepted')
    inv=[{'name':n,'chart':ca[n],'rank':len(charts[ca[n]]),'columns':sorted(v)}for n,v in sorted(cv.items())]
    result={'status':'PASS_INDEPENDENT_FOUR_PLANE_ALL222_GEOMETRY_AND_PUBLIC_MAP','native_sha256':NATIVE,'word_sha256':WORD,'cut':435,'source_roles':sources,'served_receivers':served,'served_count':29,'foreign_coefficients':174,'completed_diagonal_outputs':0,'query_groups':groups,'stats':stats,'moment_rational':list(map(str,q)),'overhead_over_222_direct_7_routes':list(map(str,overhead)),'necessary_room_rational':list(map(str,room)),'controls':controls,'scope':'Actual partial foreign-correction map for every characteristic-two field and whole-record width; requires earlier routes and ground Y preloads. No complete supplier or new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'INDEPENDENT-CUT.json').write_text(json.dumps(inv,indent=2)+'\n')
    print(result['status'],'29 Ys, 174 foreign terms, all222 columns and original restorations verified')


if __name__=='__main__':main()
