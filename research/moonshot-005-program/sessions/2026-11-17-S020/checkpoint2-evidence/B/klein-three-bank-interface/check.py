#!/usr/bin/env python3
"""Exact group, source, all-input word, inverse and invoice controls."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import argparse,hashlib,importlib.util,json,sys

ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
engine=args.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
assert hashlib.sha256(engine.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
sp=importlib.util.spec_from_file_location('klein_exact_engine',engine);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
I=m.eye(16);Z=m.zero(16);roots=(m.O,m.II,(-1,0),(0,-1))
def sm(x,c):
 c=Q(c);assert c.denominator&(c.denominator-1)==0
 y=x.scale((c.numerator,0))
 return m.M(y.a,y.k+(c.denominator.bit_length()-1)).norm()
def add(*xs):
 out=m.zero(xs[0].n)
 for x in xs:out=out+x
 return out
def tab(dest,phase):
 return m.monomial([dest(*[(x>>j)&1 for j in range(4)]) for x in range(16)],[phase(*[(x>>j)&1 for j in range(4)])%4 for x in range(16)])
rot=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
Xb=m.monomial([x^2 for x in range(16)],[0]*16)
A=sm(I.scale((1,1))+Xb.scale((1,-1)),Q(1,2))@rot
s=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
t=m.monomial([x^12 for x in range(16)],[0]*16);st=s@t
assert s@s==t@t==st@st==I and s@t==t@s
assert [g.trace()[0] for g in [I,s,t,st]]==[16,8,0,8]
def mono_table(x):
 assert x.k==0;out=[]
 for j in range(x.n):
  nz=[i for i in range(x.n) if x.a[i][j]!=m.Z];assert len(nz)==1
  out.append([nz[0],roots.index(x.a[nz[0]][j])])
 return out
monos={'I':I,'s':s,'t':t,'st':st}
for j in (1,2):
 for name,g in [('s',s),('t',t)]:
  h=A.power(-j)@g@A.power(j);mono_table(h);monos[f'r{j}{name}']=h
Ht=A@t@A.star();mono_table(Ht);monos['Ht']=Ht
assert Ht@Ht==I and Ht.trace()==(0,0)
assert monos['r1s']==tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0)
assert monos['r2s']==tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0)
assert (A@s@A.star()).k>0

# Universal Klein algebra, independently of a particular physical width.
one=(Q(1),Q(0),Q(0),Q(0));zero=(Q(0),)*4
def ga(*xs):return tuple(sum(x[j] for x in xs) for j in range(4))
def gs(x,c):return tuple(Q(c)*v for v in x)
def gm(x,y):return tuple(sum(x[i]*y[j] for i in range(4) for j in range(4) if i^j==k) for k in range(4))
def ge(u,v):return tuple(Q(z,4) for z in (1,u,v,u*v))
def geye():return [[one if i==j else zero for j in range(3)] for i in range(3)]
def gmm(X,Y):return [[ga(*(gm(X[i][k],Y[k][j]) for k in range(3))) for j in range(3)] for i in range(3)]
es={(u,v):ge(u,v) for u in(1,-1) for v in(1,-1)}
assert ga(*es.values())==one
for ch,x in es.items():
 for ch2,y in es.items():assert gm(x,y)==(x if ch==ch2 else zero)
shears=[(1,0,es[1,1]),(2,0,es[1,1]),(1,0,es[-1,1]),(0,1,gs(es[-1,1],-1)),(1,0,es[-1,1]),(2,0,es[-1,-1]),(0,2,gs(es[-1,-1],-1)),(2,0,es[-1,-1])]
def group_replay(ops):
 X=geye()
 for i,j,c in ops:X[i]=[ga(a,gm(c,b)) for a,b in zip(X[i],X[j])]
 return X
Cg=group_replay(shears);Cig=group_replay([(i,j,gs(c,-1)) for i,j,c in reversed(shears)])
assert gmm(Cg,Cig)==gmm(Cig,Cg)==geye()
assert [Cg[i][0] for i in range(3)]==[(Q(1,2),Q(1,2),0,0),(Q(1,2),0,Q(1,2),0),(Q(1,2),0,0,Q(1,2))]
def physical(x,V=1):
 return add(*(sm(monos[name].tp(V),c) for name,c in zip(['I','s','t','st'],x)))
def compile_shear(i,j,terms):
 out=[]
 for name,c in terms:
  if not c:continue
  if name!='I':out.append({'op':'MONO','bank':j,'name':name})
  out.append({'op':'SCALE','bank':j,'coefficient':str(c)})
  out.append({'op':'ADD','source':j,'target':i})
  out.append({'op':'SCALE','bank':j,'coefficient':str(1/c)})
  if name!='I':out.append({'op':'MONO','bank':j,'name':name})
 return out
def compile_word(ops):return sum((compile_shear(i,j,list(zip(['I','s','t','st'],c))) for i,j,c in ops),[])
Cword=compile_word(shears);Ciword=compile_word([(i,j,gs(c,-1)) for i,j,c in reversed(shears)])
Hword=[{'op':'SCALE','bank':0,'coefficient':'2'}]+compile_shear(1,0,[('I',Q(-1,2)),('Ht',Q(-1,2))])
Hiword=compile_shear(1,0,[('I',Q(1,2)),('Ht',Q(1,2))])+[{'op':'SCALE','bank':0,'coefficient':'1/2'}]
def replay(word):
 X=[[I if i==j else Z for j in range(3)] for i in range(3)];bounds=[Q(1)]*3;peak=Q(1)
 for op in word:
  if op['op']=='ADD':
   i,j=op['target'],op['source'];X[i]=[a+b for a,b in zip(X[i],X[j])];bounds[i]+=bounds[j]
  elif op['op']=='SCALE':
   i=op['bank'];c=Q(op['coefficient']);X[i]=[sm(x,c) for x in X[i]];bounds[i]*=abs(c)
  else:
   i=op['bank'];X[i]=[monos[op['name']]@x for x in X[i]]
  peak=max(peak,*bounds)
 return X,peak
def bm(X,Y):return [[add(*(X[i][k]@Y[k][j] for k in range(3))) for j in range(3)] for i in range(3)]
Id3=[[I if i==j else Z for j in range(3)] for i in range(3)]
Pt=sm(I+Ht,Q(1,2));H=[[sm(I,2),Z,Z],[sm(Pt,-2),I,Z],[Z,Z,I]];Hi=[[sm(I,Q(1,2)),Z,Z],[Pt,I,Z],[Z,Z,I]]
expected={'C':[[physical(x) for x in row] for row in Cg],'C_inverse':[[physical(x) for x in row] for row in Cig],'H':H,'H_inverse':Hi}
words={'C':Cword,'C_inverse':Ciword,'H':Hword,'H_inverse':Hiword};stats={};omitted=0
for name,word in words.items():
 X,peak=replay(word);assert X==expected[name]
 stats[name]={'counts':dict(Counter(x['op'] for x in word)),'prefix_bound':str(peak),'generator_pass_upper_bound':sum(2 if x['name']=='st' else 1 for x in word if x['op']=='MONO')}
 for j,op in enumerate(word):
  if op['op']=='ADD':assert replay(word[:j]+word[j+1:])[0]!=X;omitted+=1
assert bm(expected['C'],expected['C_inverse'])==bm(expected['C_inverse'],expected['C'])==Id3
assert bm(H,Hi)==bm(Hi,H)==Id3

# Actual source and component equations at width1, and transported trace/kernel controls at width2.
B2=A@s@A.power(3);quartic=A.power(4)
gauge_path=args.repo/'research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint2-evidence/B/forward-row-range-and-spectator-kernels/GAUSSIAN-GAUGES.json'
assert hashlib.sha256(gauge_path.read_bytes()).hexdigest()=='7c654a4de1a78f582781edd216bb863d93f0047c27e343005554b2a06e8dee02'
gauges=json.loads(gauge_path.read_text())
for name,word,r in [('A4',quartic,4),('B2',B2,2)]:
 g=gauges[name];assert g['rank']==r;target=I
 for bit in range(r):
  flip=m.monomial([x^(1<<bit) for x in range(16)],[0]*16)
  target=target@sm(I.scale((1,1))+flip.scale((1,-1)),Q(1,2))
 left=m.monomial([x[0] for x in g['left']],[x[1] for x in g['left']]);right=m.monomial([x[0] for x in g['right']],[x[1] for x in g['right']])
 assert left@target@right==word
 assert m.monomial([x[0] for x in g['left']],[0]*16)@target@m.monomial([x[0] for x in g['right']],[0]*16)!=word
widths=[]
for V in(1,2):
 iv=m.eye(16**V);av=A.tp(V);sv=s.tp(V);tv=t.tp(V);gv=st.tp(V);pv=sm(iv+sv,Q(1,2));qv=sm(iv+tv,Q(1,2));em=sm(add(iv,sm(sv,-1),sm(tv,-1),gv),Q(1,4))
 R1=physical(es[-1,-1],V)
 R1=av.star()@R1@av;R2=av.power(-2)@em@av.power(2)
 assert em@em==em and em.trace()==(16**V//4,0)
 assert R1==sm(add(iv,sm(monos['r1s'].tp(V),-1),sm(monos['r1t'].tp(V),-1),monos['r1s'].tp(V)@monos['r1t'].tp(V)),Q(1,4))
 assert R2==sm(add(iv,sm(monos['r2s'].tp(V),-1),sm(monos['r2t'].tp(V),-1),monos['r2s'].tp(V)@monos['r2t'].tp(V)),Q(1,4))
 k0=av@pv@av;k1=av@qv@av
 assert k0@R1==k1@R1==m.zero(16**V)
 assert k0@av@R2==k1@av@R2==m.zero(16**V)
 assert k0.star()@k0+k1.star()@k1==av.star()@(pv+qv)@av
 ht=Ht.tp(V);pout=sm(iv+ht,Q(1,2));b=B2.tp(V);a4=quartic.tp(V)
 assert sm(k0@av.power(2),2)==a4+b
 assert add(k1@av.power(2),sm(pout@k0@av.power(2),-2))==sm(pout@b,-1)
 assert ht.trace()==(0,0) and pout.trace()==(16**V//2,0)
 widths.append({'width':V,'bank_dimension':16**V,'kernel_rank':16**V//4,'source_rank':3*16**V//4,'residue_image_intersection':16**V//2})

# A source/range control: using the active swap in place of the spectator changes the identity.
wrong=monos['r2s'];assert A@wrong@A.power(3)!=B2
result={'status':'PASS_DYADIC_KLEIN_THREE_BANK_SOURCE_INTERFACE','universal_group_inverse':True,'all_input_words':4,'primitive_ADD_omission_controls':omitted,'Gaussian_gauge_phase_controls':2,'width_checks':widths,'invoices':stats,'source_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'gaussian_gauge_sha256':hashlib.sha256(gauge_path.read_bytes()).hexdigest(),'proof_sha256':hashlib.sha256(Path(__file__).with_name('PROOF.md').read_bytes()).hexdigest(),'scope':'Actual all-width first interface and inverse, genuine ordinary kernels and aligned Gaussian4/rank2 source components. Full Q and independent endpoints not supplied.','new_complete_kappa':False}
for name,data in [('RESULT.json',result),('WORDS.json',{'words':words,'tables':{n:mono_table(g) for n,g in monos.items()},'group_shears':[(i,j,[str(x) for x in c]) for i,j,c in shears],'invoices':stats})]:(args.out/name).write_text(json.dumps(data,indent=2)+'\n')
source_paths=[engine,gauge_path,gauge_path.with_name('PROOF.md')]
manifest={'source_repository':'CubeJerry/integer-mult-bounds','source_ref':'93b11dd75d7ffda723204bd212e5728cbea95592','source_files':{str(p.relative_to(args.repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},'generated_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('PROOF.md'),args.out/'RESULT.json',args.out/'WORDS.json']},'credit':'@CubeJerry; preserved source authors; root/C Klein module construction; B dyadic unit and source application; substantial OpenAI assistance.'}
(args.out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(result,indent=2))
