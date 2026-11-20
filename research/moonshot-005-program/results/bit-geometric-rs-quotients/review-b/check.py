#!/usr/bin/env python3
"""Independent geometric-node, sparse-polynomial and native rank-escape audit."""
from argparse import ArgumentParser
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

PINS={
 'geometry':('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'),
 'binary_basis':('bit-clifford-one-evaluation-gate/author/BASIS.json','d2a825f09a4d24a8a0319743ec84bed9b9e6b50656d3105a1c4577ec78fba9ab'),
 'triangle_witnesses':('bit-single-rs-anchor-obstruction/author/WITNESSES.json.gz','c74e4cd954ed1d68d7be46dc35290241558c785ff22c37e25061ecb379f26798'),
 'node_witnesses':('bit-geometric-rs-quotients/review-b/NODE-WITNESSES.json.gz','8aeee87046645cb89f1f44768686cb6b93930c4fb2570b18e2318cab047ed9b2'),
 'old_RS_source':('bit-spread-rs-physical-word/author/rs_source.py','a51189b6d5422ec07fb2fedc822dc856e3277ea8ae0631894c34464419b8c7f9'),
 'old_RS_proof':('bit-spread-rs-physical-word/author/RS-SOURCE.md','432e19d4d11e6068eac7bea94dba459464e804b539634be54824c30f25f7fcae'),
}

def module(name):
    path=Path(__file__).with_name(name+'.py')
    spec=importlib.util.spec_from_file_location('independent_geometric_'+name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    return value

def main():
    cli=ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    f=module('arith');geom=module('geometry');fc=module('field_checks');nc=module('node_checks')
    base=args.repo/'research/moonshot-005-program/results';payload={}
    for key,(name,digest) in PINS.items():
        raw=(base/name).read_bytes()
        if name.endswith('.gz'):raw=gzip.decompress(raw)
        f.need(sha256(raw).hexdigest()==digest,'independent source pin '+key);payload[key]=raw
    Q,blocks,polynomials,field=fc.verify(f)
    print('PASS_SPARSE_FIELD_IDENTITIES_AND_ALL_CENTRE_PAIR_RANKS',flush=True)
    ctx=geom.reconstruct(json.loads(payload['geometry']),json.loads(payload['binary_basis']),f)
    assignments=json.loads(payload['node_witnesses'])
    certificate=json.loads(payload['triangle_witnesses'])['witnesses']
    nodes=nc.verify(ctx,assignments,certificate,f,geom,Q,polynomials)
    print('PASS_ALL_GEOMETRIC_NODE_BINDINGS_AND_NATIVE_PROPAGATION_RANKS',flush=True)
    details=nodes.pop('witnesses');raw=(json.dumps(details,sort_keys=True,separators=(',',':'))+'\n').encode()
    (args.out/'DETAILS.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    field_raw=(json.dumps(field,sort_keys=True,indent=2)+'\n').encode();(args.out/'FIELD-RESULT.json').write_bytes(field_raw)
    result={'status':'PASS_INDEPENDENT_GEOMETRIC_RS_ESCAPE','source_pins':PINS,
            'field_receipt_sha256':sha256(field_raw).hexdigest(),'details_payload_sha256':sha256(raw).hexdigest(),
            'field':{'nodes':28,'blocks':63,'global_block_polynomial_rank':7,'all_fixed_centre_rank':6,
                     'all_common_node_pair_rank':5,'pairs_checked':378},
            'native':nodes,'scalar_bank_dimension':16,'scalar_quotient_dimension':1,
            'extension_scope':'fixed GF64 node and receiver sets; exact ranks persist over every field extension',
            'positive_width_scope':'tensor RS tuple F_R=(1,a_R,...,a_R^15) tensor I_t, every positive integer t',
            'tensor_rank_formulas':{'fixed_centre':'6*t','common_two_node_upper_bound':'5*t','all_certified_native_pairs':'5*t','saturation_needed':'15*t'},
            'tensor_bank_3840_example':{'quotient_width':240,'fixed_centre_span_rank':1440,'common_two_node_span_rank':1200,'saturation_needed':3600},
            'Hermite_jet_rank_claim':False,'physical_source_word_claim':False,'common_H_word_claim':False,
            'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'anchors':99,'selected_and_full_native_tests':2970,
                      'native_two_node_pairs':37422},sort_keys=True),flush=True)

if __name__=='__main__':main()
