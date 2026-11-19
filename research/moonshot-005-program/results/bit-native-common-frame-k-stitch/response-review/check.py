#!/usr/bin/env python3
"""Independent algebraic response audit of the five-tile shared-K word. Same separate B response engine as the two-tile audit.
This is not a replacement for the separate full physical-owner word review.
"""
from argparse import ArgumentParser
from pathlib import Path
from hashlib import sha256
from collections import Counter
from itertools import combinations
import gzip,json
PINS={'word':'806dca8703c7ca75854b91d9946f81c5df72b77614aa3b62b5a2e2c53692411a','certificate':'3b11e44b0fbb7b43b3f5699774935e8bd77e7096589ef8973f866d5a9f4e1cf1','layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'}
N=111;BANK=480;FIELD=5;XFIELDS=N*BANK;XF=XFIELDS*FIELD;PUBLIC=2*XF


def load(path,key,jsonl=False):
    raw=gzip.decompress(path.read_bytes());assert sha256(raw).hexdigest()==PINS[key]
    return [json.loads(x)for x in raw.splitlines()]if jsonl else json.loads(raw)

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


def mm(A,B):
    out=[]
    for row in A:
        rr=[]
        for col in zip(*B):
            v=0
            for x,y in zip(row,col):v^=mul(x,y)
            rr.append(v)
        out.append(rr)
    return out

def local_aggregate(act,group):
    fields=set(group['input_fields'])|{group['output_field']}|{z//5 for op in act['word']for z in op[1:]}
    bits=[5*f+r for f in sorted(fields)for r in range(5)];col={z:i for i,z in enumerate(bits)};v={z:1<<i for z,i in col.items()}
    for op in act['word']:
        assert op[0]=='ADD'and op[1]!=op[2];v[op[1]]^=v[op[2]]
    assert rank(v.values())==len(bits)
    for r in range(5):assert v[5*group['output_field']+r]==sum(1<<col[5*f+r]for f in group['input_fields'])

def capture(W,col,tag,field):
    values={bit:1<<i for bit,i in col.items()}
    for a in W['actions']:
        for op in a['word']:
            if op[0]=='INIT':values[op[1]]=0
            elif op[0]=='ADD':values[op[1]]^=values[op[2]]
            else:del values[op[1]]
        if a['tag']==tag:return [values[5*field+r]for r in range(5)]
    raise AssertionError(tag)

def early_intervention(W,C):
    fs=[r[3]for r in C['source_X_owners']];assert len(fs)==len(set(fs))==240
    ix={5*f+r:i for i,(f,r)in enumerate((f,r)for f in fs for r in range(5))};value={z:1<<i for z,i in ix.items()}
    for a in W['actions']:
        if a['stage']=='X_NATIVE':continue
        for op in a['word']:
            if op[0]=='INIT':value[op[1]]=0
            elif op[0]=='ADD':value[op[1]]=value.get(op[1],0)^value.get(op[2],0)
            else:value.pop(op[1],None)
    outputs={z:v for z,v in value.items()if XF<=z<PUBLIC and v}
    assert set(outputs)=={XF+5*(80*BANK+c)+r for c in range(4)for r in range(5)}
    assert rank(outputs.values())==20
    per={}
    for j in W['source_donors']:
        mask=sum(1<<ix[5*f+r]for d,jj,h,f in C['source_X_owners']if j==jj for r in range(5))
        assert rank(v&mask for v in outputs.values())==20;per[str(j)]=4
    return per

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    layout=load(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','layout')
    routes=load(base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','routes',True)
    W=load(a.author/'output/WORD.json.gz','word');C=load(a.author/'output/CERTIFICATE.json.gz','certificate')
    H=list(map(set,layout['A2']));D=list(map(set,layout['D4']));roots=layout['root_table']
    neighbors=[j for j in range(111)if sum(x*y for x,y in zip(roots[80],roots[j]))==0]
    assert neighbors==C['neighbor80_order'];donors=sorted(set().union(*(D[d]for d in W['middle_tiles'])))
    assert donors==W['source_donors']and len(donors)==31 and max(donors)<111
    route={(0 if r[0]=='X'else XFIELDS)+r[1]*BANK+r[2]:r for r in routes}
    mask_fields=[int(j)*BANK+c for j,cols in W['private_mask_columns_by_donor'].items()for c in cols]
    assert len(mask_fields)==len(set(mask_fields))==116
    col={z:i for i,z in enumerate(sorted(public_bits(W)))};B,result=evaluate(W,col)
    mask=sum(1<<col[5*f+r]for f in mask_fields for r in range(5));assert all(not(v&mask)for v in B.values())
    for i in [80,1]:
        for t in range(4):
            fields=[]
            for j in donors:
                cc=[t];p=neighbors.index(j)
                if i==80 and p==0:cc.append(t+1)
                elif i==80 and 2<=p<=60:cc.append(8*(p-1)+t)
                fields.extend(j*BANK+c for c in cc)
            for r in range(5):assert B[5*(i*BANK+t)+r]==sum(1<<col[5*f+r]for f in fields)
    # Receiver frames and every actual selected four-column inverse.
    inverses={(d,i):M for d,i,M in C['D_frame_codes']};minor_checks=0
    for i in [80,1]:
        active=C['active_K'][str(i)];F=C['frames'][str(i)];assert len(active)==12 and len(F)==4
        for sel in combinations(range(12),4):assert fieldrank([[row[k]for k in sel]for row in F])==4;minor_checks+=1
        for d in W['middle_tiles']:
            ks=[k for k in C['K'][str(d)]if i in H[k]];assert len(ks)==4
            R=[[row[active.index(k)]for k in ks]for row in F];I=[[int(r==c)for c in range(4)]for r in range(4)]
            assert mm(R,inverses[d,i])==I and mm(inverses[d,i],R)==I
    acts={a['tag']:a for a in W['actions']};agg_checks=0
    for phase,key,i in [('X','early_K_aggregates',80),('Y','late_K_aggregates',1)]:
        groups=C[key];assert len(groups)==12 and sum(len(g['input_fields'])for g in groups)==20
        for g in groups:
            k=g['K'];assert k in C['active_K'][str(i)]and i in H[k]
            assert len(g['input_fields'])==len(set(g['input_fields']))
            assert {route[f][4]for f in g['input_fields']}==set(g['tiles'])
            assert all(route[f][0]==phase and route[f][5]==k for f in g['input_fields'])
            rr=route[g['output_field']];assert rr[0]==phase and rr[5]==k and(rr[7]if phase=='X'else rr[1])==i
            tag=f'aggregate-{phase}-K-{k}';act=acts.get(tag,{'word':[]})
            if act['word']:assert act['chart']==['K',k]and act['stage']==f'{phase}_K'
            local_aggregate(act,g);agg_checks+=1
    # The actual K370 late aggregate has all31 original donor supports.
    g=next(g for g in C['late_K_aggregates']if g['K']==370)
    captured=capture(W,col,'aggregate-Y-K-370',g['output_field']);inv={i:z for z,i in col.items()}
    support=set()
    for row in captured:
        v=row
        while v:
            low=v&-v;z=inv[low.bit_length()-1];v^=low
            if z<XF:support.add(z//5//BANK)
    assert support==set(donors)
    # One field's missing frame contribution breaks global mask cancellation.
    fault=json.loads(json.dumps(W));f370=next(g['output_field']for g in C['early_K_aggregates']if g['K']==370)
    for act in fault['actions']:
        if act['stage']=='X_F':act['word']=[op for op in act['word']if not(op[0]=='ADD'and op[2]//5==f370)]
    faultB,_=evaluate(fault,col);fault_rank=rank(v&mask for v in faultB.values());assert fault_rank==5
    per=early_intervention(W,C);source=[]
    for j in donors:
        entries=[e for e in C['matrices']if e['donor']==j];stack=[r for e in entries for r in e['U']];m=4*len(entries)
        assert fieldrank(stack)==m<=480
        for e in entries:assert all(not any(row[c]for c in W['private_mask_columns_by_donor'].get(str(j),[]))for row in e['V'])
        source.append({'donor':j,'tile_incidence':len(entries),'independent_early_rows':m,'private_masks':len(W['private_mask_columns_by_donor'].get(str(j),[]))})
    out={'status':'PASS_INDEPENDENT_SHARED_K_RESPONSE_AUDIT','pins':PINS,'algebraic_word_result':result,
         'selected_target_field_rows_per_receiver':4,'selected_receivers':[80,1],'served_donors':31,
         'all_private_original_mask_fields':116,'all_private_original_mask_binary_columns':580,'full_output_mask_response_rank':0,
         'receiver_frame_four_column_minors_checked':minor_checks,'actual_D_frame_inverses_checked':10,'actual_K_aggregates_checked':agg_checks,
         'actual_K370_late_packet_native_support':sorted(support),'terminal_packets_per_receiver':12,'uncompressed_tile_packets_per_receiver':20,
         'early_source_intervention_full_output_field_rank':4,'early_source_intervention_per_donor':per,'joint_source_rows':source,
         'missing_K370_frame_contribution_mask_field_rank':fault_rank//5,
         'author_python_imported_or_executed':False,'uses_same_B_response_engine':True,'replaces_full_owner_review':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['status']);print('proper rank',result['proper_response_binary_rank']//5,'exact q',result['exact_return_field_rank'],'mask response0; K370 support31')
if __name__=='__main__':main()
