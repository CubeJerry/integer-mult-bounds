#!/usr/bin/env python3
"""New source-to-cut reconstruction; imports only this package's field code."""
import argparse,gzip,hashlib,json
from pathlib import Path
from pack import T,INV,rank,add

def read(path):
    raw=path.read_bytes()
    if path.suffix=='.gz':raw=gzip.decompress(raw)
    return json.loads(raw),hashlib.sha256(raw).hexdigest()
def mm(a,b):
    out=[[0]*len(b[0]) for _ in a]
    for i,row in enumerate(a):
        for k,v in enumerate(row):
            if v:
                for j,w in enumerate(b[k]):out[i][j]^=T[v][w]
    return out
def inv(a):
    n=len(a);rows=[r[:]+[int(i==j) for j in range(n)] for i,r in enumerate(a)]
    assert all(len(r)==2*n for r in rows)
    for j in range(n):
        k=next(k for k in range(j,n) if rows[k][j]);rows[j],rows[k]=rows[k],rows[j]
        tab=T[INV[rows[j][j]]];rows[j]=[tab[v] for v in rows[j]]
        for k in range(n):
            if k!=j and rows[k][j]:
                tab=T[rows[k][j]];rows[k]=[x^tab[y] for x,y in zip(rows[k],rows[j])]
    eye=[[int(i==j) for j in range(n)] for i in range(n)];out=[r[n:] for r in rows]
    assert mm(a,out)==eye and mm(out,a)==eye
    return out
def power(a,n):
    out=1
    for _ in range(n):out=T[out][a]
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--source',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
    p=a.repo/'research/moonshot-005-program/results'
    layout,lpin=read(p/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz')
    partition,ppin=read(p/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz')
    src,spin=read(a.source/'output/ALL-CLASSES-SOURCE.json.gz')
    assert (lpin,ppin,spin)==('9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','2c3fd50f5b9e1e12f25b48baaaaf15d92690af9ac3685a7b29ce7cc982c8fc25','362a7ea7798acae4c9d92d2035f41e016aae9d9f8af8a127c6bfd359026410af')
    roots=layout['root_table'];H=list(map(set,layout['A2']));D=list(map(set,layout['D4']));receiver=10;donors=[29,36,77]
    orth=[{j for j,v in enumerate(roots) if sum(x*y for x,y in zip(u,v))==0} for u in roots]
    native=[[int(i==j or j in orth[i]) for j in range(111)] for i in range(111)];outside=[j for j in range(111) if j not in orth[receiver]]
    assert rank(native)==9 and rank([[row[j] for j in outside] for row in native])==9
    maps={(c,j,h):m for c,j,h,m in src['source_maps']};V=[[power(z,k) for k in range(9)] for z in range(1,10)];spaces={};labels={};checks=[]
    for c in range(5):
        decoders={};boundary={};port_ids={}
        for jpos,j in enumerate(donors):
            hs=[h for h,lines in enumerate(H) if j in lines and lines<=orth[receiver]];assert len(hs)==16
            source_inverse=inv([row for h in hs for row in maps[c,j,h]])
            for pos,h in enumerate(hs):
                ports=partition['classes'][str(h)][c];indices=[k for k,d in enumerate(ports) if D[d]<=orth[receiver]];assert len(indices)==3
                slot=sorted(H[h]).index(j);local=[[V[k][3*slot+t] for t in range(3)] for k in indices]
                decoder=mm([row[3*pos:3*pos+3] for row in source_inverse],inv(local))
                if h in decoders:assert decoders[h]==decoder
                decoders[h]=decoder;port_ids[h]=[ports[k] for k in indices]
                rows=boundary.setdefault(h,[[0]*144 for _ in range(3)]);emission=mm(local,maps[c,j,h])
                for k,row in enumerate(emission):rows[k][48*jpos:48*jpos+48]=row
        full=[row for h in sorted(boundary) for row in boundary[h]];assert len(full)==135 and rank(full)==135
        target=[[0]*144 for _ in range(48)]
        for h,decoder in decoders.items():
            term=mm(decoder,boundary[h]);target=[[x^y for x,y in zip(r,s)] for r,s in zip(target,term)]
            for k,d in enumerate(port_ids[h]):
                vector=[0]*240;vector[48*c:48*c+48]=[row[k] for row in decoder]
                spaces.setdefault(d,[]).append(vector);labels.setdefault(d,[]).append([h,c,k])
        assert target==[[int(j==k%48) for k in range(144)] for j in range(48)]
        checks.append([c,135,144,rank(target)])
    selected=[640,726,845,81,88,93,118,123,138,395,442,443,473,558,564,605,663,672,693,696,706,708,717,771,774,803,835,849,865,937,974,991,1053]
    individual=[rank(spaces[d]) for d in selected];union=[v for d in selected for v in spaces[d]]
    assert individual==[9,9,9]+[7]*30 and rank(union)==sum(individual)==237
    assert rank([v for d in selected[:3] for v in spaces[d]])==27
    assert rank([v for d in [640,640,845] for v in spaces[d]])==18
    right={d:[k for k,lines in enumerate(H) if receiver in lines and lines<=D[layout['dual_D4'][d]]] for d in selected};assert all(len(v)==4 for v in right.values())
    local=[];helper=[]
    for d in selected:
        basis={}
        for v in spaces[d]:add(basis,v)
        independent=[basis[k] for k in sorted(basis)];local.extend(independent[:4]);helper.extend(independent[4:])
    assert rank(local)==132 and rank(helper)==105 and rank(local+helper)==237 and rank(local+helper[:-1])==236
    result={'status':'PASS_TRIANGLE_MULTIPLE_MIDDLE_REPAIR_FLOOR','source_pins':{'layout':lpin,'partition':ppin,'source':spin},'receiver':10,'classes':checks,'middles':selected,'right_planes':right,'individual_ranks':individual,'union_rank':237,'original_capacity':132,'auxiliary_floor_per_stripe':105,'normalized_floor':'7/16','first_three':{'middles':selected[:3],'rank':27,'capacity':12,'auxiliary_floor':15},'canonical_rank_outside_foreign_set':9,'controls':{'duplicate_middle_rank':18,'matching_relaxation_helper_rank':105,'one_helper_removed_rank':236},'predecessor_code_imported':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RECONSTRUCTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (a.out/'WITNESS.json.gz').write_bytes(gzip.compress(json.dumps({'spaces':{str(d):spaces[d] for d in selected},'labels':{str(d):labels[d] for d in selected}},separators=(',',':')).encode(),mtime=0))
    print('PASS_TRIANGLE_MULTIPLE_MIDDLE_REPAIR_FLOOR rank237 capacity132 auxiliary105')
if __name__=='__main__':main()
