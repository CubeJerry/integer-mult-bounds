"""Verify supplied fanout duals by parity and independent source geometry."""
from pathlib import Path
from collections import Counter
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json
GEO='983c931bc9907de160fa59fc2011cff434766d7e7384ce898df05574cc5c61fc'
ARITH='41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(p,name):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def rank2(rows):
    piv={}
    for row in rows:
        while row:
            c=(row&-row).bit_length()-1
            if c in piv:row^=piv[c]
            else:piv[c]=row;break
    return len(piv)
def record(interval):
    with localcontext()as c:
        c.prec=55;return {'rational':list(map(str,interval)),'decimal':[str(Decimal(x.numerator)/Decimal(x.denominator))for x in interval]}
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--fanout',type=Path,required=True);p.add_argument('--pair-certificate',type=Path,required=True);p.add_argument('--nine-certificate',type=Path,required=True);p.add_argument('--geometry',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert digest(a.geometry)==GEO;g=module(a.geometry,'own_source_geometry')
    base=a.repo/'research/moonshot-005-program';arithmetic=base/'sessions/2026-11-17-S020/checkpoint2-evidence/C/four-plane-review/check.py';assert digest(arithmetic)==ARITH;m=module(arithmetic,'pinned_interval_arithmetic')
    native=base/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert digest(native)==g.NATIVE;R=json.loads(native.read_text())['native_roots']
    old=json.loads(a.fanout.read_text());pairs=json.loads(a.pair_certificate.read_text());nine=json.loads(a.nine_certificate.read_text());assert nine['status']=='PASS_MAPPED_17_OVER_2_WITNESS_AND_FIVE_ACTUAL_CUTS'
    N=[{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)];K=[(1<<i)|sum(1<<j for j in N[i])for i in range(111)];xmask=(1<<111)-1
    low=json.loads((a.inputs/'low-retention-corrections/WORD.json').read_text());_,lv,_=g.replay_cut(low);queries=[lv[f'Y{i}']&xmask for i in range(111)];assert rank2(K)==9 and rank2(queries)==12
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in m.moment(gate));cases=[];total_duals=0
    for name,pin in g.PINS.items():
        wp=a.inputs/name/'WORD.json';assert digest(wp)==pin;word=json.loads(wp.read_text());charts,V,P=g.replay_cut(word)
        E={i for i in range(111)if len(charts[P[f'X{i}']])>1};assert E==set(range(8))|set(range(22,46))|set(range(88,96))
        assert all(V[f'NATIVE_{i}']==1<<i and P[f'NATIVE_{i}']==f'L{i}'for i in range(111))
        ground=[i for i in range(111)if not charts[P[f'Y{i}']]];assert ground==[4,5,6,7]
        if name.startswith('direct-pair'):
            count=int(name.rsplit('-',1)[1]);src=next(c for c in pairs['cases']if c['exports']==count);bank=K+queries+[v&xmask for n,v in V.items()if n.startswith('DIRECT_PAIR_')];rank=25 if count==4 else 29
        else:
            src=next(c for c in old['cases']if c['source']==name);bank=K+(queries if name.startswith('low-')else[v&xmask for n,v in V.items()if n.startswith('QUERY_EXPORT_')]);rank=21
        assert src['word_sha256']==pin and rank2(bank)==rank
        fan=src['fanout'];assert {z['expired_role']for z in fan}==E;counts=[];duals_checked=0
        for z in fan:
            j=z['expired_role'];receivers=z['independent_receiver_roles'];witnesses=z.get('dual_witnesses',z.get('duals'));assert [v['receiver']for v in witnesses]==receivers
            normal_rank=len(g.rref([R[i]for i in receivers]));assert normal_rank==z.get('demand_normal_rank',z.get('rank'))and normal_rank in[6,7]
            if normal_rank==7:assert g.nullspace([R[i]for i in receivers])==charts[f'L{j}']
            for witness in witnesses:
                i=witness['receiver'];d=int(witness['dual_hex'],16);assert j in N[i]and(d>>i)&1 and(d>>j)&1
                assert all((d&v).bit_count()%2==0 for v in bank)
                for n,v in V.items():
                    if not n.startswith('NATIVE_')and g.contains(charts[f'F{i}'],charts[P[n]]):assert (d&v&xmask).bit_count()%2==0
                assert all(not(d>>k&1)for k in E&N[i]if k!=j);duals_checked+=1
            counts.append((j,normal_rank,2 if normal_rank==7 else 1))
        assert Counter(r for _,r,_ in counts)=={7:39,6:1}and [j for j,r,_ in counts if r==6]==[3]
        exits=sum(n for _,_,n in counts);owned=exits-len(ground);assert exits==79 and owned==75 and duals_checked==279;total_duals+=duals_checked
        ncase=next(c for c in nine['cases']if c['source']==name);assert ncase['word_sha256']==pin and ncase['minimum_future_whole_record_descents']==9 and not ncase['nonlocal_leaks']
        # Independently verify Q0 is exactly prefix plus direct public closures.
        places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};profile=Counter();suffix=set()
        for step,(kind,n,*args)in enumerate(word['operations']):
            if kind=='INIT':places[n]=args[0]
            elif kind=='MOVE':
                dest=args[0];profile[abs(len(charts[places[n]])-len(charts[dest]))]+=1
                if step>=word['carrier_interface_before_operation']:
                    assert n.startswith(('X','Y'))and n not in suffix;suffix.add(n);assert dest==('Hub'if n.startswith('X')else'F'+n[1:])
                places[n]=dest
            elif kind=='CLEAR':del places[n]
        assert suffix=={f'X{i}'for i in range(111)}|{f'Y{i}'for i in range(111)}
        assert all(1<=d<=7 and c>=0 for d,c in profile.items());mandatory=dict(profile);mandatory[1]+=84
        lower=m.moment(mandatory);excess=(lower[0]-ceiling[1],lower[1]-ceiling[0]);assert excess[0]>0
        cases.append({'source':name,'word_sha256':pin,'global_bank_rank':rank,'verified_binary_duals':duals_checked,'geometric_rank_histogram':{'7':39,'6':1},'native_departures':79,'owned_ascents':75,'independent_required_descents':9,'future_owned_moves':84,'Q0_profile':dict(profile),'mandatory_profile':mandatory,'target_excess':record(excess)})
    result={'status':'PASS_INDEPENDENT_FANOUT_DUALS_AND_84_MOVE_GATES','native_sha256':digest(native),'geometry_sha256':GEO,'arithmetic_sha256':ARITH,'fanout_candidate_sha256':digest(a.fanout),'pair_candidate_sha256':digest(a.pair_certificate),'nine_certificate_sha256':digest(a.nine_certificate),'verified_duals_total':total_duals,'cases':cases,'scope':'Linear, monotone public continuation; all descending X payloads in each declared actual-source-specific bank. All-field/block dual argument in written review; nine descents use the independently reviewed transcript theorem.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],total_duals,'duals')
if __name__=='__main__':main()
