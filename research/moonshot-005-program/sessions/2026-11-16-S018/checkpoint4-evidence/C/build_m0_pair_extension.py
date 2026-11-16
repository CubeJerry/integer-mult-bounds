#!/usr/bin/env python3
"""Three M0 pair decoders after dead-use mutable-original release.

New C construction on A's frozen pure52 word.  No A code imported.
"""
import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from release_projection import N, binary_basis, chart, replay, require, rref
from price_projection import moment, record

PIN='dd0af2d4467b722c1692fb60b883407b4a95a8ea10b112fca0683dfc4a930edf'
PAIRS=[[21,34],[64,108],[65,104]]


def ints(rows):
    out=[]
    for row in rows:
        scale=math.lcm(*(x.denominator for x in row))
        out.append([int(x*scale)for x in row])
    return out


def main():
    ap=argparse.ArgumentParser()
    for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
    a=ap.parse_args()
    bp=a.work/'A/d4-cohort-pruned78/WORD.json';raw=bp.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==PIN,'frozen pure52 source pin')
    b=json.loads(raw);sr=(a.repo/b['source_path']).read_bytes()
    require(hashlib.sha256(sr).hexdigest()==b['source_sha256'],'native source pin')
    R=json.loads(sr)['native_roots'];before,bt,_=replay(b,collect=True)
    D=sorted(i for pair in PAIRS for i in pair);ds=set(D)
    require(not ds&set(b['cohort']['targets']),'new cache routes disjoint from first D4 cache inputs')
    normal=chart({'kind':'ann','rows':b['charts']['M0']['rows']})
    common_rec={'kind':'ann','rows':ints(normal)+[R[34]]}
    C=chart(common_rec);require(len(C)==4,'second common chart rank4')
    require(len(rref(C+chart(b['charts']['M0']))[0])==5,'second common below actual M0')
    eligible=[i for i in range(N)if all(sum(x*y for x,y in zip(v,R[i]))==0 for v in C)]
    require(eligible==[3,21,34,47,64,65,76,80,88,92,104,108],'actual second D4 geometry')
    for pair in PAIRS:require(sum(x*y for x,y in zip(R[pair[0]],R[pair[1]]))==0,'orthogonal pair')
    fields=['KEEP_C0','KEEP_C1','KEEP_C2'];packets=['P0','P1','P2']
    caps={p:b['operations'].index(['ADD',p,f])for p,f in zip(packets,fields)}
    resets={p:b['operations'].index(['ADD',f,p])for p,f in zip(packets,fields)}
    for p in packets:
        require([o for o in b['operations'][:caps[p]+1]if o[0]=='ADD'and o[1]==p]==[['ADD',p,fields[int(p[1:])]]],'exclusive first payload reader')
    donor_reads=[];donor_writes=[]
    for k,o in enumerate(b['operations']):
        if o[0]!='ADD':continue
        if o[1]in{f'X{i}'for i in D}:
            require(o[2]in packets and k<caps[o[2]],('all released donor reads belong to replaced encoders',k,o))
            donor_reads.append({'index':k,'operation':o})
        if o[2]in{f'X{i}'for i in D}:donor_writes.append({'index':k,'operation':o})
    require(len(donor_writes)==6 and {o['operation'][2]for o in donor_writes}=={'X21','X64','X65'},'three actual mutable originals with two old writes each')
    require(not any(o[0]=='ADD'and o[1].startswith('Y')for o in b['operations']),'old output rows have no source readers')
    charts=copy.deepcopy(b['charts']);charts['M0_PAIR_COMMON']=common_rec
    for i in D:charts[f'M0_PAIR_FLAG_{i}']={'kind':'span','rows':ints(C)+[R[i]]}
    new=[];newowners=[]
    for i in D:
        n=f'M0_PAIR_RAW_{i}';newowners.append(n);loc=f'M0_PAIR_FLAG_{i}'
        require(len(chart(charts[loc]))==5,'actual pair raw-cache flag rank5')
        new.extend([['MOVE',f'X{i}',loc],['INIT',n,loc],['ADD',f'X{i}',n],['MOVE',f'X{i}','Hub']])
    prelude_end=len(new);mapping={};removed=[];programs=[];decode_start=None;newcut=None
    oldcut=b['cohort']['continuation_before_operation']
    for k,o in enumerate(b['operations']):
        if k==oldcut:
            decode_start=len(new)
            new.extend([['MOVE',f,'M0_PAIR_COMMON']for f in fields])
            for f,pair in zip(fields,PAIRS):
                for i in pair:
                    other=pair[1]if i==pair[0]else pair[0]
                    new.extend([['MOVE',f'Y{i}','M0_PAIR_COMMON'],['ADD',f,f'Y{i}'],
                        ['MOVE',f'Y{i}',f'M0_PAIR_FLAG_{other}'],['ADD',f'M0_PAIR_RAW_{other}',f'Y{i}'],
                        ['MOVE',f'Y{i}',f'F{i}']])
            newcut=len(new)
        op,n,*q=o;skip=False
        if op=='MOVE'and n in{f'X{i}'for i in D}:skip=True
        if op=='ADD'and(n in{f'X{i}'for i in D}or q[0]in{f'X{i}'for i in D}):skip=True
        if n in{f'Y{i}'for i in D}:skip=True
        if op=='ADD'and q[0]in{f'Y{i}'for i in D}:skip=True
        if op=='ADD'and q[0]in packets and k<caps[q[0]]:skip=True
        if skip:
            removed.append({'old_index':k,'operation':o});mapping[k]=len(new);continue
        if op=='MOVE'and n in packets and bt[k][1][n]=='Hub':
            pair=PAIRS[int(n[1:])]
            for i in pair:new.append(['ADD',f'X{i}',n])
            programs.append({'packet':n,'before_old_index':k,'pair':pair,'after_new_index':len(new)})
        new.append(o);mapping[k]=len(new)
    require(newcut is not None and len(programs)==3,'three actual source programs and decoder cut')
    new.extend([['CLEAR',n]for n in newowners])
    w=copy.deepcopy(b)
    w.update(schema='M0-pair-extension-with-dead-use-mutable-carrier-release-v1',
        source_base_sha256=PIN,charts=charts,operations=new,targets=sorted(set(b['targets'])|ds),
        released_carriers=sorted(set(b['released_carriers'])-ds),carrier_interface_before_operation=newcut,
        pair_extension={'pairs':PAIRS,'common':'M0_PAIR_COMMON','fields':fields,
            'prelude_end':prelude_end,'decode_start':decode_start,'continuation_before_operation':newcut,
            'source_programs':programs,'mutable_originals':[21,64,65],
            'dead_old_mutable_reads':donor_reads,'deleted_old_mutable_writes':donor_writes},
        scope='Preserves the frozen pure52 endpoints and completes34,104,108 using three actual M0 pair sums. Releases three mutable original routes only after every old content reader is removed with the replaced source encoders. All costs and arbitrary222 columns remain. No all111 supplier or kappa.')
    w['retained_d4_cohort']={k:copy.deepcopy(b['cohort'][k])for k in ['meet','targets','frames','fields']}
    del w['cohort']
    w['base_word_sha256']=PIN
    after,nt,_=replay(w,collect=True)
    values,locations=nt[newcut]
    require(len(w['targets'])==55 and len(w['released_carriers'])==69,'actual target/carrier counts')
    for i in range(N):
        require(values[f'X{i}']==1<<i,'all originals raw at actual new cut')
        if i in w['released_carriers']:require(locations[f'X{i}']==f'L{i}','retained native original')
        if i in w['targets']:
            require(values[f'Y{i}']==(1<<(N+i))^(1<<i)and locations[f'Y{i}']==f'F{i}','completed output at native facet')
        else:require(values[f'Y{i}']==1<<(N+i)and locations[f'Y{i}']=='zero','unfinished output actually raw at ground')
    for f,pair in zip(fields,PAIRS):
        require(values[f]==sum(1<<i for i in pair)and locations[f]=='M0_PAIR_COMMON','actual common pair sum')
    bv,ba=bt[oldcut]
    originals={f'{p}{i}'for p in ['X','Y']for i in range(N)}
    ground=sorted(n for n,z in bv.items()if n not in originals and z and len(chart(b['charts'][ba[n]]))==0)
    require(len(ground)==25,'predecessor individual ground fields')
    require(all(values[n]==bv[n]and len(chart(w['charts'][locations[n]]))==0 for n in ground),'all25 actual named ground fields unchanged')
    for f in b['cohort']['fields']:require(values[f]==bv[f]and locations[f]==ba[f],'first D4 shared code unchanged')
    for i in D:
        require(values[f'M0_PAIR_RAW_{i}']==1<<i and locations[f'M0_PAIR_RAW_{i}']==f'M0_PAIR_FLAG_{i}','real stationary pair cache')
    for p,pair in zip(packets,PAIRS):
        f=fields[int(p[1:])];cap=new.index(['ADD',p,f]);reset=new.index(['ADD',f,p])
        require(nt[cap][0][p]==sum(1<<i for i in pair),'complete real pair source at capture')
        require(nt[reset+1][0][p]==0,'packet reset preserves old lower computation')
    compared=0
    for k,o in enumerate(b['operations'][:-1]):
        ov,oa=bt[k+1];vv,aa=nt[mapping[k]]
        for n,z in ov.items():
            if n in fields or(n in packets and k<resets[n]):continue
            if n in{f'X{i}'for i in D}|{f'Y{i}'for i in D}:continue
            require(n in vv and vv[n]==z,('unaffected old record value',k,o,n))
            require(chart(charts[aa[n]])==chart(b['charts'][oa[n]]),('unaffected old record chart',k,n))
            compared+=1
    controls=[]
    for label,event in [
        ('omit new raw cache',['ADD','X21','M0_PAIR_RAW_21']),
        ('omit actual pair source coefficient',['ADD','X34','P0']),
        ('omit actual shared descent',['MOVE','KEEP_C0','M0_PAIR_COMMON']),
        ('omit changed source reset',['ADD','KEEP_C0','P0']),
        ('omit owned retirement',['CLEAR','M0_PAIR_RAW_21'])]:
        bad=copy.deepcopy(w);bad['operations'].remove(event)
        try:replay(bad)
        except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':True,'reason':str(e)})
        else:raise ValueError(('accepted pair omission',label))
    bad=copy.deepcopy(w);bad['operations'].insert(newcut,['ADD','X10','X21'])
    try:replay(bad)
    except(ValueError,KeyError)as e:controls.append({'control':'obsolete original restoration retained','rejected':True,'reason':str(e)})
    else:raise ValueError('obsolete old original restoration was harmless')
    owned={n:z for n,z in values.items()if n not in originals};support=0
    for z in owned.values():support|=z
    for i in range(N):support|=values[f'Y{i}']^(1<<(N+i))
    require(support>>N==0,'pureX retained source and offsets')
    S=[i for i in range(N)if support>>i&1]
    gate={127:37,64:74,1:-74}
    for j in range(1,9):
        gate[1+7*j]=gate.get(1+7*j,0)+74
        gate[7*j]=gate.get(7*j,0)-74
    gl,gh=moment(gate);limit=(gl/6,gh/6)
    q,oq=moment(after['movement_profile']),moment(before['movement_profile'])
    direct=moment({1:len(S),7:222})
    result={'status':'PASS_AUTHOR_ACTUAL_M0_PAIR_EXTENSION_TO55',
        'base_word_sha256':PIN,'native_source_sha256':b['source_sha256'],
        'before':before,'after':after,'new_targets':sorted(set(w['targets'])-set(b['targets'])),
        'all_targets':w['targets'],'actual_new_source_fields':fields,'pairs':PAIRS,
        'retained_native_originals':w['released_carriers'],'native_count':len(w['released_carriers']),
        'unfinished_ground_Y_count':N-len(w['targets']),'new_interface':newcut,
        'unaffected_old_state_comparisons':compared,'removed_operations':removed,
        'mutable_original_dead_reads':donor_reads,'mutable_original_removed_writes':donor_writes,
        'all25_named_ground_fields_unchanged':ground,'first_D4_fields_unchanged':b['cohort']['fields'],
        'live_owner_count':len(owned),'live_owner_rank':len(binary_basis(owned.values())),
        'actual_source_coordinate_support':S,'source_coordinate_support_count':len(S),
        'whole_moment':record(q),'moment_increment':record((q[0]-oq[1],q[1]-oq[0])),
        'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),
        'conditional_raw_source_reset_reference':record(direct),
        'controls':controls,'scope':w['scope']}
    a.out.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(data)
    result['word_sha256']=hashlib.sha256(data).hexdigest()
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['status','word_sha256','after','source_coordinate_support_count','whole_moment','necessary_limiting_room']},indent=2))


if __name__=='__main__':main()
