#!/usr/bin/env python3
"""Paid same-cardinality hosted/coupled repartition of a complete native word.

The old complete word is retained literally after register renaming; removed
old dual inputs are genuine zero-initialized owned registers, not helpers.
"""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CALLER='3828d53e80ea97e8b866320f081af20b6b93bfebd58b95b56b85a7afe151af5e'
ENGINE='21f46a8340331abb1486b50bd4e04453f1968b0a5950d86ff7780dd368590874'
FULL='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
NEW_COUPLED=[26,33,40,47,52,57,72,82]
def need(ok,label):
    if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path,pin):
    raw=path.read_bytes();need(sha(raw)==pin,'source pin '+str(path));return json.loads(gzip.decompress(raw)if path.suffix=='.gz'else raw)
def main(args):
    old=load(args.native,NATIVE);caller=load(args.caller,CALLER)
    need(sha(args.full.read_bytes())==FULL,'complete baseline receipt pin')
    need(sha(args.engine.read_bytes())==ENGINE,'retained independent native/caller engine pin')
    sp=importlib.util.spec_from_file_location('repartition_retained_native',args.engine);engine=importlib.util.module_from_spec(sp)
    engine_changes=[]
    if args.variant=='allhosted':
        # The original all-column interpreter hard-codes its old96-hosted
        # census in one assertion. The target construction and every other
        # check are unchanged; the new104-hosted target is proved explicitly.
        source=args.engine.read_text();before='len(D)==96';after='len(D)==104'
        need(source.count(before)==1,'one and only one hosted-census scope extension')
        source=source.replace(before,after);engine_changes.append({'before':before,'after':after})
        exec(compile(source,str(args.engine),'exec'),engine.__dict__)
    else:sp.loader.exec_module(engine)
    n=old['public'];live=old['live'];oldH={live[i]:(b,d)for i,b,d in zip(old['hosted']['Dports'],old['hosted']['X2'],old['hosted']['Y2'])}
    oldU=sorted(set(live)-set(oldH));newU=[]if args.variant=='allhosted'else sorted(NEW_COUPLED);newH=sorted(set(live)-set(newU))
    need(len(oldU)==8 and set(newU)<=set(live),'actual native port partitions')
    removed=sorted(set(oldH)-set(newH));added=sorted(set(newH)-set(oldH));minus=len(removed);plus=len(added)
    need((minus,plus)==((0,8)if args.variant=='allhosted'else(5,5)),'stated source partition cardinalities')
    growth=2*(plus-minus);public=n+growth
    pairs={h:oldH[h]for h in newH if h in oldH};replaced={}
    for k,newh in enumerate(added):
        if k<minus:pairs[newh]=oldH[removed[k]];replaced[newh]=removed[k]
        else:pairs[newh]=(n+2*(k-minus),n+2*(k-minus)+1);replaced[newh]=None
    removed_roles=[role for h in removed for role in oldH[h]]
    zero_roles={role:public+old['owned_fields']+i for i,role in enumerate(removed_roles)}
    q=public+old['owned_fields']+len(removed_roles);O=3;Hub=127
    word=copy.deepcopy(old);word['schema']='moonshot-S012-paid-native-repartition-v1'
    word['owned_fields']=old['owned_fields']+len(removed_roles)+1
    word['public']=public;word['initial'].extend([None]*growth);word['final'].extend([None]*growth)
    for h in added:
        b,d=pairs[h];word['initial'][b]=old['initial'][h];word['initial'][d]=O
        word['final'][b]=Hub;word['final'][d]=old['final'][h+112]
    newindices=[i for i,h in enumerate(live)if h in pairs]
    word['hosted']['Dports']=newindices;word['hosted']['X2']=[pairs[live[i]][0]for i in newindices]
    word['hosted']['Y2']=[pairs[live[i]][1]for i in newindices]
    out=[];events={};markers={}
    def emit(op):out.append(op);return len(out)-1
    def add(d,s,c,C):return emit(['ADD',d,s,str(c),C])
    def ferry(source,dest,c,A,B):
        emit(['INIT',q,A]);add(q,source,1,A);move=emit(['MOVE',q,A,B,True]);read=add(dest,q,c,B);emit(['CLEAR',q,B]);return move,read
    for role,target in zero_roles.items():emit(['INIT',target,old['initial'][role]])
    events['A_to_B_entries']=[];events['B_to_A_entries']=[];events['new_dual_entries']=[]
    for h in removed:
        events['A_to_B_entries'].append(ferry(h+112,h,-1,O,old['initial'][h]))
        emit(['SCALE',h+112,'2',O])
    for h in added:
        events['B_to_A_entries'].append(ferry(h+112,h,1,O,old['initial'][h]))
        b,d=pairs[h];events['new_dual_entries'].append(ferry(d,b,-1,O,old['initial'][h]))
        emit(['MOVE',b,old['initial'][h],Hub,False]);emit(['MOVE',d,O,old['final'][h+112],False])
    markers['old_body_begin']=len(out)
    def renamed(op):
        def role(r):return zero_roles.get(r,r+growth if r>=n else r)
        e=op.copy();e[1]=role(e[1])
        if e[0]in('ADD','COPY'):e[2]=role(e[2])
        if e[0]=='MOVE'and op[1]in zero_roles:e[4]=True
        return e
    out.extend(renamed(op)for op in old['program']);markers['old_body_end']=len(out)
    # These extended inputs have both been zero. Correctness of the complete
    # old native makes their final B-D and D values exactly zero.
    events['zero_retirements']=[]
    for role,target in zero_roles.items():events['zero_retirements'].append(emit(['CLEAR',target,old['final'][role]]))
    for h in removed:emit(['SCALE',h+112,'1/2',old['final'][h+112]])
    events['B_to_A_output_repairs']=[]
    for h in added:events['B_to_A_output_repairs'].append(ferry(h,h+112,F(1,2),Hub,old['final'][h+112]))
    word['program']=out
    word['repartition']={'variant':args.variant,'old_native_sha256':NATIVE,'old_caller_sha256':CALLER,'old_coupled':oldU,'new_coupled':newU,
       'old_hosted_to_new_coupled':removed,'old_coupled_to_new_hosted':added,
       'new_dual_role_to_old_host_port':replaced,'zero_extension_old_to_owned':zero_roles,'adapter_owner':q,
       'markers':markers,'events':events,'old_complete_body_retained_after_exact_renaming':True,
       'additional_paid_profile':{1:minus+3*plus,8:2*plus},'helper_credit_changes':{},
       'public_growth':growth,'old_owned_register_shift':growth,'retained_engine_scope_extension':engine_changes,
       'scope':'Complete finite native conversion, not a new kappa or a discharge of physical/native/compiler assumptions.'}
    caller=copy.deepcopy(caller);caller['types']['A']['ports']=newindices
    caller['types']['B']['ports']=[i for i in range(len(live))if i not in set(newindices)]
    original_call=load(args.caller,CALLER)
    normalized=copy.deepcopy(caller)
    for tag in('A','B'):normalized['types'][tag]['ports']=original_call['types'][tag]['ports']
    need(normalized==original_call,'only caller port membership changes, no polynomial events or scalar laws')
    args.output.mkdir(parents=True,exist_ok=True)
    payload=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    (args.output/'WORD.json.gz').write_bytes(blob)
    cb=(json.dumps(caller,sort_keys=True,separators=(',',':'))+'\n').encode();(args.output/'CALLER.json').write_bytes(cb)
    print(json.dumps({'status':'EMITTED_PAID_NATIVE_REPARTITION','word_sha256':sha(blob),'caller_sha256':sha(cb),
                      'events':len(out),'old_body_operations':len(old['program']),'changed_to_coupled':minus,'changed_to_hosted':plus},sort_keys=True),flush=True)
    result=engine.native(word)
    need(not result['bad_inputs'],'all independent native columns satisfy the new exact target')
    old_result=json.loads(args.full.read_text())['native']
    paid=Counter({int(k):v for k,v in old_result['paid'].items()});paid[1]+=minus+3*plus;paid[8]+=2*plus
    need(Counter(result['paid'])==paid,'full paid histogram equals source plus exact adapter movements')
    need(result['helpers']=={int(k):v for k,v in old_result['helpers'].items()},'all old independent helper credits retained exactly')
    ordinary=engine.ordinary(word,caller,result)
    need(ordinary['conservative_total']<10**9,'existing complete ordinary billion ceiling remains satisfied')
    receipt={'status':'PASS_COMPLETE_FINITE_PAID_NATIVE_REPARTITION','word_sha256':sha(blob),'caller_sha256':sha(cb),
      'source_pins':{'native':NATIVE,'caller':CALLER,'retained_native_engine':ENGINE},'old_coupled':oldU,'new_coupled':newU,
      'variant':args.variant,'changed_to_coupled':minus,'changed_to_hosted':plus,'main_public_fields':208+2*len(newH),
      'new_native':result,'old_native':old_result,'additional_paid_profile':{1:minus+3*plus,8:2*plus},
      'retained_engine_scope_extension':engine_changes,
      'complete_ordinary_invoice':ordinary,'caller_only_port_membership_changed':True,
      'scope':'Author exact finite all-public-column verification with retained independent engine; independent review separate. All five foundations retained. No new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':receipt['status'],'word_sha256':sha(blob),'native':result,
                      'ordinary_total':ordinary['conservative_total']},sort_keys=True,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--caller',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--full',type=Path,required=True)
    p.add_argument('--variant',choices=('orthogonal','allhosted'),required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
