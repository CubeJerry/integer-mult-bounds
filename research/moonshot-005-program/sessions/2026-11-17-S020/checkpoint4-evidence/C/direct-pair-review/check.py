#!/usr/bin/env python3
"""Independent direct-pair source replay and enlarged fixed-bank fanout screen."""
from pathlib import Path
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
REVIEW_PIN='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PARENT='c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'
CASES=[(4,'33a07beacc3895822300eb34ebb847f5b9ff030cc2ad82cdfbc3152fe8402fc0'),
       (12,'6472eee72de969e204b546549fabdd9bd1cfaa5353ea8d4078b94d5ab1a44e05'),
       (16,'91cd623b23d299d44da5355838d5ead01614bc2ce6f2cf696a8d6500b73824c1')]
NEW_KEYS=['direct_pair_birth','actual_pair_snapshot','paid_pair_descent','direct_pair_donor_load',
          'unload_pair_at_Hub_before_old_inverses','direct_pair_retirement']

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
    b=basis(rows);r=residual(target,b);assert r
    p=r.bit_length()-1
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
    s=importlib.util.spec_from_file_location('own_source_replay',a.source_review)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.geo=m.load_arithmetic(a.arithmetic)
    raw=a.native.read_bytes();assert hashlib.sha256(raw).hexdigest()==NATIVE
    R=json.loads(raw)['native_roots'];xmask=(1<<111)-1
    N=[{j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0}for i in range(111)]
    K=[(1<<i)^sum(1<<j for j in N[i])for i in range(111)]
    praw=a.parent.read_bytes();assert hashlib.sha256(praw).hexdigest()==PARENT
    parent=json.loads(praw);charts={n:m.geo.chart(c)for n,c in parent['charts'].items()}
    correction=[int(v,16)for v in parent['Y_correction_rows_hex']]
    parent_stats,PV,PP=m.replay(parent,charts,correction,check_cut=False)
    assert sum(v.bit_count()for v in correction)==528
    assert all(not(v>>i&1)and all(j in N[i]for j in range(111)if v>>j&1)for i,v in enumerate(correction))
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));results=[];banks=[]
    for k,pin in CASES:
        path=a.inputs/f'direct-pair-exports-{k}'/'WORD.json';raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
        w=json.loads(raw);assert w['charts']==parent['charts']and w['Y_correction_rows_hex']==parent['Y_correction_rows_hex']
        assert w['operations'][:parent['carrier_interface_before_operation']]==parent['operations'][:parent['carrier_interface_before_operation']]
        inserted={j for key in NEW_KEYS for j in w['semantic_operation_indices'][key]}
        assert [op for j,op in enumerate(w['operations'])if j not in inserted]==parent['operations']
        exports=w['construction']['direct_pair_exports'];assert len(exports)==k
        stats,V,P=m.replay(w,charts,correction,check_cut=False)
        assert stats['counts']=={'INIT':111+k,'ADD':455+3*k,'MOVE':508+k,'CLEAR':111+k}
        assert stats['movement_profile']=={1:175+k,2:111,3:4,4:111,5:16,6:16,7:75}
        assert stats['owned_downward_profile']=={1:k}and stats['peak_owned']==stats['dirty_CLEAR']==111+k
        assert len(basis(V[f'X{i}']for i in range(111)))==111
        pair_rows=[];destinations=[]
        for z in exports:
            u=int(z['row_hex'],16);src=z['source_original'];don=z['changed_donor'];own=z['owner'];Q=z['source_query'];P2=z['destination_chart']
            assert u==sum(1<<i for i in z['source_pair'])and u.bit_count()==2
            assert PV[src]==u and PP[src]==Q and PV[don]==1<<z['changed_donor_native_role']and PP[don]==P2
            assert len(charts[Q])==3 and len(charts[P2])==2 and m.geo.contained(charts[P2],charts[Q])
            source_span=m.geo.basis(tuple(tuple(R[i])for i in z['source_pair']))
            assert len(source_span)==2 and not m.geo.contained(source_span,charts[P2])and len(m.geo.basis(source_span+charts[P2]))==3
            assert V[own]==u and P[own]==P2 and V[don]==PV[don]^u and P[don]==P2
            assert V[src]==u and P[src]==Q
            pair_rows.append(u);destinations.append(don)
        assert len(set(destinations))==k and len(basis(pair_rows))==k
        DS=[r&~255 for r in correction];DF=correction
        ranks=[len(basis(K+pair_rows)),len(basis(K+DS+pair_rows)),len(basis(K+DF+pair_rows))]
        assert ranks==[9+k,25,25 if k==4 else 29]
        controls={}
        for label in ['actual_pair_snapshot','paid_pair_descent','direct_pair_donor_load','unload_pair_at_Hub_before_old_inverses']:
            alt=json.loads(json.dumps(w));j=alt['semantic_operation_indices'][label][0];del alt['operations'][j]
            if j<alt['carrier_interface_before_operation']:alt['carrier_interface_before_operation']-=1
            try:m.replay(alt,charts,correction,check_cut=False)
            except ValueError as err:controls['omit_'+label]=str(err)
            else:raise AssertionError('missing operation accepted')
        alt=json.loads(json.dumps(w));unloads=set(alt['semantic_operation_indices']['unload_pair_at_Hub_before_old_inverses'])
        oldend=max(alt['semantic_operation_indices']['deferred_sign_inverse_at_Hub'])
        moved=[o for j,o in enumerate(alt['operations'])if j in unloads]
        kept=[o for j,o in enumerate(alt['operations'])if j not in unloads]
        where=oldend+1-len(unloads);alt['operations']=kept[:where]+moved+kept[where:]
        try:m.replay(alt,charts,correction,check_cut=False)
        except ValueError as err:controls['unload_after_old_inverses']=str(err)
        else:raise AssertionError('wrong inverse order accepted')
        Q=m.geo.moment(stats['movement_profile']);room=(ceiling[0]-Q[1],ceiling[1]-Q[0])
        results.append({'exports':k,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],'stats':stats,
                        'source_original_X_rank':111,'code_ranks_C_pairs_C_sign_pairs_C_full_pairs':ranks,
                        'moment':record(Q),'necessary_room':record(room),'negative_controls':controls})
        E=[i for i in range(111)if len(charts[P[f'X{i}']])>1];assert len(E)==40
        G=list(basis(K+DF+pair_rows).values());L={i:[V[n]&xmask for n in V if not n.startswith('NATIVE_')and m.geo.contained(charts[P[n]],charts[f'F{i}'])]for i in range(111)}
        forced={}
        for i in range(111):
            b=basis(G+L[i]);target=residual(1<<i,b);J=sorted(set(E)&N[i]);cols={j:residual(1<<j,b)for j in J}
            forced[i]=[j for j in J if residual(target,basis(cols[h]for h in J if h!=j))]
        fanout=[]
        for j in E:
            chosen=[];rb=()
            for i in range(111):
                if j not in forced[i]:continue
                trial=m.geo.basis(rb+(tuple(R[i]),))
                if len(trial)>len(rb):chosen.append(i);rb=trial
            rank=len(rb);assert rank==(6 if j==3 else 7)
            ws=[]
            for i in chosen:
                obs=G+L[i]+[1<<h for h in E if h in N[i]and h!=j];d=dual_for(obs,1<<i);assert d>>j&1
                ws.append({'receiver':i,'dual_hex':hex(d)})
            if rank==7:assert m.geo.kernel(rb)==charts[f'L{j}']
            fanout.append({'expired_role':j,'rank':rank,'independent_receiver_roles':chosen,'duals':ws})
        U=[8,9,14,15];umask=sum(1<<i for i in U)
        inside=[n for n in V if any(m.geo.contained(charts[P[n]],charts[f'F{i}'])for i in U)]
        assert all(not(V[n]&umask)for n in inside)
        ground=[i for i in range(111)if not charts[P[f'Y{i}']]];assert ground==[4,5,6,7]
        lower_profile=dict(stats['movement_profile']);lower_profile[1]+=79
        lower=m.geo.moment(lower_profile);excess=(lower[0]-ceiling[1],lower[1]-ceiling[0]);assert excess[0]>0
        banks.append({'exports':k,'word_sha256':pin,'bank':'C plus old full-query span plus actual pair span','bank_rank':len(G),
                      'fanout':fanout,'owned_upward_lower_bound':75,'fresh_cut_roles':U,'fresh_cut_inside_fields':len(inside),
                      'owned_downward_lower_bound':4,'total_future_owned_move_lower_bound':79,
                      'mandatory_profile':lower_profile,'target_excess':record(excess)})
        print('direct pair',k,'PASS all222 source; enlarged fixed-bank gate excess',excess[0])
    (a.out/'RESULT.json').write_text(json.dumps({'status':'PASS_INDEPENDENT_DIRECT_PAIR_SOURCES','native_sha256':NATIVE,'parent_sha256':PARENT,'cases':results},indent=2)+'\n')
    (a.out/'BANK-CERTIFICATE.json').write_text(json.dumps({'status':'PASS_ENLARGED_FIXED_PAIR_BANK_FANOUT_GATE','cases':banks,
        'scope':'Actual direct-pair cuts; monotone public routes; every future downward X payload remains in C plus the full old-query and actual-pair spans. Additional modes and changed sources escape.'},indent=2)+'\n')

if __name__=='__main__':main()
