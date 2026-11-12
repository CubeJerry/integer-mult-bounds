#!/usr/bin/env python3
"""Check every newly introduced map with pinned lowering and Pauli engines."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from pathlib import Path
PINS={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
def need(q,m):
    if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main(a):
    need(__debug__,'retained phase engines require assertions')
    sourcepath=a.repo/'research/shared-wire-split-composition/data/final.json.gz';sb=sourcepath.read_bytes();need(sha(sb)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin')
    s=json.loads(gzip.decompress(sb));pb=(a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz').read_bytes();need(sha(gzip.decompress(pb))=='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a','parent pin');p=json.loads(gzip.decompress(pb));wb=a.word.read_bytes();w=json.loads(gzip.decompress(wb));frames=s['frames']+[x['frame'] for x in w['additional_charts']]
    need(w['additional_charts'][:len(p['additional_charts'])]==p['additional_charts'],'old charts unchanged')
    def module(name):
        path=a.repo/'research/shared-wire-split-composition/frozen'/name;need(sha(path.read_bytes())==PINS[name],'engine pin');spec=importlib.util.spec_from_file_location('late2_'+name[:-3],path);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);return m
    c=module('clifford_exact.py');v=module('native_verify.py')
    old={(e[2],e[3]) for e in p['program'] if e[0]=='MOVE'};new={(e[2],e[3]) for e in w['program'] if e[0]=='MOVE'};records=[]
    for x,y in sorted(new-old):
        A,B=frames[x],frames[y];recipe,_=c.lower_child(c.canonical_frame(9,tuple(A)).adjoint().then(c.canonical_frame(9,tuple(B))))
        v.equal(v.recipe(recipe),v.adjoint(v.frame(A,9))+v.frame(B,9),'new late2 source map')
        need(recipe['rank']==abs(len(B)-len(A)),'new late2 exact rank')
        records.append({'source':x,'target':y,'source_dimension':len(A),'target_dimension':len(B),'recipe':recipe})
    need(records,'real new maps')
    bad=copy.deepcopy(records[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4;rejected=False
    try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong global phase')
    except ValueError:rejected=True
    need(rejected,'wrong phase rejected')
    result={'status':'PASS_LATE_TWO_INTRODUCED_CHART_MAPS','source_sha256':sha(sb),'parent_payload_sha256':sha(gzip.decompress(pb)),'word_payload_sha256':sha(gzip.decompress(wb)),'engine_pins':PINS,'introduced_maps':records,'wrong_global_phase_rejected':True,'scope':'Pinned exact Clifford lowering with separately implemented signed-Pauli/global-phase equality, not a full physical compiler theorem.'}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'],len(records))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
