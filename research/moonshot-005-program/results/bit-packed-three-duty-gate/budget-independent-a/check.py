#!/usr/bin/env python3
"""Separate binary-root enclosure and coefficient check of root's invoice."""
import hashlib,importlib.util,json
from fractions import Fraction as F
from pathlib import Path
ap=Path(__file__).resolve().parent
p=ap.parent/'paired-flag-source'/'check.py';sp=importlib.util.spec_from_file_location('independent_binary_arithmetic',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
root=ap.parent.parent/'root'/'two-copy-budget';receipt=json.loads((root/'RESULT.json').read_text())
N=m.lin({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10});H=m.lin({2:1,4:25,6:1,8:410})
P=m.add(m.scale(36,N),m.lin({1:444,**{7*j:444 for j in range(1,9)}}));T=m.add(m.scale(36,H),m.lin({127:222,**{1+7*j:444 for j in range(1,10)}}));delta=m.add(T,m.scale(-1,P));L=m.add(N,m.scale(-1,H),m.scale(F(1,36),delta))
base={1:183,2:12,3:119,4:71,7:110};cases=[]
for x in receipt['cases']:
 n=x['principal_physical_banks'];extra=n-16
 profile={r:2*c for r,c in base.items()};profile[1]+=14;profile[7]-=2
 if extra:profile[8]=extra
 assert profile=={int(r):v for r,v in x['full_movement_profile'].items()}
 Q=m.scale(F(1,2),m.lin(profile));room=m.add(L,m.scale(-1,Q));slope=m.scale(18,room)
 for ours,theirs in [(Q,x['normalized_Q']),(room,x['limiting_normalized_room']),(slope,x['finite_margin_slope'])]:
  assert ours[0]<=F(theirs['upper_rational']) and F(theirs['lower_rational'])<=ours[1]
 margins=[]
 for z in x['finite_samples']:
  k=z['m'];v=m.add(m.scale(18*(k-1),room),m.scale(F(1,2),delta))
  assert v[0]<=F(z['normalized_margin']['upper_rational']) and F(z['normalized_margin']['lower_rational'])<=v[1]
  margins.append((k,v[0]>0,v[1]<0))
 first=next((k for k,pos,neg in margins if pos),None)
 assert first==x['finite_even_m_first_certified']
 if n>=20:assert room[1]<0 and all(neg for k,pos,neg in margins)
 cases.append({'banks':n,'first_even_m':first,'room':m.enc(room),'slope':m.enc(slope),'all_m_sample_signs_separated':all(pos or neg for k,pos,neg in margins)})
out={'status':'PASS_INDEPENDENT_TWO_COPY_MOVEMENT_INVOICE','arithmetic':'Independent binary denominator2^160 integer200th-root enclosures; author uses10^50. New reviewer coefficient assembly.','author_pins':{n:hashlib.sha256((root/n).read_bytes()).hexdigest()for n in ['check.py','RESULT.json']},'cases':cases,'scope':'Movement-only optimistic interface. No decoder, proper-cover physical charging theorem, supplier or new kappa inferred.'}
(ap/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
