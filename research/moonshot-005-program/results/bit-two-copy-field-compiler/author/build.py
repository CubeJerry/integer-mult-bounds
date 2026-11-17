#!/usr/bin/env python3
"""Literal GL(4,2) frame service on two separately paid native copies.

All fields remain whole records. F4 is notation for binary mixing ACROSS
two independent native copies at an actual common chart, never a new
within-record primitive. Output is a complete-invoice partial source.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import argparse, hashlib, importlib.util, json

BASE='research/moonshot-005-program'
SOURCE=f'{BASE}/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
SOURCE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PARENT=f'{BASE}/sessions/2026-11-17-S020/checkpoint5-evidence/A/full-half-reservoir/WORD.json'
PARENT_SHA='6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980'
GEO=f'{BASE}/results/bit-leaf-capacity-quotient/author/check.py'
PRICE=f'{BASE}/sessions/2026-11-17-S019/checkpoint3-evidence/A/build_common_carrier_fanout.py'
A=[14,17,19,20]; B=[96,99,101,102]; ROLES=A+B

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return z

def inverse(a):
    assert a
    return next(b for b in range(1,4) if mul(a,b)==1)

def expand(M):
    return [sum(((mul(M[i//2][j//2],1<<(j%2))>>(i%2))&1)<<j for j in range(2*len(M[0]))) for i in range(2*len(M))]

def compile_binary(M):
    """Return literal source,destination ADDs executing nonsingular binary M."""
    n=len(M);r=list(M);reduction=[]
    def add(s,d):r[d]^=r[s];reduction.append((s,d))
    for j in range(n):
        p=next(i for i in range(j,n) if r[i]>>j&1)
        if p!=j:
            add(p,j);add(j,p);add(p,j)
        for i in range(n):
            if i!=j and r[i]>>j&1:add(j,i)
    assert r==[1<<i for i in range(n)]
    result=list(reversed(reduction));check=[1<<i for i in range(n)]
    for s,d in result:check[d]^=check[s]
    assert check==M
    return result

def bmul(M,rows):
    out=[]
    for r in M:
        v=0
        for j,x in enumerate(rows):
            if r>>j&1:v^=x
        out.append(v)
    return out

def public_name(c,kind,i):return f'C{c}__{kind}{i}'
def source_column(c,kind,i):return c*222+(i if kind=='X' else 111+i)

def replay(w,R,g,check_cut=None):
    C={n:g.chart(c)for n,c in w['charts'].items()}
    for i,r in enumerate(R):
        assert C[f'L{i}']==g.basis((tuple(r),))
        assert C[f'F{i}']==g.chart({'kind':'ann','rows':[r]})
    values={public_name(c,k,i):1<<source_column(c,k,i)for c in range(2)for k in ['X','Y']for i in range(111)}
    places={public_name(c,k,i):(f'L{i}'if k=='X'else'zero')for c in range(2)for k in ['X','Y']for i in range(111)}
    owned=set();born=set();counts=Counter();profile=Counter();owned_profile=Counter();dirty=peak=0;cv=cp=None
    for step,(op,n,*q)in enumerate(w['operations']):
        if step==w['carrier_interface_before_operation']:cv=values.copy();cp=places.copy()
        counts[op]+=1
        if op=='INIT':
            assert n not in values and n not in born and q[0]in C
            values[n]=0;places[n]=q[0];owned.add(n);born.add(n)
        elif op=='ADD':
            dest=q[0];assert n!=dest and n in values and dest in values
            assert C[places[n]]==C[places[dest]],(step,n,dest,'cochart')
            values[dest]^=values[n]
        elif op=='MOVE':
            before,after=C[places[n]],C[q[0]]
            assert g.sub(after,before)if n in owned else g.sub(before,after),(step,n,'direction')
            gap=abs(len(after)-len(before));assert gap>0
            profile[gap]+=1
            if n in owned:owned_profile[gap]+=1
            places[n]=q[0]
        elif op=='CLEAR':
            assert n in owned;dirty+=bool(values[n]);owned.remove(n);del values[n],places[n]
        else:raise AssertionError(op)
        peak=max(peak,len(owned))
    assert cv is not None and not owned and len(values)==444
    for c in range(2):
        for i in range(111):
            x=public_name(c,'X',i);y=public_name(c,'Y',i)
            assert values[x]==1<<source_column(c,'X',i)and places[x]=='Hub'
            assert values[y]==(1<<source_column(c,'Y',i))^int(w['Y_correction_rows_hex'][str(c)][i],16)
            assert places[y]==f'F{i}'
    if check_cut is not None:assert(cv,cp)==check_cut
    return C,cv,cp,{'all_original_columns':444,'copies':2,'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),
                  'owned_downward_profile':dict(sorted(owned_profile.items())),'owned_upward_moves':0,'dirty_CLEAR':dirty,'peak_owned':peak}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    raw=(args.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA;R=json.loads(raw)['native_roots']
    pr=(args.repo/PARENT).read_bytes();assert hashlib.sha256(pr).hexdigest()==PARENT_SHA;parent=json.loads(pr)
    g=load_module(args.repo/GEO,'two_copy_geometry');h=load_module(args.repo/PRICE,'two_copy_price')
    assert all(sum(x*y for x,y in zip(R[i],R[j]))==0 for i in ROLES for j in ROLES if i!=j)
    lam=2
    ps=[1,lam,1,lam];qs=[lam,1,lam,1]
    maps=[[[1,ps[i]],[1,qs[i]]] for i in range(4)]+[[[1,0],[1,1]] for i in range(4)]+[[[1,1],[inverse(ps[i]),inverse(qs[i])]] for i in range(4)]
    binary=[expand(M)for M in maps];programs=[compile_binary(M)for M in binary]
    charts=json.loads(json.dumps(parent['charts']));C={n:g.chart(c)for n,c in charts.items()}
    ops=[];sem={};values={public_name(c,k,i):1<<source_column(c,k,i)for c in range(2)for k in ['X','Y']for i in range(111)}
    places={public_name(c,k,i):(f'L{i}'if k=='X'else'zero')for c in range(2)for k in ['X','Y']for i in range(111)}
    def emit(o,key):
        sem.setdefault(key,[]).append(len(ops));ops.append(o);op,n,*q=o
        if op=='INIT':assert n not in values;values[n]=0;places[n]=q[0]
        elif op=='ADD':assert C[places[n]]==C[places[q[0]]];values[q[0]]^=values[n]
        elif op=='MOVE':places[n]=q[0]
        elif op=='CLEAR':del values[n],places[n]
    def translate(o,c):
        op,n,*q=o
        return [op,f'C{c}__{n}']+([f'C{c}__{q[0]}']if op=='ADD'else q)
    oldsem={j:k for k,indices in parent['semantic_operation_indices'].items()for j in indices}
    for c in range(2):
        for j,o in enumerate(parent['operations'][:parent['carrier_interface_before_operation']]):emit(translate(o,c),'parent_'+oldsem[j])
    parent_cut=len(ops);pv=values.copy();pp=places.copy()
    events=[]
    for roundno in range(3):
        for i in range(4):events.append({'round':roundno+1,'i':i,'j':(i+roundno)%4,'roles':[A[i],B[(i+roundno)%4]],'map':4*roundno+i})
    def local_apply(event,backward=False):
        fields=[public_name(c,'Y',i)for i in event['roles']for c in range(2)]
        word=list(reversed(programs[event['map']]))if backward else programs[event['map']]
        for src,dst in word:emit(['ADD',fields[src],fields[dst]],'ground_inverse_ADD'if backward else'forward_pair_compiler_ADD')
    for e in reversed(events):local_apply(e,True)
    seed={A[i]:A[(i+1)%4]for i in range(4)}|{B[j]:B[(j-1)%4]for j in range(4)}
    history={i:{seed[i]}for i in ROLES}
    for i in ROLES:
        for c in range(2):
            emit(['MOVE',public_name(c,'Y',i),f'L{seed[i]}'],'native_seed_arrival')
            emit(['ADD',f'C{c}__NATIVE_{seed[i]}',public_name(c,'Y',i)],'native_seed_read')
    for e in events:
        i,j=e['roles'];both=history[i]|history[j];assert i not in both and j not in both
        chart=f'DOUBLED_FRAME_R{e["round"]}_{e["i"]}';charts[chart]={'kind':'span','rows':[R[z]for z in sorted(both)]};C[chart]=g.chart(charts[chart])
        assert len(C[chart])==[2,4,6][e['round']-1]and g.sub(C[chart],C[f'F{i}'])and g.sub(C[chart],C[f'F{j}'])
        e['chart']=chart;e['source_roles']=sorted(both)
        for role in [i,j]:
            for c in range(2):emit(['MOVE',public_name(c,'Y',role),chart],'actual_two_copy_rendezvous')
            history[role]=both.copy()
        local_apply(e)
    cut=len(ops);cv=values.copy();cp=places.copy()
    expected={str(c):[int(x,16)<<(c*222)for x in parent['Y_correction_rows_hex']]for c in range(2)}
    expected_coeff={}
    for group,other,invert in [(A,B,False),(B,A,True)]:
        for i,role in enumerate(group):
            coeff={r:1 for r in group if r!=role}
            pcoef=inverse(ps[i]) if invert else ps[i];qcoef=inverse(qs[i]) if invert else qs[i]
            coeff[other[(i-1)%4]]=pcoef;coeff[other[i]]=qcoef;coeff[other[(i+1)%4]]=qcoef
            expected_coeff[str(role)]={str(r):x for r,x in coeff.items()}
            for c in range(2):
                for source,scalar in coeff.items():
                    for lane in range(2):
                        if mul(scalar,1<<lane)>>c&1:expected[str(c)][role]^=1<<source_column(lane,'X',source)
    assert all(values[public_name(c,'Y',i)]==(1<<source_column(c,'Y',i))^expected[str(c)][i]for c in range(2)for i in range(111))
    for c in range(2):
        for j,o in enumerate(parent['operations'][parent['carrier_interface_before_operation']:],parent['carrier_interface_before_operation']):emit(translate(o,c),'parent_'+oldsem[j])
    w={'schema':'two-separately-paid-native-copies-F4-frame-service-v1','source_path':SOURCE,'source_sha256':SOURCE_SHA,
       'parent_word_path':PARENT,'parent_word_sha256':PARENT_SHA,'native_copies':2,'original_column_convention':'copy*222+kind_offset+role; X offset0, Y offset111',
       'charts':charts,'operations':ops,'semantic_operation_indices':sem,'carrier_interface_before_operation':cut,
       'Y_correction_rows_hex':{c:list(map(hex,rows))for c,rows in expected.items()},
       'construction':{'roles_A':A,'roles_B':B,'field_modulus':7,'lambda':2,'local_F4_matrices':maps,'binary_row_masks':binary,
         'local_ADD_programs':programs,'local_ADD_lengths':list(map(len,programs)),'events':events,'seed_map':seed,'parent_copy_prefix_cut':parent_cut,
         'expected_foreign_coefficients':expected_coeff,'copies_are_independent_whole_records':True,'ancillas_for_local_compiler':0},
       'scope':'Two independent and separately charged native copies; only whole-record INIT/ADD/MOVE/CLEAR. An actual characteristic-two block-coded native receiver service, with all444 arbitrary original columns and all endpoints.8 coordinate outputs per copy remain complete; no new diagonal or complete supplier.'}
    _,V,P,stats=replay(w,R,g,check_cut=(cv,cp))
    assert stats['counts']=={'INIT':368,'ADD':2712+16+2*sum(map(len,programs)),'MOVE':992,'CLEAR':368}
    assert stats['movement_profile']=={1:326,2:238,4:206,7:222}
    assert len(V)==812 and Counter(len(C[P[public_name(c,'Y',i)]])for c in range(2)for i in range(111))=={0:206,6:16}
    for n in pv:
        if not any(n==public_name(c,'Y',i)for c in range(2)for i in ROLES):assert(V[n],P[n])==(pv[n],pp[n])
    original_ymask=sum(1<<source_column(c,'Y',i)for c in range(2)for i in range(111))
    for c in range(2):
        for i in range(111):assert V[public_name(c,'Y',i)]&original_ymask==1<<source_column(c,'Y',i)
    pin=h.save(args.out/'WORD.json',w)
    h.save(args.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'all_original_columns':444,
        'fields':[{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())]})
    normalized={k:v//2 for k,v in stats['movement_profile'].items()};assert all(v%2==0 for v in stats['movement_profile'].values())
    q=h.moment(normalized);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in h.moment(gate));room=(ceiling[0]-q[1],ceiling[1]-q[0])
    controls=[]
    for key in ['ground_inverse_ADD','native_seed_read','forward_pair_compiler_ADD','actual_two_copy_rendezvous','parent_cross_half_paid_unit_descent','parent_canonical_actual_Hub_gather']:
        bad=json.loads(json.dumps(w));ix=sem[key][0];del bad['operations'][ix];bad['carrier_interface_before_operation']-=1
        try:replay(bad,R,g,check_cut=(cv,cp))
        except (AssertionError,KeyError):controls.append('omit_'+key)
        else:raise AssertionError(('accepted',key))
    # Formal invariant: whole-record coordinate permutations plus record ADD
    # preserve the subspace of constant vectors; this nonidentity multiplier
    # sends (1,1) to (1,0), so it is not that single-record operation.
    assert mul(lam,3)==1
    controls.append('single_record_constant_lane_lambda_is_uncompilable_in_the_old_class')
    result={'status':'PASS_LITERAL_TWO_COPY_F4_WHOLE_RECORD_COMPILER','word_sha256':pin,'parent_word_sha256':PARENT_SHA,
       'native_copies':2,'all_original_columns':444,'cut':cut,'live_fields':len(V),'completed_coordinate_outputs':16,
       'new_diagonal_outputs':0,'serviced_Y_records':16,'serviced_geometric_roles':8,'public_Y_rank_histogram':{0:206,6:16},
       'local_ADD_lengths':list(map(len,programs)),'actual_added_compiler_ADDs':2*sum(map(len,programs)),'actual_seed_ADDs':16,
       'all_arbitrary_Y_baselines_restored':True,'all222_original_X_raw_at_Hub':True,'no_new_owned_fields':True,
       'strict_downward_owned_model':True,'stats':stats,'normalized_movement_profile':normalized,'normalized_moment':h.record(q),
       'total_two_copy_moment':h.record(h.moment(stats['movement_profile'])),'normalized_necessary_limiting_room':h.record(room),
       'normalized_ADD_count':str(Fraction(stats['counts']['ADD'],2)),'source_admission_does_not_prove_complete_caller':True,
       'negative_controls':controls,'scope':w['scope']}
    h.save(args.out/'RESULT.json',result)
    h.save(args.out/'COMPILER.json',w['construction'])
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
