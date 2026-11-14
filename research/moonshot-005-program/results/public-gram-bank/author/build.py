#!/usr/bin/env python3
"""Actual public Gram-pivot preload and dyadically reversible proper relay."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
PINS={'retained':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
      'allhosted':'3dec380d820ed631636bdc77adb4a4c3e35abdb31d2b312f8f41edadff389d96',
      'seed':'6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc',
      'engine':'045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e',
      'codec':'4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297',
      'dynamic':'3845c44744ee0a05300bc237e9b9d10b45ca1272262f09f11e8a3ac2313a9e04'}
I=[0,7,20,27,36,46,57,111]
U0=[17,19,30,38,40,47,52,60]
T20=[4,78,28,110,58,99,81,63,88,37,80,9,11,68,49,87,98,33,92,85]
T28=[4,60,47,17,78,52,19,38,28,110,58,40,99,81,63,88,30,37,80,9,11,68,49,87,98,33,92,85]
OTHER=[0,5,15,67,48,51,111,53,50,69,13,32,18,103,72,59,70,27,89,36,104,106,91,55,71,29,74,23,65,107,95,100,82,2,109,84,97,42,8,10,77,6,12,102,45,86,41,43,7,79,57,44,94,25,16,20,62,46,56,66,1,83,75,31,26,73,54,64,35,22,96,101,24,105,108,90]
def need(ok,label):
    if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path,key):
    raw=path.read_bytes();need(sha(raw)==PINS[key],key+' input pin');return json.loads(gzip.decompress(raw))
def module(path,key):
    need(sha(path.read_bytes())==PINS[key],key+' engine pin')
    sp=importlib.util.spec_from_file_location('public_Gram_'+key,path);obj=importlib.util.module_from_spec(sp)
    sys.modules[sp.name]=obj;sp.loader.exec_module(obj);return obj
def clean(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):clean(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v)for v in value]
    return value
def coordinates(rows,target):
    n=len(rows);A=[[F(rows[j][i])for j in range(n)]+[F(target[i])]for i in range(len(target))]
    for c in range(n):
        k=next((k for k in range(c,len(A))if A[k][c]),None);need(k is not None,'independent actual seven-mode basis')
        A[c],A[k]=A[k],A[c];a=A[c][c];A[c]=[x/a for x in A[c]]
        for k in range(len(A)):
            if k!=c and A[k][c]:a=A[k][c];A[k]=[x-a*y for x,y in zip(A[k],A[c])]
    need(all(not any(row[:-1])and row[-1]==0 for row in A[n:]),'actual target in seven-mode root span')
    return [A[k][-1]for k in range(n)]
def mod_rank(rows,columns,p):
    A=[[int(row.get(j,F(0)).numerator)*pow(row.get(j,F(0)).denominator,-1,p)%p for j in columns]for row in rows]
    r=0
    for c in range(len(columns)):
        k=next((k for k in range(r,len(A))if A[k][c]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];a=pow(A[r][c],-1,p);A[r]=[a*x%p for x in A[r]]
        for k in range(r+1,len(A)):
            if A[k][c]:a=A[k][c];A[k]=[(x-a*y)%p for x,y in zip(A[k],A[r])]
        r+=1
        if r==len(A):break
    return r

def main(args):
    native=load(args.native,args.variant);seed=load(args.seed,'seed')
    e=module(args.engine,'engine');c=module(args.codec,'codec');dyn=module(args.dynamic,'dynamic')
    P=native['live'];oldhost={P[i]:(b,d)for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    H=sorted(oldhost);U=sorted(set(P)-set(H));T=T20 if args.variant=='retained'else T28
    need(set(T).isdisjoint(I)and set(I)<=set(H),'all eight actual public pivots outside restored cycle')
    need(sorted(T+OTHER)==H,'actual cycles partition all hosted ports')
    original=sorted(P+[h+112 for h in P]+[r for pair in oldhost.values()for r in pair]);roles={r:i for i,r in enumerate(original)}
    n=len(roles);need(n==(400 if args.variant=='retained'else 416),'correct independent main input domain')
    X={h:roles[h]for h in P};Y={h:roles[h+112]for h in P};host={h:(roles[b],roles[d])for h,(b,d)in oldhost.items()}
    initial=[native['initial'][r]for r in original];final=[native['final'][r]for r in original]
    v={h:native['frames'][native['initial'][h]][0]for h in P};roots={h:c.root(v[h])for h in P}
    G={(h,j):sum(x*y for x,y in zip(roots[h],roots[j]))/18 for h in P for j in P}
    need(all(G[i,j]==int(i==j)for i in I for j in I),'actual native orthogonal eight-frame')
    need(all(G[h,j]==sum(G[h,i]*G[i,j]for i in I)for h in P for j in P),'exact full104 Gram pivot factorization')
    omitted=c.root(448)
    need(all(sum(x*y for x,y in zip(roots[h],omitted))/18 in(F(0),F(1,2),F(-1,2))for h in P),
         'every actual frame root has zero or half projection on omitted448')
    need(all(any(G[i,j]for i,j in combinations(J,2))for J in combinations(U0,4)),
         'all70 coupled four-subsets contain a real nonorthogonal pair')
    M=U0[1:];beta={h:coordinates([roots[u]for u in M],roots[h])for h in T}
    need(all(z.denominator&(z.denominator-1)==0 for row in beta.values()for z in row),'true dyadic relay coefficients')
    frames=copy.deepcopy(seed['frames']);where={frozenset(e.span(f)):i for i,f in enumerate(frames)}
    def chart(vectors):
        f=c.basis(vectors);S=frozenset(e.span(f))
        if S not in where:where[S]=len(frames);frames.append(f)
        return where[S]
    O=3;Hub=127;lines={h:initial[X[h]]for h in P};facets={h:final[Y[h]]for h in P}
    C=chart([v[u]for u in U0]);CS=e.span(frames[C]);need(len(frames[C])==7,'actual proper bank rank7')
    need(sorted(h for h in P if v[h]in CS)==sorted(T28),'all28 actual native sources inside this bank')
    perm={cy[k]:cy[(k+1)%len(cy)]for cy in(T,OTHER)for k in range(len(cy))};ip={p:h for h,p in perm.items()}
    need(all((v[h]&v[j]).bit_count()%2==0 for h,j in perm.items()),'every public source-line/final-facet assignment legal')
    stops={h:chart(x for x in CS if (x&v[h]).bit_count()%2==0)for h in T}
    need(all(len(frames[stops[h]])==6 and e.span(frames[lines[perm[h]]])<e.span(frames[stops[h]])<e.span(frames[facets[h]])for h in T),'actual proper relay stops')
    qrow={i:{host[h][1]:G[i,h]for h in H if G[i,h]}for i in I}
    rrow={h:e.add({host[h][1]:F(-1)},{host[j][1]:G[h,j]for j in H if G[h,j]})for h in H}
    pre={h:qrow[h]if h in I else rrow[h]for h in H}
    mode={u:{host[h][1]:G[u,h]for h in H if G[u,h]}for u in M}
    out=[];marks={};events={'pivot_correction':[],'q_acquisition':[],'r_acquisition':[],'bank_acquisition':[],
                          'decoded_owner':[],'public_restoration':[],'B_reads':[]}
    def emit(op):out.append(op);return len(out)-1
    def add(d,s,z,C0):return emit(['ADD',d,s,str(z),C0])
    def move(d,A,B,owned=False):return emit(['MOVE',d,A,B,owned])
    def swap(d,s,C0):
        first=add(d,s,1,C0);add(s,d,-1,C0);add(d,s,1,C0);emit(['SCALE',s,'-1',C0]);return first
    for h in U:
        emit(['INIT',n,O]);add(n,Y[h],1,O);move(n,O,lines[h],True);add(X[h],n,-1,lines[h]);emit(['CLEAR',n,lines[h]])
    for i in I:
        emit(['INIT',n,O]);add(n,host[i][1],1,O);move(n,O,lines[i],True)
        events['pivot_correction'].append(add(host[i][0],n,-1,lines[i]));emit(['CLEAR',n,lines[i]])
    S=[h for h in H if h not in I]
    for i in I:
        for h in S:
            if G[i,h]:events['q_acquisition'].append(add(host[i][1],host[h][1],G[i,h],O))
    marks['all_public_q_ready']=len(out)
    for h in S:
        d=host[h][1];emit(['SCALE',d,'-1',O])
        for i in I:
            if G[h,i]:events['r_acquisition'].append(add(d,host[i][1],G[h,i],O))
    for k,u in enumerate(M):
        emit(['INIT',n+k,O])
        for i in I:
            if G[u,i]:events['bank_acquisition'].append(add(n+k,host[i][1],G[u,i],O))
    marks['ground_preload_and_bank_ready']=len(out)
    for cy in(T,OTHER):
        for h,j in zip(cy,cy[1:]):swap(host[h][1],host[j][1],O)
    marks['public_permutation_complete']=len(out)
    for h in H:
        j=perm[h];move(host[h][1],O,lines[j]);events['B_reads'].append(add(host[j][0],host[h][1],1,lines[j]))
    for h in H:move(host[h][0],lines[h],Hub)
    marks['all_B_duties_complete']=len(out)
    for k,u in enumerate(M):move(n+k,O,C,True)
    active=n+7;emit(['INIT',active,lines[T[0]]]);add(active,host[ip[T[0]]][1],1,lines[T[0]])
    move(active,lines[T[0]],C,True);marks['relay_start']=len(out)
    for k,h in enumerate(T):
        emit(['SCALE',active,'-1',C])
        for j,z in enumerate(beta[h]):
            if z:add(active,n+j,z,C)
        events['decoded_owner'].append({'port':h,'step':len(out)})
        move(host[h][1],lines[perm[h]],stops[h]);move(active,C,stops[h],True)
        at=swap(host[h][1],active,stops[h]);events['public_restoration'].append({'port':h,'step':len(out),'first_swap':at,'next':perm[h]})
        move(host[h][1],stops[h],facets[h])
        if k+1<len(T):move(active,stops[h],C,True)
    emit(['CLEAR',active,stops[T[-1]]])
    for k,u in enumerate(M):emit(['CLEAR',n+k,C])
    marks['relay_complete']=len(out)
    for h in OTHER:move(host[h][1],lines[perm[h]],facets[h])
    for h in P:move(X[h],lines[h],Hub);move(Y[h],O,facets[h])
    # Explicit abstract inverse of the final public-D block. This is an
    # algebraic certificate, not a free cochart decoder at final facets.
    inverse={}
    for h in S:
        if h in T:inverse[h]={host[h][1]:F(1)}
        else:inverse[h]=e.add({host[ip[h]][1]:F(-1)},{host[ip[i]][1]:G[h,i]for i in I if G[h,i]})
    for i in I:
        inverse[i]={host[ip[i]][1]:F(1)}
        for h in S:inverse[i]=e.add(inverse[i],inverse[h],-G[i,h])
    word={'schema':'moonshot-S012-public-Gram-bank-proper-relay-v1','public':n,'owned_fields':8,
        'initial':initial,'final':final,'frames':frames,'source_role_map':roles,'program':out,'source_pins':PINS,
        'public_Gram_bank':{'variant':args.variant,'pivot_ports':I,'restored_targets':T,'unrestored_targets':OTHER,
          'preload_nonpivots':S,'permutation':perm,'inverse_permutation':ip,'bank':C,'bank_modes':M,'beta':clean(beta),
          'stops':stops,'active_owner':active,'markers':marks,'events':events,'final_D_abstract_inverse':clean(inverse),
          'final_pivot_payload_locations':{i:{'carrier_port':ip[i],'field':host[ip[i]][1],'chart':facets[ip[i]]}for i in I},
          'inverse_requires_real_future_acquisition':True,'all_pivot_q_are_genuine_public_values':True}}
    restored_at={z['step']:z for z in events['public_restoration']};decoded_at={z['step']:z for z in events['decoded_owner']}
    retired=[];checks=Counter()
    def capture(t,op,rr,ll):
        step=t+1
        if step==marks['all_public_q_ready']:
            need(all(rr[host[i][1]]==qrow[i]for i in I),'actual original-data Gram values in eight public pivots');checks['public_pivots']+=8
        if step==marks['ground_preload_and_bank_ready']:
            need(all(rr[host[h][1]]==pre[h]for h in H),'exact public q/r preload')
            need(all(rr[n+k]==mode[u]for k,u in enumerate(M)),'seven pure Gram rows from genuine public pivots')
            checks['ground_mode_bank']+=7
        if step in decoded_at:
            h=decoded_at[step]['port'];need(rr[active]=={host[h][1]:F(1)}and ll[active]==C,'actual relay original d before import');checks['original_d_import']+=1
        if step in restored_at:
            z=restored_at[step];h=z['port']
            need(rr[host[h][1]]=={host[h][1]:F(1)}and rr[active]==rrow[z['next']],'swap restores original D and retains actual next r');checks['swap_restoration']+=1
        if step<len(out)and out[step][0]=='CLEAR':
            d=out[step][1];need(bool(rr[d]),'actual dirty retirement');retired.append({'operation':step,'role':d,'chart':ll[d],'support':len(rr[d])})
    rows,locations,bill=dyn.replay(word,out,e,capture);want={j:{j:F(1)}for j in range(n)}
    for h in U:want[X[h]][Y[h]]=F(-1)
    for h,(b,d)in host.items():
        want[b]=e.add({b:F(1)},rrow[h]);want[d]={d:F(1)}if h in T else pre[perm[h]]
    need(rows==want and locations==dict(enumerate(final)),'every original public input coefficient and literal native endpoint')
    need(e.exact_rank(rows.values())==n,'full rational public rank')
    for h in H:
        recovered={}
        for d,z in inverse[h].items():recovered=e.add(recovered,rows[d],z)
        need(recovered=={host[h][1]:F(1)},'explicit terminal dyadic inverse for original D '+str(h))
    need(all(z.denominator&(z.denominator-1)==0 for row in inverse.values()for z in row.values()),'entire abstract inverse is dyadic')
    dcols=[host[h][1]for h in H];dranks={p:mod_rank([rows[d]for d in dcols],dcols,p)for p in(3,5,7)}
    need(all(r==len(H)for r in dranks.values()),'complete terminal D rank over three odd finite fields')
    reverse=e.exact_rank([e.add(rows[b],{b:F(1),d:F(-1)},F(-1))for b,d in host.values()]);need(reverse==8,'all original B duties retain exactly rank8 Gram debt')
    need(sum(rows[d]=={d:F(1)}for b,d in host.values())==len(T),'exact original-D restoration count')
    raw=Counter();owned=Counter();facet_visits=[]
    for k,op in enumerate(out):
        if op[0]=='MOVE':
            (owned if op[4]else raw)[abs(len(frames[op[3]])-len(frames[op[2]]))]+=1
            if op[4]and op[3]in set(facets[h]for h in H):facet_visits.append(k)
    expectedraw={1:96,2:20,5:20,7:76,8:304}if args.variant=='retained'else{1:104,2:28,5:28,7:76,8:312}
    expectedowned={1:55,6:1,7:7}if args.variant=='retained'else{1:63,6:1,7:7}
    need(raw==Counter(expectedraw)and owned==Counter(expectedowned),'complete paid public and owned movement ledger')
    need(sum(k*v for k,v in raw.items())==8*n and not facet_visits,'all public rank mass and zero owned hosted-facet visits')
    scalars=[F(op[3]if op[0]=='ADD'else op[2])for op in out if op[0]in('ADD','SCALE')]
    need(all(z.denominator&(z.denominator-1)==0 for z in scalars),'all actual operations dyadic')
    need(bill['lifetimes']==len(retired)==(24 if args.variant=='retained'else 16)and bill['peak']==8,'all owner lifetimes and reduced physical peak')
    controls=[];chosen={'omit_paid_pivot_B_correction':events['pivot_correction'][0],
        'wrong_actual_public_q_shear':events['q_acquisition'][0],'wrong_nonpivot_preload':events['r_acquisition'][0],
        'wrong_actual_mode_bank':events['bank_acquisition'][0],'wrong_relay_sign':marks['relay_start'],
        'wrong_dirty_swap':events['public_restoration'][0]['first_swap']+1,'omit_real_B_read':events['B_reads'][0]}
    for label,k in chosen.items():
        bad=copy.deepcopy(word);op=bad['program'][k]
        if op[0]=='ADD':op[3]='0'if label.startswith('omit_')else str(-F(op[3]))
        elif op[0]=='SCALE':op[2]='1'
        else:raise ValueError('negative-control opcode')
        try:rr,ll,_=dyn.replay(bad,bad['program'],e);rejected=rr!=rows or ll!=locations
        except ValueError:rejected=True
        need(rejected,'negative control '+label);controls.append(label)
    # Terminal arithmetic control, deliberately not represented as a legal
    # free final-facet operation: replace all eight saved q rows by r rows.
    erased=copy.deepcopy(rows)
    for i in I:erased[host[ip[i]][1]]=rrow[i]
    lostrank=mod_rank([erased[d]for d in dcols],dcols,3)
    need(lostrank<len(H),'deleting the public Gram information recreates a mod3 obstruction')
    payload=(json.dumps(clean(word),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    result={'status':'PASS_PUBLIC_GRAM_BANK_DYADIC_RELAY_SOURCE','variant':args.variant,'word_sha256':sha(blob),
       'native_sha256':PINS[args.variant],'source_pins':PINS,'public':n,'full_input_rank':n,'hosted':len(H),
       'original_D_restored':len(T),'original_D_unrestored':len(OTHER),'terminal_D_determinant':'-1',
       'explicit_dyadic_inverse_checked':True,'terminal_D_modular_ranks':dranks,'terminal_public_q_replaced_by_r_mod3_rank':lostrank,
       'final_public_pivot_payload_locations':word['public_Gram_bank']['final_pivot_payload_locations'],
       'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),'reverse_residual_rank':reverse,
       'forward_endpoint_debt':104+len(U),'paired_forward_required':'I-G on hosted block; unchanged Y remains unpaired',
       'owned_hosted_facet_visits':facet_visits,'all_actual_scalars_dyadic':True,'retirements':retired,
       'chronology_checks':dict(checks),'negative_controls':controls,
       'scope':'Actual public storage of eight Gram directions repairs old terminal arithmetic loss.76 original D restorations, all forward and paired completion remain open. No new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('status','variant','word_sha256','public','original_D_restored','terminal_D_modular_ranks','terminal_public_q_replaced_by_r_mod3_rank','source_bill','raw_histogram','owned_histogram')},sort_keys=True,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--codec',type=Path,required=True);p.add_argument('--dynamic',type=Path,required=True)
    p.add_argument('--variant',choices=('retained','allhosted'),required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
