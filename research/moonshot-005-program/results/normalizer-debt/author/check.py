#!/usr/bin/env python3
"""Actual zero-frequency omission replay and the separate class-row tariff."""
import argparse,gzip,hashlib,importlib.util,json,random
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(c,m):
    if not c:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def eye(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def add(a,b,c=1):return [x+c*y for x,y in zip(a,b)]
def span(vs):
    s={0}
    for v in vs:s|={x^v for x in s}
    return s
def replay(c,omit):
    n=c['roles'];rows=eye(n);L=2*c['arms']+1
    for op in c['events']:
        k=op[0]
        if k=='ADD':rows[op[1]]=add(rows[op[1]],rows[op[2]],int(op[3]))
        elif k=='SCALE':rows[op[1]]=[int(op[2])*z for z in rows[op[1]]]
        elif k=='SWAP':rows[op[1]],rows[op[2]]=rows[op[2]],rows[op[1]]
        elif k=='QUERY':rows[op[1]]=add(rows[op[1]],rows[op[2]])
        elif k=='HOST2':
            _,stage,x,y,u,v=op;need([x,y,u,v]==[1,0,L,L+1],'actual four source roles')
            rows[y]=add(rows[y],rows[x]);rows[u]=add(rows[u],rows[v],-1)
            if 2*(stage-1)in omit:rows[y]=[-z for z in rows[y]]
            if 2*(stage-1)+1 in omit:rows[v]=[-z for z in rows[v]]
        elif k in('LAMBDA','IDLE_ONE'):pass
        else:raise ValueError('unknown actual opcode '+k)
    return rows
def witnesses(c,omit,rows):
    a=c['arms'];L=2*a+1;ans=[]
    for bit in sorted(omit):
        stage=bit//2;i=(stage%a)+1;isV=bit%2
        if stage<a and not isV:
            row=i;col=0;v=rows[row][col];need(v%4==2,'left-Y debt modulo4 invariant');kind='left_Y_offdiagonal_2_mod4'
        elif stage>=a and not isV:
            row=col=a+i;v=rows[row][col];need(v==-3,'right-Y diagonal−3 invariant');kind='right_Y_diagonal_minus3'
        elif stage<a:
            row=col=L+i;v=rows[row][col];need(v==-1,'left-V diagonal−1 invariant');kind='left_V_diagonal_minus1'
        else:
            row=col=L+a+i;v=rows[row][col];need(v==3,'right-V diagonal3 invariant');kind='right_V_diagonal3'
        ans.append({'omitted_bit':bit,'kind':kind,'row':row,'column':col,'actual':v,'target':int(row==col)})
    return ans
def main(output):
    pins=json.loads((HERE/'SOURCES.json').read_text())['pins']
    for path,pin in pins.items():need(sha(HERE/path)==pin,'pinned source '+path)
    w=json.loads(gzip.decompress((HERE/'source/R0-minimal.json.gz').read_bytes()));d=w['logical_involution'];P=d['ports']
    R={int(h):{int(j):F(a)for j,a in row.items()}for h,row in d['R_rows'].items()};h=P[0]
    v={j:F(j==h)-R[j].get(h,F(0))for j in P};v={j:a for j,a in v.items()if a}
    need(v and all(sum(a*v.get(j,F(0))for j,a in R[i].items())==-v.get(i,F(0))for i in P),'actual nonzero R0−1 eigenvector')
    checks=[];examples={};rng=random.Random(120056)
    for a in(1,2,6):
        c=json.loads(gzip.decompress((HERE/f'output/a{a}/CALLER.json.gz').read_bytes()));need(c['arms']==a and c['body_dimension']==8,'actual caller shape')
        need(replay(c,set())==eye(c['roles']),'fully normalized caller at actual zero frequency')
        if a<=2:patterns=[{j for j in range(4*a)if mask>>j&1}for mask in range(1,1<<(4*a))]
        else:
            patterns=[{j}for j in range(4*a)]+[set(range(4*a)),set(range(0,4*a,2)),set(range(1,4*a,2))]
            patterns += [{j for j in range(4*a)if rng.getrandbits(1)}for _ in range(32)]
        total=0
        for omit in patterns:
            rows=replay(c,omit);need(rows!=eye(c['roles']),'every tested nonempty omission fails')
            witnesses(c,omit,rows);total+=1
        allbits=set(range(4*a));rows=replay(c,allbits)
        need(rows[0][2*a]==4,'universal all-omitted H_a to A witness4')
        examples[str(a)]={'all_omitted_root_row':{str(j):z for j,z in enumerate(rows[0])if z},
            'all_omitted_witnesses':witnesses(c,allbits,rows)}
        checks.append({'arms':a,'stages':2*a,'roles':c['roles'],'omission_patterns':total,'full_pattern_domain':a<=2,'caller_sha256':sha(HERE/f'output/a{a}/CALLER.json.gz')})
    # Actual geometry for the separately scoped completed-row repair gate.
    normals={int(h):q for h,q in d['normals'].items()};halves={}
    for z in d['halves']:halves.setdefault(z['class'],[]).append(z['ports'])
    geometry=[]
    for c,(A,B)in sorted(halves.items()):
        need(len(A)==len(B)==4,'two real-orthogonal halves')
        need(all((normals[i]&normals[j]).bit_count()%2==int((i in A)==(j in A))for i in A+B for j in A+B),'actual binary pairing diag(J4,J4)')
        need(all(F(i==j)-R[i].get(j,F(0))==int(i==j)for H in(A,B)for i in H for j in H),'both real diagonal D blocks equal I4')
        W=span(normals[h]for h in A+B);K={x for x in W if all((x&normals[h]).bit_count()%2==0 for h in A+B)}
        need(len(W)==16 and len(K)==4 and all(K<span(normals[h]for h in H)<W for H in(A,B)),'actual class W4 and radical K2')
        geometry.append({'class':c,'A':A,'B':B,'binary_pairing_rank':2,'diagonal_rank_sum':8,'W4':sorted(W),'K2':sorted(K)})
    sp=importlib.util.spec_from_file_location('debt_interval',HERE/'source/interval.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
    old=json.loads((HERE/'source/R0-price.json').read_text());room=tuple(F(x)for x in old['sources']['R0-minimal']['conditional_twelve_stage_margin_per_native'])
    gate=p.moment({2:112});need(gate[0]>room[1],'separate class completed rows exceed whole limiting room')
    candidate=p.moment({1:448,2:560,5:448});allowance=tuple(F(x)for x in old['conditional_outside_allowance_per_native'])
    need(candidate[0]>allowance[1],'explicit class-W-to-radical codec fails optimistic invoice')
    result={'status':'PASS_NORMALIZER_DEBT_OMISSION_AND_SCOPED_CLASS_GATE','source_pins':pins,
        'actual_negative_eigenvector':{str(k):str(x)for k,x in v.items()},'zero_frequency_valid_for_every_width':True,
        'omission_checks':checks,'exact_examples':examples,'class_geometry':geometry,
        'class_separated_row_gate':{'profile_lower_bound':{2:112},'moment':p.enc(gate),'actual_minimal_source_room':p.enc(room),
          'explicit_class_codec_profile':{1:448,2:560,5:448},'codec_moment':p.enc(candidate),
          'scope':'No new productive helper credits; one completed payload per separate owned chain; no cross-class sharing or feedback. This is not a lower bound for arbitrary N service.'},
        'new_normalizer_service_constructed':False,'new_kappa':False,
        'scope':'Universal theorem in PROOF.md excludes deleting any nonempty subset of the fixed caller postservices while leaving other operations unchanged. It does not exclude a rescheduled encoded caller or shared nonunitary service.'}
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'patterns':sum(z['omission_patterns']for z in checks),'class_gate':float(gate[0]),'room':float(room[0]),'class_codec':float(candidate[0])},indent=2))
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,default=HERE/'RESULT.json');x=a.parse_args();main(x.output)
