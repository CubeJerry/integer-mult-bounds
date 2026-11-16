#!/usr/bin/env python3
"""Independent integer literal-C census and edge recipes; no verifier imports."""
from pathlib import Path
import argparse,itertools,json,hashlib
roots=((1,0),(0,1),(-1,0),(0,-1))
def add(x,y):return x[0]+y[0],x[1]+y[1]
def mul(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]
def adj(M):return [[(M[j][i][0],-M[j][i][1])for j in range(len(M))]for i in range(len(M))]
def mm(X,Y):
 Z=[[(0,0)for _ in Y[0]]for _ in X]
 for i,j,k in itertools.product(range(len(X)),range(len(Y)),range(len(Y[0]))):Z[i][k]=add(Z[i][k],mul(X[i][j],Y[j][k]))
 return Z
def mt(M,den):
 out=[];seen=set();values=[(den*r,den*s)for r,s in roots]
 for j in range(len(M)):
  ss=[i for i in range(len(M))if M[i][j]!=(0,0)]
  if len(ss)!=1 or ss[0]in seen or M[ss[0]][j]not in values:return None
  i=ss[0];seen.add(i);out.append((i,values.index(M[i][j])))
 return out
def tm(T):
 M=[[(0,0)for _ in T]for _ in T]
 for j,(i,e)in enumerate(T):M[i][j]=roots[e%4]
 return M
def inv(T):
 O=[None]*len(T)
 for j,(i,e)in enumerate(T):O[i]=(j,-e%4)
 return O
def comp(L,R):return [(L[i][0],(e+L[i][1])%4)for i,e in R]
def edges_for(perm):
 cur=list(perm);sw=[]
 for j in range(16):
  if cur[j]!=j:
   u,v=j,cur[j];sw.append((u,v));cur=[v if x==u else u if x==v else x for x in cur]
 assert cur==list(range(16));edges=[]
 for u,v in reversed(sw):
  path=[u]
  for bit in range(4):
   if (u^v)>>bit&1:path.append(path[-1]^(1<<bit))
  fw=list(zip(path,path[1:]));edges.extend(fw+fw[-2::-1])
 out=list(range(16))
 for u,v in edges:
  assert (u^v).bit_count()==1;out=[v if x==u else u if x==v else x for x in out]
 assert out==list(perm)
 for u,v in reversed(edges):out=[v if x==u else u if x==v else x for x in out]
 assert out==list(range(16));translations=sum(2*(3-(u&~(u^v)).bit_count())for u,v in edges)
 assert len(edges)<=105 and translations<=630
 return edges,translations
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root-package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);o=ap.parse_args();dot=lambda x,y:(x&y).bit_count()%2
 census=[];accepted=0
 for perm in itertools.permutations(range(4)):
  for es in itertools.product(range(4),repeat=4):
   # Literal U_xy=i^(1-popcount(x xor y))/2; no preliminary Walsh gauge.
   N=[[(0,0)for _ in range(4)]for _ in range(4)]
   for j,k,x in itertools.product(range(4),repeat=3):N[j][k]=add(N[j][k],roots[((perm[x]^j).bit_count()-(x^k).bit_count()+es[x])%4])
   actual=mt(N,4);f=[(es[x]-x.bit_count()+perm[x].bit_count())%4 for x in range(4)];qs=[q for q in range(4)if all(f[x]==(f[0]+2*dot(q,x))%4 for x in range(4))]
   assert bool(actual)==bool(qs);census.append(int(bool(actual)))
   if actual:
    accepted+=1;t=perm[0];c0=perm[1]^t;c1=perm[2]^t;assert c0 and c1 and c0!=c1 and perm[3]==t^c0^c1;expected=[]
    for k in range(4):
     ell=next(l for l in range(4)if dot(l,c0)+2*dot(l,c1)==k^qs[0]);expected.append((ell,(f[0]+2*dot(ell,t)+ell.bit_count()-k.bit_count())%4))
    assert actual==expected
 assert len(census)==6144 and accepted==384
 # Literal source input phase abd; A numerator has denominator2.
 A=[[(0,0)for _ in range(16)]for _ in range(16)]
 for x in range(16):
  r=(x>>1)|((x&1)<<3);sgn=-1 if(x&11)==11 else 1;A[r][x]=(sgn,sgn);A[r^2][x]=(sgn,-sgn)
 A2=mm(A,A);U=[[(0,0)for _ in range(16)]for _ in range(16)]
 for z,j,k in itertools.product(range(4),repeat=3):U[j+4*z][k+4*z]=roots[(1-(j^k).bit_count())%4]
 R=mt(mm(adj(U),A2),8);assert R is not None
 assert mm(U,tm(R))==[[(x//2,y//2)for x,y in row]for row in A2]
 rootpath=o.root_package/'RESULT.json';data=json.loads(rootpath.read_text());checks=[]
 for entry in data['all24_fibre_permutation_controls']:
  Q=[tuple(x)for x in entry['literal_Q_table']];B=mt(mm(mm(A2,tm(Q)),adj(A2)),16);assert B is not None;sigma=entry['sigma']
  assert all(B[x+4*z][0]//4==sigma[z]for x,z in itertools.product(range(4),repeat=2))
  for z in range(4):
   pm=[B[x+4*z][0]%4 for x in range(4)];ee=[(B[x+4*z][1]-x.bit_count()+pm[x].bit_count())%4 for x in range(4)];assert any(all(ee[x]==(ee[0]+2*dot(q,x))%4 for x in range(4))for q in range(4))
  assert all((Q[x][0]&3)==sigma[x&3]for x in range(16));edges,xx=edges_for([x for x,e in Q]);assert comp(inv(Q),Q)==[(j,0)for j in range(16)]
  checks.append({'sigma':sigma,'literal_B':B,'source_transport':True,'inverse_phases':True,'edge_gates':edges,'edge_count':len(edges),'negative_control_X_count':xx,'phase_passes':1})
 assert len(checks)==24
 negatives=[]
 for name,T in [('broken_fibre',[(4 if x==0 else 0 if x==4 else x,0)for x in range(16)]),('noncharacter_quarter',[(x,int(x==1))for x in range(16)])]:
  assert mt(mm(mm(adj(A2),tm(T)),A2),16)is None;negatives.append(name)
 result={'status':'PASS_B_INDEPENDENT_COMPLETE_SQUARE_NORMALIZER_REVIEW','scope':'Separate literal-C integer census, source-square reconstruction, every root table and independently emitted reversible edge networks. Complete-class theorem rests on the separately reviewed support/character proof.','local_candidates':6144,'local_admitted':accepted,'literal_B_census_sha256':hashlib.sha256(bytes(census)).hexdigest(),'global_count':24*384**4,'diagonal_root_four_count':16**4,'Boolean_count':8**4,'independent_R2_table':R,'global_checks':checks,'negative_controls':negatives,'generic_per_direction_bound':{'three_control_edges':105,'negative_control_X_translations':630,'input_Z4_phase_pass':1,'extra_whole_field_owner':0},'physical_tariff':'O(volume*((f log p)^tau+1)), complete field volume at least16^V, not tensor width V','root_proof_sha256':hashlib.sha256((o.root_package/'PROOF.md').read_bytes()).hexdigest(),'root_result_sha256':hashlib.sha256(rootpath.read_bytes()).hexdigest()}
 o.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ('status','local_admitted','global_count')},indent=2))
if __name__=='__main__':main()
