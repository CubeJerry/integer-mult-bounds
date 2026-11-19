#!/usr/bin/env python3
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip,json

def binary_basis(vectors):
    pivots={}
    for value in vectors:
        v=value
        while v:
            bit=v.bit_length()-1
            if bit in pivots:v^=pivots[bit]
            else:pivots[bit]=v;break
    return list(pivots.values())

def gf32_times_t(a):
    b=a<<1
    return b^0x25 if b&32 else b

def expand_field_columns(columns):
    out=[]
    for col in columns:
        assert len(col)==240 and all(0<=v<32 for v in col)
        v=list(col)
        for _ in range(5):
            out.append(sum(x<<(5*j)for j,x in enumerate(v)))
            v=[gf32_times_t(x)for x in v]
    return out

def solve_columns(columns,target):
    pivots={}
    for j,value in enumerate(columns):
        v=value;coef=1<<j
        while v:
            bit=v.bit_length()-1
            if bit in pivots:
                w,c=pivots[bit];v^=w;coef^=c
            else:pivots[bit]=(v,coef);break
    v=target;answer=0
    while v:
        bit=v.bit_length()-1;w,c=pivots[bit];v^=w;answer^=c
    return answer

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    wp=a.author/'output/WITNESS.json.gz';raw=gzip.decompress(wp.read_bytes());wit=json.loads(raw)
    layoutp=a.repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    lr=gzip.decompress(layoutp.read_bytes());assert sha256(lr).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
    lay=json.loads(lr);R=lay['root_table'];H=list(map(set,lay['A2']));D=list(map(set,lay['D4']))
    spaces={int(k):v for k,v in wit['spaces'].items()};selected=[640,726,845,81,88,93,118,123,138,395,442,443,473,558,564,605,663,672,693,696,706,708,717,771,774,803,835,849,865,937,974,991,1053]
    assert set(selected)==set(spaces) and len(selected)==33
    ranks={d:len(binary_basis(expand_field_columns(spaces[d]))) for d in selected}
    assert [ranks[d] for d in selected[:3]]==[45]*3
    assert all(ranks[d]==35 for d in selected[3:])
    total=len(binary_basis([x for d in selected for x in expand_field_columns(spaces[d])]))
    three=len(binary_basis([x for d in selected[:3] for x in expand_field_columns(spaces[d])]))
    assert total==sum(ranks.values())==1185 and three==135
    duplicate=len(binary_basis([x for d in [640,726,640] for x in expand_field_columns(spaces[d])]))
    assert duplicate==90
    orth=[{j for j,v in enumerate(R)if sum(x*y for x,y in zip(u,v))==0}for u in R]
    four_flags={}
    for d in selected:
        assert D[d]<=orth[10]
        perp={j for j in range(120)if all(j in orth[k]for k in D[d])}
        ks=[h for h,V in enumerate(H)if 10 in V and V<=perp]
        assert len(ks)==4
        four_flags[d]=ks
    rows=[(1<<i)^sum(1<<j for j in orth[i] if j<111)for i in range(111)]
    basis=binary_basis(rows);assert len(basis)==9
    outside=[j for j in range(111)if j not in orth[10]]
    cols={j:sum(((r>>j)&1)<<k for k,r in enumerate(basis))for j in range(111)}
    chosen=[]
    for j in outside:
        if len(binary_basis([cols[k]for k in chosen]+[cols[j]]))>len(chosen):chosen.append(j)
        if len(chosen)==9:break
    assert len(chosen)==9
    completions={}
    for active in [29,36,77]:
        c=solve_columns([cols[j]for j in chosen],cols[active])
        x=(1<<active)^sum(1<<chosen[k]for k in range(9)if(c>>k)&1)
        assert all((x&r).bit_count()%2==0 for r in rows)
        assert all(j==active or j not in orth[10]for j in range(111)if(x>>j)&1)
        completions[active]=[chosen[k]for k in range(9)if(c>>k)&1]
    transcripts={};short={}
    for x0,x1,y0,y1 in product(range(2),repeat=4):
        helper=(x1^(x0&y0),y1^(x0|y0));t=(x0,y0,*helper);target=(x0,x1,y0,y1)
        assert t not in transcripts;transcripts[t]=target
        short.setdefault((x0,y0,helper[0]),set()).add(target)
    assert len(transcripts)==16 and len(short)==8 and all(len(s)==2 for s in short.values())
    Hsmall=[1,2];Asmall=[1,4]
    assert len(binary_basis(Hsmall))==len(binary_basis(Asmall))==2
    h=0;r=len(binary_basis(Hsmall+Asmall))-2;assert r==1 and r>h
    out={'status':'PASS_INDEPENDENT_JOINT_TRIANGLE_CUT_REVIEW','witness_decompressed_sha256':sha256(raw).hexdigest(),
      'binary_expansion':{'field_modulus':'t^5+t^2+1','three_rank':135,'full_rank':1185,'field_full_rank':237,'direct_sum':True,'duplicate_three_rank':90},
      'physical_flags':four_flags,'per_middle_binary_ranks':ranks,
      'canonical':{'rank':9,'outside_restriction_rank':9,'outside_basis_columns':chosen,'explicit_active_completions':completions},
      'abstract_helper_control':{'full_target_states':16,'sharp_transcript_states':16,'one_symbol_short_states':8,'collision_size':2},
      'replacement_scope_control':{'h':h,'r':r},'author_code_imported_or_executed':False,
      'source_to_decoder_reconstructed_here':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status']);print('binary rank',total,'field rank',total//5,'helper floor',total//5-4*33)
if __name__=='__main__':main()
