#!/usr/bin/env python3
"""Exact changed-C kernels, source cancellation and paid unit words/inverses."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
NPINS={'WORDS.json':'910edc04d35cb414202ba275cbc25d1ca21755a7186c9820f88f5f2eecebfe42','PROOF.md':'00087f521760e76198724f4ccd119cbf74fbe7f9b3b4c906df4d560de4130c41'}

def run(repo,normalizer,out):
 for name,h in NPINS.items():assert hashlib.sha256((normalizer/name).read_bytes()).hexdigest()==h,name
 nw=json.loads((normalizer/'WORDS.json').read_text());assert nw['forward'][0]['name']=='R' and nw['inverse'][-1]['name']=='R'
 ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==SHA
 spec=importlib.util.spec_from_file_location('anticommuting_prefix_exact',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 def scale(x,c):
  re,im=map(F,c);den=max(re.denominator,im.denominator);assert den&(den-1)==0;y=x.scale((int(re*den),int(im*den)));return m.M(y.a,y.k+den.bit_length()-1).norm()
 def tab(n,dest,phase):return m.monomial([dest(*[(x>>k)&1 for k in range(n)]) for x in range(1<<n)],[phase(*[(x>>k)&1 for k in range(n)])%4 for x in range(1<<n)])
 half=lambda q:scale(q,(F(1,2),0));i4=m.eye(4);i16=m.eye(16)
 r0=tab(4,lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);xb=m.monomial([x^2 for x in range(16)],[0]*16);a0=half(i16.scale((1,1))+xb.scale((1,-1)))@r0
 r2=tab(4,lambda a,b,c,d:(c^(a*b))+2*d+4*a+8*b,lambda a,b,c,d:a*b*(1+2*c+2*d));sab=tab(4,lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0);scd=tab(4,lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0);sad=tab(4,lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0);j0=r2.star()@sab@r2
 zs=tab(2,lambda s,t:s+2*t,lambda s,t:2*s);zt=tab(2,lambda s,t:s+2*t,lambda s,t:2*t);xt=tab(2,lambda s,t:s+2*(t^1),lambda s,t:0);dt=tab(2,lambda s,t:s+2*t,lambda s,t:t)
 I=m.eye(64);Z=m.zero(64);a=i4.tensor(a0);S=zs.tensor(scd);S1=zs.tensor(sad);S2=zs.tensor(sab);T=zt.tensor(i16);R=xt.tensor(i16);J=i4.tensor(j0);Dt=dt.tensor(i16)
 assert T@R==(R@T).scale((-1,0)) and a.star()@S@a==S1 and a.power(-2)@S@a.power(2)==S2
 P=half(I+T);N=I+P.scale((-1,0));U=half(I+R);V=I+U.scale((-1,0));As=half(I+S);Bs=I+As.scale((-1,0));A2=half(I+S2);B2=I+A2.scale((-1,0))
 assert P@V@P==half(P) and V@P@V==half(V)
 def sm(xs):
  q=Z
  for x in xs:q=q+x
  return q
 def mm(A,B):return [[sm(A[i][k]@B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
 def ident():return [[I if i==j else Z for j in range(3)] for i in range(3)]
 def diag(x,y,z):return [[x,Z,Z],[Z,y,Z],[Z,Z,z]]
 def adj(A):return [[A[j][i].star() for j in range(len(A))] for i in range(len(A[0]))]
 def rot(i,j,h):
  p=half(I+h);n=I+p.scale((-1,0));q=ident();q[i][i]=q[j][j]=p;q[i][j]=n.scale((-1,0));q[j][i]=n;return q
 def swapmat(i,j,e):
  q=ident();q[i][i]=q[j][j]=I+e.scale((-1,0));q[i][j]=q[j][i]=e;return q
 C=mm(mm(mm(diag(I,J,I),rot(0,2,T)),rot(1,2,R)),rot(0,1,S));Ci=adj(C);assert mm(C,Ci)==mm(Ci,C)==ident()
 c00=P@As+(N@V@Bs).scale((-1,0));c10=J@U@Bs;c20=N@As+P@V@Bs;c21=(N@Bs).scale((-1,0))+P@V@As;c22=P@U;c02=(N@U).scale((-1,0))
 assert C[0][0]==c00 and C[1][0]==c10 and C[2]==[c20,c21,c22] and C[0][2]==c02
 gram=c00.star()@c00+c10.star()@c10;expected=As@P+Bs@U+half(Bs@V);assert gram==expected
 kernel=As@N;support=I+kernel.scale((-1,0));pinv=As@P+Bs@U+(Bs@V).scale((2,0));assert gram@pinv==pinv@gram==support
 assert kernel@kernel==kernel and kernel.trace()==(16,0) and c00@kernel==c10@kernel==Z
 right0=As@N+(Bs@V@P).scale((2,0));right1=(Bs@N).scale((-1,0))+(As@V@P).scale((2,0));assert c20@right0+c21@right1==I
 assert c02.star()@c02+c22.star()@c22==U
 H=scale(T+R,(F(1,2),F(1,2)));assert H@H.star()==I and H@U@H.star()==P
 p=U@B2;z=R@H@U@A2;w=V;assert p.star()@p+z.star()@z+w.star()@w==I and N@A2@z==z and V@w==w
 Q=mm(mm(mm(diag(H.star(),R,H.star()),swapmat(1,2,P@A2)),swapmat(0,2,P@B2)),diag(I,I,H));Qi=adj(Q);assert mm(Q,Qi)==mm(Qi,Q)==ident() and [Q[j][2] for j in range(3)]==[p,z,w]
 assert [p.star()@p,z.star()@z,w.star()@w]==[U@B2,U@A2,V]
 assert [q.trace()[0] for q in [U@B2,U@A2,V]]==[16,16,32]
 az=a@a@z;assert c00@az==c10@az==Z and c02@w==c22@w==Z
 L=[[a,Z,Z],[I,a,Z],[Z,Z,I]];UN=[[a,(a@a).scale((-1,0)),Z],[Z,a,Z],[Z,Z,I]];body=mm(mm(L,C),UN);last=mm(body,[[p],[z],[w]])
 f1=[[a@C[0][2]@w],[C[0][0]@a@p+C[0][1]@a@z+a@C[1][2]@w],[C[2][0]@a@p+C[2][1]@a@z]]
 f2=[[a@C[0][0]@a@p+a@C[0][1]@a@z],[a@C[1][0]@a@p+(C[0][0]@a@a@z).scale((-1,0))+a@C[1][1]@a@z],[(C[2][0]@a@a@z).scale((-1,0))]]
 assert all(last[j][0]==f1[j][0]+f2[j][0] for j in range(3)) and any(x[0]!=Z for x in f1) and any(x[0]!=Z for x in f2)
 # Full exact Walsh-block gauge check for the finite source heads used above.
 def rank_g(q):
  counts={sum(v!=(0,0) for v in row) for row in q.a};assert len(counts)==1;n=counts.pop();assert n and n&(n-1)==0;r=n.bit_length()-1
  assert all(n*(v[0]*v[0]+v[1]*v[1])==1<<(2*q.k) for row in q.a for v in row if v!=(0,0));groups={}
  for row in q.a:groups.setdefault(tuple(j for j,v in enumerate(row) if v!=(0,0)),[]).append(row)
  assert len(groups)==16//n
  for cols,rows in groups.items():
   assert len(rows)==n;phase={m.gm(rows[0][cols[0]],u):k for k,u in enumerate([(1,0),(0,1),(-1,0),(0,-1)])};assert all(row[j] in phase for row in rows for j in cols)
   ex=[[phase[row[j]] for j in cols] for row in rows];masks=[]
   for row in ex:
    dd=[(row[j]-row[0]-ex[0][j]+ex[0][0])%4 for j in range(n)];assert all(x in(0,2) for x in dd);masks.append(sum((x//2)<<j for j,x in enumerate(dd)))
   span={0}
   for q0 in masks:
    if q0 not in span:span|={x^q0 for x in tuple(span)}
   assert set(masks)==span and len(span)==n
  return r
 ranks={}
 for name,head,want in [('AJA',a0@j0@a0,2),('AJSA',a0@j0@scd@a0,2),('AJA2',a0@j0@a0.power(2),3),('AJSA2',a0@j0@scd@a0.power(2),3)]:ranks[name]=rank_g(head);assert ranks[name]==want
 mon={'I':I,'S':S,'T':T,'R':R,'J':J,'HPminus':N+P@S2,'HPplus':N+(P@S2).scale((-1,0)),'NX':R,'NZ':T,'NZX':T@R,'ND':Dt}
 for name,g in mon.items():assert g.k==0 and m.gaussian_rank(g)==0 and g@g.star()==I,name
 def M(name,bank,inverse=False):return {'op':'MONO','name':name,'bank':bank,'inverse':inverse}
 def SC(bank,v):return {'op':'SCALE','bank':bank,'coefficient':[str(v),'0']}
 def ADD(i,j):return {'op':'ADD','target':i,'source':j}
 def h2(i,j,inverse=False):return [ADD(i,j),SC(j,-2),ADD(j,i)]+([SC(i,F(1,2)),SC(j,F(1,2))] if inverse else [])
 def swap(i,j,h):return h2(i,j)+[M(h,j)]+h2(i,j,True)
 def rotw(i,j,h,inverse=False):return [M(h,i)]+swap(i,j,h) if inverse else swap(i,j,h)+[M(h,i)]
 def hp(target,helper,inverse=False):return {'op':'PREFIX_H','target':target,'helper':helper,'inverse':inverse}
 Cw=rotw(0,1,'S')+rotw(1,2,'R')+rotw(0,2,'T')+[M('J',1)];Cwi=[M('J',1,True)]+rotw(0,2,'T',True)+rotw(1,2,'R',True)+rotw(0,1,'S',True)
 Qw=[hp(2,0)]+swap(0,2,'HPminus')+swap(1,2,'HPplus')+[hp(0,1,True),M('R',1),hp(2,1,True)]
 Qwi=[hp(2,1),M('R',1,True),hp(0,1)]+swap(1,2,'HPplus')+swap(0,2,'HPminus')+[hp(2,0,True)]
 def expand(macros):
  ws=[];bounds=[F(1)]*3;peak=F(1)
  for op in macros:
   if op['op']=='PREFIX_H':
    dest,helper=op['target'],op['helper'];iv=op['inverse'];peak=max(peak,3*max(bounds[dest],bounds[helper]));bounds[dest]*=2;peak=max(peak,*bounds)
    base=nw['inverse'][:-1] if iv else nw['forward'][1:];remap={0:dest,1:helper};local=[M('ND',dest,iv)]
    for old in base:
     q=old.copy()
     if q['op']=='MONO':assert q['name'] in('X','Z','ZX','D');q['name']={'X':'NX','Z':'NZ','ZX':'NZX','D':'ND'}[q['name']]
     for key in ['bank','target','source']:
      if key in q:q[key]=remap[q[key]]
     q['inherited_prefix']=True;local.append(q)
    local.append(M('ND',dest,iv));ws.extend(local)
   else:
    ws.append(op)
    if op['op']=='ADD':bounds[op['target']]+=bounds[op['source']]
    elif op['op']=='SCALE':cf=list(map(F,op['coefficient']));bounds[op['bank']]*=abs(cf[0])+abs(cf[1])
    peak=max(peak,*bounds)
  return ws,peak
 def mono_left(g,x):
  rows=[None]*64
  for j in range(64):
   i=next(i for i in range(64) if g.a[i][j]!=(0,0));rows[i]=tuple(m.gm(g.a[i][j],v) for v in x.a[j])
  return m.M(tuple(rows),x.k)
 def replay(ws,omit=None):
  bs=ident()
  for k,op in enumerate(ws):
   if k==omit:continue
   if op['op']=='ADD':i,j=op['target'],op['source'];bs[i]=[x+y for x,y in zip(bs[i],bs[j])]
   elif op['op']=='SCALE':bs[op['bank']]=[scale(x,tuple(map(F,op['coefficient']))) for x in bs[op['bank']]]
   elif op['op']=='PREFIX_H':
    h=H.star() if op['inverse'] else H;bs[op['target']]=[h@x for x in bs[op['target']]]
   else:
    g=mon[op['name']];g=g.star() if op['inverse'] else g;bs[op['bank']]=[mono_left(g,x) for x in bs[op['bank']]]
  return bs
 # Verify both imported local Hadamards on an arbitrary bank/helper pair.
 for iv in [False,True]:
  ww,_=expand([hp(0,1,iv)]);assert Counter(q['op'] for q in ww)=={'ADD':24,'SCALE':48,'MONO':39};assert replay(ww)==diag(H.star() if iv else H,I,I)
 receipts={};wordout={};direct=0
 for name,fw,bw,want,wanti,ct in [('Cprime',Cw,Cwi,C,Ci,{'ADD':12,'SCALE':12,'MONO':7}),('Q0',Qw,Qwi,Q,Qi,{'ADD':80,'SCALE':152,'MONO':120})]:
  f,fb=expand(fw);b,bb=expand(bw);assert Counter(q['op'] for q in f)==Counter(q['op'] for q in b)==ct
  assert replay(f)==want and replay(b)==wanti and replay(fw)==want and replay(bw)==wanti
  for macros,target in [(fw,want),(bw,wanti)]:
   for k,op in enumerate(macros):
    if op['op']=='ADD':assert replay(macros,k)!=target;direct+=1
  receipts[name]={'forward':ct,'inverse':ct,'uniform_prefix_forward':str(fb),'uniform_prefix_inverse':str(bb)};wordout[name]={'forward':f,'inverse':b,'forward_macros':fw,'inverse_macros':bw};print('checked',name,ct,'prefix',fb,bb,flush=True)
 out.mkdir(parents=True,exist_ok=True)
 result={'status':'PASS_ANTICOMMUTING_PREFIX_FIRST_INTERFACE','scope':'exact paid units, source kernels and last-column ordinary/cubic cancellation; no independent endpoint','bank_dimension_control':64,'all_unit_input_columns':192,'last_column_input_columns':64,'active_kernel_rank':16,'ordinary_last_kernel_rank':32,'column_initial_ranks':[16,16,32],'third_row_explicit_right_inverse':True,'source_head_gaussian_ranks':ranks,'ordinary_and_cubic_last_terms_zero':True,'whole_last_column_equals_linear_plus_quadratic':True,'primitive_omitted_ADD_direct':direct,'primitive_omitted_ADD_inherited_from_pinned_prefix_word':144,'receipts':receipts,'new_gaussian_queries':0,'new_owners':0,'new_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(out/'WORDS.json').write_text(json.dumps(wordout,indent=2)+'\n');manifest={'engine':ENGINE,'engine_sha256':SHA,'normalizer_pins':NPINS,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json',out/'WORDS.json']}};(out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print(result['status'],'direct ADD controls',direct,flush=True)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--normalizer',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args();run(args.repo,args.normalizer,args.out)
