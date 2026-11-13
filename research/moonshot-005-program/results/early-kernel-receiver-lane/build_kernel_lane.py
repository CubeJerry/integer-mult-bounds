#!/usr/bin/env python3
"""Early coupled-Y null lane and actual late decoder on the full current Q."""
import argparse,copy,gzip,hashlib,importlib.util,json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def main(a):
    ep=HERE/'source-evidence/extract_rail.py';need(sha(ep.read_bytes())=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372','exact replay engine')
    spec=importlib.util.spec_from_file_location('kernel_lane_exact',ep);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
    qb=(HERE/'source-evidence/rail-consumer.json.gz').read_bytes();need(sha(qb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','exact current Q')
    q=json.loads(gzip.decompress(qb));sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(sha(sb)==e.SOURCE_PIN,'native pin');s=json.loads(gzip.decompress(sb))
    roles={int(k):v for k,v in q['source_role_map'].items()};U=[17,19,30,38,40,47,52,60];R=[17,19,38,40];pivot=roles[129];yr={j:roles[j+112] for j in R}
    entry=[]
    for j in U:
        x,y=roles[j],roles[j+112];L=s['initial'][j]
        entry.extend([['INIT',400,3],['ADD',400,y,'1',3],['MOVE',400,3,L,True],['ADD',x,400,'-1',L],['CLEAR',400,L]])
    need(q['program'][:40]==entry,'all8 entry preconditions retained before Y encoding')
    spaces=list(map(e.span,q['frames']));C=frozenset.intersection(*(spaces[s['final'][j+112]] for j in R));need(len(C)==64,'actual common6-space')
    frame=[];sp={0}
    for v in sorted(C):
        if v not in sp:frame.append(v);sp|={x^v for x in tuple(sp)}
    need(frozenset(sp)==C and len(frame)==6,'exact new chart frame')
    ci=len(q['frames']);frames=q['frames']+[frame];spaces.append(C);temp=400+q['owned_fields']
    direct={}
    for j in R:
        hit=[k for k,o in enumerate(q['program']) if o[0]=='MOVE' and o[1]==yr[j]]
        need(len(hit)==1 and q['program'][hit[0]]==['MOVE',yr[j],3,s['final'][j+112],False],'true original direct coupled-Y path');direct[j]=hit[0]
    packets=[];drop=set(direct.values())
    for k,o in enumerate(q['program']):
        if o[0]!='MOVE' or o[2:4]!=[127,3]:continue
        r=o[1];end=next(t for t in range(k+1,len(q['program'])) if q['program'][t][:2]==['CLEAR',r]);coeff={j:F(0) for j in R};hits=[]
        for t,z in enumerate(q['program'][k+1:end],k+1):
            if z[0]=='ADD' and z[2]==r and z[1] in yr.values():
                j=next(j for j in R if yr[j]==z[1]);coeff[j]+=F(z[3])
                if j==17:hits.append(t)
        need(coeff[17]-coeff[19]-coeff[38]+coeff[40]==0 and len(hits)==1,'true packet-invariant null row')
        drop.update(hits);packets.append({'down':k,'clear':end,'dropped_pivot_add':hits[0],'coefficients':coeff})
    need(len(packets)==8 and min(direct.values())>max(p['clear'] for p in packets),'all forward packet reads precede reunion')
    for k,o in enumerate(q['program'][40:],40):
        if o[1]==pivot or o[0] in ['ADD','COPY'] and o[2]==pivot:need(k in drop,'no hidden pivot use')
    early=[['ADD',pivot,yr[19],'-1',3],['ADD',pivot,yr[38],'-1',3],['ADD',pivot,yr[40],'1',3],['MOVE',pivot,3,ci,False]]
    if a.observe:early.extend([['INIT',temp,ci],['ADD',temp,pivot,'1',ci],['MOVE',temp,ci,127,True]])
    late=[['MOVE',yr[j],3,ci,False] for j in R if j!=17]
    late.extend([['ADD',pivot,yr[19],'1',ci],['ADD',pivot,yr[38],'1',ci],['ADD',pivot,yr[40],'-1',ci]])
    late.extend([['MOVE',yr[j],ci,s['final'][j+112],False] for j in R])
    at=min(direct.values());ops=[];bounds={};lineage=[]
    for k,o in enumerate(q['program']):
        if k==40:ops.extend(early);lineage.extend([None]*len(early))
        if k==at:ops.extend(late);lineage.extend([None]*len(late))
        bounds[k]=len(ops)
        if k not in drop:ops.append(copy.deepcopy(o));lineage.append(k)
    observation_boundary=len(ops)
    if a.observe:ops.append(['CLEAR',temp,127]);lineage.append(None)
    w=copy.deepcopy(q);w.update(schema='moonshot-S010-early-coupled-null-lane-v1',program=ops,frames=frames,owned_fields=q['owned_fields']+int(a.observe),parent_rail_sha256=sha(qb),parent_event_of_output=lineage)
    w['kernel_lane']={'support_ports':R,'pivot_port':17,'pivot_field':pivot,'kernel_coefficients':[1,-1,-1,1],'chart_index':ci,'chart_frame':frame,'early_parent_boundary':40,'reunion_parent_boundary':at,'observer_field':temp if a.observe else None,'observation_boundary':observation_boundary,'dropped_parent_events':sorted(drop),'packet_checks':packets,'caller_observation':'original y17-y19-y38+y40; public lane at C6, optionally copied to Hub'}
    basis={i:{i:F(1)} for i in range(400)};before,bl,oldbill=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,basis)
    after,al,bill=e.run(w['program'],w['initial'],400,w['owned_fields'],spaces,basis)
    need(after==before and al==bl,'all400 original public rows and final charts exactly unchanged')
    nul={yr[17]:F(1),yr[19]:F(-1),yr[38]:F(-1),yr[40]:F(1)}
    er,el,_=e.run(q['program'][:40]+early[:4],q['initial'],400,q['owned_fields'],spaces,basis)
    need(er[pivot]==nul and el[pivot]==ci,'genuine original null row at early actual chart')
    if a.observe:
        host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};pr=roles[host[77][0]]
        probe=w['program'][:-1]+[['ADD',pr,temp,'1',127],['CLEAR',temp,127]]
        rr,rl,_=e.run(probe,w['initial'],400,w['owned_fields'],spaces,basis)
        need(all(rr[i]==e.plus(before[i],nul if i==pr else {}) and rl[i]==bl[i] for i in range(400)),'actual early Hub observation is pure original null Y row')
    need(bill['instructions']==5244+4*int(a.observe),'exact complete instruction count')
    need(bill['lifetimes']==oldbill['lifetimes']+int(a.observe) and bill['peak']<=30,'all actual lifetimes and peak counted')
    dm={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in bill['moves'].keys()|oldbill['moves'].keys()};dm={k:v for k,v in dm.items() if v}
    want={2:4,6:4,8:-4}
    if a.observe:want[3]=1
    need(dm==want,'all raw refinement and observer calls fully charged')
    eligible=[i for i in s['live'] if spaces[s['initial'][i]]<=C];need(not(set(eligible)&set(U)),'no coupled raw X line inside safe reunion')
    controls=[]
    for kind in ['missing_initial_null_term','missing_late_decode_term','stale_packet_add_at0']:
        z=copy.deepcopy(w)
        if kind=='missing_initial_null_term':z['program'][40][3]='0'
        elif kind=='missing_late_decode_term':ix=next(i for i,o in enumerate(z['program']) if o[0]=='ADD' and o[1]==pivot and o[4]==ci);z['program'][ix][3]='0'
        else:
            ix=bounds[packets[0]['dropped_pivot_add']];z['program'].insert(ix,['ADD',pivot,q['program'][packets[0]['dropped_pivot_add']][2],str(packets[0]['coefficients'][17]),3])
        try:rr,rl,_=e.run(z['program'],z['initial'],400,z['owned_fields'],spaces,basis);rejected=rr!=after or rl!=al;reason='all400-input endpoint map differs'
        except (AssertionError,ValueError) as ex:rejected=True;reason=str(ex)
        need(rejected,'kernel-lane negative control '+kind);controls.append({'name':kind,'rejected':True,'reason':reason})
    payload=(json.dumps(e.clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'rail-kernel.json.gz').write_bytes(blob)
    r={'status':'PASS_ACTUAL_ENCODED_COUPLED_Y_NULL_LANE','parent_rail_sha256':sha(qb),'native_sha256':e.SOURCE_PIN,'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'inputs':400,'all_public_rows_and_charts_unchanged':True,'full_forward_packet_access_preserved':True,'owned_Hub_observer':a.observe,'observer_original_row':nul if a.observe else None,'early_lane_original_row':nul,'eligible_foreign_initial_X_lines':eligible,'no_coupled_initial_X_line_reachable':True,'chart_index':ci,'chart_frame':frame,'ordinary_bill':bill,'move_increment':dm,'ordinary_increment':{k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in bill['counts'].keys()|oldbill['counts'].keys()},'negative_controls':controls,'scope':'Actual encoded forward-receiver timing interface, not coupled S implementation or entry8 removal. All old endpoint debts, coupled entry calls, strict suppliers and five foundations remain.'}
    (a.output/'RESULT.json').write_text(json.dumps(e.clean(r),sort_keys=True,indent=2)+'\n');print(json.dumps(e.clean({k:r[k] for k in ['status','word_sha256','owned_Hub_observer','ordinary_bill','ordinary_increment','move_increment']}),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--observe',action='store_true');main(p.parse_args())
