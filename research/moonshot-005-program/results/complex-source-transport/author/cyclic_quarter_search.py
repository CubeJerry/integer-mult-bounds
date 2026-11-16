#!/usr/bin/env python3
"""New four-sector ordinary routing with an exactly testable cyclic Q algebra.

Exploratory modular search, not an exhaustive mathematical obstruction. A
positive unit in the four cyclic sectors has a direct all-width inversion
mechanism after exact coefficient lifting; no one-column span is used as a
substitute for a tensor identity.
"""
from pathlib import Path
import sys
repo=Path('/workspace/scratch/5b84182f4f70/programme')
base=repo/'research/moonshot-005-program/results/complex-four-bit-family/audit/discovery'
helper=(base/'nonclifford_sector_search.py').read_text().split("if __name__=='__main__':")[0]
helper=helper.replace("repo=Path('/workspace/scratch/6e036830f982/programme')",'repo=Path('+repr(str(repo))+')')
script=(base/'four_bit_caller_search.py').read_text()
loader="exec(Path(__file__).with_name('nonclifford_sector_search.py').read_text().split(\"if __name__=='__main__':\")[0])"
script=script.replace(loader,'')
prefix=script.split('profile=tuple(map(int,args.profile))')[0]
sys.argv=[__file__,'--sourcegauges','--orientation','010','--profile','421']
exec(compile(helper,str(base/'nonclifford_sector_search.py'),'exec'))
exec(compile(prefix,str(base/'four_bit_caller_search.py'),'exec'))

def ordinary(g):
    return g.k==0 and all(sum(z!=(0,0)for z in row)==1 for row in g.a)and all(sum(g.a[i][j]!=(0,0)for i in range(N))==1 for j in range(N))and all(z in units for row in g.a for z in row if z!=(0,0))
def eye3():return [[comb((I,1))if r==c else{}for c in range(3)]for r in range(3)]
def diag(gs):return [[comb((gs[r],1))if r==c else{}for c in range(3)]for r in range(3)]
def scalar_det(a):return(a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))%p
def sector_dets(v):
    return [scalar_det([[sum(v[(i*3+j)*4+e]*pow(iu,s*e,p)for e in range(4))%p for j in range(3)]for i in range(3)])for s in range(4)]
def quarter_route(perms):
    out=[[{}for _ in range(3)]for _ in range(3)];iv4=pow(4,-1,p)
    for s,pm in enumerate(perms):
        for c in range(3):
            for e in range(4):
                g=Ds[2].power(e);r=pm[c]
                out[r][c][g]=(out[r][c].get(g,0)+iv4*pow(iu,-s*e%4,p))%p
    return [[{g:z for g,z in row.items()if z}for row in rr]for rr in out]

L=[[comb((A,1)),{},{}],[comb((I,1)),comb((A,1)),{}],[{},{},comb((I,1))]]
U=[[comb((A,1)),comb((A.power(2),-1)),{}],[{},comb((A,1)),{}],[{},{},comb((I,1))]]
clock=S.star()@Ds[2]
bankperms=list(itertools.permutations(range(3)))
configs=[]
for perm1,perm2,perm3,side,mask,sgn in itertools.product(bankperms,bankperms,bankperms,[0,1],[1,2,3],[1,-1]):
    perms=((0,1,2),perm1,perm2,perm3);cr=quarter_route(perms)
    hh=clock if sgn==1 else clock.star()
    dc=diag([hh if mask>>i&1 else I for i in range(3)])
    cc=mm(dc,cr)if side==0 else mm(cr,dc)
    configs.append(({'permutations':perms,'clock_active_mask':mask,'clock_sign':sgn,'clock_side':side},cc))
kinds_k=[('Db',Ds[2]),('Dc',Ds[4]),('L4_Db_L4',l4@Ds[2]@l4),('R4_Dc_R4',r4@Ds[4]@r4)]
assert len({k for nm,k in kinds_k})==len(kinds_k)
targets={r:A.power(r)for r in(1,2,4)}
@lru_cache(None)
def allowed(g,r):return ordinary(targets[r].star()@g)

rng=random.Random(2026111604);start=time.time();found=[];stats={};scopes=0
for kname,k in kinds_k:
    assert k.power(4)==I
    HS=[k.power(e)for e in range(4)];nv=36
    for ci,(desc,C1) in enumerate(configs):
        B=mm(mm(L,C1),U)
        rows=constraints2(B,L)
        good={g:{r:allowed(g,r)for r in targets}for rr,cc,g in rows}
        grank={g:kind(g)for rr,cc,g in rows}
        for mode,rr in itertools.product(['fixed_left_coset','pure_rank_rows'],itertools.permutations((4,2,1))):
            free,piv=sparse_null([row for(r,c,g),row in rows.items()if not(good[g][rr[r]]if mode=='fixed_left_coset'else grank[g]==rr[r])],nv)
            scopes+=1;key=f'{mode}:{len(free)}';stats[key]=stats.get(key,0)+1
            if not free:continue
            for trial in range(20):
                v=sample(free,piv);dets=sector_dets(v)
                if all(dets):
                    found.append({'mode':mode,'k':kname,'C':desc,'ranks':rr,'nullity':len(free),'vector_modp':v,'sector_determinants_modp':dets})
                    print('ALL_SECTOR_UNIT',json.dumps({k:z for k,z in found[-1].items()if k!='vector_modp'}),flush=True)
                    break
        if ci%20==0:
            res={'status':'running','k':kname,'config_index':ci,'configs':len(configs),'scopes':scopes,'nullity_counts':stats,'candidates':found,'seconds':time.time()-start}
            Path(__file__).with_suffix('.json').write_text(json.dumps(res,indent=2)+'\n')
            print(json.dumps({k:z for k,z in res.items()if k!='candidates'}),flush=True)
result={'status':'complete','scope':'Finite four-sector first routing, one cyclic order-four second algebra, phase residue1, field65537,20 unit samples per kernel. No general impossibility or exact coefficient lift claimed.','configs':len(configs),'cyclic_algebras':len(kinds_k),'scopes':scopes,'nullity_counts':stats,'candidates':found,'seconds':time.time()-start}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print('DONE',json.dumps({k:z for k,z in result.items()if k!='candidates'}),flush=True)
