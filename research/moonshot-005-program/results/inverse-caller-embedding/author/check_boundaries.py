#!/usr/bin/env python3
"""Fresh signed rank-zero inverses of the actual native boundary adapters."""
import argparse,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,pins):
    p=HERE/'source'/name;need(sha(p)==pins['source/'+name],'engine pin')
    s=importlib.util.spec_from_file_location('inverse_boundary_'+name[:-3],p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);return m
def main(out):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for f,pin in pins.items():need(sha(HERE/f)==pin,'source pin '+f)
    c=module('clifford_exact.py',pins);v=module('native_verify.py',pins)
    w=json.loads(gzip.decompress((HERE/'source/FORWARD.json.gz').read_bytes()));d=w['logical_involution']
    old=json.loads((HERE/'source/NORMALIZERS.json').read_text());records={x['port']:x for x in old['records']}
    H=c.fourier(9);ans=[]
    for h in d['ports']:
        q=int(d['normals'][str(h)]);x=d['role_map']['X'][str(h)];y=d['role_map']['Y'][str(h)]
        L=w['frames'][w['initial'][x]];F=w['frames'][w['final'][y]];a=records[h]
        need(a['normal']==q and a['line']==L and a['facet']==F,'authentic minimal source boundary')
        S=c.canonical_frame(9,tuple(L));T=c.canonical_frame(9,tuple(F));Q=c.cgate(9,q)
        ix=S.adjoint().then(Q);iy=H.adjoint().then(Q).then(T)
        rx,_=c.lower_child(ix);ry,_=c.lower_child(iy)
        need(rx['rank']==ry['rank']==0,'ordinary inverse boundaries')
        v.equal(v.recipe(rx),ix.circuit,'literal inverse NX');v.equal(v.recipe(ry),iy.circuit,'literal inverse NY')
        v.equal(v.recipe(rx),v.adjoint(v.recipe(a['line_normalizer'])),'inverse of pinned line normalizer')
        v.equal(v.recipe(ry),v.adjoint(v.recipe(a['facet_normalizer'])),'inverse of pinned facet normalizer')
        ans.append({'port':h,'normal':q,'line_inverse':rx,'facet_inverse':ry})
    bad=json.loads(json.dumps(ans[0]['line_inverse']));bad['left']['phase']=(bad['left']['phase']+1)%4
    try:v.equal(v.recipe(bad),v.recipe(ans[0]['line_inverse']),'wrong inverse boundary phase');rejected=False
    except ValueError:rejected=True
    need(rejected,'absolute inverse boundary phase control')
    result={'status':'PASS_ALL224_SIGNED_ORDINARY_INVERSE_BOUNDARIES','source_pins':pins,'ports':112,
      'new_gaussian_calls':0,'all_inverse_pairs_checked':224,'recipes':ans,'wrong_global_phase_rejected':True,
      'scope':'Actual inverse canonical-boundary recipes with absolute phase. Width lift tensors each factor and its global phase; uniform tape/compiler assumptions retained.'}
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output/BOUNDARIES.json');a=p.parse_args();main(a.output)
