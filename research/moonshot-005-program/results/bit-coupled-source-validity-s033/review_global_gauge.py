"""Independent source/H inheritance review of the global-gauge lift.

Uses predecessor field arithmetic, separate from the root's reverse-pivot
implementation; does not import the new lift constructor.
"""
from pathlib import Path
import argparse,importlib.util,json,gzip,numpy as np

def mod(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def need(v,msg):
 if not v:raise ValueError(msg)

def review(repo,gauge,out,candidate_path=None):
 here=Path(__file__).parent;b=mod(here/'check.py','review_source');g,a,s,e,old,c,changed=b.load(repo);z=b.read(gauge);base=repo/'research/moonshot-005-program/results';systems=b.read(base/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');fib=b.read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz');T=np.array(b.read(base/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz')['matrix'],dtype=np.uint8);TT=np.array(z['D_matrix'],dtype=np.uint8);L=np.array(s['simultaneous_original_space'],dtype=np.uint8);R=[6,9,48,73];O={int(r):ii for r,ii in systems['D_outputs'].items()};I={int(j):ii for j,ii in systems['D_inputs'].items()};records=[]
 # load() defaults to t=1 changes; the theorem starts at literal S032 maps.
 old={int(j):{int(h):np.array(F,dtype=np.uint8)for h,F in mm.items()}for j,mm in s['paired_maps'].items()}
 candidate=b.read(candidate_path or here/'global-gauge-q4/CANDIDATE.json.gz')
 need(np.array_equal(np.array(candidate['D_matrix'],dtype=np.uint8),TT),'compiler D candidate binding')
 for j0,G0 in z['source_right_gauges'].items():
  j=int(j0);G=np.array(G0,dtype=np.uint8);need(a.rank(G)==96,'invertible protected gauge');GG=np.eye(480,dtype=np.uint8);GG[np.ix_(b.PROT,b.PROT)]=G;changed_sources={h:a.mm(F,GG)for h,F in old[j].items()};basis=np.array(e[j0]['physical_matrix'],dtype=np.uint8);composed=a.mm(basis,GG)
  for h,F in old[j].items():
   materialized=F.copy();materialized[np.ix_(b.PROWS,b.PROT)]^=np.array(candidate['source_protected_delta'][f'{j}/{h}'],dtype=np.uint8);need(np.array_equal(materialized,changed_sources[h]),'compiled quotient equals full right gauge')
  physical=np.zeros((480,480),dtype=np.uint8)
  for q,(h,owner)in enumerate(e[j0]['row_owners']):
   within=sum(t[0]==h for t in e[j0]['row_owners'][:q]);Q=np.array(s['frames'][f'{j}/{h}'],dtype=np.uint8);physical[owner]=a.mm(Q,changed_sources[h])[within]
  need(np.array_equal(composed,physical),'physical preparation is common right composition')
  hcount=0
  for h0,rr in fib.items():
   if int(h0)not in old[j]:continue
   for r,entry in rr.items():
    K=np.array(entry['kernel'],dtype=np.uint8);Z=np.zeros_like(K);KK=np.block([[K,Z],[Z,K]]);need(np.array_equal(a.mm(GG,KK),KK),'entire paired H fibre fixed pointwise');hcount+=1
  for k,r in enumerate(R):
   S=T[np.ix_(O[r],I[j])];Sn=TT[np.ix_(O[r],I[j])];U=a.mm(L[:,8*k:8*k+8],a.mm(S,g.inverse(Sn,a)));need(np.array_equal(a.mm(GG,L[:,8*k:8*k+8]),U),'required D inverse image')
  records.append({'donor':j,'protected_gauge_rank':96,'all_source_quotients_composed':len(changed_sources),'physical_early_composition_checked':True,'whole_H_fibres_fixed':hcount,'four_oriented_frame_equations':True});print('REVIEW_GLOBAL_SOURCE',j,flush=True)
 dw=b.read(base/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz');owners=dw['owners'];sections=[]
 for j in sorted(a.charts[1509]):
  ii=[q for q,x in enumerate(owners)if x[3]is not None and j in a.planes[x[3]]]
  for r in range(120):
   if not a.charts[1509]<=a.adj[r]:continue
   oo=[q for q,x in enumerate(owners)if x[5]is not None and r in a.planes[x[5]]];M=TT[np.ix_(oo,ii)];need(M.shape==(8,8)and a.rank(M)==8,'all geometric D sections');sections.append([j,r,8])
 need(len(sections)==144 and a.rank(TT[:19,:19])==19 and a.rank(TT[19:,19:])==16,'all geometric D counts and phases')
 result={'geometric_D_sections':sections,'phase_ranks':[19,16],'status':'PASS_INDEPENDENT_GLOBAL_SOURCE_GAUGE_COMPOSITION_REVIEW','source_records':records,'source_view_and_propagation_inheritance_proved':True,'author_lift_constructor_imported':False,'independent_field_implementation_relative_to_root':True,'full_old_source_replay_repeated':False,'new_complete_kappa':False};out.mkdir(parents=True,exist_ok=True);(out/'GLOBAL-GAUGE-REVIEW.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--gauges',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--candidate',type=Path);q=p.parse_args();review(q.repo.resolve(),q.gauges.resolve(),q.out.resolve(),q.candidate.resolve()if q.candidate else None)
