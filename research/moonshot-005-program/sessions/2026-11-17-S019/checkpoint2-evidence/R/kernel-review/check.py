"""Independent exact review of the free-range ordinary-kernel interface."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--root-control',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
text=args.root_control.read_text();exec(text[text.index('I=s.eye(16)'):text.index('words=')],globals());exec(text[text.index('def execute(word):'):text.index('receipts={}')],globals())
Zc=mono([(x,2*((x>>2)&1))for x in range(16)]);freePi=s.diag(Mh,Ph,Z);O=block([[Mh,Ph,Z],[Ph,Mh,Z],[Z,Z,I]])
Cold=block([[M,P,Z],[J*P,J*M,Z],[Z,Z,I]]);Qseed=block([[Z,I,Z],[I,Z,Z],[Z,Z,I]])
Kold=block([[clean(A*M*A),Z,Z],[clean(A*J*P*A),Z,Z],[Z,Z,Z]])
assert clean(Kold.H*Kold)==s.diag(I,Z,Z) and O*freePi*O==s.diag(I,Z,Z)
wdata=json.loads((args.author/'WORDS.json').read_text());gdata=json.loads((args.author/'GAUSSIAN-GAUGES.json').read_text());results={};omissions=0
for case,T0 in [('failed_JZa',J*F),('surviving_SZc',S*Zc)]:
 T=(I+T0)/2;Nt=I-T;assert T0*T0==I and T0.trace()==0
 Cn=clean(Cold*block([[T,Z,Nt],[Z,I,Z],[Nt,Z,T]]));K=block([[clean(A*M*T*A),Z,Z],[clean(A*J*P*T*A),Z,Z],[Z,Z,Z]])
 B=clean(A*(M+J*P)*T*A);H0=clean(A.H*T0*A);H2=clean(A2.H*T0*A2)
 assert clean(freePi*K)==K and clean(O*K)==block([[B,Z,Z],[Z,Z,Z],[Z,Z,Z]]) and clean(K.H*K)==s.diag(clean(A.H*T*A),Z,Z)
 support0=max(sum(H0[r,c]!=0 for r in range(16))for c in range(16));support2=max(sum(H2[r,c]!=0 for r in range(16))for c in range(16));assert support0>1
 if case=='failed_JZa':
  assert support2>1 and clean(J*P*T)==clean(P*T) and clean(A*T*A3)==clean((A4+Fh*Kd*B2)/2)
 else:
  assert H2==J*F;Rm=(I-H2)/2;assert Rm*Rm==Rm and Rm.trace()==8 and clean(B*A*Rm)==Z and clean(B*Rm)!=Z
 monos={n:mono(t)for n,t in wdata['cases'][case]['monomial_tables'].items()};assert monos=={'F':F,'Fhat':Fh,'J':J,'T0':T0,'S':S,'Kdec':Kd}
 word=wdata['cases'][case]['words']
 for n,want in {'C_new':Cn,'Q_seed':Qseed,'O':O}.items():
  f=execute(word[n]);v=execute(word[n+'_inverse']);assert f==want and clean(f*v)==s.eye(48)and clean(v*f)==s.eye(48)
  for name in [n,n+'_inverse']:
   full=execute(word[name]);counts={op:sum(x['op']==op for x in word[name])for op in ['ADD','SCALE','MONO']};assert {k:v for k,v in counts.items()if v}==wdata['invoices'][case][name]['counts']
   for j,op in enumerate(word[name]):
    if op['op']=='ADD':assert execute(word[name][:j]+word[name][j+1:])!=full;omissions+=1
 matrices={'A2':A2,'AJA':clean(A*J*A),'A3':A3,'AJA2':clean(A*J*A2),'AT0A':clean(A*T0*A),'AJT0A':clean(A*J*T0*A),'AT0A2':clean(A*T0*A2),'AJT0A2':clean(A*J*T0*A2),'H0':H0}
 for name,gauge in gdata[case].items():
  h=I
  for bit in range(gauge['rank']):h=clean(h*((1+s.I)*I+(1-s.I)*mono([(x^(1<<bit),0)for x in range(16)]))/2)
  assert clean(mono(gauge['left'])*h*mono(gauge['right']))==matrices[name]
 results[case]={'physical_prefix_rank':8,'physical_ambient_rank':16,'H0_max_column_support':support0,'H2_max_column_support':support2,'free_image_decoder_checked':True,'gaussian_gauges_checked':len(gdata[case]),'ordinary_kernel_channel':case=='surviving_SZc'}
result={'status':'PASS_INDEPENDENT_FREE_RANGE_KERNEL_BRIDGE','method':'Root exact SymPy literals and primitive row updates; no author arithmetic or executor imported.','cases':results,'omitted_ADD_controls':omissions,'pins':{n:hashlib.sha256((args.author/n).read_bytes()).hexdigest()for n in ['PROOF.md','check.py','WORDS.json','GAUSSIAN-GAUGES.json']},'root_control_sha256':hashlib.sha256(args.root_control.read_bytes()).hexdigest(),'scope':'Physical controls at one column plus separately reviewed multiplicative all-width identities and faithful finite-word kernel proof. No inference of large-width ordinary injectivity from one-column ranks. No full421 caller.'}
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
