#!/usr/bin/env python3
from pathlib import Path
import json,argparse,hashlib
WORD='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e'
def basis(rows):
 b={}
 for r in rows:
  while r:
   p=r.bit_length()-1
   if p in b:r^=b[p]
   else:b[p]=r;break
 return b
def rem(b,r):
 for p in sorted(b,reverse=True):
  if r>>p&1:r^=b[p]
 return r
def dual(rows,i):
 b={}
 for r,t in [(r,0)for r in rows]+[(1<<i,1)]:
  while r:
   p=r.bit_length()-1
   if p in b:r^=b[p][0];t^=b[p][1]
   else:b[p]=(r,t);break
  assert r or not t
 v=0
 for p,(r,t)in sorted(b.items()):
  if ((r&v).bit_count()%2)^t:v|=1<<p
 assert v>>i&1 and all(not((v&r).bit_count()%2)for r in rows);return v

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();wr=a.word.read_bytes();assert hashlib.sha256(wr).hexdigest()==WORD;w=json.loads(wr);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));H=w['singular_h'];h0=[j for j in range(111)if H[j]==0];extra=w['history_extra_query_roles'];h1=[j for j in range(111)if H[j]==1 and j not in extra];g0=int(w['extra_source_delivery']['first_retention_hex'],16);g1=int(w['higher_source_delivery']['first_retention_hex'],16)
 banks={'h0':{'ports':[7,11,12],'raw':h0,'rows':[1<<j for j in h0]},'h1':{'ports':[0,28,44],'raw':h1,'rows':[1<<j for j in h1]},'extra':{'ports':[19],'raw':extra,'rows':[1<<j for j in extra]+[g0]},'D3':{'ports':[27],'raw':h0,'rows':[1<<j for j in h0]+[g1]}}
 ground=[1<<j for j in w['targets']];rows=[];visible=[]
 for i in range(111):
  rr=ground+[1<<j for j in range(111)if dot(i,j)==0];vv=[]
  for name,b in banks.items():
   if any(dot(i,d)==0 for d in b['ports']):rr+=b['rows'];vv.append(name)
  rows.append(rr);visible.append(vv)
 known=set(w['targets']);waves=[]
 while True:
  nxt={i for i,rr in enumerate(rows)if rem(basis(rr+[1<<j for j in known]),1<<i)==0};assert known<=nxt
  if nxt==known:break
  waves.append(sorted(nxt-known));known=nxt
 excluded=[{'receiver':i,'visible_banks':visible[i],'dual_hex':hex(dual(rr+[1<<j for j in known],i))}for i,rr in enumerate(rows)if i not in known]
 out={'word_sha256':WORD,'native_source_sha256':w['source_sha256'],'bank_description':{name:{'ports':b['ports'],'raw_indices':b['raw'],'rank':len(basis(b['rows'])),'rows_hex':[hex(r)for r in b['rows']]}for name,b in banks.items()},'freely_given_completed_points':w['targets'],'feedback_waves':waves,'closure':sorted(known),'closure_count':len(known),'excluded':excluded,'all_receivers_see_some_bank':all(visible),'scope':'Optimistic source-separated full-bank grant at allcurrentleafports, fixedgroundpointterminals andfixedP6/P7higherpreloads. Notone-rowachievability.'};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print('closure',len(known),'waves',waves,'excluded',excluded)
if __name__=='__main__':main()
