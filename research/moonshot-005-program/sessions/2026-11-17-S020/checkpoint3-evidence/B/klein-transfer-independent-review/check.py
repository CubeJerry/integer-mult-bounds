#!/usr/bin/env python3
"""Independent reconstruction/replay using B's pinned Gaussian-dyadic engine.
The author's checker and arithmetic are not imported.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,itertools,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
ENGINE_SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'

def run(repo,source,out):
    ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==ENGINE_SHA
    spec=importlib.util.spec_from_file_location('B_exact_review_engine',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    data=json.loads((source/'output/WORDS.json').read_text())
    claimed=json.loads((source/'output/RESULT.json').read_text())
    I=m.eye(16);Z=m.zero(16)
    def frac(x,c):
        c=F(c);assert c.denominator&(c.denominator-1)==0
        y=x.scale((c.numerator,0));return m.M(y.a,y.k+c.denominator.bit_length()-1).norm()
    def plus(x):return frac(I+x,F(1,2))
    def minus(x):return frac(I+x.scale((-1,0)),F(1,2))
    def tab(dest,phase):return m.monomial([dest(*[(x>>j)&1 for j in range(4)]) for x in range(16)],[phase(*[(x>>j)&1 for j in range(4)])%4 for x in range(16)])
    Rsrc=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
    Xb=m.monomial([x^2 for x in range(16)],[0]*16)
    A=frac(I.scale((1,1))+Xb.scale((1,-1)),F(1,2))@Rsrc
    s=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
    t=m.monomial([x^12 for x in range(16)],[0]*16)
    s1=A.star()@s@A;s2=A.power(-2)@s@A.power(2)
    t1=A.star()@t@A;t2=A.power(-2)@t@A.power(2)
    h=tab(lambda a,b,c,d:a+2*b+4*(c^(1^a^d))+8*d,lambda a,b,c,d:(1-2*c)*(1^a^d))
    G=m.monomial([0,1,3,5,7,9,4,13,2,8,6,11,10,15,14,12],[0]*13+[2,0,2])
    assert h@h==I and h@s1==s1@h and h@t1==t1@h
    assert m.gaussian_rank(A.power(2)@h@A.power(-2))==0
    assert G@s1@G.star()==s2 and G@h@G.star()==s2@t2
    hp=tab(lambda a,b,c,d:a+2*b+4*(c^(1^a^d))+8*d,lambda a,b,c,d:0)
    assert m.gaussian_rank(A.power(2)@hp@A.power(-2))!=0
    Gp=m.monomial([0,1,3,5,7,9,4,13,2,8,6,11,10,15,14,12],[0]*16)
    assert Gp@h@Gp.star()!=s2@t2
    N0=minus(s1)@plus(h);R2=minus(s2)@minus(t2);E2=plus(s2)@plus(t2)
    V=G@N0;p=I+N0.scale((-1,0));z=V
    assert V.star()@V==N0 and V@V.star()==R2
    assert N0.trace()==(4,0)
    Q=m.block([[Z,V.star().scale((-1,0)),p],[Z,I+R2.scale((-1,0)),V],[I,Z,Z]])
    M=I+E2.scale((-1,0));g=Rsrc.star()@Xb
    assert A@g@A==Rsrc and A.power(2)@g@A==A@Rsrc
    W=m.block([[E2,(M@g).scale((-1,0)),Z],[M,E2@g,Z],[Z,Z,I]])
    Qh=Q@W
    wanted={'Q_column':Q,'Q_column_inverse':Q.star(),'Q_high_low':Qh,'Q_high_low_inverse':Qh.star()}
    # Every factor is unitary: projector rotations, input bank permutation,
    # monomial g and the partial-isometry rotation. Hence adjoints are inverses.
    assert Q@Q.star()==m.eye(48) and Qh@Qh.star()==m.eye(48)
    monos={'I':I,'s2':s2,'t2':t2,'s2t2':s2@t2,'g':g,'G':G,'Gs1':G@s1,'Gh':G@h,'Gs1h':G@s1@h}
    for name,x in list(monos.items()):monos[name+'_inverse']=x.star()
    for name,table in data['tables'].items():
        from_table=m.monomial([x[0] for x in table],[x[1] for x in table]);assert from_table==monos[name]
    def replay(ws,omit=None):
        b=[[I if i==j else Z for j in range(3)] for i in range(3)]
        bound=F(1)
        for k,op in enumerate(ws):
            if k==omit:continue
            if op['op']=='ADD':
                d,src=op['target'],op['source'];b[d]=[x+y for x,y in zip(b[d],b[src])]
            elif op['op']=='SCALE':b[op['bank']]=[frac(x,F(op['coefficient'])) for x in b[op['bank']]]
            elif op['op']=='MONO':b[op['bank']]=[monos[op['name']]@x for x in b[op['bank']]]
            else:raise AssertionError(op)
            bound=max(bound,max(sum(F(abs(x.a[r][c][0])+abs(x.a[r][c][1]),1<<x.k) for x in row for c in range(16)) for row in b for r in range(16)))
        return m.block(b),bound
    expected_counts={'Q_column':{'ADD':15,'SCALE':27,'MONO':24},'Q_column_inverse':{'ADD':15,'SCALE':27,'MONO':24},'Q_high_low':{'ADD':30,'SCALE':53,'MONO':43},'Q_high_low_inverse':{'ADD':30,'SCALE':55,'MONO':43}}
    receipts={};omissions=0
    for name,ws in data['words'].items():
        actual,bound=replay(ws);assert actual==wanted[name]
        counts=dict(Counter(x['op'] for x in ws));assert counts==expected_counts[name]
        adds=[j for j,x in enumerate(ws) if x['op']=='ADD']
        for j in [adds[0],adds[-1]]:assert replay(ws,j)[0]!=wanted[name];omissions+=1
        receipts[name]={'counts':counts,'width_one_gaussian_l1_prefix_control':str(bound),'all_input_columns':True,
                        'universal_prefix_bound':'retain the author\u0027s coefficient-triangle bound; the smaller width-one value is not promoted'}
    # Universal endpoint-gate premises, proved by literal identities then
    # tensor lifting. U s1 U^-1 is nonordinary, so its two left cosets differ.
    U=A.power(2);Tp=A@t@A.star();Pp=plus(Tp);Mp=minus(Tp)
    e=plus(s1)@minus(t1)
    assert e.trace()==(4,0) and N0@e==Z and p@e==e and z@e==Z
    assert U@t1@U.star()==Tp
    assert m.gaussian_rank(U@s1@U.star())==2
    assert U@e==frac(Mp@U+Mp@U@s1,F(1,2))
    assert Pp@U@e==Z
    Ps1=plus(s1);Pt1=plus(t1);E1=minus(s1)@plus(t1)
    M0=Ps1@p+(E1@z).scale((-1,0));M1=Pt1@p+(I+E1.scale((-1,0)))@z
    assert M0@e==e and M1@e==Z and z@e==Z
    # The last-column quadratic kernel is the exact commuting character
    # (-,-,-), with eight traces retained before tensoring.
    tr=[]
    for i,j,k in itertools.product((0,1),repeat=3):
        x=s1.power(i)@t1.power(j)@h.power(k);tr.append({'exponents':[i,j,k],'trace':x.trace()[0]})
    assert [x['trace'] for x in tr]==[16,8,0,0,8,0,8,8]
    rank_rows=[]
    for width in range(1,13):
        D=16**width;defect=sum((-1)**sum(x['exponents'])*x['trace']**width for x in tr)//8
        assert defect==(D-2*8**width)//8
        rank_rows.append({'width':width,'quadratic_last_column_kernel':defect,'quadratic_last_column_rank':D-defect})
    assert N0==minus(s1)@minus(t1)
    I256=m.eye(256)
    def p256(x,sgn):return frac(I256+x.scale((sgn,0)),F(1,2))
    N02=p256(s1.tp(2),-1)@p256(h.tp(2),1)
    R12=p256(s1.tp(2),-1)@p256(t1.tp(2),-1)
    assert N02!=R12
    result={'status':'PASS_INDEPENDENT_KLEIN_TRANSFER_AND_ENDPOINT_GATE_REVIEW',
      'source_proof_sha256':hashlib.sha256((source/'PROOF.md').read_bytes()).hexdigest(),
      'source_words_sha256':hashlib.sha256((source/'output/WORDS.json').read_bytes()).hexdigest(),
      'engine_sha256':ENGINE_SHA,'literal_phase_sensitive_conjugacies':True,
      'all_width_partial_isometry_and_actual_inverse':True,'primitive_receipts':receipts,
      'negative_controls':{'phase_drop_h':True,'phase_drop_G':True,'omitted_ADDs':omissions,'width_one_N0_equals_R1_but_width_two_does_not':True},
      'endpoint_gate':{'partial_column_condition':'p e=e,z e=w e=0, e=Ps1 Mt1',
        'nonordinary_conjugate_support_rank':2,'same_plus_capacity_applies_to_actual_encoder_and_decoder':True,
        'all_completions_with_transferred_last_column_excluded':True,'different_last_columns_not_excluded':True},
      'quadratic_kernel_traces':tr,'quadratic_last_column_ranks':rank_rows,'new_complete_kappa':False}
    out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.name in ('check.py','REVIEW.md','ENDPOINT-GATE.md','RESULT.json')}
    (out/'MANIFEST.json').write_text(json.dumps({'base_remote':'93b11dd75d7ffda723204bd212e5728cbea95592','source_package':str(source),'files':files},indent=2)+'\n')
    print(json.dumps({'status':result['status'],'primitive_receipts':receipts,'gate_scope':result['endpoint_gate'],'rank_controls':rank_rows[:3]},indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();run(a.repo,a.source,a.out)
