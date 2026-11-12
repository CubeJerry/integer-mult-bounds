#!/usr/bin/env python3
"""Rotate E8 packets and deliver the last two on actual nested late charts."""
import argparse,copy,sys
from pathlib import Path

PARENT_PAYLOAD='2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a'
BASIS_NORMALS=[7,25,52,76,97,127,42,82]

def main(a):
    reconstruction=a.repo/'research/moonshot-005-program/results/cohort-reconstruction'
    sys.path.insert(0,str(reconstruction))
    from common import F,Counter,Emitter,need,sha,load_inputs,root,space,basis,add,gzip,json
    import build as replay
    s,_,invoice=load_inputs(a.repo)
    parentpath=a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz'
    pb=parentpath.read_bytes();need(sha(gzip.decompress(pb))==PARENT_PAYLOAD,'exact rank88 parent payload')
    p=json.loads(gzip.decompress(pb));raw={int(x):r for x,r in p['private_role_map'].items()}
    xs=s['live'];roots={x:root(s['frames'][s['initial'][x]][0]) for x in xs}
    normals={s['frames'][s['initial'][x]][0] for x in xs}
    wr=[root(z) for z in BASIS_NORMALS]
    dot=lambda x,y:sum(u*v for u,v in zip(x,y))
    need(not(set(BASIS_NORMALS)&normals),'omitted source roots')
    need([[dot(x,y) for y in wr] for x in wr]==[[8*int(i==j) for j in range(8)] for i in range(8)],'orthogonal omitted root basis')
    U=[[F(dot(w,roots[x]),8) for x in xs] for w in wr]
    need(all(sum(bool(c) for c in row)==52 for row in U),'52 nonzero source coefficients per packet')
    need(all(sum(U[k][i]*U[k][j] for k in range(8))==F(dot(roots[x],roots[y]),8) for i,x in enumerate(xs) for j,y in enumerate(xs)),'entire104-by104 Gram decoder unchanged')
    z1,z2=BASIS_NORMALS[-2:];S1={xs[i] for i,c in enumerate(U[6]) if c};S2={xs[i] for i,c in enumerate(U[7]) if c};both=S1&S2
    need(len(S1)==len(S2)==52 and len(both)==24,'actual late recipient support census')
    decl=copy.deepcopy(p['additional_charts']);spaces=list(map(space,s['frames']+[d['frame'] for d in decl]))
    def chart(frame,name):
        S=space(frame)
        if S in spaces:return spaces.index(S)
        i=len(spaces);spaces.append(S);decl.append({'index':i,'frame':basis(S),'construction':name});return i
    c1=chart([z1],'late packet1 missing-root line');c2=chart([z2],'late packet2 missing-root line');c12=chart([z1,z2],'actual two-line packet intersection span')
    firstmoves={}
    for x in S1|S2:
        moves=[(i,e) for i,e in enumerate(p['program'][:p['marks']['common_starts']]) if e[0]=='MOVE' and e[1]==raw[x+112]]
        need(len(moves)==1 and moves[0][1][2]==3,'single unread receiver prefix ascent')
        i,e=moves[0];oldtarget=e[3]
        current=c12 if x in both else c1 if x in S1 else c2
        need(spaces[current]<spaces[oldtarget],'new receiver stop belongs to actual existing prefix endpoint')
        firstmoves[x]=(i,oldtarget,current)
    # Detect the eight old packet lifetimes without trusting a fixed index range.
    olddesc=[(i,e) for i,e in enumerate(p['program'][:p['marks']['initial_decoders']]) if e[0]=='MOVE' and e[2:]==[127,3,True]]
    need(len(olddesc)==8 and len({e[1] for i,e in olddesc})==1,'eight original packet descents')
    packet=olddesc[0][1][1]
    packet_begin=max(i for i,e in enumerate(p['program'][:olddesc[0][0]]) if e==['INIT',packet,127])
    packet_end=p['marks']['initial_decoders']
    need(p['program'][packet_end-1]==['CLEAR',packet,3],'exact old packet block endpoint')
    first_move=next(i for i in range(packet_end,p['marks']['common_starts']) if p['program'][i][0]=='MOVE')
    early=list(range(packet_end,first_move))
    rawY={raw[x+112] for x in xs}
    need(len(early)==164 and all(p['program'][i][0]=='ADD' and p['program'][i][1] in rawY and p['program'][i][2]<1480 and p['program'][i][4]==3 for i in early),'164 authentic independent common-input additions at empty chart')
    # All first-Y reads between old packet end and its prefix ascent are exactly
    # these hoisted additions or the ascent; collectors are consumed later.
    for x,(i,_,_) in firstmoves.items():
        uses=[(j,e) for j,e in enumerate(p['program'][packet_end:i],packet_end) if e[1]==raw[x+112] or e[0] in ('ADD','COPY') and e[2]==raw[x+112]]
        need(all(j in early for j,e in uses),'no stale receiver observation skipped by retiming')
    hosted={s['live'][k] for k in s['hosted']['Dports']};scales={x:F(1) if x in hosted else F(1,2) for x in xs}
    E=Emitter();mapping={};boundaries={};packet_records=[];route_records=[];newblock=None;hoist_begin=None
    def emit(op,parent=None):return E.emit(op,parent)
    def partial_route(x,start,end):
        old=firstmoves[x][0];j=emit(['MOVE',raw[x+112],start,end,False],old);mapping.setdefault(old,j)
        route_records.append({'source_receiver':x+112,'event':j,'from':start,'to':end,'replaces_parent_move':old});return j
    def packet_start(k):
        rec={'basis_normal':BASIS_NORMALS[k],'begin':len(E.ops),'encoder':[],'descents':[],'deliveries':[]}
        emit(['INIT',packet,127])
        for x,c in zip(xs,U[k]):
            if c:rec['encoder'].append(emit(['ADD',packet,raw[x],str(c),127]))
        return rec
    def deliver(k,rec,receivers,at):
        for x,c in zip(xs,U[k]):
            if x in receivers:
                need(c,'only nonzero packet delivery');rec['deliveries'].append({'firstX':x,'event':emit(['ADD',raw[x+112],packet,str(scales[x]*c),at]),'chart':at})
    def replacement():
        nonlocal hoist_begin,newblock
        hoist_begin=len(E.ops)
        for i in early:mapping[i]=len(E.ops);emit(copy.deepcopy(p['program'][i]),i)
        newblock=[len(E.ops),None]
        for k in range(6):
            rec=packet_start(k);rec['descents'].append(emit(['MOVE',packet,127,3,True]));deliver(k,rec,{x for x,c in zip(xs,U[k]) if c},3);emit(['CLEAR',packet,3]);rec['end']=len(E.ops);packet_records.append(rec)
        for x in sorted(S1):partial_route(x,3,c1)
        rec=packet_start(6);rec['descents'].append(emit(['MOVE',packet,127,c1,True]));deliver(6,rec,S1,c1);emit(['CLEAR',packet,c1]);rec['end']=len(E.ops);packet_records.append(rec)
        for x in sorted(both):partial_route(x,c1,c12)
        for x in sorted(S2-S1):partial_route(x,3,c2)
        rec=packet_start(7);rec['descents'].append(emit(['MOVE',packet,127,c12,True]));deliver(7,rec,both,c12);rec['descents'].append(emit(['MOVE',packet,c12,c2,True]));deliver(7,rec,S2-S1,c2);emit(['CLEAR',packet,c2]);rec['end']=len(E.ops);packet_records.append(rec)
        newblock[1]=len(E.ops)
    replaced_moves={v[0]:x for x,v in firstmoves.items()}
    for i,op in enumerate(p['program']):
        if i==packet_begin:replacement()
        boundaries[i]=len(E.ops)
        if packet_begin<=i<packet_end or i in early:continue
        if i in replaced_moves:
            x=replaced_moves[i];_,target,current=firstmoves[x];partial_route(x,current,target);continue
        mapping[i]=len(E.ops);emit(copy.deepcopy(op),i)
    boundaries[len(p['program'])]=len(E.ops)
    need(all(v in mapping for v in p['native_event_to_physical']),'all native source operations retained literally')
    marks={}
    for name,i in p['marks'].items():
        if name=='initial_decoders':marks[name]=hoist_begin
        elif packet_begin<=i<packet_end:raise ValueError('unhandled packet-internal boundary '+name)
        else:marks[name]=boundaries[i]
    w=copy.deepcopy(p);w['parent_second_frame_feedback_provenance']=w.pop('second_frame_feedback')
    w.update(schema='moonshot-S009-two-late-Gram-packets-v1',program=E.ops,additional_charts=decl,parent_event_of_output=E.lineage,parent_word_sha256=sha(pb),marks=marks,native_event_to_physical=[mapping[v] for v in p['native_event_to_physical']],late_packet_delivery={'basis_normals':BASIS_NORMALS,'encoder_matrix':[[str(c) for c in row] for row in U],'first_line':c1,'second_line':c2,'joint_chart':c12,'first_support':sorted(S1),'second_support':sorted(S2),'common_support':sorted(both),'old_packet_range':[packet_begin,packet_end],'new_packet_range':newblock,'hoisted_initial_decoder_range':[packet_end,first_move],'hoist_begin':hoist_begin,'packets':packet_records,'new_raw_segments':route_records,'parent_receivers_rerouted':{str(x+112):list(v) for x,v in sorted(firstmoves.items())}})
    before,bloc=replay.interpret_prefix(s,p);after,aloc=replay.interpret_prefix(s,w)
    need(before==after and bloc==aloc,'identical full1880-coordinate common-entry state')
    need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'literal identical common suffix')
    bill=replay.typed(s,w);oldbill=replay.typed(s,p);need(bill.pop('final_locations')==oldbill.pop('final_locations'),'all final charts unchanged')
    rawhist=Counter(bill['raw_histogram']);oldraw=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw)
    need(sum(r*n for r,n in rawhist.items())==3200,'unchanged total raw rank mass')
    own=Counter({9:6,8:1,7:1,1:1});T=Counter({int(k):v for k,v in invoice['T4'].items()});P=Counter({int(k):v for k,v in invoice['P4'].items()})
    for r in rawhist.keys()|oldraw.keys():P[r]+=18*(rawhist[r]-oldraw[r])
    for r,n in own.items():P[r]+=18*n
    need(all(n>=0 for n in P.values()),'complete nonnegative invoice');lo,hi=replay.interval({r:T[r]-P[r] for r in T.keys()|P.keys()})
    oldresult=json.loads((parentpath.parent/'RESULT.json').read_text());oldlo=F(oldresult['conditional_caller']['remaining_moment_per_native_lower']);oldhi=F(oldresult['conditional_caller']['remaining_moment_per_native_upper'])
    result={'status':'PASS_ACTUAL_TWO_LATE_PACKET_SOURCE_WORD','source_sha256':p['source_sha256'],'parent_payload_sha256':PARENT_PAYLOAD,'all_input_columns':1880,'same_exact_parent_prefix_state':True,'same_literal_parent_suffix':True,'reverse_residual_rank':88,'forward_residual_coefficients':4569,'basis_normals':BASIS_NORMALS,'late_support_counts':[len(S1),len(S2),len(both)],'owned_packet_histogram':dict(sorted(own.items())),'hoisted_common_input_adds':len(early),'raw_paths_refined':len(firstmoves),'bill':bill,'ordinary_increment':{op:bill['opcode_counts'].get(op,0)-oldbill['opcode_counts'].get(op,0) for op in sorted(bill['opcode_counts'].keys()|oldbill['opcode_counts'].keys())},'conditional_caller':{'T4':dict(sorted(T.items())),'P_partial':dict(sorted(P.items())),'paid_positions':sum(P.values()),'target_positions':sum(T.values()),'rank_surplus':sum(r*(T[r]-P[r]) for r in T.keys()|P.keys()),'remaining_moment_per_native_lower':str(lo/18),'remaining_moment_per_native_upper':str(hi/18),'saving_per_native_lower':str(lo/18-oldhi),'saving_per_native_upper':str(hi/18-oldlo),'retained_paid_packets':dict(sorted(own.items()))},'scope':'Actual unchanged-map source retiming and rotated Gram delivery with full recursive accounting. No new complete kappa; physical scalar/compiler/uniformity and all five foundations remain.'}
    a.out.mkdir(parents=True,exist_ok=True);payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);result['word_payload_sha256']=sha(payload);result['word_sha256']=sha(blob);(a.out/'WORD.json.gz').write_bytes(blob);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);main(ap.parse_args())
