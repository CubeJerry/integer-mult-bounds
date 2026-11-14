#!/usr/bin/env python3
"""Literal OPEN continuation retaining all eight actual old ground Gram owners."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
OLD='0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c'
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
ENGINE='045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e'
CODEC='4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297'
def need(ok,label):
    if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path,pin):
    raw=path.read_bytes();need(sha(raw)==pin,'source pin');return json.loads(gzip.decompress(raw))
def module(path,pin,name):
    need(sha(path.read_bytes())==pin,'engine pin');sp=importlib.util.spec_from_file_location('open_Gram_'+name,path)
    obj=importlib.util.module_from_spec(sp);sys.modules[sp.name]=obj;sp.loader.exec_module(obj);return obj
def replay(word,e):
    n=word['public'];rows={j:{j:F(1)}for j in range(n)};loc=dict(enumerate(word['initial']))
    spaces=[e.span(f)for f in word['frames']];paid=Counter();counts=Counter();peak=life=0
    for op in word['program']:
        ty,d=op[:2];counts[ty]+=1
        if ty=='INIT':need(d>=n and d not in loc,'INIT');rows[d]={};loc[d]=op[2];life+=1
        elif ty=='CLEAR':need(d>=n and loc.get(d)==op[2],'CLEAR');del rows[d];del loc[d]
        elif ty=='MOVE':
            a,b,owned=op[2:];need(loc.get(d)==a and owned==(d>=n),'MOVE source/ownership')
            need(spaces[a]<spaces[b]or owned and spaces[b]<spaces[a],'nested MOVE')
            loc[d]=b;paid[abs(len(word['frames'][a])-len(word['frames'][b]))]+=1
        elif ty in('ADD','COPY'):
            s,c,at=op[2:];need(d!=s and loc.get(d)==loc.get(s)==at,'cochart ADD/COPY')
            need(ty!='COPY'or not rows[d],'zero COPY');rows[d]=e.add(rows[d],rows[s],F(c))
        elif ty=='SCALE':c,at=op[2:];need(F(c)!=0 and loc.get(d)==at,'SCALE');rows[d]=e.scale(rows[d],F(c))
        else:raise ValueError(ty)
        peak=max(peak,len(loc)-n)
    terminal={int(k):v for k,v in word['terminal_owned'].items()}
    need(set(loc)==set(range(n))|set(terminal)and all(loc[k]==v for k,v in terminal.items()),'exact open owned outputs')
    return rows,loc,{'instructions':len(word['program']),'counts':dict(counts),'moves':dict(paid),'peak':peak,'lifetimes':life}
def main(args):
    old=load(args.old,OLD);native=load(args.native,NATIVE);e=module(args.engine,ENGINE,'engine');c=module(args.codec,CODEC,'codec')
    n=old['public'];need(n==400,'retained400 interface');start=old['relay']['markers']['ground_preload']
    removed=set(range(start,start+8));need(old['program'][start:start+8]==[['CLEAR',n+i,3]for i in range(8)],'eight real q owners retired together')
    begin=next(i for i,op in enumerate(old['program'])if i>old['relay']['markers']['all_B_reads']and op[:2]==['INIT',n])
    active=n+15;ops=[];origins=[];prefix=[0]
    for i,op in enumerate(old['program']):
        if i not in removed:
            op=op.copy()
            if i>=begin:
                if op[1]==n:op[1]=active
                if op[0]in('ADD','COPY')and op[2]==n:op[2]=active
            ops.append(op);origins.append(i)
        prefix.append(len(ops))
    word=copy.deepcopy(old);word['schema']='moonshot-S012-open-ground-Gram-preservation-v1';word['program']=ops;word['owned_fields']=16
    word['terminal_owned']={n+i:3 for i in range(8)};word['source_program_events']=origins
    word['relay']['markers']={k:prefix[v]for k,v in old['relay']['markers'].items()}
    for key,items in word['relay']['events'].items():
        if key=='first_swap':word['relay']['events'][key]=[prefix[j]for j in items]
        else:
            for z in items:z['step']=prefix[z['step']]
    word['open_preservation']={'source_word_sha256':OLD,'removed_original_CLEAR_indices':sorted(removed),
        'new_active_role':active,'all_eight_ground_q_kept':True,'source_moves_unchanged':True,'closed_native_interface':False,
        'future_obligation':'Decode all required original values before retiring these eight live owners; pay every future transport, storage and retirement operation.'}
    rows,loc,bill=replay(word,e);oldrows,oldloc,oldbill=e.replay(old,old['program'])
    need(word['frames']==old['frames']and [op[2:]for op in ops if op[0]=='MOVE']==[op[2:]for op in old['program']if op[0]=='MOVE'],
         'every ordered signed map literally inherited; no new geometry')
    need({j:rows[j]for j in range(n)}==oldrows and {j:loc[j]for j in range(n)}==oldloc,'all public rows and endpoints unchanged')
    need(bill['moves']==oldbill['moves']and bill['lifetimes']==oldbill['lifetimes']==24,'paid MOVEs and births unchanged')
    need(bill['peak']==16 and oldbill['peak']==15 and bill['counts']['CLEAR']==16,'peak16 and eight deferred retirements')
    roles={int(k):v for k,v in old['source_role_map'].items()};P=native['live'];host={P[i]:(roles[b],roles[d])for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    Z=old['relay']['ground_Gram_frame'];roots={h:c.root(native['frames'][native['initial'][h]][0])for h in P}
    g={h:[sum(x*y for x,y in zip(roots[h],c.root(z)))/18 for z in Z]for h in P}
    for i in range(8):need(rows[n+i]=={host[h][1]:g[h][i]for h in host if g[h][i]}and loc[n+i]==3,'true Gram value at ground')
    T=set(old['relay']['restored_ports']);perm={int(k):v for k,v in old['relay']['permutation'].items()};ip={j:h for h,j in perm.items()};inverse={}
    for h,(b,d)in host.items():
        coeff={d:F(1)}if h in T else e.add({host[ip[h]][1]:F(-1)},{n+i:g[h][i]for i in range(8)if g[h][i]})
        recovered={}
        for r,a in coeff.items():recovered=e.add(recovered,rows[r],a)
        need(recovered=={d:F(1)},'dyadic open-interface recovery of original D')
        inverse[h]={str(r):str(a)for r,a in coeff.items()}
    word['open_preservation']['abstract_original_D_recovery']=inverse
    bad=copy.deepcopy(word)
    for op in bad['program']:
        if op[1]==active:op[1]=n
        if op[0]in('ADD','COPY')and op[2]==active:op[2]=n
    try:replay(bad,e);rejected=False
    except ValueError:rejected=True
    need(rejected,'unrenamed active-owner alias rejected')
    payload=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    result={'status':'PASS_OPEN_OWNED_GROUND_GRAM_PRESERVATION','source_word_sha256':OLD,'word_sha256':sha(blob),
       'public_inputs':400,'open_owned_outputs':8,'open_owner_locations':word['terminal_owned'],
       'all_original_public_rows_unchanged':True,'all_eight_actual_Gram_payloads_retained':True,
       'all_ordered_signed_maps_inherited_from_pinned_old_word':True,
       'explicit_dyadic_left_inverse_checked':True,'source_bill':bill,'old_source_bill':oldbill,
       'negative_controls':['unrenamed_active_owner_alias_rejected'],'native_admissible':False,
       'remaining_original_D_restorations':76,'reverse_residual_rank':8,'forward_endpoint_debt':112,
       'scope':'Open owned continuation, with eight extra live outputs and all future costs retained. No closed native, supplier or new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'word_sha256':result['word_sha256'],'open_outputs':8,'source_bill':bill},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--old',type=Path,required=True);p.add_argument('--native',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--codec',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
