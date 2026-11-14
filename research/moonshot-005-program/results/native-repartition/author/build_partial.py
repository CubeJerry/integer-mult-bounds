#!/usr/bin/env python3
"""Fresh 416-independent-input all-hosted Gram and minimal-C4 sources.

This is a new source under the paid all-hosted native conversion. No old
coupled D=0 premise or old 400-column target is reused.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PINS={'native':'3dec380d820ed631636bdc77adb4a4c3e35abdb31d2b312f8f41edadff389d96',
      'seed':'6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc',
      'engine':'045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e',
      'codec':'4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297'}
def need(ok,label):
    if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path,key):
    raw=path.read_bytes();need(sha(raw)==PINS[key],key+' pin');return json.loads(gzip.decompress(raw))
def module(path,key):
    need(sha(path.read_bytes())==PINS[key],key+' pin')
    sp=importlib.util.spec_from_file_location('allhosted_'+key,path);obj=importlib.util.module_from_spec(sp)
    sys.modules[sp.name]=obj;sp.loader.exec_module(obj);return obj
def clean(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):clean(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v)for v in value]
    return value

def replay(word,ops,e,callback=None):
    """Explicit dimension-parametric extension of the pinned sparse replay.

    Only the former literal public census 400 is generalized to word.public.
    All original cochart, owner, strict nesting and nonzero SCALE rules stay.
    """
    n=word['public'];need(n==len(word['initial']),'literal initial public census')
    rows={j:{j:F(1)}for j in range(n)};loc=dict(enumerate(word['initial']))
    spaces=[e.span(f)for f in word['frames']];bill=Counter();counts=Counter();peak=life=0
    if callback:callback(-1,None,rows,loc)
    for t,op in enumerate(ops):
        ty,d=op[:2];counts[ty]+=1
        if ty=='INIT':
            need(d>=n and d not in loc,'INIT');rows[d]={};loc[d]=op[2];life+=1
        elif ty=='CLEAR':
            need(d>=n and loc.get(d)==op[2],'CLEAR');del rows[d];del loc[d]
        elif ty=='MOVE':
            a,b,owned=op[2:];need(loc.get(d)==a and owned==(d>=n),'MOVE source/ownership')
            need(spaces[a]<spaces[b]or owned and spaces[b]<spaces[a],'nested MOVE')
            loc[d]=b;bill[abs(len(word['frames'][a])-len(word['frames'][b]))]+=1
        elif ty in('ADD','COPY'):
            s,c,at=op[2:];need(d!=s and loc.get(d)==loc.get(s)==at,'cochart ADD/COPY')
            need(ty!='COPY'or not rows[d],'zero COPY');rows[d]=e.add(rows[d],rows[s],F(c))
        elif ty=='SCALE':
            c,at=op[2:];need(F(c)!=0 and loc.get(d)==at,'SCALE');rows[d]=e.scale(rows[d],F(c))
        else:raise ValueError(ty)
        peak=max(peak,len(loc)-n)
        if callback:callback(t,op,rows,loc)
    need(len(loc)==n,'every owned record retired')
    return rows,loc,{'instructions':len(ops),'counts':dict(counts),'moves':dict(bill),'peak':peak,'lifetimes':life}

def main(args):
    native=load(args.native,'native');seed=load(args.seed,'seed')
    e=module(args.engine,'engine');codec=module(args.codec,'codec');ports=native['live']
    oldhost={ports[i]:(b,d)for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    need(set(oldhost)==set(ports)and len(ports)==104,'all104 actual native ports hosted')
    original=sorted(ports+[h+112 for h in ports]+[r for pair in oldhost.values()for r in pair])
    need(len(original)==len(set(original))==416,'416 distinct arbitrary main inputs')
    roles={old:i for i,old in enumerate(original)};n=len(roles)
    X={h:roles[h]for h in ports};Y={h:roles[h+112]for h in ports}
    host={h:(roles[b],roles[d])for h,(b,d)in oldhost.items()}
    initial=[native['initial'][r]for r in original];final=[native['final'][r]for r in original]
    normals={h:native['frames'][native['initial'][h]][0]for h in ports};roots={h:codec.root(normals[h])for h in ports}
    Z=seed['duplex']['omitted_frame'];g={h:[sum(x*y for x,y in zip(roots[h],codec.root(z)))/18 for z in Z]for h in ports}
    G={(h,j):sum(g[h][i]*g[j][i]for i in range(8))for h in ports for j in ports}
    need(all(sum(g[h][i]*g[h][j]for h in ports)==13*int(i==j)for i in range(8)for j in range(8)),
         'exact full104 tight-frame identity A^T A=13I')
    frames=copy.deepcopy(seed['frames']);where={frozenset(e.span(f)):i for i,f in enumerate(frames)}
    def chart(vectors):
        basis=codec.basis(vectors);space=frozenset(e.span(basis))
        if space not in where:where[space]=len(frames);frames.append(basis)
        return where[space]
    O=3;Hub=127;lines=seed['duplex']['lines'];facets={h:final[Y[h]]for h in ports}
    patterns={}
    for h in ports:patterns.setdefault(tuple(i for i,x in enumerate(g[h])if x),[]).append(h)
    groups=[];classof={};halves=[];halfof={}
    for modes,members in sorted(patterns.items()):
        members=sorted(members);A=[[g[h][i]for h in members]for i in modes]
        _,piv=e.select([[int(x.numerator)*pow(x.denominator,-1,e.PRIME)%e.PRIME for x in row]for row in A])
        need(len(modes)==len(piv)==4,'four true class modes and four original-D pivots')
        M=[[F(i==j)for j in range(len(members))]for i in range(len(members))]
        for i,p in zip(modes,piv):M[p]=[g[h][i]for h in members]
        enc=codec.encoder(M);C=chart([Z[i]for i in modes]);gi=len(groups)
        need(len(frames[C])==3,'class C3')
        need(all(e.span(frames[C])<e.span(frames[facets[h]])for h in members),'actual receiver C3 containment')
        group={'modes':list(modes),'ports':members,'D_roles':[host[h][1]for h in members],
               'Y_roles':[Y[h]for h in members],'pivots':piv,'C3':C,'M':M,'encoder':enc,'markers':{}}
        for h in members:classof[h]=gi
        if args.variant=='parity':
            parts={-1:[],1:[]}
            for h in members:
                s=1
                for i in modes:s*=1 if g[h][i]>0 else -1
                parts[s].append(h)
            for sign,T in sorted(parts.items()):
                S=parts[-sign];C4=chart(frames[C]+[normals[j]for j in S]);hi=len(halves)
                need(len(frames[C4])==4,'true minimal C4')
                need(all(G[h,j]==int(h==j)for h in T for j in T),'orthogonal parity receiver half')
                need(all(e.span(frames[C4])<e.span(frames[facets[h]])for h in T),'actual receiver C4 containment')
                si=sorted(j for j in ports if normals[j]in e.span(frames[C4]))
                ri=sorted(h for h in ports if e.span(frames[C4])<=e.span(frames[facets[h]]))
                need(si==sorted(S)and ri==sorted(T),'full104 source and receiver incidence')
                halves.append({'class':gi,'ports':T,'sources':S,'C3':C,'C4':C4,'markers':{}})
                for h in T:halfof[h]=hi
        groups.append(group)
    need(len(groups)==14 and Counter(i for z in groups for i in z['modes'])==Counter({i:7 for i in range(8)}),
         'parity factor E has EE^T=7I, so E^TE-I56 is invertible')
    K={(h,j):G[h,j]if args.variant=='gram'or classof[h]!=classof[j]else F(h==j)for h in ports for j in ports}
    # For parity K=I+cross-class Gram, whereas gram retains G itself.
    out=[];markers={};events={};cache={h:n+8+i for i,h in enumerate(ports)}
    def emit(op):out.append(op);return len(out)-1
    def add(d,s,c,C):return emit(['ADD',d,s,str(c),C])
    def move(d,A,B,owned=False):
        if A!=B:return emit(['MOVE',d,A,B,owned])
    def bop(bank,ops,C):
        for ty,i,j,c in ops:emit(['ADD',bank[i],bank[j],str(c),C]if ty=='ADD'else['SCALE',bank[i],str(c),C])
    for i,L in enumerate(lines):emit(['INIT',n+i,L])
    for z in groups:
        bank=z['D_roles'];C=z['C3'];enc=z['encoder'];bop(bank,enc,O);pmap=dict(zip(z['pivots'],z['modes']))
        for j,d in enumerate(bank):
            if j in pmap:
                i=pmap[j];move(d,O,lines[i]);add(n+i,d,1,lines[i]);move(d,lines[i],C)
            else:move(d,O,C)
        bop(bank,[codec.inverse_op(op)for op in reversed(enc)],C);z['markers']['D_restored_at_C3']=len(out)
        for h,d in zip(z['ports'],bank):move(d,C,halves[halfof[h]]['C4']if args.variant=='parity'else facets[h])
    markers['all_D_restored_and_reverse_acquired']=len(out)
    events['local_reverse_reads']=[];events['local_forward_sources']=[]
    if args.variant=='parity':
        for z in halves:
            C=z['C4'];S=z['sources']
            for j in S:
                move(X[j],initial[X[j]],C);move(host[j][0],initial[host[j][0]],C)
            for h in z['ports']:
                emit(['INIT',cache[h],C])
                for j in S:events['local_forward_sources'].append(add(cache[h],X[j],-G[h,j],C))
            for j in S:
                for h in z['ports']:events['local_reverse_reads'].append(add(host[j][0],host[h][1],G[h,j],C))
            z['markers']['actual_caches']=len(out)
            for j in S:move(X[j],C,Hub);move(host[j][0],C,Hub)
        for h,(b,d)in host.items():move(d,halves[halfof[h]]['C4'],facets[h])
    else:
        for h in ports:move(X[h],initial[X[h]],Hub);move(host[h][0],initial[host[h][0]],Hub)
    markers['all_XB_at_Hub_and_D_at_endpoints']=len(out)
    events['reverse_consumers']=[]
    for i,L in enumerate(lines):
        move(n+i,L,Hub,True)
        for h,(b,d)in host.items():
            if g[h][i]:events['reverse_consumers'].append(add(b,n+i,-g[h][i],Hub))
        emit(['CLEAR',n+i,Hub])
    for i,L in enumerate(lines):
        emit(['INIT',n+i,Hub])
        for h in ports:
            if g[h][i]:add(n+i,X[h],g[h][i],Hub)
        move(n+i,Hub,L,True)
    markers['all_forward_modes_at_lines']=len(out);events['forward_reads']=[];events['correction_reads']=[]
    for z in groups:
        bank=z['Y_roles'];C=z['C3'];enc=[codec.dual_op(op)for op in z['encoder']];bop(bank,enc,O)
        pmap=dict(zip(z['pivots'],z['modes']))
        for j,y in enumerate(bank):
            if j in pmap:
                i=pmap[j];move(y,O,lines[i]);events['forward_reads'].append(add(y,n+i,1,lines[i]));move(y,lines[i],C)
            else:move(y,O,C)
        bop(bank,[codec.inverse_op(op)for op in reversed(enc)],C);z['markers']['full_Y_Gram_decoded']=len(out)
        for h,y in zip(z['ports'],bank):
            if args.variant=='parity':
                C4=halves[halfof[h]]['C4'];move(y,C,C4);events['correction_reads'].append(add(y,cache[h],1,C4))
                emit(['CLEAR',cache[h],C4]);move(y,C4,facets[h])
            else:move(y,C,facets[h])
    for i,L in enumerate(lines):emit(['CLEAR',n+i,L])
    word={'schema':'moonshot-S012-all104-hosted-Gram-C4-source-v1','public':n,'owned_fields':112 if args.variant=='parity'else 8,
          'initial':initial,'final':final,'frames':frames,'source_role_map':roles,'program':out,'source_pins':PINS,
          'allhosted':{'variant':args.variant,'omitted_frame':Z,'lines':lines,'groups':clean(groups),'halves':halves,
          'cache_roles':cache if args.variant=='parity'else{},'markers':markers,'events':events,
          'all104_D_original_and_independent':True,'owned_erasure_assumption_retained':True}}
    boundaries=set(markers.values())|{z['markers']['D_restored_at_C3']for z in groups}|{z['markers']['full_Y_Gram_decoded']for z in groups}
    boundaries|={z['markers']['actual_caches']for z in halves};observed={};retired=[]
    def capture(t,op,rows,loc):
        if t+1 in boundaries:observed[t+1]=(copy.deepcopy(rows),dict(loc))
        if t+1<len(out)and out[t+1][0]=='CLEAR':
            d=out[t+1][1];retired.append({'operation':t+1,'role':d,'chart':loc[d],'nonzero':bool(rows[d]),'support':len(rows[d])})
    rows,locations,bill=replay(word,out,e,capture)
    want={i:{i:F(1)}for i in range(n)}
    for h in ports:
        for j in ports:want[Y[h]]=e.add(want[Y[h]],{X[j]:F(1)},K[h,j])
        b,d=host[h]
        for j in ports:want[b]=e.add(want[b],{host[j][1]:F(1)},-K[j,h])
    need(rows==want and locations==dict(enumerate(final)),'all416 original columns and exact converted-native endpoint charts')
    need(e.exact_rank(rows.values())==416,'all416 independent input directions')
    for z in groups:
        rr,ll=observed[z['markers']['D_restored_at_C3']]
        need(all(rr[d]=={d:F(1)}and ll[d]==z['C3']for d in z['D_roles']),'every original D restored at its true C3')
        rr,ll=observed[z['markers']['full_Y_Gram_decoded']]
        for h in z['ports']:
            expected=e.add({Y[h]:F(1)},{X[j]:G[h,j]for j in ports if G[h,j]})
            need(rr[Y[h]]==expected and ll[Y[h]]==z['C3'],'whole-class Gram decoder before actual C4 correction')
    rr,ll=observed[markers['all_D_restored_and_reverse_acquired']]
    for i,L in enumerate(lines):need(rr[n+i]=={host[h][1]:g[h][i]for h in ports if g[h][i]}and ll[n+i]==L,'all104-independent-D reverse mode')
    rr,ll=observed[markers['all_forward_modes_at_lines']]
    for i,L in enumerate(lines):need(rr[n+i]=={X[h]:g[h][i]for h in ports if g[h][i]}and ll[n+i]==L,'all104 original-X forward mode')
    for z in halves:
        rr,ll=observed[z['markers']['actual_caches']]
        for h in z['ports']:need(rr[cache[h]]=={X[j]:-G[h,j]for j in z['sources']}and ll[cache[h]]==z['C4'],'actual C4 source cache')
    need(all(rows[host[h][0]].get(host[j][1],F(0))+rows[Y[j]].get(X[h],F(0))==0 for h in ports for j in ports),'all10816 adjoint entries')
    residual=e.exact_rank([e.add(rows[b],{b:F(1),d:F(-1)},F(-1))for b,d in host.values()])
    need(residual==(56 if args.variant=='parity'else 104),'exact new all-hosted endpoint residual rank')
    raw=Counter();owned=Counter()
    for op in out:
        if op[0]=='MOVE':(owned if op[4]else raw)[abs(len(frames[op[3]])-len(frames[op[2]]))]+=1
    expectedraw={1:320,2:112,3:304,4:208,5:208}if args.variant=='parity'else{1:112,2:112,3:96,5:208,8:208}
    need(raw==Counter(expectedraw)and owned==Counter({8:16}),'complete raw and owned profiles')
    need(sum(r*c for r,c in raw.items())==3328,'416 original fields each have complete rank-eight rise')
    need(len(retired)==(120 if args.variant=='parity'else 16)and all(z['nonzero']for z in retired),'every dirty retirement stated')
    scalars=[F(op[3]if op[0]=='ADD'else op[2])for op in out if op[0]in('ADD','SCALE')]
    need(all(z.denominator&(z.denominator-1)==0 for z in scalars),'all new coefficients exactly dyadic')
    controls=[];chosen={'wrong_forward_read':events['forward_reads'][0],'wrong_reverse_consumer':events['reverse_consumers'][0],
        'omit_D_decoder':groups[0]['markers']['D_restored_at_C3']-1,'omit_Y_decoder':groups[0]['markers']['full_Y_Gram_decoded']-1}
    if args.variant=='parity':chosen.update({'wrong_C4_forward_source':events['local_forward_sources'][0],
        'omit_C4_reverse_read':events['local_reverse_reads'][0],'omit_C4_cache_delivery':events['correction_reads'][0]})
    for label,index in chosen.items():
        bad=copy.deepcopy(word);op=bad['program'][index]
        if op[0]=='ADD':op[3]='0'if label.startswith('omit_')else str(-F(op[3]))
        elif op[0]=='SCALE':op[2]='1'
        else:raise ValueError('negative control opcode')
        try:rr,ll,_=replay(bad,bad['program'],e);rejected=rr!=rows or ll!=locations
        except ValueError:rejected=True
        need(rejected,'negative control '+label);controls.append(label)
    # A promoted D is a true independent input; omitting its acquisition must fail.
    promoted=set(native['repartition']['old_coupled_to_new_hosted']);d0=host[min(promoted)][1]
    need(any(rows[b].get(d0)for b,d in host.values()),'promoted D participates in genuine reverse public outputs')
    def suppress_new_input(t,op,rr,ll):
        if t==-1:rr[d0]={}
    rr,ll,_=replay(word,out,e,suppress_new_input)
    need(rr!=want and e.exact_rank(rr.values())==415,'old coupled zero-input premise fails for the promoted original D')
    controls.append('promoted_original_D_cannot_be_specialized_to_zero')
    payload=(json.dumps(clean(word),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    receipt={'status':'PASS_FRESH_ALL104_HOSTED_SOURCE','variant':args.variant,'word_sha256':sha(blob),'source_pins':PINS,
        'public':416,'all_input_rank':416,'all_original_D_restored':True,'all_original_X_restored':True,
        'hosted_adjoint_entries_checked':10816,'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),
        'exported_mode_history_rank':8,'reverse_residual_rank':residual,'Gram_residual_determinant':12**8,
        'forward_offdiagonal_debt':sum(h!=j and bool(K[h,j])for h in ports for j in ports),
        'all_scalars_dyadic':True,'owner_retirements':retired,'negative_controls':controls,
        'scope':'Actual fresh416-input source under converted all-hosted interface. Incomplete endpoint; no supplier and no new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(clean(receipt),sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:receipt[k]for k in('status','variant','word_sha256','source_bill','raw_histogram','owned_histogram','reverse_residual_rank','forward_offdiagonal_debt')},sort_keys=True,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--codec',type=Path,required=True)
    p.add_argument('--variant',choices=('gram','parity'),required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
