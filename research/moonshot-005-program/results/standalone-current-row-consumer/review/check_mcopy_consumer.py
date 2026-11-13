"""Independent exact audit of standalone Q, its consumer, and fixed m=3."""
import argparse, gzip, hashlib, json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--repo',required=True,type=Path)
p.add_argument('--package',required=True,type=Path)
a=p.parse_args(); repo=a.repo; package=a.package
src=repo/'research/shared-wire-split-composition/data/final.json.gz'
fullpath=repo/'research/shared-wire-split-composition/FULL-RESULT.json'
cyclicpath=repo/'research/moonshot-005-program/results/joint-current-row-codes/cyclic-dual/WORD.json.gz'
ev=package/'source-evidence'; basepath=ev/'rail-repaired.json.gz'
consumerpath=package/'output/rail-consumer.json.gz'; m3path=package/'m3/WORD.json.gz'
PIN={'source':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
 'full':'d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7',
 'cyclic':'ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2',
 'base_q':'90440c9115da1b98242113832c296faf314caf0ab7e0743119275dbfc372c9d2',
 'consumer_q':'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc',
 'm3':'9001ff407427dd86176f5d2ef9ba6d3baef457c023b132e36648d3f7c1159124',
 'choice':'24fc794c72895918eb810225a0b8c9f1d7d0266a70073e322861b084d05596b2'}
OLDRAW={1:990,2:360,3:105,4:112,5:133,6:8,7:2}
def need(ok,msg):
    if not ok: raise AssertionError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def read(path):
    b=path.read_bytes()
    return json.loads(gzip.decompress(b) if path.suffix=='.gz' else b)
def q(x): return Q(str(x))
def plus(x,y,c=Q(1)):
    z=x.copy()
    for k,v in y.items():
        t=z.get(k,Q(0))+c*v
        if t:z[k]=t
        else:z.pop(k,None)
    return z
def span(f):
    z={0}
    for v in f:z|={x^v for x in tuple(z)}
    return frozenset(z)
def rank(A):
    if not A:return 0
    B=[list(x) for x in A];m=len(B);n=len(B[0]);r=0
    for c in range(n):
        p=next((i for i in range(r,m) if B[i][c]),None)
        if p is None:continue
        B[r],B[p]=B[p],B[r];v=B[r][c];B[r]=[x/v for x in B[r]]
        for i in range(m):
            if i!=r and B[i][c]:
                v=B[i][c];B[i]=[x-v*y for x,y in zip(B[i],B[r])]
        r+=1
        if r==m:break
    return r
def replay(w,n):
    f=w['frames'];owned=w['owned_fields'];rows=[{i:Q(1)} for i in range(n)]+[{} for _ in range(owned)]
    loc=list(w['initial'])+[None]*owned;live=set(range(n));ops=Counter();moves=Counter();om=Counter();rm=Counter();now=peak=life=0
    need(len(w['initial'])==n,'initial count')
    for t,o in enumerate(w['program']):
        op,d=o[:2];ops[op]+=1
        if op=='INIT':
            need(d>=n and d not in live and loc[d] is None,f'INIT {t}');loc[d]=o[2];rows[d]={};live.add(d);now+=1;life+=1;peak=max(peak,now)
        elif op=='CLEAR':
            need(d>=n and d in live and loc[d]==o[2],f'CLEAR {t}');live.remove(d);loc[d]=None;rows[d]={};now-=1
        elif op=='MOVE':
            x,y,owned=o[2:];need(d in live and loc[d]==x and type(owned)is bool and owned==(d>=n),f'MOVE source {t}')
            sx,sy=span(f[x]),span(f[y]);need(sx<sy or owned and sy<sx,f'MOVE nesting {t}')
            r=abs(len(f[x])-len(f[y]));moves[r]+=1;(om if owned else rm)[r]+=1;loc[d]=y
        elif op=='SCALE':
            c=q(o[2]);need(c and d in live and loc[d]==o[3],f'SCALE {t}');rows[d]={i:c*v for i,v in rows[d].items() if c*v}
        else:
            need(op in ('ADD','COPY'),f'opcode {t}');s,c,ch=o[2],q(o[3]),o[4]
            need(s in live and d in live and d!=s and loc[d]==loc[s]==ch,f'ADD/COPY {t}')
            if op=='COPY':need(not rows[d],f'COPY_ZERO {t}')
            rows[d]=plus(rows[d],rows[s],c)
    need(live==set(range(n)) and now==0 and all(loc[i] is not None for i in range(n)),'all inputs retained, owned fields retired')
    return rows,loc,ops,moves,om,rm,peak,life
def remap(o,mapping,oldn,totaln):
    f=lambda r:mapping[r] if r<oldn else totaln+r-oldn
    z=list(o);z[1]=f(o[1])
    if o[0] in ('ADD','COPY'):z[2]=f(o[2])
    return z
def moment(profile):
    den=10**30;lo=hi=Q(0)
    for r,c in profile.items():
        n=r**199*den**200;left=0;right=r*den+1
        while right-left>1:
            mid=(left+right)//2
            if mid**200<=n:left=mid
            else:right=mid
        need(left**200<=n<right**200,f'power bracket {r}')
        x=Q(left,den);y=Q(left if left**200==n else right,den)
        if c>=0:lo+=c*x;hi+=c*y
        else:lo+=c*y;hi+=c*x
    return lo,hi

s=read(src);fc=read(fullpath);parent=read(cyclicpath);q0=read(basepath);q1=read(consumerpath);m3=read(m3path)
result=read(package/'m3/RESULT.json');choice=read(ev/'B7-COORDINATE-CHOICE.json')
base_result=read(ev/'PURE-RAIL-RESULT.json');consumer_result=read(package/'output/RAIL-CONSUMER-RESULT.json')
need(sha(src.read_bytes())==PIN['source'],'native pin');need(sha(fullpath.read_bytes())==PIN['full'],'full invoice pin')
need(sha(cyclicpath.read_bytes())==PIN['cyclic'],'cyclic parent pin');need(sha(basepath.read_bytes())==PIN['base_q'],'base Q pin')
need(sha(consumerpath.read_bytes())==PIN['consumer_q'],'Q consumer pin');need(sha(m3path.read_bytes())==PIN['m3'],'m3 word pin')
need(sha((ev/'B7-COORDINATE-CHOICE.json').read_bytes())==PIN['choice'],'choice pin')
need(base_result['word_sha256']==PIN['base_q'],'base-Q receipt pin')
need(consumer_result['word_sha256']==PIN['consumer_q'] and consumer_result['source_rail_sha256']==PIN['base_q'],'consumer-Q receipt pins')
need(consumer_result['hosted_reverse_residual_rank']==58 and len(consumer_result['completed_original_hosted_reverse_ports'])==24,
     'consumer-Q published residual and endpoint receipt')
need(result['word_sha256']==PIN['m3'] and result['rail_sha256']==PIN['consumer_q'],'m3 result pins')
need(result['word_payload_sha256']==sha(gzip.decompress(m3path.read_bytes())),'m3 canonical payload pin')
role={int(k):v for k,v in q1['source_role_map'].items()};rev={v:k for k,v in role.items()}
need(len(role)==400 and set(rev)==set(range(400)),'400-role bijection')
host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};H=list(host)
need(len(H)==96 and q0['frames'][:len(s['frames'])]==s['frames'],'96 hosted pairs and source frames')
need(q1['source_role_map']==q0['source_role_map'] and q1['initial']==q0['initial'] and q1['frames']==q0['frames'],'Q interface preserved')
need(q0['initial']==[s['initial'][rev[i]] for i in range(400)],'standalone initial chart interface')
need(q1['consumer']['source_rail_sha256']==PIN['base_q'] and q1['consumer']['begin']==len(q0['program']) and
     q1['consumer']['end']==len(q1['program']),'Q consumer chronology metadata')

# Reconstruct Q's actual current matrix and the exact 31-column patch.
r0,l0,c0,m0,om0,rm0,pk0,life0=replay(q0,400)
r1,l1,c1,m1,om1,rm1,pk1,life1=replay(q1,400)
b={i:role[host[i][0]] for i in H};d={i:role[host[i][1]] for i in H};J=choice['J']
need(q0['program']==q1['program'][:len(q0['program'])],'Q is literal prefix')
need(l0[:400]==[s['final'][rev[i]] for i in range(400)] and l1==l0,'all Q endpoint charts')
need(all(r0[d[i]]=={d[i]:Q(1)} and l0[d[i]]==s['final'][host[i][1]] for i in H),'all96 authentic D values restored')
need(all(l0[b[i]]==127 for i in H),'all96 actual B consumers at Hub')
need(len({span(q0['frames'][l0[d[i]]]) for i in H})==96,'all96 D source chart nodes distinct')
M0={i:{j:Q(i==j)+r0[b[i]].get(d[j],Q(0)) for j in H} for i in H}
need(all(r0[b[i]].get(b[j],Q(0))==Q(i==j) for i in H for j in H),'identity B input block')
need(all(any(M0[i][j] for i in H) for j in H) and all(M0[i][i]==1 for i in H),'96 nonzero residual columns with unit diagonal')
patch=q1['program'][len(q0['program']):];want=[];tmp=400
for j in J:
    F=l0[d[j]];want += [['INIT',tmp,F],['ADD',tmp,d[j],'1',F],['MOVE',tmp,F,127,True]]
    for i in H:
        if M0[i][j]:want.append(['ADD',b[i],tmp,str(-M0[i][j]),127])
    want.append(['CLEAR',tmp,127])
need(patch==want,'actual whole-column consumer operations')
cyclic_pairs={(o[2],o[3]) for o in parent['program'] if o[0]=='MOVE'}
new_returns=[o for o in patch if o[0]=='MOVE']
need(len(J)==31 and len(new_returns)==31 and all((o[2],o[3]) in cyclic_pairs for o in new_returns),'31 inherited rank-one consumer maps')
M1={i:{j:(Q(0) if j in J else M0[i][j]) for j in H} for i in H}
need(rank([[M1[i][j] for j in H] for i in H])==58,'Q consumer residual rank58')
complete={i for i in H if all(M1[i][j]==0 for j in H)}
need(complete==set(choice['completed_original_B']) and len(complete)==24,'exact24 completed hosted outputs')
need(sum(any(M1[i][j] for i in H) for j in H)==65,'65 nonzero residual columns after consumer')
for i in range(400):
    expected=r0[i].copy()
    if i in b.values():
        port=next(t for t in H if b[t]==i)
        for j in J:expected=plus(expected,{d[j]:Q(1)},-M0[port][j])
    need(r1[i]==expected,f'all400 Q output coefficients {i}')
need(c1['ADD']-c0['ADD']==370 and c1['INIT']-c0['INIT']==31 and c1['CLEAR']-c0['CLEAR']==31,'Q consumer ordinary increment')
need(m1==m0+Counter({1:31}) and pk1==pk0==29 and life1==life0+31,'Q consumer tariff/lifetimes')
need(c1['ADD']==3596 and c1['MOVE']==840 and c1['INIT']==402 and c1['CLEAR']==402,'Q consumer complete bill')
hosted_inputs=set(b.values())|set(d.values())
need(all(not(set(r1[i])&hosted_inputs) for i in range(400) if i not in hosted_inputs),'all other terminal Q rows independent of hosted b/d')

# Rebuild the complete m3 program byte-for-byte from Q/Q/W/recoupling.
copies=3;public=1480+400*(copies-1)
need(m3['public']==public and m3['copies']==copies and len(m3['initial'])==public,'m3 input arity')
need(m3['source_sha256']==PIN['source'] and m3['rail_sha256']==PIN['consumer_q'],'m3 recorded pins')
need(m3['frames']==q1['frames'] and m3['initial']==s['initial']+q1['initial']*(copies-1),'m3 frames and initial charts')
need(m3['owned_fields']==max(q1['owned_fields'],s['owned_fields']),'serial owned field capacity')
ops=[];blocks=[]
for bankidx in range(copies-1):
    bank={i:1480+400*bankidx+i for i in range(400)};start=len(ops)
    ops += [['ADD',bank[i],rev[i],'-1',q1['initial'][i]] for i in range(400)]
    ops += [remap(o,bank,400,public) for o in q1['program']]
    blocks.append({'copy':bankidx+1,'start':start,'stop':len(ops)})
common_start=len(ops)
ops += [remap(o,{i:i for i in range(1480)},1480,public) for o in s['program']]
common_end=len(ops)
for bankidx in range(copies-1):
    ops += [['ADD',1480+400*bankidx+i,rev[i],'1',s['final'][rev[i]]] for i in range(400)]
need(ops==m3['program'],'literal m3 program composition')
need(m3['private_blocks']==blocks and m3['common_block']==[common_start,common_end],'literal block marks')
need(len(ops)==83345,'m3 instruction count')

# Exact arbitrary-input replay of native W and complete m3; compare all 800
# private outputs with the separately composed E(u)+L(v-u) formula.
rw,lw,cw,mw,omw,rmw,pkw,lwlife=replay(s,1480)
rm,lm,cm,mm,omm,rmm,pkm,lm_life=replay(m3,public)
need(all(rm[i]==rw[i] and lm[i]==lw[i] for i in range(1480)),'all common outputs equal W(u)')
for bankidx in range(copies-1):
    off=1480+400*bankidx
    for i in range(400):
        expected=rw[rev[i]].copy()
        for k,c in r1[i].items():
            expected=plus(expected,{off+k:Q(1)},c)
            expected=plus(expected,{rev[k]:Q(1)},-c)
        need(rm[off+i]==expected and lm[off+i]==l1[i]==s['final'][rev[i]],f'm3 composed private output bank{bankidx} field{i}')
need(cm['ADD']==69972,'m3 ADD count')
need(cm['MOVE']==7990 and cm['INIT']==858 and cm['CLEAR']==858 and cm['SCALE']==3666 and cm['COPY']==1,'m3 opcode counts')
need(pkm==43 and lm_life==858,'m3 peak and lifetime count')
need(result['ordinary_bill']['counts']=={str(k):v for k,v in cm.items()},'m3 receipt opcode counts')
need(result['ordinary_bill']['moves']=={str(k):v for k,v in mm.items()},'m3 receipt MOVE histogram')
need(result['ordinary_bill']['peak']==pkm and result['ordinary_bill']['lifetimes']==lm_life,'m3 receipt peak/lifetimes')

# Exact full-caller profiles, including one common helper credit and the real
# per-rail Qpaid histogram measured from the independent Q row interpreter.
T={int(k):int(v) for k,v in fc['invoice']['T'].items()};P={int(k):int(v) for k,v in fc['invoice']['P'].items()}
Hprof={int(k):int(v) for k,v in fc['native']['helpers'].items()};N={int(k):int(v) for k,v in fc['native']['paid'].items()}
R=OLDRAW;Qpaid={r:m1.get(r,0) for r in set(m1)|set(R)};G={r:N.get(r,0)-R.get(r,0) for r in set(N)|set(R)}
need(sum(R.values())==1710 and sum(r*v for r,v in R.items())==3200,'old main raw profile mass')
Tm={r:copies*T.get(r,0)-18*(copies-1)*Hprof.get(r,0) for r in set(T)|set(Hprof)}
Pm={r:copies*P.get(r,0)-18*(copies-1)*G.get(r,0)+18*(copies-1)*(Qpaid.get(r,0)-R.get(r,0)) for r in set(P)|set(G)|set(Qpaid)|set(R)}
alt={r:copies*(P.get(r,0)-18*N.get(r,0))+18*N.get(r,0)+18*(copies-1)*Qpaid.get(r,0) for r in set(P)|set(N)|set(Qpaid)}
need(all(Pm.get(r,0)==alt.get(r,0) for r in set(Pm)|set(alt)),'independent paid profile identity')
need(Tm=={int(k):int(v) for k,v in result['T'].items()},'exact m3 target profile')
need(Pm=={int(k):int(v) for k,v in result['P'].items()},'exact m3 paid profile')
need(sum(Tm.values())==31296 and sum(Pm.values())==155916,'m3 target/paid totals')
surplus=sum(r*(Tm.get(r,0)-Pm.get(r,0)) for r in set(Tm)|set(Pm))
need(surplus==4380,'m3 full rank surplus')
mb=moment({r:Tm.get(r,0)-Pm.get(r,0) for r in set(Tm)|set(Pm)})
per=[x/(18*(copies-1)) for x in mb]
auth_mb=[Q(x) for x in result['moment_bounds']]
auth_per=[Q(x) for x in result['per_rail_moment_bounds']]
need(auth_mb[0]<=mb[0]<=mb[1]<=auth_mb[1],'author full-moment bracket contains tighter exact replay bracket')
need(auth_per[0]<=per[0]<=per[1]<=auth_per[1],'author per-rail bracket contains tighter exact replay bracket')
need(abs(float(per[0])-result['per_rail_moment_decimal'])<1e-14,'m3 per-rail decimal')

# Recompute the finite-m rail ceilings from the complete pinned caller, then
# compare their leftover allowance with the actual current-column first-exit
# lower bounds (96 before returns; 65 after the31 current returns).
caller_M0=moment({r:T.get(r,0)-P.get(r,0) for r in set(T)|set(P)})
dint=(-caller_M0[1]/18,-caller_M0[0]/18)
gint=moment({r:G.get(r,0)-Hprof.get(r,0) for r in set(G)|set(Hprof)})
ainf=(gint[0]-dint[1],gint[1]-dint[0])
a3=(ainf[0]-dint[1]/2,ainf[1]-dint[0]/2)
c0=moment({r:m0.get(r,0)-OLDRAW.get(r,0) for r in set(m0)|set(OLDRAW)})
c1=moment({r:m1.get(r,0)-OLDRAW.get(r,0) for r in set(m1)|set(OLDRAW)})
rem0inf=(ainf[0]-c0[1],ainf[1]-c0[0]);rem0m3=(a3[0]-c0[1],a3[1]-c0[0])
rem1inf=(ainf[0]-c1[1],ainf[1]-c1[0]);rem1m3=(a3[0]-c1[1],a3[1]-c1[0])
def deficit(required,remaining): return (Q(required)-remaining[1],Q(required)-remaining[0])
definite_deficits={'base_limit':deficit(96,rem0inf),'base_m3':deficit(96,rem0m3),
                   'after31_limit':deficit(65,rem1inf),'after31_m3':deficit(65,rem1m3)}
need(all(x[0]>0 for x in definite_deficits.values()),'append-only first-departure fees exceed finite-m rail room')

basepairs={(o[2],o[3]) for o in q0['program'] if o[0]=='MOVE'}
cyclicpairs={(o[2],o[3]) for o in parent['program'] if o[0]=='MOVE'}
chartmaps=read(ev/'CHART-MAPS.json')
certified={(o['source'],o['target']) for o in chartmaps['new_maps']}
need(basepairs-cyclicpairs==certified and len(certified)==6,'six new standalone repair maps match map certificates')
need(chartmaps['parent_sha256']==PIN['cyclic'],'new repair chart-map parent pin')

print(json.dumps({'status':'PASS_INDEPENDENT_STANDALONE_CONSUMER_M3_COMPOSITION_AUDIT',
 'pins':PIN,
 'base_Q':{'instructions':len(q0['program']),'residual_rank':rank([[M0[i][j] for j in H] for i in H]),'nonzero_columns':96,'D_facets_distinct':True,'other_terminal_fields_independent':True},
 'consumer_Q':{'instructions':len(q1['program']),'returns':len(J),'new_rank1_MOVEs':31,'residual_rank':58,'complete_outputs':24,'remaining_nonzero_columns':65,'all_new_returns_inherited':True},
 'm3':{'instructions':len(ops),'input_directions':public,'copies':copies,'literal_Q_Q_W_composition':True,'all_common_outputs_exact':True,'all800_private_outputs_exact':True,'MOVE_count':sum(mm.values()),'peak_owned':pkm,'lifetimes':lm_life,'rank_surplus':surplus,'target_positions':sum(Tm.values()),'paid_positions':sum(Pm.values()),'per_rail_moment_bounds':[str(x) for x in per],'per_rail_moment_decimal':float(per[0])},
 'append_only_terminal_gate':{'base_Q_remaining_columns':96,'after31_column_residual':65,'A_infinity':list(map(str,ainf)),'A_m3':list(map(str,a3)),'base_Q_cost_c':list(map(str,c0)),'consumer_Q_cost_c':list(map(str,c1)),'remaining_after_base_Q_at_limit':list(map(str,rem0inf)),'remaining_after_base_Q_m3':list(map(str,rem0m3)),'remaining_after_consumer_Q_at_limit':list(map(str,rem1inf)),'remaining_after_consumer_Q_m3':list(map(str,rem1m3)),'positive_lower_deficits':{k:list(map(str,v)) for k,v in definite_deficits.items()}},
 'scope':'Exact scalar source and full-caller arithmetic replay; partial endpoint only. The terminal gate applies to append-only private-only suffixes after common/shared calls are spent.'},indent=2))
