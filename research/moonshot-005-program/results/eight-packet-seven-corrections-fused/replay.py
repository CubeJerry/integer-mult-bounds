#!/usr/bin/env python3
"""Integration replay of the fused word using the pinned parent exact interpreter.

This reuses source-coupling's seven-correction replay explicitly; it is not an
independent proof engine. The root generic fusion rewrite has a separate review.
"""
import argparse
from fractions import Fraction as F
import gzip,hashlib,importlib.util,json
from pathlib import Path

SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='ae7a86a02b853f3166c6727d66e0a2440b0e5e4e8e3a7d35e69dae029d66942d'
VERIFIER='0367ae2b674de218acaad4528a5efb1ff488b136f5a2cec867829ff1ea4adfaa'

def need(ok,message):
    if not ok:raise ValueError(message)

def main(a):
    sb=a.source.read_bytes();need(hashlib.sha256(sb).hexdigest()==SOURCE,'source pin');w=json.loads(gzip.decompress(sb))
    parent_blob=(a.parent/'WORD.json.gz').read_bytes();need(hashlib.sha256(parent_blob).hexdigest()==PARENT,'parent pin');parent=json.loads(gzip.decompress(parent_blob))
    vp=a.parent/'verify.py';need(hashlib.sha256(vp.read_bytes()).hexdigest()==VERIFIER,'reused exact parent verifier pin')
    spec=importlib.util.spec_from_file_location('pinned_seven_correction_parent',vp);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    cb=(a.parent/'INPUT-CONTROLLERS.json').read_bytes();need(hashlib.sha256(cb).hexdigest()==m.CONTROLLER_PIN,'controller pin');cert=json.loads(cb)
    pb=gzip.decompress((a.parent/'INPUT-PREFIX.json.gz').read_bytes());need(hashlib.sha256(pb).hexdigest()==m.PREFIX_PIN,'prefix pin');p=json.loads(pb)
    wb=a.word.read_bytes();word=json.loads(gzip.decompress(wb));need(word['parent_word_sha256']==PARENT,'fused parent identity')
    need(word['initial']==parent['initial'] and word['private_role_map']==parent['private_role_map'] and word['owned_fields']==parent['owned_fields'],'unchanged physical bank')
    T,Z,decoders,scalings,guards=m.source_certificate(w,cert)
    raw={int(r):q for r,q in p['difference_role_map'].items()};targets,q,weights,residuals=m.prefix_targets(w,p,raw)
    corrections={x['receiver']:{int(d):weights[x['receiver']-112]*F(c) for d,c in x['resulting_private_row'].items()} for x in decoders}
    need(word['corrections']=={str(y):m.ser(row) for y,row in corrections.items()},'unchanged joint correction matrix')
    caches={int(d):r for d,r in parent['donor_caches'].items()};bill=m.execute(w,p,word,raw,T,Z,targets,q,corrections,caches)
    need(bill['instructions']==74757 and bill['opcode_counts']['MOVE']==6725 and bill['peak_owned']==43 and bill['owned_lifetimes']==67,'exact fused word bill')
    record=dict(status='PASS_FUSED_SEVEN_CORRECTION_ALL1880_INPUT_INTEGRATION_REPLAY',source_sha256=SOURCE,parent_sha256=PARENT,reused_parent_verifier_sha256=VERIFIER,word_sha256=hashlib.sha256(wb).hexdigest(),word_decompressed_sha256=hashlib.sha256(gzip.decompress(wb)).hexdigest(),independent_physical_inputs=1880,common_all1480_rows_restored=True,all400_final_private_rows_and_charts_checked=True,private_difference_inverse_checked=True,seven_selected_residuals_zero=True,other4985_residual_coefficients_unchanged=True,COPY_guards=guards,bill=bill,method='Pinned parent full rational interpreter reused on the actual fused literal word. Integration replay, not a new independent review engine.',scope='Partial firstY correction only; remaining4985 residuals, private reverse duties and foundational supplier/compiler services remain open; no new kappa.')
    a.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='bill'},indent=2));print(json.dumps({k:v for k,v in bill.items() if k!='peak_increase_events'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
