#!/usr/bin/env python3
"""Fresh source reproduction of the recovered odd8 cut for E8 packets.

No recovered author/reviewer implementation or result certificate is imported.
The recovered witness ports are credited; exact source rows and capacity are
reconstructed here. This is an interface corollary of the existing cut.
"""
import argparse,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from cohort_geometry import SOURCE_PIN,space,require
from check_cohort_word import load,sha,rowadd,root_bounds,moment,PARENT_PIN,PARENT_PAYLOAD,INVOICE_PIN

PORTS=[24,103,0,32,97,72,37,86]

def rank_and_minor(rows):
 piv={};chosen=[];columns=[]
 for role,row in sorted(rows.items()):
  x=dict(row)
  while x:
   col=min(x);v=x[col]
   if col not in piv:
    piv[col]={j:c/v for j,c in x.items()};chosen.append(role);columns.append(col);break
   x=rowadd(x,piv[col],-v)
 return len(piv),chosen,columns

def det(rows,columns):
 a=[{j:row[k] for j,k in enumerate(columns) if k in row} for row in rows];ans=F(1)
 for j in range(len(a)):
  i=next((i for i in range(j,len(a)) if a[i].get(j)),None)
  if i is None:return F(0)
  if i!=j:a[i],a[j]=a[j],a[i];ans=-ans
  v=a[j][j];ans*=v
  for i in range(j+1,len(a)):
   if a[i].get(j):a[i]=rowadd(a[i],a[j],-a[i][j]/v)
 return ans

def actual_output_rows(source,outputs):
 state=[{} for _ in range(source['public']+source['owned_fields'])]
 for role in outputs:state[role]={role:F(1)}
 for op in reversed(source['program']):
  kind,r=op[:2]
  if kind=='ADD':state[op[2]]=rowadd(state[op[2]],state[r],F(op[3]))
  elif kind=='SCALE':state[r]={j:c*F(op[2]) for j,c in state[r].items()}
  elif kind=='COPY':state[op[2]]=rowadd(state[op[2]],state[r],F(op[3]));state[r]={}
  elif kind in ('INIT','CLEAR'):state[r]={}
  else:require(kind=='MOVE','recognized native opcode')
 require(not any(state[source['public']:]),'no invented owned input')
 rows={r:{} for r in outputs}
 for j,col in enumerate(state[:source['public']]):
  for r,c in col.items():rows[r][j]=c
 return rows

def main(a):
 source=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',True,SOURCE_PIN)
 base=a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused'
 parent=load(base/'WORD.json.gz',True,PARENT_PIN,PARENT_PAYLOAD);invoice=load(base/'INPUT-INVOICE.json',pin=INVOICE_PIN)
 spaces=[space(v) for v in source['frames']];xs=source['live'];ports=[source['ports'][i] for i in PORTS]
 require(len(set(ports))==8 and set(PORTS)<=set(source['hosted']['Dports']),'actual eight hosted ports')
 require(all((x&y).bit_count()%2==1 for x in ports for y in ports),'all64 odd pairings')
 inside={i for i,C in enumerate(spaces) if any(p in C for p in ports)}
 require(len(inside)==377 and 127 in inside and 3 not in inside,'actual cut source charts')
 n=source['public'];I={r for r in range(n) if source['initial'][r] in inside};O={r for r in range(n) if source['final'][r] in inside}
 M=set(xs)|{x+112 for x in xs}|set(source['hosted']['X2'])|set(source['hosted']['Y2'])
 require((n,len(M),len(I),len(O),len(I&M),len(O&M))==(1480,400,53,1300,16,384),'all actual conditional domain counts')
 target={r:{r:F(1)} for r in range(n)}
 for i,x in enumerate(xs):
  y=x+112
  if i in source['hosted']['Dports']:target[y][x]=F(1)
  else:target[x][y]=F(-1);target[y]={x:F(1,2),y:F(1,2)}
 for b,d in zip(source['hosted']['X2'],source['hosted']['Y2']):target[b][d]=F(-1)
 actual=actual_output_rows(source,O);require(actual=={r:target[r] for r in O},'fresh exact1300 source outputs on all1480 initial columns')
 matrices={};certs={}
 for name,outputs,columns in [('common',O,set(range(n))-I),('private',O&M,M-I)]:
  rows={r:{j:c for j,c in actual[r].items() if j in columns} for r in outputs};rk,rs,cs=rank_and_minor(rows)
  determinant=det([rows[r] for r in rs],cs);require(determinant!=0,'independent conditional minor nonzero')
  serial={str(r):[[j,str(c)] for j,c in sorted(row.items())] for r,row in sorted(rows.items())}
  matrices[name]=rows;certs[name]=dict(rank=rk,rows=len(rows),outside_columns=len(columns),matrix_sha256=sha(json.dumps(serial,sort_keys=True).encode()),minor_rows=rs,minor_columns=cs,minor_determinant=str(determinant))
 require(certs['common']['rank']==1255 and certs['private']['rank']==376,'exact1631 complete conditional target rank')
 incoming=[];outgoing=[];loc=dict(enumerate(source['initial']));rawhist=Counter()
 for e,op in enumerate(source['program']):
  kind,r=op[:2]
  if kind=='INIT':require(r>=n and r not in loc,'native INIT');loc[r]=op[2]
  elif kind=='CLEAR':require(r>=n and loc.get(r)==op[2],'native CLEAR');del loc[r]
  elif kind=='MOVE':
   _,_,u,v,owned=op;require(loc[r]==u and owned==(r>=n),'actual native move endpoint and ownership')
   require(spaces[u]<spaces[v] or (owned and spaces[v]<spaces[u]),'native nested movement')
   rec=[e,r,u,v,owned,abs(len(source['frames'][v])-len(source['frames'][u]))]
   if u not in inside and v in inside:incoming.append(rec)
   if u in inside and v not in inside:outgoing.append(rec)
   if r in M:require(not owned and spaces[u]<spaces[v],'original raw reservation monotone');rawhist[rec[-1]]+=1
   loc[r]=v
  elif kind in ('ADD','COPY'):require(loc[r]==loc[op[2]]==op[4],'actual native cochart')
  elif kind=='SCALE':require(loc[r]==op[3] and F(op[2]),'native nonzero scale')
  else:raise ValueError(kind)
 require(loc==dict(enumerate(source['final'])),'complete native location closure')
 require(len(incoming)==1255 and sum(r[4] for r in incoming)==8 and len(outgoing)==8 and all(r[4] for r in outgoing),'exact saturated common crossing count')
 require(rawhist=={1:990,2:360,3:105,4:112,5:133,6:8,7:2} and sum(rawhist.values())==1710,'all1710 original raw reservation counts')
 classes=Counter()
 for r in M:
  u,v=source['initial'][r],source['final'][r];require(spaces[u]<spaces[v] and len(source['frames'][v])-len(source['frames'][u])==8,'all400 prescribed endpoints nested with gap8')
  classes[str((u in inside,v in inside))]+=1
 require(classes=={'(True, True)':16,'(False, False)':16,'(False, True)':368},'exact arbitrary-monotone raw capacity')
 packet=[op for op in parent['program'] if op[0]=='MOVE' and op[4] and op[2]==127 and op[3]==3]
 require(len(packet)==8 and all(len(spaces[op[2]])==512 and spaces[op[3]]=={0} for op in packet),'eight actual retained rank9 outward E8 packets')
 require(all(not(op[2] not in inside and op[3] in inside) for op in packet),'no E8 packet inward capacity')
 needed=1255+376;funded=1255+368;require(needed-funded==8,'eight additional inward fields required')
 no_reverse={r:dict(row) for r,row in matrices['private'].items()}
 for b,d in zip(source['hosted']['X2'],source['hosted']['Y2']):
  if b in no_reverse:no_reverse[b].pop(d,None)
 chosen=source['hosted']['Dports'].index(PORTS[0]);b,d=source['hosted']['X2'][chosen],source['hosted']['Y2'][chosen];minus_one={r:dict(row) for r,row in matrices['private'].items()};minus_one[b].pop(d)
 require(rank_and_minor(no_reverse)[0]==368 and rank_and_minor(minus_one)[0]==375,'reverse target coefficients cause the gap')
 even=space([257,258,260,264,272,288,320,384]);require(len(even)==256 and all(v.bit_count()%2==0 for v in even) and all(p not in even for p in source['ports']),'universal even-hyperplane cut-filling edge')
 raw_can_visit_even=[r for r in M if spaces[source['initial'][r]]<=even<=spaces[source['final'][r]]]
 require(raw_can_visit_even==[],'no prescribed monotone raw holder can ever occupy the even hyperplane')
 require(all(C!=even for C in spaces),'no original common chart or native MOVE endpoint at the even hyperplane')
 facet=source['final'][d];facet_holders=sorted(r for r in M if spaces[source['initial'][r]]<=spaces[facet]<=spaces[source['final'][r]])
 require(len(facet_holders)==91 and {xs[PORTS[0]]+112,d}<=set(facet_holders),'availability scope control: a real selected facet admits91 raw paths, including its two receivers')
 c=root_bounds(9)[0]/9;slack=10*c-root_bounds(8)[1]-1;slope=2*c-1;require(slack>F(973,1000) and slope>0,'universal nested-detour cost charge')
 T={int(r):m for r,m in invoice['T4'].items()};P={int(r):m for r,m in invoice['P4'].items()}
 paid={r:P.get(r,0)-18*rawhist[r]+18*(400 if r==8 else 0)+18*(8 if r==9 else 0) for r in P.keys()|rawhist.keys()|{8,9}}
 require(all(v>=0 for v in paid.values()),'nonnegative complete400-direct plus E8 invoice')
 margin=tuple(x/18 for x in moment({r:T.get(r,0)-paid.get(r,0) for r in T.keys()|paid.keys()}));require(F(47079,1000)<margin[0]<margin[1]<F(47080,1000),'source allowance47.079.. before new communications')
 proof=a.repo/'research/moonshot-005-program/sessions/2026-11-12-S007/recovery/budget/odd8-saturated-cut/PROOF.md'
 result=dict(status='PASS_FRESH_SOURCE_CUT_AND_E8_INTERFACE_APPLICATION',source_sha256=SOURCE_PIN,parent_sha256=PARENT_PIN,parent_payload_sha256=PARENT_PAYLOAD,invoice_sha256=INVOICE_PIN,
  recovered_proof_sha256=sha(proof.read_bytes()),reviewer_sha256=sha(Path(__file__).read_bytes()),witness_port_indices=PORTS,witness_port_vectors=ports,
  actual_source_outputs=1300,independent_original_common_columns=1480,conditional_matrices=certs,inside_chart_count=377,inside_common_initials=53,inside_common_finals=1300,inside_private_initials=16,inside_private_finals=384,
  native_incoming_MOVEs=incoming,native_outgoing_MOVEs=outgoing,raw_endpoint_classes=dict(classes),raw_forced_incoming_fields=368,E8_packets=packet,E8_incoming_capacity=0,
  conditional_required_rank=needed,retained_incoming_capacity=funded,minimum_additional_incoming_fields=8,
  negative_controls=dict(remove_all96_reverse_coefficients_rank=368,remove_one_selected_reverse_coefficient_rank=375,omit_E8_outward_packet_does_not_remove_inward_deficit=True,
    reverse_all_E8_packet_directions_would_add8_inward_fields_but_change_interface=True,real_selected_facet_has_raw_holders=facet_holders),
  even_hyperplane=dict(basis=[257,258,260,264,272,288,320,384],source_chart_ids=[i for i,C in enumerate(spaces) if C==even],raw_monotone_holders=[],all_active_ports_excluded=True,rank1_exit_to_hub=True,scope='A universal dual-normalization edge, not an available data holder; every useful acquisition and new incoming movement still needs funding.'),
  nested_detour_charge=dict(cycle_slack_lower=str(slack),cycle_slope_lower=str(slope),additional_moment_at_least=8),
  direct_raw_E8_allowance_exact=[str(x) for x in margin],direct_raw_E8_allowance_approx=float(margin[0]),allowance_after_necessary8_exact=[str(x-8) for x in margin],
  scope='Inherited odd8 spatial-cut theorem freshly reproduced and applied to fixed common MOVE endpoints plus the retained8 outward E8 packet legs, with all400 raw endpoints fixed. Arbitrary field-linear recoding, dirty mixtures, feedback and all ambient-nine charts permitted. Eight is necessary, not sufficient, and does not exclude the current E8 target allowance. The E8 implication was already stated in recovered S007 nine-layer notes. No new kappa.')
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k] for k in ('status','conditional_required_rank','retained_incoming_capacity','minimum_additional_incoming_fields','direct_raw_E8_allowance_approx','even_hyperplane')},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
