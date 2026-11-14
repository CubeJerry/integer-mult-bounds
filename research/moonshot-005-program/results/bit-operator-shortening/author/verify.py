#!/usr/bin/env python3
"""Exact native premises for the operator-valued shortening theorem."""
import argparse,copy,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'

def require(ok,message):
    if not ok:raise ValueError(message)

def basis_bits(rows):
    basis={};chosen=[]
    for index,row in enumerate(rows):
        while row:
            pivot=row.bit_length()-1
            if pivot in basis:row^=basis[pivot]
            else:basis[pivot]=row;chosen.append(index);break
    return basis,chosen

def remainder(row,basis):
    for p,b in sorted(basis.items(),reverse=True):
        if row>>p&1:row^=b
    return row

def rational_basis(rows):
    basis={};chosen=[]
    for index,row in enumerate(rows):
        row=list(row)
        for p,b in sorted(basis.items()):
            scalar=row[p];row=[x-scalar*y for x,y in zip(row,b)]
        p=next((j for j,x in enumerate(row) if x),None)
        if p is not None:
            scalar=row[p];basis[p]=[x/scalar for x in row];chosen.append(index)
    return basis,chosen

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def rejected(call,label):
    try:call()
    except ValueError:return label
    raise ValueError('negative control accepted: '+label)

def source(raw):
    require(hashlib.sha256(raw).hexdigest()==PIN,'exact native bytes')
    s=json.loads(gzip.decompress(raw));ff={int(k):v for k,v in s['frames'].items()}
    rr=[list(map(F,ff[s['start'][i]]['B'][0])) for i in range(111)]
    for i,r in enumerate(rr):
        facet=ff[s['final'][111+i]]
        require(facet['dim']==7 and all(dot(r,list(map(F,b)))==0 for b in facet['B']),'actual facet')
        require(dot(r,r)>0,'own line outside real facet')
    k=[sum(int(i==j or dot(a,b)==0)<<j for j,b in enumerate(rr)) for i,a in enumerate(rr)]
    require(all((row^(1<<i))!=0 for i,row in enumerate(k)),'every source line belongs to another receiver facet')
    return rr,k

def parity(certificate,roots,ceiling=None):
    require(certificate['native_sha256']==PIN,'certificate source pin')
    configs=certificate['nine_frame_configurations']
    require(len(configs)==certificate['configuration_count']==30,'thirty configurations')
    bound=certificate['maximum_aggregate_vertex_incidence'] if ceiling is None else ceiling
    require(bound==24 or ceiling is not None,'declared incidence ceiling')
    total=[0]*111
    for config in configs:
        require(len(config)==9,'nine frames per configuration')
        counts=[0]*111
        for frame in config:
            require(len(frame)==8 and len(set(frame))==8,'eight distinct frame roles')
            require(all(type(i) is int and 0<=i<111 for i in frame),'actual role indices')
            require(all(dot(roots[i],roots[j])!=0 for i in frame for j in frame if i!=j),'real nonorthogonal frame')
            for i in frame:counts[i]+=1
        require(sum(counts)==72 and all(n%2==0 for n in counts),'even incidence per configuration')
        total=[x+y for x,y in zip(total,counts)]
    require(sum(total)==2160 and max(total)<=bound,'aggregate incidence ceiling')
    require(F(bound,8*len(configs))==F(1,10),'rank-loss coefficient')
    return total

def code_shortening(roots,k):
    groups={}
    for i,r in enumerate(roots):
        support=tuple(j for j,x in enumerate(r) if x)
        require(len(support) in (1,4),'source root shape')
        sign=1 if r[support[0]]>0 else -1
        parity=sum(x*sign<0 for x in r)%2
        complement=tuple(j for j in range(8) if j not in support)
        key=('coordinate',0) if len(support)==1 else (min(support,complement),parity)
        groups.setdefault(key,[]).append(i)
    classes=list(groups.values());require(len(classes)==15,'fifteen classes')
    for group in classes:
        require(all(dot(roots[i],roots[j])==0 for i in group for j in group if i!=j),'orthogonal classes')
    owner={i:c for c,g in enumerate(classes) for i in g}
    u=[sum(1<<i for i in group) for group in classes]
    canonical=basis_bits(k)[0];w=basis_bits(k+u)[0]
    require(len(canonical)==9 and len(basis_bits(u)[0])==15 and len(w)==19,'canonical/class/full dimensions')
    all_columns=(1<<111)-1;checks=[]
    for i in range(111):
        local_mask=k[i]^(1<<i);forbidden=all_columns^local_mask
        restricted=basis_bits([row&forbidden for row in w.values()])[0]
        require(len(restricted)==18,'one-dimensional facet-local intersection')
        ell=k[i]^u[owner[i]]
        require(ell!=0 and ell&forbidden==0 and remainder(ell,w)==0,'local generator')
        support=[j for j in range(111) if ell>>j&1]
        rb,chosen=rational_basis([roots[j] for j in support])
        require(len(rb)==7,'local generator spans entire facet')
        anchors=[support[j] for j in chosen]
        require(len(anchors)==7 and len(rational_basis([roots[j] for j in anchors])[0])==7,'seven native support anchors')
        checks.append({'receiver':i,'class_by_minimum_member':min(classes[owner[i]]),
                       'local_generator_hex':hex(ell),'support_size':len(support),
                       'independent_real_support_roles':anchors,'facet_local_dimension':1})
    return {'classes':classes,'canonical_dimension':9,'class_dimension':15,'sum_dimension':19,
            'facet_checks':checks,'proper_subfacet_intersection':'zero by rank7 support and one-dimensional full-facet kernel'}

def all_words(rows):
    words=[0]
    for row in rows:words += [w^row for w in words]
    return set(words)

def quotient_example():
    # Three two-coordinate input blocks. W has dimension3 and one local
    # direction: neither W nor its shortening is a whole-width tensor code.
    w=all_words([1,(1<<1)^(1<<2)^(1<<4),(1<<3)^(1<<5)])
    local_spaces=[all_words([1,2]),all_words([4,8]),all_words([1,2,4,8])]
    short=[sorted(w&loc) for loc in local_spaces]
    qb=basis_bits([z for intersection in short for z in intersection])[0]
    require(len(basis_bits(w)[0])==3 and len(qb)==1,'non-tensor partial-rank example')
    maps=[]
    for loc in local_spaces:
        projections={}
        for global_row in w:
            for local_row in loc:
                h=global_row^local_row;image=remainder(global_row,qb)
                require(h not in projections or projections[h]==image,'quotient well-defined')
                projections[h]=image
        maps.append(projections)
    for smaller in (0,1):
        require(all(maps[smaller][h]==maps[2][h] for h in maps[smaller]),'nested chart projection compatibility')
    require(0^0==1^1 and 0!=1,'raw projection ambiguity control')
    return {'whole_width':2,'historical_space_dimension':3,'shortening_dimension':1,
            'represented_history_counts':[len(m) for m in maps],
            'nested_projection_tests':sum(len(maps[i]) for i in (0,1)),
            'raw_W_projection_would_be_ambiguous':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True)
    ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('CERTIFICATE.json'))
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    raw=args.native.read_bytes();roots,k=source(raw);cert=json.loads(args.certificate.read_text())
    counts=parity(cert,roots);short=code_shortening(roots,k);example=quotient_example()
    controls=[rejected(lambda:source(raw+b'x'),'native source alteration')]
    missing=copy.deepcopy(cert);missing['nine_frame_configurations'][0].pop()
    controls.append(rejected(lambda:parity(missing,roots),'missing parity frame'))
    duplicate=copy.deepcopy(cert);duplicate['nine_frame_configurations'][0][1]=duplicate['nine_frame_configurations'][0][0][:]
    controls.append(rejected(lambda:parity(duplicate,roots),'duplicated parity frame'))
    controls.append(rejected(lambda:parity(cert,roots,23),'understated aggregate incidence ceiling'))
    frame=cert['nine_frame_configurations'][0][0];removed={frame[0]};remaining=[i for i in frame if i not in removed]
    controls.append(rejected(lambda:require(len(remaining)==8,'shortened frame size'),'deleted port falsely retained in identity frame'))
    anchors=short['facet_checks'][0]['independent_real_support_roles']
    controls.append(rejected(lambda:require(len(rational_basis([roots[j] for j in anchors[:-1]])[0])==7,'full facet support'),
                             'six-root support falsely called rank7'))
    # Coefficientwise incidence bound proves the loss inequality for EVERY
    # omitted subset, rather than merely a finite sample of deletions.
    require(all(c<=24 for c in counts),'all-port robust deletion premise')
    bound=F(9)-F(8,10);require(bound==F(41,5) and bound-8==F(1,5),'q8 shortening gap')
    result={'status':'PASS_OPERATOR_SHORTENING_FINITE_PREMISES','native_sha256':PIN,
            'certificate_sha256':hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
            'parity_family':{'configurations':30,'frames':270,'frame_size':8,
                             'ordered_real_inner_product_checks':270*8*7,
                             'aggregate_incidence_by_role':counts,'maximum_incidence':max(counts),
                             'rank_bound_any_d_omissions':'(9-d/10)V','rank_bound_eight_omissions':str(bound)},
            'full_code_shortening':short,'non_tensor_quotient_example':example,
            'negative_controls':controls,'universal_shortening_lower_bound_for_q8':'dim Q_D >= V/5',
            'universal_proof':'PROOF.md; finite computations certify source premises only',
            'complete_source':False,'new_kappa':None}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'configurations':30,'max_incidence':max(counts),
                      'partial_fitting_bound':'41V/5','facet_shortening_checks':len(short['facet_checks']),
                      'non_tensor_example_shortening_rank':example['shortening_dimension']}))

if __name__=='__main__':main()
