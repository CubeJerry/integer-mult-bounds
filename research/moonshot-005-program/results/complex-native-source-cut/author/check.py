#!/usr/bin/env python3
"""Exact static export count for every chart-3 funded retarget family."""
import argparse,hashlib,importlib.util,json,sys
from collections import Counter
from pathlib import Path

def need(x,s):
 if not x:raise ValueError(s)

ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
package=Path(__file__).resolve().parent.parent;pins=json.loads((package/'SOURCE-PINS.json').read_text())
for name,h in pins['files'].items():need(hashlib.sha256((a.repo/name).read_bytes()).hexdigest()==h,'source pin '+name)
source=a.repo/'research/moonshot-005-program/results/complex-native-funded-donor-cuts/inputs';spec=importlib.util.spec_from_file_location('retarget_source',source/'7833-construction.py');S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S)
w=S.load_word(source/'DOUBLE-CANDIDATE.json.gz');g=S.compensated(w);five=S.compensated(w,True)
rail=a.repo/'research/moonshot-005-program/results/complex-native-contested-restoration/rail';sys.path.insert(0,str(rail));import check
original=check.Graph();endpoint,mains,binding=check.transfer(original);need(check.rank(endpoint)==1289,'authentic target is injective on all originals')
need({e:dict(row)for e,row in w.forms.items()}==original.forms and w.routes==original.moves,'both readers bind the same original word')
inside_frames=[[],[261],[296],[45,261]];inside={check.span(tuple(f))for f in inside_frames};spaces=[check.span(tuple(f))for f in w.frames];aliases=[i for i,c in enumerate(spaces)if c in inside]
need(set(aliases)=={3,11,58,278},'all equal-span aliases included')
A={~e for e,c in w.inputs.items()if spaces[c]in inside};outs={e for e,c in w.terminals.items()if spaces[c]in inside};need(len(A)==912 and not outs,'912 arbitrary inputs and no public outputs in source set')
need(check.rank(check.reduce_rows(endpoint,range(1289),A))==912,'required outside output rank')
def exports(graph):return {e for e,(u,v)in graph.routes.items()if spaces[u]in inside and spaces[v]not in inside}
old=exports(w);new=exports(g);restored=exports(five)
need((len(old),len(new),len(restored))==(912,911,912),'cut capacities')
changes=[]
for e in sorted(set(w.routes)|set(g.routes)):
 if w.routes.get(e)!=g.routes.get(e):changes.append({'slot':e,'old':w.routes.get(e),'new':g.routes.get(e),'old_export':e in old,'new_export':e in new})
need(len(changes)==4 and sum(int(z['new_export'])-int(z['old_export'])for z in changes)==-1,'four literal surgery changes lose one export')
first=w.clock[w.readers(S.OBSERVER)[0]];donors=[e for e in w.schedule if e in w.routes and w.routes[e][0]==3 and w.clock[e]<first and w.grade(w.routes[e])>=3 and e not in(S.RETARGET,S.OBSERVER)]
need(len(donors)==181 and all(e in new and spaces[g.routes[e][1]]not in inside for e in donors),'entire early funding roster already exports')
need(spaces[282]not in inside,'proposed observer destination outside')
# Replace ALL 181 destinations simultaneously: the same 911 export slots remain.
changed=g.routes.copy()
for e in donors:changed[e]=(3,282)
all_export={e for e,(u,v)in changed.items()if spaces[u]in inside and spaces[v]not in inside};need(all_export==new,'all-subsets certificate: each replacement preserves its indicator')
# Also cover later and otherwise ineligible chart-3 arcs of grade >=3.
wide=[e for e,(u,v)in g.routes.items()if u==3 and g.grade((u,v))>=3];need(all(e in new for e in wide),'every high-grade chart-3 transfer is an export')
# Controls: original graph and genuine fifth channel recover the missing capacity.
shadow,=set(five.routes)-set(w.routes);need(shadow in restored and five.routes[shadow]==(3,282),'actual extra fifth channel crosses')
receipt={'status':'PASS_ALL_SOURCE3_FUNDED_SUBSETS_EXPORT_DEFICIT_ONE','complete_kappa_claimed':False,'source_binding':binding,'cut_frames':inside_frames,'all_chart_aliases':aliases,'independent_initial_inputs':len(A),'inside_public_outputs':len(outs),'target_outside_rank':912,'original_exports':len(old),'four_channel_exports':len(new),'five_channel_exports':len(restored),'surgery_changes':changes,'eligible_early_donors':len(donors),'early_grade_histogram':dict(Counter(w.grade(w.routes[e])for e in donors)),'all_high_grade_chart3_donors':len(wide),'all_subset_argument':'Each changed destination remains outside; every subset preserves each source-cut crossing indicator.','arbitrary_redesign_required_new_exports':1,'controls':['Original target/source has 912 export capacity.','The authentic fifth-channel control has 912 export capacity.','All 181 simultaneous funded redirections still have only 911 exports.'],'export_slots':sorted(new),'eligible_donors':donors,'actual_extra_channel':shadow}
(a.out/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],len(donors),len(wide),flush=True)
