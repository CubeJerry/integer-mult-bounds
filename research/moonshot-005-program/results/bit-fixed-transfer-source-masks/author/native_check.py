#!/usr/bin/env python3
"""Independent algebraic response audit of the pinned overlapping native words.
This is not a replacement for the separate full physical-owner word review.
"""
from argparse import ArgumentParser
from pathlib import Path
from hashlib import sha256
from collections import Counter
import gzip,json
PINS={'preferred_word':'6096382d0542028f812130d707dbd299de23bbc52a800283ef219f9f9ab45ae7','preferred_certificate':'431033a6d94e43531b2991deb2c4a16c4dada66fd126fa68a3610cf0e8e558aa','control_word':'9f0cd288c783a55417405e7e78ce97800863e9f8cbda59d9e516f71e5890fd24','control_certificate':'eed91a2185ba221a5afb81589fbfbe58e53cde5a0a80c14d23dc1c983d7dc198'}
N=111;BANK=480;FIELD=5;XFIELDS=N*BANK;XF=XFIELDS*FIELD;PUBLIC=2*XF
SHARED=[5,7,42,43,44,45];MASK_FIELDS=[j*BANK+c for j in SHARED for c in range(476,480)]

def load(path,key):
    raw=gzip.decompress(path.read_bytes());assert sha256(raw).hexdigest()==PINS[key]
    return json.loads(raw)

def rank(rows):
    piv={}
    for v in rows:
        while v:
            k=v.bit_length()-1
            if k in piv:v^=piv[k]
            else:piv[k]=v;break
    return len(piv)

def mul(a,b):
    t=0
    for j in range(5):
        if b>>j&1:t^=a<<j
    for j in range(8,4,-1):
        if t>>j&1:t^=0x25<<(j-5)
    return t

def fieldrank(M):
    return rank([sum(mul(1<<b,x)<<(5*k)for k,x in enumerate(row))for row in M for b in range(5)])//5

def public_bits(W):return {bit for a in W['actions']for op in a['word']for bit in op[1:]if bit<PUBLIC}

def evaluate(W,col):
    value={bit:1<<i for bit,i in col.items()};live=set();counts=Counter();peak=0;dirty=0
    for a in W['actions']:
        for op in a['word']:
            counts[op[0]]+=1
            if op[0]=='INIT':
                z=op[1];assert z>=PUBLIC and z not in live;live.add(z);value[z]=0;peak=max(peak,len(live))
            elif op[0]=='ADD':
                dst,src=op[1:];assert dst!=src
                assert all(z<PUBLIC or z in live for z in [dst,src]);value[dst]^=value[src]
            elif op[0]=='CLEAR':
                z=op[1];assert z in live;dirty+=bool(value[z]);live.remove(z);del value[z]
            else:raise AssertionError(op[0])
    assert not live
    ym=sum(1<<i for z,i in col.items()if z>=XF)
    assert all(value[z]==1<<i for z,i in col.items()if z<XF)
    assert all(value[z]&ym==1<<i for z,i in col.items()if z>=XF)
    B={z-XF:value[z]^(1<<i)for z,i in col.items()if z>=XF and value[z]!=(1<<i)}
    assert all((v&ym)==0 for v in B.values())
    original={i:z for z,i in col.items()};blocks={}
    for outbit,row in B.items():
        v=row
        while v:
            low=v&-v;index=low.bit_length()-1;inbit=original[index];v^=low
            assert inbit<XF
            block=blocks.setdefault((outbit//5,inbit//5),[0]*5)
            block[inbit%5]^=1<<(outbit%5)
    assert all(block==[mul(block[0],1<<r)for r in range(5)]for block in blocks.values())
    R=sorted(B);rpos={x:i for i,x in enumerate(R)}
    principal=[]
    for z in R:
        row=1<<rpos[z]
        for x in R:
            if x in col and B[z]>>col[x]&1:row^=1<<rpos[x]
        principal.append(row)
    q_binary=XF-len(R)+rank(principal)
    return B,{'proper_response_binary_rank':rank(B.values()),'nonzero_output_fields':len({z//5 for z in B}),
              'nonzero_output_bits':len(R),'return_principal_binary_rank':rank(principal),'exact_return_binary_rank':q_binary,
              'exact_return_field_rank':q_binary//5 if q_binary%5==0 else None,'counts':dict(counts),'peak':peak,'dirty_CLEAR':dirty,'GF32_blocks_checked':len(blocks)}

def early_intervention(W,C):
    records=C['source_X_owners'];fs=[r[3]for r in records];assert len(fs)==len(set(fs))==96
    bits=[5*f+b for f in fs for b in range(5)];ix={z:i for i,z in enumerate(bits)}
    values={z:1<<i for z,i in ix.items()}
    for a in W['actions']:
        if a['stage']=='X_NATIVE':continue
        for op in a['word']:
            if op[0]=='INIT':values[op[1]]=0
            elif op[0]=='ADD':values[op[1]]=values.get(op[1],0)^values.get(op[2],0)
            else:values.pop(op[1],None)
    outputs={z:val for z,val in values.items()if XF<=z<PUBLIC and val}
    wanted={XF+5*(80*BANK+c)+b for c in range(4)for b in range(5)}
    assert set(outputs)==wanted and rank(outputs.values())==20
    per={}
    for j in sorted({r[1]for r in records}):
        mask=sum(1<<ix[5*r[3]+b]for r in records if r[1]==j for b in range(5))
        r=rank(v&mask for v in outputs.values());assert r==20
        per[str(j)]={'early_input_field_count':sum(r[1]==j for r in records),'full_output_field_rank':r//5,'selected_output_field_rank':r//5}
    return outputs,per

def pure_late(W):
    return [(a['stage'],a['chart'],op)for a in W['actions']if a['stage'] in ['Y_H','Y_D','Y_K','Y_F']for op in a['word']
            if op[0]=='ADD'and XF<=op[1]<PUBLIC and XF<=op[2]<PUBLIC]

def late_intervention(W,C):
    records=C['source_Y_owners'];fs=[r[3]for r in records];assert len(fs)==len(set(fs))==96
    ix={5*f+b:i for i,(f,b)in enumerate((f,b)for f in fs for b in range(5))}
    values={z:1<<i for z,i in ix.items()}
    for _,__,op in pure_late(W):values[op[1]]=values.get(op[1],0)^values.get(op[2],0)
    outputs={z:v for z,v in values.items()if v};assert rank(outputs.values())==480
    clean={XF+5*(80*BANK+c)+b for c in range(4)for b in range(5)}
    assert all(not outputs.get(z,0)for z in clean)
    per={}
    for j in sorted({r[1]for r in records}):
        mask=sum(1<<ix[5*r[3]+b]for r in records if r[1]==j for b in range(5))
        r=rank(v&mask for v in outputs.values());expected=5*sum(v[1]==j for v in records);assert r==expected
        per[str(j)]=r//5
    return outputs,per

def main():
    ap=ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    W=load(a.author/'output/WORD.json.gz','preferred_word');C=load(a.author/'output/CERTIFICATE.json.gz','preferred_certificate')
    V=load(a.author/'late-mask-control/WORD.json.gz','control_word');D=load(a.author/'late-mask-control/CERTIFICATE.json.gz','control_certificate')
    assert W['shared_donors']==V['shared_donors']==SHARED
    assert C['source_X_owners']==D['source_X_owners']and C['source_Y_owners']==D['source_Y_owners']
    assert pure_late(W)==pure_late(V)
    col={z:i for i,z in enumerate(sorted(public_bits(W)|public_bits(V)))}
    BP,rp=evaluate(W,col);BC,rc=evaluate(V,col)
    mask=sum(1<<col[5*f+b]for f in MASK_FIELDS for b in range(5))
    assert all(not(v&mask)for v in BP.values())
    mask_control={z:v&mask for z,v in BC.items()if v&mask};assert rank(mask_control.values())==120
    diff={z:BP.get(z,0)^BC.get(z,0)for z in set(BP)|set(BC)if BP.get(z,0)!=BC.get(z,0)}
    assert all(v&~mask==0 for v in diff.values())and rank(diff.values())==120
    fault=json.loads(json.dumps(W))
    for act in fault['actions']:
        if act['stage']=='X_F':
            assert len(act['word'])==15;act['word']=act['word'][:10]
    faultB,_=evaluate(fault,col);faultmask=rank(v&mask for v in faultB.values());assert faultmask==20
    selected={5*(i*BANK+c)+b for i in [1,80]for c in range(4)for b in range(5)}
    assert all(not mask_control.get(z,0)for z in selected)
    E,perE=early_intervention(W,C);L,perL=late_intervention(W,C)
    joint=rank(E.get(z,0)|(L.get(z,0)<<480)for z in set(E)|set(L));assert joint==500
    # Check source-mask independence and the exact 24-row late difference.
    cm={(e['D'],e['donor']):e for e in C['matrices']};dm={(e['D'],e['donor']):e for e in D['matrices']}
    source_checks=[]
    for j in SHARED:
        stack=cm[12,j]['U']+cm[99,j]['U'];assert fieldrank(stack)==8
        assert all(cm[d,j]['U']==dm[d,j]['U']for d in [12,99])
        delta=[]
        for d in [12,99]:
            P=cm[d,j]['V'];Q=dm[d,j]['V']
            assert all(not any(row[476:480])for row in P)
            for x,y in zip(P,Q):
                row=[xx^yy for xx,yy in zip(x,y)];assert not any(row[:476]);delta.append(row[476:480])
        assert fieldrank(delta)==4
        source_checks.append({'donor':j,'early_source_row_rank':8,'late_mask_difference_rank':4})
    out={'status':'PASS_INDEPENDENT_NATIVE_MASK_CANCELLATION_AUDIT','pins':PINS,'preferred':rp,'late_mask_control':rc,
         'original_mask_field_coordinates':24,'original_mask_binary_columns':120,'preferred_full_Y_mask_response_rank':0,
         'control_full_Y_mask_response_field_rank':24,'whole_map_difference_field_rank':24,
         'difference_has_only_mask_input_columns':True,'omit_second_tile_early_cancellation_control_field_rank':faultmask//5,'selected_receiver_mask_response_rank':0,
         'early_intervention_formal_fields':96,'early_intervention_full_output_field_rank':4,'early_intervention_per_donor':perE,
         'late_intervention_formal_fields':96,'late_intervention_full_output_field_rank':96,'late_intervention_per_donor':perL,
         'combined_full_transfer_field_rank':joint//5,'source_checks':source_checks,
         'author_python_imported_or_executed':False,'physical_owner_review_replaced':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'NATIVE-RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['status']);print('preferred q',rp['exact_return_field_rank'],'control q',rc['exact_return_field_rank'],'full mask difference rank24')
if __name__=='__main__':main()
