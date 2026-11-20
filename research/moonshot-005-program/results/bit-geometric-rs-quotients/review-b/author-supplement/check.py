#!/usr/bin/env python3
"""Bind the frozen 99-source review to the published 111-source manuscript."""
from argparse import ArgumentParser
from collections import Counter
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

PINS={
 'SOURCE-PINS.json':'48bb8a5a65b7ee9b096de62fb545f74791a2d0658b510e41c356229775b267df',
 'author/PROOF.md':'aedb79d7c8409bc89ba6db7c826f3a65ac826a5a4f6f6ff8162e2d5843bcf173',
 'author/check.py':'9b083e799622afa55d7be0fd36f76c89e5314ecd87f48aad2d7f3f9782c4c007',
 'author/field_identity.py':'048d9f1cc63b947b60a15d968bd943e0a60a948dc7f8696eba08b908d000c2df',
 'author/output/NODES.json':'b14eea36361961fe4788f03e4b4ca885563d41673bc1d21b56cca59f039c991c',
 'author/output/NODE-CHECKS.json':'8aeee87046645cb89f1f44768686cb6b93930c4fb2570b18e2318cab047ed9b2',
 'author/output/RESULT.json':'c80d5a6f335e1b915c0cb70bd646e6e0c9de9c060f6298e2e786a0c49d5746df',
 'author/output/FIELD-IDENTITY.json':'e653cbf857adb880dc787d42f3785fb7082e76c76541506832d5e8af914516b2',
 'review-b/MANIFEST.json':'b2da14ae8158efd6574b78a8f6c5ebc73fe422e2e889df5c415f6531332d05ac',
}

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    return value

def main():
    cli=ArgumentParser(description=__doc__);cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    base=args.repo/'research/moonshot-005-program/results';folder=base/'bit-geometric-rs-quotients';prior=folder/'review-b'
    f=module(prior/'arith.py','frozen_independent_field');geom=module(prior/'geometry.py','frozen_independent_geometry')
    checks=module(prior/'field_checks.py','frozen_independent_field_checks')
    for name,digest in PINS.items():f.need(sha256((folder/name).read_bytes()).hexdigest()==digest,'author-binding pin '+name)
    frozen=json.loads((prior/'MANIFEST.json').read_bytes())
    for name,digest in frozen['files'].items():f.need(sha256((prior/name).read_bytes()).hexdigest()==digest,'original scientific review bytes unchanged '+name)
    for name,item in json.loads((folder/'SOURCE-PINS.json').read_bytes())['files'].items():
        raw=(args.repo/name).read_bytes();f.need(len(raw)==item['bytes'] and sha256(raw).hexdigest()==item['sha256'],'published source pin '+name)
    old_raw=gzip.decompress((prior/'NODE-WITNESSES.json.gz').read_bytes())
    f.need(old_raw==(folder/'author/output/NODE-CHECKS.json').read_bytes(),'all ninety-nine earlier tables and rank receipts preserved byte for byte')
    old={r['anchor']:r for r in json.loads(old_raw)}
    Q,blocks,polynomials,field=checks.verify(f)
    ctx=geom.reconstruct(json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())),
                         json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_bytes()),f)
    sources=json.loads((folder/'author/output/NODES.json').read_bytes());seen=set();native_views=0;summaries=[]
    for row in sources:
        j=row['anchor'];f.need(j in range(111) and j not in seen,'one table for every native donor');seen.add(j)
        source=geom.assignment(ctx,row,f,Q)
        f.need({int(r):v for r,v in row['receiver_parameters'].items()}==source.receivers,'all sixty-three literal geometric receiver parameters')
        if j in old:
            f.need(row['base_H']==old[j]['base_H'] and row['nodes']==old[j]['nodes'],'published source labels equal the independently reviewed source')
        count=sum(r<111 for r in source.views);native_views+=count
        summaries.append({'anchor':j,'geometric_views':63,'native_views':count,'base_H':source.base_H})
    f.need(seen==set(range(111)) and 63*len(sources)==6993 and native_views==6470,'complete all111 geometric and native source-view census')
    published_field=json.loads((folder/'author/output/FIELD-IDENTITY.json').read_bytes())
    f.need(len(published_field['blocks'])==63 and published_field['span_rank']==7,'published global block-polynomial span')
    for row in published_field['blocks']:
        v=row['v'];f.need(row=={'v':v,'q':f.q6(v),'roots':list(blocks[v]),'polynomial':list(polynomials[v])},'all literal published field-block coefficients')
    terms={'0':[[7,1],[16,1],[34,1],[61,1]],'1':[[6,1]],'2':[[14,1]],'4':[[30,1]],
           '5':[[2,1]],'8':[[62,1]],'14':[[2,1]],'16':[[0,1]]}
    f.need(published_field['coefficients']==terms,'complete sparse coefficient formula')
    subfield={x for x in range(64) if f.power(x,8)==x};norms=Counter(f.power(x,9) for x in range(1,64))
    f.need(len(subfield)==8 and set(norms)==subfield-{0} and set(norms.values())=={9},'norm to GF8 has nine nonzero preimages')
    trace=lambda x:x^f.power(x,2)^f.power(x,4)
    f.need(sum(trace(x)==0 for x in subfield-{0})==3 and all(f.q6(x)==trace(f.power(x,9)) for x in range(64)),
           'binary trace of the field norm')
    f.need(all(len(set(Q)&{a^v for a in Q})==12 for v in range(1,64)),'all sixty-three quadratic difference-set intersections')
    author=json.loads((folder/'author/output/RESULT.json').read_bytes())
    f.need(author=={'status':'PASS_GEOMETRIC_QUADRIC_RS_QUOTIENTS','source_donors':111,'geometric_source_views':6993,
                   'native_source_views':6470,'anchor_certificates':99,'selected_and_all_native_propagations':2970,
                   'propagation_span':5,'physical_source_word':False,'complete_H_word':False,'new_complete_kappa':False},
           'entire published source-scope receipt')
    result={'status':'PASS_ALL111_AUTHOR_BINDING_SUPPLEMENT','source_pins':PINS,'previous_review_bytes_unchanged':True,
            'original99_receipt_identical':True,'source_donors':111,'geometric_source_views':6993,'native_source_views':6470,
            'new_source_tables':sorted(set(range(111))-set(old)),'field_blocks_verified':63,'field_centres_verified':28,
            'field_pairs_verified':378,'norm_fibre_size':9,'nonzero_trace_zero_GF8_elements':3,
            'all_nonzero_quadratic_difference_intersections':12,'sources':summaries,
            'physical_singleton_input_word_claim':False,'Hermite_claim':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','source_donors','geometric_source_views','native_source_views')},sort_keys=True),flush=True)

if __name__=='__main__':main()
