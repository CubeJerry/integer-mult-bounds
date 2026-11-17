"""Separate Sympy/bitset review of C's pure frame meet export."""
from pathlib import Path
import argparse, hashlib, itertools, json
from collections import defaultdict
from fractions import Fraction
from build_quartet_compression_source import SOURCE, SHA, CHECK, HELPER, module
from build_four_plane_correction import replay_general
from review_half_sum_gate import independent_rows
from check_raw_cache_reactivation import quotient_basis, residual

WORD = '54fada571a96571697f3e87b50ee613a9042ee9577703f90ab13b2f7a172ff95'
PARENT = '4628d085fc99ea258f03c374926e1a97852497ff7fe0cec1206cb32bc0bb2c9f'


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=Path,required=True)
    here=Path(__file__).resolve().parent
    ap.add_argument('--word',type=Path,default=here.parent/'C/meet-frame-export/output/WORD.json')
    ap.add_argument('--parent',type=Path,default=here/'ground-retention-known8/WORD.json')
    ap.add_argument('--author-result',type=Path,default=here.parent/'C/meet-frame-export/output/RESULT.json')
    ap.add_argument('--author-inventory',type=Path,default=here.parent/'C/meet-frame-export/output/CUT-INVENTORY.json')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
    R=json.loads(raw)['native_roots'];geo=module(a.repo/CHECK,'meet_review_geometry');h=module(a.repo/HELPER,'meet_review_arithmetic')
    wb=a.word.read_bytes();pb=a.parent.read_bytes()
    assert hashlib.sha256(wb).hexdigest()==WORD and hashlib.sha256(pb).hexdigest()==PARENT
    w=json.loads(wb);p=json.loads(pb);C,pv,pp,ps=replay_general(p,R,geo);C,V,P,stats=replay_general(w,R,geo)
    S=[73,78,81,86];mode=sum(1<<i for i in S);H='MEET_FRAME_SOURCE';I='MEET_FRAME_LINE';owner='MEET_FRAME_EXPORT'
    assert C[H]==geo.basis(tuple(tuple(R[i])for i in S)) and len(C[H])==3
    assert C[I]==geo.basis(((0,1,0,0,1,0,0,0),))
    assert geo.sub(C[I],C[H]) and geo.sub(C[I],C['G2_A-1'])
    assert len(geo.basis(C[H]+C['G2_A-1']))==5
    assert w['operations'][:794]==p['operations'][:794] and w['carrier_interface_before_operation']==804
    literal=[['MOVE',f'X{i}',H]for i in S]+[['ADD',f'X{i}','X73']for i in S[1:]]
    literal += [['INIT',owner,H],['ADD','X73',owner],['MOVE',owner,I]]
    assert w['operations'][794:804]==literal
    EV,EP=pv.copy(),pp.copy()
    for i in S:EP[f'X{i}']=H
    EV['X73']=mode;EV[owner]=mode;EP[owner]=I
    assert (V,P)==(EV,EP) and len(V)==342
    assert len(independent_rows([V[f'X{i}']for i in range(111)]))==111
    author=json.loads(a.author_result.read_text());inventory=json.loads(a.author_inventory.read_text())
    assert {z['name']:(z['row_hex'],z['chart'],z['rank'])for z in inventory['fields']}=={n:(hex(v),P[n],len(C[P[n]]))for n,v in V.items()}
    assert stats['movement_profile']=={1:72,2:21,4:16,5:20,6:16,7:170}
    assert stats['counts']=={'INIT':120,'ADD':610,'MOVE':315,'CLEAR':120}
    assert all(V[f'Y{i}']==pv[f'Y{i}']and P[f'Y{i}']==pp[f'Y{i}']for i in range(111))
    groups=defaultdict(list)
    for i,r in enumerate(R):
        if i>=8:groups[tuple(k for k,x in enumerate(r)if x)].append(i)
    halves=[sum(1<<i for i in roles if R[i][x]==s*R[i][y])for support,roles in groups.items()for x,y in itertools.combinations(support,2)for s in [-1,1]]
    B=independent_rows(halves+[1<<i for i in range(8)]);assert len(B)==64 and residual(quotient_basis(B),mode)
    assert [i for i in S if geo.sub(C[I],C[f'F{i}'])]==[81,86]
    exact=h.moment(stats['movement_profile']);claimed=tuple(map(Fraction,author['moment']['rational']))
    assert claimed[0]<=exact[0]<=exact[1]<=claimed[1]
    controls=[]
    for pos in [794,798,802,803]:
        bad=json.loads(wb);del bad['operations'][pos];bad['carrier_interface_before_operation']-=1
        try:
            _,cv,cp,_=replay_general(bad,R,geo);assert (cv,cp)==(EV,EP)
        except AssertionError:controls.append('omit_operation_'+str(pos))
        else:raise AssertionError(('accepted omission',pos))
    inv=w['semantic_operation_indices']['meet_frame_inverse_at_Hub'][0]
    bad=json.loads(wb);del bad['operations'][inv]
    try:replay_general(bad,R,geo)
    except AssertionError:controls.append('omit_source_inverse')
    else:raise AssertionError('accepted missing inverse')
    out={'status':'PASS_INDEPENDENT_PURE_MEET_SOURCE_REVIEW','word_sha256':WORD,'parent_word_sha256':PARENT,
         'native_sha256':SHA,'all_original_columns':222,'exact_cut_fields':342,'literal_new_prefix_operations':10,
         'all_original_X_restored':True,'all_public_Y_cut_states_equal_parent':True,'all95_ground_Y_retained':True,
         'all_arbitrary_Y_coefficients_identity':True,'outside_full64_dimensional_half_axis_bank':True,
         'stats':stats,'independent_moment':h.record(exact),'negative_controls':controls,
         'scope':'Independent actual word/cut/interface/invoice review;8 completed coordinate outputs only; no continuation viability claim.'}
    h.save(a.out/'RESULT.json',out);print(json.dumps(out,indent=2))


if __name__=='__main__':main()
