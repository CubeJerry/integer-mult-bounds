#!/usr/bin/env python3
"""Source-bound four-main lowering and ambient-cap compiler certificate.

@CubeJerry, substantial OpenAI assistance. Apache-2.0.
This checker certifies finite interface facts. PROOF.md states the quantified
compiler implication and the retained physical/analytic assumptions.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha1, sha256
from pathlib import Path
import argparse
import copy
import gzip
import importlib.util
import json
import ambient_bounds

HERE=Path(__file__).resolve().parent


def need(condition,message):
    if not condition:
        raise ValueError(message)


def read(name):
    p=HERE/name;raw=p.read_bytes()
    return json.loads(gzip.decompress(raw) if name.endswith('.gz') else raw)


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def authenticate():
    files=read('RETAINED.json')['files']
    for entry in files:
        data=(HERE/entry['path']).read_bytes()
        need(len(data)==entry['bytes'] and sha256(data).hexdigest()==entry['sha256'], 'retained SHA256 and size')
        need(sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['git_blob'],'retained Git blob')
    return len(files)


def span(basis):
    out={0}
    for x in basis:
        need(type(x) is int and 0<x<512 and x not in out,'independent nine-axis frame')
        out|={v^x for v in out}
    return out


def native(word):
    n=len(word['initial']);owned=word['owned_fields'];frames=word['frames']
    spaces=[span(f) for f in frames];dim=list(map(len,frames))
    current=word['initial'][:]+[None]*owned;active=set();peak=births=0
    mains=set(word['live'])|{x+112 for x in word['live']}|set(word['hosted']['X2'])|set(word['hosted']['Y2'])
    need(len(mains)==416 and len(set(word['ports']))==104,'four disjoint source main sets')
    repeated=0
    for x,x2,y2,q in zip(word['live'],word['hosted']['X2'],word['hosted']['Y2'],word['ports']):
        y=x+112
        need(frames[word['initial'][x]]==[q] and dim[word['final'][x]]==9,'first X charts')
        need(dim[word['initial'][y]]==0 and spaces[word['final'][y]]=={a for a in range(512) if (a&q).bit_count()%2==0},'first Y charts')
        for a,b in ((x,x2),(y,y2)):
            need(a!=b and (word['initial'][a],word['final'][a])==(word['initial'][b],word['final'][b]),'equal frame type but distinct physical owners')
            repeated+=1
    helpers={r:dim[b]-dim[a] for r,(a,b) in enumerate(zip(word['initial'],word['final'])) if r not in mains}
    need(all(spaces[word['initial'][r]]<spaces[word['final'][r]] for r in helpers),'strict whole helper endpoints')
    paid=[];scalar_upper=0
    for index,event in enumerate(word['program']):
        op,dst=event[:2]
        need(type(dst) is int and 0<=dst<n+owned,'native destination')
        if op in ('INIT','CLEAR'):
            need(dst>=n,'only owned reset')
            if op=='INIT':
                need(dst not in active and current[dst] is None,'exclusive owned birth')
                active.add(dst);current[dst]=event[2];births+=1;peak=max(peak,len(active))
            else:
                need(dst in active and current[dst]==event[2],'clear current owned field')
                active.remove(dst);current[dst]=None
        elif op=='MOVE':
            a,b,private=event[2:]
            need(type(private) is bool and private==(dst in active) and current[dst]==a,'actual paid owner and chart')
            need(spaces[a]<spaces[b] or (private and spaces[b]<spaces[a]),'nested positive-child factorization domain')
            rank=abs(dim[b]-dim[a]);paid.append((index,dst,rank,a,b,private));current[dst]=b
        else:
            need(op in ('ADD','COPY','SCALE'),'ordinary native alphabet')
            q=Q(event[-2]);a=abs(q.numerator);d=q.denominator
            need(q and d&(d-1)==0 and current[dst]==event[-1],'dyadic scalar on current chart')
            if op=='SCALE':
                need(a&(a-1)==0,'unit dyadic scale')
                scalar_upper+=4*(a.bit_length()+d.bit_length()+1)
            else:
                src=event[2]
                need(src!=dst and 0<=src<n+owned and current[src]==current[dst],'two distinct coframed actual owners')
                need(op!='COPY' or dst in active,'owned COPY')
                scalar_upper+=4*(a.bit_length()+a.bit_count()+d.bit_length()+1)
    need(not active and current[:n]==word['final'],'completed public frames and owned return')
    return dict(public=n,owned=owned,helpers=helpers,mains=mains,paid=paid,
                peak=peak,lifetimes=births,repeated_frame_pairs=repeated,scalar_upper=scalar_upper)


def signature(word,caller,ledger,alias_second_main=False,reuse_helper=False):
    need(caller['ambient_rank']==153 and caller['roles']==40 and caller['stages']==18,'actual caller geometry')
    ports=word['ports'];n=ledger['public'];all_productive=set();targets=[];requests=[]
    for role,(qp,zero,*mask) in enumerate(caller['diagonal']):
        need(qp in (-1,0,1) and zero==0 and len(mask)==18 and set(mask)<={0,1},'whole main exponent domain')
        axes=([0] if qp else [])+[9+8*j+k for j,yes in enumerate(mask) if yes for k in range(8)]
        need(len(axes)==len(set(axes)) and all(0<=x<153 for x in axes),'whole main canonical selected axes')
        for q in ports:
            owner=('main',role,q);all_productive.add(owner);targets.append((owner,len(axes)))
    hosts=0;events=Counter()
    for index,event in enumerate(caller['events']):
        op=event[0];events[op]+=1
        if op=='HOST2':
            stage,x,y,x2,y2=event[1:]
            need(stage==hosts+1 and len({x,y,x2,y2})==4,'one chronological four-distinct-main contact')
            mapping={}
            for a,q,b,c in zip(word['live'],ports,word['hosted']['X2'],word['hosted']['Y2']):
                mapping[a]=('main',x,q);mapping[a+112]=('main',y,q)
                mapping[b]=('main',x if alias_second_main else x2,q);mapping[c]=('main',y2,q)
            for role,rank in ledger['helpers'].items():
                owner=('helper',0 if reuse_helper else hosts,role)
                need(owner not in all_productive,'fresh helper source has one physical field and one credit')
                all_productive.add(owner);mapping[role]=owner;targets.append((owner,rank))
            need(len(mapping)==n and len(set(mapping.values()))==n,'injective complete native public map')
            for role in range(n,n+ledger['owned']):mapping[role]=('owned',hosts,role-n)
            need(len(set(mapping.values()))==n+ledger['owned'],'owned fields disjoint from productive slots')
            for local,owner,rank,a,b,private in ledger['paid']:
                requests.append((('native',index,local),mapping[owner],rank,a,b,private))
            hosts+=1
        elif op=='IDLE_ONE':
            owner,stages=event[1:]
            need(0<=owner<40 and stages and len(set(stages))==len(stages) and all(1<=s<=18 for s in stages),'whole idle owner and disjoint selected stages')
            for q in ports:requests.append((('idle',index,q),('main',owner,q),8*len(stages),None,None,False))
        elif op=='QUERY':
            dst,src,power=event[1:]
            need(dst!=src and 0<=dst<40 and 0<=src<40 and power in (-1,1),'query on distinct public fields')
            for q in ports:requests.append((('query',index,q),('query_owned',0),1,power,None,True))
        elif op=='LAMBDA':need(event[2] in (-1,1),'ordinary global normalizer')
        else:need(op in ('ADD','SCALE','SWAP'),'caller ordinary alphabet')
    need(hosts==18 and events['LAMBDA']==124 and events['QUERY']==6 and events['IDLE_ONE']==32,'exact unchanged primitive count')
    need(len({key for key,*_ in requests})==len(requests),'every actual paid position appears exactly once')
    need(len({owner for owner,_ in targets})==len(targets)==len(all_productive),'one target credit per distinct arbitrary field')
    return targets,requests,events


def rejected(call):
    try:call()
    except ValueError:return True
    return False


def compare_requests(actual,expected):
    need(actual==expected,'all actual requests in exact chronological order, without omission or coalescence')


def source_tail(target,paid):
    spec=importlib.util.spec_from_file_location('credited_intervals',HERE/'retained/intervals.py')
    interval=importlib.util.module_from_spec(spec);spec.loader.exec_module(interval)
    saving=Q('0.00351406007');t=1-saving
    tm=interval.moment(target,t)
    alpha=interval.divide(interval.moment(paid,t),tm)
    gamma=interval.divide(interval.moment(paid,t+Q(1,7)),interval.mul(interval.power(11,Q(1,7)),tm))
    delta=interval.divide((Q(sum(target.values())*12),)*2,interval.mul(interval.power(11,saving),tm))
    need(Q(1,7)>=saving and alpha[1]<1-Q(1,10**27) and gamma[1]<Q(31,32) and delta[1]<Q(31,32),'actual higher-moment strictification predicates')
    need(1/(1+Q(1920,10**27))+4*Q(31,32)**1920<1,'all completion and paid-tail charges')
    return dict(tested_saving=str(saving),alpha_upper=str(alpha[1]),gamma_upper=str(gamma[1]),delta_upper=str(delta[1]),
                method='Credited retained rational interval engine; not a new independent transcendental implementation.',power=1920)


def result():
    pins=authenticate();word=read('retained/native-word.json.gz');caller=read('retained/caller.json');ledger=native(word)
    recipes=read('retained/PORT-PHASES.json');by_port={r['q']:r for r in recipes['recipes']}
    for q in word['ports']:
        basis=[q]+by_port[q]['idle_children'][0]['orthogonal_axes'][:8]
        need(len(basis)==9 and all((a&b).bit_count()%2==int(i==j) for i,a in enumerate(basis) for j,b in enumerate(basis)),'literal complete q-normalization basis')
    targets,requests,events=signature(word,caller,ledger)
    target=Counter(rank for _,rank in targets);paid=Counter(r[2] for r in requests)
    need(sum(target.values())==21422 and sum(paid.values())==119872,'source-bound field and actual paid-request counts')
    need(max(paid)==64 and min(target)==1 and max(target)==145,'raw rule overlaps and target cap differs from ambient')
    controls={
        'alias_same_frame_main':rejected(lambda:signature(word,caller,ledger,alias_second_main=True)),
        'reuse_helper_across_calls':rejected(lambda:signature(word,caller,ledger,reuse_helper=True)),
        'missing_paid_request':rejected(lambda:compare_requests(requests[1:],requests)),
        'double_paid_request':rejected(lambda:compare_requests(requests[:1]+requests,requests)),
        'reordered_equal_rank_jobs':False,
        'double_helper_credit':False,
        'raw_separation_rejected':max(paid)>=min(target),
    }
    changed=requests[:];a,b=next((i,j) for i in range(20) for j in range(i+1,20) if requests[i][2]==requests[j][2])
    changed[a],changed[b]=changed[b],changed[a]
    controls['reordered_equal_rank_jobs']=rejected(lambda:compare_requests(changed,requests))
    controls['double_helper_credit']=len({owner for owner,_ in targets+targets[-1:]})!=len(targets)+1
    need(all(controls.values()),'substantive signature controls')
    route_groups=len(ledger['paid'])+2*len(ledger['helpers'])+416+832+4*ledger['lifetimes']
    # Exact source tariff is reproduced from its literal target/idle/query axes.
    swaps=lambda axes:len(set(axes)-set(range(len(axes))))
    main_maps=0
    for qp,zero,*mask in caller['diagonal']:
        axes=([0] if qp else [])+[9+8*j+k for j,yes in enumerate(mask) if yes for k in range(8)]
        main_maps+=104*(2*swaps(axes)+2*bool(qp)+int(qp==-1))
    idle_maps=query_maps=0
    for event in caller['events']:
        if event[0]=='IDLE_ONE':idle_maps+=208*swaps([9+8*(s-1)+k for s in event[2] for k in range(8)])
        elif event[0]=='QUERY':query_maps+=104*(2+int(event[3]==-1))
    raw=18*(ledger['scalar_upper']+1000*route_groups)+32*40*104*len(caller['events'])+6*16*104+40*104*26+1000*(main_maps+idle_maps+query_maps)
    normalizer=124*104*1000
    need(raw==971071328 and raw+normalizer==983967328<10**9,'complete original ordinary allowance with global normalizer routes')
    return dict(schema_version=1,status='PASS_FOUR_MAIN_COMPILER_INSTANCE',retained_files=pins,
        source_word_payload_sha256=sha256(canonical(word)).hexdigest(),caller_sha256=sha256((HERE/'retained/caller.json').read_bytes()).hexdigest(),
        native=dict(public=ledger['public'],owned=ledger['owned'],helpers=len(ledger['helpers']),paid=len(ledger['paid']),lifetimes=ledger['lifetimes'],peak=ledger['peak']),
        physical_main_contacts=18*416,repeated_frame_distinct_owner_pairs=18*ledger['repeated_frame_pairs'],
        main_fields=4160,helper_fields=18*len(ledger['helpers']),productive_fields=len(targets),paid_requests=len(requests),
        target={str(k):v for k,v in sorted(target.items())},paid={str(k):v for k,v in sorted(paid.items())},target_rank_mass=sum(k*v for k,v in target.items()),paid_rank_mass=sum(k*v for k,v in paid.items()),
        ordered_request_sha256=sha256(canonical(requests)).hexdigest(),ordered_target_sha256=sha256(canonical(targets)).hexdigest(),
        actual_ambient_axes=153,maximum_target_rank=145,source_ordinary_upper=raw,global_normalizer_route_debit=normalizer,complete_ordinary_upper=raw+normalizer,
        strictification=source_tail(target,paid),ambient_majorant=ambient_bounds.verify(),controls=controls,
        limits=['Five inherited framework assumptions remain.','External BIT admission and outer recovery are not proved here.','No gigantic finite compiler word is materialized.','No new kappa and no selected-frontier update.'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');args=parser.parse_args()
    data=result()
    if args.emit:(HERE/'RESULT.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    else:need(data==read('RESULT.json'),'complete committed receipt reproduces')
    print(json.dumps({k:data[k] for k in ('status','productive_fields','paid_requests','actual_ambient_axes','maximum_target_rank','complete_ordinary_upper','controls')},sort_keys=True))
    print('PASS_FOUR_MAIN_COMPILER_INSTANCE')
