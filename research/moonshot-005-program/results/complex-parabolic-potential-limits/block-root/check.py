#!/usr/bin/env python3
import argparse,hashlib,json,random
from pathlib import Path

def rank(a,p):
 a=[row[:]for row in a];k=0
 for j in range(len(a[0])):
  x=next((i for i in range(k,len(a))if a[i][j]%p),None)
  if x is None:continue
  a[k],a[x]=a[x],a[k];inv=pow(a[k][j]%p,-1,p);a[k]=[v*inv%p for v in a[k]]
  for i in range(k+1,len(a)):
   t=a[i][j]%p;a[i]=[(u-t*v)%p for u,v in zip(a[i],a[k])]
  k+=1
 return k

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--table',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();raw=a.table.read_bytes();T=json.loads(raw)['orbit_intersection_matrices'];pairs=[(i,j)for i in range(4)for j in range(i+1,4)];q=[[T[r][i][j]for i,j in pairs]for r in range(1,4)];assert q==[[1,0,0,12,0,32],[0,1,0,3,8,24],[0,0,1,7,7,28]]
 assert [u-v for u,v in zip(q[0],q[1])]==[1,-1,0,9,-8,8]
 assert [5*u-4*v for u,v in zip(q[0],q[2])]==[5,0,-4,32,-28,48]
 rng=random.Random(151202);cases=[]
 for p in[2,3]:
  for k in[1,2,3,4]:
   for _ in range(24):
    A=[[[rng.randrange(p)for j in range(k)]for i in range(k)]for s in range(4)];d=[rank([[(A[s][i][j]-A[t][i][j])%p for j in range(k)]for i in range(k)],p)for s,t in pairs];v=[sum(x*y for x,y in zip(row,d))for row in q];assert v[1]<=v[0]and 4*v[2]<=5*v[0];assert v[0]or not any(d);cases.append({'field':p,'block_size':k,'distances':d,'q':v})
 sharp=[0,1,1,1,1,0];assert [sum(x*y for x,y in zip(row,sharp))for row in q]==[12,12,15]
 vs=[7,3,1,0];sq=[(vs[i]-vs[j])**2 for i,j in pairs];hv=[sum(x*y for x,y in zip(row,sq))for row in q];assert hv[:2]==[96,144]
 out={'status':'PASS_BLOCK_RADIAL_RANK_METRIC_IDENTITIES','table_sha256':hashlib.sha256(raw).hexdigest(),'distance_pair_order':pairs,'q_coefficients':q,'cases':cases,'case_count':len(cases),'sharp_values':[12,12,15],'squared_Hilbert_negative_control':hv,'pauli_block_ratios':[4,6,7],'universal_validity':'Written rank-triangle proof,not finite extrapolation.','new_complete_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':len(cases),'sharp':[12,12,15],'Hilbert_control':hv}))
if __name__=='__main__':main()
