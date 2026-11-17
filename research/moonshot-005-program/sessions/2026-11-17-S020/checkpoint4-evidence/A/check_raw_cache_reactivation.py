"""Exact source-aware raw-cache reactivation minima by meet in the middle.

No subset-size sampling: all eligible expired-coordinate subsets are covered.
This is an author certificate; geometry helpers are credited dependencies.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
from build_quartet_compression_source import SOURCE,SHA,CHECK,module
from review_half_sum_gate import independent_rows

CASES=[('low-retention-corrections','c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe','full_query'),
       ('proper-query-exports','4d4e0a4163483d35741505c747981a2bc8b8da1bc373bb0cb8d10f0aa651f96c','sign_query')]


def quotient_basis(rows):
    return sorted(independent_rows(rows),key=lambda x:(x&-x).bit_length())


def residual(rows,value):
    for row in rows:
        if value&(row&-row):value^=row
    return value


def subset_map(columns,roles):
    """All half-subsets, retaining a minimum-weight native mask per syndrome."""
    out={0:(0,0)};syndrome=mask=previous=0
    for index in range(1,1<<len(columns)):
        gray=index^(index>>1);changed=(gray^previous).bit_length()-1;previous=gray
        syndrome^=columns[changed];mask^=1<<roles[changed]
        candidate=(gray.bit_count(),mask)
        if syndrome not in out or candidate<out[syndrome]:out[syndrome]=candidate
    return out


def minimum_raw_grant(basis,target,roles):
    goal=residual(basis,target);columns=[residual(basis,1<<j)for j in roles];middle=len(roles)//2
    left=subset_map(columns[:middle],roles[:middle]);right=subset_map(columns[middle:],roles[middle:])
    best=None
    for syndrome,(weight,mask)in left.items():
        other=right.get(goal^syndrome)
        if other is None:continue
        candidate=(weight+other[0],mask|other[1])
        if best is None or candidate<best:best=candidate
    assert best is not None and residual(basis,target^best[1])==0
    assert best[0]==best[1].bit_count()
    return best,{'target_residual_hex':hex(goal),'raw_coordinate_residuals_hex':[hex(x)for x in columns],
                 'left_subsets_enumerated':1<<middle,'right_subsets_enumerated':1<<(len(roles)-middle),
                 'left_distinct_syndromes':len(left),'right_distinct_syndromes':len(right)}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--inputs',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'raw-cache-reactivation')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);e=module(a.repo/CHECK,'raw_cache_geometry')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots'];xmask=(1<<111)-1
    N=[sum(1<<j for j,s in enumerate(R)if sum(u*v for u,v in zip(r,s))==0)for r in R]
    K=[n^(1<<i)for i,n in enumerate(N)];results=[]
    for folder,pin,kind in CASES:
        word_bytes=(a.inputs/folder/'WORD.json').read_bytes();assert hashlib.sha256(word_bytes).hexdigest()==pin
        w=json.loads(word_bytes);inv=json.loads((a.inputs/folder/'CUT-INVENTORY.json').read_text())
        assert inv['word_sha256']==pin and inv['cut_before_operation']==w['carrier_interface_before_operation']
        C={name:e.chart(c)for name,c in w['charts'].items()};fields=inv['fields'];byname={f['name']:f for f in fields}
        ground=[i for i in range(111)if len(C[byname[f'Y{i}']['chart']])==0];assert ground==[4,5,6,7]
        expired=[i for i in range(111)if len(C[byname[f'X{i}']['chart']])>1];assert len(expired)==40
        assert all(byname[f'NATIVE_{i}']['chart']==f'L{i}'and int(byname[f'NATIVE_{i}']['row_hex'],16)==1<<i for i in range(111))
        initial=[]
        for f in fields:
            if not f['name'].startswith('NATIVE_'):initial.append(f)
        D=list({int(v,16)&(~255 if kind=='sign_query'else xmask)for v in w['Y_correction_rows_hex']})
        G=quotient_basis(K+D);assert len(G)==21 and len(independent_rows(D))==12
        records=[]
        for i in range(111):
            available=[f for f in initial if e.sub(C[f['chart']],C[f'F{i}'])]
            local=[int(f['row_hex'],16)&xmask for f in available]
            basis=quotient_basis(G+local);eligible=[j for j in expired if N[i]>>j&1]
            (minimum,witness),audit=minimum_raw_grant(basis,1<<i,eligible)
            assert minimum>0
            records.append({'receiver':i,'visible_initial_fields':[f['name']for f in available],
                            'initial_visible_X_rank':len(independent_rows(local)),'combined_observation_rank':len(basis),
                            'combined_basis_hex':list(map(hex,basis)),'eligible_expired_raw_coordinates':eligible,
                            'minimum_added_raw_coordinates':minimum,'one_minimum_raw_grant':[j for j in eligible if witness>>j&1],
                            **audit})
        histogram=dict(sorted(Counter(r['minimum_added_raw_coordinates']for r in records).items()));maximum=max(histogram)
        result={'source':folder,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],'global_bank_kind':kind,
                'global_bank_rank':21,'current_query_rank':12,'ground_public_Y_roles':ground,'expired_native_cache_roles':expired,
                'minimum_raw_grant_histogram':histogram,'maximum_receiver_minimum':maximum,
                'maximizing_receivers':[r['receiver']for r in records if r['minimum_added_raw_coordinates']==maximum],
                'receivers_not_recoverable_with_four_raw_grants':sum(r['minimum_added_raw_coordinates']>4 for r in records),
                'necessary_additional_owned_native_cache_upward_departures_if_global_bank_fixed':maximum-len(ground),
                'receivers':records}
        results.append(result)
    out={'status':'PASS_EXACT_RAW_CACHE_REACTIVATION_MINIMA','source_sha256':SHA,'cases':results,
         'scope':'Necessary affine-information condition for linear continuations with monotone public routes and every future descending X payload inside the stated global bank. Arbitrary initial Y is generously known. Native-cache raw coordinates may be recovered by the four ground public Ys or paid owned upward departures. New descending modes outside the bank are not covered. No complete-source impossibility.'}
    (a.out/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'cases':[{k:v for k,v in z.items()if k!='receivers'}for z in results]},indent=2))


if __name__=='__main__':main()
