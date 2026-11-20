#!/usr/bin/env python3
"""Independent raw Clifford equations from direct native off-node products.
Reuses C field/native-root arithmetic; no B scaffold or U constructor.
"""
import argparse,gzip,hashlib,importlib.util,json
from collections import defaultdict
from pathlib import Path
import numpy as np

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    base=args.repo/'research/moonshot-005-program/results';package=Path(__file__).resolve().parents[1];review=package/'root-review'
    for path,digest in json.loads((review/'PINS.json').read_text()).items():need(hashlib.sha256((args.repo/path).read_bytes()).hexdigest()==digest,'pinned '+path)
    author=package/'author-b'
    for path,digest in json.loads((author/'MANIFEST.json').read_text())['files'].items():need(hashlib.sha256((author/path).read_bytes()).hexdigest()==digest,'frozen author '+path)
    spec=importlib.util.spec_from_file_location('separate_C_arithmetic',base/'bit-coupled-native-geometric-cycle-source/review-c/check.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
    L=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());roots=C.roots_from_files(L,B)
    H=[set(x)for x in L['A2']];D=[set(x)for x in L['D4']];adj=[{j for j,y in enumerate(roots)if j!=i and not C.b(x,y)}for i,x in enumerate(roots)]
    shared=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text());nodes=shared['H_nodes'];prm={int(j):{int(i):v for i,v in row.items()}for j,row in shared['receiver_parameters'].items()}
    singletons={next(iter(P&set(range(111))))for P in H if len(P&set(range(111)))==1};ordinary=set(range(111))-singletons-{10};centres=[263,4,5,6,7,8]
    generators=[]
    for k in range(4):
        create=np.zeros((16,16),dtype=np.uint8);contract=create.copy()
        for s in range(16):
            if not s&(1<<k):create[s|(1<<k),s]=1
            else:contract[s^(1<<k),s]=1
        generators.extend([create,contract])
    G=[]
    for v in range(256):
        g=np.zeros((16,16),dtype=np.uint8)
        for bit in range(8):
            if v&(1<<bit):g^=generators[bit]
        G.append(g)
    I=np.eye(16,dtype=np.uint8)
    for v in range(256):need(np.array_equal(C.mm(G[v],G[v]),C.q(v)*I),'all Clifford squares')
    for a in range(8):
        for b in range(8):need(np.array_equal(C.mm(generators[a],generators[b])^C.mm(generators[b],generators[a]),C.b(1<<a,1<<b)*I),'basis anticommutators')
    complement=np.eye(16,dtype=np.uint8)[[s^15 for s in range(16)]]
    for v in range(256):need(np.array_equal(C.mm(C.mm(complement,G[v]),complement),G[v].T),'one common transpose conjugation')
    exits={h:defaultdict(list)for h in centres}
    for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase,owner,coordinate,h,d,*_=json.loads(line)
        if h in exits:exits[h][d].extend((((phase=='Y')*111+owner)*480+coordinate)*8+lane for lane in range(8))
    def polynomial(zeros):
        z=np.array([1],dtype=np.uint8)
        for a in zeros:
            y=np.zeros(len(z)+1,dtype=np.uint8);y[:-1]^=C.M[a,z];y[1:]^=z;z=y
        return z
    fibres={};local=[];receiver_counts=[];kernel_checks=0
    for h in centres:
        donors=sorted(H[h]);need(H[h]<=ordinary,'ordinary identity donors');receivers=[i for i in range(111)if i!=80 and H[h]<=adj[i]];receiver_counts.append(len(receivers));ports=exits[h];holders=[x for row in ports.values()for x in row]
        need(len(ports)==45 and {len(x)for x in ports.values()}=={16} and len(holders)==len(set(holders))==720,'literal720/45/16 cut')
        need(all(sum(len(row)for d,row in ports.items()if D[d]<=adj[i])==240 for i in receivers),'literal240 receiver cuts')
        cores={}
        for j in donors:
            stars=[p for p,P in enumerate(H)if j in P];need(len(stars)==28 and len({nodes[p]for p in stars})==28,'shared28 source nodes')
            extension={0:np.zeros(16,dtype=np.uint8)}
            for i in receivers:
                visible=[p for p in stars if H[p]<=adj[i]];need(h in visible and len(visible)==16,'actual sixteen-plane view')
                off=[nodes[p]for p in visible if p!=h];need(len(set(off))==15,'fifteen distinct off-nodes');v=prm[j][i];need(v!=0,'nonzero parameter');u=C.M[C.M[v,v],polynomial(off)];fibres[h,j,i]=u;kernel_checks+=1
                for a in off:
                    value=0
                    for coefficient in reversed(u):value=int(C.M[value,a])^int(coefficient)
                    need(value==0,'direct off-node root')
                value=0
                for coefficient in reversed(u):value=int(C.M[value,nodes[h]])^int(coefficient)
                need(value!=0,'central quotient injective on fibre')
                if v not in extension:
                    old=list(extension.items())
                    for w,z in old:extension[w^v]=z^u
            need(len(extension)==64,'native binary parameters span six')
            for i in receivers:need(np.array_equal(extension[prm[j][i]],fibres[h,j,i]),'direct products give one binary-linear fibre map')
            core=np.array([extension[1<<bit]for bit in range(6)],dtype=np.uint8).T;need(C.rank(core)==6,'injective field-linear extension');cores[j]=core
        a=donors[0]
        for other in donors[1:]:
            values=[prm[a][i]for i in receivers];need(len(values)==len(set(values)),'native parameter uniqueness');V=set(values);graph={v:{w for w in V if w!=v and v^w in V}for v in V};reached={values[0]};todo=list(reached)
            while todo:
                fresh=graph[todo.pop()]-reached;reached|=fresh;todo.extend(fresh)
            need(reached==V,'native additive triangle graph connected')
            linear={0:0}
            for i in receivers:
                v,w=prm[a][i],prm[other][i]
                if v not in linear:
                    old=list(linear.items())
                    for x,y in old:linear[x^v]=y^w
            need(len(linear)==64 and all(linear[prm[a][i]]==prm[other][i]for i in receivers),'actual parameter transport is binary linear')
            J=np.array([[(linear[1<<c]>>r)&1 for c in range(6)]for r in range(6)],dtype=np.uint8)
            need(np.array_equal(C.mm(J,J)^J,np.eye(6,dtype=np.uint8)),'J order three');need(C.rank(np.vstack([np.eye(6,dtype=np.uint8).reshape(36),J.reshape(36)]))==2,'I J independent over GF64')
            need(np.array_equal(cores[a],cores[other]),'same normalized Ucore at each centre')
            prod=C.mm(G[roots[a]],G[roots[other]]);need(np.array_equal(C.mm(prod,prod)^prod,I),'Clifford pair order three')
            local.append({'H':h,'donors':[a,other],'receivers':len(receivers),'parameter_span':6,'Ucore_rank':6,'graph_connected':True,'I_J_span_rank':2})
    witness=json.loads(gzip.decompress((author/'output/WITNESSES.json.gz').read_bytes()));labels=witness['selected_equation_rows'];need(len(labels)==256,'256 original equation labels');rows=[]
    for label in labels:
        h,i=label['H'],label['receiver'];a,b=label['donors'];q=label['output_coordinate'];need(h in centres and a==min(H[h])and b in H[h]-{a}and i<111 and i!=80 and H[h]<=adj[i]and 0<=q<16,'actual labelled native equation')
        row=np.outer(G[roots[a]][q],fibres[h,a,i])^np.outer(G[roots[b]][q],fibres[h,b,i]);rows.append(row.reshape(256))
    matrix=np.array(rows,dtype=np.uint8);need(np.array_equal(matrix,np.asarray(witness['row_basis'],dtype=np.uint8)),'all selected raw coefficients independently reconstructed');need(C.rank(matrix)==256,'independent full rank contradiction')
    bad=matrix.copy();bad[-1]=bad[0];need(C.rank(bad)==255,'duplicate equation negative control')
    result={'status':'PASS_INDEPENDENT_PROJECTIVE_CLIFFORD_SCAFFOLD','centres':centres,'native_receivers_per_centre':receiver_counts,'direct_off_H_polynomial_fibres':kernel_checks,'local_projective_guards':local,'independent_raw_equation_rank':256,'duplicate_row_rank':255,'no_author_scaffold_or_U_constructor_used':True,'reused_separate_C_arithmetic':True,'arbitrary_donor_gauges_excluded':False,'feedback_excluded':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],6,256,len(local),kernel_checks,flush=True)
if __name__=='__main__':main()
