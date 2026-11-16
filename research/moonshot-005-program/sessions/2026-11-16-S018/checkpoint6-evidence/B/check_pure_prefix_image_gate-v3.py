#!/usr/bin/env python3
"""Bounded discovery with new pulled-back phase controls and coordinate frames.

Reuses the pinned exact one-column dyadic word engine. Modular samples and
width-one unit tests are filters only, never universal impossibility proofs.
"""
from pathlib import Path
import argparse,sys,json,itertools,time,random
p0=argparse.ArgumentParser();p0.add_argument('--repo',type=Path,required=True);p0.add_argument('--out',type=Path,required=True);p0.add_argument('--seconds',type=int,default=900);p0.add_argument('--start',type=int,default=0);p0.add_argument('--count',type=int,default=16);opts=p0.parse_args()
repo=opts.repo;base=repo/'research/moonshot-005-program/results/complex-four-bit-family/audit/discovery'
helper=(base/'nonclifford_sector_search.py').read_text().split("if __name__=='__main__':")[0].replace("repo=Path('/workspace/scratch/6e036830f982/programme')",'repo=Path('+repr(str(repo))+')')
script=(base/'four_bit_caller_search.py').read_text();loader="exec(Path(__file__).with_name('nonclifford_sector_search.py').read_text().split(\"if __name__=='__main__':\")[0])"
prefix=script.replace(loader,'').split('profile=tuple(map(int,args.profile))')[0]
sys.argv=[__file__,'--sourcegauges','--orientation','010','--profile','421'];exec(compile(helper,str(base/'nonclifford_sector_search.py'),'exec'));exec(compile(prefix,str(base/'four_bit_caller_search.py'),'exec'))
def eye3():return [[comb((I,1))if r==c else{}for c in range(3)]for r in range(3)]
def diag(gs):return [[comb((gs[r],1))if r==c else{}for c in range(3)]for r in range(3)]
def scalecom(d,k):return {g:x*k%p for g,x in d.items()if x*k%p}
def addcom(x,y):
 z=x.copy()
 for g,c in y.items():z[g]=(z.get(g,0)+c)%p
 return {g:c for g,c in z.items()if c}
def route(perms,D):
 out=[[{}for _ in range(3)]for _ in range(3)];iv2=pow(2,-1,p)
 for sector,pm in enumerate(perms):
  proj=comb((I,iv2),(D,iv2 if sector==0 else-iv2))
  for c in range(3):out[pm[c]][c]=addcom(out[pm[c]][c],proj)
 return out
L=[[comb((A,1)),{},{}],[comb((I,1)),comb((A,1)),{}],[{},{},comb((I,1))]];U=[[comb((A,1)),comb((A.power(2),-1)),{}],[{},comb((A,1)),{}],[{},{},comb((I,1))]]
Ha=Ai.power(2)@Ds[1].power(2)@A.power(2);Hb=Ai.power(2)@Ds[2].power(2)@A.power(2)
assert kind(Ha)==kind(Hb)==0 and Ha.power(2)==Hb.power(2)==I and Ha@Hb==Hb@Ha
pull=[I,Ha,Hb,Ha@Hb]
perms4=[]
for pm in itertools.permutations(range(4)):
 mp=[sum(((x>>j)&1)<<pm[j]for j in range(4))for x in range(16)];perms4.append(m.monomial(mp,[0]*16))
HS=list(dict.fromkeys([h@g for h in pull for g in perms4]+[h@g for h in pull for g in [S,S.star(),r2,r2.star(),l4,r4,tt]]))
# Add source-bit parity/quarter twists on the simplest new channels.
HS=list(dict.fromkeys(HS+[d@h for d in [Ds[b].power(e)for b in(1,2,4,8)for e in(1,2,3)]for h in pull]))
nv=9*len(HS);MHS=[mmg(g)for g in HS]
# Boolean-controlled first routes have an actual transported ordinary decoder.
first_pairs=[((0,1,2),(1,2,0)),((0,2,1),(1,0,2)),((0,1,2),(0,2,1)),((1,0,2),(1,2,0))]
rng=random.Random(2026111601802)
masks=[]
for mon in range(1,16):
 masks.append(sum((1 if (x&mon)==mon else 0)<<x for x in range(16)))
masks+= [rng.randrange(1,65535)for _ in range(17)]
masks=list(dict.fromkeys(masks))
kind=lru_cache(None)(kind)
def group_for(hp,hm):
 r=hp@hm;rot=[I];v=r
 while v!=I:
  rot.append(v);v=v@r
  if len(rot)>96:raise RuntimeError('Bounded ordinary group grew too large')
 G=list(dict.fromkeys(rot+[x@hm for x in rot]));idx={g:i for i,g in enumerate(G)}
 table=[[idx[x@y]for y in G]for x in G]
 return G,table

def regular(vec,table):
 n=len(table);out=[[0]*(3*n)for _ in range(3*n)]
 for i,j,e in itertools.product(range(3),range(3),range(n)):
  z=vec[(i*3+j)*n+e]
  if z:
   for v in range(n):out[i*n+table[e][v]][j*n+v]=(out[i*n+table[e][v]][j*n+v]+z)%p
 return out

# Active-swap enlargement of the rank-four-capable spectator CNOT family.
spm=(0,3,2,1);bspec=m.monomial([(x&3)+4*spm[x>>2]for x in range(16)],[0]*16)
cc=r2.star()@bspec@r2
ba=m.monomial([((x&1)<<1)|((x&2)>>1)|(x&12)for x in range(16)],[0]*16)
J=r2.star()@ba@r2
cz=m.monomial(list(range(16)),[2*int((x&3)==3)for x in range(16)])
assert J.power(2)==cc.power(2)==I and J@Ha@J==Hb and J@Hb@J==Ha
assert all(J@g==g@J for g in (cc,Ds[1],Ds[2],cz))
assert kind(A@J@Ai)==2 and kind(A.power(3)@J@A)==4
labels=list(itertools.product(range(2),range(2),range(2),range(4),range(4),range(2),range(2)))
HS=[Ha.power(u)@Hb.power(v)@J.power(ja)@Ds[1].power(da)@Ds[2].power(db)@cz.power(z)@cc.power(e)for u,v,ja,da,db,z,e in labels]
assert len(set(HS))==len(set(canon(g)[0]for g in HS))==512
nv=9*len(HS);MHS=[mmg(g)for g in HS]
# Product of faithful induced-character representations: D8 x spectator64.
reps=[]
for ha,hb,r,t,zc in itertools.product((1,-1),(1,-1),range(4),range(4),range(2)):
 mats=[]
 for u,v,ja,da,db,z,e in labels:
  av=[ha**u*hb**v,hb**u*ha**v]
  sv=[pow(iu,(r*da+t*db+2*zc*z)%4,p),pow(iu,(r*(da+db+2*z)+t*db+2*zc*(db+z))%4,p)]
  mat=[[0]*4 for _ in range(4)]
  for ac,sc in itertools.product(range(2),repeat=2):
   ar=ac^ja;sr=sc^e;mat[2*ar+sr][2*ac+sc]=av[ar]*sv[sr]%p
  mats.append(mat)
 reps.append((4,mats))
assert len(reps)==128

def unit_all_irreps(vec):
 for d,mats in reps:
  M=[[0]*(3*d)for _ in range(3*d)]
  for r,c in itertools.product(range(3),repeat=2):
   block=vec[(3*r+c)*len(HS):(3*r+c+1)*len(HS)]
   for z,mat in zip(block,mats):
    if z:
     for x,y in itertools.product(range(d),repeat=2):M[r*d+x][c*d+y]=(M[r*d+x][c*d+y]+z*mat[x][y])%p
  if rank(M)<3*d:return False
 return True

def route4(perms,D):
 out=[[{}for _ in range(3)]for _ in range(3)];iv4=pow(4,-1,p)
 for sector,pm in enumerate(perms):
  proj=comb(*[(D.power(j),iv4*pow(iu,(-sector*j)%4,p))for j in range(4)])
  for c in range(3):out[pm[c]][c]=addcom(out[pm[c]][c],proj)
 return out
perms3=list(itertools.permutations(range(3)))
routes=[]
for pm,qn in itertools.product(perms3,repeat=2):
 routes.append((pm,qn,pm,qn))
routes.sort(key=lambda pp:0 if pp[0]==(1,0,2)and pp[1]==(1,2,0)else 1)
for _ in range(24):routes.append(tuple(rng.choice(perms3)for _ in range(4)))
routes=list(dict.fromkeys(routes))
from hashlib import sha256
from collections import Counter
from check_triangular_first_interstage import add as pa,mul as pp,neg as pn,atom as pat,mm as pmm
one,zero={():1},{}
def product(*xs):
 z=one
 for x in xs:z=pp(z,x)
 return z
ax,sx,bx,cx,tx,dx,ex,ux,fx,gx=map(pat,('a','s','b','c','t','d','e','u','f','g'));a2=product(ax,ax);LL=[[ax,zero,zero],[one,ax,zero],[zero,zero,one]];UU=[[ax,pn(a2),zero],[zero,ax,zero],[zero,zero,one]];CC=[[sx,bx,cx],[tx,dx,ex],[ux,fx,gx]]
K=[product(ax,sx,ax),product(ax,tx,ax),zero];W=[zero,sx,ux];Z=[product(ax,bx,ax),pa(product(bx,ax),product(ax,dx,ax)),product(fx,ax)];F=[product(ax,cx),pa(cx,product(ax,ex)),gx]
assert pmm(pmm(LL,CC),UU)==[[pa(K[r],product(W[r],ax)),pa(pn(product(K[r],ax)),pn(product(W[r],a2)),Z[r]),F[r]]for r in range(3)]
G=set(HS)
for gen in(Ha,Hb,J,Ds[1],Ds[2],cz,cc):assert all(gen@h in G for h in HS)
checks=[];word_hash=sha256()
for j in range(4):
 d=Ds[4].power(j);r2k=kind(A@d@A);r3k=kind(A@d@A.power(2));assert(r2k,r3k)==(2,3)
 census=Counter()
 for h in HS:
  word=A@d@A.power(2)@h@A;knd=kind(word);census[knd]+=1;word_hash.update(repr((word.k,word.a)).encode())
 assert census==Counter({4:512});checks.append({'quarter_c_power':j,'double_rank':r2k,'triple_rank':r3k,'four_source_census':dict(census)})
for r in range(4):assert A@Ds[2].power(r)==Ds[1].power(r)@A
mixed=Counter(kind(A@J@A.power(2)@h@A)for h in HS);assert mixed==Counter({2:256,3:256})
proof=Path(__file__).with_name('PURE-PREFIX-IMAGE-GATE-v3.md');baseproof=Path(__file__).with_name('INVERSE-CUT-SUPPORT-GATE-v2.md')
result={'status':'PASS_AUTHOR_PREFIX_IMAGE_GATE_V3_SOURCE_CONTROLS','scope':'The v3 written theorem gives pure-quartic and ordinary-prefix-range sufficient hypotheses. These exact source controls establish the retained O_bc/G512 pure-quartic instance; the separate residue-selective checker tests the concrete ordinary-range branch. No finite failed search is used.','formal_prefix':True,'actual_group_order':512,'projective_classes':512,'closure_under_all_generators':True,'first_coefficient_generators':16,'four_source_words_checked':2048,'literal_word_digest':word_hash.hexdigest(),'source_class_checks':checks,'actual_Db_to_Da_transport':True,'mixed_J_control_census':dict(mixed),'proof_sha256':sha256(proof.read_bytes()).hexdigest(),'inverse_cut_proof_sha256':sha256(baseproof.read_bytes()).hexdigest(),'word_engine_pins':{str(x.relative_to(repo)):sha256(x.read_bytes()).hexdigest()for x in(base/'nonclifford_sector_search.py',base/'four_bit_caller_search.py')}}
result['helper_dependencies']={x.name:sha256(x.read_bytes()).hexdigest() for x in (Path(__file__).with_name('check_triangular_first_interstage.py'),baseproof)};opts.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],result['proof_sha256'])
