#!/usr/bin/env python3
"""Independent exact certificate for full-facet acquisition obstruction.

Geometry is over the reals. Integer minors reduced modulo a proved prime
certify their nonzero integer determinants. Binary payload ranks are separate.
"""
import argparse,hashlib,importlib.util,json,math
from pathlib import Path

SOURCE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
PIN='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
P=1009
PAIRS=[(a,b)for a in range(8)for b in range(a,8)]

def choose_rows_and_columns(rows,p=P):
    basis={};chosen=[]
    for row_id,rr in enumerate(rows):
        a=[z%p for z in rr]
        while any(a):
            j=next(k for k,x in enumerate(a)if x)
            if j in basis:
                q=a[j];a=[(x-q*y)%p for x,y in zip(a,basis[j])]
            else:
                q=pow(a[j],-1,p);basis[j]=[x*q%p for x in a];chosen.append(row_id);break
    return chosen,sorted(basis)

def determinant_mod(a,p=P):
    a=[[x%p for x in rr]for rr in a];n=len(a);d=1
    for j in range(n):
        k=next((k for k in range(j,n)if a[k][j]),None)
        if k is None:return 0
        if k!=j:a[k],a[j]=a[j],a[k];d=-d
        pivot=a[j][j];d=d*pivot%p;inv=pow(pivot,-1,p)
        for k in range(j+1,n):
            q=a[k][j]*inv%p
            a[k]=[(x-q*y)%p for x,y in zip(a[k],a[j])]
    return d%p

def bits(z):return sum(1<<i for i in z)
def inds(z):return [i for i in range(111)if z>>i&1]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def quad(r):return [r[a]*r[b]for a,b in PAIRS]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--audit-module',type=Path,default=Path(__file__).resolve().parents[1]/'portable'/'audit_cp6.py');a=ap.parse_args()
    sp=importlib.util.spec_from_file_location('own_exact_geometry',a.audit_module);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);need=m.insist
    source=a.repo/SOURCE;need(m.sha(source)==PIN,'pinned native roots');R=json.loads(source.read_text())['native_roots'];need(len(R)==111,'native dimension')
    need(all(P%d for d in range(2,math.isqrt(P)+1)),'modulus is prime')
    N=[{j for j,r in enumerate(R)if dot(R[i],r)==0}for i in range(111)];K=[z^{i}for i,z in enumerate(N)]
    nb=m.binary_basis(N);kb=m.binary_basis(K);need(len(nb)==108 and len(kb)==9,'independent actual payload ranks')
    chosen_N=[];chosen_K=[];b={}
    for i,z in enumerate(N):
        if not m.in_span(z,b):chosen_N.append(i);b=m.binary_basis(N[j]for j in chosen_N)
    b={}
    for i,z in enumerate(K):
        if not m.in_span(z,b):chosen_K.append(i);b=m.binary_basis(K[j]for j in chosen_K)
    kernel=[]
    for free in set(range(111))-set(nb):
        h=1<<free
        for p,row in sorted(nb.items()):
            if (row&h).bit_count()&1:h^=1<<p
        need(all(not((bits(z)&h).bit_count()&1)for z in N),'kernel vector exact');kernel.append(inds(h))
    need(len(kernel)==len(m.binary_basis(kernel))==3,'full rank-three payload kernel')
    certificates=[]
    for i,neighbors in enumerate(N):
        facet=m.chart({'kind':'ann','rows':[R[i]]});span=m.reduced(tuple(tuple(R[j])for j in sorted(neighbors)))
        need(len(facet)==7 and span==facet,('full real support facet',i))
        ids=sorted(neighbors);matrix=[quad(R[j])for j in ids];selected,columns=choose_rows_and_columns(matrix)
        need(len(selected)==len(columns)==28,('full restricted quadratic rank',i))
        minor=[[matrix[j][c]for c in columns]for j in selected];d=determinant_mod(minor);need(d!=0,('nonzero exact integer minor',i))
        # Deliberately singular negative control exercises determinant arithmetic.
        bad=[row[:]for row in minor];bad[0]=bad[1][:];need(determinant_mod(bad)==0,'duplicate-row negative control')
        certificates.append({'facet':i,'support_size':len(neighbors),'real_support_rank':7,'quadratic_rank':28,'selected_native_roles':[ids[j]for j in selected],'selected_ambient_monomial_columns':[list(PAIRS[c])for c in columns],'determinant_mod_1009':d})
    # A union of two genuine proper subcharts must fail full quadratic rank.
    F=m.chart({'kind':'ann','rows':[R[0]]});B1=m.chart({'kind':'ann','rows':[R[0],R[1]]});B2=m.chart({'kind':'ann','rows':[R[0],R[2]]})
    need(len(F)==7 and len(B1)==len(B2)==6 and B1!=B2,'two actual distinct proper predecessor charts')
    covered=[j for j in sorted(N[0])if dot(R[j],R[1])==0 or dot(R[j],R[2])==0];rr,cc=choose_rows_and_columns([quad(R[j])for j in covered]);need(len(rr)<28,'union-of-two-subcharts negative control')
    product_witness=None
    for u in F:
        for v in F:
            z=tuple(x+y for x,y in zip(u,v))
            if dot(z,R[1])*dot(z,R[2]):product_witness=[str(x)for x in z];break
        if product_witness:break
    need(product_witness is not None,'product of defining linear forms is nonzero on facet')
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    allowance=tuple(z/6 for z in m.moment(gate));conditional=m.moment({1:780,7:111,8:9});conditional_margin=(allowance[0]-conditional[1],allowance[1]-conditional[0]);separated=m.moment({1:74,7:222,8:9});excess=(separated[0]-allowance[1],separated[1]-allowance[0])
    need(conditional_margin[0]>0 and excess[0]>0,'exact optimistic and obstructed budget comparisons')
    result={'status':'PASS_ALL111_QUADRATIC_FACET_SOURCE_OBSTRUCTION','source_path':SOURCE,'source_sha256':PIN,'geometry':'real charts; nonzero integer minors certified modulo prime 1009','payload':'binary/characteristic-two ranks, separate from geometry','orthogonality_payload_rank':108,'canonical_payload_rank':9,'independent_N_roles':chosen_N,'independent_K_roles':chosen_K,'N_kernel_basis':kernel,'quadratic_minor_certificates':certificates,'universal_source_obstruction':{'scope':'Only the 111 original X records transport input information; X ascends, all other input-independent zero-born records are stationary; arbitrary local processing allowed; no owned MOVE.','minimum_distinct_X_visitors_per_full_correction_facet':3,'maximum_distinct_full_correction_facets':37,'assertion':'An actual full pure N_i record at F_i needs three arrivals. Masked or distributed corrections and moving Y originals are outside this count.'},'negative_controls':{'duplicate_minor_row_is_singular':True,'two_proper_subchart_cover':{'target':0,'other_normals':[1,2],'covered_native_roles':covered,'quadratic_rank_mod_1009':len(rr),'nonzero_defining_product_point':product_witness}},'conditional_108_source_bridge':{'status':'Accounting and algebra valid under an impossible X-only source hypothesis; not an admitted supplier','maximum_X_movement':777,'nine_code_fields_Hub_to_ground':9,'remaining_full_correction_fields_Hub_to_facet':3,'complete_movement_upper_bound':m.interval_json(conditional),'necessary_allowance':m.interval_json(allowance),'optimistic_room':m.interval_json(conditional_margin)},'separated_full_correction_architecture':{'at_least_individual_Hub_to_facet_corrections':74,'complete_movement_lower_bound':m.interval_json(separated),'excess_over_necessary_allowance':m.interval_json(excess),'scope':'At most 37 source-acquired full facet corrections; every remaining N_i acquired at Hub and sent individually to F_i; nine canonical fields sent Hub-to-ground; all originals closed.'},'kappa_status':'No new kappa. A stronger earlier source or interleaved receiver/descending construction remains necessary.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print('Payload ranks N,K:',len(nb),len(kb));print('111/111 real quadratic ranks28; at least3 arrivals; at most37 full facets.');print('Separated-architecture movement excess:',m.interval_json(excess)['decimal'])
if __name__=='__main__':main()
