#!/usr/bin/env python3
"""Independent paid-repartition composition and fresh all-hosted source audit.

Reuses the previously independently authored root replay kernel, credited in
REVIEW.md. @CubeJerry with OpenAI assistance. Apache-2.0.
"""
import argparse, copy, gzip, hashlib, importlib.util, json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def rank(rows):
    basis = {}
    for original in rows:
        row = dict(original)
        for j in sorted(basis):
            if j in row:
                c = row[j]
                for k, value in basis[j].items():
                    v = row.get(k, F(0)) - c * value
                    if v: row[k] = v
                    else: row.pop(k, None)
        if row:
            j = min(row); c = row[j]
            basis[j] = {k: v / c for k, v in row.items()}
    return len(basis)

def determinant(matrix):
    a = [[F(v) for v in row] for row in matrix]; answer = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None: return F(0)
        if pivot != j: a[j], a[pivot] = a[pivot], a[j]; answer = -answer
        x = a[j][j]; answer *= x
        a[j] = [v/x for v in a[j]]
        for i in range(j+1, len(a)):
            c = a[i][j]
            a[i] = [v-c*w for v,w in zip(a[i], a[j])]
    return answer

def root_vector(bits):
    on = [i for i in range(9) if bits >> i & 1]
    if len(on) == 3: return [2 if i in on else -1 for i in range(9)]
    off = [i for i in range(9) if not (bits >> i & 1)]
    need(len(off) == 2, 'native real root type')
    return [3*(int(i == off[0])-int(i == off[1])) for i in range(9)]

from itertools import combinations
from engine import replay,span,plus

BASE=Path(__file__).resolve().parents[2]
AUTHOR=BASE/'worker-b/native-repartition'
REPO=BASE/'programme'

def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def dot(a,b):return sum(x*y for x,y in zip(a,b))

def roles(w):
    live=w['live'];host={live[i]:(b,d)for i,b,d in zip(w['hosted']['Dports'],w['hosted']['X2'],w['hosted']['Y2'])}
    main=set(live)|{h+112 for h in live}|{j for pair in host.values()for j in pair}
    return host,main

def target(w):
    host,main=roles(w);r={i:{i:F(1)}for i in range(w['public'])}
    for h in w['live']:
        y=h+112
        if h in host:r[y]={y:F(1),h:F(1)}
        else:r[h]={h:F(1),y:-F(1)};r[y]={h:F(1,2),y:F(1,2)}
    for b,d in host.values():r[b]={b:F(1),d:-F(1)}
    return r

def scalar_ops(ops,rows):
    for o in ops:
        tag,d=o[:2]
        if tag=='INIT':need(d not in rows,'fresh scalar adapter owner');rows[d]={}
        elif tag=='CLEAR':need(d in rows,'actual scalar adapter retirement');del rows[d]
        elif tag=='ADD':rows[d]=plus(rows[d],rows[o[2]],F(o[3]))
        elif tag=='COPY':rows[d]={j:F(o[3])*v for j,v in rows[o[2]].items()if F(o[3])*v}
        elif tag=='SCALE':rows[d]={j:F(o[2])*v for j,v in rows[d].items()if F(o[2])*v}
        else:need(tag=='MOVE','literal scalar instruction')

def physical(w):
    spaces=[span(f)for f in w['frames']];loc=dict(enumerate(w['initial']));pub=w['public'];paid=Counter();raw=Counter();owned=Counter();peak=life=0;counts=Counter()
    for o in w['program']:
        tag,d=o[:2];counts[tag]+=1
        if tag=='INIT':need(d>=pub and d not in loc,'fresh owned lifetime');loc[d]=o[2];life+=1
        elif tag=='CLEAR':need(d>=pub and loc[d]==o[2],'actual owned retirement');del loc[d]
        elif tag=='MOVE':
            _,d,a,b,isowned=o;need(loc[d]==a and isowned==(d>=pub),'actual physical source and ownership')
            need((spaces[a]<spaces[b])or(isowned and spaces[b]<spaces[a]),'monotone public and nested owned moves')
            k=abs(len(w['frames'][a])-len(w['frames'][b]));paid[k]+=1;(owned if isowned else raw)[k]+=1;loc[d]=b
        elif tag=='SCALE':need(loc[d]==o[-1],'cochart scalar')
        else:need(tag in('ADD','COPY')and d!=o[2]and loc[d]==loc[o[2]]==o[-1],'genuine cochart read')
        if tag in('ADD','COPY','SCALE'):
            v=F(o[2]if tag=='SCALE'else o[3]);need(v and abs(v)+1<2**16,'bounded nonzero scalar')
            den=v.denominator
            for p in[2,3,5]:
                while den%p==0:den//=p
            need(den==1,'retained smooth denominator')
        peak=max(peak,len(loc)-pub)
    need(set(loc)==set(range(pub))and list(loc.values())==w['final'],'all final public charts and owners closed')
    host,main=roles(w);helper=Counter()
    for i in range(pub):
        if i not in main:
            need(spaces[w['initial'][i]]<spaces[w['final'][i]],'each independent helper has a positive original boundary')
            helper[len(w['frames'][w['final'][i]])-len(w['frames'][w['initial'][i]])]+=1
    need(pub-len(main)==1080,'all1080 independent original helpers retained')
    return {'paid':dict(paid),'raw':dict(raw),'owned':dict(owned),'helpers':dict(helper),'peak':peak,'lifetimes':life,'counts':dict(counts),'main':len(main),'public':pub}

def converted(old,w,mutant=None):
    m=w['repartition'];oldpub=old['public'];z={int(k):v for k,v in m['zero_extension_old_to_owned'].items()};growth=w['public']-oldpub;first=m['markers']['old_body_begin'];last=m['markers']['old_body_end']
    def rename(r):return z.get(r,r+growth if r>=oldpub else r)
    for e,o in zip(w['program'][first:last],old['program']):
        want=o.copy();want[1]=rename(o[1])
        if o[0]in('ADD','COPY'):want[2]=rename(o[2])
        if o[0]=='MOVE'and o[1]in z:want[4]=True
        need(e==want,'every retained original operation has only exact role/ownership renaming')
    need(last-first==len(old['program']),'entire old body retained')
    host,main=roles(w);oldhost,oldmain=roles(old);need(w['frames']==old['frames'],'same complete native chart domain')
    need(set(range(oldpub))-oldmain==set(range(w['public']))-main,'exact same1080 helper identities')
    rows={i:{i:F(1)}for i in range(w['public'])};prefix=copy.deepcopy(w['program'][:first]);suffix=copy.deepcopy(w['program'][last:])
    if mutant is not None:
        where,index=mutant
        if where=='prefix':prefix[index][3]=str(-F(prefix[index][3]))
        elif where=='suffix':suffix[index-last][3]=str(-F(suffix[index-last][3]))
        else:prefix.insert(len(z),['ADD',next(iter(z.values())),old['live'][0]+112,'1',3])
    scalar_ops(prefix,rows);before={i:dict(row)for i,row in rows.items()};oldtarget=target(old)
    for r,coefs in oldtarget.items():
        out={}
        for j,c in coefs.items():out=plus(out,before[rename(j)],c)
        rows[rename(r)]=out
    zeros={r:rows[owned]for r,owned in z.items()};need(all(not row for row in zeros.values()),'all removed old dual outputs truly zero before retirement')
    scalar_ops(suffix,rows);need(rows==target(w),'all independent public input/output entries after actual adapters and inherited complete body')
    need(all(rows[i]=={i:F(1)}for i in set(range(w['public']))-main),'every helper identity retains independence')
    return {'inherited_body_operations':last-first,'all_public_columns':w['public'],'all_public_rows':len(rows),'helpers':1080,'zero_extension_outputs':len(zeros),'new_main_inputs':len(main)-len(oldmain),'inherited_body_scope':'Exact literal operation equality plus admitted original complete native target; old source arithmetic is not relabelled as a fresh independent proof.'}

def complete_review(old,w,caller,oldcaller,full):
    m=w['repartition'];info=physical(w);comp=converted(old,w);oldH,oldmain=roles(old);newH,newmain=roles(w);r=len(set(oldH)-set(newH));s=len(set(newH)-set(oldH))
    need((r,s)==((5,5)if m['variant']=='orthogonal'else(0,8)),'actual partition differences')
    if r:
        rr=[root_vector(w['frames'][w['initial'][h]][0])for h in m['new_coupled']]
        need([[dot(a,b)for b in rr]for a in rr]==[[18*int(i==j)for j in range(8)]for i in range(8)],'actual real orthogonal new coupled frame')
    oldN={int(k):v for k,v in full['native']['paid'].items()};oldhelpers={int(k):v for k,v in full['native']['helpers'].items()}
    expected=Counter(oldN);expected[1]+=r+3*s;expected[8]+=2*s
    need(info['paid']==dict(expected)and info['helpers']==oldhelpers,'every old operation and helper plus full paid adapter profile')
    norm=copy.deepcopy(caller)
    for t in['A','B']:norm['types'][t]['ports']=oldcaller['types'][t]['ports']
    need(norm==oldcaller,'only actual caller membership changes')
    need(caller['types']['A']['ports']==w['hosted']['Dports']and caller['types']['B']['ports']==[i for i in range(104)if i not in set(w['hosted']['Dports'])],'caller matches exact converted interface')
    T=Counter();P=Counter();calls=0
    for e in caller['events']:
        if e[0]=='J':calls+=1;T.update(info['helpers']);P.update(info['paid'])
        elif e[1]=='QUERY':P[1]+=len(caller['types'][e[0]]['ports'])
        elif e[1]=='IDLE_ONE':P[8*len(e[3])]+=len(caller['types'][e[0]]['ports'])
    for d in caller['types'].values():
        for q,z,*mask in d['diagonal']:T[q%2+8*sum(mask)]+=len(d['ports'])
    need(calls==18,'all18 actual native calls retained')
    delta={k:T[k]-P[k]-int(full['invoice']['T'].get(str(k),0))+int(full['invoice']['P'].get(str(k),0))for k in set(T)|set(P)};delta={k:v for k,v in delta.items()if v}
    want={1:-18*(r+3*s),8:-36*s}if r else{1:-432};need(delta==want,'signed whole-caller change before moment evaluation')
    neg=[]
    for key in['A_to_B_entries','B_to_A_entries','new_dual_entries','B_to_A_output_repairs']:
        events=m['events'][key]
        if not events:continue
        t=events[0][1];where='prefix'if t<m['markers']['old_body_begin']else'suffix'
        try:converted(old,w,(where,t))
        except ValueError as e:neg.append({'mutation':key,'rejected_by':str(e)})
        else:raise ValueError('adapter sign mutation passed')
    if r:
        try:converted(old,w,('dirty',0))
        except ValueError as e:neg.append({'mutation':'dirty_zero_extension','rejected_by':str(e)})
        else:raise ValueError('dirty zero extension accepted')
    return {'variant':m['variant'],'composition':comp,'physical':info,'caller_T':dict(T),'caller_P':dict(P),'signed_caller_change':delta,'negative_controls':neg,'ordinary':ordinary_bound(w,caller,info)}

def ordinary_bound(w,c,info):
    scalar=0;odd=0
    for o in w['program']:
        if o[0]in('ADD','COPY','SCALE'):
            v=F(o[2]if o[0]=='SCALE'else o[3]);num=abs(v.numerator);den=v.denominator
            scalar+=4*(num.bit_length()+den.bit_length()+1+(num.bit_count()if o[0]!='SCALE' else 0));odd+=bool(den&(den-1))
    A=len(c['types']['A']['ports']);ports=sum(len(v['ports'])for v in c['types'].values())
    routing=1000*(sum(info['paid'].values())+2*sum(info['helpers'].values())+6*ports+6*A+4*info['lifetimes'])
    rest=0;lambda_count=0
    def swap(axes):return len(set(axes)-set(range(len(axes))))
    for ty,data in c['types'].items():
        p=len(data['ports']);nr=data['roles'];ev=[e for e in c['events']if e[0]in(ty,'J')];qs=[e for e in ev if e[0]==ty and e[1]=='QUERY'];idle=[e for e in ev if e[0]==ty and e[1]=='IDLE_ONE']
        lambda_count+=p*sum(e[0]==ty and e[1]=='LAMBDA'for e in ev)
        rest+=32*nr*p*len(ev)+16*p*len(qs)+26*nr*p
        for qp,z,*mask in data['diagonal']:
            axes=([0]if qp else[])+[a for k,v in enumerate(mask)if v for a in range(9+8*k,17+8*k)]
            rest+=p*1000*(2*swap(axes)+2*bool(qp)+(qp==-1))
        rest+=sum(2*p*1000*swap([a for k in e[3]for a in range(1+8*k,9+8*k)])for e in idle)
        rest+=sum(p*1000*(2+(e[4]==-1))for e in qs)
    total=18*(scalar+routing)+rest+18*w['public']*104+1000*lambda_count
    need(total==(829505256 if A==96 else 816530592)and total<10**9,'complete conservative ordinary invoice reconstructed')
    return {'conservative_total':total,'scalar_upper':scalar,'routing_upper':routing,'caller_rest':rest,'old_odd_division_operations':odd,'classification':'Inherited ordinary accounting conventions independently enumerated; no new precision theorem.'}

def partial_context(native,w):
    nh,main=roles(native);live=native['live'];oldroles=sorted(main);role={int(k):v for k,v in w['source_role_map'].items()}
    need(len(main)==416 and len(nh)==104 and role==dict(zip(oldroles,range(416))),'416 actual independent promoted inputs')
    need(w['initial']==[native['initial'][i]for i in oldroles]and w['final']==[native['final'][i]for i in oldroles],'exact416 initial/final interfaces')
    need(w['frames'][:len(native['frames'])]==native['frames'],'actual native chart prefix')
    X={h:role[h]for h in live};Y={h:role[h+112]for h in live};H={h:(role[b],role[d])for h,(b,d)in nh.items()};spaces=[span(f)for f in w['frames']]
    vv={h:native['frames'][native['initial'][h]][0]for h in live};rr={h:root_vector(vv[h])for h in live};m=w['allhosted'];Z=m['omitted_frame'];need(Z==[7,25,42,52,76,82,97,127],'omitted real frame pin')
    rz=[root_vector(z)for z in Z];g=[{h:F(dot(r,rr[h]),18)for h in live}for r in rz]
    need([[dot(a,b)for b in rz]for a in rz]==[[18*int(i==j)for j in range(8)]for i in range(8)],'orthogonal omitted basis')
    need([[sum(g[i][h]*g[j][h]for h in live)for j in range(8)]for i in range(8)]==[[13*int(i==j)for j in range(8)]for i in range(8)],'genuine104-input tight frame13')
    G={h:{j:F(dot(rr[h],rr[j]),18)for j in live}for h in live}
    need(all(G[h][j]==sum(g[i][h]*g[i][j]for i in range(8))for h in live for j in live),'all10816 native Gram entries')
    classes={}
    for h in live:
        support=tuple(i for i in range(8)if g[i][h]);need(len(support)==4,'four coordinates per native root');classes.setdefault(support,[]).append(h)
    need(len(classes)==14 and set(classes)=={tuple(z['modes'])for z in m['groups']},'complete fourteen native classes')
    co={};codecs=[]
    for z in m['groups']:
        ports=z['ports'];modes=z['modes'];piv=z['pivots'];n=len(ports);C=z['C3']
        need(ports==classes[tuple(modes)]and z['D_roles']==[H[h][1]for h in ports]and z['Y_roles']==[Y[h]for h in ports],'literal full independent class banks')
        s={0}
        for i in modes:s|={x^Z[i]for x in tuple(s)}
        need(spaces[C]==frozenset(s)and len(s)==8,'actual rank3 source chart')
        need(len(piv)==len(set(piv))==4 and all(0<=p<n for p in piv),'four actual distinct independent-input pivots')
        M=[[F(i==j)for j in range(n)]for i in range(n)]
        for i,p in zip(modes,piv):M[p]=[g[i][h]for h in ports]
        det=determinant(M);need(det and M==[[F(x)for x in row]for row in z['M']],'exact invertible full-input encoder')
        encoded={i:{i:F(1)}for i in range(n)}
        for tag,a,b,c in z['encoder']:
            if tag=='ADD':encoded[a]=plus(encoded[a],encoded[b],F(c))
            else:need(tag=='SCALE','codec elementary opcode');encoded[a]={j:F(c)*v for j,v in encoded[a].items()if F(c)*v}
        need([[encoded[i].get(j,F(0))for j in range(n)]for i in range(n)]==M,'literal encoder matrix independently reconstructed')
        for h in ports:co[h]=tuple(modes);need(spaces[C]<spaces[w['final'][Y[h]]],'class proper receiver facet')
        codecs.append({'modes':modes,'ports':len(ports),'determinant':str(det)})
    need(Counter(i for z in m['groups']for i in z['modes'])==Counter({i:7 for i in range(8)}),'every mode occurs in exactly seven classes')
    for i,L in enumerate(m['lines']):need(spaces[L]==frozenset([0,Z[i]]),'actual omitted source line')
    halves={};cache={int(k):v for k,v in m['cache_roles'].items()}
    for z in m['halves']:
        T=z['ports'];S=z['sources'];C4=z['C4'];C3=z['C3'];need(set(T+S)==set(classes[co[T[0]]])and set(T).isdisjoint(S),'exact class split')
        need(all(G[h][j]==int(h==j)for h in T for j in T),'real orthogonal receiver half')
        need(all(G[h][j]for h in T for j in S),'all actual cross-half contacts')
        space=set(spaces[C3])
        for j in S:space|={x^vv[j]for x in tuple(space)}
        need(spaces[C4]==frozenset(space)and len(space)==16,'actual minimal proper rank4 half chart')
        need([j for j in live if vv[j]in space]==sorted(S),'full104 exact source incidence')
        need([h for h in live if spaces[C4]<=spaces[w['final'][Y[h]]]]==sorted(T),'full104 exact receiver incidence')
        for h in T:halves[h]=z
    parity=m['variant']=='parity';need((len(halves),len(cache))==((104,104)if parity else(0,0)),'every parity cache belongs to one true half')
    L={h:{j:(F(h==j)if parity and co[h]==co[j]else G[h][j])for j in live}for h in live}
    q=[{H[h][1]:g[i][h]for h in live if g[i][h]}for i in range(8)];p=[{X[h]:g[i][h]for h in live if g[i][h]}for i in range(8)]
    return dict(role=role,live=live,X=X,Y=Y,H=H,spaces=spaces,g=g,G=G,L=L,q=q,p=p,halves=halves,cache=cache,codecs=codecs,parity=parity)

def partial_audit(w,c,full=True):
    X=c['X'];Y=c['Y'];H=c['H'];g=c['g'];G=c['G'];L=c['L'];live=c['live'];q=c['q'];p=c['p'];cache=c['cache'];halves=c['halves'];parity=c['parity'];m=w['allhosted'];marks=m['markers'];events=m['events'];lines=m['lines']
    expected={}
    for h in live:
        b,d=H[h];expected[X[h]]={X[h]:F(1)};expected[d]={d:F(1)}
        expected[Y[h]]=plus({Y[h]:F(1)},{X[j]:L[h][j]for j in live if L[h][j]},1)
        expected[b]=plus({b:F(1)},{H[j][1]:-L[j][h]for j in live if L[j][h]},1)
    zrows={h:{X[j]:-G[h][j]for j in halves[h]['sources']}for h in halves};bytime={};seen=[];reads=Counter()
    for group in m['groups']:
        bytime.setdefault(group['markers']['D_restored_at_C3'],[]).append(('D',group))
        bytime.setdefault(group['markers']['full_Y_Gram_decoded'],[]).append(('Y',group))
    for half in m['halves']:bytime.setdefault(half['markers']['actual_caches'],[]).append(('cache',half))
    def after(t,rows,loc):
        for kind,z in bytime.get(t,[]):
            seen.append((t,kind))
            if kind=='D':need(all(rows[H[h][1]]=={H[h][1]:F(1)}and loc[H[h][1]]==z['C3']for h in z['ports']),'all original independent D restored at C3')
            elif kind=='Y':need(all(rows[Y[h]]==plus({Y[h]:F(1)},{X[j]:G[h][j]for j in live if G[h][j]},1)and loc[Y[h]]==z['C3']for h in z['ports']),'actual full Gram Y decoded before local correction')
            else:
                need(all(rows[cache[h]]==zrows[h]and loc[cache[h]]==z['C4']for h in z['ports']),'genuine stationary forward cache')
                need(all(rows[H[h][1]]=={H[h][1]:F(1)}and loc[H[h][1]]==z['C4']for h in z['ports']),'original D present for transpose service')
                need(all(rows[X[j]]=={X[j]:F(1)}and loc[X[j]]==z['C4']for j in z['sources']),'original X present for local paired source')
        if t==marks['all_D_restored_and_reverse_acquired']:
            need(all(rows[H[h][1]]=={H[h][1]:F(1)}for h in live),'all104 original D remain independent')
            need(all(rows[416+i]==q[i]and loc[416+i]==lines[i]for i in range(8)),'actual reverse history includes all104 original D');seen.append((t,'reverse'))
        if t==marks['all_XB_at_Hub_and_D_at_endpoints']:
            need(all(rows[X[h]]=={X[h]:F(1)}and loc[X[h]]==loc[H[h][0]]==127 and rows[H[h][1]]=={H[h][1]:F(1)}and loc[H[h][1]]==w['final'][H[h][1]]for h in live),'all actual X/B arrived and all D at final facets');seen.append((t,'hub'))
        if t==marks['all_forward_modes_at_lines']:
            need(all(rows[416+i]==p[i]and loc[416+i]==lines[i]for i in range(8)),'actual original-X forward modes')
            need(all(rows[H[h][0]]==expected[H[h][0]]for h in live),'all actual reverse endpoints complete to partial target');seen.append((t,'forward'))
    reverse=set(events['reverse_consumers']);forward=set(events['forward_reads']);lf=set(events['local_forward_sources']);lr=set(events['local_reverse_reads']);cr=set(events['correction_reads'])
    reverse_h={b:h for h,(b,d)in H.items()};Xh={x:h for h,x in X.items()};Dh={d:h for h,(b,d)in H.items()};Yh={y:h for h,y in Y.items()};ch={v:h for h,v in cache.items()}
    def hook(t,phase,o,rows,loc):
        if phase=='after':after(t,rows,loc);return
        if o[0]=='MOVE'and not o[-1]:need(c['spaces'][o[2]]<c['spaces'][o[3]],'every public source route monotone')
        if t in reverse:
            h=reverse_h[o[1]];i=o[2]-416;need(rows[o[2]]==q[i]and loc[o[2]]==127 and F(o[3])==-g[i][h],'actual full reverse delivery');reads['reverse']+=1
        if t in forward:
            i=o[2]-416;need(rows[o[2]]==p[i]and loc[o[2]]==lines[i],'actual full forward delivery');reads['forward']+=1
        if t in lf:
            h=ch[o[1]];j=Xh[o[2]];need(j in halves[h]['sources']and rows[o[2]]=={X[j]:F(1)}and F(o[3])==-G[h][j],'actual original-X local source');reads['local_forward']+=1
        if t in lr:
            j=reverse_h[o[1]];h=Dh[o[2]];need(j in halves[h]['sources']and rows[o[2]]=={H[h][1]:F(1)}and F(o[3])==G[h][j],'actual original-D transpose service');reads['local_reverse']+=1
        if t in cr:
            h=Yh[o[1]];need(o[2]==cache[h]and rows[o[2]]==zrows[h]and loc[o[2]]==halves[h]['C4']and F(o[3])==1,'actual cached correction after Gram decoder');reads['correction']+=1
    rows,loc,raw,owned,counts,peak,life,tr,retire=replay(w,mode='new_allhosted',hook=hook)
    need(rows==expected,'all416 independent-input endpoint rows, with genuine new dual contributions')
    need([loc[i]for i in range(416)]==w['final'],'every416 exact final chart')
    need(len(seen)==31+len(m['halves']),'all actual source chronology cuts')
    want={1:320,2:112,3:304,4:208,5:208,8:16}if parity else{1:112,2:112,3:96,5:208,8:224}
    need(dict(Counter(raw)+Counter(owned))==want and owned=={8:16},'complete actual movement invoice')
    need(sum(k*v for k,v in raw.items())==3328 and peak==(112 if parity else 8)and life==(120 if parity else 16),'actual all416 raw rank mass and ownership')
    need(all(payload for t,i,ch,payload in retire)and len(retire)==life,'every actual retirement dirty, inherited assumption retained')
    if not full:return True
    need(rank(list(rows.values()))==416,'full actual arbitrary-input rank416')
    need(all(rows[b].get(dj,F(0))+rows[Y[j]].get(X[h],F(0))==0 for h,(b,d)in H.items()for j,(bj,dj)in H.items()),'all10816 paired adjoint entries')
    residual=rank([{j:L[h][j]-int(h==j)for j in live if L[h][j]!=int(h==j)}for h in live]);need(residual==(56 if parity else 104),'fresh full-domain residual rank')
    debt=sum(bool(L[h][j])for h in live for j in live if h!=j);need(debt==(4608 if parity else 4992),'whole remaining actual forward contact debt')
    return {'variant':m['variant'],'public_rank':416,'paired_entries':10816,'residual_rank':residual,'offdiagonal_debt':debt,'counts':counts,'peak':peak,'lifetimes':life,'dirty_retirements':len(retire),'raw':raw,'owned':owned,'Q':want,'chronology_checks':len(seen),'actual_reads':dict(reads),'codecs':c['codecs']}

def partial_controls(w,c):
    events=w['allhosted']['events'];jobs=[]
    for key in['reverse_consumers','forward_reads','local_forward_sources','local_reverse_reads','correction_reads']:
        if events[key]:jobs.append((key,events[key][0]))
    first_D=w['allhosted']['groups'][0]['markers']['D_restored_at_C3']-1;jobs.append(('D_inverse_codec',first_D))
    out=[]
    for label,t in jobs:
        bad=copy.deepcopy(w);o=bad['program'][t];need(o[0]in('ADD','SCALE'),'literal decoder/read control')
        if o[0]=='ADD':o[3]=str(-F(o[3]))
        else:o[2]=str(2*F(o[2]))
        try:partial_audit(bad,c,False)
        except (ValueError,KeyError)as e:out.append({'mutation':label,'instruction':t,'rejected_by':str(e)})
        else:raise ValueError('source mutant accepted '+label)
    # Removing an independent promoted D cannot be excused as an old coupled zero.
    d=c['H'][17][1];need(d>=400,'promoted genuine dual input')
    bad=copy.deepcopy(w);bad['program'].insert(0,['SCALE',d,'0',3])
    try:partial_audit(bad,c,False)
    except (ValueError,KeyError)as e:out.append({'mutation':'suppress_promoted_independent_D','rejected_by':str(e)})
    else:raise ValueError('old zero-coupled premise accepted')
    return out

def phase_review(w,parent,path):
    need(w['frames'][:len(parent['frames'])]==parent['frames'],'phase parent exact chart prefix')
    inherited={(o[2],o[3])for o in parent['program']if o[0]=='MOVE'};used={(o[2],o[3])for o in w['program']if o[0]=='MOVE'};new=used-inherited
    data=load(path);recs=data['recipes'];need({(r['source'],r['target'])for r in recs}==new and len(recs)==len(new),'all and only introduced ordered maps certified')
    engine=REPO/'research/moonshot-005-program/results/complex-omitted-line-gram/author/dependencies/native_verify.py';pin='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38';need(hashlib.sha256(engine.read_bytes()).hexdigest()==pin,'retained independent phase interpreter')
    sp=importlib.util.spec_from_file_location('repartition_review_phase',engine);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
    for r in recs:
        a,b=r['source'],r['target'];need((r['source_frame'],r['target_frame'])==(w['frames'][a],w['frames'][b]),'actual literal recipe frames')
        need(r['rank']==r['recipe']['rank']==abs(len(w['frames'][a])-len(w['frames'][b])),'true nested rank in recipe')
        v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(w['frames'][a],9))+v.frame(w['frames'][b],9),'exact signed map')
    rejected=None
    if recs:
        r=copy.deepcopy(recs[0]);r['recipe']['left']['phase']=(r['recipe']['left']['phase']+1)%4
        try:v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(r['source_frame'],9))+v.frame(r['target_frame'],9),'wrong phase')
        except ValueError:rejected=True
        else:raise ValueError('wrong phase accepted')
    return {'introduced_maps':len(new),'inherited_used_maps':len(used&inherited),'phase_mutation_rejected':rejected,'scope':'Retained-interpreter certificate reproduction; zero-new-map case inherits exact pinned parent evidence.'}

def compare_invoices(full,complete,partial):
    def combine(*terms):
        out={}
        for c,d in terms:
            for k,v in d.items():out[int(k)]=out.get(int(k),F(0))+F(c)*F(v)
        return {k:v for k,v in out.items()if v}
    B=10**35;cache={}
    def bound(n):
        if n not in cache:
            N=n**199*B**200;lo=0;hi=n*B+1
            while hi-lo>1:
                m=(lo+hi)//2
                if m**200<=N:lo=m
                else:hi=m
            need(lo**200<=N<hi**200,'exact radical brackets');cache[n]=(F(lo,B),F(hi,B))
        return cache[n]
    def moment(d):
        lo=hi=F(0)
        for n,c in d.items():
            a,b=bound(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
        return lo,hi
    oldbase=combine((F(1,18),full['invoice']['T']),(-F(1,18),full['invoice']['P']),(1,full['native']['paid']),(-1,full['native']['helpers']))
    converted=[]
    for r in complete:
        base=combine((F(1,18),r['caller_T']),(-F(1,18),r['caller_P']),(1,r['physical']['paid']),(-1,r['physical']['helpers']))
        penalty=moment(combine((F(1,18),r['caller_P']),(-F(1,18),r['caller_T'])))
        if r['variant']=='allhosted':
            need(combine((1,base),(-1,oldbase))=={8:F(16)},'all-hosted caller/adapters yield exactly16 raw rank8 allowance')
            need(combine((1,base),(-416,{8:1}))==combine((1,oldbase),(-400,{8:1})),'no extra raw-field oracle credit')
            allbase=base;allpenalty=penalty
        else:need(base==oldbase,'same-cardinality adapter expenses cancel only through correct full substitution')
        converted.append({'variant':r['variant'],'finite_m_penalty':penalty})
    data=[]
    for r in partial:
        rm=moment(combine((1,allbase),(-1,r['Q'])));m=2
        while rm[0]-allpenalty[1]/(m-1)<=0:m+=1
        need(rm[1]-allpenalty[0]/(m-2)<0,'exact first positive fixed integer multiplicity')
        need(m==(5 if r['variant']=='gram'else 8),'Gram5/parity8')
        data.append({'variant':r['variant'],'limiting_room':rm,'first_positive_fixed_m':m})
    gram=next(r for r in partial if r['variant']=='gram');parity=next(r for r in partial if r['variant']=='parity');oldseed={1:120,2:112,3:88,5:200,8:216}
    gain=combine((1,allbase),(-1,gram['Q']),(-1,oldbase),(1,oldseed));need(gain=={1:F(8),8:F(8),3:-F(8),5:-F(8)},'exact complete old/new source gain')
    extra=combine((1,parity['Q']),(-1,gram['Q']));need(extra=={1:F(208),3:F(208),4:F(208),8:-F(208)},'exact C4 overhead')
    return {'exponent':'199/200','formula':'remaining_room(m)=limiting_room-finite_m_penalty/(m-1), fixed m>=2','complete_variants':converted,'partial_sources':data,'full_source_Gram_gain':moment(gain),'C4_extra':moment(extra),'unchanged_raw_oracle_allowance':moment(combine((1,oldbase),(-400,{8:1}))),'classification':'Actual partial-source allowance only; every remaining paired endpoint and all five foundations retained.'}

PINS={'PROOF.md':'54281240fda5fef8b12417c8e89520d83fc322bc2a663108a6de2b7ebcddf969','MANIFEST.json':'8ded0e2e0679c9205e5e81b46939bc214feae1d7e8587c9abedb3eb1a671181b','dependencies/native.json.gz':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','dependencies/caller.json':'3828d53e80ea97e8b866320f081af20b6b93bfebd58b95b56b85a7afe151af5e','dependencies/FULL-RESULT.json':'d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','output/orthogonal/WORD.json.gz':'210dcdbb6aad3a5634b056ce336701b44eae5e5182ce8ea4f374ad2729693566','output/allhosted/WORD.json.gz':'3dec380d820ed631636bdc77adb4a4c3e35abdb31d2b312f8f41edadff389d96','output/orthogonal/CALLER.json':'f8d9031e8ea020f04d71f6db654cb397acfcb70018087573139980ab817c8a4d','output/allhosted/CALLER.json':'31187aead2a665412177ee24110f9fc383f0bdb5b8fc6b728ad9b646ec4de608','output/allhosted-gram/WORD.json.gz':'721949af97ebb48344437477c99b7b1dcc8f1e52811a1ed80c8b683b3ef46f0d','output/allhosted-parity/WORD.json.gz':'f212f5fb73979e4c9842883e84435805d3ea87147e53afe322015019f6d21d22'}

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v)for v in x]
    return x

def main():
    global AUTHOR,REPO
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--repo',type=Path,default=REPO);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));p.add_argument('--skip-phases',action='store_true');a=p.parse_args();AUTHOR=a.author;REPO=a.repo
    for name,pin in PINS.items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen source pin '+name)
    old=load(AUTHOR/'dependencies/native.json.gz');oldcaller=load(AUTHOR/'dependencies/caller.json');full=load(AUTHOR/'dependencies/FULL-RESULT.json');complete=[];partial=[]
    for name in['orthogonal','allhosted']:
        w=load(AUTHOR/'output'/name/'WORD.json.gz');caller=load(AUTHOR/'output'/name/'CALLER.json');r=complete_review(old,w,caller,oldcaller,full)
        if not a.skip_phases:r['phase_certificates']=phase_review(w,old,AUTHOR/'output'/name/'PHASES.json')
        complete.append(r);print(json.dumps({'variant':name,'status':'PASS','public':r['physical']['public'],'ordinary':r['ordinary']['conservative_total']}),flush=True)
    native=load(AUTHOR/'output/allhosted/WORD.json.gz');seedpath=REPO/'research/moonshot-005-program/results/complex-omitted-line-gram/author/output/WORD.json.gz'
    need(hashlib.sha256(seedpath.read_bytes()).hexdigest()=='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc','exact retained partial chart source');seed=load(seedpath)
    for name in['allhosted-gram','allhosted-parity']:
        w=load(AUTHOR/'output'/name/'WORD.json.gz');c=partial_context(native,w);r=partial_audit(w,c);r['negative_controls']=partial_controls(w,c)
        if not a.skip_phases:r['phase_certificates']=phase_review(w,seed,AUTHOR/'output'/name/'PHASES.json')
        partial.append(r);print(json.dumps({'variant':name,'status':'PASS','rank':r['public_rank'],'residual':r['residual_rank'],'controls':len(r['negative_controls'])}),flush=True)
    result={'status':'PASS_INDEPENDENT_PAID_REPARTITION_AND_ALL_HOSTED_SOURCE_REVIEW','pins':PINS,'complete_conversions':complete,'partial_sources':partial,'invoice':compare_invoices(full,complete,partial),'scope':'Complete interface conversions inherit pinned old native correctness via exact body equality; new adapters, all1496 symbolic entries, chronology, fresh416 sources and signed accounting independently checked. All five foundations retained. No new kappa.'}
    a.output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n');print('PASS: two complete conditional conversions, two fresh paired partial sources, exact whole-caller invoices')

if __name__=='__main__':main()
