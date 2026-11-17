"""Independent check of C's 279 forced-coordinate/normal witnesses per cut."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import argparse
import hashlib
import json
from sympy import Matrix

HERE=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,default=HERE)
    ap.add_argument('--author-certificate',type=Path,default=HERE.parent/'C/forced-raw-fanout/output/CERTIFICATE.json')
    ap.add_argument('--out',type=Path,default=HERE/'forced-raw-fanout-review');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=(a.inputs/'SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    R=json.loads(raw)['native_roots'];assert len({tuple(Matrix([r]).rref()[0])for r in R})==111
    own=json.loads((a.inputs/'raw-cache-reactivation/CERTIFICATE.json').read_text())
    cut=json.loads((a.inputs/'four-facet-fresh-cut/CERTIFICATE.json').read_text())
    author_bytes=a.author_certificate.read_bytes();author=json.loads(author_bytes);results=[]
    for case in author['cases']:
        src=case['source'];observations=next(z for z in own['cases']if z['source']==src)
        fresh=next(z for z in cut['cases']if z['source']==src)
        assert case['word_sha256']==observations['word_sha256']==fresh['word_sha256']
        by_i={r['receiver']:r for r in observations['receivers']};hist=Counter();duals=0;exits=0
        assert sorted(z['expired_role']for z in case['fanout'])==observations['expired_native_cache_roles']
        for f in case['fanout']:
            j=f['expired_role'];I=f['independent_receiver_roles'];M=Matrix([R[i]for i in I]);rank=M.rank()
            assert rank==len(I)==f['demand_normal_rank'] and rank in [6,7]
            assert all(sum(x*y for x,y in zip(R[i],R[j]))==0 for i in I)
            if rank==7:
                null=M.nullspace();assert len(null)==1
                assert Matrix.hstack(null[0],Matrix(R[j])).rank()==1
            assert [d['receiver']for d in f['dual_witnesses']]==I
            for d in f['dual_witnesses']:
                i=d['receiver'];v=int(d['dual_hex'],16);o=by_i[i];eligible=o['eligible_expired_raw_coordinates']
                assert eligible==d['eligible_raw_coordinates']and j in eligible
                assert v>>i&1 and v>>j&1
                assert all((int(row,16)&v).bit_count()%2==0 for row in o['combined_basis_hex'])
                assert all(not(v>>k&1)for k in eligible if k!=j)
                duals+=1
            bound=1+int(rank==7);assert bound==f['minimum_native_line_departures'];exits+=bound;hist[rank]+=1
        assert dict(hist)=={7:39,6:1}and exits==79 and duals==279
        assert observations['ground_public_Y_roles']==[4,5,6,7]
        assert case['minimum_owned_upward_moves']==exits-4==75
        assert case['fresh_cut_roles']==cut['roles']==[8,9,14,15]
        assert case['fresh_cut_inside_field_count']==fresh['inside_union_field_count']
        assert case['minimum_owned_downward_moves']==fresh['necessary_future_owned_downward_transfers_with_monotone_public_routes']==4
        assert case['minimum_total_future_owned_moves']==79
        room_hi=Fraction(fresh['necessary_limiting_room']['rational'][1]);assert Fraction(79)>room_hi
        results.append({'source':src,'checked_duals':duals,'normal_rank_histogram':dict(hist),
                        'native_line_departures':79,'owned_upward_moves':75,'independent_future_owned_downward_moves':4,
                        'total_future_owned_moves':79,'exact_positive_excess_lower_bound':str(Fraction(79)-room_hi)})
    result={'status':'PASS_INDEPENDENT_FORCED_SOURCE_FANOUT_REVIEW',
            'author_certificate_sha256':hashlib.sha256(author_bytes).hexdigest(),'cases':results,
            'scope':'Checks C fanout duals against A separately derived actual-cut observation spaces, native exact normal geometry, and independent four-facet cut. Uses fixed descending bank and monotone public routes. No universal source exclusion.'}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
