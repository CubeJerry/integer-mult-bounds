#!/usr/bin/env python3
"""Sparse reverse-row audit of the real adapter and zero-extension chronology."""
import argparse,copy,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path

WORDS={'orthogonal':'210dcdbb6aad3a5634b056ce336701b44eae5e5182ce8ea4f374ad2729693566',
       'allhosted':'3dec380d820ed631636bdc77adb4a4c3e35abdb31d2b312f8f41edadff389d96'}
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(ok,label):
    if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path,pin):
    raw=path.read_bytes();need(sha(raw)==pin,'input pin');return json.loads(gzip.decompress(raw))
def pullback(program,role):
    coef={role:F(1)}
    for op in reversed(program):
        ty,d=op[:2]
        if d not in coef:continue
        if ty in('INIT','CLEAR'):coef.pop(d)
        elif ty=='SCALE':coef[d]*=F(op[2])
        elif ty in('ADD','COPY'):
            s=op[2];q=coef.get(s,F(0))+coef[d]*F(op[3])
            if q:coef[s]=q
            else:coef.pop(s,None)
            if ty=='COPY':coef.pop(d,None)
        elif ty!='MOVE':raise ValueError(ty)
    return coef
def main(args):
    old=read(args.native,NATIVE);word=read(args.word,WORDS[args.variant]);meta=word['repartition']
    def realroot(h):
        v=word['frames'][word['initial'][h]][0];one=[i for i in range(9)if v>>i&1]
        if len(one)==3:return [2 if i in one else -1 for i in range(9)]
        zero=[i for i in range(9)if i not in one];need(len(zero)==2,'actual root normal')
        return [3*(int(i==zero[0])-int(i==zero[1]))for i in range(9)]
    if args.variant=='orthogonal':
        roots=[realroot(h)for h in meta['new_coupled']]
        need(all(sum(x*y for x,y in zip(roots[i],roots[j]))==18*int(i==j)for i in range(8)for j in range(8)),
             'new coupled set is an authentic orthogonal eight-frame')
    zero={int(k):v for k,v in meta['zero_extension_old_to_owned'].items()};growth=meta['public_growth']
    def rename(op):
        def role(r):return zero.get(r,r+growth if r>=old['public']else r)
        op=op.copy();oldr=op[1];op[1]=role(op[1])
        if op[0]in('ADD','COPY'):op[2]=role(op[2])
        if op[0]=='MOVE'and oldr in zero:op[4]=True
        return op
    first=meta['markers']['old_body_begin'];last=meta['markers']['old_body_end']
    need(word['program'][first:last]==[rename(op)for op in old['program']],
         'every old complete operation retained with only the stated source/register ownership renaming')
    zero_checks=[]
    for oldrole,newrole in zero.items():
        need(pullback(word['program'][:last],newrole)=={},'literal zero old dual extension at old-body exit')
        zero_checks.append({'old_role':oldrole,'owned_role':newrole,'final_chart':old['final'][oldrole]})
    live=word['live'];host={live[i]:(b,d)for i,b,d in zip(word['hosted']['Dports'],word['hosted']['X2'],word['hosted']['Y2'])}
    controls=[]
    def reject(label,idx,role,target):
        ops=copy.deepcopy(word['program']);op=ops[idx];need(op[0]=='ADD','actual ADD mutation')
        op[3]=str(-F(op[3]));need(pullback(ops,role)!=target,'adapter mutation '+label);controls.append(label)
    for key,ports in [('A_to_B_entries',meta['old_hosted_to_new_coupled']),('B_to_A_entries',meta['old_coupled_to_new_hosted'])]:
        for h,(_,index)in zip(ports,meta['events'][key]):
            target={h:F(1)}if h in host else{h:F(1),h+112:F(-1)}
            need(pullback(word['program'],h)==target,'exact converted X output row')
            reject('wrong_'+key+'_'+str(h),index,h,target)
    for h,(_,index)in zip(meta['old_coupled_to_new_hosted'],meta['events']['B_to_A_output_repairs']):
        target={h:F(1),h+112:F(1)};need(pullback(word['program'],h+112)==target,'exact hosted Y row')
        reject('wrong_hosted_Y_repair_'+str(h),index,h+112,target)
    for h,(_,index)in zip(meta['old_coupled_to_new_hosted'],meta['events']['new_dual_entries']):
        b,d=host[h];target={b:F(1),d:F(-1)}
        need(pullback(word['program'],b)==target,'exact new independent B-D output row')
        need(pullback(word['program'],d)=={d:F(1)},'new independent D unchanged')
        reject('wrong_new_dual_shear_'+str(h),index,b,target)
    if zero:
        # The old complete target isolates each dual pair from first X/Y.
        # A dirty fake zero can leave all kept outputs unchanged. The explicit
        # discarded-output check must therefore catch it on its own.
        oldH={old['live'][i]:(b,d)for i,b,d in zip(old['hosted']['Dports'],old['hosted']['X2'],old['hosted']['Y2'])}
        h=meta['old_hosted_to_new_coupled'][0];_,d=oldH[h];r=zero[d]
        prefix=copy.deepcopy(word['program'][:last]);prefix.insert(len(zero),['ADD',r,h+112,'1',3])
        need(pullback(prefix,r)=={h+112:F(1)},'dirty-zero-extension injection detected despite kept-output isolation')
        controls.append('dirty_zero_extension_caught_by_explicit_discarded_output_check')
    result={'status':'PASS_LITERAL_NATIVE_ADAPTER_AND_ZERO_EXTENSION_AUDIT','variant':args.variant,
        'word_sha256':WORDS[args.variant],'old_native_sha256':NATIVE,'old_body_operations':len(old['program']),
        'zero_extension_outputs':zero_checks,'negative_controls':controls,
        'scope':'Fresh sparse reverse-row derivation in addition to retained all-public-column replay; author checks, independent review separate.'}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':result['status'],'variant':args.variant,'zero_outputs':len(zero_checks),'mutants':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--word',type=Path,required=True)
    p.add_argument('--variant',choices=WORDS,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
