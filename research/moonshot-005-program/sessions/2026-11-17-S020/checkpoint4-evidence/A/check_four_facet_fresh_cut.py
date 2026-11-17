"""Four actual untouched columns force four future downward transfers.

The current cuts and all222 columns are replayed. This is an author certificate,
using credited retained geometry and word-interpreter helpers.
"""
from pathlib import Path
import argparse
import hashlib
import json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general

CASES=[('low-retention-corrections','c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'),
       ('proper-query-exports','4d4e0a4163483d35741505c747981a2bc8b8da1bc373bb0cb8d10f0aa651f96c')]
ROLES=[8,9,14,15]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--inputs',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'four-facet-fresh-cut')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    geo=module(a.repo/CHECK,'fresh_four_geometry');h=module(a.repo/HELPER,'fresh_four_helper')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    R=json.loads(raw)['native_roots'];source_mask=sum(1<<i for i in ROLES)
    dots=[[sum(x*y for x,y in zip(R[i],R[j]))for j in ROLES]for i in ROLES]
    assert all(all(z!=0 for z in row)for row in dots)
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in h.moment(gate));results=[]
    for folder,pin in CASES:
        wb=(a.inputs/folder/'WORD.json').read_bytes();assert hashlib.sha256(wb).hexdigest()==pin
        w=json.loads(wb);C,values,places,stats=replay_general(w,R,geo)
        inv=json.loads((a.inputs/folder/'CUT-INVENTORY.json').read_text())
        assert inv['word_sha256']==pin and inv['cut_before_operation']==w['carrier_interface_before_operation']
        assert {f['name']:(f['chart'],int(f['row_hex'],16))for f in inv['fields']}=={n:(places[n],v)for n,v in values.items()}
        inside=[n for n in values if any(geo.sub(C[places[n]],C[f'F{i}'])for i in ROLES)]
        assert all(values[n]&source_mask==0 for n in inside)
        outside_sources=[n for n,v in values.items()if v&source_mask]
        assert all(not any(geo.sub(C[places[n]],C[f'F{i}'])for i in ROLES)for n in outside_sources)
        moment=h.moment(stats['movement_profile']);room=(ceiling[0]-moment[1],ceiling[1]-moment[0])
        results.append({'source':folder,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],
                        'cut_fields':len(values),'inside_union_field_count':len(inside),
                        'inside_union_fields':inside,'fields_carrying_selected_X_columns':outside_sources,
                        'selected_X_column_rank_inside_union':0,
                        'required_final_selected_X_column_rank_inside_union':4,
                        'necessary_future_owned_downward_transfers_with_monotone_public_routes':4,
                        'closed_partial_profile':stats['movement_profile'],
                        'closed_partial_moment':h.record(moment),'necessary_limiting_room':h.record(room),
                        'conditional_total_with_independent_75_upward_exit_bound':79,
                        'conditional_budget_rejection':79>room[1]})
    out={'status':'PASS_ACTUAL_FOUR_FACET_FRESH_CUT','source_sha256':SHA,'roles':ROLES,
         'native_dot_product_matrix':dots,'cases':results,
         'scope':'Unconditional four-future-downward-transfer necessity at the two exact cuts under monotone public routes and whole-record fields. Combining with75 upward departures requires the separately proved fixed descending-history bank premise. No universal source exclusion or new kappa.'}
    h.save(a.out/'CERTIFICATE.json',out)
    print(json.dumps({'status':out['status'],'roles':ROLES,'cases':[{k:v for k,v in r.items()if k not in ['inside_union_fields']}for r in results]},indent=2))


if __name__=='__main__':main()
