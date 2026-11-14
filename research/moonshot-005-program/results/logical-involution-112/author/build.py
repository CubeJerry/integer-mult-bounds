#!/usr/bin/env python3
"""Actual448-input paired shears for two full112 logical involutions.

No physical caller/query/productive-head admission is inferred from R^2=I.
"""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PINS={'native':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
 'seed':'6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc',
 'engine':'045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e',
 'codec':'4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297',
 'dynamic':'3845c44744ee0a05300bc237e9b9d10b45ca1272262f09f11e8a3ac2313a9e04',
 'geometry':'e8e48d62be188293677d5c2f7c9a1b104e944bff8ac97669fbaa9a70b41613c6'}
def need(ok,label):
    if not ok:raise ValueError(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(path,key):
    raw=path.read_bytes();need(sha(raw)==PINS[key],key+' pin');return json.loads(gzip.decompress(raw)if path.suffix=='.gz'else raw)
def module(path,key):
    need(sha(path.read_bytes())==PINS[key],key+' engine pin');sp=importlib.util.spec_from_file_location('logical112_'+key,path)
    obj=importlib.util.module_from_spec(sp);sys.modules[sp.name]=obj;sp.loader.exec_module(obj);return obj
def clean(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):clean(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v)for v in value]
    return value
def main(args):
    native=load(args.native,'native');seed=load(args.seed,'seed');fixture=load(args.geometry,'geometry')
    e=module(args.engine,'engine');c=module(args.codec,'codec');dyn=module(args.dynamic,'dynamic')
    v={int(h):x for h,x in fixture['normal_by_port'].items()};P=sorted(v);n=448
    Z=fixture['omitted_frame'];expected={z for z in range(512)if z.bit_count()in(3,7)}-set(Z)
    need(len(P)==112 and set(v.values())==expected,'full120 root lines minus exactly omitted eight-frame')
    need(all(v[h]==native['frames'][native['initial'][h]][0]for h in native['live']),'old104 geometry retained only as geometry')
    roots={h:c.root(v[h])for h in P};g={h:[sum(x*y for x,y in zip(roots[h],c.root(z)))/18 for z in Z]for h in P}
    need(all(sum(g[h][i]*g[h][j]for h in P)==14*int(i==j)for i in range(8)for j in range(8)),'global A^T A=14I')
    G={(h,j):sum(g[h][i]*g[j][i]for i in range(8))for h in P for j in P}
    frames=copy.deepcopy(seed['frames']);where={frozenset(e.span(f)):i for i,f in enumerate(frames)}
    def chart(vectors):
        f=c.basis(vectors);S=frozenset(e.span(f))
        if S not in where:where[S]=len(frames);frames.append(f)
        return where[S]
    O=3;Hub=127;lines={h:chart([v[h]])for h in P};facets={h:chart(z for z in range(512)if (z&v[h]).bit_count()%2==0)for h in P}
    X={h:i for i,h in enumerate(P)};Y={h:112+i for i,h in enumerate(P)};B={h:224+i for i,h in enumerate(P)};D={h:336+i for i,h in enumerate(P)}
    initial=[None]*n;final=[None]*n
    for h in P:
        initial[X[h]]=initial[B[h]]=lines[h];initial[Y[h]]=initial[D[h]]=O
        final[X[h]]=final[B[h]]=Hub;final[Y[h]]=final[D[h]]=facets[h]
    groups=[];halves=[];classof={};halfof={}
    for raw in fixture['classes']:
        modes=raw['modes'];ports=raw['ports'];C3=chart([Z[i]for i in modes]);gi=len(groups)
        need(len(ports)==8 and len(frames[C3])==3,'eight ports and actual class C3')
        need(len(c.basis([v[h]for h in ports]))==4,'actual binary class label rank4')
        need(all(sum(g[h][i]*g[h][j]for h in ports)==2*int(i==j)for i in modes for j in modes),'each class A_C^T A_C=2I4')
        A=[[g[h][i]for h in ports]for i in modes];_,piv=e.select([[z.numerator*pow(z.denominator,-1,e.PRIME)%e.PRIME for z in row]for row in A])
        need(len(piv)==4,'actual class four-mode rank')
        M=[[F(i==j)for j in range(8)]for i in range(8)]
        for i,p in zip(modes,piv):M[p]=[g[h][i]for h in ports]
        groups.append({'ports':ports,'modes':modes,'C3':C3,'pivots':piv,'encoder':c.encoder(M),'M':M,'markers':{}})
        for h in ports:classof[h]=gi
        for rawhalf in raw['halves']:
            T=rawhalf['ports'];S=sorted(set(ports)-set(T));C4=chart(frames[C3]+[v[j]for j in S]);hi=len(halves)
            need(len(c.basis([v[h]for h in T]))==len(c.basis([v[h]for h in S]))==3,'actual binary half label ranks3')
            need(len(T)==len(S)==len(frames[C4])==4,'full four-source/four-receiver C4')
            need(all(e.span(frames[C3])<e.span(frames[C4])<e.span(frames[facets[h]])for h in T),'real receiver proper C4 containment')
            need(all(G[h,j]==int(h==j)for h in T for j in T),'real orthogonal parity half')
            si=sorted(h for h in P if v[h]in e.span(frames[C4]));ri=sorted(h for h in P if e.span(frames[C4])<=e.span(frames[facets[h]]))
            need(si==S and ri==sorted(T),'exact full112 source and receiver incidence')
            halves.append({'ports':T,'sources':S,'C4':C4,'class':gi,'markers':{}})
            for h in T:halfof[h]=hi
    alpha=F(0)if args.variant=='R0'else F(1,7)
    RR={(h,j):alpha*G[h,j]-(G[h,j]if h!=j and classof[h]==classof[j]else 0)for h in P for j in P}
    Rrows={h:{j:RR[h,j]for j in P if RR[h,j]}for h in P}
    for h in P:
        square={}
        for j,a in Rrows[h].items():square=e.add(square,Rrows[j],a)
        need(square=={h:F(1)},'exact R^2=I on all112 coefficients')
    need(all(RR[h,j]==RR[j,h]for h in P for j in P),'exact symmetric logical involution')
    out=[];events={};marks={};cache={h:n+8+i for i,h in enumerate(P)}
    def emit(op):out.append(op);return len(out)-1
    def add(d,s,a,C0):return emit(['ADD',d,s,str(a),C0])
    def move(d,A,B0,owned=False):return emit(['MOVE',d,A,B0,owned])
    def bop(bank,ops,C0):
        for ty,i,j,a in ops:emit(['ADD',bank[i],bank[j],str(a),C0]if ty=='ADD'else['SCALE',bank[i],str(a),C0])
    if args.variant=='R0':
        events['local_forward']=[];events['local_reverse']=[]
        for z in halves:
            C4=z['C4'];T=z['ports'];S=z['sources']
            for h in T:move(Y[h],O,C4);move(D[h],O,C4)
            for j in S:move(X[j],lines[j],C4);move(B[j],lines[j],C4)
            for h in T:
                for j in S:
                    events['local_forward'].append(add(Y[h],X[j],-G[h,j],C4))
                    events['local_reverse'].append(add(B[j],D[h],G[h,j],C4))
            for h in T:move(Y[h],C4,facets[h]);move(D[h],C4,facets[h])
            for j in S:move(X[j],C4,Hub);move(B[j],C4,Hub)
    else:
        modes=seed['duplex']['lines'];events['reverse_reads']=[];events['forward_reads']=[]
        events['local_forward']=[];events['local_reverse']=[];events['cache_delivery']=[]
        for i,L in enumerate(modes):emit(['INIT',n+i,L])
        for z in groups:
            bank=[D[h]for h in z['ports']];C3=z['C3'];enc=z['encoder'];bop(bank,enc,O);pmap=dict(zip(z['pivots'],z['modes']))
            for k,d in enumerate(bank):
                if k in pmap:
                    i=pmap[k];move(d,O,modes[i]);add(n+i,d,1,modes[i]);move(d,modes[i],C3)
                else:move(d,O,C3)
            bop(bank,[c.inverse_op(op)for op in reversed(enc)],C3);z['markers']['D_original']=len(out)
            for h,d in zip(z['ports'],bank):move(d,C3,halves[halfof[h]]['C4'])
        marks['reverse_modes_acquired']=len(out)
        for z in halves:
            C4=z['C4'];T=z['ports'];S=z['sources']
            for j in S:move(X[j],lines[j],C4);move(B[j],lines[j],C4)
            for h in T:
                emit(['INIT',cache[h],C4])
                for j in S:events['local_forward'].append(add(cache[h],X[j],-G[h,j],C4))
            for j in S:
                for h in T:events['local_reverse'].append(add(B[j],D[h],G[h,j],C4))
            z['markers']['cache_ready']=len(out)
            for j in S:move(X[j],C4,Hub);move(B[j],C4,Hub)
        for h in P:move(D[h],halves[halfof[h]]['C4'],facets[h])
        for i,L in enumerate(modes):
            move(n+i,L,Hub,True)
            for h in P:
                if g[h][i]:events['reverse_reads'].append(add(B[h],n+i,-alpha*g[h][i],Hub))
            emit(['CLEAR',n+i,Hub])
        for i,L in enumerate(modes):
            emit(['INIT',n+i,Hub])
            for h in P:
                if g[h][i]:add(n+i,X[h],g[h][i],Hub)
            move(n+i,Hub,L,True)
        marks['forward_modes_acquired']=len(out)
        for z in groups:
            bank=[Y[h]for h in z['ports']];C3=z['C3'];enc=[c.dual_op(op)for op in z['encoder']]
            bop(bank,enc,O);pmap=dict(zip(z['pivots'],z['modes']))
            for k,y in enumerate(bank):
                if k in pmap:
                    i=pmap[k];move(y,O,modes[i]);events['forward_reads'].append(add(y,n+i,alpha,modes[i]));move(y,modes[i],C3)
                else:move(y,O,C3)
            bop(bank,[c.inverse_op(op)for op in reversed(enc)],C3);z['markers']['global_Y_decoded']=len(out)
            for h,y in zip(z['ports'],bank):
                C4=halves[halfof[h]]['C4'];move(y,C3,C4);events['cache_delivery'].append(add(y,cache[h],1,C4))
                emit(['CLEAR',cache[h],C4]);move(y,C4,facets[h])
        for i,L in enumerate(modes):emit(['CLEAR',n+i,L])
    word={'schema':'moonshot-S012-full112-logical-involution-source-v1','public':n,
       'owned_fields':0 if args.variant=='R0'else 120,'initial':initial,'final':final,'frames':frames,'program':out,
       'source_pins':PINS,'logical_involution':{'variant':args.variant,'alpha':str(alpha),'ports':P,'normals':v,
       'role_map':{'X':X,'Y':Y,'B':B,'D':D},'omitted_frame':Z,'groups':clean(groups),'halves':halves,
       'markers':marks,'events':events,'R_rows':clean(Rrows),'all448_inputs_independent':True,
       'new_domain_not_old_native_certificate':True,'physical_QUERY_admission':False,'productive_head_admission':False,
       'denominator7_service_required':args.variant!='R0'}}
    checked=Counter();retired=[]
    dsteps={z['markers']['D_original']:z for z in groups}if args.variant!='R0'else{}
    ysteps={z['markers']['global_Y_decoded']:z for z in groups}if args.variant!='R0'else{}
    csteps={z['markers']['cache_ready']:z for z in halves}if args.variant!='R0'else{}
    def capture(t,op,rows,loc):
        step=t+1
        if step in dsteps:
            for h in dsteps[step]['ports']:need(rows[D[h]]=={D[h]:F(1)},'every D exactly restored before C4');checked['original_D_at_C3']+=1
        if step in ysteps:
            for h in ysteps[step]['ports']:
                expect=e.add({Y[h]:F(1)},{X[j]:alpha*G[h,j]for j in P if G[h,j]})
                need(rows[Y[h]]==expect,'full global coefficient at actual decoded C3');checked['global_Y_at_C3']+=1
        if step in csteps:
            z=csteps[step]
            for h in z['ports']:need(rows[cache[h]]=={X[j]:-G[h,j]for j in z['sources']},'actual local X cache');checked['actual_C4_cache']+=1
        if args.variant!='R0'and step==marks['reverse_modes_acquired']:
            for i in range(8):need(rows[n+i]=={D[h]:g[h][i]for h in P if g[h][i]},'actual full112 D mode');checked['reverse_Gram_modes']+=1
        if args.variant!='R0'and step==marks['forward_modes_acquired']:
            for i in range(8):need(rows[n+i]=={X[h]:g[h][i]for h in P if g[h][i]},'actual full112 X mode');checked['forward_Gram_modes']+=1
        if step<len(out)and out[step][0]=='CLEAR':
            role=out[step][1];need(bool(rows[role]),'actual dirty retirement');retired.append({'operation':step,'role':role,'chart':loc[role],'support':len(rows[role])})
    rows,locations,bill=dyn.replay(word,out,e,capture);want={j:{j:F(1)}for j in range(n)}
    for h in P:
        for j in P:
            want[Y[h]]=e.add(want[Y[h]],{X[j]:F(1)},RR[h,j])
            want[B[h]]=e.add(want[B[h]],{D[j]:F(1)},-RR[j,h])
    need(rows==want and locations==dict(enumerate(final)),'all448 true inputs and logical paired-R endpoints')
    need(e.exact_rank(rows.values())==448,'full448 rational input rank')
    need(all(rows[Y[h]].get(X[j],F(0))+rows[B[j]].get(D[h],F(0))==0 for h in P for j in P),'all12544 paired entries')
    rank=e.exact_rank([e.add(Rrows[h],{h:F(1)},F(-1))for h in P]);need(rank==(56 if args.variant=='R0'else 48),'honest rank(R-I)')
    raw=Counter();owned=Counter()
    for op in out:
        if op[0]=='MOVE':(owned if op[4]else raw)[abs(len(frames[op[3]])-len(frames[op[2]]))]+=1
    need(sum(k*v for k,v in raw.items())==3584,'all448 original rank-eight raw paths counted')
    expected={3:224,4:448,5:224}if args.variant=='R0'else{1:336,2:112,3:336,4:224,5:224}
    need(raw==Counter(expected)and owned==Counter({}if args.variant=='R0'else{8:16}),'complete movement profiles')
    need(bill['peak']==(0 if args.variant=='R0'else 120)and bill['lifetimes']==len(retired)==(0 if args.variant=='R0'else 128),'actual owner peak and dirty retirements')
    def smooth(z):
        for prime in(2,3,5):
            while z%prime==0:z//=prime
        return z==1
    scalars=[];unsupported=[]
    for k,op in enumerate(out):
        if op[0]in('ADD','SCALE'):
            a=F(op[3]if op[0]=='ADD'else op[2]);scalars.append(a)
            ok=smooth(a.denominator)and(op[0]!='SCALE'or smooth(abs(a.numerator)))
            if not ok:unsupported.append({'operation':k,'coefficient':str(a)})
    need(bool(unsupported)==(args.variant!='R0'),'retained coefficient gate distinguishes new denominator7 obligation')
    if args.variant=='R0':need(set(bill['counts'])=={'MOVE','ADD'}and set(scalars)=={F(1,2),F(-1,2)},'R0 only dyadic direct contacts; no owned cache')
    controls=[];choices={'wrong_local_forward_sign':events['local_forward'][0],'omit_local_reverse_read':events['local_reverse'][0],
        'omit_real_raw_stop':next(k for k,op in enumerate(out)if op[0]=='MOVE'and op[1]in set(X.values())and not op[4])}
    if args.variant!='R0':choices.update({'wrong_global_forward_read':events['forward_reads'][0],
        'omit_global_reverse_read':events['reverse_reads'][0],'omit_local_cache_delivery':events['cache_delivery'][0]})
    for label,k in choices.items():
        bad=copy.deepcopy(word);op=bad['program'][k]
        if op[0]=='MOVE':op[3]=Hub
        else:op[3]='0'if label.startswith('omit_')else str(-F(op[3]))
        try:rr,ll,_=dyn.replay(bad,bad['program'],e);rejected=rr!=rows or ll!=locations
        except ValueError:rejected=True
        need(rejected,'actual semantic control '+label);controls.append(label)
    oldP=native['live'];cut={h:{j:RR[h,j]for j in oldP if RR[h,j]}for h in oldP};witness=None
    for h in oldP:
        square={}
        for j,a in cut[h].items():square=e.add(square,cut[j],a)
        diff=e.add(square,{h:F(1)},F(-1))
        if diff:witness={'row':h,'nonzero_R_square_minus_I':clean(diff)};break
    need(witness is not None,'old104 principal restriction fails actual involution identity')
    payload=(json.dumps(clean(word),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    result={'status':'PASS_EXACT_FULL112_LOGICAL_INVOLUTION_SOURCE','variant':args.variant,'word_sha256':sha(blob),'source_pins':PINS,
       'public':448,'full_input_rank':448,'ports':112,'class_census':{8:14},'half_census':{4:28},
       'R_symmetric':True,'R_squared_identity':True,'rank_R_minus_identity':rank,'all_X_and_D_original':True,
       'all12544_adjoint_entries':True,'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),
       'retained_scalar_primitive_gate_passes':not unsupported,'unsupported_scalar_count':len(unsupported),
       'unsupported_scalars':unsupported,'owner_retirements':retired,'actual_chronology_checks':dict(checked),
       'negative_controls':controls,'old104_restriction_involution_counterexample':witness,
       'physical_QUERY_or_productive_head_admitted':False,'new_complete_integer_bound':False,
       'scope':'Exact finite paired shear for a new112-port logical involution. R0 dyadic and owned-free; R1 needs denominator7 service. Neither has physical caller/query/productive-target admission; no new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in('status','variant','word_sha256','source_bill','raw_histogram','owned_histogram','rank_R_minus_identity','retained_scalar_primitive_gate_passes','unsupported_scalar_count')},sort_keys=True,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--codec',type=Path,required=True);p.add_argument('--dynamic',type=Path,required=True)
    p.add_argument('--geometry',type=Path,required=True);p.add_argument('--variant',choices=('R0','R1'),required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
