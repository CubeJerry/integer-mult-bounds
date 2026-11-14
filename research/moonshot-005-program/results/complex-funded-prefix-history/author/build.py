#!/usr/bin/env python3
"""Actual paired prefix histories on one funded reverse/forward Gram pair.

@CubeJerry; substantial OpenAI assistance; Apache-2.0. No new complete kappa.
"""
from __future__ import annotations
import argparse, copy, gzip, hashlib, importlib.util, json, sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SEED='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc'
REPLAY='045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e'
CODEC='4cb31f8f1c5b2e069afbbb3a3f028c787b677684a558bc12c2f31f51a4871297'

def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(blob): return hashlib.sha256(blob).hexdigest()
def read(path,pin):
    blob=path.read_bytes();need(sha(blob)==pin,'exact source pin '+str(path))
    return json.loads(gzip.decompress(blob))
def module(path,pin,name):
    need(sha(path.read_bytes())==pin,'retained utility pin '+str(path))
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);sys.modules[name]=result
    spec.loader.exec_module(result);return result
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x
def determinant(matrix):
    A=[[F(x) for x in row] for row in matrix];value=F(1);n=len(A)
    for i in range(n):
        k=next((k for k in range(i,n) if A[k][i]),None)
        if k is None:return F(0)
        if k!=i:A[k],A[i]=A[i],A[k];value=-value
        pivot=A[i][i];value*=pivot
        for j in range(i+1,n):
            c=A[j][i]/pivot;A[j]=[x-c*y for x,y in zip(A[j],A[i])]
    return value

def main(args):
    native=read(args.native,NATIVE);seed=read(args.seed,SEED)
    e=module(args.engine,REPLAY,'funded_prefix_replay')
    codec=module(args.codec,CODEC,'funded_prefix_retained_codec')
    flag=json.loads(args.flag.read_text());need(flag['native_sha256']==NATIVE and flag['seed_sha256']==SEED,'candidate source pins')
    roles={int(k):v for k,v in seed['source_role_map'].items()};ports=native['live']
    host={ports[i]:(roles[b],roles[d]) for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    X={h:roles[h] for h in ports};Y={h:roles[h+112] for h in ports};U=sorted(set(ports)-set(host))
    normals={h:native['frames'][native['initial'][h]][0] for h in ports}
    root={h:codec.root(normals[h]) for h in ports};Z=seed['duplex']['omitted_frame']
    g={h:[sum(x*y for x,y in zip(root[h],codec.root(z)))/18 for z in Z] for h in ports}
    gram={(h,j):sum(g[h][i]*g[j][i] for i in range(8)) for h in ports for j in ports}
    mode=flag['mode'];J=flag['receiver_class'];donors=flag['donors'];need(set(J)<=set(host),'this literal first instance uses genuine hosted receivers')
    sd={int(k):v for k,v in flag['source_dimensions'].items()};rd={int(k):v for k,v in flag['receiver_dimensions'].items()}
    active=flag['active_dimensions'];frames=copy.deepcopy(seed['frames']);spaces=[frozenset(e.span(f)) for f in frames]
    def chart(frame):
        space=frozenset(e.span(frame))
        if space not in spaces:spaces.append(space);frames.append(frame)
        return spaces.index(space)
    stations={d:chart(flag['chain'][d-3]) for d in active};Hub=127;O=3;lines=seed['duplex']['lines'];L=lines[mode]
    facets={h:spaces.index(frozenset(e.span(native['frames'][native['final'][h+112]]))) for h in ports}
    dims=[1,*active,9];route=[L,*[stations[d] for d in active],Hub]
    need(all(spaces[a]<spaces[b] for a,b in zip(route,route[1:])),'actual strict nested funded trajectory')
    need(all(len(frames[stations[d]])==d for d in active),'exact station dimensions')
    pairs=[(h,j) for h in J for j in donors if sd[j]<=rd[h]]
    need(pairs==[tuple(p) for p in flag['pairs']] and len(pairs)==52,'exact 52-pair finite candidate')
    need(all(j not in J and g[j][mode] and spaces[seed['initial'][X[j]]]<spaces[stations[sd[j]]] for j in donors),'actual source acquisition stations')
    need(all(spaces[stations[rd[h]]]<=spaces[facets[h]] for h in J),'actual receiver stations before facets')
    need(all(gram[h,j]==2*g[h][mode]*g[j][mode] for h,j in pairs),'exact targeted cross-class coefficient')
    groups=copy.deepcopy(seed['duplex']['groups']);changed_group=next(z for z in groups if z['ports']==J)
    need(mode in changed_group['modes'],'mode belongs to actual class')
    need(all((spaces[z['C']]<=spaces[facets[h]])==(h in z['ports']) for z in groups for h in ports),'all 1456 class-C3/facet incidences: no cross-class retained decoder chain')
    for z in groups:
        z['D_encoder']=[(ty,i,j,F(c)) for ty,i,j,c in z['D_encoder']]
        z['Y_encoder']=[(ty,i,j,F(c)) for ty,i,j,c in z['Y_encoder']]
        z['D_modes']=z['modes'][:];z['D_pivots']=z['pivots'][:];z['markers']={}
    # The selected class contributes no mode-i row at the original omitted line.
    z=changed_group;hs=z['hosted'];kept=[i for i in z['modes'] if i!=mode]
    A=[[g[h][i] for h in hs] for i in kept]
    _,piv=e.select([[int(v.numerator)*pow(v.denominator,-1,e.PRIME)%e.PRIME for v in row] for row in A])
    need(len(piv)==3,'actual reduced D mode rank')
    MD=[[F(i==j) for j in range(len(hs))] for i in range(len(hs))]
    for i,p in zip(kept,piv):MD[p]=[g[h][i] for h in hs]
    z['D_encoder']=codec.encoder(MD);z['D_modes']=kept;z['D_pivots']=piv;z['M_D']=MD
    MY=[[F(x) for x in row] for row in z['M_Y']];yp=z['pivots'][z['modes'].index(mode)]
    MY[yp]=[2*v for v in MY[yp]];z['M_Y']=MY;z['Y_encoder']=codec.encoder(MY)
    need(determinant(MD)==F(-1,2) and determinant(MY)==-2,'actual dyadic encoder determinant certificates')
    source_dims=sorted(set(sd.values()));receiver_dims=sorted(set(rd.values()))
    source_cache={d:408+k for k,d in enumerate(source_dims)}
    output_cache={d:408+len(source_dims)+k for k,d in enumerate(receiver_dims)}
    p={j:2*g[j][mode] for j in donors};q={h:-g[h][mode] for h in J}
    out=[];marks={};events={};up_phases=[];down_phases=[]
    def emit(o):out.append(o)
    def add(dst,src,c,C):emit(['ADD',dst,src,str(c),C])
    def move(role,A,B,owned):
        if A!=B:emit(['MOVE',role,A,B,owned])
    def bop(bank,ops,C):
        for ty,i,j,c in ops:emit(['ADD',bank[i],bank[j],str(c),C] if ty=='ADD' else ['SCALE',bank[i],str(c),C])
    for h in U:
        emit(['INIT',400,O]);add(400,Y[h],1,O);move(400,O,seed['initial'][X[h]],True)
        add(X[h],400,-1,seed['initial'][X[h]]);emit(['CLEAR',400,seed['initial'][X[h]]])
    marks['entry_end']=len(out)
    for i,line in enumerate(lines):emit(['INIT',400+i,line])
    for z in groups:
        bank=z['D_roles'];C=z['C'];enc=z['D_encoder'];bop(bank,enc,O)
        pmap={pivot:i for pivot,i in zip(z['D_pivots'],z['D_modes'])}
        for j,d in enumerate(bank):
            if j in pmap:
                i=pmap[j];move(d,O,lines[i],False);events.setdefault('line_acquisitions',[]).append(len(out));add(400+i,d,1,lines[i]);move(d,lines[i],C,False)
            else:move(d,O,C,False)
        bop(bank,[codec.inverse_op(o) for o in reversed(enc)],C)
        z['markers']['D_restored']=len(out)
        for h,d in zip(z['hosted'],bank):move(d,C,stations[rd[h]] if h in J else facets[h],False)
    marks['D_all_restored']=len(out)
    for d,cache in source_cache.items():emit(['INIT',cache,stations[d]])
    for h in ports:
        if h in sd:
            C=stations[sd[h]];move(X[h],seed['initial'][X[h]],C,False);add(source_cache[sd[h]],X[h],p[h],C);move(X[h],C,Hub,False)
        else:move(X[h],seed['initial'][X[h]],Hub,False)
    for h,(b,d) in host.items():move(b,seed['initial'][b],stations[sd[h]] if h in sd else Hub,False)
    marks['source_cached']=len(out)
    R=400+mode;current=L
    for dim in active:
        C=stations[dim];move(R,current,C,True);phase={'dimension':dim,'arrival':len(out)}
        for j in donors:
            if sd[j]==dim:
                events.setdefault('local_B_reads',[]).append(len(out));add(host[j][0],R,-p[j],C);move(host[j][0],C,Hub,False)
        phase['B_consumed']=len(out)
        for h in J:
            if rd[h]==dim:
                events.setdefault('reverse_restorations',[]).append(len(out));add(R,host[h][1],-q[h],C);move(host[h][1],C,facets[h],False)
        phase['D_contribution_restored']=len(out);up_phases.append(phase);current=C
    move(R,current,Hub,True);marks['reverse_mode_restored']=len(out)
    for j in donors:events.setdefault('Hub_B_compensation',[]).append(len(out));add(host[j][0],R,p[j],Hub)
    marks['prefix_reverse_complete']=len(out)
    for i,line in enumerate(lines):
        if i!=mode:move(400+i,line,Hub,True)
        for h,(b,d) in host.items():
            if g[h][i]:add(b,400+i,-g[h][i],Hub)
        emit(['CLEAR',400+i,Hub])
    marks['all_reverse_consumed']=len(out)
    for i,line in enumerate(lines):
        Fowner=400+i;emit(['INIT',Fowner,Hub])
        for h in ports:
            if g[h][i]:add(Fowner,X[h],g[h][i],Hub)
        if i!=mode:move(Fowner,Hub,line,True);continue
        for j in donors:events.setdefault('forward_augmentation',[]).append(len(out));add(Fowner,X[j],p[j],Hub)
        current=Hub
        for dim in reversed(active):
            C=stations[dim];move(Fowner,current,C,True);phase={'dimension':dim,'arrival':len(out)}
            if dim in output_cache:
                emit(['INIT',output_cache[dim],C]);phase['output_capture']=len(out);add(output_cache[dim],Fowner,1,C)
            phase['receiver_prefix_recorded']=len(out)
            if dim in source_cache:
                phase['source_shed']=len(out);add(Fowner,source_cache[dim],-1,C);emit(['CLEAR',source_cache[dim],C])
            phase['after_source_shed']=len(out);down_phases.append(phase);current=C
        move(Fowner,current,line,True);marks['forward_mode_restored']=len(out)
    marks['all_forward_modes_ready']=len(out)
    reads_left=Counter(rd.values())
    for z in groups:
        bank=z['Y_roles'];C=z['C'];enc=[codec.dual_op(o) for o in z['Y_encoder']];bop(bank,enc,O)
        pmap={pivot:i for pivot,i in zip(z['pivots'],z['modes'])}
        for j,y in enumerate(bank):
            if j in pmap:
                i=pmap[j];move(y,O,lines[i],False);add(y,400+i,1,lines[i]);move(y,lines[i],C,False)
            else:move(y,O,C,False)
        bop(bank,[codec.inverse_op(o) for o in reversed(enc)],C);z['markers']['Y_decoded']=len(out)
        for h,y in zip(z['ports'],bank):
            if h in J:
                dim=rd[h];where=stations[dim];move(y,C,where,False);events.setdefault('output_reads',[]).append(len(out));add(y,output_cache[dim],q[h],where)
                reads_left[dim]-=1
                if not reads_left[dim]:emit(['CLEAR',output_cache[dim],where])
                move(y,where,facets[h],False)
            else:move(y,C,facets[h],False)
    for i,line in enumerate(lines):emit(['CLEAR',400+i,line])
    w={k:copy.deepcopy(v) for k,v in seed.items() if k not in ('duplex','program')}
    w.update(schema='moonshot-S012-funded-paired-prefix-v1',frames=frames,owned_fields=17,program=out,
             funded_prefix={'mode':mode,'receiver_class':J,'donors':donors,'source_dimensions':sd,'receiver_dimensions':rd,'stations':stations,'route':route,'source_caches':source_cache,'output_caches':output_cache,'p':p,'q':q,'groups':groups,'markers':marks,'up_phases':up_phases,'down_phases':down_phases,'events':events,'candidate_flag_sha256':sha(args.flag.read_bytes()),'seed_sha256':SEED,'codec_sha256':CODEC})
    base,base_locs,_=e.replay(seed,seed['program']);a_rows={h:{X[h]:F(1)} if h in host else {X[h]:F(1),Y[h]:F(-1)} for h in ports}
    gd={host[h][1]:g[h][mode] for h in host if g[h][mode]};ga={}
    for h in ports:ga=e.add(ga,a_rows[h],g[h][mode])
    upward_boundary=[];downward_boundary=[];captures=[]
    def check(k,o,rows,loc):
        t=k+1
        for z in groups:
            if t==z['markers']['D_restored']:need(all(rows[d]=={d:F(1)} for d in z['D_roles']),'all original D restored at actual C3')
        if t==marks['D_all_restored']:
            expected=gd.copy()
            for h in J:expected=e.add(expected,{host[h][1]:F(1)},q[h])
            need(rows[R]==expected and loc[R]==L,'actual modified line preload, no free replacement')
        if t==marks['source_cached']:
            for dim,cache in source_cache.items():
                wanted={}
                for j in donors:
                    if sd[j]==dim:wanted=e.add(wanted,a_rows[j],p[j])
                need(rows[cache]==wanted and loc[cache]==stations[dim],'actual original-source stationary acquisition')
        for phase in up_phases:
            if t==phase['arrival']:
                dim=phase['dimension'];wanted=gd.copy()
                for h in J:
                    if rd[h]>=dim:wanted=e.add(wanted,{host[h][1]:F(1)},q[h])
                need(rows[R]==wanted and loc[R]==stations[dim],'actual reverse suffix invariant');captures.append(('reverse',dim))
        if t==marks['reverse_mode_restored']:need(rows[R]==gd and loc[R]==Hub,'old reverse mode duty exactly restored')
        if t==marks['prefix_reverse_complete']:
            for j in donors:
                wanted={host[j][0]:F(1)}
                for h in J:
                    if sd[j]<=rd[h]:wanted=e.add(wanted,{host[h][1]:F(1)},-p[j]*q[h])
                need(rows[host[j][0]]==wanted,'true accumulated paired B correction before old Gram consumer')
        for phase in down_phases:
            if t==phase['arrival']:
                dim=phase['dimension'];wanted=ga.copy()
                for j in donors:
                    if sd[j]<=dim:wanted=e.add(wanted,a_rows[j],p[j])
                need(rows[R]==wanted and loc[R]==stations[dim],'actual forward prefix invariant');captures.append(('forward',dim))
            if t==phase['receiver_prefix_recorded'] and phase['dimension'] in output_cache:
                need(rows[output_cache[phase['dimension']]]==rows[R],'actual prefix record before same-station source removal')
        if t==marks['forward_mode_restored']:need(rows[R]==ga and loc[R]==L,'old forward mode duty exactly restored')
        if o and o[0]=='MOVE' and o[1]==R and o[4]:
            if marks['source_cached']<=k<marks['all_reverse_consumed']:
                upward_boundary.append(copy.deepcopy(rows[R]))
            elif k>=marks['all_reverse_consumed']:
                downward_boundary.append(copy.deepcopy(rows[R]))
    rows,loc,bill=e.replay(w,out,check);wanted=copy.deepcopy(base)
    for h,j in pairs:
        wanted[Y[h]]=e.add(wanted[Y[h]],a_rows[j],-gram[h,j]);wanted[host[j][0]]=e.add(wanted[host[j][0]],{host[h][1]:F(1)},gram[h,j])
    need(rows==wanted and loc==base_locs,'complete actual 400-column paired source and final charts')
    need(e.exact_rank(rows.values())==400,'all original input directions survive')
    need(all(rows[host[j][0]].get(host[h][1],F(0))+rows[Y[h]].get(X[j],F(0))==0 for h in host for j in host),'all 9216 paired transpose entries')
    raw=Counter();owned=Counter()
    for o in out:
        if o[0]=='MOVE':(owned if o[4] else raw)[abs(len(frames[o[3]])-len(frames[o[2]]))]+=1
    need(dict(raw)=={1:129,2:131,3:105,4:6,5:206,6:16,7:16,8:154},'complete raw route ledger')
    need(dict(owned)=={1:20,2:2,8:14},'funded trajectory refinement ledger')
    need(sum(k*v for k,v in raw.items())==3200 and sum(k*v for k,v in owned.items())==136,'unchanged actual public and owned rank masses')
    reverse_rank=e.exact_rank([e.add(rows[b],{b:F(1),d:F(-1)},-1) for b,d in host.values()])
    forward_debt=sum(len(e.add(rows[Y[h]],{X[h]:F(1) if h in host else F(1,2),Y[h]:F(1) if h in host else F(1,2)},-1)) for h in ports)
    correction_rows=[{j:-gram[h,j] for hh,j in pairs if hh==h} for h in J]
    rank=e.exact_rank(correction_rows);need(rank==3,'three independently used prefix correction modes')
    denominators=sorted({F(o[3] if o[0]=='ADD' else o[2]).denominator for o in out if o[0]in('ADD','SCALE')})
    need(all(d&(d-1)==0 for d in denominators),'actual complete scalar word is dyadic')
    good_captures=copy.deepcopy(captures);up_rank=e.exact_rank(upward_boundary);down_rank=e.exact_rank(downward_boundary)
    need(len(upward_boundary)==7 and len(downward_boundary)==7 and up_rank==5 and down_rank==6,'actual lifetime-specific transported histories, without earlier numerical-label reuse')
    controls=[]
    for label,event in [('wrong_line_preload',next(k for k in events['line_acquisitions'] if out[k][1]==R)),('omit_reverse_reacquisition',events['reverse_restorations'][-1]),('omit_Hub_B_compensation',events['Hub_B_compensation'][0]),('omit_forward_augmentation',events['forward_augmentation'][0]),('omit_source_shedding',next(p['source_shed'] for p in down_phases if 'source_shed'in p)),('omit_output_read',events['output_reads'][0])]:
        bad=copy.deepcopy(w);bad['program'][event][3]='0'
        try:bad_rows,bad_locs,_=e.replay(bad,bad['program'],check);rejected=bad_rows!=rows or bad_locs!=loc
        except ValueError:rejected=True
        need(rejected,'meaningful negative control '+label);controls.append(label)
    phase=next(p for p in down_phases if 'output_capture'in p and 'source_shed'in p)
    bad=copy.deepcopy(w);a,b=phase['output_capture'],phase['source_shed'];bad['program'][a],bad['program'][b]=bad['program'][b],bad['program'][a]
    try:bad_rows,bad_locs,_=e.replay(bad,bad['program']);rejected=bad_rows!=rows or bad_locs!=loc
    except ValueError:rejected=True
    need(rejected,'same-station capture before removal is essential');controls.append('wrong_same_station_chronology')
    payload=(json.dumps(clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    args.output.mkdir(parents=True,exist_ok=True);(args.output/'WORD.json.gz').write_bytes(blob)
    result={'status':'PASS_ACTUAL_FUNDED_PAIRED_PREFIX_SOURCE','mode':'funded-prefix','word_sha256':sha(blob),'payload_sha256':sha(payload),'seed_sha256':SEED,'native_sha256':NATIVE,'replay_engine_sha256':REPLAY,'codec_sha256':CODEC,'paired_coefficients_removed_each_side':len(pairs),'correction_rank':rank,'reverse_mode_transport_history_rank':up_rank,'forward_mode_transport_history_rank':down_rank,'new_moving_owner_lifetimes':0,'new_stationary_owner_lifetimes':len(source_cache)+len(output_cache),'all400_input_rank':400,'all_final_charts_equal_seed':True,'all_original_D_restored_at_C3':True,'both_old_mode_endpoint_duties_restored':True,'hosted_R_plus_L_transpose_zero':True,'D_encoder_determinant':F(-1,2),'Y_encoder_determinant':F(-2),'class_C3_facet_incidences_checked':1456,'different_class_C3_contained_in_facet':0,'source_bill':bill,'raw_histogram':dict(raw),'owned_histogram':dict(owned),'owned_rank_mass':sum(k*v for k,v in owned.items()),'current_a_forward_offdiagonal_coefficients':4992-len(pairs),'original_coordinate_forward_debt':forward_debt,'reverse_residual_rank':reverse_rank,'all_source_scalar_denominators':denominators,'positive_phase_observations':good_captures,'negative_controls':controls,'scope':'Actual retained-mode prefix histories with complete endpoint restoration and all routes billed. One-class partial construction; no complete supplier or new kappa.'}
    (args.output/'RESULT.json').write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps(clean(result),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('native','seed','engine','codec','flag','output'):p.add_argument('--'+name,type=Path,required=True)
    main(p.parse_args())
