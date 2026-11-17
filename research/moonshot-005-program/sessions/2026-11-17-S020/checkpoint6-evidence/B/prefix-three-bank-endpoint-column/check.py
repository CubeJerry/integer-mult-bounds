#!/usr/bin/env python3
"""Exact full-column endpoint identity and all ordinary unit words/inverses."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'

def run(repo,out):
 ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==SHA
 spec=importlib.util.spec_from_file_location('prefix_endpoint_exact_engine',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 def scale(x,c):
  re,im=map(F,c);den=max(re.denominator,im.denominator);assert den&(den-1)==0;y=x.scale((int(re*den),int(im*den)));return m.M(y.a,y.k+den.bit_length()-1).norm()
 def inv(c):
  re,im=map(F,c);n=re*re+im*im;assert n;return re/n,-im/n
 def mul(x,y):return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]
 def neg(x):return -x[0],-x[1]
 def tab(n,dest,phase):return m.monomial([dest(*[(x>>k)&1 for k in range(n)]) for x in range(1<<n)],[phase(*[(x>>k)&1 for k in range(n)])%4 for x in range(1<<n)])
 i16=m.eye(16);i4=m.eye(4);R=tab(4,lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);xb=m.monomial([x^2 for x in range(16)],[0]*16)
 a0=scale(i16,(F(1,2),F(1,2)))+scale(xb,(F(1,2),F(-1,2)));a0=a0@R
 r2=tab(4,lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d))
 sab=tab(4,lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0);s0=tab(4,lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0);s10=tab(4,lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0);g0=tab(4,lambda a,b,c,d:c+2*b+4*a+8*d,lambda a,b,c,d:0)
 j0=r2.star()@sab@r2;k0=a0@j0@s0@a0.star();assert k0.k==0 and m.gaussian_rank(k0)==0
 zs=tab(2,lambda s,t:s+2*t,lambda s,t:2*s);zt=tab(2,lambda s,t:s+2*t,lambda s,t:2*t);xs=tab(2,lambda s,t:(s^1)+2*t,lambda s,t:0);xt=tab(2,lambda s,t:s+2*(t^1),lambda s,t:0)
 I=m.eye(64);Z=m.zero(64);a=i4.tensor(a0);S=zs.tensor(s0);S1=zs.tensor(s10);T=zt.tensor(i16);X=xt.tensor(i16);J=i4.tensor(j0);K=zs.tensor(k0);G=xs.tensor(g0)
 assert a.star()@S@a==S1 and a@J@S@a.star()==K and J@S==S@J and G@S1@G.star()==S.scale((-1,0)) and X@T==(T@X).scale((-1,0))
 half=lambda q:scale(q,(F(1,2),0));P=half(I+T);N=half(I+T.scale((-1,0)));Ps=half(I+S);Ns=half(I+S.scale((-1,0)));P1=half(I+S1);N1=half(I+S1.scale((-1,0)))
 c=(F(1,2),F(1,2));d=(F(1,2),F(-1,2));ci=inv(c)
 C=[[Ps@P,Ns.scale((-1,0)),(Ps@N).scale((-1,0))],[J@Ns@P,J@Ps,(J@Ns@N).scale((-1,0))],[N,Z,P]]
 p=N;z=X@P@N1;w=X@G@P@P1
 assert p.star()@p+z.star()@z+w.star()@w==I and P@z==P@w==Z and S1@z==z.scale((-1,0)) and S@w==w.scale((-1,0))
 def mm(A,B):return [[sum_m(A[i][k]@B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
 def sum_m(xs):
  ans=Z
  for x in xs:ans=ans+x
  return ans
 def ident():return [[I if i==j else Z for j in range(3)] for i in range(3)]
 def diag(x,y,z):return [[x,Z,Z],[Z,y,Z],[Z,Z,z]]
 def route(i,j,E):
  q=ident();q[i][i]=q[j][j]=I+E.scale((-1,0));q[i][j]=q[j][i]=E;return q
 Q=mm(mm(diag(I,X,X@G),route(1,2,P@N1)),route(0,2,N));assert [Q[j][2] for j in range(3)]==[p,z,w]
 O0=[[P,scale(N,c),scale(N,neg(c))],[P@X,scale(N,c),scale(N,c)],[Z,P+scale(N,c),N@X]]
 H=[[I,K.star().scale((-1,0)),Z],[I,K.star(),Z],[Z,Z,I]];Hi=[[half(I),half(I),Z],[scale(K,(F(-1,2),0)),half(K),Z],[Z,Z,I]];assert mm(H,Hi)==mm(Hi,H)==ident()
 O=mm(Hi,O0);B=N+scale(P,ci);CG=N+P@G;E21=ident();E21[2][1]=S@J
 Iin=mm(mm(mm(E21,diag(I,X.scale((-1,0)),X@CG)),route(1,2,P@N1)),diag(N+scale(P,c),I,B))
 ell=scale((S@J@z).scale((-1,0))+w,ci)+X@p;assert [Iin[j][2] for j in range(3)]==[Z,scale(z,neg(ci)),ell]
 L=[[a,Z,Z],[I,a,Z],[Z,Z,I]];U=[[a,(a@a).scale((-1,0)),Z],[Z,a,Z],[Z,Z,I]];D=diag(a.power(4),a.power(2),a)
 E=mm(mm(mm(mm(L,C),U),Q),L);target=mm(mm(O,D),Iin)
 assert all(E[j][2]==target[j][2] for j in range(3));assert E!=target
 full=m.block(E);wanted=m.block(target);defect=full+wanted.scale((-1,0));witness=next((i,j,list(v),defect.k) for i,row in enumerate(defect.a) for j,v in enumerate(row) if v!=(0,0));assert witness[1]<128
 mon={'I':I,'S':S,'T':T,'minusT':T.scale((-1,0)),'J':J,'K':K,'X':X,'XG':X@G,'H1':N+P@S1,'DN':P+N.scale((0,1)),'minusX':X.scale((-1,0)),'XCG':X@CG,'SJ':S@J,'minusSJ':(S@J).scale((-1,0))}
 for name,q in mon.items():assert q.k==0 and m.gaussian_rank(q)==0 and q@q.star()==I,name
 def M(name,bank,inverse=False):return {'op':'MONO','name':name,'bank':bank,'inverse':inverse}
 def SC(bank,cf):return {'op':'SCALE','bank':bank,'coefficient':list(map(str,cf))}
 def ADD(target,source):return {'op':'ADD','target':target,'source':source}
 def SH(target,source,terms):return {'op':'SHEAR','target':target,'source':source,'terms':[[name,list(map(str,cf))] for name,cf in terms]}
 def proj(which,cf):return [('I',mul(cf,(F(1,2),0))),('T',mul(cf,(F(1 if which=='P' else -1,2),0)))]
 def h2(i,j,inverse=False):
  ans=[ADD(i,j),SC(j,(-2,0)),ADD(j,i)]
  if inverse:ans +=[SC(i,(F(1,2),0)),SC(j,(F(1,2),0))]
  return ans
 def swap(i,j,h):return h2(i,j)+[M(h,j)]+h2(i,j,True)
 def rot(i,j,h,inverse=False):return [M(h,i)]+swap(i,j,h) if inverse else swap(i,j,h)+[M(h,i)]
 Cw=rot(0,2,'T')+rot(0,1,'S')+[M('J',1)];Cwi=[M('J',1,True)]+rot(0,1,'S',True)+rot(0,2,'T',True)
 Qw=swap(0,2,'T')+swap(1,2,'H1')+[M('X',1),M('XG',2)];Qwi=[M('XG',2,True),M('X',1,True)]+swap(1,2,'H1')+swap(0,2,'T')
 Pw=swap(1,2,'T')+[M('X',2)]+swap(1,2,'minusT')+[M('X',1)]+swap(0,1,'T')+[M('X',1)]
 Pwi=[M('X',1)]+swap(0,1,'T')+[M('X',1)]+swap(1,2,'minusT')+[M('X',2)]+swap(1,2,'T')
 Hw=[M('K',1,True),SC(1,(-1,0))]+h2(0,1);Hwi=h2(0,1,True)+[SC(1,(-1,0)),M('K',1)]
 Ow0=Pw+[SH(2,0,proj('N',c)),SH(0,1,proj('N',(0,-1))),SH(1,0,proj('N',d)),SH(0,1,proj('N',(-1,0))),M('DN',1)]
 Owi0=[M('DN',1,True),SH(0,1,proj('N',(1,0))),SH(1,0,proj('N',neg(d))),SH(0,1,proj('N',(0,1))),SH(2,0,proj('N',neg(c)))]+Pwi
 Ow=Ow0+Hwi;Owi=Hw+Owi0
 def stable(inverse=False):
  # diag(x,x^-1), x=N+cP (or x=N+c^-1P for the inverse).
  if not inverse:return [SH(2,0,proj('N',(-1,0))+proj('P',neg(c))),SH(0,2,proj('P',(0,-1))),ADD(2,0),SH(0,2,proj('P',neg(d)))]
  return [SH(2,0,proj('N',(-1,0))+proj('P',neg(ci))),SH(0,2,proj('P',neg(d))),ADD(2,0),SH(0,2,proj('P',(0,-1)))]
 Iw=stable()+swap(1,2,'H1')+[M('minusX',1),M('XCG',2),SH(2,1,[('SJ',(1,0))])]
 Iwi=[SH(2,1,[('minusSJ',(1,0))]),M('XCG',2,True),M('minusX',1,True)]+swap(1,2,'H1')+stable(True)
 def compile_word(macros):
  ws=[];bounds=[F(1)]*3;peak=F(1)
  for op in macros:
   if op['op']=='SHEAR':
    dst,src=op['target'],op['source'];source_bound=bounds[src]
    for name,cf in op['terms']:
     cf=tuple(map(F,cf));aabs=abs(cf[0])+abs(cf[1]);peak=max(peak,source_bound*aabs)
     if name!='I':ws.append(M(name,src))
     if cf!=(1,0):ws.append(SC(src,cf))
     ws.append(ADD(dst,src));bounds[dst]+=source_bound*aabs;peak=max(peak,*bounds)
     if cf!=(1,0):ws.append(SC(src,inv(cf)))
     if name!='I':ws.append(M(name,src,True))
   else:
    ws.append(op)
    if op['op']=='ADD':bounds[op['target']]+=bounds[op['source']]
    elif op['op']=='SCALE':q=list(map(F,op['coefficient']));bounds[op['bank']]*=abs(q[0])+abs(q[1])
    peak=max(peak,*bounds)
  return ws,peak
 def mono_left(g,x):
  rows=[None]*64
  for j in range(64):
   ii=next(i for i in range(64) if g.a[i][j]!=(0,0));v=g.a[ii][j];rows[ii]=tuple(m.gm(v,w) for w in x.a[j])
  return m.M(tuple(rows),x.k)
 def replay(ws,omit=None):
  bs=ident()
  for k,op in enumerate(ws):
   if k==omit:continue
   if op['op']=='ADD':i,j=op['target'],op['source'];bs[i]=[x+y for x,y in zip(bs[i],bs[j])]
   elif op['op']=='SCALE':bs[op['bank']]=[scale(x,tuple(map(F,op['coefficient']))) for x in bs[op['bank']]]
   else:
    g=mon[op['name']];g=g.star() if op['inverse'] else g;bs[op['bank']]=[mono_left(g,x) for x in bs[op['bank']]]
  return bs
 units={'C':(Cw,Cwi,C,{'ADD':8,'SCALE':8,'MONO':5},{'ADD':8,'SCALE':8,'MONO':5}),'Q0':(Qw,Qwi,Q,{'ADD':8,'SCALE':8,'MONO':4},{'ADD':8,'SCALE':8,'MONO':4}),'O0':(Ow0,Owi0,O0,{'ADD':20,'SCALE':28,'MONO':15},{'ADD':20,'SCALE':28,'MONO':15}),'O':(Ow,Owi,O,{'ADD':22,'SCALE':32,'MONO':16},{'ADD':22,'SCALE':30,'MONO':16}),'I0':(Iw,Iwi,Iin,{'ADD':14,'SCALE':20,'MONO':13},{'ADD':14,'SCALE':20,'MONO':13})}
 receipts={};wordout={};omissions=0
 for name,(fw,bw,want,fc,bc) in units.items():
  f,fp=compile_word(fw);b,bp=compile_word(bw);assert dict(Counter(o['op'] for o in f))==fc,(name,Counter(o['op'] for o in f));assert dict(Counter(o['op'] for o in b))==bc,(name,Counter(o['op'] for o in b))
  got=replay(f);back=replay(b);assert got==want,name;assert mm(got,back)==mm(back,got)==ident(),name
  if name!='O0':
   for ws,target0 in [(f,got),(b,back)]:
    for k,op in enumerate(ws):
     if op['op']=='ADD':assert replay(ws,k)!=target0,(name,k);omissions+=1
  receipts[name]={'forward':fc,'inverse':bc,'uniform_triangle_prefix_forward':str(fp),'uniform_triangle_prefix_inverse':str(bp)};wordout[name]={'forward':f,'inverse':b,'forward_macros':fw,'inverse_macros':bw};print('checked',name,'prefix bounds',fp,bp,flush=True)
 out.mkdir(parents=True,exist_ok=True)
 result={'status':'PASS_EXACT_PREFIX_THREE_BANK_ENDPOINT_COLUMN','scope':'complete ordinary units and exact final input column only; not a full 421 caller','source_relations':True,'bank_dimension_control':64,'unit_all_input_columns':192,'endpoint_column_checked_inputs':64,'primitive_omitted_ADD_failures':omissions,'receipts':receipts,'last_column_exact_endpoint_identity':True,'all_width_basis':'two fixed prefix Pauli bits and literal tensor-tail source identities','other_two_input_columns_not_completed':True,'nonzero_full_endpoint_defect_entry':{'row':witness[0],'column':witness[1],'gaussian_numerator':witness[2],'denominator_power_two':witness[3]},'new_gaussian_queries':0,'new_owners':0,'new_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(out/'WORDS.json').write_text(json.dumps(wordout,indent=2)+'\n');manifest={'engine':ENGINE,'engine_sha256':SHA,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json',out/'WORDS.json']}};(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print(result['status'],'ADD controls',omissions,flush=True)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args();run(args.repo,args.out)
