#!/usr/bin/env python3
"""Exact source-derived two-by-two determinant and minimal-rank certificate."""
from pathlib import Path
import argparse,gzip,json,hashlib
from build import *
pa=argparse.ArgumentParser();pa.add_argument('--source',type=Path,required=True);pa.add_argument('--output',type=Path,required=True);args=pa.parse_args();raw=args.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==OLD,'old source authentication');w=json.loads(gzip.decompress(raw));_,T,S,H,P,U,g,L,B,D=prepare(w)
C=mm(trans([g[h]for h in S]),[g[h]for h in S]);A0=[[F(i==j)-C[i][j]for j in range(8)]for i in range(8)];M=[[-x for x in row]for row in mm(C,inverse(A0))];u=list(map(F,['1','1/2','2','1/2','9/2','-3/2','1/2','-5/2']));v=list(map(F,['0','1','0','-1','1/2','1/2','-1/2','1/2']));Mu=[sum(M[i][j]*u[j]for j in range(8))for i in range(8)];Mv=[sum(M[i][j]*v[j]for j in range(8))for i in range(8)];aa=dot(u,Mu);bb=dot(v,Mv);cc=dot(u,Mv);K=[[L[i][j]-int(i==j)for j in range(8)]for i in range(8)];small=[[F(i==j)-x for j,x in enumerate(row)]for i,row in enumerate(mm(L,C))];need(determinant(small)==determinant(A0)*(1+aa*bb-cc*cc)==2**13*5**8,'two-by-two determinant identity');need(dot(u,v)==0 and dot(u,u)==F(69,2)and dot(v,v)==3,'chosen dyadic wedge');need(ff_rank(A0,127)==6 and ff_rank(K,127)==2 and ff_rank(small,127)==8,'minimal modal rank certificate');need(all(dot(g[h],[sum(L[i][j]*g[h][j]for j in range(8))for i in range(8)])==1 for h in P),'all104 diagonals unchanged')
normal={h:w['frames'][w['initial'][w['source_role_map'][str(h)]]][0]for h in P};violations={}
for name,ports in [('hosted96',H),('full104',P)]:
 bad=[(i,j)for i in ports for j in ports if i!=j and(normal[i]&normal[j]).bit_count()%2];vals=[]
 for i,j in bad:
  z=sum(g[i][a]*K[a][b]*g[j][b]for a in range(8)for b in range(8))
  if z:vals.append(z)
 violations[name]={'forbidden_off_diagonal_ordered_pairs':len(bad),'new_nonzero_forbidden_pairs':len(vals),'coefficient_histogram':dict(Counter(map(str,vals))),'diagonal_defects':0}
out={'status':'PASS_EXACT_RANK_TWO_ARITHMETIC_CERTIFICATE','source_sha256':OLD,'C':[[str(x)for x in row]for row in C],'u':list(map(str,u)),'v':list(map(str,v)),'u_M_u':str(aa),'v_M_v':str(bb),'u_M_v':str(cc),'old_det':str(determinant(A0)),'new_det':str(determinant(small)),'Lambda_det':str(determinant(L)),'u_norm_squared':str(dot(u,u)),'v_norm_squared':str(dot(v,v)),'u_dot_v':str(dot(u,v)),'old_mod127_rank':6,'perturbation_mod127_rank':2,'new_mod127_rank':8,'all104_diagonal_gram_entries':1,'forward_fitting_debt':violations};args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in['status','u_M_u','v_M_v','u_M_v','old_det','new_det','Lambda_det']},indent=2))
