"""Exact-path discovery filter for mixed orientations and nonlinear clock sectors."""
from pathlib import Path
exec(Path(__file__).with_name('nonclifford_sector_search.py').read_text().split("if __name__=='__main__':")[0])
N=16
I=m.eye(N);X={b:m.monomial([j^b for j in range(N)],[0]*N)for b in[1,2,4,8]};C={b:m.M((I.scale((1,1))+X[b].scale((1,-1))).a,1).norm()for b in X};P=m.monomial([(j>>1)|((j&1)<<3)for j in range(N)],[0]*N)
def kind(g):
 groups={}
 for i,row in enumerate(g.a):
  supp=tuple(j for j,z in enumerate(row)if z!=(0,0));groups.setdefault(supp,[]).append(i)
 sizes={len(z)for z in groups}
 if len(sizes)!=1:return -1
 sz=next(iter(sizes));r=sz.bit_length()-1
 if sz!=2**r or len(groups)!=N//sz or any(len(c)!=len(rr)for c,rr in groups.items()):return -1
 if any(set(a)&set(b)for a,b in itertools.combinations(groups,2)):return -1
 target=I
 for j in range(r):target=target@C[1<<j]
 if g.k!=target.k:return -1
 if {a*a+b*b for row in g.a for a,b in row if a or b}!={a*a+b*b for row in target.a for a,b in row if a or b}:return -1
 for cols,rs in groups.items():
  vec=[]
  for x in rs:
   mask=0
   for j,y in enumerate(cols):
    num=m.gm(g.a[x][y],g.a[rs[0]][cols[0]]);den=m.gm(g.a[x][cols[0]],g.a[rs[0]][y])
    if num==den:pass
    elif num==tuple(-z for z in den):mask|=1<<j
    else:return -1
   vec.append(mask)
  span={0};rank=0
  for x in vec:
   if x not in span:span|={z^x for z in list(span)};rank+=1
  if rank!=r or set(vec)!=span:return -1
 return r
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--loose',action='store_true');ap.add_argument('--coupled',action='store_true');ap.add_argument('--sourcegauges',action='store_true');ap.add_argument('--concentration',action='store_true');ap.add_argument('--orientation');ap.add_argument('--profile',default='421');ap.add_argument('--mask',type=int,default=40960);ap.add_argument('--headsign',type=int,default=0);ap.add_argument('--bothcontrols',action='store_true');ap.add_argument('--fullphase',action='store_true');ap.add_argument('--sector',action='store_true');ap.add_argument('--shears',action='store_true');ap.add_argument('--frames',action='store_true');ap.add_argument('--allbanks',action='store_true');ap.add_argument('--mixed',action='store_true');ap.add_argument('--residue',type=int,default=1);args=ap.parse_args();p=65537;iu=256
Df=m.monomial(list(range(N)),[2*(args.mask>>x&1)for x in range(N)]);S=Df@P;A=C[2]@S;Ai=A.star();H=m.monomial(list(range(N)),[0]*(N-1)+[2]);k=A.star()@H@A
Ds={b:m.monomial(list(range(N)),[int(bool(x&b))for x in range(N)])for b in[1,2,4,8]}
HS=[]
for ex in itertools.product(range(4),repeat=4 if args.fullphase else 2):
 d=I
 for b,e in zip([1,2,4,8]if args.fullphase else[2,4],ex):d=d@Ds[b].power(e)
 HS.extend([d,d@k,d@(A@H@A.star()),d@k@(A@H@A.star())] if args.bothcontrols else [d,d@k])
if args.frames:HS=[d@P.power(j)for d in HS for j in range(4)]
if args.sourcegauges:
 def tab(perm,ph):
  return m.monomial([perm(*[(x>>j)&1 for j in range(4)])for x in range(N)],[ph(*[(x>>j)&1 for j in range(4)])%4 for x in range(N)])
 l4=tab(lambda a,b,c,d:a+2*(b^(c*d))+4*c+8*d,lambda a,b,c,d:c*d*(2*a+2*b-1))
 r4=tab(lambda a,b,c,d:a+2*b+4*(c^(a*b))+8*d,lambda a,b,c,d:a*b*(1+2*c+2*d))
 r2=P.power(2)@r4
 tt=m.monomial([int(f'{x:04b}'[::-1],2)for x in range(N)],[2*(x.bit_count()%2)for x in range(N)])
 gauges=[I,S,S.star(),r2,r2.star(),l4,r4,tt]
 HS=[Ds[2].power(u)@Ds[4].power(v)@g for u,v,g in itertools.product(range(4),range(4),gauges)]
 HS=list(dict.fromkeys(HS))
assert len(HS)==len(set(HS));nv=9*len(HS)
K0=[[comb((I,1)),{},comb((A,1),(I,-1))],[comb((A,1)),{},comb((A,-1))],[comb((I,1)),comb((I,1)),comb((I,-1))]]
K2=[[comb((A.power(2),-1)),{},comb((A,1),(A.power(2),1))],[comb((A,1)),{},comb((A,-1))],[comb((I,1)),comb((I,1)),comb((I,-1))]]
KK=[K0,K2]
def forms(a):
 return [[[comb((I,1)),{},comb((a,1),(I,-1))],[comb((a,1)),{},comb((a,-1))],[comb((I,1)),comb((I,1)),comb((I,-1))]],[[comb((a.power(2),-1)),{},comb((a,1),(a.power(2),1))],[comb((a,1)),{},comb((a,-1))],[comb((I,1)),comb((I,1)),comb((I,-1))]]]
Kstage=[forms(A.star() if args.headsign>>j&1 else A)for j in range(3)]
def constraints2(B,KR):
 rows={}
 for i,j,e in itertools.product(range(3),range(3),range(len(HS))):
  idx=(i*3+j)*len(HS)+e
  for r,c in itertools.product(range(3),repeat=2):
   for a,x in B[r][i].items():
    for b,y in KR[j][c].items():
     g,ph=canon(mul(mul(a,HS[e]),b));key=(r,c,g);row=rows.setdefault(key,{})
     row[idx]=(row.get(idx,0)+x*y*pow(iu,ph*args.residue,p))%p
 return rows
def sparse_null(rows,n):
 piv={}
 for row in rows:
  row={j:x%p for j,x in row.items()if x%p}
  while row:
   j=min(row)
   if j not in piv:
    inv=pow(row[j],-1,p);piv[j]={k:x*inv%p for k,x in row.items()};break
   fac=row[j]
   for k,x in piv[j].items():
    z=(row.get(k,0)-fac*x)%p
    if z:row[k]=z
    elif k in row:del row[k]
  if len(piv)==n:return [],{}
 return [j for j in range(n)if j not in piv],piv

def sample(free,piv):
 v=[0]*nv
 for j in free:v[j]=rng.randrange(p)
 for j,row in sorted(piv.items(),reverse=True):v[j]=-sum(x*v[l]for l,x in row.items()if l!=j)%p
 return v

def rank(a):
 a=[list(r)for r in a];r=0
 for c in range(len(a[0])):
  q=next((i for i in range(r,len(a))if a[i][c]%p),None)
  if q is None:continue
  a[r],a[q]=a[q],a[r];iv=pow(a[r][c]%p,-1,p);a[r]=[x*iv%p for x in a[r]]
  for i in range(r+1,len(a)):
   x=a[i][c]%p
   if x:a[i]=[(u-x*v)%p for u,v in zip(a[i],a[r])]
  r+=1
  if r==len(a):break
 return r

def mmg(g):
 den=pow(pow(2,g.k,p),-1,p);return [[(z[0]+iu*z[1])*den%p for z in row]for row in g.a]
MHS=[mmg(g)for g in HS]
def physical(v):
 out=[[0]*(3*N) for _ in range(3*N)]
 for i,j,e in itertools.product(range(3),range(3),range(len(HS))):
  c=v[(i*3+j)*len(HS)+e]
  if c:
   for r,s in itertools.product(range(N),repeat=2):out[i*N+r][j*N+s]=(out[i*N+r][j*N+s]+c*MHS[e][r][s])%p
 return out
sectors=[('none',[[comb((I,1))if i==j else{}for j in range(3)]for i in range(3)])]
if args.sector:
 for u,v in itertools.combinations(range(3),2):
  Q=[[comb((I,2))if i==j else{}for j in range(3)]for i in range(3)];Q[u][u]=Q[v][v]=comb((I,1),(H,1));Q[u][v]=Q[v][u]=comb((I,1),(H,-1));sectors.append((str((u,v)),Q))
Qs=[]
for sg,bank,(nm,sec),side in itertools.product([0,1,-1] if args.mixed else [1,-1],(range(1,8) if args.allbanks else range(3)),sectors,range(2)if args.sector else range(1)):
 clock=S.star()@Ds[2].power(sg%4) if sg else I;dr=[[comb((clock if ((bank>>i)&1 if args.allbanks else i==bank) else I,1))if i==j else{}for j in range(3)]for i in range(3)];Qs.append((f'{sg}:{bank}:{nm}:{side}',mm(dr,sec)if side==0 else mm(sec,dr)))
if args.shears:
 Qs=[]
 for i,j,hs,coef in itertools.product(range(3),range(3),[1,-1],[1,-1]):
  if i==j:continue
  clock=(S.star()@Ds[2]).power(hs)
  q=[[comb((I,1))if r==c else{}for c in range(3)]for r in range(3)];q[i][j]=comb((clock,coef));Qs.append((f'shear:{i}:{j}:{hs}:{coef}',q))
if args.concentration:
 b0=[[comb((I,z))if z else{}for z in row]for row in[[1,1,0],[-1,0,1],[0,1,0]]]
 Qs=[('concentration_base',b0)]+[(nm+':concentration:'+str(side),mm(q,b0)if side==0 else mm(b0,q))for nm,q in Qs for side in[0,1]]
if args.coupled:
 assert args.sourcegauges
 b0=[[comb((I,z))if z else{}for z in row]for row in[[1,1,0],[-1,0,1],[0,1,0]]]
 def el(i,j,g,coef=1):
  q=[[comb((I,1))if u==v else{}for v in range(3)]for u in range(3)];q[i][j]=comb((g,coef));return q
 Qs=[]
 for first,second,hs,(gn,g),sg,order in itertools.product([(2,0),(2,1)],[(0,2),(1,2),(2,0),(2,1)],[1,-1],[('I',I),('T',tt),('R4',r4)],[1,-1],[0,1]):
  h=(S.star()@Ds[2]).power(hs);e1=el(*first,h);e2=el(*second,g,sg);cc=mm(e1,e2)if order==0 else mm(e2,e1);Qs.append((f'coupled:{first}:{second}:{hs}:{gn}:{sg}:{order}',mm(b0,cc)))
profile=tuple(map(int,args.profile));rrs=[(1,None,2),(2,None,1)]if args.loose else [None]if args.mixed else sorted(set(itertools.permutations(profile)));rng=random.Random(2026111601);start=time.time();counts={};found=[];scopes=0
for ori in ([tuple(map(int,args.orientation))]if args.orientation else itertools.product(range(2),repeat=3)):
 for nm,Q1 in Qs:
  rows=constraints2(mm(mm(Kstage[0][ori[0]],Q1),Kstage[1][ori[1]]),Kstage[2][ori[2]]);kinds={g:kind(g)for r,c,g in rows}
  for rr in rrs:
   free,piv=sparse_null([row for(r,c,g),row in rows.items()if (kinds[g] not in profile if rr is None or rr[r] is None else kinds[g]!=rr[r])],nv);scopes+=1;counts[len(free)]=counts.get(len(free),0)+1
   if not free:continue
   for _ in range(3):
    v=sample(free,piv)
    if rank(physical(v))==3*N:
     
     cr={}
     if rr is None or args.loose:
      for typ in sorted(set(profile)):
       M=[[0]*(3*N) for _ in range(3*N)]
       for (r,c,g),row in rows.items():
        if kinds[g]!=typ:continue
        coeff=sum(z*v[j]for j,z in row.items())%p
        if not coeff:continue
        gm=mmg(g)
        for x,y in itertools.product(range(N),repeat=2):M[r*N+x][c*N+y]=(M[r*N+x][c*N+y]+coeff*gm[x][y])%p
       cr[str(typ)]=rank(M)
     found.append({'orientation':ori,'Q1':nm,'ranks':rr,'component_ranks':cr,'nullity':len(free),'vector_modp':v});print('GOOD_CENSUS' if cr and sum(cr.values())==3*N and all(z==N for z in cr.values()) else 'CANDIDATE',{'orientation':ori,'Q1':nm,'ranks':rr,'component_ranks':cr,'nullity':len(free)},flush=True);break
  print('progress',args.mask,ori,nm,'scopes',scopes,'counts',counts,'found',len(found),'sec',round(time.time()-start,2),flush=True)
result={'scope':'finite exact phase-word filter at fixed width residue, modular scalar solve, necessary width1 physical-unit filter; not theorem or all-width unit','mask':args.mask,'fullphase':args.fullphase,'sector':args.sector,'residue':args.residue,'basis':len(HS),'scopes':scopes,'nullity_counts':counts,'candidates':found,'seconds':time.time()-start};Path(__file__).with_name(f'fourbit_{args.profile}_{args.mask}_{args.fullphase}_{args.sector}_{args.residue}_{args.mixed}_{args.frames}_{args.allbanks}_{args.shears}_{args.headsign}_{args.bothcontrols}_{args.concentration}_{args.orientation}_{args.sourcegauges}_{args.coupled}_{args.loose}.json').write_text(json.dumps(result,indent=2)+'\n');print('DONE',{'candidates':len(found),'seconds':time.time()-start},flush=True)
