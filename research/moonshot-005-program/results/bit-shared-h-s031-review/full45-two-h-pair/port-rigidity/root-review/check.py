#!/usr/bin/env python3
"""Reconstruct all native port translation spaces from raw geometry."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,why):
    if not ok:raise ValueError(why)
def read(p):return json.loads(gzip.decompress(p.read_bytes()))

p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
here=Path(__file__).resolve().parent;base=args.repo/'research/moonshot-005-program/results'
for path,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((args.repo/path).read_bytes()).hexdigest()==digest,'pin '+path)
s=importlib.util.spec_from_file_location('old_independent_geometry',base/'bit-coupled-native-geometric-cycle-source/review-c/check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
layout=read(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());roots=g.roots_from_files(layout,basis)
planes=[set(x) for x in layout['A2']];charts=[set(x) for x in layout['D4']];adj=[{j for j,y in enumerate(roots) if j!=i and not g.b(x,y)} for i,x in enumerate(roots)]
parent=here.parents[1]/'author';literal=read(parent/'output/COEFFICIENTS.json.gz');saved=read(parent/'output/FIBRES.json.gz');certificate=read(here.parent/'author/output/CERTIFICATES.json.gz')
maps={int(j):{int(h):np.array(Q,dtype=np.uint8) for h,Q in row.items()} for j,row in literal['source_maps'].items()};counts=[];total=0;readouts=0;mutation_failures=0
for h,expected in [(263,45),(642,44)]:
    ds=sorted(planes[h]);ports=[d for d,D in enumerate(charts) if planes[h]<=D];P=np.array(literal['H'][str(h)]['word'],dtype=np.uint8);views=[i for i in range(111) if planes[h]<=adj[i]]
    need(ports==literal['H'][str(h)]['ports'] and len(ports)==45 and 80 not in views and 10 not in ds,'actual native identity interface')
    constraints={};stored_constraints={}
    for i in views:
        off=np.vstack([maps[ds[0]][a] for a in sorted(maps[ds[0]]) if a!=h and planes[a]<=adj[i]])
        K=g.null(off);KS=np.array(saved[str(h)][str(i)]['kernel'],dtype=np.uint8)
        need(off.shape==(225,240) and K.shape==(240,15) and g.rank(np.hstack([K,KS]))==15,'fresh whole native fibre matches frozen literal')
        pencils=[];stored_pencils=[]
        for j in ds:
            X=np.vstack([maps[j][a] for a in sorted(maps[j]) if a!=h and planes[a]<=adj[i]])
            need(g.rank(X)==225 and not np.any(g.mm(X,K)),'same complete kernel on each donor')
            pencils.append(g.mm(maps[j][h],K));stored_pencils.append(g.mm(maps[j][h],KS));need(g.rank(pencils[-1])==15,'free central amplitudes')
        def translation(D):
            Z=np.zeros((15,15),dtype=np.uint8)
            return np.block([[D[0].T,D[1].T,Z],[D[0].T,Z,D[2].T]])
        constraints[i]=translation(pencils);stored_constraints[i]=translation(stored_pencils)
        need(g.rank(constraints[i])==30,'zero-sum translations')
        visible=[r for r,d in enumerate(ports) if charts[d]<=adj[i]];need(len(visible)==15,'tight native packets')
        R=[g.mm(P[np.ix_(visible,range(15*k,15*k+15))],pencils[k]) for k in range(3)]
        need(g.rank(R[0])==15 and np.array_equal(R[0],R[1]) and np.array_equal(R[0],R[2]),'common full target readout');readouts+=1
    witnesses=certificate[str(h)]['port_certificates'];need(len(witnesses)==45,'all certificate ports');support_sizes=[]
    for index,d in enumerate(ports):
        viewers=[i for i in views if charts[d]<=adj[i]];need(bool(viewers),'native audience at every physical port')
        C=np.vstack([constraints[i] for i in viewers]);ell=P[index:index+1];N=g.null(C)
        need(g.rank(C)==44 and N.shape==(45,1) and g.rank(np.vstack([N.T,ell]))==1 and not np.any(g.mm(C,ell.T)),'complete one-dimensional port quotient')
        w=witnesses[index];need(w['D']==d and w['native_audience']==viewers and w['canonical_packet']==ell[0].tolist(),'actual certificate binding')
        chosen=w['witness_receivers'];need(set(chosen)<=set(viewers) and len(chosen)==len(set(chosen)),'native supporting audience')
        SC=np.vstack([stored_constraints[i] for i in chosen]);rows=w['constraint_minor_rows'];cols=w['constraint_minor_columns']
        need(len(rows)==len(set(rows))==len(cols)==len(set(cols))==44 and g.rank(SC[np.ix_(rows,cols)])==44,'independently checked literal nonzero44 minor')
        support_sizes.append(len(chosen));total+=1
        bad=ell.copy();bad[0,0]^=1
        if np.any(g.mm(C,bad.T)):mutation_failures+=1
    need(g.rank(P)==expected,'joint quotient rank')
    if h==642:
        kernel=np.zeros((45,1),dtype=np.uint8);kernel[[0,15,30]]=1;need(not np.any(g.mm(P,kernel)) and g.rank(np.vstack([P,np.eye(45,dtype=np.uint8)[0:1]]))==45,'exact lost line and complementary field')
    counts.append({'H':h,'native_receivers':len(views),'port_quotient_ranks':[1]*45,'joint_rank':expected,'support_sizes':support_sizes})
need(total==90 and readouts==67 and mutation_failures>0,'full census and coefficient sensitivity')
result={'status':'PASS_ROOT_FULL45_NATIVE_PORT_RIGIDITY','physical_ports':90,'native_readouts':67,'constraint_rank_each':44,'joint_ranks':[45,44],'minimum_H642_extra_fields_bank3840':16,'centres':counts,'damaged_packet_constraints_detected':mutation_failures,'new_author_code_imported':False,'arbitrary_nonlinear_H_functions_proved_by_translation_argument':True,'all_tensor_copy_mixing_allowed':True,'changed_sources_or_nonproper_information_excluded':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],90,67,44,45,44,16,flush=True)
