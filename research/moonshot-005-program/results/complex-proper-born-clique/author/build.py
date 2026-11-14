#!/usr/bin/env python3
"""Actual paired clique-sum compiler on native monotone cyclic flags.

Two proper-born moving owners; actual stationary source caches.
The programme's owned-erasure assumption is retained; scratch may be dirty.
"""
from __future__ import annotations
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

PINS={
 'native':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883',
 'seed':'6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc',
 'replay':'045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e',
 'codec':'4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297'}
CLIQUE=[48,50,71,80,87,98,103,105]

def need(ok,message):
    if not ok:raise ValueError(message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def read(path,name):
    raw=path.read_bytes();need(sha(raw)==PINS[name],name+' pin');return json.loads(gzip.decompress(raw))
def module(path,name):
    need(sha(path.read_bytes())==PINS[name],name+' pin')
    spec=importlib.util.spec_from_file_location('proper_born_clique_'+name,path)
    obj=importlib.util.module_from_spec(spec);sys.modules[spec.name]=obj;spec.loader.exec_module(obj);return obj
def clean(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {str(k):clean(v)for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [clean(v)for v in value]
    return value
def determinant(rows):
    a=[[F(v)for v in row]for row in rows];answer=F(1)
    for i in range(len(a)):
        k=next((k for k in range(i,len(a))if a[k][i]),None)
        if k is None:return F(0)
        if k!=i:a[k],a[i]=a[i],a[k];answer=-answer
        pivot=a[i][i];answer*=pivot
        for j in range(i+1,len(a)):
            c=a[j][i]/pivot;a[j]=[x-c*y for x,y in zip(a[j],a[i])]
    return answer

def main(args):
    need(2<=args.size<=8,'native clique size in proved range')
    n=read(args.native,'native');seed=read(args.seed,'seed')
    e=module(args.engine,'replay');codec=module(args.codec,'codec')
    ports=n['live'];roles={int(k):v for k,v in seed['source_role_map'].items()}
    host={ports[i]:(roles[b],roles[d])for i,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2'])}
    X={h:roles[h]for h in ports};Y={h:roles[h+112]for h in ports};U=sorted(set(ports)-set(host))
    normals={h:n['frames'][n['initial'][h]][0]for h in ports}
    roots={h:codec.root(normals[h])for h in ports};Z=seed['duplex']['omitted_frame']
    g={h:[sum(x*y for x,y in zip(roots[h],codec.root(z)))/18 for z in Z]for h in ports}
    G={(h,j):sum(g[h][i]*g[j][i]for i in range(8))for h in ports for j in ports}
    J=CLIQUE[:args.size];k=len(J);selected=set(J)
    need(selected<=set(host),'literal instance has hosted clique ports')
    need(all(G[h,j] and (normals[h]&normals[j]).bit_count()%2==0 for h in J for j in J if h!=j),'actual nonorthogonal native clique')
    need(len(codec.basis(normals[h]for h in J))==k,'clique source normals independent')
    oldgroups=seed['duplex']['groups'];old_nonpivots={h for z in oldgroups for i,h in enumerate(z['hosted'])if i not in z['pivots']}
    need(selected<=old_nonpivots,'all removed ports are authentic D/Y nonpivots')
    frames=copy.deepcopy(seed['frames']);where={frozenset(e.span(f)):i for i,f in enumerate(frames)}
    def chart(vectors):
        basis=codec.basis(vectors);space=frozenset(e.span(basis))
        if space not in where:where[space]=len(frames);frames.append(basis)
        return where[space]
    O=3;Hub=127;lines=seed['duplex']['lines'];P=chart(normals[h]for h in J)
    facets={h:where[frozenset(e.span(n['frames'][n['final'][h+112]]))]for h in ports}
    intervals={}
    for i,h in enumerate(J):
        intervals[h,0]=O
        for length in range(1,k):
            members=[J[(i+z)%k]for z in range(1,length+1)]
            C=chart(normals[j]for j in members);intervals[h,length]=C
            need(len(frames[C])==length and e.span(frames[C])<e.span(frames[facets[h]]),'actual proper receiver cyclic interval')
    source_stations={}
    for i,j in enumerate(J):
        for length in range(1,k):
            h=J[(i-length)%k];source_stations[j,length]=intervals[h,length]
        need(source_stations[j,1]==seed['initial'][X[j]]==seed['initial'][host[j][0]],'first station is actual source line')
    groups=[];codec_receipts=[]
    for old in oldgroups:
        z=copy.deepcopy(old);hs=[h for h in old['hosted']if h not in selected];ys=[h for h in old['ports']if h not in selected]
        original_pivot_ports=[old['hosted'][p]for p in old['pivots']]
        need(all(h in hs for h in original_pivot_ports),'every old pivot survives')
        pivots=[hs.index(h)for h in original_pivot_ports]
        MD=[[F(i==j)for j in range(len(hs))]for i in range(len(hs))]
        MY=[[F(i==j)for j in range(len(ys))]for i in range(len(ys))]
        for mode,pivot_port in zip(old['modes'],original_pivot_ports):
            MD[hs.index(pivot_port)]=[g[h][mode]for h in hs]
            MY[ys.index(pivot_port)]=[g[h][mode]*(1 if h in host else F(1,2))for h in ys]
        detD=determinant(MD);detY=determinant(MY)
        need(detD==determinant(old['M_D']) and detY==determinant(old['M_Y']),'nonpivot deletion preserves codec determinants')
        z.update({'hosted':hs,'ports':ys,'coupled':[h for h in ys if h not in host],
                  'D_roles':[host[h][1]for h in hs],'Y_roles':[Y[h]for h in ys],
                  'pivots':pivots,'M_D':MD,'M_Y':MY,'D_encoder':codec.encoder(MD),'Y_encoder':codec.encoder(MY),'markers':{}})
        groups.append(z);codec_receipts.append({'class_ports':old['ports'],'removed':sorted(selected&set(old['ports'])),'pivot_ports':original_pivot_ports,'D_determinant':detD,'Y_determinant':detY})
    out=[];markers={};events={};q=408;w=409
    caches={(h,j):410+i for i,(h,j)in enumerate((h,j)for h in J for j in J if h!=j)}
    def emit(op):out.append(op);return len(out)-1
    def add(d,s,c,C):return emit(['ADD',d,s,str(c),C])
    def move(d,A,B,owned=False):
        if A!=B:return emit(['MOVE',d,A,B,owned])
        return None
    def bop(bank,operations,C):
        for ty,i,j,c in operations:
            emit(['ADD',bank[i],bank[j],str(c),C]if ty=='ADD'else['SCALE',bank[i],str(c),C])

    for h in U:
        emit(['INIT',400,O]);add(400,Y[h],1,O);move(400,O,seed['initial'][X[h]],True)
        add(X[h],400,-1,seed['initial'][X[h]]);emit(['CLEAR',400,seed['initial'][X[h]]])
    markers['entry_end']=len(out)
    for i,L in enumerate(lines):emit(['INIT',400+i,L])
    for z in groups:
        bank=z['D_roles'];C=z['C'];enc=z['D_encoder'];bop(bank,enc,O)
        piv={p:mode for p,mode in zip(z['pivots'],z['modes'])}
        for i,d in enumerate(bank):
            if i in piv:
                mode=piv[i];move(d,O,lines[mode]);add(400+mode,d,1,lines[mode]);move(d,lines[mode],C)
            else:move(d,O,C)
        bop(bank,[codec.inverse_op(o)for o in reversed(enc)],C);z['markers']['D_restored_at_C3']=len(out)
        for h,d in zip(z['hosted'],bank):move(d,C,facets[h])
    markers['old_reverse_modes_acquired_without_selected_D']=len(out)

    emit(['INIT',q,O]);events['new_q_sources']=[]
    for h in J:events['new_q_sources'].append(add(q,host[h][1],1,O))
    events['local_B_adds']=[];events['source_cache_copies']=[]
    for length in range(1,k):
        for h in J:move(host[h][1],intervals[h,length-1],intervals[h,length])
        if length>1:
            for j in J:
                move(X[j],source_stations[j,length-1],source_stations[j,length])
                move(host[j][0],source_stations[j,length-1],source_stations[j,length])
        for i,h in enumerate(J):
            j=J[(i+length)%k];C=intervals[h,length]
            need(C==source_stations[j,length],'literal cyclic source/receiver cochart')
            emit(['INIT',caches[h,j],C]);events['source_cache_copies'].append(add(caches[h,j],X[j],1,C))
            events['local_B_adds'].append(add(host[j][0],host[h][1],1,C))
    for h in J:move(host[h][1],intervals[h,k-1],facets[h])
    markers['all_D_original_at_final_facets']=len(out)
    for j in J:
        move(X[j],source_stations[j,k-1],P);move(host[j][0],source_stations[j,k-1],P)
    events['q_move']=move(q,O,P,True);markers['q_at_birth_plane']=len(out)
    events['q_reads']=[add(host[j][0],q,-1,P)for j in J];emit(['CLEAR',q,P])
    emit(['INIT',w,P]);events['W_sources']=[add(w,X[j],1,P)for j in J]
    events['W_move']=move(w,P,O,True);markers['W_at_ground']=len(out)
    events['W_reads']=[add(Y[h],w,1,O)for h in J];emit(['CLEAR',w,O])
    events['local_Y_subtractions']=[]
    for length in range(1,k):
        for i,h in enumerate(J):
            j=J[(i+length)%k];C=intervals[h,length]
            move(Y[h],intervals[h,length-1],C)
            events['local_Y_subtractions'].append(add(Y[h],caches[h,j],-1,C));emit(['CLEAR',caches[h,j],C])
    for h in J:move(Y[h],intervals[h,k-1],facets[h])
    markers['selected_Y_exactly_completed']=len(out)
    for h in ports:move(X[h],P if h in selected else seed['initial'][X[h]],Hub)
    for h,(b,d)in host.items():move(b,P if h in selected else seed['initial'][b],Hub)
    markers['all_XB_at_Hub']=len(out)

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
    markers['old_forward_modes_at_lines']=len(out)
    for z in groups:
        bank=z['Y_roles'];C=z['C'];enc=[codec.dual_op(o)for o in z['Y_encoder']];bop(bank,enc,O)
        piv={p:mode for p,mode in zip(z['pivots'],z['modes'])}
        for i,y in enumerate(bank):
            if i in piv:
                mode=piv[i];move(y,O,lines[mode]);add(y,400+mode,1,lines[mode]);move(y,lines[mode],C)
            else:move(y,O,C)
        bop(bank,[codec.inverse_op(o)for o in reversed(enc)],C)
        for h,y in zip(z['ports'],bank):move(y,C,facets[h])
    for i,L in enumerate(lines):emit(['CLEAR',400+i,L])

    word={'schema':'moonshot-S012-proper-born-clique-v1','public':400,'owned_fields':10+k*(k-1),
          'initial':seed['initial'],'frames':frames,'source_role_map':seed['source_role_map'],'program':out,
          'source_pins':PINS,'clique_compiler':{'clique':J,'plane':P,'plane_frame':frames[P],
          'interval_charts':{str(h):[intervals[h,l]for l in range(k)]for h in J},
          'source_stations':{str(j):[source_stations[j,l]for l in range(1,k)]for j in J},
          'new_q_role':q,'new_W_role':w,'cache_roles':{str(h)+','+str(j):z for (h,j),z in caches.items()},
          'old_groups':clean(groups),'codec_determinants':clean(codec_receipts),'markers':markers,'events':events,
          'dirty_owned_retirement_assumption_retained':True}}

    captures={};boundaries=set(markers.values())|{z['markers']['D_restored_at_C3']for z in groups}
    retired=[]
    def capture(t,op,rows,locations):
        if t+1 in boundaries:captures[t+1]=(copy.deepcopy(rows),dict(locations))
        if t+1<len(out) and out[t+1][0]=='CLEAR':
            role=out[t+1][1];retired.append({'operation':t+1,'role':role,'chart':locations[role],
                                           'nonzero':bool(rows[role]),'input_support':len(rows[role])})
    rows,locations,bill=e.replay(word,out,capture)
    aa={h:{X[h]:F(1)}if h in host else{X[h]:F(1),Y[h]:F(-1)}for h in ports}
    forward_rows=[]
    for i in range(8):
        row={}
        for h in ports:row=e.add(row,aa[h],g[h][i])
        forward_rows.append(row)
    sum_row={}
    for h in J:sum_row=e.add(sum_row,aa[h])
    need(e.exact_rank(forward_rows)==8 and e.exact_rank(forward_rows+[sum_row])==9,'new proper-born row is genuinely independent of canonical Gram')
    want={j:{j:F(1)}for j in range(400)};wantloc={}
    L={(h,j):F(h==j)if h in selected else G[h,j]for h in ports for j in ports}
    for h in ports:
        want[X[h]]=aa[h];wantloc[X[h]]=Hub;wantloc[Y[h]]=facets[h]
        for j in ports:want[Y[h]]=e.add(want[Y[h]],aa[j],L[h,j]*(1 if h in host else F(1,2)))
    for h,(b,d)in host.items():
        wantloc[b]=Hub;wantloc[d]=facets[h]
        for j,(bj,dj)in host.items():want[b]=e.add(want[b],{dj:F(1)},-L[j,h])
    need(rows==want and locations==wantloc,'all400 original rows and exact native endpoint identifiers')
    need(e.exact_rank(rows.values())==400,'full independent original input rank')
    for z in groups:
        observed,_=captures[z['markers']['D_restored_at_C3']]
        need(all(observed[d]=={d:F(1)}for d in z['D_roles']),'each retained D restored at actual C3')
    observed,loc=captures[markers['all_D_original_at_final_facets']]
    need(all(observed[d]=={d:F(1)}and loc[d]==facets[h]for h,(b,d)in host.items()),'all96 original D restored and final before new forward delivery')
    observed,_=captures[markers['old_reverse_modes_acquired_without_selected_D']]
    for i in range(8):
        expect={d:g[h][i]for h,(b,d)in host.items()if h not in selected and g[h][i]}
        need(observed[400+i]==expect,'each old reverse mode has exactly the changed source, no selected-D double count')
    observed,loc=captures[markers['q_at_birth_plane']]
    need(observed[q]=={host[h][1]:F(1)for h in J}and loc[q]==P,'actual new paired adjoint at clique plane')
    observed,loc=captures[markers['W_at_ground']]
    expect={}
    for h in J:expect=e.add(expect,aa[h])
    need(observed[w]==expect and loc[w]==O,'actual proper-born new forward row at ground')
    observed,loc=captures[markers['selected_Y_exactly_completed']]
    need(all(observed[Y[h]]==e.add({Y[h]:F(1)},aa[h]) and loc[Y[h]]==facets[h]for h in J),'all selected forward rows exactly completed')
    observed,_=captures[markers['old_forward_modes_at_lines']]
    for i in range(8):
        expect={}
        for h in ports:expect=e.add(expect,aa[h],g[h][i])
        need(observed[400+i]==expect,'all eight original forward Gram modes preserved')
    need(all(rows[b].get(dj,F(0))+rows[Y[j]].get(X[h],F(0))==0
             for h,(b,d)in host.items()for j,(bj,dj)in host.items()),'all9216 hosted transpose entries')
    reverse=e.exact_rank([e.add(rows[b],{b:F(1),d:F(-1)},F(-1))for h,(b,d)in host.items()])
    need(reverse==96-k,'exact rank-reducing residual')
    det=determinant([[F(i==j)-sum(g[h][i]*g[h][j]for h in host)for j in range(8)]for i in range(8)])
    need(det==F(415068771,2),'exact retained hosted I-Gram determinant via rank-eight factor')
    raw=Counter();owned=Counter()
    for op in out:
        if op[0]=='MOVE':(owned if op[4]else raw)[abs(len(frames[op[3]])-len(frames[op[2]]))]+=1
    expected_raw=Counter({1:112,2:112,3:88,5:200,8:200})
    expected_raw.subtract({8:2*k,3:2*k,5:2*k});expected_raw[1]+=4*k*(k-1);expected_raw[9-k]+=4*k
    expected_raw=+expected_raw;expected_owned=Counter({1:8,8:16});expected_owned[k]+=2
    need(raw==expected_raw and owned==expected_owned,'complete signed raw and owned source profiles')
    need(sum(r*c for r,c in raw.items())==3200 and sum(r*c for r,c in owned.items())==136+2*k,'unchanged private rank mass and fully charged new bidirectional owners')
    scalars=[F(op[3]if op[0]=='ADD'else op[2])for op in out if op[0]in('ADD','SCALE')]
    need(all(x.denominator&(x.denominator-1)==0 for x in scalars),'all scalar coefficients exactly dyadic')
    new_retirements=[x for x in retired if x['role']>=408]
    need(len(new_retirements)==k*(k-1)+2 and all(x['nonzero']for x in new_retirements),'dirty auxiliary retirement explicitly retained')
    forward_current=sum(h!=j and bool(L[h,j])for h in ports for j in ports)
    need(forward_current==4992-48*k,'exact current-a forward debt')
    forward_original=sum(len(e.add(rows[Y[h]],{X[h]:F(1)if h in host else F(1,2),Y[h]:F(1)if h in host else F(1,2)},F(-1)))for h in ports)

    controls=[]
    choices={'wrong_new_forward_row':events['W_sources'][0],
             'wrong_new_reverse_row':events['new_q_sources'][0],
             'omit_local_forward_subtraction':events['local_Y_subtractions'][0],
             'omit_local_reverse_addition':events['local_B_adds'][0],
             'copy_original_D_instead_of_X':events['source_cache_copies'][0],
             'wrong_old_reverse_consumer':events['old_reverse_consumers'][0],
             'false_new_mode_destination':events['W_move']}
    for label,index in choices.items():
        bad=copy.deepcopy(word);op=bad['program'][index]
        if label=='copy_original_D_instead_of_X':op[2]=host[J[0]][1]
        elif label=='false_new_mode_destination':op[3]=P
        elif label.startswith('omit_'):op[3]='0'
        else:op[3]=str(-F(op[3]))
        try:mr,ml,_=e.replay(bad,bad['program']);rejected=mr!=rows or ml!=locations
        except ValueError:rejected=True
        need(rejected,'negative control '+label);controls.append(label)
    payload=(json.dumps(clean(word),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    receipt={'status':'PASS_ACTUAL_PAIRED_PROPER_BORN_CLIQUE_SOURCE','clique':J,'size':k,
             'word_sha256':sha(blob),'payload_sha256':sha(payload),'source_pins':PINS,
             'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),
             'all400_input_rank':400,'all96_D_original_at_final_facets':True,
             'old_reverse_modes_exactly_omit_selected_D':True,'old_forward_modes_preserved':True,
             'selected_Y_completed':J,'hosted_transpose_entries_checked':9216,
             'forward_global_history_rank':9,
             'reverse_residual_rank':reverse,'hosted_I_minus_Gram_determinant':det,
             'current_a_forward_offdiagonal_coefficients':forward_current,'original_coordinate_forward_debt':forward_original,
             'new_nonzero_owned_retirements':new_retirements,'owned_erasure_assumption_retained':True,
             'codec_determinants':codec_receipts,'all_scalars_dyadic':True,'negative_controls':controls,
             'scope':'Actual partial source for every field volume by its stated linear identities; inherited owned erasure and all uniform physical/foundational duties remain. No new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(clean(receipt),sort_keys=True,indent=2)+'\n')
    print(json.dumps(clean({key:receipt[key]for key in('status','clique','word_sha256','source_bill','raw_histogram','owned_histogram','reverse_residual_rank','current_a_forward_offdiagonal_coefficients')}),sort_keys=True,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--seed',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--codec',type=Path,required=True);p.add_argument('--size',type=int,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
