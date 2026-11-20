from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent));from algebra import *
ap=argparse.ArgumentParser();ap.add_argument('--h',type=int,required=True);h=ap.parse_args().h
res=np.load(folder/('DESIGN-%d.npz'%h));roles=list(map(int,res['I']))
atlas=Atlas(Path(os.environ['FE_REPO']),base/'bit-gf64-actual-k-atlas/author/output',base/'bit-minimum-cache-d-atlas/author/output/CHARTS.json.gz',folder/'mul.so')
atlas.left={i:atlas.left(i)for i in range(111)}.__getitem__
draw=np.random.default_rng(51280);source_dim=res['first'].shape[1]
sub=draw.integers(0,64,(source_dim,h+16),dtype=np.uint8);tests=[];ids0=[];frs=[];prs=[];phi=[];sground=[];natives=[]
for si,i in enumerate(roles):
 st=np.load(folder/f'S{i}.npz');fold=st['fold'];Es=list(st['e']);Ys=list(st['y']);m=len(Es)+len(Ys);ph=res[f'phi{i}'];parts=(ph[:,:m],ph[:,m:]);phi.append(ph)
 orig=K[i*w:(i+1)*w].copy();orig[:,i*w:(i+1)*w]^=np.eye(w,dtype=np.uint8);assert np.array_equal(mm(fold,st['sens']),orig)
 fr=mm(res['forms'][si],sub);pr=mm(res['outputs'][si],sub);frs.append(fr);prs.append(pr);tests.append(fr);ids0.append([i,'forms'])
 def protected(j,obs,B):
  ib=inverse(B);g=np.hstack([mm(mm(ph0,obs),ib)for ph0 in parts]);g0=fr^mm(g,pr);tests.append(g0);ids0.append([i,j]);return g
 g=protected('ground',np.vstack([np.zeros((len(Es),w),np.uint8),np.eye(w,dtype=np.uint8)]),fold[:,len(Es):]);sground.append(g);c=0
 for j in sorted(t for t in atlas.orth[i]if t<111):
  e,E,y,Y=atlas.terminal_inputs(i,j);ee={t:k for k,t in enumerate(e)};yy={t:k for k,t in enumerate(y)}
  obs=np.vstack([E[[ee[t]for t in Es],96:],Y[[yy[t]for t in Ys],96:]]);B=mm(fold,obs);assert np.array_equal(B,atlas.block(i,j)[96:,96:]);protected(j,obs,B);c+=1
 natives.append(c);print('physical role',i,'#',c,flush=True)
# Every protected h-dimensional image must have full rank on the same columns.
# Certify the first h-1 columns once, then solve the remaining proper
# nonvanishing conditions as explicit scalar linear forms on a shared vector.
for first_draw in range(100):
 V=draw.integers(0,64,(h+16,h-1),dtype=np.uint8)
 nulls=[]
 for t in tests:
  u=kernel(mm(t,V).T)
  if u.shape!=(h,1):break
  nulls.append(mm(u.T,t)[0])
 if len(nulls)==len(tests):break
else:raise ValueError('first h-1 physical directions')
for last_draw in range(100):
 trials=draw.integers(0,64,(h+16,4096),dtype=np.uint8)
 ok=np.flatnonzero(np.all(mm(np.stack(nulls),trials)!=0,axis=0))
 if len(ok):break
else:raise ValueError('last shared physical direction')
V=np.column_stack((V,trials[:,ok[0]]));assert all(rank(mm(t,V))==h for t in tests);sel=mm(sub,V);acts=[];curr=K0.copy();entries=[]
costs=np.array([sum(int(TABLE[z,1<<bit]).bit_count()for bit in range(6))for z in range(64)],np.int64);cost=lambda x:int(costs[x].sum());Ih=np.eye(h,dtype=np.uint8)
for si,i in enumerate(roles):
 U=mm(mm(prs[si],V),inverse(mm(frs[si],V)));acts.append(U);curr[i*d:(i+1)*d]^=mm(U,res['features'][si]);g=sground[si];ig=mm(U,inverse(Ih^mm(g,U)));entries.append([cost(phi[si])+cost(U),cost(g)+cost(ig)])
x1=mm(res['first'],sel);x2=mm(res['second'],sel);old=mm(Z,kernel(res['ell']));witness=np.hstack([old,x1,x2]);assert rank(witness)==2*d+h and not mm(curr,witness).any();rr=rank(curr);actual=8*d-rr
new_large=(111-8)*d+rr;tot=4*(20852+new_large);q={'h':h,'seed_first_last':[first_draw,last_draw,int(ok[0])],'comparable_protected_factors':len(tests),'per_role_foreigns':natives,'old_large_pair_nullity':2*d,'new_large_pair_nullity':actual,'marked_separate_small_pair_nullity':460,'large_pair_rank':new_large,'native_total_rank':tot,'saved_moves_over_frozen':6*(426240-tot),'extra_gauge_ADDs_over_small_six_large_four':4*sum(sum(row)for row in entries),'per_facet_pair_forward_and_ground':entries,'full_fixed_and_changed_proper_ADDs':3185065948+4*sum(sum(row)for row in entries),'added_INIT_and_dirty_CLEAR_each_over_small_six_large_four':2*4*6*h*6,'lower_over_m870_budget':tot-34688};print(q,flush=True)
np.savez_compressed(folder/f'NEW-{h}.npz',acts=np.stack(acts),allk=witness,**{f'phi{i}':x for i,x in zip(roles,phi)});(folder/f'NEW-{h}.json').write_text(json.dumps(q,indent=2)+'\n')
