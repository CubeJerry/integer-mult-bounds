#!/usr/bin/env python3
"""Exact return/clock gauges, paid mixed unit and scoped source equations."""
import argparse,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
def run(repo,out):
 ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==SHA
 sp=importlib.util.spec_from_file_location('mixed_return_exact',ep);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
 def sc(x,v):
  v=F(v);assert v.denominator&(v.denominator-1)==0;y=x.scale((v.numerator,0));return m.M(y.a,y.k+v.denominator.bit_length()-1).norm()
 half=lambda x:sc(x,F(1,2));I=m.eye(16);Z=m.zero(16)
 def tab(dest,phase):return m.monomial([dest(*[(x>>k)&1 for k in range(4)]) for x in range(16)],[phase(*[(x>>k)&1 for k in range(4)])%4 for x in range(16)])
 R=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);X=m.monomial([x^2 for x in range(16)],[0]*16);Cb=half(I.scale((1,1))+X.scale((1,-1)));a=Cb@R
 s=tab(lambda a,b,c,d:a+2*c+4*b+8*d,lambda a,b,c,d:0);h=tab(lambda a,b,c,d:a+2*c+4*b+8*d,lambda a,b,c,d:b-c)
 D=lambda ex:tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:sum(x*y for x,y in zip(ex,(a,b,c,d))))
 Db=D((0,1,0,0));K=R@s;L=K@Db;rights=[D((0,0,1,-1)),D((-1,0,0,1)),D((1,-1,0,0))];B=tab(lambda a,b,c,d:d+2*(1-c)+4*a+8*b,lambda a,b,c,d:0)
 assert s@s==h@h==I and K@Cb==Cb@K and K@Db==Db@K and Cb@Db@Cb==Db@Cb@Db
 assert a@s@a==B and a.star()@rights[0]@a==rights[1] and a.star()@rights[1]@a==rights[2]
 for j in range(1,4):assert a@h@a.power(j)==L@a.power(j)@rights[j-1]
 for j in range(1,6):assert a@s@a.power(j)==B@a.power(j-1)
 mon={'s':s,'h':h,'K':K,'L':L,'B':B,**{f'r{j}':g for j,g in enumerate(rights)}};tables={};roots=[(1,0),(0,1),(-1,0),(0,-1)]
 for name,g in mon.items():
  assert m.gaussian_rank(g)==0 and g@g.star()==g.star()@g==I
  ds=[];ph=[]
  for j in range(16):
   i=next(i for i in range(16) if g.a[i][j]!=(0,0));ds.append(i);ph.append(roots.index(g.a[i][j]))
  tables[name]={'destinations':ds,'phases':ph}
 def rank_g(q):
  counts={sum(v!=(0,0) for v in row) for row in q.a};assert len(counts)==1;n=counts.pop();assert n and n&(n-1)==0
  assert all(n*(v[0]*v[0]+v[1]*v[1])==1<<(2*q.k) for row in q.a for v in row if v!=(0,0));groups={}
  for row in q.a:groups.setdefault(tuple(j for j,v in enumerate(row) if v!=(0,0)),[]).append(row)
  assert len(groups)==16//n
  for cols,rows in groups.items():
   assert len(rows)==n;ph={m.gm(rows[0][cols[0]],u):k for k,u in enumerate(roots)};assert all(row[j] in ph for row in rows for j in cols)
   ex=[[ph[row[j]] for j in cols] for row in rows];masks=[]
   for row in ex:
    dd=[(row[j]-row[0]-ex[0][j]+ex[0][0])%4 for j in range(n)];assert all(v in(0,2) for v in dd);masks.append(sum((v//2)<<j for j,v in enumerate(dd)))
   span={0}
   for x in masks:
    if x not in span:span|={y^x for y in tuple(span)}
   assert set(masks)==span and len(span)==n
  return n.bit_length()-1
 ranks={}
 for name,g,want in [('I',I,[2,3,4]),('h',h,[1,2,3]),('s',s,[0,1,2]),('sh',s@h,[2,3,4])]:
  rs=[rank_g(a@g@a.power(j)) for j in range(1,4)];assert rs==want;ranks[name]=rs
 def sm(xs):
  r=Z
  for x in xs:r=r+x
  return r
 def mm(A,B):return [[sm(A[i][k]@B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
 ident=lambda:[[I if i==j else Z for j in range(3)] for i in range(3)]
 def rot(i,j,g):
  p=half(I+g);n=I+sc(p,-1);q=ident();q[i][i]=q[j][j]=p;q[i][j]=sc(n,-1);q[j][i]=n;return q
 C=mm(rot(1,2,s),rot(0,1,h));Ci=[[C[j][i].star() for j in range(3)] for i in range(3)];assert mm(C,Ci)==mm(Ci,C)==ident()
 Ph=half(I+h);Nh=I+sc(Ph,-1);Ps=half(I+s);Ns=I+sc(Ps,-1)
 assert C==[[Ph,sc(Nh,-1),Z],[Ps@Nh,Ps@Ph,sc(Ns,-1)],[Ns@Nh,Ns@Ph,Ps]]
 assert a@C[0][0]@a.power(2)==half(a.power(3)+a@h@a.power(2))
 assert a@C[1][0]@a.power(2)==sc(a.power(3)+sc(a@h@a.power(2),-1)+a@s@a.power(2)+sc(a@s@h@a.power(2),-1),F(1,4))
 Lower=[[a,Z,Z],[I,a,Z],[Z,Z,I]];Upper=[[a,sc(a@a,-1),Z],[Z,a,Z],[Z,Z,I]];body=mm(mm(Lower,C),Upper)
 assert body[0]==[half(a.power(2)+a@h@a),sc(a.power(2)+sc(a@h@a,-1)+a.power(3)+a@h@a.power(2),F(-1,2)),Z]
 assert [body[j][2] for j in range(3)]==[Z,sc(a@Ns,-1),Ps]
 # D8 exact group relations and character calculation; no width-one inference.
 d=s@h;assert d.power(4)==I and s@d@s==d.star()
 trs=[d.power(j).trace()[0] for j in range(4)];ref=[(s@d.power(j)).trace()[0] for j in range(4)];assert trs==[16,8,0,8] and ref==[8]*4
 e= sc((I+sc(s,-1))@sm(d.power(j) for j in range(4)),F(1,8));assert e==Z
 dims=[(sum(t**w for t in trs)-sum(t**w for t in ref))//8 for w in range(1,7)];assert dims==[(16**w-2*8**w)//8 for w in range(1,7)] and dims[1]==16
 def AD(i,j):return {'op':'ADD','target':i,'source':j}
 def SC(i,v):return {'op':'SCALE','bank':i,'coefficient':str(v)}
 def MO(i,g):return {'op':'MONO','bank':i,'name':g}
 def h2(i,j,iv=False):return [AD(i,j),SC(j,-2),AD(j,i)]+([SC(i,F(1,2)),SC(j,F(1,2))] if iv else [])
 def sw(i,j,g):return h2(i,j)+[MO(j,g)]+h2(i,j,True)
 def rw(i,j,g,iv=False):return [MO(i,g)]+sw(i,j,g) if iv else sw(i,j,g)+[MO(i,g)]
 fw=rw(0,1,'h')+rw(1,2,'s');bw=rw(1,2,'s',True)+rw(0,1,'h',True)
 def replay(word,omit=None):
  q=ident();bounds=[F(1)]*3;peak=F(1)
  for k,op in enumerate(word):
   if k==omit:continue
   if op['op']=='ADD':i,j=op['target'],op['source'];q[i]=[x+y for x,y in zip(q[i],q[j])];bounds[i]+=bounds[j]
   elif op['op']=='SCALE':i=op['bank'];v=F(op['coefficient']);q[i]=[sc(x,v) for x in q[i]];bounds[i]*=abs(v)
   else:i=op['bank'];q[i]=[mon[op['name']]@x for x in q[i]]
   peak=max(peak,*bounds)
  return q,peak
 receipts={};om=0
 for name,word,want in [('forward',fw,C),('inverse',bw,Ci)]:
  q,peak=replay(word);assert q==want and Counter(x['op'] for x in word)=={'ADD':8,'SCALE':8,'MONO':4}
  for k,op in enumerate(word):
   if op['op']=='ADD':assert replay(word,k)[0]!=want;om+=1
  receipts[name]={'ADD':8,'SCALE':8,'MONO':4,'uniform_prefix_bound':str(peak)}
 result={'status':'PASS_RETURN_CLOCK_SOURCE_INTERFACE','scope':'source gauges, paid mixed unit, D8 kernel and scoped Cmix 421 gate; no complete endpoint','inherited_return':'S019/checkpoint3-evidence/C/s3-review actual_return_monomial_A_Sbc_A','all_width_gauge_identities':True,'full_walsh_block_ranks':ranks,'all_unit_input_columns':48,'omitted_ADD_controls':om,'D8_kernel_dimensions_W1_to_W6':dims,'receipts':receipts,'new_gaussian_queries':0,'new_owners':0,'new_kappa':False}
 out.mkdir(parents=True,exist_ok=True);(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(out/'WORDS.json').write_text(json.dumps({'forward':fw,'inverse':bw,'literal_monomials':tables},indent=2)+'\n')
 manifest={'engine':ENGINE,'engine_sha256':SHA,'files':{x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json',out/'WORDS.json']}};(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print(result['status'],'16 ADD omissions',flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.repo,a.out)
