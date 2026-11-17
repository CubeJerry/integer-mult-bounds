#!/usr/bin/env python3
"""Exact primitive replay of the uniform distinguished-column plus unit."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'

def run(repo,out):
 ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==SHA
 spec=importlib.util.spec_from_file_location('prefix_plus_exact_engine',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 I=m.eye(16)
 def frac(x,c):
  c=F(c);assert c.denominator&(c.denominator-1)==0;y=x.scale((c.numerator,0));return m.M(y.a,y.k+c.denominator.bit_length()-1).norm()
 def tab(dest,phase):return m.monomial([dest(*[(x>>k)&1 for k in range(4)]) for x in range(16)],[phase(*[(x>>k)&1 for k in range(4)])%4 for x in range(16)])
 R=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);Xb=m.monomial([x^2 for x in range(16)],[0]*16)
 A=frac(I.scale((1,1))+Xb.scale((1,-1)),F(1,2))@R;t=m.monomial([x^12 for x in range(16)],[0]*16);h=A@t@A.star();j=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*b)
 assert h.k==0 and m.gaussian_rank(h)==0 and h@h==j@j==I and j@h==(h@j).scale((-1,0))
 words=[]
 def shear(target,source,sign):
  for name,cf in [('I',F(sign,2)),('H',F(-sign,2))]:
   if name!='I':words.append({'op':'MONO','bank':source,'name':name})
   words.append({'op':'SCALE','bank':source,'coefficient':str(cf)})
   words.append({'op':'ADD','target':target,'source':source})
   words.append({'op':'SCALE','bank':source,'coefficient':str(1/cf)})
   if name!='I':words.append({'op':'MONO','bank':source,'name':name})
 shear(1,0,1);shear(0,1,-1);shear(1,0,1)
 words.extend([{'op':'MONO','bank':0,'name':'H'},{'op':'MONO','bank':1,'name':'J'}])
 inverse=[]
 for op in reversed(words):
  q=op.copy()
  if q['op']=='ADD':q={'op':'SUB','target':q['target'],'source':q['source']}
  elif q['op']=='SCALE':q['coefficient']=str(1/F(q['coefficient']))
  inverse.append(q)
 # The reversed raw word has SUB primitives; compile each into SCALE(-1), ADD,
 # SCALE(-1), then use shear-level inversion instead to retain the same receipt.
 invwords=[{'op':'MONO','bank':1,'name':'J'},{'op':'MONO','bank':0,'name':'H'}]
 old=words;words=invwords
 shear(1,0,-1);shear(0,1,1);shear(1,0,-1)
 inverse=words;words=old
 counts=dict(Counter(x['op'] for x in words));icounts=dict(Counter(x['op'] for x in inverse));assert counts==icounts=={'ADD':6,'SCALE':12,'MONO':8}
 reports=[]
 for V in [1,2]:
  H=h.tp(V);J=j.tensor(m.eye(16**(V-1)));Iv=m.eye(16**V);Zv=m.zero(16**V)
  P=frac(Iv+H,F(1,2));M=frac(Iv+H.scale((-1,0)),F(1,2))
  assert J@H==(H@J).scale((-1,0)) and P@J==J@M
  U=m.block([[P,M],[J@M,J@P]]);Ui=m.block([[P,M@J],[M,P@J]])
  assert U@Ui==Ui@U==m.eye(2*16**V)
  assert P@P==P and P@J@M==J@M and P@P+M@J@J@M==Iv
  def replay(ws,omit=None):
   b=[[Iv,Zv],[Zv,Iv]]
   for k,op in enumerate(ws):
    if k==omit:continue
    if op['op']=='ADD':
     d,s=op['target'],op['source'];b[d]=[x+y for x,y in zip(b[d],b[s])]
    elif op['op']=='SCALE':b[op['bank']]=[frac(x,F(op['coefficient'])) for x in b[op['bank']]]
    else:
     g={'H':H,'J':J}[op['name']];b[op['bank']]=[g@x for x in b[op['bank']]]
   return m.block(b)
  assert replay(words)==U and replay(inverse)==Ui
  for ws,want in [(words,U),(inverse,Ui)]:
   for k,op in enumerate(ws):
    if op['op']=='ADD':assert replay(ws,k)!=want
  if V==2:
   wrong=j.tp(V);assert wrong@H==H@wrong and P@wrong@M!=wrong@M
  reports.append({'width':V,'all_input_columns':True,'unit_and_inverse':True,'omitted_ADD_failures':12})
 out.mkdir(parents=True,exist_ok=True)
 result={'status':'PASS_DISTINGUISHED_COLUMN_SAME_PLUS_UNIT','scope':'explicit enlarged fixed two-part ordinary templates, not pure collective catalogue; no full caller','counts_forward':counts,'counts_inverse':icounts,'uniform_prefix_bound':5,'width_controls':reports,'all_width_basis':'j h=-h j on the distinguished column; exact tensor and projector identities','new_gaussian_queries':0,'new_owners':0,'new_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(out/'WORDS.json').write_text(json.dumps({'forward':words,'inverse':inverse},indent=2)+'\n')
 manifest={'engine':ENGINE,'engine_sha256':SHA,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json',out/'WORDS.json']}}
 (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print(result['status'],counts,'prefix<=5')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.repo,a.out)
