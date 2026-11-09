"""Independent observer of the K8 original-coordinate physical Core receipt.

Regenerate the immutable Reference, derive labels from original address bits,
interpret every dense event and sparse block using separately authored review
interpreters, then check a closed-form inverse in original order. Observations
never supply physical payloads; this is not a second physical execution.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from argparse import ArgumentParser
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


def need(ok, why):
    if not ok:
        raise ValueError(why)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def original_of_packed(j):
    # Original low bits: spectator, axis-low, axis-high-0, axis-high-1.
    # Packed low bits: axis-low, spectator, axis-high-0, axis-high-1.
    return ((j & 1) << 1) | ((j >> 1) & 1) | (j & 12)


def direct_target(original, matrices):
    """Closed-form inverse; no Layout or producer factor/helper calls."""
    answer = [None] * 16
    for block in range(4):
        for spectator in range(2):
            i, j = 4 * block + spectator, 4 * block + 2 + spectator
            a, b = matrices[2 * block + spectator][0]
            c, d = matrices[2 * block + spectator][1]
            det = a * d - b * c
            need(det != 0, 'invertible original complete 2x2 source')
            answer[i] = tuple((d*x-b*y)/det for x,y in zip(original[i],original[j]))
            answer[j] = tuple((-c*x+a*y)/det for x,y in zip(original[i],original[j]))
    return tuple(answer)


def rejected(call, label):
    try:
        call()
    except ValueError:
        return label
    raise ValueError('negative control accepted: ' + label)


def main():
    ap = ArgumentParser()
    ap.add_argument('--source-package', type=Path, required=True)
    ap.add_argument('--receipt', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    package = args.source_package.resolve()
    sys.path.insert(0, str(package))
    from independent_numerics import (bandwidth, budget, canonical_json, ceil_log2,
        decode_pairs, five_factors, fraction_digest, identity, pow2, row_norm,
        squared_error, squared_norm)
    from stage_observer import KINDS, check_stages
    from check_source_join import dense_replay
    from staged_oracle import first_inverse, supplied_action

    path = args.receipt or package/'ORIGINAL-PHYSICAL-RESULT.json'
    raw = path.read_bytes()
    result = json.loads(raw)
    need(result['status'] == 'PASS_ORIGINAL_COORDINATE_PHYSICAL_NARROW_CORE',
         'completed original-coordinate physical receipt')
    plan, source = result['allocation'], result['source']
    need((plan['labels'],plan['g'],plan['side'],plan['n']) == (8,1,2,4),
         'exact K8/g1/L2/n4 scope')
    need(source['parameters'] == [7,1,2,1,3,64] and source['interior'] == [1],
         'fixed actual Reference and scalar interior')
    origins = tuple(2*(c//2) for c in range(8))
    def check_origins(values):
        need(tuple(values) == origins, 'independent original-coordinate coarse labels')
    check_origins(source['origins'])
    initial = tuple(tuple(z) for z in result['initial'])
    returned = tuple(tuple(z) for z in result['returned'])
    need(len(initial) == len(returned) == 16, 'complete original field')
    packed_initial = tuple(initial[original_of_packed(j)] for j in range(16))
    def check_initial(values):
        need(tuple(tuple(z) for z in values) == packed_initial, 'independent first route')
    check_initial(result['packed_initial'])
    need(packed_initial != initial, 'fixture first route is nonidentity')
    join = load('_root_original_join', package/'join_sources.py')
    with join.numerical() as runtime:
        reference = runtime.reference.Reference(runtime.raw, *source['parameters'])
        need(reference.description_hash == source['reference_sha256'], 'same immutable Reference')
        matrices = tuple(tuple(tuple(reference.entry('narrow',o+i,o+j).value
                    for j in range(2)) for i in range(2)) for o in origins)
        reported = tuple(tuple(tuple(Q(x) for x in row) for row in c[0]) for c in source['Q'])
        need(matrices == reported, 'all original Q matrices independently regenerated')
        nonidentity_contexts = sum(q != identity(2) for q in matrices)
        need(nonidentity_contexts == 6, 'six coupled and two identity source contexts')
        factors = tuple(five_factors(q,(1,)) for q in matrices)
        need(all(f['A'] == ((Q(1),),) for f in factors), 'identity scalar interior limitation')
        norm = max(max(row_norm(m),row_norm(tuple(zip(*m)))) for f in factors for m in f['factors'])
        need(norm <= plan['h'], 'all source row/column norms')
        checked_plan = budget(4,1,plan['h'],plan['target'],plan['P'],plan['R0'].bit_length()-1)
        for key in ('H','R0','R2','Rstar','stage_target','local_target','V2'):
            need(checked_plan[key] == plan[key], 'independent full-volume allocation: '+key)
        P,width,rb = plan['P'],plan['width'],plan['radius_bits']
        need(plan['V2'] == 4 and width >= P+rb+2, 'global-volume factor and common carrier')
        need(squared_norm(decode_pairs(initial,P)) <= plan['R0']**2, 'initial whole-field radius')
        adapter = load('_root_original_admission',package/'admitted_context.py')
        family = tuple((adapter.AdmittedPartition(runtime,reference,'narrow',o,2,1,((1,),)),)
                       for o in origins)
        programs = tuple(adapter.prepare(runtime,family,d,target=plan['stage_target'],
            radius_bits=rb,incoming=P,fractional_bits=P) for d in (True,False))
        need(len(result['dense_programs']) == 2, 'two stored global source directions')
        for p,stored in zip(programs,result['dense_programs']):
            need(canonical_json(p.record()) == canonical_json(stored), 'regenerated complete dense certificate')
            need(p.records == 16 and p.axes == 1 and p.labels == 8, 'whole eight-context dense field')
            need(p.total_error < pow2(-plan['stage_target']), 'dense error certificate')
        ws = load('_root_original_window',join.INVERSE/'source_window.py')
        windows,uppers,errors,blocks = [],[],[],[]
        for o,q,f in zip(origins,matrices,factors):
            band = max(1,bandwidth(q))
            sufficient = ws.sufficient_allocation(reference,band=band,radius=plan['Rstar'],
                target=plan['local_target'],incoming=P,largest_descriptor=reference.target_size)
            w = ws.make_window(reference,origin=o,length=2,interior_blocks=((1,),),band=band,cap=1,
                block=sufficient['block'],precision=P,width=width,radius=plan['Rstar'],target=plan['local_target'])
            upper = tuple(tuple(f['factors'][3][i][j] for j in w.E) for i in w.E)
            error = Q(max(sum(bool(x) for x in row) for row in upper)*plan['Rstar']+6,1<<P)
            need(error <= pow2(-plan['local_target']), 'all-context forward error')
            need(max(Q(1),row_norm(upper))*plan['Rstar'] < 1<<(width-P-1), 'forward carrier')
            lift = max(abs(2*i-(2*j+1)) for i,row in enumerate(upper) for j,x in enumerate(row) if x)
            windows.append(w); uppers.append(upper); errors.append(error)
            blocks.append(1<<ceil_log2(max(2,lift)))
        allowances = (programs[0].total_error,4*max(w.total_error for w in windows),
            programs[1].total_error,4*max(errors),programs[0].total_error)
        names = ('D_Ainv_1','T1','D_A','T2','D_Ainv_2')
        observations = [dict(kind=kind,input=result['observations'][name]['input'],
            output=result['observations'][name]['output'],input_precision=P,output_precision=P,
            input_width=width,output_width=width,input_radius=plan['R2'])
            for kind,name in zip(KINDS,names)]
        contexts,interiors = tuple((q,) for q in matrices),(((1,),),)*8
        checked = check_stages(contexts,interiors,packed_initial,P,observations,
                               allowances,plan['target'],common_precision=P)
        dense_counts,sparse_calls = [],[]
        for stage,observed in enumerate(observations):
            before,after = (tuple(tuple(z) for z in observed[k]) for k in ('input','output'))
            if stage in (0,2,4):
                expected,counts = dense_replay(runtime,programs[int(stage==2)],before)
                dense_counts.append(counts)
            else:
                actual = list(decode_pairs(before,P))
                for c,(w,u,b) in enumerate(zip(windows,uppers,blocks)):
                    ids = tuple(2*c+j for j in w.E)
                    rows = tuple(actual[i] for i in ids)
                    need(max(sum(map(abs,z),Q()) for z in rows) <= plan['Rstar'], 'actual sparse radius')
                    out = first_inverse(w,rows) if stage==1 else supplied_action(u,rows,b,P)
                    for i,z in zip(ids,out):actual[i]=z
                expected = tuple(tuple(int(x*(1<<P)) for x in z) for z in actual)
                need(decode_pairs(expected,P) == tuple(actual), 'staged output remains common-grid')
                sparse_calls.append(len(windows))
            need(expected == after, 'bitwise independent staged words: '+names[stage])
        packed_returned = tuple(tuple(z) for z in observations[-1]['output'])
        need(tuple(tuple(z) for z in result['packed_returned']) == packed_returned, 'literal last-stage result')
        def check_return(values):
            need(tuple(tuple(z) for z in values) == tuple(packed_returned[original_of_packed(i)]
                 for i in range(16)), 'independent original-coordinate inverse route')
        check_return(returned)
        target = direct_target(decode_pairs(initial,P),matrices)
        error = squared_error(decode_pairs(returned,P),target)
        need(error <= pow2(-2*plan['target']), 'closed-form original inverse meets requested target')
        need(result['complete_dense_calls']==3 and result['complete_dense_events']==
             2*programs[0].stages+programs[1].stages, 'all three complete global event streams')
        need(result['online_new_tapes']==0 and result['fixed_private_inventory']>0,
             'fixture reports no online role allocation')
        seam=deepcopy(observations); seam[1]['input'][0][0]+=1
        wrong_origins=list(origins); wrong_origins[3]+=2
        wrong_return=[list(z) for z in returned]; wrong_return[0][0]+=1
        controls=[rejected(lambda:check_initial(initial),'omitted first route'),
            rejected(lambda:check_return(packed_returned),'omitted inverse route'),
            rejected(lambda:check_origins(wrong_origins),'wrong source origin'),
            rejected(lambda:check_stages(contexts,interiors,packed_initial,P,seam,
                allowances,plan['target'],common_precision=P),'one-ulp sparse seam corruption'),
            rejected(lambda:check_return(wrong_return),'one-ulp protected-output corruption')]
        checked.update(status='PASS_INDEPENDENT_ORIGINAL_CORE_NUMERICS',
            physical_receipt_sha256=sha256(raw).hexdigest(),reviewer_replayed_physical_execution=False,
            reviewed_observed_physical_execution=True,regenerated_reference=True,
            regenerated_dense_certificates=True,bitwise_staged_agreement=True,
            original_address_oracle=True,closed_form_original_inverse=True,
            original_error_squared=fraction_digest(error),independently_interpreted_dense=dense_counts,
            sparse_context_interpretations=sparse_calls,identity_scalar_interior_limitation=True,
            nonidentity_complete_contexts=nonidentity_contexts,
            identity_complete_contexts=len(matrices)-nonidentity_contexts,
            source_origins=origins,negative_controls=controls,
            reviewed_source_sha256={n:sha256((package/n).read_bytes()).hexdigest() for n in
                ('physical_join.py','original_layout.py','verify_original.py',
                 'check_source_join.py','staged_oracle.py')})
        output=canonical_json(checked)+'\n'
        if args.output:args.output.write_text(output)
        print(output,end='')


if __name__=='__main__':main()
