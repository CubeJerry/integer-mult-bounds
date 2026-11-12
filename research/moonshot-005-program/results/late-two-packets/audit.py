#!/usr/bin/env python3
"""Author provenance and decisive source-mutation checks; not independent review."""
import argparse,copy,gzip,hashlib,json,sys
from collections import defaultdict
from pathlib import Path

def need(q,m):
    if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main(a):
    reconstruction=a.repo/'research/moonshot-005-program/results/cohort-reconstruction';sys.path.insert(0,str(reconstruction))
    import build as replay
    from common import load_inputs,F
    s,_,_=load_inputs(a.repo);pb=(a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz').read_bytes();need(sha(gzip.decompress(pb))=='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a','parent payload pin')
    p=json.loads(gzip.decompress(pb));wb=a.word.read_bytes();w=json.loads(gzip.decompress(wb));meta=w['late_packet_delivery'];raw={int(x):r for x,r in w['private_role_map'].items()}
    target,loc=replay.interpret_prefix(s,p);actual,actual_loc=replay.interpret_prefix(s,w);need((actual,actual_loc)==(target,loc),'all1880 exact common-entry rows')
    occ=defaultdict(list)
    for j,i in enumerate(w['parent_event_of_output']):
        if i is not None:occ[i].append(j)
    pbeg,pend=meta['old_packet_range'];ebeg,eend=meta['hoisted_initial_decoder_range'];rerouted={v[0]:int(y) for y,v in meta['parent_receivers_rerouted'].items()}
    for i,op in enumerate(p['program']):
        js=occ[i]
        if pbeg<=i<pend:need(not js,'old packet macro explicitly replaced')
        elif i in rerouted:
            need(len(js) in (2,3),'every rerouted original ascent has all actual segments')
            chain=[w['program'][j] for j in js]
            need(all(e[0]=='MOVE' and e[1]==op[1] and e[4] is False for e in chain),'same authentic raw carrier')
            need(chain[0][2]==op[2] and chain[-1][3]==op[3] and all(e[3]==f[2] for e,f in zip(chain,chain[1:])),'exact original route endpoints and ordered segment chain')
        else:need(len(js)==1 and w['program'][js[0]]==op,'unchanged or hoisted parent opcode')
    kept=[i for i in w['parent_event_of_output'] if i is not None and not ebeg<=i<eend and i not in rerouted]
    expected=[i for i in range(len(p['program'])) if not pbeg<=i<pend and not ebeg<=i<eend and i not in rerouted]
    need(kept==expected,'all non-hoisted retained chronology')
    need(w['native_event_to_physical']==[occ[i][0] for i in p['native_event_to_physical']],'authentic native operation map')
    need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'identical common suffix')
    mutants={}
    def reject(name,m):
        try:
            rows,places=replay.interpret_prefix(s,m);need(rows==target and places==loc,'mutant endpoint row mismatch')
        except (ValueError,KeyError,IndexError) as e:mutants[name]=str(e)
        else:raise ValueError('unrejected mutation '+name)
    hosted={s['live'][i] for i in s['hosted']['Dports']};coupled=set(s['live'])-hosted
    coupled_event=next(d['event'] for p0 in meta['packets'] for d in p0['deliveries'] if d['firstX'] in coupled)
    m=copy.deepcopy(w);m['program'][coupled_event][3]=str(2*F(m['program'][coupled_event][3]));reject('coupled_half_factor_removed',m)
    m=copy.deepcopy(w);i=meta['packets'][6]['descents'][0];m['program'][i][3]=meta['second_line'];reject('penultimate_packet_wrong_line',m)
    m=copy.deepcopy(w);i=meta['packets'][7]['descents'][1];m['program'][i][4]=False;reject('last_owned_descent_marked_public',m)
    affected=set(meta['first_support'])|set(meta['second_support']);hoisted=next(j for j in range(meta['hoist_begin'],meta['new_packet_range'][0]) if w['program'][j][1] in {raw[x+112] for x in affected})
    m=copy.deepcopy(w);op=m['program'].pop(hoisted);m['program'].insert(meta['new_packet_range'][1]-1,op);reject('required_empty_chart_add_not_hoisted',m)
    m=copy.deepcopy(w);i=meta['packets'][7]['deliveries'][0]['event'];m['program'][i][3]=str(-F(m['program'][i][3]));reject('late_shared_delivery_sign',m)
    need(len(mutants)==5,'five meaningful source mutations')
    result={'status':'PASS_AUTHOR_LATE_TWO_PROVENANCE_AND_MUTANTS','word_payload_sha256':sha(gzip.decompress(wb)),'parent_payload_sha256':sha(gzip.decompress(pb)),'all1880_prefix_columns_match':True,'old_packet_macro_replaced':pend-pbeg,'raw_paths_fully_lineaged':len(rerouted),'hoisted_adds':eend-ebeg,'native_clock_map_exact':True,'literal_suffix_unchanged':True,'mutants_rejected':mutants,'scope':'Author additional audit; independent mathematical/source review remains separate.'}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],len(mutants))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
