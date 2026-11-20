#!/usr/bin/env python3
"""Use the unconditional Clebsch deficits at exactly the leaves of the normalized tree."""
from collections import Counter
from pathlib import Path
import argparse,gzip,json
def load(f):return json.loads(gzip.decompress(f.read_bytes())if f.suffix=='.gz'else f.read_bytes())
def verify(a):
    c=load(a.weighted);exception={(7,80),(10,81),(80,96),(81,95)};exception|={(j,i)for i,j in exception}
    leaf={tuple(z):(0,1,int(tuple(z)in exception))for z in c['tree']}
    # Left/right row pair and column pair of each rectangle are recorded as i,l and x,y.
    for e,i,l,x,y,clique,charge in c['closure']:
        g=divmod(e,111);parents={(i,x),(i,y),(l,x),(l,y)}-{g}
        w=1+sum(leaf[z][0]for z in parents);n=sum(leaf[z][1]for z in parents);exc=sum(leaf[z][2]for z in parents)
        assert len(parents)==3 and w==charge and n==2*w+1;leaf[g]=w,n,exc
    assert len(leaf)==6470
    def amounts(side,uv,J):
        es=[(j,z)if side=='L'else(z,j) for z in uv for j in J];return [sum(leaf[e][t]for e in es)for t in range(3)]
    def bill(p,h):
        c,n,exc=p
        return c*h+(n-exc)*(7*h//5)+exc*3*h
    cs=load(a.charts);t=load(a.pairs);res={};claims={}
    for side,pair,J in [('L',[1,8],[0,3,5,6,16,17,18,19]),('R',[0,14],[1,3,5,7,10,11,12,47])]:
        info=amounts(side,pair,J);bound=next(h for h in range(1000) if bill(info,h)>=3840)
        res[side]={'weights_leaves_exceptional_leaves':info,'minimum_h_unconditionally_if_half_frozen':bound,'return_q_at_b3840':9*3840+bound,
                   'max_error_at_h49':bill(info,49),'max_error_at_h56':bill(info,56)}
    for row in cs:
        cst=amounts(row['side'],row['pair'],row['opposite']);assert cst[0]==row['cost']
        claims[row['side'],row['plane']]=[cst,row]
    bounds={}
    for h in (49,56):
        for side in 'LR':
            used=[(p,w)for (s,k),(p,w)in claims.items()if s==side]
            # Uniform exact dual. Each row forces a minimum lost-label count and,
            # by the largest site capacities, a minimum support count.
            col=Counter();credit=0;ccol=Counter();ccred=0;positive=0
            for p,w in used:
                gs=8*sum(v[2]-min(v[:2])for v in w['sector_ranks']);t=max(0,(gs-bill(p,h)+63)//64)
                if not t:continue
                m={int(d):q for d,q in w['chart_multiplicities'].items()};positive+=1;credit+=t;col.update(m);qq=sorted(m.values(),reverse=True)
                km=next(z for z in range(len(qq)+1)if sum(qq[:z])>=t);ccred+=km;ccol.update(m.keys())
            bounds[f'{side}/{h}']={'number_strict_constraints':positive,'unconditionally_at_least_changed_D':max((credit+max(col.values())-1)//max(col.values()),(ccred+max(ccol.values())-1)//max(ccol.values()))}
    out={'exceptional_tree_edges':sorted(exception&{tuple(z)for z in c['tree']}),'two_original_witnesses':res,'global_census_basic_bound':bounds}
    a.out.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out)
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for arg in ('weighted','charts','pairs','out'):p.add_argument('--'+arg,type=Path,required=True)
 verify(p.parse_args())
