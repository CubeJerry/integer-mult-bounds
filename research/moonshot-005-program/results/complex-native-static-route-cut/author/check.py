#!/usr/bin/env python3
"""Exact source-bound two-way cut. No numerical solver is needed."""
import argparse,hashlib,json,sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

def need(condition,label):
 if not condition:raise ValueError(label)

ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
package=Path(__file__).resolve().parent.parent
pins=json.loads((package/'SOURCE-PINS.json').read_text())
for name,digest in pins['files'].items():need(hashlib.sha256((args.repo/name).read_bytes()).hexdigest()==digest,'source pin '+name)
rail=args.repo/'research/moonshot-005-program/results/complex-native-contested-restoration/rail'
sys.path.insert(0,str(rail));import check
w=check.read('rail-base.json.gz');L,ends,paid,pairs,bill=check.replay(w)
C=[{int(j):check.rational(x)for j,x in row.items()}for row in check.read('base-correction.json.gz')];E=check.product(C,L)
g=check.Graph();full,mains,binding=check.transfer(g);bound=check.remap(g,full,mains,check.read('LAYOUT.json.gz'),w,ends)
need(E==bound and check.rank(E)==400,'authentic all-column main endpoint')
need(sum(paid.values())==803 and len(w['program'])==4748,'old word census')
canonical={};chart={}
for i,frame in enumerate(w['frames']):
 space=check.span(tuple(frame));chart[i]=canonical.setdefault(space,i)
cert=json.loads((package/'CUT.json').read_text());inside=set(cert['inside_canonical_chart_ids']);need(len(inside)==128,'cut size')
need(all(chart[i]==i for i in inside),'canonical cut identifiers')
inp={j for j,c in enumerate(w['initial'])if chart[c]in inside};out={i for i,c in enumerate(ends)if chart[c]in inside};allids=set(range(400))
need(len(inp)==172 and len(out)==228,'boundary census')
forward_rows=check.reduce_rows(E,sorted(allids-out),inp);reverse_rows=check.reduce_rows(E,sorted(out),allids-inp)
rf=check.rank(forward_rows);rr=check.rank(reverse_rows)
need((rf,rr)==(90,146),'two target cross ranks')
cross={'forward':[],'reverse':[]};hist={'forward':Counter(),'reverse':Counter()}
for k,o in enumerate(w['program']):
 if o[0]!='MOVE':continue
 _,reg,a,b,owned=o;aa,bb=chart[a]in inside,chart[b]in inside
 if aa==bb:continue
 direction='forward'if aa else'reverse';r=abs(len(w['frames'][a])-len(w['frames'][b]));need(r>0,'positive crossing grade')
 cross[direction].append({'instruction':k,'source':a,'destination':b,'register':reg,'rank':r});hist[direction][r]+=1
nf=len(cross['forward']);nr=len(cross['reverse']);need((nf,nr)==(8,64),'old crossing capacities')
need(all(z['source']==127 and z['destination']==3 and z['rank']==9 for z in cross['forward']),'only old downward heads cross forward')
need(check.rank(check.reduce_rows(L,sorted(allids-out),inp))<=nf and check.rank(check.reduce_rows(L,sorted(out),allids-inp))<=nr,'implemented source obeys cut')
# Each diagonal target crossing is explicit; replacing E by its old endpoint
# must not yield the 82+82 deficit.
old_ranks=[check.rank(check.reduce_rows(L,sorted(allids-out),inp)),check.rank(check.reduce_rows(L,sorted(out),allids-inp))]
need(sum(max(0,x-y)for x,y in zip(old_ranks,[nf,nr]))==0,'old endpoint positive control')
need((rf-nf,rr-nr)==(82,82),'two directional deficits')
t=Fraction(199,200);old=check.moment(paid,t);caller=check.moment(check.add_profiles((1,g.fixed_root),(-1,g.fixed_paid)),t);limit=(caller[0]/g.calls,caller[1]/g.calls)
native=check.moment(check.add_profiles((1,g.native),(-1,g.helpers)),t);d=(native[0]-limit[1],native[1]-limit[0]);need(d[0]>0,'strict finite-m penalty')
extra=rf-nf+rr-nr;new=(old[0]+extra,old[1]+extra);short=(new[0]-limit[1],new[1]-limit[0]);allow=(limit[0]-old[1],limit[1]-old[0]);need(short[0]>100 and short[1]<101,'strict fixed-route price failure')
# If an old move is removed, its maximum saving after replacing its lost
# crossing capacity is at most 8^t. Every old rank-nine move crosses the cut.
need(paid[9]==8 and hist['forward'][9]+hist['reverse'][9]==8,'rank-nine removal capacity debit')
eight=check.moment({8:1},t);need(12*eight[1]<short[0] and 13*eight[0]>short[1],'at least thirteen old movement changes')
receipt={'status':'PASS_TWO_WAY_STATIC_CUT_164','complete_kappa_claimed':False,'binding':binding,'source':bill,'cut_size':len(inside),'initial_inside':len(inp),'final_inside':len(out),'target_cross_ranks':[rf,rr],'old_cross_capacities':[nf,nr],'old_endpoint_cross_ranks':old_ranks,'new_move_deficits':[rf-nf,rr-nr],'minimum_new_moves':extra,'old_crossing_histograms':{k:dict(sorted(v.items()))for k,v in hist.items()},'old_crossings':cross,'price':{'old_private_moment':check.pretty(old),'limiting_private_allowance':check.pretty(limit),'limiting_extra_allowance':check.pretty(allow),'minimum_complete_fixed_route_moment':check.pretty(new),'minimum_shortfall':check.pretty(short),'finite_m_native_penalty':check.pretty(d),'maximum_discount_per_removed_old_move':check.pretty(eight),'necessary_number_of_removed_or_retargeted_old_moves':13},'controls':['The implemented old endpoint has no cut deficit.','All chart aliases are merged by literal binary span.','Both demand directions use exact rational elimination.','All eight old rank-nine moves cross the cut.']}
(args.out/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],extra,flush=True)
