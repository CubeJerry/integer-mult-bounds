#!/usr/bin/env python3
"""Exact source geometry for the proposed coupled ghost activation points."""
import argparse,gzip,hashlib,json
from pathlib import Path

def need(ok,why):
    if not ok:raise ValueError(why)
def span(frame):
    out={0}
    for v in frame:out|={x^v for x in tuple(out)}
    return out
def main(a):
    src=a.repo/'research/shared-wire-split-composition/data/final.json.gz'
    word=a.repo/'research/moonshot-005-program/results/cohort-reconstruction/eight/WORD.json.gz'
    sb=src.read_bytes();wb=word.read_bytes();payload=gzip.decompress(wb)
    need(hashlib.sha256(sb).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin')
    need(hashlib.sha256(payload).hexdigest()=='b729da0247aac10019ce6bdd93017b64d185e00101c57f655165a44c4d445f3b','eight cohort pin')
    s=json.loads(gzip.decompress(sb));w=json.loads(payload);X=sorted(s['live']);H={X[i] for i in s['hosted']['Dports']}
    U=[17,19,30,38,40,47,52,60];indices=[24,103,0,32,97,72,37,86]
    S=[s['live'][i] for i in indices]
    need(set(X)-H==set(U),'actual coupled complement')
    L={i:s['frames'][s['initial'][i]][0] for i in X};V={s['ports'][i] for i in indices}
    need(V=={L[i] for i in S},'explicit port-index to physical-role map')
    need(all((x&y).bit_count()%2 for x in V for y in V),'all ordered odd cut incidences')
    wrong={L[i] for i in indices}
    need(not all((x&y).bit_count()%2 for x in wrong for y in wrong),'port-indices-as-role-labels mutant rejected')
    frames=s['frames']+[x['frame'] for x in w['additional_charts']]
    spaces=[span(f) for f in frames];inside=lambda C:bool(V&spaces[C])
    need(not inside(3) and inside(127),'zero outside and hub inside')
    rows=[]
    for u in U:
        groups=[g for g in w['cohort_collection']['groups'] if u in g['donors']]
        need(len(groups)==1,'one genuine first acquisition for coupled slot')
        g=groups[0];C=g['chart'];need(len(frames[C])==6,'dimension six activation')
        need(all(L[d] in spaces[C] for d in g['donors']),'all actual donor lines reach acquisition')
        need(not inside(s['initial'][u]),'coupled entry does not cross')
        rows.append({'slot':u,'chart':C,'frame':frames[C],'cut_ports_in_chart':[i for i in S if L[i] in spaces[C]],'inside':inside(C),'monotone_inward_tail_capacity':int(not inside(C))})
    need(sum(r['monotone_inward_tail_capacity'] for r in rows)==8,'all eight coupled ghost tails enter')
    choices=[]
    for j in sorted(H):
        F=s['final'][j+112]
        need(spaces[F]=={x for x in range(512) if not (x&L[j]).bit_count()%2},'source polar facet')
        need((not inside(F))==(j in S),'only the selected eight hosted facets are outside')
        if j in S:
            need(inside(s['initial'][j]),'selected line already inside')
            ghost,ret=0,1
        else:
            ghost,ret=1,0
        choices.append({'slot':j,'facet':F,'facet_inside':inside(F),'ghost_capacity_upper':ghost,'return_capacity':ret,'combined_upper':ghost+ret})
    need(len(choices)==96 and all(c['combined_upper']==1 for c in choices),'universal reserved-slot upper bound')
    result={'status':'PASS_CURRENT_COHORT_GHOST_CUT_GEOMETRY','source_sha256':hashlib.sha256(sb).hexdigest(),'cohort_payload_sha256':hashlib.sha256(payload).hexdigest(),'cut_port_indices':indices,'cut_physical_roles':S,'cut_port_vectors':sorted(V),'coupled_activations':rows,'all_hosted_choices':choices,'coupled_entry_inward':0,'coupled_ghost_inward':8,'reserved_ghost_and_return_upper':1,'inherited_complete_target_additional_inward_requirement':8,'necessary_capacity_floor_met_by_coupled_tails':True,'negative_controls':{'port_indices_used_as_role_labels_rejected':True,'moving_an_uninformed_zero_is_not_an_innovation':True},'scope':'Finite geometry for a conditional global ghost interface. Eight eligible crossings do not prove useful payloads, acquisition, global composition or sufficiency.'}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],'eight eligible inward tails')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
