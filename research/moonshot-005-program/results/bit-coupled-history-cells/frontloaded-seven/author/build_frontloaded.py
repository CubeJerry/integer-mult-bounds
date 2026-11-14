#!/usr/bin/env python3
"""Frontloaded original-Y local masks and reflected seven-target recoding."""
import argparse,gzip,hashlib,json,runpy
from collections import Counter
from pathlib import Path

BASE_PIN='244bedc78693645fdd70ed4540689e7d047e0a6eb260c3d40403ac691d43b7e8'
TARGETS=[92,36,54,38,55] # orthogonality cycle1,2,3,4,5
EXTRA=[110,23]
COMPLETED=TARGETS+EXTRA

def replay(word,m):
    need=m['need'];rref=m['rref'];included=m['included'];dot=m['dot']
    spaces={int(c):rref(f['B']) for c,f in word['frames'].items()}
    for c,f in word['frames'].items():
        b=spaces[int(c)];a=rref(f['A'])
        need(len(b)==f['dim'] and len(a)+len(b)==8 and all(dot(x,y)==0 for x in a for y in b),('frame',c))
    where=dict(enumerate(word['start']));rows={i:1<<i for i in range(222)}
    counts=Counter();paid=Counter();peak=lifetimes=0;clears=[]
    snapshots={};snapshot_events=set(word.get('snapshot_events',[]))
    for event,op in enumerate(word['program']):
        kind,a=op[:2];counts[kind]+=1
        if kind=='INIT':
            need(a>=222 and a not in rows,('owned birth',event,op));rows[a]=0;where[a]=op[2]
            lifetimes+=1;peak=max(peak,len(rows)-222)
        elif kind=='ADD':
            _,a,b,c=op;need(a!=b and a in rows and b in rows and where[a]==where[b]==c,('cochart',event,op));rows[a]^=rows[b]
        elif kind=='MOVE':
            _,a,c,d=op;need(a in rows and where[a]==c,('move source',event,op))
            dc,dd=len(spaces[c]),len(spaces[d]);need(dc!=dd,('positive move',event,op))
            need(included(spaces[c],spaces[d]) if dc<dd else included(spaces[d],spaces[c]),('real nested move',event,op))
            direction=word['directions'].get(str(a),'up' if a<222 else 'stationary')
            need((dd>dc if direction=='up' else dd<dc if direction=='down' else a>=222 if direction=='mixed' else False),('direction',event,op))
            paid[abs(dd-dc)]+=1;where[a]=d
        elif kind=='CLEAR':
            need(a>=222 and a in rows and where[a]==op[2],('owned retirement',event,op))
            clears.append({'event':event,'field':a,'chart':where[a],'row_hex':hex(rows[a])});del rows[a];del where[a]
        else:raise ValueError(('unknown operation',event,op))
        if event in snapshot_events:
            snapshots[str(event)]={'rows':{str(i):hex(rows[i])for i in list(range(339,342))+[111+j for j in COMPLETED] if i in rows},
                                  'charts':{str(i):where[i]for i in list(range(339,342))+[111+j for j in COMPLETED] if i in rows}}
    need(set(rows)==set(range(222))|set(word.get('end_owned',[])),'exact live set')
    need([where[i]for i in range(222)]==word['final'],'public endpoint charts')
    return {'rows':[rows[i]for i in range(222)],'owned_rows':{str(i):hex(rows[i])for i in rows if i>=222},
            'owned_where':{str(i):where[i]for i in rows if i>=222},'counts':dict(counts),
            'paid_profile':dict(sorted(paid.items())),'owned_lifetimes':lifetimes,'peak_owned':peak,
            'clear_rows':clears,'snapshots':snapshots}

def emit(native,c,m):
    need=m['need'];s=m['Source'](native)
    roots=[s.spaces[native['start'][j]][0]for j in TARGETS];Y={i:111+TARGETS[i-1]for i in range(1,6)}
    F={i:native['final'][Y[i]]for i in range(1,6)}
    def intersection(*labels):return s.chart(m['perpendicular']([roots[i-1]for i in labels]))
    C14=intersection(1,4);D134=intersection(1,3,4);D1345=intersection(1,3,4,5);D12345=intersection(1,2,3,4,5)
    need([len(s.spaces[q])for q in(C14,D134,D1345,D12345)]==[6,5,4,3],'actual reflection lattice ranks')
    need(all((m['dot'](roots[i],roots[j])==0)==((i-j)%5 in(1,4))for i in range(5)for j in range(5)if i!=j),'actual orthogonality cycle')
    copies={};events={};restore=[];undo=[];local_masks=[]
    prefix={'end_owned':list(range(222,333))+list(range(336,339))}
    # Preserve every original point before any source departs.
    for j in range(111):
        field=222+j;chart=s.where[j];s.init(field,chart);s.add(field,j,chart);copies[j]=field
    # All seven selected Y fields are still their arbitrary originals here.
    precode=[]
    for j,labels in((110,(1,2,5)),(23,(2,3,4))):
        for b in labels:precode.append(s.add(111+j,Y[b],s.zero))
    for a,b in((2,3),(2,4),(5,1),(5,3),(5,4),(4,1),(4,3)):
        precode.append(s.add(Y[a],Y[b],s.zero))
    line2=native['start'][TARGETS[1]]
    shared_reads=[]
    for receiver in(1,3):
        s.move(Y[receiver],line2);shared_reads.append(s.add(Y[receiver],TARGETS[1],line2))
    # Y4 reads X5 before that ORIGINAL leaves its source line.
    line5=native['start'][TARGETS[4]];s.move(Y[4],line5)
    y4local=s.add(Y[4],TARGETS[4],line5);s.move(Y[4],C14)
    # The two original private inputs visit actual rank-two cocharts on their ascent.
    for receiver,private,shared in((1,5,shared_reads[0]),(3,4,shared_reads[1])):
        source=TARGETS[private-1];chart=s.chart([roots[1],roots[private-1]])
        s.move(source,chart);s.move(Y[receiver],chart);private_read=s.add(Y[receiver],source,chart)
        s.move(Y[receiver],F[receiver])
        local_masks.append({'source_original':source,'receiver':receiver,'chart':chart,'copy':shared,'private_read':private_read})
    events['early_local_masks_acquired']=len(s.ops)-1
    # No halfbank is needed to encode E. All originals reach Hub unchanged.
    for j in range(111):s.move(j,s.hub)
    events['all_originals_at_Hub']=len(s.ops)-1
    core_copies=[];core_deposits=[]
    for t,b in enumerate(c['B']):
        packet=333+t;s.init(packet,s.hub)
        for j in range(111):
            if(b>>j)&1:s.add(packet,j,s.hub)
        s.move(packet,s.zero);core=336+t;s.init(core,s.zero);core_copies.append(s.add(core,packet,s.zero))
        for i,a in enumerate(c['A']):
            if i not in COMPLETED and(a>>t)&1:core_deposits.append(s.add(111+i,packet,s.zero))
        s.clear(packet)
    need(len(core_deposits)==162,'only104 unfinished receivers receive E')
    events['actual_core_ready']=len(s.ops)-1
    packets=[]
    for p,labels,receiver in ((339,(1,2,5),1),(340,(2,3,4),3)):
        s.init(p,s.hub);reads=[s.add(p,TARGETS[j-1],s.hub)for j in labels]
        s.move(p,F[receiver]);s.add(Y[receiver],p,F[receiver]);s.add(p,Y[receiver],F[receiver])
        packets.append({'field':p,'encoder_targets':labels,'reads':reads,'completion':len(s.ops)-2})
    events['first_and_third_complete']=len(s.ops)-1
    s.move(339,C14);s.move(340,D134)
    # Reflect one actual packet history upward, use it, and return its recoded history.
    s.init(341,D134);copyB=s.add(341,340,D134);s.move(341,C14)
    y4a=s.add(Y[4],339,C14);y4b=s.add(Y[4],341,C14);recoding=s.add(341,Y[4],C14)
    events['fourth_complete_copy_recoded']=len(s.ops)-1
    s.move(341,D134);s.move(339,D134)
    swap=[]
    for a,b in ((340,341),(341,340),(340,341)):swap.append(s.add(a,b,D134))
    s.clear(341);events['new_history_returned']=len(s.ops)-1
    # The last two targets require no local X masks.
    s.move(339,D1345);s.move(340,D1345);s.move(Y[5],D1345)
    y5a=s.add(Y[5],339,D1345);y5b=s.add(Y[5],340,D1345)
    feedback=[s.add(339,Y[5],D1345)]
    s.move(Y[5],F[5]);s.move(Y[4],F[4])
    s.move(340,D12345);s.move(339,D12345);s.move(Y[2],D12345);y2=s.add(Y[2],340,D12345)
    feedback += [s.add(339,Y[2],D12345),s.add(340,Y[2],D12345)]
    events['first_five_complete_Y_only_packets']=len(s.ops)-1
    s.move(Y[2],F[2]);refills=[]
    for packet,j in zip((339,340),EXTRA):
        line=native['start'][j]
        need(m['included'](s.spaces[line],s.spaces[D12345]),'actual refill point is in common orthogonal complement')
        s.move(packet,line);read=s.add(packet,copies[j],line);s.move(packet,s.zero)
        done=s.add(111+j,packet,s.zero);s.clear(packet);s.move(111+j,native['final'][111+j])
        refills.append({'packet':packet,'input':j,'line':line,'read':read,'completion':done})
    events['all_seven_complete']=len(s.ops)-1
    def word(scope):
        w=s.word(prefix['end_owned'],scope);w['schema']='BIT-native-frontloaded-reflected-pentagon-with-refill-v1';w['owned_fields']=120
        w['directions'].update({str(i):'down'for i in(339,340)}|{'341':'mixed'})
        w['snapshot_events']=list(events.values());return w
    partial=word('Exact paid seven-target coupled decoder with frontloaded original-source reads. All111 X restored; other104 Y remain unfinished. No complete source or kappa.')
    remaining_restore=[]
    for i in range(111):s.move(111+i,native['final'][111+i])
    for p in prefix['end_owned']:s.clear(p)
    closed=word('Closed partial map: allXrestoredHub; sevenYcorrect; other104Y=y+E; allownedretired. No complete supplier or kappa.');closed['end_owned']=[]
    return partial,closed,{'targets':TARGETS,'extra_targets':EXTRA,'feedback':feedback,'refills':refills,'charts':{'C14':C14,'D134':D134,'D1345':D1345,'D12345':D12345},
        'events':events,'restoration':restore,'remaining_restoration':remaining_restore,'core_undo':undo,'precode':precode,
        'local_masks':local_masks,'core_copies':core_copies,'core_deposits':core_deposits,'Y4_local_read':y4local,'packets':packets,'reflected_copy':copyB,
        'Y4_decoding':[y4a,y4b],'copy_recoding':recoding,'return_swap':swap,'Y5_decoding':[y5a,y5b],'Y2_decoding':y2}

def main(a):
    need=lambda ok,msg:None if ok else (_ for _ in ()).throw(ValueError(msg))
    need(hashlib.sha256(a.prefix_builder.read_bytes()).hexdigest()==BASE_PIN,'prefix builder pin')
    m=runpy.run_path(str(a.prefix_builder));raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==m['PIN'],'native pin')
    native=json.loads(gzip.decompress(raw));c=m['analyse'](native);partial,closed,meta=emit(native,c,m)
    pr=replay(partial,m);cr=replay(closed,m)
    want=[1<<i for i in range(222)]
    for i,e in enumerate(c['E']):want[111+i]^=(1<<i)if i in COMPLETED else e
    need(cr['rows']==want,'all222 independent columns of closed partial map')
    pwant=list(want)
    need(pr['rows']==pwant,'all original X unchanged at Hub and exact unfinished Y values')
    need(closed['final']==native['final'][:222],'all actual native closed endpoint charts')
    need(partial['final'][:111]==native['final'][:111],'all original X actually at Hub')
    need(all(partial['final'][111+i]==(native['final'][111+i]if i in COMPLETED else native['start'][111+i])for i in range(111)),'actual completed and unfinished Y locations')
    need(pr['owned_rows']==({str(222+j):hex(1<<j)for j in range(111)}|{str(336+t):hex(b)for t,b in enumerate(c['B'])}),'all actual point and pure core values')
    need(pr['owned_where']==({str(222+j):native['start'][j]for j in range(111)}|{str(336+t):native['start'][111]for t in range(3)}),'all actual point and pure core locations')
    need(pr['paid_profile']=={1:868}and cr['paid_profile']=={1:1596},'complete MOVE invoices')
    need(pr['counts']=={'INIT':120,'ADD':452,'MOVE':868,'CLEAR':6},'partial ordinary and ownership invoice')
    need(cr['counts']=={'INIT':120,'ADD':452,'MOVE':1596,'CLEAR':120},'closed partial invoice')
    need(pr['peak_owned']==117,'actual peak ownership')
    controls=[]
    def omit(k,word=partial):
        w=json.loads(json.dumps(word));del w['program'][k];return replay(w,m)
    for name,k in [('actual_core_cache',meta['core_copies'][0]),('initial_Y_precoding',meta['precode'][0]),('actual_original_x2_read',meta['local_masks'][0]['copy']),
                   ('local_x5_read',meta['Y4_local_read']),('reflected_packet_copy',meta['reflected_copy']),('copy_recoding',meta['copy_recoding']),
                   ('Y5_first_channel',meta['Y5_decoding'][0]),('Y2_completion',meta['Y2_decoding'])]:
        bad=omit(k);need(bad['rows']!=pwant or bad['owned_rows']!=pr['owned_rows'],('mutation not detected',name));controls.append({'name':'omit_'+name,'rejected':True})
    for k in meta['feedback']+[r['read']for r in meta['refills']]:
        bad=omit(k);need(bad['rows']!=pwant,'missing real reuse operation');controls.append({'name':'omit_reuse_operation_'+str(k),'rejected':True})
    retained_copy=next(k for k,op in enumerate(partial['program'])if op[0]=='ADD'and op[1:3]==[230,8])
    bad=omit(retained_copy);need(bad['owned_rows']!=pr['owned_rows'],'uncounted unused point retention');controls.append({'name':'omit_actual_retained_point_copy','rejected':True})
    for kind in ('up','down'):
        k=next(n for n,op in enumerate(partial['program'])if op[0]=='MOVE'and op[1]==341 and (partial['frames'][op[3]]['dim']>partial['frames'][op[2]]['dim'])==(kind=='up'))
        try:omit(k)
        except ValueError:pass
        else:raise ValueError('unpaid reflection move accepted')
        controls.append({'name':'omit_reflection_'+kind+'_MOVE','rejected':True})
    # The exact unfinished state still has a six-dimensional untouched receiver cut.
    S=[8,9,14,15,30,31,59]
    rootrows=[[m['F'](x) for x in native['frames'][str(native['start'][i])]['B'][0]]for i in S]
    def inside(chart):
        chartbasis=m['rref'](partial['frames'][chart]['B'])
        return any(all(m['dot'](r,v)==0 for v in chartbasis)for r in rootrows)
    observed=[pr['rows'][i]for i,chart in enumerate(partial['final'])if inside(chart)]
    observed += [int(row,16)for i,row in pr['owned_rows'].items()if inside(pr['owned_where'][i])]
    before=m['rank'](observed);after=m['rank'](observed+[(1<<i)^(1<<(111+i))for i in S])
    need(after-before==6,'remaining actual-state cut deficit')
    cut={'receivers':S,'inside_observation_rank':before,'rank_with_targets':after,'deficit':after-before,
         'premise':'After both new Hub packets retire, no additional inward records other than future Hub packets; all114 point/core caches remain as emitted.'}
    a.output.mkdir(parents=True,exist_ok=True)
    pins={name:m['save_word'](a.output/name,w)for name,w in [('PARTIAL-WORD.json.gz',partial),('CLOSED-WORD.json.gz',closed)]}
    for r in(pr,cr):r.pop('rows')
    out={'status':'PASS_FRONTLOADED_SEVEN_TARGET_RECODING_TWO_EXTRA_MOVES','native_sha256':m['PIN'],'prefix_builder_sha256':BASE_PIN,
         'metadata':meta,'remaining_receiver_cut':cut,'partial_receipt':pr,'closed_receipt':cr,'word_pins':pins,'negative_controls':controls,
         'scope':'Actual frontloaded seven-target partial module, arbitrary originalY, two newHub packets, two reflection unitmoves, original-source local acquisition, completed-Y feedback and two physical point refills. Not a complete six/sevenpacket decoder.',
         'dominated_C5_subcell_control':'One direct point drop plus two orthogonal-pair packets is cheaper for the isolated5target task; no optimality or target-budget gain claimed.',
         'complete_supplier':False,'new_kappa':False}
    (a.output/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':out['status'],'partial_counts':pr['counts'],'closed_counts':cr['counts'],'peak_owned':pr['peak_owned'],'negative_controls':len(controls)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--prefix-builder',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
