#!/usr/bin/env python3
"""Independent literal reconstruction and review; imports no author verifier."""
import argparse,copy,gzip,importlib.util,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from engine import Q,need,sha,load,space,add,root9,rank,interpret,interval

def main(a):
 pkg=a.repo/'research/moonshot-005-program/results';sp=a.repo/'research/shared-wire-split-composition/data/final.json.gz';pp=pkg/'paired-cohort/output/WORD.json.gz';wp=a.author/'output/WORD.json.gz'
 sb,pb,wb=[x.read_bytes() for x in (sp,pp,wp)]
 need(sha(sb)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin');need(sha(pb)=='bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17','parent pin');need(sha(wb)=='a312df6c1ea30b8779dbf9f77ceccf2734aa73703f3cccffd7804a5661e5efd7','reviewed star pin')
 s,p,w=map(load,(sp,pp,wp));receipt=load(a.author/'output/RESULT.json');raw={int(x):y for x,y in p['private_role_map'].items()};H={s['live'][i]:(x,y) for i,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};B=p['paired_collection']['selected_first_receivers'];t=0;Y=t+112;d=H[t][1];F=s['final'][Y]
 roots={x:root9(s['frames'][s['initial'][x]][0]) for x in s['live']};gram=lambda x,y:sum(i*j for i,j in zip(roots[x],roots[y]))/2
 need(all(gram(x,y)==int(x==y) for x in B for y in B),'independent Q9 orthonormal frame');need(all(x in H for x in B+[t]) and t not in B,'no aliased coupled port')
 C={b:gram(b,t) for b in B if gram(b,t)};need(len(C)==4 and set(C.values())=={Q(1,2),Q(-1,2)} and sum(c*c for c in C.values())==1,'four contacts')
 roles=list(C)+[H[b][0] for b in C]+[d];need(len(set(roles))==9,'nine distinct real carriers');need(s['initial'][d]==3 and s['final'][d]==F,'actual reverse source facet');old={}
 for z in roles:
  ms=[(i,o) for i,o in enumerate(p['program']) if o[0]=='MOVE' and o[1]==raw[z]];need(len(ms)==1,'unspent unique route');i,o=ms[0];need(o==['MOVE',raw[z],s['initial'][z],s['final'][z],False] and 400<=i<p['marks']['common_starts'],'literal direct parent ascent');old[z]=i
 arrivals=[i for i,o in enumerate(p['program']) if o[0]=='MOVE' and o[1]==raw[Y] and o[3]==F];need(len(arrivals)==1,'actual forward arrival');arrival=arrivals[0]
 need(all(space(s['frames'][s['initial'][b]])<space(s['frames'][F]) for b in C),'actual source incidence')
 fresh=1880+p['owned_fields'];insert=[['INIT',fresh,F],['MOVE',raw[d],3,F,False]]
 for b,c in C.items():insert += [['MOVE',raw[b],s['initial'][b],F,False],['ADD',fresh,raw[b],str(-c),F],['MOVE',raw[b],F,127,False]]
 for b,c in C.items():z=H[b][0];insert += [['MOVE',raw[z],s['initial'][z],F,False],['ADD',raw[z],raw[d],str(c),F],['MOVE',raw[z],F,127,False]]
 expected=[];boundaries={};consumed=[]
 for i,o in enumerate(p['program']):
  if i==400:expected+=copy.deepcopy(insert)
  boundaries[i]=len(expected)
  if i in old.values():consumed.append(i);continue
  expected.append(o)
  if i==arrival:expected += [['ADD',raw[Y],fresh,'1',F],['CLEAR',fresh,F]]
 need(expected==w['program'],'independent full instruction reconstruction');need(len(set(consumed))==9,'nine original routes consumed once');need(w['marks']['common_starts']==boundaries[p['marks']['common_starts']],'common entry marker')
 P,L0=interpret(s,p);W,L1=interpret(s,w);need(L0==L1 and set(P)==set(W),'identical physical prefix interface');q={z:{raw[z]:Q(1),z:Q(-1)} for z in raw};D={raw[Y]:{}}
 for b,c in C.items():D[raw[Y]]=add(D[raw[Y]],q[b],-c);D[raw[H[b][0]]]=add({},q[d],c)
 need(all(W[z]==add(P[z],D.get(z,{})) for z in P),'all1880 columns of every prefix row')
 tail=w['program'][w['marks']['common_starts']:];need(tail==p['program'][p['marks']['common_starts']:],'identical common suffix')
 for z in [Y]+[H[b][0] for b in C]:
  uses=[o for o in tail if o[1]==raw[z] or o[0] in ('ADD','COPY') and o[2]==raw[z]];need(uses==[['ADD',raw[z],z,'1',s['final'][z]]],'changed outputs have no later feedback')
 for b,c in C.items():need(add(W[raw[H[b][0]]],W[raw[d]],-c)==q[H[b][0]],'actual hosted inverse')
 restored=W[raw[Y]]
 for b,c in C.items():restored=add(restored,W[raw[b]],c)
 need(restored==P[raw[Y]],'actual preserved-source forward inverse')
 keys=list(H);M=[];oldM=[]
 for x in keys:
  br=raw[H[x][0]];original=q[H[x][0]];rr=[];oo=[]
  for y in keys:
   yy=H[y][1];c=W[br].get(raw[yy],Q(0));oc=P[br].get(raw[yy],Q(0));rr.append(Q(x==y)+c);oo.append(Q(x==y)+oc);original=add(original,q[yy],c);need(oc==(gram(x,y) if y in B and x not in B else 0),'parent entire reverse block from actual rows')
  need(W[br]==original,'all1880 input coefficients of actual hosted row');M.append(rr);oldM.append(oo)
 need(len(keys)==96 and rank(oldM)==96 and rank(M)==95,'exact96to95rank');kernel=[-gram(x,t) if x in B else gram(x,t) for x in keys];need(all(sum(v*z for v,z in zip(row,kernel))==0 for row in M),'exact source kernel')
 dropped=copy.deepcopy(M);first=next(iter(C));dropped[keys.index(first)][keys.index(t)]-=C[first];need(rank(dropped)==96,'missing feedback contact restores rank96')
 other=next(x for x in keys if x not in B and x!=t and gram(x,t));two=copy.deepcopy(M)
 for b in B:two[keys.index(b)][keys.index(other)]+=gram(b,other)
 need(rank(two)==96 and -gram(t,other)**2==Q(-1,4),'two nonorthogonal stars restore full rank')
 bill,final=interpret(s,w,True);oldbill,oldfinal=interpret(s,p,True);need(final==oldfinal,'all final charts');expectbill={k:({int(r):v for r,v in val.items()} if k in ('move_rank_histogram','raw_histogram') else val) for k,val in receipt['bill'].items()};need(bill==expectbill,'independent full-word counts')
 inc={k:bill['opcode_counts'].get(k,0)-oldbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys()};need({k:v for k,v in inc.items() if v}=={'MOVE':8,'ADD':9,'INIT':1,'CLEAR':1},'ordinary delta')
 dr={k:bill['raw_histogram'].get(k,0)-oldbill['raw_histogram'].get(k,0) for k in bill['raw_histogram'].keys()|oldbill['raw_histogram'].keys()};need({k:v for k,v in dr.items() if v}=={1:8,7:8,8:-8},'raw route delta')
 pr=load(pkg/'paired-cohort/output/RESULT.json')['conditional_caller'];PP={int(k):v for k,v in pr['P_partial'].items()};T={int(k):v for k,v in pr['T4'].items()}
 for k,v in dr.items():PP[k]=PP.get(k,0)+18*v
 need(PP=={int(k):v for k,v in receipt['conditional_caller']['P_partial'].items()},'complete invoice from actual routes');lo,hi=interval({k:T.get(k,0)-PP.get(k,0) for k in T.keys()|PP.keys()});lo/=18;hi/=18
 need(lo<=Q(receipt['conditional_caller']['remaining_moment_per_native_upper']) and hi>=Q(receipt['conditional_caller']['remaining_moment_per_native_lower']),'independent dyadic bounds agree');need(lo>40 and hi<41,'strict complete provisional margin')
 pins={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
 def mod(fn):
  path=a.repo/'research/shared-wire-split-composition/frozen'/fn;need(sha(path.read_bytes())==pins[fn],'chart engine pin');spec=importlib.util.spec_from_file_location('review_star_'+fn[:-3],path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
 need(__debug__,'phase engines require assertions');cl,nv=mod('clifford_exact.py'),mod('native_verify.py');frames=s['frames']+[z['frame'] for z in w.get('additional_charts',[])];oldpairs={(o[2],o[3]) for o in p['program'] if o[0]=='MOVE'};newpairs={(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'};maps=[]
 for A,Bb in sorted(newpairs-oldpairs):
  f,g=frames[A],frames[Bb];recipe,_=cl.lower_child(cl.canonical_frame(9,tuple(f)).adjoint().then(cl.canonical_frame(9,tuple(g))));nv.equal(nv.recipe(recipe),nv.adjoint(nv.frame(f,9))+nv.frame(g,9),'independent star chart');need(recipe['rank']==len(g)-len(f),'exact chart rank');maps.append({'source':A,'target':Bb,'recipe':recipe})
 need(maps,'nonempty map coverage');bad=copy.deepcopy(maps[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4;phase=False
 try:nv.equal(nv.recipe(bad['recipe']),nv.adjoint(nv.frame(frames[bad['source']],9))+nv.frame(frames[bad['target']],9),'mutated phase')
 except ValueError:phase=True
 need(phase,'phase mutant rejected')
 result={'status':'PASS_INDEPENDENT_FEEDBACK_STAR_REVIEW','source_sha256':sha(sb),'parent_word_sha256':sha(pb),'reviewed_word_sha256':sha(wb),'reviewed_payload_sha256':sha(gzip.decompress(wb)),'author_builder_sha256':sha((a.author/'build_feedback_star.py').read_bytes()),'literal_word_reconstructed':True,'full_prefix_rows':len(W),'independent_input_columns':1880,'literal_suffix_unchanged':True,'actual_reverse_rank_before':96,'actual_reverse_rank_after':95,'source_derived_kernel':{str(x):str(k) for x,k in zip(keys,kernel) if k},'full_bill':bill,'ordinary_increment':inc,'raw_histogram_delta':dr,'remaining_moment_per_native_dyadic_lower':str(lo),'remaining_moment_per_native_dyadic_upper':str(hi),'introduced_map_count':len(maps),'introduced_maps':maps,'retained_chart_engine_pins':pins,'negative_controls':{'missing_contact_actual_rank':rank(dropped),'nonorthogonal_two_star_actual_rank':rank(two),'nonorthogonal_reduced_determinant':'-1/4','wrong_global_phase_rejected':phase},'scope':'Independent exact source reconstruction, matrix proof, inverse and invoice; finite source result, no complete supplier or new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'REVIEW.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],bill['instructions'],'instructions;',len(maps),'new maps; rank',rank(M))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
