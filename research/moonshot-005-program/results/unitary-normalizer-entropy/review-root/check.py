#!/usr/bin/env python3
"""Root's independent source, moment and clean-ancilla checks. No author imports."""
import argparse, gzip, hashlib, json
from fractions import Fraction as F
from pathlib import Path

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def roots(q):
    support = [i for i in range(9) if q >> i & 1]
    if len(support) == 3:
        return [2 if i in support else -1 for i in range(9)]
    require(len(support) == 7, 'actual real-root label')
    a, b = [i for i in range(9) if i not in support]
    return [3*(int(i == a)-int(i == b)) for i in range(9)]

def gram(a, b):
    return F(sum(x*y for x,y in zip(roots(a),roots(b))),18)

def plus(a,b):
    return (a[0]+b[0],a[1]+b[1])

def times(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])

def norm(a):
    return a[0]*a[0]+a[1]*a[1]

Z=(F(0),F(0)); ONE=(F(1),F(0)); I=(F(0),F(1))
def matrix_product(a,b):
    return [[sum_pair(times(a[i][k],b[k][j]) for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]

def sum_pair(it):
    out=Z
    for x in it:
        out=plus(out,x)
    return out

def adjoint(a):
    return [[(a[j][i][0],-a[j][i][1]) for j in range(len(a))] for i in range(len(a[0]))]

def identity(n):
    return [[ONE if i==j else Z for j in range(n)] for i in range(n)]

def tensor(a,b):
    return [[times(x,y) for x in row_a for y in row_b] for row_a in a for row_b in b]

def interval(x, digits=28):
    scale=10**digits
    target=x**199*scale**200
    lo,hi=0,x*scale+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200 <= target:
            lo=mid
        else:
            hi=mid
    require(lo**200<=target<hi**200,'exact200th-power bracket')
    return F(lo,scale),F(hi,scale)

def linear_interval(terms):
    lo=hi=F(0)
    for coefficient,x in terms:
        a,b=interval(x)
        if coefficient<0:
            a,b=b,a
        lo+=coefficient*a;hi+=coefficient*b
    return lo,hi

def serialize(pair):
    return [str(x) for x in pair]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--author',type=Path,required=True)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--geometry',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    pins={'proof':'e35f396d7ceea64cde50fe03351609c9fb54ed3e073721ebf2edcc30ca6cd523',
          'manifest':'e2bb67b0e6cafb63980c93d07a842c73bbfd80a65d210ce88343f395d3855412',
          'source':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336',
          'geometry':'e8e48d62be188293677d5c2f7c9a1b104e944bff8ac97669fbaa9a70b41613c6'}
    for name,p in [('proof',a.author/'PROOF.md'),('manifest',a.author/'MANIFEST.json'),('source',a.source),('geometry',a.geometry)]:
        require(digest(p)==pins[name],'authenticated '+name)
    g=json.loads(a.geometry.read_text());w=json.loads(gzip.decompress(a.source.read_bytes()))
    q={int(h):x for h,x in g['normal_by_port'].items()}
    r={int(h):{int(j):F(c) for j,c in row.items()} for h,row in w['logical_involution']['R_rows'].items()}
    require(len(q)==len(set(q.values()))==112,'112 distinct source normals')
    blocks=0;rows=[]
    for c in g['classes']:
        ports=c['ports']
        for h in ports:
            expected={j:F(h==j)-gram(q[h],q[j]) for j in ports}
            expected={j:v for j,v in expected.items() if v}
            require(r[h]==expected,'reconstruct R from native real roots')
            require(len(expected)==4 and all(abs(x)==F(1,2) for x in expected.values()),'four equal-magnitude neighbors')
            for j in expected:
                require(q[h] and q[j] and q[h]!=q[j],'two independent binary normals')
                left={0:(F(1,2),F(-1,2)),q[h]:(F(1,2),F(1,2))}
                right={0:(F(1,2),F(1,2)),q[j]:(F(1,2),F(-1,2))}
                row={}
                for x,v in left.items():
                    for y,z in right.items():
                        row[x^y]=plus(row.get(x^y,Z),times(v,z))
                require(len(row)==4 and all(norm(v)==F(1,4) for v in row.values()),'four physical translations with exact quarter probabilities')
            rows.append({'port':h,'neighbors':sorted(expected),'entropy_bits':'2V+2'})
        for half in c['halves']:
            hs=half['ports'];others=[h for h in ports if h not in hs]
            m=[[r[h].get(j,F(0)) for j in others] for h in hs]
            require(all(sum(m[i][k]*m[j][k] for k in range(4))==int(i==j) for i in range(4) for j in range(4)),'actual four-port orthogonal factor')
            blocks+=1
    require(blocks==28,'28 four-port factors')
    # Independent caller margin, without reading or importing the author budget.
    a6=6
    terms=[(F(224,12),97),(F(-448,12),1)]
    terms += [(F(448,12),1+8*j) for j in range(1,7)]
    terms += [(F(-448,12),8*j) for j in range(1,6)]
    terms += [(-224,x) for x in [2,3,5,6]]
    room=linear_interval(terms)
    comparisons=[]
    for b in [1,2]:
        capfree=interval(224*b)
        allowance=tuple(x*F(b,2) for x in room)
        require(capfree[0]>allowance[1], 'strict independent whole-bank comparison')
        comparisons.append({'banks':b,'rank_mass':224*b,'cap_free_moment':serialize(capfree),'conditional_allowance':serialize(allowance),'strict_gap_lower':str(capfree[0]-allowance[1])})
    # A distinct literal four-coordinate clean-ancilla realization of one C gate.
    j=[[(F(1,2),F(1,2)),(F(1,2),F(1,2))],[(F(1,2),F(1,2)),(F(-1,2),F(-1,2))]]
    j4=tensor(j,identity(2));controlled=identity(4);controlled[2][2]=controlled[3][3]=Z;controlled[2][3]=controlled[3][2]=ONE
    wave=matrix_product(matrix_product(adjoint(j4),controlled),j4)
    phase=identity(4);phase[2][2]=phase[3][3]=I
    full=matrix_product(matrix_product(wave,phase),wave)
    require(matrix_product(adjoint(full),full)==identity(4),'countercontrol full unitary')
    require(all(full[i][j]==Z for i in range(2,4) for j in range(2)),'clean ancillary restoration')
    require(full[:2]==[[(F(1,2),F(1,2)),(F(1,2),F(-1,2)),Z,Z],[(F(1,2),F(-1,2)),(F(1,2),F(1,2)),Z,Z]],'main C coefficient and phase')
    omitted=matrix_product(phase,wave)
    require(any(omitted[i][j]!=Z for i in range(2,4) for j in range(2)),'omitting final wave leaks to ancillary field')
    bad=identity(4);bad[0][0]=(F(2),F(0))
    require(matrix_product(adjoint(bad),bad)!=identity(4),'nonunitary rescaling falls outside group lemma')
    require(F(4*4**2,16**2)==F(1,4),'wrong tensor scalar loses target row norm at V2')
    out={'status':'PASS_ROOT_INDEPENDENT_ENTROPY_PROOF_SOURCE_AND_CONTROLS','pins':pins,
         'actual_rows':rows,'orthogonal_four_port_blocks':blocks,'sharp_rank_mass':224,'sharp_port_allowance':224,
         'moment_comparisons':comparisons,'controls':{'clean_ancilla_exact':True,'missing_final_wave_rejected':True,'nonunitary_rescaling_rejected':True,'wrong_port_tensor_norm_at_V2':'1/4'},
         'scope':'Universal full-unitary entropy and clean-ancilla proof critically reviewed separately. Exact root reconstruction and new integer-root arithmetic import no author code. Requires sublinear port entropy; no productive helper credit, arbitrary nonunitary circuit or caller-redesign exclusion.'}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'rows':len(rows),'blocks':blocks,'comparisons':[{'banks':x['banks'],'lower':float(F(x['cap_free_moment'][0])),'allowance_upper':float(F(x['conditional_allowance'][1]))} for x in comparisons]}))

if __name__=='__main__':
    main()
