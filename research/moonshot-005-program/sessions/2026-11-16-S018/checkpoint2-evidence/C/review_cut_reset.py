#!/usr/bin/env python3
"""Independent proof-control replay for root's known-source cut reset."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from ground_output_normalization import evaluate
from release_projection import N, binary_basis, chart, replay, require
from price_projection import moment, record


def main():
    ap = argparse.ArgumentParser()
    for n in ['repo','work','out']:
        ap.add_argument('--'+n, type=Path, required=True)
    ap.add_argument('--feedback',action='store_true')
    a = ap.parse_args()
    pins = {
        'A/pruned78/WORD.json': 'c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245',
        'R/cut-reset/control/OLD-WORD.json': 'ffb84c8b14f460818b34dbcfec5e099a6d712ce5d46dd9218b9553bd2b9aad61',
        'R/cut-reset/control/RESET-WORD.json': '7c70a61320a81bed31f70378be8be0668244024058bbbc418f3b575873ec6bcf',
    }
    if a.feedback:
        pins = {
            'A/pruned78/WORD.json': 'c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245',
            'R/cut-reset/control-feedback/OLD-WORD.json': '4baab219091309a0191cb351ba091b5f32f6912b408be78e0d01b4ab887dc396',
            'R/cut-reset/control-feedback/RESET-WORD.json': '1f0bd254b3e9316f02b31701f593ed361bae99eadc8b02283666d79e22bc7ab8',
        }
    ws = []
    for path, pin in pins.items():
        b = (a.work/path).read_bytes()
        require(hashlib.sha256(b).hexdigest() == pin, ('word pin',path))
        ws.append(json.loads(b))
    base, old, new = ws
    source = (a.repo/base['source_path']).read_bytes()
    require(hashlib.sha256(source).hexdigest() == base['source_sha256'], 'native source pin')
    roots = json.loads(source)['native_roots']
    for i, root in enumerate(roots):
        require(chart(base['charts'][f'L{i}']) == chart({'kind':'span','rows':[root]}), ('native L',i))
        require(chart(base['charts'][f'F{i}']) == chart({'kind':'ann','rows':[root]}), ('native F',i))
    require(old['charts'] == new['charts'] == base['charts'], 'same actual chart dictionary')
    base_stats, bs, _ = replay(base, collect=True)
    old_stats, os, _ = replay(old, collect=True)
    new_stats, ns, _ = replay(new, collect=True)
    cut = base['carrier_interface_before_operation']
    oc = old['operations'].index(['MOVE','X5','M1'])
    nc = new['operations'].index(['MOVE','X5','M1'])
    bv, ba = bs[cut]; ov, oa = os[oc]; nv, na = ns[nc]
    originals = {f'{b}{i}' for b in ['X','Y'] for i in range(N)}
    owners = sorted(set(bv)-originals)
    old_prefix = copy.deepcopy(base['operations'][:cut])
    old_prefix.remove(['MOVE','Y13','F13'])
    require(old['operations'][:oc] == old_prefix, 'exact old source prefix with held Y13')
    require(ov == bv and all(oa[n] == ('zero' if n=='Y13' else ba[n]) for n in ov), 'exact actual old cut')
    require(new['operations'][nc:-2] == old['operations'][oc:], 'literal unchanged continuation')
    inverse = [['ADD','X29','X5'],['ADD','X42','X5']]
    require(new['operations'][-2:] == inverse, 'actual Hub inverse word')
    S = set(base['targets']) | {61,67}; smask = sum(1 << i for i in S)
    require(len(S) == 48 and len(owners) == 94, 'source size')
    actual_support = 0
    for n in owners:
        actual_support |= ov[n]
        require(ov[n] & ~smask == 0 and nv[n] == 0 and na[n] == oa[n], ('zeroed actual known owner',n))
    for i in range(N):
        x, y = f'X{i}', f'Y{i}'
        require(ov[x] == nv[x] == 1 << i and oa[x] == na[x], ('raw X cut',i))
        offset = ov[y] ^ (1 << (N+i)); actual_support |= offset
        require(offset & ~smask == 0, ('known Y offset',i))
        require(na[y] == oa[y] and (nv[y] >> N) == 1 << i, ('actual Y homogeneous cut',i))
    require(actual_support == smask, 'exact source support S48')
    before_inverse = copy.deepcopy(new); before_inverse['operations'] = before_inverse['operations'][:-2]
    final, fa, _, _ = evaluate(before_inverse)
    M = [final[f'X{i}'] for i in range(N)]
    require(M == [(1 << i) ^ (((1 << 29) ^ (1 << 42)) if i==5 else 0) for i in range(N)], 'reset original matrix')
    require(len(binary_basis(M)) == N and all(r >> N == 0 for r in M), 'invertible y-free original map')
    require(all(fa[f'X{i}']=='Hub' for i in range(N)), 'all actual inverse operands at Hub')
    require(all(final[f'Y{i}'] == (1 << (N+i)) ^ ((1 << i) if i in new['targets'] else 0)
                for i in range(N)), 'Y endpoints already correct before X inverse')
    no_preloads = copy.deepcopy(before_inverse)
    preloads = [o for o in new['operations'][:nc] if o[0]=='ADD' and o[1].startswith('RESET_RAW') and o[2].startswith('Y')]
    no_preloads['operations'] = [o for o in no_preloads['operations'] if o not in preloads]
    zfinal, _, _, _ = evaluate(no_preloads)
    deltas = {}
    for i in range(N):
        desired = (1 << (N+i)) ^ ((1 << i) if i in new['targets'] else 0)
        d = zfinal[f'Y{i}'] ^ desired
        require(d & ~smask == 0, ('reset discrepancy known',i))
        require(d == (nv[f'Y{i}'] ^ (1 << (N+i))), ('actual ground preload equals discrepancy',i))
        if d:
            deltas[i] = hex(d)
    require(deltas[13] == hex(1 << 7), 'nontrivial additional Y13 preload')
    controls = []

    def reject(label, word):
        try:
            replay(word)
        except (ValueError,KeyError) as e:
            controls.append({'control':label,'rejected':True,'reason':str(e)})
        else:
            raise ValueError(('accepted reset control',label))

    for label, op in [
        ('omit known Y13 preload',['ADD','RESET_RAW7','Y13']),
        ('omit actual native capture',['ADD','X7','RESET_RAW7']),
        ('omit actual ground arrival',['MOVE','RESET_RAW7','zero']),
        ('omit raw owner retirement',['CLEAR','RESET_RAW61'])]:
        bad = copy.deepcopy(new); bad['operations'].remove(op); reject(label,bad)
    bad = copy.deepcopy(new); bad['operations'].pop(); reject('omit final Hub inverse ADD',bad)
    feedback_rows = None
    if a.feedback:
        fi = new['operations'].index(['ADD','Y13','X0'])
        feedback_rows = [ns[fi+j][0]['X0'] for j in range(6)]
        require(ns[fi+1][0]['X0'] == (1 << (N+13)) ^ (1 << 7), 'actual arbitrary-y swap into X0')
        move_back = next(j for j in range(fi,len(new['operations'])) if new['operations'][j] == ['MOVE','X0','Hub'])
        require(ns[move_back][0]['X0'] == 1, 'actual swap restoration before Hub ascent')
        require(ns[move_back][0]['Y13'] == (1 << (N+13)) ^ (1 << 13), 'packet correction actually applied through X0')
        bad = copy.deepcopy(new); bad['operations'].pop(fi); reject('omit actual Y-to-X swap operation',bad)
    # Independently constructed native singular fixture; no root code imported.
    sp = [['MOVE',f'X{i}','Hub'] for i in range(N)] + [['MOVE',f'Y{i}',f'F{i}'] for i in range(N)]
    sp += [['INIT','REVIEW_B','Hub'],['ADD','X0','REVIEW_B']]
    sf = [['INIT','REVIEW_C','Hub'],['ADD','X0','REVIEW_C'],['ADD','REVIEW_C','X0'],
          ['ADD','REVIEW_B','X0'],['CLEAR','REVIEW_C'],['CLEAR','REVIEW_B']]
    sing = {k:copy.deepcopy(base[k]) for k in ['source_path','source_sha256','charts']}
    sing.update(targets=[],operations=sp+sf)
    replay(sing)
    sing['operations'] = sp[:-1]+sf
    sv, _, _, _ = evaluate(sing)
    sm = [sv[f'X{i}'] for i in range(N)]
    require(sm == [0]+[1 << i for i in range(1,N)] and len(binary_basis(sm)) == N-1, 'actual singular map and kernel')
    reject('singular reset loses x0 despite old correct endpoint',sing)
    expected_counts = {'INIT':143,'ADD':110 if a.feedback else 104,'MOVE':273 if a.feedback else 272,'CLEAR':143}
    expected_profile = {1:50,3:1,4:1,6:1,7:220} if a.feedback else {1:49,3:1,4:1,7:221}
    require(new_stats['counts'] == expected_counts, 'complete reset counts')
    require(new_stats['movement_profile'] == expected_profile, 'complete reset movement profile')
    require(new_stats['dirty_CLEAR'] == 49 and new_stats['peak_owned'] == 95, 'reset ownership ledger')
    gate = {127:37,64:74,1:-74}
    for j in range(1,9):
        gate[1+7*j] = gate.get(1+7*j,0)+74
        gate[7*j] = gate.get(7*j,0)-74
    gl, gh = moment(gate); limit = (gl/6,gh/6)
    nl, nh = moment(new_stats['movement_profile'])
    old_price = moment(old_stats['movement_profile'])
    baseline = moment({1:48,7:222})
    proof = (a.work/'R/cut-reset/PROOF.md').read_bytes()
    proof_pin = hashlib.sha256(proof).hexdigest()
    require(proof_pin == 'ed754aec0a04d4e9d4bf44f80bb09145d365f8365649db5d2c975c9447505d28', 'final reviewed proof pin')
    require(b'actual retained pure-X side records' in proof and b'full-column observation criterion' in proof,
            'reviewed side-data nuisance qualification')
    result = {'status':'PASS_INDEPENDENT_KNOWN_SOURCE_CUT_RESET_REVIEW',
        'actual_Y_to_X_feedback_variant':a.feedback,
        'intermediate_X0_feedback_rows_hex':None if feedback_rows is None else [hex(r) for r in feedback_rows],
        'reviewed_proof_sha256':proof_pin,
        'previous_reviewed_proof_sha256':'42b82eed13017355e34d4797a1ae40d6480f9cd321607eb376c3adba44e9d0f1',
        'side_information_qualification_confirmed':True,
        'source_pins':pins,'native_source_sha256':base['source_sha256'],
        'old_actual_cut':oc,'reset_actual_cut':nc,'base_cut':cut,
        'known_coordinates':sorted(S),'live_cut_owners':len(owners),
        'owned_row_rank':len(binary_basis(ov[n] for n in owners)),
        'raw_native_X_at_cut':sum(oa[f'X{i}']==f'L{i}' for i in range(N)),
        'raw_Hub_X_at_cut':sum(oa[f'X{i}']=='Hub' for i in range(N)),
        'source_report':base_stats,'old_report':old_stats,'reset_report':new_stats,
        'known_preloads':deltas,'nonidentity_original_row5_hex':hex(M[5]),
        'actual_Hub_inverse':inverse,'homogeneous_XY_zero':True,'homogeneous_YY_identity':True,
        'old_moment':record(old_price),'reset_moment':record((nl,nh)),
        'reset_limiting_room':record((limit[0]-nh,limit[1]-nl)),
        'direct48_baseline':record(baseline),
        'direct48_limiting_room':record((limit[0]-baseline[1],limit[1]-baseline[0])),
        'physical_singular_map_rank':len(binary_basis(sm)),'singular_kernel_hex':'0x1',
        'controls':controls,
        'scope':('Independent exact native/all222 replay, source48 audit, literal continuation identity, actual nontrivial Hub inverse and singular-M control. No root/A execution code imported. '+
            ('This variant exercises actual arbitrary-Y content in X0 and applies a new packet through that mixed original before restoring it. ' if a.feedback else 'This original control has no Y-source operations. ')+
            'No all111 supplier or kappa.')}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['status','reset_report','reset_moment','reset_limiting_room','reviewed_proof_sha256']},indent=2))


if __name__ == '__main__':
    main()
