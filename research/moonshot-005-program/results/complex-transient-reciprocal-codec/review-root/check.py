#!/usr/bin/env python3
"""Independent dense400-column review of restored complex receiver codecs."""
import argparse,copy,gzip,hashlib,importlib.util,json,math
from pathlib import Path
from fractions import Fraction as F

def need(b,s):
 if not b:raise ValueError(s)
def read(p,pin=None):
 b=p.read_bytes();need(pin is None or hashlib.sha256(b).hexdigest()==pin,'source pin');return json.loads(gzip.decompress(b))
def rank(rows):
 basis={}
 for row in rows:
  v=list(row)
  for p,b in sorted(basis.items()):
   if v[p]:
    x,y=v[p],b[p];v=[y*a-x*c for a,c in zip(v,b)];g=math.gcd(*v)
    if g>1:v=[a//g for a in v]
  p=next((p for p,x in enumerate(v) if x),None)
  if p is not None:basis[p]=v
 return len(basis)
def det(A):
 a=[list(map(F,r)) for r in A];d=F(1)
 for j in range(len(a)):
  k=next((k for k in range(j,len(a)) if a[k][j]),None)
  if k is None:return F(0)
  if k!=j:a[k],a[j]=a[j],a[k];d=-d
  z=a[j][j];d*=z
  for k in range(j+1,len(a)):
   z0=a[k][j]/z;a[k]=[x-z0*y for x,y in zip(a[k],a[j])]
 return d
def main(a):
 ep='c4389c80322c875c4739af6ee558619f01da6112682c565e4f638a01750e5ec1'
 need(hashlib.sha256(a.engine.read_bytes()).hexdigest()==ep,'independent engine pin')
 spec=importlib.util.spec_from_file_location('independent_dense',a.engine);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
 n=read(a.native,'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883')
 p=read(a.parent,'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc')
 p['program']=p['program'][:p['consumer']['begin']];need(len(p['program'])==4779,'exact stripped boundary')
 old,od,ol,ob,_=e.run(p,list(map(e.span,p['frames'])))
 role={int(k):v for k,v in p['source_role_map'].items()}
 hosted=sorted((n['live'][i],role[b],role[d]) for i,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2']))
 H={h for h,b,d in hosted};Bset={b for h,b,d in hosted};Dset={d for h,b,d in hosted}
 def residual(rr,den):
  out=[]
  for h,b,d in hosted:
   v=rr[b].copy();v[b]-=den;v[d]+=den;out.append(v)
  return out
 def debt(rr,den):
  z=0;done=[]
  for h in n['live']:
   y=role[h+112];c=F(1) if h in H else F(1,2)
   k=sum(F(x,den)!=c*(int(j==role[h])+int(j==y)) for j,x in enumerate(rr[y]));z+=k
   if not k:done.append(h)
  return z,done
 def root(h):
  mask=n['frames'][n['initial'][h]][0];on=[i for i in range(9) if mask>>i&1]
  if len(on)==3:return [3*int(i in on)-1 for i in range(9)]
  off=[i for i in range(9) if not(mask>>i&1)];need(len(off)==2,'native root type')
  return [3*(int(i==off[0])-int(i==off[1])) for i in range(9)]
 roots={h:root(h) for h,b,d in hosted};G=[[sum(x*y for x,y in zip(roots[h],roots[j])) for j,bj,dj in hosted] for h,b,d in hosted]
 need(all(G[i][i]==18 for i in range(96)) and rank(G)==8,'actual normalized real Gram rank8')
 def invariant(rr,den):
  return [[F(rr[b][dj]+rr[role[j+112]][role[h]],den) for j,bj,dj in hosted] for h,b,d in hosted]
 def current_a(rr,den):
  for h in n['live']:
   y=role[h+112];coeff=[rr[y][role[j]] for j in n['live']]
   for c in range(400):
    value=sum(z*rr[role[j]][c] for z,j in zip(coeff,n['live']) if z)
    need((rr[y][c]-den*int(c==y))*den==value,'all104 actual-current-X expressions')
 need(debt(old,od)[0]==4920 and rank(residual(old,od))==82,'retained source baseline')
 balfile=a.bundle/'balanced/WORD.json.gz';bal=read(balfile,'7cfefc12e666f1fa39a311f13ba5e919c307bfb8264d933a71d2abf2b2de55f2')
 lineage=bal['parent_event_of_output'];repair=sum([z['ops'] for z in p['repair_manifest']],[])
 need(len(repair)==31 and p['program'][-31:]==repair,'six actual one-way repair blocks')
 need(lineage==sorted(set(lineage)) and all(0<=i<4748 for i in lineage),'monotone actual lineage')
 need(bal['program']==[p['program'][i] for i in lineage],'unchanged retained operations')
 missing=sorted(set(range(4748))-set(lineage));need(len(missing)==72,'exact72 removed reads')
 need(all(p['program'][i][0]=='ADD' and p['program'][i][1] in Bset and p['program'][i][2] in Dset for i in missing),'all removed reads are actual D-to-B')
 br,bd,bl,bb,_=e.run(bal,list(map(e.span,bal['frames'])))
 need(bl==ol and all(e.eqrow(br[i],bd,old[i],od) for i in range(104)),'all first-X and endpoint charts retained')
 need(all(br[d]==[bd*int(i==d) for i in range(400)] for d in Dset),'all original D unchanged')
 current_a(br,bd);GI=[[F(x,18) for x in r] for r in G];need(invariant(br,bd)==GI,'all9216 hosted reciprocal Gram entries')
 need(rank(br.values())==400 and rank(residual(br,bd))==88 and debt(br,bd)[0]==4928,'balanced exact ranks and reopened debt')
 need({r:bb['moves'].get(r,0)-ob['moves'].get(r,0) for r in set(bb['moves'])|set(ob['moves']) if bb['moves'].get(r,0)!=ob['moves'].get(r,0)}=={1:-6},'six removed rank1 moves')
 balcontrols=[]
 t=missing[0];at=next((k for k,i in enumerate(lineage) if i>t),len(lineage))
 for label,ops in [('retain_one_D_read',bal['program'][:at]+[p['program'][t]]+bal['program'][at:]),('retain_one_forward_repair',bal['program']+p['repair_manifest'][0]['ops'])]:
  bad=dict(bal);bad['program']=ops;rr,dd,ll,bi,_=e.run(bad,list(map(e.span,bad['frames'])))
  need(invariant(rr,dd)!=GI,'alignment negative control');balcontrols.append(label)
 out={'balanced':dict(word_sha256=hashlib.sha256(balfile.read_bytes()).hexdigest(),bill=bb,move_delta={1:-6},forward_debt=4928,reverse_rank=88,full_public_rank=400,removed_actual_D_reads=72,removed_repair_packets=6,Gram_rank=8,current_a_identity_rows=104,negative_controls=balcontrols)}
 for variant,base,base_rows,base_den,base_loc,base_bill,sub,pin in [('parent',p,old,od,ol,ob,'output','777be9c2991cb9755e82ee43251d906831d1d08e303d8e2bbf89d53e6962c4be'),('balanced',bal,br,bd,bl,bb,'balanced-output','79bf4bd0ce0d6e2c0bd44c3134141314bea0b8c5b77ea486d8496e17ddd7beb3')]:
  wp=a.bundle/sub/'WORD.json.gz';w=read(wp,pin);c=w['transient_codec'];m=c['markers'];xs=c['X_roles'];bs=c['B_roles'];ys=c['Y_roles'];ds=c['D_roles'];caches=c['X_stationary_caches'];M=[list(map(F,r)) for r in c['encoder_M']];A=[list(map(F,r)) for r in c['desired_A']];piv=c['pivot_positions'];C=c['C'];ops=w['program'];spaces=list(map(e.span,w['frames']))
  need(w['initial']==p['initial'] and w['public']==400 and w['owned_fields']==p['owned_fields']+2,'actual input interface')
  need(xs==[role[h] for h in c['I_ports']] and bs==[next(b for h,b,d in hosted if h==i) for i in c['I_ports']],'authentic donor roles')
  need(ys==[role[j+112] for j in c['J_ports']] and ds==[next(d for h,b,d in hosted if h==j) for j in c['J_ports']],'authentic receiver roles')
  need(c['I_ports']==[0,6] and len(ys)==len(ds)==20 and len(set(ys+ds))==40,'actual two-by-twenty module')
  need(piv==[0,16] and det(M)==F(-1,2) and all(M[z]==A[i] for i,z in enumerate(piv)),'exact invertible row-completion encoder')
  need(all(A[i][j]==-F(base_rows[y][x],base_den) and A[i][j] in (F(1,2),F(-1,2)) for i,x in enumerate(xs) for j,y in enumerate(ys)),'actual forty correction coefficients')
  need(len(spaces[C])==4 and all(spaces[p['initial'][b]]<spaces[C] for b in bs) and all(spaces[C]<spaces[base_loc[d]] for d in ds),'real physical common plane/branches/facets')
  captures={m['ground_encoding_end']-1:('encoded',ds+ys),m['common_decode_end']-1:('decoded',ds+ys)}
  before={m['gadget_begin']:('before',ds+ys)}
  rr,dd,ll,bill,sn=e.run(w,spaces,capture_before=before,capture_after=captures)
  db,rb,lb=sn['before'];de,re,le=sn['encoded'];du,ru,lu=sn['decoded']
  need(all(lb[r]==le[r]==3 for r in ds+ys) and all(lu[r]==C for r in ds+ys),'actual transform charts')
  for i,d in enumerate(ds):
   need(all(F(rb[d][j],db)==int(j==d) and F(ru[d][j],du)==int(j==d) for j in range(400)),'every D restored before departure')
   need(all(F(re[d][j],de)==sum(M[i][k]*int(j==z) for k,z in enumerate(ds)) for j in range(400)),'actual D encoding M')
  for i,y in enumerate(ys):
   for j in range(400):
    need(sum(M[k][i]*F(re[ys[k]][j],de) for k in range(20) if M[k][i])==F(rb[y][j],db),'actual inverse-transpose Y encoding')
    need(F(ru[y][j],du)==F(rb[y][j],db)+sum(A[k][i]*int(j==x) for k,x in enumerate(xs)),'actual Y uncompute and paired addition')
  changes={y:{x:A[k][j] for k,x in enumerate(xs)} for j,y in enumerate(ys)}
  changes.update({b:{d:-A[k][j] for j,d in enumerate(ds)} for k,b in enumerate(bs)})
  need(ll==base_loc,'all400 final charts')
  need(all(F(rr[i][j],dd)==F(base_rows[i][j],base_den)+changes.get(i,{}).get(j,0) for i in range(400) for j in range(400)),'complete all400-column paired source delta')
  need(rank(rr.values())==400,'full original input rank400')
  need(invariant(rr,dd)==invariant(base_rows,base_den),'entire hosted reciprocal matrix preserved')
  current_a(rr,dd)
  aft,completed=debt(rr,dd);bef,oldcompleted=debt(base_rows,base_den);rk=rank(residual(rr,dd))
  need(aft==bef-40 and completed==oldcompleted and rk==({'parent':83,'balanced':89}[variant]),'debt and actual reverse ranks')
  move_delta={r:bill['moves'].get(r,0)-base_bill['moves'].get(r,0) for r in set(bill['moves'])|set(base_bill['moves']) if bill['moves'].get(r,0)!=base_bill['moves'].get(r,0)}
  need(move_delta=={1:8,2:36,6:40,8:-40},'complete paid movement increment')
  ordinary_delta={tag:bill['counts'].get(tag,0)-base_bill['counts'].get(tag,0) for tag in set(bill['counts'])|set(base_bill['counts'])}
  need(ordinary_delta=={'INIT':2,'CLEAR':2,'ADD':86,'MOVE':44,'SCALE':4},'every ordinary and ownership increment')
  need(all(o[0]!='MOVE' or not o[4] for o,t in zip(ops,w['baseline_event_of_output']) if t is None),'no added owned moves')
  need(bill['lifetimes']==base_bill['lifetimes']+2 and bill['peak']==31,'both stationary cache lives and peak')
  for cache,x,b in zip(caches,xs,bs):
   seq=[o for o in ops if o[1]==cache];line=p['initial'][b]
   need(seq==[['INIT',cache,line],['ADD',cache,x,'1',line],['CLEAR',cache,line]],'authentic stationary X acquisition and erasure')
  controls=[]
  indexes={'omit_D_decode':m['all_at_common_plane'],'omit_Y_decode':m['all_at_common_plane']+21,'omit_actual_X_cache':1,'omit_B_transpose_update':m['branch_0_before_read']+1}
  for label,t in indexes.items():
   bad=dict(w);bad['program']=ops[:t]+ops[t+1:]
   try:
    z,zd,zl,zb,_=e.run(bad,spaces);need(zl==ll and all(e.eqrow(z[i],zd,rr[i],dd) for i in range(400)),'all-column mutant endpoint')
   except (AssertionError,ValueError):controls.append(label)
   else:raise ValueError('accepted transient mutant '+label)
  bad=copy.deepcopy(w);bad['program'][m['branch_0_before_read']][4]=C
  try:e.run(bad,spaces)
  except (AssertionError,ValueError):controls.append('wrong_branch_chart')
  else:raise ValueError('accepted nonlocal branch mutant')
  out[variant+'-codec']=dict(word_sha256=pin,bill=bill,move_delta=move_delta,forward_debt=aft,reverse_rank=rk,full_public_rank=400,complete_forward_ports=completed,all_original_D_restored_at_common_plane=True,all400_rows_checked=True,hosted_invariant_preserved=True,encoder_determinant=str(det(M)),negative_controls=controls,new_ordered_maps=sorted(set((o[2],o[3]) for o in ops if o[0]=='MOVE')-set((o[2],o[3]) for o in base['program'] if o[0]=='MOVE')))
 result=dict(status='PASS_INDEPENDENT_RESTORED_TRANSIENT_RECIPROCAL_CODEC',engine_sha256=ep,results=out,source_scope='Fixed source maps and all-width scalar identity lifts; no uniform physical/compiler or complete supplier. Alternatives are separately costed.',new_kappa=None)
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'reverse_ranks':{k:v['reverse_rank'] for k,v in out.items()},'forward_debts':{k:v['forward_debt'] for k,v in out.items()}}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','parent','bundle','engine','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
