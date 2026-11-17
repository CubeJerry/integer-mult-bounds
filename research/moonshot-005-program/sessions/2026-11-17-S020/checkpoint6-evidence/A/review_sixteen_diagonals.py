"""Independent Sympy/bitset review of C's proper16-diagonal source."""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general

WORD='6256e8349cd6b74e91bcd225141eb84325557eda92fba25cc51ed288dd4a7000'
PARENT='eb49a700e9d815d975120ba56271d414a2a15ee01254c8f5f3203fdfb52c2a59'
FRAMES=[([14,17,19,20],[0,2,4,6]),([96,99,101,102],[1,3,5,7])]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);here=Path(__file__).resolve().parent
    ap.add_argument('--word',type=Path,default=here.parent/'C/parity-sixteen-diagonals/output/WORD.json')
    ap.add_argument('--parent',type=Path,default=here/'parity-receiver-relays/WORD.json')
    ap.add_argument('--author-result',type=Path,default=here.parent/'C/parity-sixteen-diagonals/output/RESULT.json')
    ap.add_argument('--author-inventory',type=Path,default=here.parent/'C/parity-sixteen-diagonals/output/CUT-INVENTORY.json')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots']
    wb=a.word.read_bytes();pb=a.parent.read_bytes();assert hashlib.sha256(wb).hexdigest()==WORD and hashlib.sha256(pb).hexdigest()==PARENT
    w=json.loads(wb);p=json.loads(pb);geo=module(a.repo/CHECK,'sixteen_review_geometry');h=module(a.repo/HELPER,'sixteen_review_intervals')
    C,pv,pp,_=replay_general(p,R,geo);C,V,P,stats=replay_general(w,R,geo)
    expected=p['operations'][:1921]+[['ADD',f'AXIS_{j}',f'Y{i}']for S,support in FRAMES for i in S for j in range(8)if j not in support]+p['operations'][1921:2021]
    new=[];EV=pv.copy();EP=pp.copy()
    for k,(S,support)in enumerate(FRAMES):
        G=next(g['quartet_chart']for g in p['construction']['quartets']if g['support']==support)
        q=sum(1<<i for i in S);collector=f'DIAGONAL_CLIQUE_{k}'
        expected.append(['INIT',collector,G]);new.append(collector)
        expected.extend([['ADD',f'PARITY_{k}_RAW{i}',collector]for i in S])
        for t,i in enumerate(S):
            if t<3:
                name=f'DIAGONAL_COPY_{k}_{i}';new.append(name)
                expected.extend([['INIT',name,G],['ADD',collector,name]])
            else:name=collector
            T=f'PARITY_{k}_T{i}';expected.extend([['MOVE',name,T],['ADD',name,f'Y{i}']])
            assert len(C[G])==4 and len(C[T])==3 and geo.sub(C[T],C[G])and geo.sub(C[T],C[f'F{i}'])
            assert all(pv[f'PARITY_{k}_RAW{j}']==1<<j and pp[f'PARITY_{k}_RAW{j}']==G for j in S)
            EV[f'Y{i}']=(1<<(111+i))^(1<<i);EV[name]=q;EP[name]=T
    assert len(expected)==2091
    expected.extend(p['operations'][2021:]);expected.extend([['CLEAR',n]for n in new])
    assert w['operations']==expected and w['carrier_interface_before_operation']==2091
    assert (V,P)==(EV,EP) and len(V)==424
    completed=[i for i in range(111)if V[f'Y{i}']==(1<<(111+i))^(1<<i)]
    assert completed==sorted(list(range(8))+[i for S,_ in FRAMES for i in S])
    assert len(completed)==16 and sum(P[f'Y{i}']=='zero'for i in range(111))==95
    author=json.loads(a.author_result.read_text());inventory=json.loads(a.author_inventory.read_text())
    assert {z['name']:(z['row_hex'],z['chart'],z['rank'])for z in inventory['fields']}=={n:(hex(v),P[n],len(C[P[n]]))for n,v in V.items()}
    assert stats['movement_profile']=={1:195,2:107,3:8,4:111,7:103}
    assert stats['counts']=={'INIT':202,'ADD':1476,'MOVE':524,'CLEAR':202}
    exact=h.moment(stats['movement_profile']);claimed=tuple(map(Fraction,author['source_moment']['rational']))
    assert claimed[0]<=exact[0]<=exact[1]<=claimed[1]
    controls=[]
    for key in ['remove_target_axis_at_ground','actual_clique_raw_gather','actual_clique_copy','proper_diagonal_unit_descent','proper_diagonal_actual_add']:
        bad=json.loads(wb);index=w['semantic_operation_indices'][key][0];del bad['operations'][index];bad['carrier_interface_before_operation']-=1
        try:
            _,bv,bp,_=replay_general(bad,R,geo);assert (bv,bp)==(V,P)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(('accepted omitted operation',key))
    bad=json.loads(wb);j=w['semantic_operation_indices']['remove_target_axis_at_ground'][0];op=bad['operations'].pop(j)
    k=next(k for k,z in enumerate(bad['operations'])if z[:2]==['MOVE',op[2]])
    bad['operations'].insert(k+1,op)
    try:replay_general(bad,R,geo)
    except AssertionError:controls.append('late_ground_axis_read_rejected')
    else:raise AssertionError('accepted late unavailable read')
    out={'status':'PASS_INDEPENDENT_SIXTEEN_DIAGONAL_SOURCE','word_sha256':WORD,'parent_word_sha256':PARENT,
         'all_original_columns':222,'exact_cut_fields':424,'literal_whole_word_reconstruction':True,
         'completed_diagonal_roles':completed,'completed_diagonal_count':16,'other95_Y_at_ground':True,
         'all111_original_X_restored':True,'arbitrary_initial_Y_identity':True,
         'global_known_raw_coordinate_roles':list(range(8)),'eight_additional_proper_clique_fields':True,
         'stats':stats,'independent_moment':h.record(exact),'negative_controls':controls,
         'scope':'Exact actual source review;16 completed output values at their actual proper charts, only8 known raw axis fields atground; no complete supplier or inherited nine-descent claim.'}
    h.save(a.out/'RESULT.json',out);print(json.dumps(out,indent=2))


if __name__=='__main__':main()
