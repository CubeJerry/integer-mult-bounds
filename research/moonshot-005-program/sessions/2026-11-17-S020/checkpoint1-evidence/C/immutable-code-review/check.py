#!/usr/bin/env python3
"""Independent finite premises for immutable canonical-packet geometry.

No author helpers imported. Reconstructs the certificate's basis from its
fitting rows, uses rational native geometry, and derives the source price
from actual movements plus direct original endpoints.
"""
import argparse,hashlib,json
from collections import Counter
from fractions import Fraction as Q
from functools import cache
from pathlib import Path

NATIVE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD_SHA='74fb050a6afb8d8e1b6895b0f092220f8e6852365a7516ef4db2284c43c1a5ee'

def need(ok,why):
    if not ok:raise ValueError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def binary_rank(rows):
    piv={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p in piv:row^=piv[p]
            else:piv[p]=row;break
    return len(piv)

@cache
def reduced(rows):
    a=[list(map(Q,row))for row in rows];k=0
    for c in range(8):
        r=next((r for r in range(k,len(a))if a[r][c]),None)
        if r is None:continue
        a[k],a[r]=a[r],a[k];q=a[k][c];a[k]=[x/q for x in a[k]]
        for r in range(len(a)):
            if r!=k and a[r][c]:
                q=a[r][c];a[r]=[x-q*y for x,y in zip(a[r],a[k])]
        k+=1
    return tuple(tuple(row)for row in a[:k])

@cache
def power(d):
    # Independent exact binary search at 10^33, not the author's interval helper.
    scale=10**33;target=d**199*scale**200;lo=0;hi=d*scale+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=target:lo=mid
        else:hi=mid
    need(lo**200<=target<hi**200,'integer root enclosure')
    if lo**200==target:hi=lo
    return Q(lo,scale),Q(hi,scale)

def moment(profile):
    lo=hi=Q(0)
    for d,c in profile.items():
        a,b=power(d);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi

def describe(interval):
    from decimal import Decimal,localcontext
    with localcontext()as c:
        c.prec=60
        return {'rational':list(map(str,interval)),'decimal':[str(Decimal(x.numerator)/Decimal(x.denominator))for x in interval]}

def main():
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(sha(a.native)==NATIVE_SHA and sha(a.word)==WORD_SHA,'authenticated source bytes')
    R=json.loads(a.native.read_text())['native_roots'];w=json.loads(a.word.read_text());cert=json.loads(a.certificate.read_text())
    need(cert['source_word_sha256']==WORD_SHA,'certificate word pin')
    U=sorted(set(range(111))-set(w['targets']));need(len(U)==54,'54 unknowns')
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
    N={i:{j for j in U if dot(i,j)==0}for i in U}
    K={i:(1<<i)^sum(1<<j for j in N[i])for i in U}
    local={z['receiver']:z for z in cert['local_restrictions']};need(set(local)==set(U),'all receiver restrictions')
    coeff={i:int(local[i]['canonical_coeff_hex'],16)for i in U}
    # Reconstruct the certificate coordinate basis from exact K_i relations.
    piv={}
    for i in U:
        v=coeff[i];r=K[i];need(0<v<512,'nonzero nine-coordinate fitting recipe')
        while v:
            j=v.bit_length()-1
            if j in piv:v^=piv[j][0];r^=piv[j][1]
            else:piv[j]=(v,r);break
        if not v:need(r==0,'source/certificate fitting relation')
    need(len(piv)==9,'coordinate map rank nine')
    B=[]
    for j in range(9):
        v=1<<j;r=0
        while v:
            k=v.bit_length()-1;v^=piv[k][0];r^=piv[k][1]
        B.append(r)
    source_rows=[int(z,16)for z in w['construction']['canonical_unknown_rows_hex']]
    need(binary_rank(B)==binary_rank(source_rows)==binary_rank(B+source_rows)==9,'same actual canonical code space')
    restrictions=[]
    for i in U:
        rebuilt=0
        for j,b in enumerate(B):
            if coeff[i]>>j&1:rebuilt^=b
        need(rebuilt==K[i],'literal canonical fitting row')
        mask=sum(1<<j for j in U if j not in N[i]);r=binary_rank([b&mask for b in B])
        need(r==9 and local[i]['neighbours']==sorted(N[i]) and local[i]['nonlocal_projection_rank']==9,'zero local intersection')
        restrictions.append({'receiver':i,'rank':r})
    dual={z['functional']:z for z in cert['binary_dual_supports']};need(set(dual)==set(range(1,512)),'all binary nonzero duals')
    histogram=Counter();verified=[]
    for d in range(1,512):
        support=[i for i in U if (coeff[i]&d).bit_count()%2]
        r=len(reduced(tuple(tuple(R[i])for i in support)));histogram[r]+=1
        z=dual[d];need(z['support']==support and z['normal_rank']==r and r>=7,'exact dual support normal rank')
        witness=z['independent_root_witness']
        need(set(witness)<=set(support) and len(witness)==r and len(reduced(tuple(tuple(R[i])for i in witness)))==r,'independent root witness')
        verified.append({'functional':d,'normal_rank':r,'support_size':len(support)})
    need(histogram=={7:70,8:441},'complete normal rank census')
    sharp=cert['sharp_rank7_dual_basis_lines'];need(len(sharp)==9 and binary_rank([z['functional']for z in sharp])==9,'rank-seven dual basis')
    for z in sharp:
        d=z['functional'];need(dual[d]['normal_rank']==7,'sharp direction rank')
        line=z['line_basis'];need(len(line)==1 and len(line[0])==8,'real line shape')
        v=list(map(Q,line[0]));need(any(v) and all(sum(x*y for x,y in zip(v,R[i]))==0 for i in dual[d]['support']),'actual common annihilator line')
    i=U[0];mask=sum(1<<j for j in U if j not in N[i] and j!=i);leak=9-binary_rank([b&mask for b in B]);need(leak==1,'own-coordinate enlargement destroys uniqueness')
    # Actual original endpoint baseline; subsequent route refinements cannot lower it.
    dims={n:len(reduced(tuple(tuple(r)for r in spec['rows']))) if spec['kind']=='span' else 8-len(reduced(tuple(tuple(r)for r in spec['rows'])))for n,spec in w['charts'].items()}
    loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owned=set();profile=Counter();prefix=None;cutloc=None;tail_owned=0
    for k,(tag,n,*arg)in enumerate(w['operations']):
        if k==w['carrier_interface_before_operation']:prefix=profile.copy();cutloc=loc.copy()
        if tag=='INIT':owned.add(n);loc[n]=arg[0]
        elif tag=='MOVE':
            d=dims[arg[0]]-dims[loc[n]];need(d<0 if n in owned else d>0,'directed source movement');profile[abs(d)]+=1;loc[n]=arg[0]
            if prefix is not None and n in owned:tail_owned+=1
        elif tag=='CLEAR':owned.remove(n);del loc[n]
    need(tail_owned==0,'source closure contains no future owned movement')
    minimum=prefix.copy()
    for i in range(111):
        for name,endrank in [(f'X{i}',8),(f'Y{i}',7)]:
            d=endrank-dims[cutloc[name]];need(d>=0,'ascending endpoint gap')
            if d:minimum[d]+=1
    need(minimum==profile=={1:165,6:108,7:114},'full closure is direct original endpoint minimum')
    packet=moment({7:9});base=moment(profile);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    cap=tuple(x/6 for x in moment(gate));gap=(base[0]+packet[0]-cap[1],base[1]+packet[1]-cap[0]);need(gap[0]>38,'strict target exclusion')
    result={'status':'PASS_INDEPENDENT_IMMUTABLE_CANONICAL_PACKET_GEOMETRY','source_sha256':NATIVE_SHA,'word_sha256':WORD_SHA,'certificate_sha256':sha(a.certificate),'receiver_local_intersections_zero':54,'binary_dual_cases':511,'normal_rank_histogram':dict(histogram),'coordinate_basis_rebuilt_from_fitting_relations':True,'sharp_independent_rank7_directions':[z['functional']for z in sharp],'own_coordinate_control_intersection_dimension':leak,'original_endpoint_minimum_profile':dict(profile),'packet_moment':describe(packet),'source_plus_packet_excess':describe(gap),'universal_proof_scope':'All characteristic-two fields, all positive block widths, arbitrary invertible nine-record rebasing, immutable post-loading packets; after any read no extra descending relay.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.out/'DUAL-CENSUS.json').write_text(json.dumps({'basis_rows_hex':list(map(hex,B)),'receiver_restrictions':restrictions,'dual_checks':verified},indent=2,sort_keys=True)+'\n')
    print(result['status'],dict(histogram),'excess',result['source_plus_packet_excess']['decimal'][0])

if __name__=='__main__':main()
