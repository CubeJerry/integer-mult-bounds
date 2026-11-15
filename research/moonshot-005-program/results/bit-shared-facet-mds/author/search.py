import json,itertools,hashlib,argparse,math
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();nb=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(nb).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(nb)['native_roots'];dot=lambda x,y:sum(a*b for a,b in zip(x,y))
def norm(v):
 v=tuple(v)
 return v if next(x for x in v if x)>0 else tuple(-x for x in v)
full={norm(r)for r in R};changed=True
while changed:
 old=sorted(full);assert all(dot(x,y)%2==0 for x,y in itertools.product(old,old));add={norm([a-(dot(x,y)//2)*b for a,b in zip(x,y)])for x,y in itertools.product(old,old)};assert all(dot(x,x)==4 for x in add);changed=bool(add-full);full|=add
assert len(full)==120;full=sorted(full);out=[]
for i in range(111):
 foreign=[j for j in range(111)if j!=i and dot(R[i],R[j])==0];allm=sum(1<<j for j in foreign);by={};fullforeign=[x for x in full if dot(R[i],x)==0];assert len(fullforeign)==63
 for q in full:
  if dot(R[i],q)==0 or abs(dot(R[i],q))==4:continue
  normal=[4*x-dot(R[i],q)*y for x,y in zip(q,R[i])];g=math.gcd(*normal);normal=norm([x//g for x in normal]);mask=sum(1<<j for j in foreign if dot(q,R[j])==0);by.setdefault(normal,{'q':list(q),'mask':mask})
 assert len(by)==28;atlas=list(by.values());masks=[z['mask']for z in atlas];assert all(sum(dot(z['q'],x)==0 for x in fullforeign)==36 for z in atlas);assert all(sum(dot(z['q'],x)==0 for z in atlas)==16 for x in fullforeign)
 best=None
 for c,cm in enumerate(masks):
  pairs=[(x,y)for x,y in itertools.combinations(range(28),2)if c not in[x,y]and(masks[x]|masks[y]|cm)==allm]
  for p1,p2 in itertools.combinations(pairs,2):
   if set(p1)&set(p2):continue
   x,y=p1;z,t=p2
   if masks[x]|masks[y]|masks[z]|masks[t]!=allm:continue
   ids=[x,y,z,t,c];best={'chart_indices':ids,'normals':[atlas[j]['q']for j in ids],'colors':[1,1,2,2,3]};break
  if best:break
 if not best:print('NO BINARY FIVE',i,flush=True)
 out.append({'receiver':i,'foreign_count':len(foreign),'atlas':[{'normal':z['q'],'native_mask_hex':hex(z['mask'])}for z in atlas],'full_E7_count':63,'each_atlas_full_support':36,'each_foreign_chart_incidence':16,'binary_five':best})
result={'status':'PASS_FULL_ATLAS_28_BY_16','native_sha256':hashlib.sha256(nb).hexdigest(),'full_roots':[list(x)for x in full],'binary_five_covered':sum(x['binary_five']is not None for x in out),'rows':out};(Path(__file__).parent/'GEOMETRY.json').write_text(json.dumps(result,indent=2)+'\n');print('atlas all111; binary five',result['binary_five_covered'],flush=True)
