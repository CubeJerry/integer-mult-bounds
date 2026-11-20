#!/usr/bin/env python3
"""Independent native shared-D cut, including actual early owner rows."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,why):
    if not ok:raise ValueError(why)
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
here=Path(__file__).resolve().parent;base=args.repo/'research/moonshot-005-program/results'
for path,want in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((args.repo/path).read_bytes()).hexdigest()==want,'pin '+path)
s=importlib.util.spec_from_file_location('independent_geometry',base/'bit-coupled-native-geometric-cycle-source/review-c/check.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
L=read(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());roots=g.roots_from_files(L,B)
H=[set(a) for a in L['A2']];D=[set(a) for a in L['D4']];adj=[{j for j,y in enumerate(roots) if j!=i and not g.b(x,y)} for i,x in enumerate(roots)]
parent=here.parents[1]/'author';literal=read(parent/'output/COEFFICIENTS.json.gz');early=read(parent/'output/EARLY.json.gz');auth=read(here.parent/'author/output/WITNESS.json.gz')
maps={int(j):{int(h):np.array(Q,dtype=np.uint8) for h,Q in table.items()} for j,table in literal['source_maps'].items()}
routes=[json.loads(line) for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()]
quota=Counter((r[1],r[3]) for r in routes if r[0]=='X');E={};labels={};owner_index={}
for j in [0,45]:
    E[j]=np.array(early['full'][str(j)]['matrix'],dtype=np.uint8);labels[j]=[tuple(x) for x in early['full'][str(j)]['row_owners']];owner_index[j]={owner:r for r,(h,owner) in enumerate(labels[j])}
    need(E[j].shape==(480,480) and len(owner_index[j])==480 and g.rank(E[j])==480,'actual invertible source basis')
    hist=Counter()
    for h,Q in maps[j].items():
        rs=[r for r,(a,owner) in enumerate(labels[j]) if a==h];q=quota[j,h];hist[q]+=1;pair=np.block([[Q,np.zeros_like(Q)],[np.zeros_like(Q),Q]])
        need(len(rs)==q and q in [15,30] and g.rank(np.vstack([pair,E[j][rs]]))==30,'all actual early emissions factor through two quotients')
    need(hist=={15:24,30:4},'no singleton extra source rows')
canonical=np.array([[int(j==i or j in adj[i]) for j in range(111)] for i in range(111)],dtype=np.uint8);rp=g.echelon(canonical.T)[1];need(len(rp)==9,'canonical rank9');Cb=canonical[rp]
for h in [263,642]:need(len([r for r in routes if r[3]==h])==90 and all(r[0]=='X' for r in routes if r[3]==h),'frozen H has no late proper slots')
data={h:literal['H'][str(h)] for h in [263,642]};P={h:np.array(data[h]['word'],dtype=np.uint8) for h in data};fibres={}
def isolate(i,d):
    if i not in fibres:
        vis=sorted(h for h in maps[0] if H[h]<=adj[i]);need(len(vis)==16,'sixteen source planes');off=np.vstack([maps[0][h] for h in vis if h!=263]);K=g.null(off);need(K.shape==(240,15),'fresh whole fibre')
        rows=[q for q,a in enumerate(data[263]['ports']) if D[a]<=adj[i]];need(len(rows)==15,'fifteen H packets');R=g.mm(P[263][np.ix_(rows,range(15))],g.mm(maps[0][263],K));need(g.rank(R)==15,'full source0 readout');fibres[i]=(vis,rows,g.mm(K,g.invert(R)))
    vis,rows,Z=fibres[i];ports=[data[263]['ports'][r] for r in rows];k=ports.index(d);return Z[:,k:k+1],vis,rows
def functional(other):
    q=data[642]['ports'].index(other);s=data[642]['donors'].index(45);return g.mm(P[642][q:q+1,15*s:15*s+15],maps[45][642])
def physical_transfer(h,j):
    ph=data[h]['physical'];rows=np.zeros((90,480),dtype=np.uint8)
    for r,(donor,owner) in enumerate(ph['input_owners']):
        if donor==j:rows[r]=E[j][owner_index[j][owner]]
    return g.mm(np.array(ph['word'],dtype=np.uint8),rows)
physical={263:physical_transfer(263,0),642:physical_transfer(642,45)}
def output_rows(h,port):
    ph=data[h]['physical'];index={tuple(a):r for r,a in enumerate(ph['input_owners'])};return [index[tuple(o['owner'])] for o in ph['output_owners'] if o['D']==port]
receipts=[]
for i,d,other,want in [(4,733,825,20),(6,1509,302,30)]:
    v,vis,rows=isolate(i,d);lam=functional(other);need(int(g.mm(lam,v)[0,0])==want,'nonzero cross-D pairing')
    record=next(z for z in auth['minimal_witnesses'] if z['receiver']==i);need(record['direction']==v[:,0].tolist() and record['functional']==lam[0].tolist(),'fresh inverse agrees with literal witness')
    need(D[d]<=adj[i] and D[other]<=adj[i] and d!=other and 45 not in H[263],'distinct visible ports and separate sources');Z=np.block([[v,np.zeros_like(v)],[np.zeros_like(v),v]])
    for h in vis:
        if h==263:continue
        need(not np.any(g.mm(maps[0][h],v)),'off-H quotient unchanged');er=[r for r,(a,owner) in enumerate(labels[0]) if a==h];need(not np.any(g.mm(E[0][er],Z)),'all actual off-H early fields unchanged')
    for port in [data[263]['ports'][r] for r in rows]:
        image=g.mm(physical[263][output_rows(263,port)],Z);need(np.array_equal(image,np.eye(2,dtype=np.uint8) if port==d else np.zeros((2,2),dtype=np.uint8)),'actual two-half isolated H output')
    need(np.array_equal(g.mm(physical[642][output_rows(642,other)],Z),np.eye(2,dtype=np.uint8)*want),'actual comparison has full rank2')
    vis45=sorted(h for h in maps[45] if H[h]<=adj[i]);need(len(vis45)==16 and g.rank(np.vstack([maps[45][h] for h in vis45]))==240,'comparison full source cut')
    boundary=[(r,x) for r,x in enumerate(routes) if x[3] in vis45 and D[x[4]]<=adj[i]];counts=Counter(x[4] for _,x in boundary);need(len(boundary)==480 and len(counts)==60 and set(counts.values())=={8},'complete two-wave boundary')
    outputs=[(r,x) for r,x in enumerate(routes) if x[4]==d and x[5] is not None and i in H[x[5]]];ks=sorted({x[5] for _,x in outputs});phases=Counter(x[0] for _,x in outputs)
    need(len(outputs)==8 and len(ks)==4 and all(sum(x[5]==k for _,x in outputs)==2 for k in ks),'actual proper capacity')
    need([r for r,x in outputs]==record['proper_output_route_ids'] and [x for r,x in outputs]==record['proper_output_routes'],'actual original holders and route IDs')
    need(phases==({'X':3,'Y':5} if d==733 else {'X':4,'Y':4}),'both early and late outputs counted')
    for x in routes:
        if x[5] is not None and i in H[x[5]]:need(D[x[4]]<=adj[i] and (x[3] is None or H[x[3]]<=D[x[4]]),'nested proper route excludes outside-foreign sources')
    outside=[j for j in range(111) if j not in adj[i]];need(g.rank(Cb[:,outside])==9,'outside inputs neutralize canonical records')
    if d==733:need(not np.any(v[:48]) and not np.any(lam[:,:48]),'complement-only witness')
    else:need(not np.any(v[48:]) and not np.any(lam[:,48:]),'protected-only witness')
    mu=np.zeros((1,240),dtype=np.uint8);pivot=int(np.flatnonzero(v[:,0])[0]);mu[0,pivot]=g.INV[v[pivot,0]];corrected=lam^g.M[want,mu];need(not np.any(g.mm(corrected,v)),'changed functional closes this witness; no full construction inferred')
    receipts.append({'receiver':i,'D':d,'other_D':other,'pairing':want,'proper_K':ks,'early_fields':phases['X'],'late_fields':phases['Y'],'outside_boundary_fields_base':472,'fibre_log64_lower_base':8,'isolated_input_dimension_base':2,'target_log64_lower_base':10,'proper_capacity_base':8,'target_log64_lower_bank3840':80,'proper_capacity_bank3840':64,'canonical_outside_rank':9})
common=sorted(set(data[263]['ports'])&set(data[642]['ports']));need(common==[296,733,825,1509,1852],'five common exits');census=[]
for d in common:
    count=0
    for i in range(111):
        if not D[d]<=adj[i]:continue
        v,_,_=isolate(i,d);others=[port for port in data[642]['ports'] if port!=d and D[port]<=adj[i]];values=[int(g.mm(functional(port),v)[0,0]) for port in others];need(any(values),'gate at every common-D native cut');count+=1
    census.append([d,count])
need(sum(n for d,n in census)==57,'all57 native cuts')
result={'status':'PASS_ROOT_FROZEN_PAIR_SHARED_D_GATE','witnesses':receipts,'common_D_census':census,'all_native_shared_cuts':57,'actual_early_owner_binding':True,'no_singleton_extra_source_rows':True,'both_D_waves_accounted':True,'arbitrary_other_H_D_K_F_functions':True,'no_extra_informative_nonproper_channel_required':True,'different_cut_deficits_added':False,'new_author_code_imported':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],4,733,825,20,6,1509,302,30,57,80,64,flush=True)
