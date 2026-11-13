#!/usr/bin/env python3
"""Root's independent review of B's coordinate-return algebra and certificates."""
import argparse,gzip,hashlib,importlib.util,itertools,json
from fractions import Fraction as F
from pathlib import Path
def need(q,m):
    if not q:raise ValueError(m)
def rank(rows):
    pivots={}
    for v in rows:
        r={j:F(x) for j,x in enumerate(v) if x}
        while r:
            p=min(r)
            if p not in pivots:
                c=r[p];pivots[p]={j:x/c for j,x in r.items()};break
            c=r[p]
            for j,x in pivots[p].items():
                r[j]=r.get(j,F(0))-c*x
                if not r[j]:del r[j]
    return len(pivots)
def main(a):
    p=a.rail/'extract_rail.py';sp=importlib.util.spec_from_file_location('root_rail_engine',p)
    e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
    sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    need(hashlib.sha256(sb).hexdigest()==e.SOURCE_PIN,'Native pin')
    s=json.loads(gzip.decompress(sb));qb=(a.rail/'rail-repaired.json.gz').read_bytes()
    need(hashlib.sha256(qb).hexdigest()=='90440c9115da1b98242113832c296faf314caf0ab7e0743119275dbfc372c9d2','Root rail pin')
    q=json.loads(gzip.decompress(qb));rows,loc,_=e.run(q['program'],q['initial'],400,q['owned_fields'],list(map(e.span,q['frames'])),{i:{i:F(1)} for i in range(400)})
    private={int(k):v for k,v in q['source_role_map'].items()}
    hosted={s['live'][k]:(b,d) for k,b,d in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
    author=json.loads((a.author/'ACTUAL-M.json').read_text());H=author['H'];K=author['K']
    need(set(H)==set(hosted) and len(H)==96,'Exactly original hosted ports')
    M=[]
    for i in H:
        b,d=hosted[i];res=e.plus(rows[private[b]],{private[b]:F(1),private[d]:F(-1)},F(-1))
        need(set(res)<=set(private[hosted[j][1]] for j in H),'No uncounted non-D residual')
        M.append([res.get(private[hosted[j][1]],F(0)) for j in H])
    need(M==[[F(x) for x in r] for r in author['M']],'Root full-input rail reproduces author residual')
    need(rank(M)==82,'Actual rank82')
    cert=json.loads((a.author/'COORDINATE-RETURN-CERTIFICATE.json').read_text())
    Z=[[F(x) for x in r] for r in cert['kernel_rows']]
    need(len(Z)==96 and all(len(z)==14 for z in Z) and rank(Z)==14,'Complete independent kernel')
    need(all(sum(M[i][j]*Z[j][k] for j in range(96))==0 for i in range(96) for k in range(14)),'MZ=0')
    def projective(z):
        need(any(z),'No weight-one codeword');c=next(v for v in z if v);return tuple(x/c for x in z)
    need(len({projective(z) for z in Z})==96,'No weight-two codeword')
    dependent=[]
    for i,j in itertools.combinations(range(96),2):
        u,v=Z[i],Z[j];p=next(k for k,x in enumerate(u) if x)
        q0=next(k for k in range(14) if u[p]*v[k]!=u[k]*v[p]);det=u[p]*v[q0]-u[q0]*v[p]
        for k in range(j+1,96):
            w=Z[k];x=(w[p]*v[q0]-w[q0]*v[p])/det;y=(u[p]*w[q0]-u[q0]*w[p])/det
            if all(x*u[t]+y*v[t]==w[t] for t in range(14)):dependent.append((H[i],H[j],H[k]))
    need(set(dependent)=={tuple(x['J']) for x in cert['dependent_triples']} and len(dependent)==324,'Complete triple enumeration')
    def root(i):
        n=s['frames'][s['initial'][i]][0];support=[j for j in range(9) if n>>j&1]
        if len(support)==3:return [2 if j in support else -1 for j in range(9)]
        need(len(support)==7,'E8 normal domain');u,v=[j for j in range(9) if j not in support]
        return [3*(int(j==u)-int(j==v)) for j in range(9)]
    weights=[]
    for block in cert['Gram_blocks']:
        kk=block['ports'];vecs=[root(i) for i in kk];need(len(kk)==11 and rank(vecs)==4,'Two rank4 root blocks')
        indices=[H.index(i) for i in kk]
        need(all(M[indices[i]][indices[j]]==F(sum(x*y for x,y in zip(vecs[i],vecs[j])),18) for i in range(11) for j in range(11)),'Real roots match actual Gram block')
        best={d:12 for d in range(1,5)}
        for bits in range(1<<11):
            keep=[vecs[j] for j in range(11) if not (bits>>j&1)];gain=4-rank(keep)
            for d in range(1,gain+1):best[d]=min(best[d],bits.bit_count())
        need(best=={int(k):v for k,v in block['generalized_weights'].items()}=={1:5,2:8,3:10,4:11},'Exact restricted support weights')
        weights.append(best)
    witness=json.loads((a.author/'B7-COORDINATE-CHOICE.json').read_text());J=set(witness['J']);cols=[k for k,i in enumerate(H) if i not in J]
    remaining=[[r[k] for k in cols] for r in M];complete=[H[i] for i,r in enumerate(remaining) if not any(r)]
    need(len(J)==31 and rank(remaining)==58 and complete==witness['completed_original_B'],'Rank58/24 true endpoint distinction')
    # A nonzero native coefficient error must invalidate the unchanged kernel witness.
    mutant=[r[:] for r in M];mutant[0][0]+=1
    need(any(sum(mutant[0][j]*Z[j][k] for j in range(96)) for k in range(14)),'Wrong residual rejected')
    reviewed={f:hashlib.sha256((a.author/f).read_bytes()).hexdigest() for f in ['ACTUAL-M.json','COORDINATE-RETURN-CERTIFICATE.json','B7-COORDINATE-CHOICE.json','COORDINATE-RETURN-LEMMA.md']}
    result={'status':'PASS_ROOT_INDEPENDENT_COORDINATE_REVIEW','source_pin':e.SOURCE_PIN,'root_rail_pin':hashlib.sha256(qb).hexdigest(),
      'rank':82,'kernel_dimension':14,'minimum_coordinate_return_rank_gain_price':3,'dependent_triples':len(dependent),
      'restricted_block_weights':weights,'B7_return_count':31,'B7_residual_rank':58,'B7_individually_complete':len(complete),
      'wrong_residual_rejected':True,'reviewed_author_files':reviewed,
      'scope':'Independent actual residual, kernel, support and endpoint checks. Does not review separate E6/D6/D5 flat census or infer universal optimality.'}
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for x in ['repo','rail','author','output']:ap.add_argument('--'+x,type=Path,required=True)
    main(ap.parse_args())
