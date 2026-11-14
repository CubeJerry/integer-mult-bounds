#!/usr/bin/env python3
"""Authenticate all cycle-native chart maps and ordinary gauges with retained signed engines."""
from pathlib import Path
from collections import Counter
import argparse,copy,gzip,hashlib,importlib.util,json,sys
sys.dont_write_bytecode=True
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
WORD='bca2056d98d0759d0c7c61104122160d13e12f099bea0cbe2de4169f9b3eac93'
def need(c,m):
 if not c:raise ValueError(m)
def load(base,name):
 p=base/name;need(hashlib.sha256(p.read_bytes()).hexdigest()==PINS[name],'retained signed engine pin');sp=importlib.util.spec_from_file_location('eisenstein_'+name[:-3],p);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m);return m
pa=argparse.ArgumentParser();pa.add_argument('--engines',type=Path,required=True);pa.add_argument('--word',type=Path,default=Path(__file__).with_name('WORD.json.gz'));pa.add_argument('--output',type=Path,default=Path(__file__).with_name('PHASE.json'));a=pa.parse_args();raw=a.word.read_bytes();need(hashlib.sha256(raw).hexdigest()==WORD,'native word pin');w=json.loads(gzip.decompress(raw));c=load(a.engines,'clifford_exact.py');v=load(a.engines,'native_verify.py');frames=w['frames'];ops={j:c.canonical_frame(9,tuple(f))for j,f in enumerate(frames)};edges=sorted(set((e[2],e[3])for e in w['program']if e[0]=='MOVE'));records=[];hist=Counter()
for u,z in edges:
 op=ops[u].adjoint().then(ops[z]);rec,_=c.lower_child(op);expected=len(frames[z])-len(frames[u]);need(rec['rank']==expected,'rank of monotone source edge');v.equal(v.recipe(rec),v.adjoint(v.frame(frames[u],9))+v.frame(frames[z],9),'literal cycle-native chart map');records.append({'source':u,'target':z,'recipe':rec});hist[rec['rank']]+=1
normalizers=[];H=c.fourier(9)
for h,q in enumerate(w['normals']):
 S=ops[2+h];T=ops[122+h];Q=c.cgate(9,q);Nx=Q.adjoint().then(S);Ny=T.adjoint().then(Q.adjoint()).then(H);rx,_=c.lower_child(Nx);ry,_=c.lower_child(Ny);need(rx['rank']==ry['rank']==0,'ordinary input/output gauge');v.equal(v.recipe(rx),Nx.circuit,'line gauge');v.equal(v.recipe(ry),Ny.circuit,'facet gauge');normalizers.append({'normal':q,'input':rx,'output':ry})
bad=copy.deepcopy(records[0]['recipe']);bad['left']['phase']=(bad['left']['phase']+1)%4;failed=False
try:v.equal(v.recipe(bad),ops[edges[0][0]].adjoint().then(ops[edges[0][1]]).circuit,'wrong global phase')
except ValueError:failed=True
need(failed,'phase control');out={'status':'PASS_ALL360_SIGNED_MAPS_AND240_ORDINARY_GAUGES','word_sha256':WORD,'engine_pins':PINS,'unique_move_maps':len(edges),'unique_map_rank_histogram':dict(sorted(hist.items())),'records':records,'normalizers':normalizers,'wrong_global_phase_rejected':failed,'scope':'Source-specific exact one-column Clifford identities; all-width tensor lift follows algebraically. Author uses retained independent engines and does not claim a new independent mathematical review.','caller_admission':False,'no_new_kappa':True};a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
