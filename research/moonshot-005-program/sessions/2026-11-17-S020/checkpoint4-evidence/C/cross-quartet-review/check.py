#!/usr/bin/env python3
"""Independent cross-quartet replay and fixed-half-bank source-expiry gates."""
from pathlib import Path
from collections import Counter,defaultdict
from itertools import combinations
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
REVIEW_PIN='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PARENT='c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'
CASES=[('cross-quartet-export-1',1,'42b37f28cbd958ffda84dbb5f4e6caa16ca465d368d965378093b0277d97541a'),
       ('cross-quartet-exports-greedy',19,'5923a3724a1aee3b0d37eee5dfc269bb12541f37155f47eb07aae2727cedfc91')]
NEW_KEYS=['actual_old_query_baseline_birth','actual_old_query_baseline_capture','fresh_native_source_arrival',
 'fresh_half_sum_encode','fresh_collector_rank4_arrival','representative_rank4_arrival','fresh_half_read',
 'new_export_birth','actual_rank4_Y_capture','paid_rank4_to_query_descent','actual_query_baseline_removal',
 'fresh_mode_original_carrier_load','returned_export_native_receiver_read','unload_fresh_modes_at_Hub',
 'fresh_half_sum_inverse_at_Hub','cross_export_retirement']

def basis(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b

def residual(x,b):
    for p in sorted(b,reverse=True):
        if x>>p&1:x^=b[p]
    return x

def dual_for(rows,target):
    b=basis(rows);r=residual(target,b);assert r;p=r.bit_length()-1
    d=sum(((residual(1<<j,b)>>p)&1)<<j for j in range(111))
    assert (d&target).bit_count()%2==1 and all((d&v).bit_count()%2==0 for v in rows)
    return d

def record(interval):
    with localcontext()as c:
        c.prec=55
        return {'rational':list(map(str,interval)),'decimal':[str(Decimal(v.numerator)/Decimal(v.denominator))for v in interval]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,default=BASE/'workers/C/native.json')
    ap.add_argument('--inputs',type=Path,default=BASE/'workers/A')
    ap.add_argument('--parent',type=Path,default=BASE/'workers/A/low-retention-corrections/WORD.json')
    ap.add_argument('--source-review',type=Path,default=BASE/'workers/C/proper-query-export-review/check.py')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    assert hashlib.sha256(a.source_review.read_bytes()).hexdigest()==REVIEW_PIN
    spec=importlib.util.spec_from_file_location('own_source',a.source_review)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.geo=m.load_arithmetic(a.arithmetic)
    raw=a.native.read_bytes();assert hashlib.sha256(raw).hexdigest()==NATIVE
    R=json.loads(raw)['native_roots'];xmask=(1<<111)-1
    N=[{j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0}for i in range(111)]
    K=[(1<<i)^sum(1<<j for j in N[i])for i in range(111)]
    praw=a.parent.read_bytes();assert hashlib.sha256(praw).hexdigest()==PARENT
    parent=json.loads(praw);oldcharts={n:m.geo.chart(c)for n,c in parent['charts'].items()}
    oldD=[int(v,16)for v in parent['Y_correction_rows_hex']]
    parent_stats,PV,PP=m.replay(parent,oldcharts,oldD,check_cut=False)
    oldcut=parent['carrier_interface_before_operation'];assert oldcut==836
    oldE={i for i in range(111)if len(oldcharts[PP[f'X{i}']])>1};assert len(oldE)==40
    pair_carriers={PP[f'X{i}']:f'X{i}'for i in range(111)if len(oldcharts[PP[f'X{i}']])==3}
    groups=defaultdict(list)
    for i,r in enumerate(R):
        if i not in oldE:groups[tuple(j for j,x in enumerate(r)if x)].append(i)
    assert len(groups)==10 and sum(map(len,groups.values()))==71
    halves=[sum(1<<i for i in I if R[i][p]==sign*R[i][q])
            for support,I in groups.items()for p,q in combinations(support,2)for sign in [1,-1]]
    assert len(halves)==120 and len(basis(halves))==40 and len(basis(K+oldD+halves))==56
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));sources=[];bankcases=[]
    for name,k,pin in CASES:
        raw=(a.inputs/name/'WORD.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        w=json.loads(raw);assert w['construction']['parent_word_sha256']==PARENT
        charts={n:m.geo.chart(c)for n,c in w['charts'].items()}
        assert all(w['charts'][n]==z for n,z in parent['charts'].items())
        assert w['operations'][:oldcut]==parent['operations'][:oldcut]
        inserted={j for key in NEW_KEYS for j in w['semantic_operation_indices'].get(key,[])}
        assert [op for j,op in enumerate(w['operations'])if j not in inserted]==parent['operations']
        exports=w['construction']['fresh_cross_quartet_exports'];assert len(exports)==k
        EV,EP=PV.copy(),PP.copy();used=set();expected_ops=[];derivedD=oldD.copy()
        profile=Counter(parent_stats['movement_profile'])
        for z in exports:
            S=z['sources'];q=z['query'];Y=z['actual_served_Y_roles'];H=z['source_plane'];J=z['rendezvous_chart']
            support=tuple(z['support']);p0,p1=z['pair'];sign=z['sign']
            assert S==[i for i in groups[support]if R[i][p0]==sign*R[i][p1]]and not(set(S)&used)
            assert sign in [1,-1]and len(S)in[3,4]and p0<p1 and p0 in support and p1 in support
            eligible=[i for i in range(111)if EP[f'Y{i}']==q and set(S)<=N[i]]
            assert Y==eligible and Y and z['representative_Y_role']==Y[0]
            collector=f'X{S[0]}';target=pair_carriers[q]
            assert z['source_collector']==collector and z['changed_old_carrier']==target
            expectedH=m.geo.basis(tuple(tuple(R[i])for i in S));expectedJ=m.geo.basis(expectedH+oldcharts[q])
            assert charts[H]==expectedH and charts[J]==expectedJ and len(expectedH)==3 and len(expectedJ)==4
            assert not m.geo.contained(expectedH,charts[q])and m.geo.contained(charts[q],expectedJ)
            assert all(m.geo.contained(expectedJ,charts[f'F{i}'])for i in Y)
            base,export=z['baseline_owner'],z['export_owner'];baseline=EV[f'Y{Y[0]}'];row=sum(1<<i for i in S)
            assert z['baseline_hex']==hex(baseline)and z['payload_hex']==hex(row)
            new=[['INIT',base,q],['ADD',f'Y{Y[0]}',base]]
            for i in S:
                assert EV[f'X{i}']==1<<i and EP[f'X{i}']==f'L{i}'
                new.append(['MOVE',f'X{i}',H]);EP[f'X{i}']=H
            new.extend([['ADD',f'X{i}',collector]for i in S[1:]])
            new.extend([['MOVE',collector,J],['MOVE',f'Y{Y[0]}',J],['ADD',collector,f'Y{Y[0]}'],
             ['INIT',export,J],['ADD',f'Y{Y[0]}',export],['MOVE',export,q],['ADD',base,export],['ADD',export,target]])
            new.extend([['ADD',export,f'Y{i}']for i in Y[1:]])
            expected_ops.extend(new);EV[base]=baseline;EP[base]=q;EV[export]=row;EP[export]=q
            EV[collector]=row;EP[collector]=J;EV[target]^=row;EP[f'Y{Y[0]}']=J
            for i in Y:EV[f'Y{i}']^=row;derivedD[i]^=row
            used.update(S);profile.update({1:3,2:len(S),3:1,5:len(S)-1,7:-len(S)})
        assert w['operations'][oldcut:w['carrier_interface_before_operation']]==expected_ops
        assert w['Y_correction_rows_hex']==list(map(hex,derivedD))
        assert all(not(d>>i&1)and all(j in N[i]for j in range(111)if d>>j&1)for i,d in enumerate(derivedD))
        stats,V,P=m.replay(w,charts,derivedD,check_cut=False)
        assert V==EV and P==EP and len(basis(V[f'X{i}']for i in range(111)))==111
        assert stats['movement_profile']==dict(sorted((d,c)for d,c in profile.items()if c))
        assert stats['owned_downward_profile']=={1:k}and stats['peak_owned']==stats['dirty_CLEAR']==111+2*k
        assert stats['cut_fields']==333+2*k
        for i in range(111):assert V[f'NATIVE_{i}']==1<<i and P[f'NATIVE_{i}']==f'L{i}'
        closure=[op for op in w['operations'][w['carrier_interface_before_operation']:]if op[0]=='MOVE']
        assert len(closure)==222 and len({op[1]for op in closure})==222
        assert all(op[2]==('Hub'if op[1].startswith('X')else f"F{op[1][1:]}")for op in closure)
        unload=[['ADD',z['source_collector'],z['changed_old_carrier']]for z in exports]
        restore=[['ADD',f'X{i}',z['source_collector']]for z in exports for i in z['sources'][1:]]
        u=w['semantic_operation_indices']['unload_fresh_modes_at_Hub'];f=w['semantic_operation_indices']['fresh_half_sum_inverse_at_Hub']
        assert [w['operations'][j]for j in u]==unload and [w['operations'][j]for j in f]==restore
        assert u+f==list(range(min(u),max(f)+1))and max(f)<min(w['semantic_operation_indices']['deferred_sign_inverse_at_Hub'])
        payloads=[sum(1<<i for i in z['sources'])for z in exports]
        assert len(basis(payloads))==k and len(basis(K+oldD+payloads))==(22 if k==1 else 37)
        controls={}
        for label in ['actual_old_query_baseline_capture','fresh_half_sum_encode','fresh_half_read','actual_rank4_Y_capture',
         'paid_rank4_to_query_descent','actual_query_baseline_removal','fresh_mode_original_carrier_load',
         'unload_fresh_modes_at_Hub','fresh_half_sum_inverse_at_Hub']:
            alt=json.loads(json.dumps(w));j=alt['semantic_operation_indices'][label][0];del alt['operations'][j]
            if j<alt['carrier_interface_before_operation']:alt['carrier_interface_before_operation']-=1
            try:m.replay(alt,charts,derivedD,check_cut=False)
            except ValueError as err:controls['omit_'+label]=str(err)
            else:raise AssertionError('missing operation accepted')
        alt=json.loads(json.dumps(w));alt['operations'][min(u):max(f)+1]=restore+unload
        try:m.replay(alt,charts,derivedD,check_cut=False)
        except ValueError as err:controls['restore_fresh_before_unload']=str(err)
        else:raise AssertionError('wrong inverse order accepted')
        Q=m.geo.moment(stats['movement_profile']);room=(ceiling[0]-Q[1],ceiling[1]-Q[0])
        T=[14,16,60,63,84,85,107,109];mask=sum(1<<i for i in T)
        assert all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for i in T for j in T)
        inside=[n for n in V if any(m.geo.contained(charts[P[n]],charts[f'F{i}'])for i in T)]
        initial_rank=len(basis(V[n]&mask for n in inside));assert initial_rank==(1 if k==1 else 4)
        sources.append({'source':name,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],'stats':stats,
         'fresh_source_roles':sorted(used),'fresh_modes':k,'source_original_X_rank':111,
         'new_receiver_reads':sum(len(z['actual_served_Y_roles'])for z in exports),
         'total_foreign_coefficients':sum(d.bit_count()for d in derivedD),'global_actual_half_bank_rank':22 if k==1 else 37,
         'moment':record(Q),'necessary_room':record(room),'negative_controls':controls,
         'eight_facet_roles':T,'eight_facet_inside_fields':len(inside),'eight_facet_initial_rank':initial_rank,
         'independent_future_owned_descent_lower_bound':8-initial_rank})
        # Source-aware fixed-bank continuation certificates are added below.
        certify_banks(name,k,pin,m,R,N,K,oldD,oldE,halves,payloads,used,charts,stats,V,P,ceiling,bankcases)
        print(name,'PASS all222 source, actual baseline chronology, real geometry and ordered inverse',flush=True)
    (a.out/'RESULT.json').write_text(json.dumps({'status':'PASS_INDEPENDENT_CROSS_QUARTET_SOURCES','native_sha256':NATIVE,
     'source_review_sha256':REVIEW_PIN,'parent_sha256':PARENT,'cases':sources},indent=2)+'\n')
    (a.out/'BANK-CERTIFICATE.json').write_text(json.dumps({'status':'PASS_SCOPED_CROSS_QUARTET_FIXED_HALF_BANK_GATES',
     'complete_fresh_half_count':120,'complete_fresh_half_rank':40,'complete_global_bank_rank':56,'cases':bankcases,
     'scope':'Exact audited cuts, monotone public routes, arbitrary paid nested owned routes, linear continuation over characteristic-two fields. Every future downward X history must remain in the stated fixed bank. New directions outside the complete half bank, earlier cuts or public turns escape.'},indent=2)+'\n')

def certify_banks(name,k,pin,m,R,N,K,oldD,oldE,halves,payloads,used,charts,stats,V,P,ceiling,out):
    E=[i for i in range(111)if len(charts[P[f'X{i}']])>1];assert set(E)==oldE|used
    assert all([n for n in V if charts[P[n]]==charts[f'L{j}']]==[f'NATIVE_{j}']for j in E)
    ground=[i for i in range(111)if not charts[P[f'Y{i}']]];assert ground==[4,5,6,7]
    L={i:[V[n]&((1<<111)-1)for n in V if not n.startswith('NATIVE_')and m.geo.contained(charts[P[n]],charts[f'F{i}'])]for i in range(111)}
    for bankname,extra in [('actual_fresh_half_bank',payloads),('complete_fresh_half_bank',halves)]:
        G=list(basis(K+oldD+extra).values());forced={}
        for i in range(111):
            b=basis(G+L[i]);target=residual(1<<i,b);J=sorted(set(E)&N[i]);cols={j:residual(1<<j,b)for j in J}
            assert not residual(target,basis(cols.values()))
            forced[i]=[j for j in J if residual(target,basis(cols[h]for h in J if h!=j))]
        fanout=[]
        for j in E:
            chosen=[];rb=()
            for i in range(111):
                if j not in forced[i]:continue
                trial=m.geo.basis(rb+(tuple(R[i]),))
                if len(trial)>len(rb):chosen.append(i);rb=trial
            rank=len(rb);assert rank>0
            if bankname=='actual_fresh_half_bank':assert rank==(6 if j==3 else 7)
            if rank==7:assert m.geo.kernel(rb)==charts[f'L{j}']
            witnesses=[]
            for i in chosen if rank==7 else chosen[:1]:
                obs=G+L[i]+[1<<h for h in E if h in N[i]and h!=j]
                d=dual_for(obs,1<<i);assert d>>j&1
                witnesses.append({'receiver':i,'dual_hex':hex(d)})
            fanout.append({'expired_role':j,'demand_normal_rank':rank,'independent_receiver_roles':chosen,
             'dual_witnesses':witnesses,'minimum_native_line_departures':2 if rank==7 else 1})
        exits=sum(z['minimum_native_line_departures']for z in fanout);owned=exits-4
        assert owned==((83 if k==1 else 213)if bankname=='actual_fresh_half_bank'else(40 if k==1 else 105))
        mandatory=dict(stats['movement_profile']);mandatory[1]+=owned
        lower=m.geo.moment(mandatory);excess=(lower[0]-ceiling[1],lower[1]-ceiling[0])
        out.append({'source':name,'word_sha256':pin,'bank':bankname,'bank_rank':len(G),
         'expired_count':len(E),'fanout':fanout,'demand_rank_histogram':dict(Counter(z['demand_normal_rank']for z in fanout)),
         'native_line_departures':exits,'maximum_public_line_departures':4,
         'minimum_future_owned_upward_moves':owned,'mandatory_profile':mandatory,
         'target_excess':record(excess),'strict_exclusion':excess[0]>0})
        print(name,bankname,'owned ascents >=',owned,'strict exclusion',excess[0]>0,flush=True)

if __name__=='__main__':main()

