#!/usr/bin/env python3
"""Minimal C4 parity stations with an optional real coupled-entry import."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PINS={
 'native':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
 'seed':'6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc',
 'parity':'f72c890e06437c3b6a177c71019f56e60f30712e5c09c1e241c893c1f180e42d',
 'replay':'045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e',
 'codec':'4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297'}
IMPORT_PORT=17
def need(ok,message):
    if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path,name):
    raw=path.read_bytes();need(sha(raw)==PINS[name],name+' pin');return json.loads(gzip.decompress(raw))
def module(path,name):
    need(sha(path.read_bytes())==PINS[name],name+' pin')
    spec=importlib.util.spec_from_file_location('parity_C4_'+name,path);obj=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=obj;spec.loader.exec_module(obj);return obj
def clean(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):clean(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v)for v in value]
    return value

def main(args):
    n=read(args.native,'native');seed=read(args.seed,'seed');parity=read(args.parity,'parity')
    e=module(args.engine,'replay');codec=module(args.codec,'codec')
    ports=n['live'];roles={int(k):v for k,v in seed['source_role_map'].items()}
    host={ports[i]:(roles[b],roles[d])for i,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2'])}
    X={h:roles[h]for h in ports};Y={h:roles[h+112]for h in ports};U=sorted(set(ports)-set(host))
    imported=IMPORT_PORT if args.variant=='imported'else None
    need(imported is None or imported in U,'import has no fictitious hosted B/D counterpart')
    normals={h:n['frames'][n['initial'][h]][0]for h in ports};roots={h:codec.root(normals[h])for h in ports}
    Z=seed['duplex']['omitted_frame'];g={h:[sum(x*y for x,y in zip(roots[h],codec.root(z)))/18 for z in Z]for h in ports}
    G={(h,j):sum(g[h][i]*g[j][i]for i in range(8))for h in ports for j in ports}
    frames=copy.deepcopy(seed['frames']);where={frozenset(e.span(f)):i for i,f in enumerate(frames)}
    def chart(vectors):
        basis=codec.basis(vectors);space=frozenset(e.span(basis))
        if space not in where:where[space]=len(frames);frames.append(basis)
        return where[space]
    O=3;Hub=127;lines=seed['duplex']['lines']
    facets={h:where[frozenset(e.span(n['frames'][n['final'][h+112]]))]for h in ports}
    groups=copy.deepcopy(seed['duplex']['groups']);halves=[];half_of={};class_of={};geometry=[]
    for gi,z in enumerate(groups):
        z['markers']={};part={-1:[],1:[]}
        for h in z['ports']:
            sign=1
            for i in z['modes']:sign*=1 if g[h][i]>0 else -1
            part[sign].append(h);class_of[h]=gi
        ids=[]
        for sign,T in sorted(part.items()):
            T=sorted(T);S=sorted(part[-sign]);C=chart(frames[z['C']]+[normals[j]for j in S]);k=len(halves)
            need(len(T)in(3,4)and len(S)in(3,4),'credited real parity half sizes')
            need(all(G[h,j]==int(h==j)for h in T for j in T),'actual receiver half is real orthogonal')
            need(all(G[h,j]for h in T for j in S),'opposite half has all nonzero Gram contacts')
            need(len(frames[C])==4 and e.span(frames[z['C']])<e.span(frames[C]),'minimal C4 containing full-class C3 and source half')
            need(all(e.span(frames[C])<e.span(frames[facets[h]])for h in T),'C4 lies in every actual receiver final facet')
            si=sorted(j for j in ports if normals[j]in e.span(frames[C]))
            ri=sorted(h for h in ports if e.span(frames[C])<=e.span(frames[facets[h]]))
            need(si==S and ri==T,'exact native source and receiver incidence of minimal C4')
            halves.append({'index':k,'class':gi,'sign':sign,'ports':T,'opposite_ports':S,'C3':z['C'],'C4':C,
                           'hosted':[h for h in T if h in host],'markers':{}})
            for h in T:half_of[h]=k
            ids.append(k);geometry.append({'half':T,'opposite':S,'C4_frame':frames[C],'source_incidence':si,'receiver_incidence':ri})
        groups[gi]['halves']=ids
    K={(h,j):G[h,j]if class_of[h]!=class_of[j]else F(0)for h in ports for j in ports}
    out=[];markers={};events={};cache={h:408+i for i,h in enumerate(ports)}
    def emit(op):out.append(op);return len(out)-1
    def add(d,s,c,C):return emit(['ADD',d,s,str(c),C])
    def move(d,A,B,owned=False):
        if A!=B:return emit(['MOVE',d,A,B,owned])
        return None
    def bop(bank,operations,C):
        for ty,i,j,c in operations:
            emit(['ADD',bank[i],bank[j],str(c),C]if ty=='ADD'else['SCALE',bank[i],str(c),C])
    def mark(name):markers[name]=len(out);return len(out)
    # No altered Y baseline is used for any coupled X entry.
    order=[h for h in U if h!=imported]+([imported]if imported is not None else[])
    for h in order:
        L=seed['initial'][X[h]];emit(['INIT',400,O]);add(400,Y[h],1,O);move(400,O,L,True)
        add(X[h],400,-1,L)
        if h==imported:
            mark('all_coupled_a_created_before_import')
            events['entry_pickup']=add(400,X[h],1,L);mark('entry_owner_contains_original_x')
            events['import_move']=move(400,L,O,True)
            events['import_cleanup']=add(400,Y[h],-1,O);mark('imported_original_a_at_ground')
            events['import_receiver_reads']=[]
            for j in ports:
                if K[j,h]:events['import_receiver_reads'].append(add(Y[j],400,-K[j,h]*(1 if j in host else F(1,2)),O))
        emit(['CLEAR',400,O if h==imported else L])
    mark('entry_and_optional_import_end')
    for i,L in enumerate(lines):emit(['INIT',400+i,L])
    for z in groups:
        bank=z['D_roles'];C=z['C'];enc=[(a,b,c,F(d))for a,b,c,d in z['D_encoder']];bop(bank,enc,O)
        piv={p:i for p,i in zip(z['pivots'],z['modes'])}
        for j,d in enumerate(bank):
            if j in piv:
                i=piv[j];move(d,O,lines[i]);add(400+i,d,1,lines[i]);move(d,lines[i],C)
            else:move(d,O,C)
        bop(bank,[codec.inverse_op(op)for op in reversed(enc)],C);z['markers']['D_restored_at_C3']=len(out)
        for h,d in zip(z['hosted'],bank):move(d,C,halves[half_of[h]]['C4'])
    mark('all_original_D_at_C4_and_old_reverse_modes_acquired')
    events['local_reverse_reads']=[];events['correction_sources']=[]
    for z in halves:
        C=z['C4'];S=z['opposite_ports']
        for j in S:
            move(X[j],seed['initial'][X[j]],C)
            if j in host:move(host[j][0],seed['initial'][host[j][0]],C)
        for h in z['ports']:
            emit(['INIT',cache[h],C])
            for j in S:events['correction_sources'].append(add(cache[h],X[j],-G[h,j]*(1 if h in host else F(1,2)),C))
        for j in S:
            if j in host:
                for h in z['hosted']:events['local_reverse_reads'].append(add(host[j][0],host[h][1],G[h,j],C))
        z['markers']['actual_source_caches_ready']=len(out)
        for j in S:
            move(X[j],C,Hub)
            if j in host:move(host[j][0],C,Hub)
    for h,(b,d)in host.items():move(d,halves[half_of[h]]['C4'],facets[h])
    mark('all_XB_at_Hub_and_D_original_at_endpoints')
    events['old_reverse_consumers']=[]
    for i,L in enumerate(lines):
        move(400+i,L,Hub,True)
        for h,(b,d)in host.items():
            if g[h][i]:events['old_reverse_consumers'].append(add(b,400+i,-g[h][i],Hub))
        emit(['CLEAR',400+i,Hub])
    for i,L in enumerate(lines):
        emit(['INIT',400+i,Hub])
        for h in ports:
            if g[h][i]:add(400+i,X[h],g[h][i],Hub)
        move(400+i,Hub,L,True)
    mark('all_old_forward_modes_at_lines')
    events['old_forward_reads']=[];events['correction_reads']=[]
    for z in groups:
        bank=z['Y_roles'];C=z['C'];enc=[codec.dual_op((a,b,c,F(d)))for a,b,c,d in z['Y_encoder']];bop(bank,enc,O)
        piv={p:i for p,i in zip(z['pivots'],z['modes'])}
        for j,y in enumerate(bank):
            if j in piv:
                i=piv[j];move(y,O,lines[i]);events['old_forward_reads'].append(add(y,400+i,1,lines[i]));move(y,lines[i],C)
            else:move(y,O,C)
        bop(bank,[codec.inverse_op(op)for op in reversed(enc)],C);z['markers']['full_class_Y_decoded_at_C3']=len(out)
        for h,y in zip(z['ports'],bank):
            D=halves[half_of[h]]['C4'];move(y,C,D);events['correction_reads'].append(add(y,cache[h],1,D))
            emit(['CLEAR',cache[h],D]);move(y,D,facets[h])
    for i,L in enumerate(lines):emit(['CLEAR',400+i,L])
    word={'schema':'moonshot-S012-C4-parity-and-coupled-entry-import-v1','public':400,'owned_fields':112,
          'initial':seed['initial'],'frames':frames,'source_role_map':seed['source_role_map'],'program':out,
          'source_pins':PINS,'C4_compiler':{'variant':args.variant,'import_port':imported,'omitted_frame':Z,
          'lines':lines,'groups':groups,'halves':halves,'C4_geometry':geometry,'cache_roles':cache,
          'markers':markers,'events':events,'dirty_owned_retirement_assumption_retained':True,
          'credited_parity_map_sha256':PINS['parity']}}

    boundaries=set(markers.values())|{z['markers']['D_restored_at_C3']for z in groups}
    boundaries|={z['markers']['full_class_Y_decoded_at_C3']for z in groups}|{z['markers']['actual_source_caches_ready']for z in halves}
    observations={};retired=[]
    def capture(t,op,rows,locations):
        if t+1 in boundaries:observations[t+1]=(copy.deepcopy(rows),dict(locations))
        if t+1<len(out)and out[t+1][0]=='CLEAR':
            role=out[t+1][1];retired.append({'operation':t+1,'role':role,'chart':locations[role],
                                           'nonzero':bool(rows[role]),'input_support':len(rows[role])})
    rows,locations,bill=e.replay(word,out,capture)
    aa={h:{X[h]:F(1)}if h in host else{X[h]:F(1),Y[h]:F(-1)}for h in ports}
    L={(h,j):F(h==j)+K[h,j]*(0 if j==imported else 1)for h in ports for j in ports}
    want={j:{j:F(1)}for j in range(400)};wantloc={}
    for h in ports:
        want[X[h]]=aa[h];wantloc[X[h]]=Hub;wantloc[Y[h]]=facets[h]
        for j in ports:want[Y[h]]=e.add(want[Y[h]],aa[j],L[h,j]*(1 if h in host else F(1,2)))
    for h,(b,d)in host.items():
        wantloc[b]=Hub;wantloc[d]=facets[h]
        for j,(bj,dj)in host.items():want[b]=e.add(want[b],{dj:F(1)},-L[j,h])
    need(rows==want and locations==wantloc,'all400 original input coefficients and literal native endpoint charts')
    need(e.exact_rank(rows.values())==400,'all400 independent input directions retained')
    oldrows,oldloc,_=e.replay(parity,parity['program'])
    if imported is None:need(rows==oldrows and locations==oldloc,'same exact400-column public map as credited parity layer')
    else:
        shifted=copy.deepcopy(oldrows)
        for h in ports:shifted[Y[h]]=e.add(shifted[Y[h]],aa[imported],-K[h,imported]*(1 if h in host else F(1,2)))
        need(rows==shifted and locations==oldloc,'only the stated original coupled source column differs from credited parity map')
        obs,loc=observations[markers['all_coupled_a_created_before_import']]
        need(all(obs[X[h]]==aa[h]and obs[Y[h]]=={Y[h]:F(1)}for h in U),'all coupled entries precede every changed Y baseline')
        obs,loc=observations[markers['entry_owner_contains_original_x']]
        need(obs[400]=={X[imported]:F(1)}and loc[400]==seed['initial'][X[imported]],'actual entry owner contains original x after pickup')
        obs,loc=observations[markers['imported_original_a_at_ground']]
        need(obs[400]==aa[imported]and loc[400]==O,'genuine nonlocal a import at ground')
    for z in groups:
        obs,_=observations[z['markers']['D_restored_at_C3']]
        need(all(obs[d]=={d:F(1)}for d in z['D_roles']),'all actual original D restored at class C3')
        obs,_=observations[z['markers']['full_class_Y_decoded_at_C3']]
        for h in z['ports']:
            expected={Y[h]:F(1)}
            for j in ports:
                coefficient=(G[h,j]-(K[h,j]if j==imported else 0))*(1 if h in host else F(1,2))
                expected=e.add(expected,aa[j],coefficient)
            need(obs[Y[h]]==expected,'full-class Y decoder accepts actual changed ground baseline')
    obs,loc=observations[markers['all_original_D_at_C4_and_old_reverse_modes_acquired']]
    for h,(b,d)in host.items():need(obs[d]=={d:F(1)}and loc[d]==halves[half_of[h]]['C4'],'D waits at actual C4 with original value')
    for i,Lchart in enumerate(lines):
        expect={d:g[h][i]for h,(b,d)in host.items()if g[h][i]}
        need(obs[400+i]==expect and loc[400+i]==Lchart,'old reverse Gram acquisition unchanged')
    obs,loc=observations[markers['all_old_forward_modes_at_lines']]
    forward=[]
    for i,Lchart in enumerate(lines):
        expect={}
        for h in ports:expect=e.add(expect,aa[h],g[h][i])
        forward.append(expect);need(obs[400+i]==expect and loc[400+i]==Lchart,'old forward Gram source unchanged')
    for z in halves:
        obs,loc=observations[z['markers']['actual_source_caches_ready']]
        for h in z['ports']:
            expect={}
            for j in z['opposite_ports']:expect=e.add(expect,aa[j],-G[h,j]*(1 if h in host else F(1,2)))
            need(obs[cache[h]]==expect and loc[cache[h]]==z['C4'],'real local source correction cache at minimal C4')
    need(all(rows[b].get(dj,F(0))+rows[Y[j]].get(X[h],F(0))==0
             for h,(b,d)in host.items()for j,(bj,dj)in host.items()),'all9216 hosted paired entries; no fabricated coupled adjoint')
    reverse=e.exact_rank([e.add(rows[b],{b:F(1),d:F(-1)},F(-1))for h,(b,d)in host.items()]);need(reverse==56,'credited hosted residual rank unchanged')
    boundary_rank=e.exact_rank(forward+([aa[imported]]if imported is not None else[]))
    need(boundary_rank==8+int(imported is not None),'exact exported Gram plus ground-import information rank')
    raw=Counter();owned=Counter()
    for op in out:
        if op[0]=='MOVE':(owned if op[4]else raw)[abs(len(frames[op[3]])-len(frames[op[2]]))]+=1
    need(raw==Counter({1:312,2:112,3:288,4:200,5:200}),'entire real C4 raw profile')
    need(owned==Counter({1:8+int(imported is not None),8:16}),'all original owned calls and actual optional return')
    need(sum(r*c for r,c in raw.items())==3200 and sum(r*c for r,c in owned.items())==136+int(imported is not None),'complete rank masses')
    need(len(retired)==128 and all(x['nonzero']for x in retired),'all128 dirty owner retirements explicitly retained')
    scalars=[F(op[3]if op[0]=='ADD'else op[2])for op in out if op[0]in('ADD','SCALE')]
    need(all(x.denominator&(x.denominator-1)==0 for x in scalars),'all real scalar coefficients dyadic')
    cancelled=sum(bool(K[h,imported])for h in ports)if imported is not None else 0
    need(cancelled in(0,44),'source column support for optional import')
    current=sum(h!=j and bool(L[h,j])for h in ports for j in ports);need(current==4608-cancelled,'actual current-a debt')
    original=sum(len(e.add(rows[Y[h]],{X[h]:F(1)if h in host else F(1,2),Y[h]:F(1)if h in host else F(1,2)},F(-1)))for h in ports)
    controls=[];choices={'wrong_local_forward_correction':events['correction_sources'][0],
      'omit_local_reverse_correction':events['local_reverse_reads'][0],'wrong_old_forward_mode':events['old_forward_reads'][0],
      'wrong_old_reverse_mode':events['old_reverse_consumers'][0],'omit_local_cache_read':events['correction_reads'][0]}
    if imported is not None:choices.update({'omit_entry_pickup':events['entry_pickup'],'omit_original_Y_cleanup':events['import_cleanup'],
        'wrong_import_read':events['import_receiver_reads'][0],'omit_actual_import_move':events['import_move']})
    for label,index in choices.items():
        bad=copy.deepcopy(word);op=bad['program'][index]
        if label=='omit_actual_import_move':op[3]=op[2]
        elif label.startswith('omit_'):op[3]='0'
        else:op[3]=str(-F(op[3]))
        try:mr,ml,_=e.replay(bad,bad['program']);rejected=mr!=rows or ml!=locations
        except ValueError:rejected=True
        need(rejected,'negative control '+label);controls.append(label)
    payload=(json.dumps(clean(word),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    receipt={'status':'PASS_ACTUAL_C4_PARITY_SOURCE_WITH_OPTIONAL_COUPLED_IMPORT','variant':args.variant,'import_port':imported,
             'word_sha256':sha(blob),'payload_sha256':sha(payload),'source_pins':PINS,'source_bill':bill,
             'raw_histogram':dict(raw),'owned_histogram':dict(owned),'all400_input_rank':400,'all96_D_original':True,
             'all_original_X_restored':True,'all_old_Gram_modes_unchanged':True,'hosted_paired_entries_checked':9216,
             'credited_parity_map_reproduced':imported is None,'exported_Gram_and_ground_import_span_rank':boundary_rank,
             'reverse_residual_rank':reverse,'current_a_offdiagonal_debt':current,'original_coordinate_forward_debt':original,
             'additional_cross_class_column_entries_removed':cancelled,'C4_geometry':geometry,
             'all_scalars_dyadic':True,'owner_retirements':retired,'owned_erasure_assumption_retained':True,
             'negative_controls':controls,'scope':'New actual chronology and tariff for credited384-term parity layer, with optional genuine coupled source import. No new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(clean(receipt),sort_keys=True,indent=2)+'\n')
    print(json.dumps(clean({k:receipt[k]for k in('status','variant','word_sha256','source_bill','raw_histogram','owned_histogram',
                    'exported_Gram_and_ground_import_span_rank','reverse_residual_rank','current_a_offdiagonal_debt','original_coordinate_forward_debt')}),sort_keys=True,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True)
    p.add_argument('--parity',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--codec',type=Path,required=True)
    p.add_argument('--variant',choices=('base','imported'),required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())

