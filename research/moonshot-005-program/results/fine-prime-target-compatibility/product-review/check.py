#!/usr/bin/env python3
"""Replay the pinned PR's native Gaussian multiplier and audit its original-coordinate rounding."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import prod
from pathlib import Path
import subprocess
import sys
import io
import tempfile
import tarfile
from types import SimpleNamespace

HEAD='4f0c67d5bb41d4af5501dcd40b3b388b35e0ff02'
SUBDIR='research/fine-prime-gaussian-product'


def require(ok,message):
    if not ok:raise ValueError(message)


def encode(x):return f'{x.numerator}/{x.denominator}'


def digits(bits,b,length):
    return [int(bits[max(0,j-b):j],2) for j in range(len(bits),0,-b)]+[0]*length


def schoolbook(left,right,b,size):
    a=digits(left,b,0);c=digits(right,b,0);out=[0]*size
    for i,x in enumerate(a):
        for j,y in enumerate(c):out[i+j]+=x*y
    return out


def run(repo,source,with_interior):
    manifest=subprocess.check_output(['git','-C',str(repo),'ls-tree','-r',HEAD+':'+SUBDIR],text=True).splitlines()
    pins={}
    for line in manifest:
        metadata,name=line.split('\t',1);blob=metadata.split()[2];local=source/name;raw=local.read_bytes()
        require(hashlib.sha1(f'blob {len(raw)}\0'.encode()+raw).hexdigest()==blob,'authentic upstream tree '+name);pins[name]=blob
    sys.path.insert(0,str(source.resolve()));import product as up;import recovery_radius as radius;from gaussian_pages import CoefficientAdmissionError
    receipts={};cases=[('primary',format(741503,'b'),format(466013,'b')),('asymmetric',format(457183,'b'),format(56987,'b')),('saturated','1'*144,'1'*144)]
    if with_interior:cases.append(('strict_interior',format(741503,'0145b'),format(466013,'0145b')))
    for key,left,right in cases:
        answer,info=up.multiply(left,right);raw=schoolbook(left,right,info['digit_bits'],prod(info['sources']));g=up.choose(max(len(left),len(right)));pages=up.catalogue(g)
        require(info['path']=='gaussian' and len(answer)==2*max(len(left),len(right)) and int(answer,2)==int(left,2)*int(right,2),'genuine original binary product or output width')
        require(raw==info['coefficients'] and int(answer,2)==sum(c<<(g.digit_bits*k)for k,c in enumerate(raw)),'independent every original coefficient and carry')
        require(2*((max(len(left),len(right))+g.digit_bits-1)//g.digit_bits)-1<=len(raw),'no-wrap ordinary convolution')
        rr=F(info['radius_numerator'],info['radius_denominator']);observed=F(info['max_residual_squared_numerator'],info['radius_denominator']**2)
        d=len(g.sources);K=1<<info['scale_exponent'];C=prod(g.sources)**2<<(2*g.digit_bits+4);h=F(1,1<<g.precision);eta=sum((r.defect for _,a,b in pages for r in (a,b)),F(0));e=(64*d+64)*h;z=F(1,4);delta=K*(eta*z+e);f=z+delta;w=f*f+2*K*K*h
        bound=C*(delta*(f+z)+2*K*K*h+K*eta*w+K**3*e);easy=C*K**3*(64*d+64)*h
        cap=F(1,1<<(g.precision+3));raw_bound=easy if all(r.defect<cap for _,a,b in pages for r in (a,b)) and easy<F(1,2)else bound
        round_up=-(-(raw_bound.numerator*(1<<g.precision))//raw_bound.denominator);require(F(round_up,1<<g.precision)==rr and rr<F(1,2) and observed<=rr*rr,'independent rational operator error and joint three-call scale')
        require(max(z,w/K**2)+e<F(1,2),'normalized intermediate entrance')
        receipts[key]={'sources':info['sources'],'targets':info['targets'],'grid':g.precision,'digit_bits':g.digit_bits,'gamma':info['scale_exponent'],'original_coefficients':len(raw),'coefficient_sha256':hashlib.sha256(json.dumps(raw,separators=(',',':')).encode()).hexdigest(),'first_coefficients':raw[:9],'binary_answer':answer,'answer':str(int(answer,2)),'radius':encode(rr),'radius_decimal':float(rr),'radius_bound_recomputed':True,'observed_squared_residual':encode(observed),'rings':info['trace']['rings'],'stages':info['trace']['stages'],'grouped_requests':info['trace']['grouped_requests'],'charged_scalar_products':info['trace']['scalar_products'],'live_at_exit':info['trace']['live'],'physical_native_requests':info['trace']['native_requests'],'above_cutoff_word_requests':info['trace']['fast_words']}
    left,right=cases[0][1:];correct=receipts['primary']['answer'];old=up.recover
    def unscale(values,S,q,b,amplification,bound,trace):return old(values,S,q,b,amplification-1,bound,trace)
    try:
        up.recover=unscale
        try:up.multiply(left,right)
        except ArithmeticError as err:scale_error=str(err)
        else:raise ValueError('missing binary normalization escaped the genuine residual guard')
    finally:up.recover=old
    old_route=up.route
    def altered_inverse(values,axes,padded,inverse,*args,**kwargs):
        ordered=old_route(values,axes,padded,inverse,*args,**kwargs)
        if inverse:ordered[0],ordered[1]=ordered[1],ordered[0]
        return ordered
    try:
        up.route=altered_inverse;wrong,info=up.multiply(left,right)
    finally:up.route=old_route
    require(str(int(wrong,2))!=correct and 2*info['radius_numerator']<info['radius_denominator'],'two real original positions must be distinguished from a geometric radius')
    strict=up.choose(145);mock=SimpleNamespace(defect=radius.page_limit(strict)*F(3,4),output_shift=3)
    try:radius.rounding_numerator(strict,[((),mock,mock)]*2)
    except CoefficientAdmissionError as err:joint_error=str(err)
    else:raise ValueError('separately passing page caps were mistaken for the whole product radius')
    theta=F(997,1000);native=F(1737,10**6);selected=F(50000002,10**10);target=F(1,200);needed=target/(1-target)
    require(1-theta*native==F(998268211,10**9) and selected/(1+selected)<target and needed==F(1,199),'exact outer arithmetic')
    ideal=F(504325518581,10**14);ordinary=ideal*(1-ideal);combined=ordinary/(1+ordinary)
    require(combined<F(499276794827,10**14)<target and ordinary<needed,'monotone raw-tariff / ordinary / outer barrier')
    return {'ideal_raw_strict_upper':encode(ideal),'ideal_ordinary_strict_upper':encode(ordinary),'ideal_double_contraction_strict_upper':encode(combined),'ideal_double_contraction_decimal':str(float(combined)),'status':'PASS_AUTHENTIC_GAUSSIAN_ORIGINAL_RECOVERY_AND_TARGET_PRICE','upstream_head':HEAD,'upstream_tree':subprocess.check_output(['git','-C',str(repo),'rev-parse',HEAD+':'+SUBDIR],text=True).strip(),'verified_blob_count':len(pins),'source_files':pins,'products':receipts,'negative_controls':{'missing_one_final_scale_bit':scale_error,'swapped_original_outputs_product':str(int(wrong,2)),'correct_product':correct,'swapped_original_outputs_still_pass_radius':True,'individually_passing_pages_fail_joint':joint_error},'supplier_retained_saving':encode(native),'literal_outer_power':encode(1-theta*native),'literal_dense_axis_power':encode(theta),'target_power':encode(1-target),'optimized_supplier_threshold':encode(needed),'optimized_saving_from_conditional_0050000002':encode(selected/(1+selected)),'new_complete_kappa':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--canonical',required=True,type=Path);p.add_argument('--source',type=Path);p.add_argument('--out',required=True,type=Path);p.add_argument('--with-interior',action='store_true');args=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='upstream-gaussian-') as td:
        source=args.source
        if source is None:
            raw=subprocess.check_output(['git','-C',str(args.canonical),'archive',HEAD,SUBDIR]);base=Path(td)
            with tarfile.open(fileobj=io.BytesIO(raw)) as bundle:bundle.extractall(base,filter='data')
            source=base/SUBDIR
        r=run(args.canonical,source,args.with_interior)
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print('PASS',r['verified_blob_count'],list(r['products']),r['negative_controls'])

if __name__=='__main__':main()
