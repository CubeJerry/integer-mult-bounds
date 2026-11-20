#!/usr/bin/env python3
"""Independent geometric component, complete source, H owner word and invoice."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import numpy as np

def local(name):
    spec=importlib.util.spec_from_file_location('geometric_H_independent_'+name,Path(__file__).with_name(name+'.py'))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

source=local('construct');need=source.need

def mathematical_checks(ctx):
    F=ctx.field; cuts=Counter(); native=Counter(); fibres=Counter(); details={}; nonrs={}
    need(10 not in ctx.H[263] and not ctx.H[263]<=ctx.perp[80], 'local interfaces avoid both S028 target perturbations')
    need(ctx.xcount[263]==90 and all(len(ctx.wires[j,263,'X'])==240 and not ctx.wires[j,263,'Y'] for j in ctx.donors), 'actual fully early H inventory')
    for (j,k), rows in sorted(ctx.maps.items()):
        need(set(rows)==set(ctx.stars[j]), 'one complete 28-plane literal source')
        for i in sorted(ctx.perp[j]):
            S=np.vstack([rows[h] for h in ctx.views[j,i]])
            need(S.shape==(16*k,16*k) and F.rank(S)==16*k, 'complete geometric source cut')
            cuts[k]+=1; native[k]+=(i<111)
    need(cuts=={3:189,12:189} and native=={3:174,12:174}, 'all claimed source cuts')
    for k in (3,12):
        chart=ctx.charts[263,k]; word=ctx.components[k]['word']; digest=sha256()
        for i in chart.receivers:
            visible=[p for p,d in enumerate(chart.ports) if ctx.D[d]<=ctx.perp[i]]
            need(len(visible)==k, 'exact geometric component output count')
            first=ctx.donors[0]; off=[h for h in ctx.views[first,i] if h!=263]
            annihilator=np.vstack([ctx.maps[first,k][h] for h in off])
            need(F.rank(annihilator)==15*k, 'whole off-centre fibre dimension')
            readout=F.mm(word[np.ix_(visible,range(k))],ctx.maps[first,k][263])
            S=np.vstack([readout,annihilator]); rhs=np.zeros((16*k,k),dtype=np.uint8);rhs[:k]=np.eye(k,dtype=np.uint8)
            lift=F.solve(S,rhs); digest.update(lift.tobytes())
            for ordinal,j in enumerate(ctx.donors):
                off=[h for h in ctx.views[j,i] if h!=263]
                need(not np.any(F.mm(np.vstack([ctx.maps[j,k][h] for h in off]),lift)), 'all actual donor side information vanishes on one common lift')
                minor=word[np.ix_(visible,range(ordinal*k,(ordinal+1)*k))]
                need(F.rank(minor)==k, 'native donor readout matrix invertible')
                need(np.array_equal(F.mm(F.mm(minor,ctx.maps[j,k][263]),lift),np.eye(k,dtype=np.uint8)), 'one common canonical source-to-output inverse at every donor')
            fibres[k]+=1
        details[str(k)]={'canonical_lift_sha256':digest.hexdigest(),'geometric_common_fibres':fibres[k],
                         'native_common_fibres':sum(i<111 for i in chart.receivers),'source_geometry_cuts':cuts[k],'source_native_cuts':native[k]}
    need(fibres=={3:36,12:36} and all(v['native_common_fibres']==33 for v in details.values()), 'all actual common H fibres')
    witnesses=json.loads(ctx.payload['non_RS'])
    need(set(map(int,witnesses))==set(ctx.donors), 'information witness for every changed source')
    for key,item in witnesses.items():
        j=int(key); hs=item['planes'];need(len(hs)==len(set(hs))==16 and set(hs)<=set(ctx.stars[j]), 'literal16 source planes')
        ranks={str(k):F.rank(np.vstack([ctx.maps[j,k][h] for h in hs])) for k in (3,12)}
        need(ranks['3']==47 and 16*sum(ranks.values())<3840, 'genuine complete information change')
        nonrs[key]={'component_ranks':ranks,'whole_bank_rank':16*sum(ranks.values())}
    need({j:v['whole_bank_rank'] for j,v in nonrs.items()}=={'0':3792,'61':3760,'62':3808}, 'three full-bank information invariants')
    # Negative controls are independently applied to actual source matrices.
    i=min(ctx.perp[0]&set(range(111))); broken=np.vstack([ctx.maps[0,3][h] for h in ctx.views[0,i]]);broken[:3]=0
    need(F.rank(broken)==45, 'one deleted ordinary quotient loses three ranks')
    c=ctx.charts[263,3]; d=ctx.components[3]; wrong=ctx.maps[61,3][263].copy();wrong[0,0]^=1
    rejected=0
    for i,K in d['fibres'].items():
        vis=[p for p,h in enumerate(c.ports) if ctx.D[h]<=ctx.perp[i]]
        good=F.mm(F.mm(d['word'][np.ix_(vis,range(3,6))],ctx.maps[61,3][263]),K)
        bad=F.mm(F.mm(d['word'][np.ix_(vis,range(3,6))],wrong),K)
        rejected+=not np.array_equal(good,bad)
    need(rejected==36 and F.null(np.zeros((6,9),dtype=np.uint8)).shape==(9,9), 'central-control and equal-weight negative controls')
    return {'components':details,'non_RS_witnesses':nonrs,'negative_controls':{'deleted_quotient_rank':45,'changed_control_rejections':rejected,'equal_weight_annihilator_dimension':9}}

def physical_H(ctx):
    F=ctx.field; exits=defaultdict(list)
    for line in ctx.payload['routes'].splitlines():
        phase,j,c,h,d,*_=json.loads(line)
        if h!=263:continue
        need(phase=='X', 'all H inputs are actual original early fields')
        exits[d].extend((j*480+c)*8+lane for lane in range(8))
    for holders in exits.values():holders.sort()
    all_holders=sorted(x for v in exits.values() for x in v)
    need(len(exits)==45 and {len(v) for v in exits.values()}=={16} and len(set(all_holders))==len(all_holders)==720, 'every original H owner appears once on one output port')
    need(set(all_holders)=={x for j in ctx.donors for x in ctx.wires[j,263,'X']}, 'source and H owner inventories coincide')
    index={v:i for i,v in enumerate(all_holders)}; matrix=np.zeros((720,720),dtype=np.uint8)
    groups={}; used_inputs=set();used_outputs=set()
    for k in (3,12):
        chart=ctx.charts[263,k]; word=ctx.components[k]['word']; prefix=0 if k==3 else 3
        for half in range(2):
            for lane in range(8):
                inputs=[ctx.wires[j,263,'X'][16*(prefix+t)+8*half+lane] for j in ctx.donors for t in range(k)]
                outputs=[exits[d][8*half+lane] for d in chart.ports]
                need(not used_inputs.intersection(inputs) and not used_outputs.intersection(outputs), 'disjoint literal component placements')
                used_inputs.update(inputs);used_outputs.update(outputs)
                for r,x in enumerate(outputs):
                    for c,y in enumerate(inputs):matrix[index[x],index[y]]=word[r,c]
                groups[f'{k}/{half}/{lane}']={'input_holders':inputs,'output_holders':outputs}
    need(used_inputs==used_outputs==set(all_holders), 'all720 physical inputs and outputs covered with no permutation omitted')
    ranks=[]
    for i in ctx.charts[263,3].receivers:
        visible=[index[x] for d in sorted(exits) if ctx.D[d]<=ctx.perp[i] for x in exits[d]]
        need(len(visible)==240, 'actual visible field capacity')
        for j in ctx.donors:
            columns=[index[x] for x in ctx.wires[j,263,'X']]
            ranks.append(F.rank(matrix[np.ix_(visible,columns)]))
    need(len(ranks)==108 and set(ranks)=={240}, 'all108 physical240-by240 donor minors')
    stream,price=F.compile(matrix)
    records={'H':263,'holders_in_matrix_order':all_holders,'component_placements':groups,
             'exit_holders':{str(d):v for d,v in sorted(exits.items())},'reduce_file':'H263-REDUCE.bin.gz','all_inputs_are_original_X':True}
    body=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
    hashes={'matrix':sha256(matrix.tobytes()).hexdigest(),'word':sha256(stream).hexdigest(),'holders':sha256(body).hexdigest()}
    expected=json.loads(ctx.payload['cost'])
    need(hashes==expected['H263_hashes'] and price==369008, 'literal H matrix, reduction word, holder dictionary, and price')
    binary=local('binary_word').verify(matrix,stream,F,price)
    bill={'H_forward_ADD':price,'H_inverse_ADD':price,'H_forward_and_inverse_ADD':2*price,
          'H_INIT':0,'H_dirty_CLEAR':0,'H_extra_MOVE':0,'physical_matrix_shape':[720,720],
          'physical_receiver_donor_minors':len(ranks),'minimum_physical_donor_minor_rank':min(ranks)}
    need(bill==expected['H263'], 'complete local H invoice')
    return {'bill':bill,'hashes':hashes,'binary_replay':binary}

def main():
    cli=ArgumentParser(description=__doc__);cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();ctx=source.context(args.repo,args.out)
    print('PASS_INDEPENDENT_COMPONENT_AND_FULL_SOURCE_COEFFICIENTS',flush=True)
    math=mathematical_checks(ctx);print('PASS_ALL_SOURCE_CUTS_COMMON_FIBRES_AND_INFORMATION_WITNESSES',flush=True)
    invoice=local('source_invoice');special,donors,hashes=invoice.source_word(ctx)
    print('PASS_SIX_EARLY_WORDS_AND_THREE_ORIGINAL_HOLDER_DICTIONARIES',flush=True)
    background,old_donors=invoice.background_invoice(ctx)
    print('PASS_ALL111_BACKGROUND_DESCRIPTORS_AND_EXACT108_RETAINED_BILLS',flush=True)
    H=physical_H(ctx);print('PASS_PHYSICAL_H_OWNERS_MINORS_AND_COMPLETE_BINARY_WORD',flush=True)
    old_inverse=background['early_basis_ADD']+background['source_owner_permutation_ADD'];cache=background['snapshot_copy_ADD_INIT_dirty_CLEAR']
    old_forward=old_inverse+cache+background['late_evaluation_ADD']
    all_sources={'donors':111,'source_forward_ADD':old_forward+special['forward_ADD'],
        'source_pure_inverse_ADD':old_inverse+special['inverse_ADD'],'source_forward_and_inverse_ADD':old_forward+old_inverse+special['total_ADD'],
        'source_INIT':cache+special['INIT'],'source_dirty_CLEAR':cache+special['dirty_CLEAR'],'source_extra_MOVE':0}
    combined={**all_sources,'source_and_H_forward_ADD':all_sources['source_forward_ADD']+H['bill']['H_forward_ADD'],
        'source_and_H_inverse_ADD':all_sources['source_pure_inverse_ADD']+H['bill']['H_inverse_ADD'],
        'source_and_H_forward_and_inverse_ADD':all_sources['source_forward_and_inverse_ADD']+H['bill']['H_forward_and_inverse_ADD']}
    expected=json.loads(ctx.payload['cost'])
    need(all_sources==expected['all111_source'] and combined==expected['combined'], 'complete independent source-plus-H invoice')
    result={'status':'PASS_INDEPENDENT_GEOMETRIC_SOURCE_AND_H_REVIEW','H':263,'donors':ctx.donors,
            'mathematics':math,'special':special,'special_donor_costs':donors,'source_word_hashes':hashes,
            'background':background,'background_donor_count':108,'H263':H,'all111_source':all_sources,'combined':combined,
            'source_pins_sha256':sha256(Path(__file__).with_name('SOURCE-PINS.json').read_bytes()).hexdigest(),
            'common_D_K_endpoint':False,'actual_global_return_rank':None,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    (args.out/'BACKGROUND-PER-DONOR.json').write_text(json.dumps(old_donors,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'source_and_H_ADD':combined['source_and_H_forward_and_inverse_ADD']},sort_keys=True),flush=True)

if __name__=='__main__':main()
