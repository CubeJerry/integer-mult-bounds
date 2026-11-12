#!/usr/bin/env python3
"""Actual early-dual fanout and single paid column for a principal Gram extension."""
import argparse,copy,gzip,hashlib,json,sys
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
PARENT='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a'
B=[5,56,65,69,77,96,100,103];S=[0,7,20,27,36,46,57,111]
def main(a):
 d=a.repo/'research/moonshot-005-program/results/cohort-reconstruction';sys.path.insert(0,str(d));from common import need,root,load_inputs,sha,space,Emitter;import build as replay
 src,_,_=load_inputs(a.repo);path=a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz';pb=path.read_bytes();need(sha(gzip.decompress(pb))==PARENT,'exact rank88 parent');p=json.loads(gzip.decompress(pb));raw={int(k):v for k,v in p['private_role_map'].items()};host={src['live'][i]:(x,y) for i,x,y in zip(src['hosted']['Dports'],src['hosted']['X2'],src['hosted']['Y2'])};t=a.port;need(t in host and t not in B+S,'outside principal hosted port')
 roots={x:root(src['frames'][src['initial'][x]][0]) for x in src['live']};G=lambda x,y:Q(sum(u*v for u,v in zip(roots[x],roots[y])),8)
 ss=[s for s in S if G(t,s)];ks=[s for s in B+S if G(t,s)];need(len(ss)==4 and len(ks)==8,'exact missing incidence sets')
 frames=src['frames']+[x['frame'] for x in p['additional_charts']];sp=list(map(space,frames));line=src['initial'][t];need(src['initial'][host[t][0]]==line,'paired raw source line')
 routes={}
 for s in ss:
  role=host[s][1];ix=[i for i,o in enumerate(p['program']) if o[0]=='MOVE' and o[1]==raw[role]];need(len(ix)==1,'one genuine raw dual path');i=ix[0];o=p['program'][i];need(o==['MOVE',raw[role],3,src['final'][role],False],'unchanged raw dual route');need(sp[line]<sp[o[3]],'actual intermediate line containment');routes[i]=s
 E=Emitter();first={};mapping={};bound={};early=[];packet=[];temp=1880
 def emit(o,parent=None):return E.emit(o,parent)
 def preload():
  for i,s in sorted(routes.items()):
   j=emit(['MOVE',raw[host[s][1]],3,line,False],i);first[i]=j;early.append(j)
   early.append(emit(['ADD',raw[host[t][0]],raw[host[s][1]],str(G(t,s)),line]))
 def feedback():
  f=src['final'][host[t][1]];packet.append(emit(['INIT',temp,f]));packet.append(emit(['ADD',temp,raw[host[t][1]],'1',f]));packet.append(emit(['MOVE',temp,f,127,True]))
  for k in ks:packet.append(emit(['ADD',raw[host[k][0]],temp,str(G(k,t)),127]))
  packet.append(emit(['CLEAR',temp,127]))
 for i,o in enumerate(p['program']):
  if i==400:preload()
  if i==p['marks']['common_starts']:feedback()
  bound[i]=len(E.ops)
  if i in routes:
   mapping[i]=first[i];emit(['MOVE',o[1],line,o[3],False],i)
  else:mapping[i]=emit(copy.deepcopy(o),i)
 bound[len(p['program'])]=len(E.ops)
 w=copy.deepcopy(p);w['parent_second_frame_feedback_provenance']=w.pop('second_frame_feedback');w.update(schema='moonshot-S009-principal-extension-early-duals-v1',program=E.ops,parent_event_of_output=E.lineage,parent_word_sha256=sha(pb),native_event_to_physical=[mapping[i] for i in p['native_event_to_physical']],marks={k:bound[v] for k,v in p['marks'].items()},principal_extension={'principal_before':B+S,'new_port':t,'early_dual_ports':ss,'hub_column_ports':ks,'line_chart':line,'early_events':early,'packet_events':packet,'refined_parent_routes':{str(i):s for i,s in routes.items()}})
 for dest,source,coef in [(t,s,G(t,s)) for s in ss]+[(k,t,G(k,t)) for k in ks]:
  key=str(host[dest][0]);row={int(j):Q(v) for j,v in w['paired_reverse_corrections'].get(key,[])};drole=host[source][1];row[drole]=row.get(drole,Q(0))+coef;w['paired_reverse_corrections'][key]=[[j,str(v)] for j,v in sorted(row.items()) if v]
 old,oloc=replay.interpret_prefix(src,p);new,nloc=replay.interpret_prefix(src,w);want=copy.deepcopy(old)
 def add(row,source,c):
  for j,v in source.items():
   q=row.get(j,Q(0))+c*v
   if q:row[j]=q
   else:row.pop(j,None)
 q={x:{raw[x]:Q(1),x:Q(-1)} for x in raw}
 for s in ss:add(want[raw[host[t][0]]],q[host[s][1]],G(t,s))
 for k in ks:add(want[raw[host[k][0]]],q[host[t][1]],G(k,t))
 need(new==want and nloc==oloc,'all1880 actual source coefficients exactly declared twelve additions')
 suffix=w['program'][w['marks']['common_starts']:];need(suffix==p['program'][p['marks']['common_starts']:],'literal parent common suffix')
 for k in [t]+ks:
  r=host[k][0];uses=[o for o in suffix if o[1]==raw[r] or o[0] in ('ADD','COPY') and o[2]==raw[r]];need(uses==[['ADD',raw[r],r,'1',src['final'][r]]],'new reverse row only recouples in common suffix')
 order=list(host);M=[[Q(i==j)+new[raw[host[i][0]]].get(raw[host[j][1]],Q(0)) for j in order] for i in order]
 N=copy.deepcopy(M);rr=0
 for j in range(len(N[0])):
  k=next((i for i in range(rr,len(N)) if N[i][j]),None)
  if k is None:continue
  N[rr],N[k]=N[k],N[rr];v=N[rr][j];N[rr]=[a/v for a in N[rr]]
  for i in range(rr+1,len(N)):
   if N[i][j]:v=N[i][j];N[i]=[a-v*b for a,b in zip(N[i],N[rr])]
  rr+=1
 need(rr==87,'actual reverse residual rank87')
 K=B+S+[t];ix={h:i for i,h in enumerate(order)};need(all(M[ix[i]][ix[j]]==G(i,j) for i in K for j in K),'closed principal Gram block');need(all(not M[ix[i]][ix[j]] for i in K for j in order if j not in K),'no new outside principal columns')
 bill=replay.typed(src,w);oldbill=replay.typed(src,p);need(bill.pop('final_locations')==oldbill.pop('final_locations'),'all final locations');P0=json.loads((path.parent/'RESULT.json').read_text())['conditional_caller'];P=Counter({int(k):v for k,v in P0['P_partial'].items()});T=Counter({int(k):v for k,v in P0['T4'].items()})
 rh=Counter(bill['raw_histogram']);oh=Counter(oldbill['raw_histogram']);dr={r:rh[r]-oh[r] for r in rh.keys()|oh.keys() if rh[r]!=oh[r]};need(dr=={1:4,7:4,8:-4},'complete raw refinement histogram');P[1]+=18
 for r,c in dr.items():P[r]+=18*c
 lo,hi=replay.interval({r:T[r]-P[r] for r in T.keys()|P.keys()});delta={k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()};need({k:v for k,v in delta.items() if v}=={'MOVE':5,'ADD':13,'INIT':1,'CLEAR':1},'complete ordinary increment')
 payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);a.out.mkdir(parents=True,exist_ok=True);(a.out/'WORD.json.gz').write_bytes(blob)
 result={'status':'PASS_SOURCE_PRINCIPAL_EXTENSION_TO_RANK87','source_sha256':p['source_sha256'],'parent_payload_sha256':PARENT,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'new_port':t,'closed_principal_ports':K,'new_reverse_coefficients':12,'actual_reverse_residual_rank':rr,'all1880_prefix_columns_exact':True,'same_literal_common_suffix':True,'forward_rows_unchanged':True,'existing_forward_residual_coefficients':4569,'bill':bill,'ordinary_increment':delta,'raw_histogram_increment':dr,'new_owned_histogram':{1:1},'conditional_caller':{'T4':dict(sorted(T.items())),'P_partial':dict(sorted(P.items())),'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(r*(T[r]-P[r]) for r in T.keys()|P.keys()),'remaining_moment_per_native_lower':str(lo/18),'remaining_moment_per_native_upper':str(hi/18)},'scope':'Actual twelve-coefficient principal block extension. Requires independent review, physical supplier and full completion. No new kappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],len(w['program']),float(lo/18),'rank',rr,'port',t)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--port',type=int,default=90);a.add_argument('--out',type=Path,required=True);main(a.parse_args())
