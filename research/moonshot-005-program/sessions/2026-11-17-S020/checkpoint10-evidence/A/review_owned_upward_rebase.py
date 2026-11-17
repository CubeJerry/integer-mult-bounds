"""Focused independent replay of the explicit paid-owned-turn model."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import argparse,hashlib,inspect,json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general
WORD='581266484817956c8f6b1dc279291a362ddf00a4c580f25a35f3fe56670c7729'
PARENT='91d4a24a995a18ed306b6c657e76e9cac1f14c8077b4143aae94581b50e2eb6e'

def paid_replay(w,R,g):
    # Reuse A's independent222-column interpreter with exactly one declared
    # change: owned moves may go either nested direction, at the same |gap|^t
    # tariff. Public direction, all ADD/INIT/CLEAR rules and endpoints remain.
    source=inspect.getsource(replay_general)
    old='assert geometry.sub(after, before) if name in owners else geometry.sub(before, after)'
    new='assert (geometry.sub(after, before) or geometry.sub(before, after)) if name in owners else geometry.sub(before, after)'
    assert source.count(old)==1
    scope={'Counter':Counter};exec(source.replace(old,new),scope)
    C,V,P,stats=scope['replay_general'](w,R,g)
    places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    owned=set();up=[];down=Counter()
    for j,(op,n,*a)in enumerate(w['operations']):
        if op=='INIT':owned.add(n);places[n]=a[0]
        elif op=='MOVE':
            gap=len(C[a[0]])-len(C[places[n]])
            if n in owned:
                if gap>0:up.append({'operation':j,'field':n,'from':places[n],'to':a[0],'gap':gap})
                else:down[-gap]+=1
            places[n]=a[0]
        elif op=='CLEAR':owned.remove(n);del places[n]
    stats['owned_upward_moves']=up;stats['owned_downward_profile']=dict(down)
    return C,V,P,stats

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);here=Path(__file__).resolve().parent
    ap.add_argument('--inputs',type=Path,default=here.parent/'C/owned-upward-half-rebase/output')
    ap.add_argument('--parent',type=Path,default=here/'proper-half-service/WORD.json')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    rb=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(rb).hexdigest()==SHA;R=json.loads(rb)['native_roots']
    wb=(a.inputs/'WORD.json').read_bytes();pb=a.parent.read_bytes()
    assert hashlib.sha256(wb).hexdigest()==WORD and hashlib.sha256(pb).hexdigest()==PARENT
    w=json.loads(wb);p=json.loads(pb);g=module(a.repo/CHECK,'paid_review_geometry');h=module(a.repo/HELPER,'paid_review_intervals')
    C,pv,pp,ps=replay_general(p,R,g);_,v0,p0,s0=paid_replay(p,R,g)
    assert(v0,p0)==(pv,pp)and s0['counts']==ps['counts']and s0['movement_profile']==ps['movement_profile']and not s0['owned_upward_moves']
    C,V,P,stats=paid_replay(w,R,g);owner='HALF_SERVICE_EXPORT_2';T=pp['Y20'];H=pp['Y96'];J='UPWARD_HALF_REBASE_J'
    assert C[J]==g.basis(C[T]+C[H])and len(C[J])==6 and g.sub(C[J],C['F20'])and g.sub(C[J],C['F96'])
    assert g.sub(C[pp[owner]],C[H])and len(C[H])-len(C[pp[owner]])==2
    literal=p['operations'][:1921]+[['ADD','Y20','Y96'],['ADD','Y96','Y20']]+p['operations'][1921:2089]
    literal += [['MOVE',owner,H],['ADD',owner,'Y96'],['MOVE','Y20',J],['MOVE','Y96',J],['ADD','Y96','Y20'],['ADD','Y20','Y96']]
    assert len(literal)==2097;literal+=p['operations'][2089:];assert literal==w['operations']
    d20=int(p['Y_correction_rows_hex'][20],16)&~255;d96=(int(p['Y_correction_rows_hex'][96],16)&~255)^pv[owner]
    assert d20.bit_count()==d96.bit_count()==3
    ev=pv.copy();ep=pp.copy();ev['Y20']^=d96;ev['Y96']^=pv[owner]^d96^d20
    ep['Y20']=ep['Y96']=J;ep[owner]=H;assert(V,P)==(ev,ep)and len(V)==420
    assert len(stats['owned_upward_moves'])==1 and stats['owned_upward_moves'][0]['gap']==2
    assert stats['owned_downward_profile']=={1:40}and stats['movement_profile']=={1:200,2:123,3:22,4:103,7:96}
    assert stats['counts']=={'INIT':198,'ADD':1466,'MOVE':544,'CLEAR':198}
    inv=json.loads((a.inputs/'CUT-INVENTORY.json').read_text())
    assert {z['name']:(z['row_hex'],z['chart'],z['rank'])for z in inv['fields']}=={n:(hex(v),P[n],len(C[P[n]]))for n,v in V.items()}
    author=json.loads((a.inputs/'RESULT.json').read_text());Q=h.moment(stats['movement_profile']);claim=tuple(map(Fraction,author['moment']['rational']))
    assert claim[0]<=Q[0]<=Q[1]<=claim[1]
    controls=[]
    for key in ['earlier_inverse','paid_owned_upward_rebase','remove_actual_half_at_courier','cross_parity_forward','native_courier_cleanup']:
        b=json.loads(wb);ix=w['semantic_operation_indices'][key][0];del b['operations'][ix];b['carrier_interface_before_operation']-=1
        try:_,bv,bp,_=paid_replay(b,R,g);assert(bv,bp)==(V,P)
        except AssertionError:controls.append('omit_'+key)
        else:raise AssertionError(key)
    try:replay_general(w,R,g)
    except AssertionError:controls.append('strict_downward_owner_guard_rejects_turn')
    else:raise AssertionError('no actual upward turn')
    result={'status':'PASS_INDEPENDENT_PAID_OWNED_ASCENT','word_sha256':WORD,'parent_word_sha256':PARENT,
      'all_original_columns':222,'exact_cut_fields':420,'literal_whole_word_match':True,'parent_interpreter_agreement':True,
      'all_X_restored_and_arbitrary_Y_identity':True,'completed_diagonal_outputs':8,'total_foreign_terms':484,
      'stats':stats,'independent_moment':h.record(Q),'independent_added_cost':h.record(h.moment({1:2,2:2,4:-1})),
      'negative_controls':controls,'scope':'Explicit retained paid nested-owned contract only; public paths remain upward. No source-model edit, no extra descent, no cost dominance or new output claim.'}
    h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
