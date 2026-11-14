#!/usr/bin/env python3
from pathlib import Path
import gzip,json,hashlib,importlib.util,sys,argparse
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38','R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','GEOMETRY.json':'e8e48d62be188293677d5c2f7c9a1b104e944bff8ac97669fbaa9a70b41613c6'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def module(name):
 path=HERE/'source'/name;need(hashlib.sha256(path.read_bytes()).hexdigest()==PINS[name],'source pin')
 spec=importlib.util.spec_from_file_location('physical112_'+name[:-3],path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
def load(name):
 raw=(HERE/'source'/name).read_bytes();need(hashlib.sha256(raw).hexdigest()==PINS[name],'source pin '+name);return json.loads(gzip.decompress(raw)if name.endswith('.gz')else raw)
def main(out):
 c=module('clifford_exact.py');v=module('native_verify.py');w=load('R0-WORD.json.gz');g=load('GEOMETRY.json')
 ports=w['logical_involution']['ports'];roles=w['logical_involution']['role_map'];H=c.fourier(9);records=[]
 for h in ports:
  q=g['normal_by_port'][str(h)];ix=int(roles['X'][str(h)]);iy=int(roles['Y'][str(h)])
  L=w['frames'][w['initial'][ix]];F=w['frames'][w['final'][iy]];need(L==[q]and len(F)==8,'actual source boundary')
  S=c.canonical_frame(9,tuple(L));T=c.canonical_frame(9,tuple(F));Q=c.cgate(9,q)
  Nx=Q.adjoint().then(S);Ny=T.adjoint().then(Q.adjoint()).then(H)
  rx,_=c.lower_child(Nx);ry,_=c.lower_child(Ny)
  need(rx['rank']==ry['rank']==0,'ordinary actual boundary normalization '+str(h))
  v.equal(v.recipe(rx),Nx.circuit,'actual line normalizer')
  v.equal(v.recipe(ry),Ny.circuit,'actual facet normalizer')
  v.equal(S.then(Q).circuit,Q.then(S).circuit,'line chart commutes normalized Q')
  v.equal(Nx.then(Q).circuit,Q.then(Nx).circuit,'ordinary line normalizer commutes Q')
  records.append(dict(port=h,normal=q,line=L,facet=F,line_normalizer=rx,facet_normalizer=ry))
 result=dict(status='PASS_112_ACTUAL_ORDINARY_BOUNDARY_NORMALIZERS',source_pins=PINS,records=records,
  scope='Finite exact signed Clifford recipes for all112 actual boundaries. All-width tensor lifting and physical caller consequences are in PROOF.md; no new kappa.')
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=HERE/'NORMALIZERS.json');main(a.parse_args().out)
