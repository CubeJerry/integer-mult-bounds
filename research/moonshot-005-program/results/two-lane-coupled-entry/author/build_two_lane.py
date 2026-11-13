#!/usr/bin/env python3
"""Four outside entries, two early Y lanes, and one real packet detour."""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(q,m):
    if not q:raise ValueError(m)
def inverse(A):
    n=len(A);B=[list(r)+[F(i==j) for j in range(n)] for i,r in enumerate(A)]
    for k in range(n):
        z=next(i for i in range(k,n) if B[i][k]);B[k],B[z]=B[z],B[k];c=B[k][k];B[k]=[x/c for x in B[k]]
        for i in range(n):
            if i!=k:
                c=B[i][k];B[i]=[x-c*y for x,y in zip(B[i],B[k])]
    return [r[n:] for r in B]
def mm(A,B):return [[sum(x*B[k][j] for k,x in enumerate(row)) for j in range(len(B[0]))] for row in A]

def main(a):
    ep=HERE/'source-evidence/extract_rail.py';need(sha(ep.read_bytes())=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372','exact source engine')
    sp=importlib.util.spec_from_file_location('two_lane_exact',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
    qb=(HERE/'source-evidence/rail-consumer.json.gz').read_bytes();need(sha(qb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','exact parent Q')
    q=json.loads(gzip.decompress(qb));sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(sha(sb)==e.SOURCE_PIN,'native pin');s=json.loads(gzip.decompress(sb));roles={int(k):v for k,v in q['source_role_map'].items()}
    sys.path.insert(0,str(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/review-star'));from engine import root9,rank
    U=[17,19,30,38,40,47,52,60];S=[17,19,38,40];roots={i:root9(s['frames'][s['initial'][i]][0]) for i in s['live']};G=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))/2
    GS=[[G(i,j) for j in S] for i in S];I4=[[F(i==j) for j in range(4)] for i in range(4)];C=inverse([[I4[i][j]+GS[i][j] for j in range(4)] for i in range(4)]);R=mm([[GS[i][j]-I4[i][j] for j in range(4)] for i in range(4)],C)
    oldentry=[];prefix=[]
    for j in U:
        L=s['initial'][j];block=[['INIT',400,3],['ADD',400,roles[j+112],'1',3],['MOVE',400,3,L,True],['ADD',roles[j],400,'-1',L],['CLEAR',400,L]];oldentry+=block
        if j not in S:prefix+=copy.deepcopy(block)
    need(q['program'][:40]==oldentry,'exact old eight-entry convention')
    for i,j in enumerate(S):prefix.extend([['INIT',400+i,3],['ADD',400+i,roles[j+112],'1',3]])
    for i,j in enumerate(S):
        prefix.append(['ADD',roles[j+112],400+i,'-1',3])
        for k,c in enumerate(C[i]):
            if c:prefix.append(['ADD',roles[j+112],400+k,str(c),3])
    prefix.extend([['CLEAR',400+i,3] for i in range(4)])
    frames=copy.deepcopy(q['frames']);spaces=list(map(e.span,frames));decl=[]
    def chart(V,label):
        V=frozenset(V)
        if V in spaces:return spaces.index(V)
        b=[];z={0}
        for v in sorted(V):
            if v not in z:b.append(v);z|={x^v for x in tuple(z)}
        need(frozenset(z)==V,'actual chart span');idx=len(frames);frames.append(b);spaces.append(V);decl.append({'index':idx,'frame':b,'meaning':label});return idx
    EA=chart(e.span([s['frames'][s['initial'][j]][0] for j in [17,38]]),'X17/38 pair');EB=chart(e.span([s['frames'][s['initial'][j]][0] for j in [19,40]]),'X19/40 pair');L=chart(spaces[EA]&spaces[EB],'shared even line51')
    CA=chart(spaces[s['final'][129]]&spaces[s['final'][150]],'Y17/38 reunion');CB=chart(spaces[s['final'][131]]&spaces[s['final'][152]],'Y19/40 reunion')
    need(len(spaces[EA])==len(spaces[EB])==4 and spaces[L]==frozenset([0,51]) and len(spaces[CA])==len(spaces[CB])==128,'exact pair/line/reunion geometry')
    need(spaces[EB]<spaces[CA] and spaces[EA]<spaces[CB],'actual early lanes below late reunions')
    prefix.extend([['ADD',roles[129],roles[150],'-1',3],['SCALE',roles[131],'-1',3],['ADD',roles[131],roles[152],'1',3]])
    xchart={17:EA,38:EA,19:EB,40:EB};replace={};first_moves={}
    for j in S:
        x=roles[j];k=next(k for k,o in enumerate(q['program']) if o[0]=='MOVE' and o[1]==x);o=q['program'][k]
        need(o[2]==s['initial'][j] and len(spaces[o[3]])==64 and spaces[xchart[j]]<spaces[o[3]],'pair chart below genuine old first donor6')
        need(not any(z[1]==x or z[0] in ['ADD','COPY'] and z[2]==x for z in q['program'][40:k]),'no skipped early donor read')
        prefix.append(['MOVE',x,o[2],xchart[j],False]);replace[k]=['MOVE',x,xchart[j],o[3],False];first_moves[j]=k
    prefix.extend([['MOVE',roles[131],3,EA,False],['MOVE',roles[129],3,EB,False],['ADD',roles[17],roles[131],'-1/2',EA],['ADD',roles[38],roles[131],'1/2',EA],['ADD',roles[19],roles[129],'1/2',EB],['ADD',roles[40],roles[129],'-1/2',EB]])
    # Rewrite the eight literal packet lifetimes by an invertible basis change.
    live=s['live'];xs=[roles[j] for j in live];ys=[roles[j+112] for j in live];pos={j:k for k,j in enumerate(live)}
    packets=[];alpha=[];beta=[[F(0)]*8 for _ in live]
    for k,o in enumerate(q['program']):
        if o==['INIT',451,127]:
            z=next(z for z in range(k+1,len(q['program'])) if q['program'][z]==['CLEAR',451,3]);mv=next(z for z in range(k+1,z) if q['program'][z][0]=='MOVE')
            need(q['program'][mv]==['MOVE',451,127,3,True],'literal original packet down')
            left=q['program'][k+1:mv];right=q['program'][mv+1:z]
            need(all(t[0]=='ADD' and t[1]==451 and t[2] in xs and t[4]==127 for t in left),'packet actual Hub X acquisition')
            need(all(t[0]=='ADD' and t[1] in ys and t[2]==451 and t[4]==3 for t in right),'packet actual first-Y reads at0')
            ar=[F(0)]*len(live)
            for t in left:ar[xs.index(t[2])]+=F(t[3])
            n=len(packets)
            for t in right:beta[ys.index(t[1])][n]+=F(t[3])
            packets.append((k,z+1));alpha.append(ar)
    need(len(packets)==8 and all(packets[k][1]==packets[k+1][0] for k in range(7)),'eight contiguous genuine packet lifetimes')
    r=[a-b for a,b in zip(beta[pos[17]],beta[pos[38]])];rq=[-a+b for a,b in zip(beta[pos[19]],beta[pos[40]])]
    need(rq==[-x for x in r] and any(r),'one common opposite lane update')
    pivot=next(k for k,c in enumerate(r) if c);T=[r]+[[F(i==j) for j in range(8)] for i in range(8) if i!=pivot];Ti=inverse(T);ap=mm(T,alpha);bp=mm(beta,Ti)
    need(mm(bp,ap)==mm(beta,alpha),'global packet operator exactly preserved')
    need([bp[pos[17]][k]-bp[pos[38]][k] for k in range(8)]==[F(1)]+[F(0)]*7,'p update only h')
    need([-bp[pos[19]][k]+bp[pos[40]][k] for k in range(8)]==[F(-1)]+[F(0)]*7,'q update only minus h')
    newpackets=[]
    for k in range(8):
        pp=[['INIT',451,127]]+[['ADD',451,xs[j],str(c),127] for j,c in enumerate(ap[k]) if c]
        if k==0:pp.extend([['MOVE',451,127,EA,True],['ADD',roles[131],451,'-1',EA],['MOVE',451,EA,L,True],['MOVE',451,L,EB,True],['ADD',roles[129],451,'1',EB],['MOVE',451,EB,3,True]])
        else:pp.append(['MOVE',451,127,3,True])
        pp.extend([['ADD',ys[j],451,str(bp[j][k]),3] for j in range(len(live)) if live[j] not in [17,19] and bp[j][k]])
        pp.append(['CLEAR',451,3]);newpackets.extend(pp)
    # Both raw lanes reunite only with their own pair partner, at a chart
    # contained in both final facets. No original output chart is reset.
    late=[['MOVE',roles[129],EB,CA,False],['MOVE',roles[150],3,CA,False],['ADD',roles[129],roles[150],'1',CA],['MOVE',roles[129],CA,s['final'][129],False],['MOVE',roles[150],CA,s['final'][150],False],['MOVE',roles[131],EA,CB,False],['MOVE',roles[152],3,CB,False],['SCALE',roles[131],'-1',CB],['ADD',roles[131],roles[152],'1',CB],['MOVE',roles[131],CB,s['final'][131],False],['MOVE',roles[152],CB,s['final'][152],False]]
    ymove={}
    for j in S:
        y=roles[j+112];uses=[(k,o) for k,o in enumerate(q['program'][40:],40) if o[1]==y or o[0] in ['ADD','COPY'] and o[2]==y]
        outside=[(k,o) for k,o in uses if not any(b<=k<z for b,z in packets)]
        need(len(outside)==1 and outside[0][1]==['MOVE',y,3,s['final'][j+112],False],'no unaccounted lane/partner uses after entry')
        ymove[j]=outside[0][0]
    ops=copy.deepcopy(prefix);index={};k=40
    while k<len(q['program']):
        index[k]=len(ops)
        if k==packets[0][0]:ops.extend(newpackets);k=packets[-1][1];ops.extend(late);continue
        if k not in ymove.values():ops.append(copy.deepcopy(replace.get(k,q['program'][k])))
        k+=1
    index[len(q['program'])]=len(ops)
    w=copy.deepcopy(q);w['frames']=frames;w['program']=ops;w['schema']='moonshot-S010-two-early-lanes-four-entries-v1';w['parent_rail_sha256']=sha(qb)
    for field in ['begin','end']:w['consumer'][field]=index[q['consumer'][field]]
    for t,old in zip(w['consumer']['lifetimes'],q['consumer']['lifetimes']):
        for field in ['begin','end']:t[field]=index[old[field]]
    w['two_lane']={'S':S,'outside_coupled_entries':[j for j in U if j not in S],'physical_c_matrix':C,'entry_X_change_matrix':R,'pair_charts':{'EA':EA,'EB':EB,'line':L,'CA':CA,'CB':CB},'new_charts':decl,'original_first_X_moves':first_moves,'forward_packet_basis':T,'forward_packet_basis_inverse':Ti,'prefix_end':len(prefix),'global_packet_begin':index[packets[0][0]],'scope':'Actual preconditioner and packet timing only. Hosted/coupled cross actions and reverse observations are not supplied.'}
    basis={i:{i:F(1)} for i in range(400)};before,bl,oldbill=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,basis);after,al,bill=e.run(ops,w['initial'],400,w['owned_fields'],spaces,basis)
    sub=copy.deepcopy(basis)
    for i,j in enumerate(S):
        sub[roles[j+112]]={roles[h+112]:C[i][k] for k,h in enumerate(S) if C[i][k]}
        sub[roles[j]]={roles[j]:F(1)}
        for k,h in enumerate(S):sub[roles[j]]=e.plus(sub[roles[j]],{roles[h+112]:F(1)},R[i][k]+C[i][k])
    expected,el,_=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,sub)
    need(after==expected and al==el==bl,'all400 coefficients and final charts equal the invertible parent precomposition')
    for i,j in enumerate(S):
        want={roles[j]:F(1)}
        for k,h in enumerate(S):want=e.plus(want,{roles[h+112]:F(1)},R[i][k])
        need(after[roles[j]]==want,'actual new coupled a=x+(G-I)C*y')
    host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
    for x,y in host.values():need(after[roles[x]]==before[roles[x]] and after[roles[y]]==before[roles[y]],'all hosted B/D rows unchanged')
    ideal=lambda i:{roles[i]:F(1,2) if i in U else F(1),roles[i+112]:F(1,2) if i in U else F(1)}
    oldH={};errors={}
    for i in live:
        olderr=e.plus(before[roles[i+112]],ideal(i),-1);errors[i]=e.plus(after[roles[i+112]],ideal(i),-1);oldH[i]={j:olderr.get(roles[j],F(0)) for j in live if olderr.get(roles[j],F(0))};rebuilt={}
        for j,c in oldH[i].items():
            av={roles[j]:F(1)}
            if j in S:
                for k,h in enumerate(S):av=e.plus(av,{roles[h+112]:F(1)},R[S.index(j)][k])
            elif j in U:av=e.plus(av,{roles[j+112]:F(1)},-1)
            rebuilt=e.plus(rebuilt,av,c)
        need(rebuilt==errors[i],'actual forward debt remains H times actual new a')
    need(sum(map(len,oldH.values()))==4569,'4569 unchanged forward coefficients in actual a basis')
    rev=[e.plus(after[roles[x]],{roles[x]:F(1),roles[y]:F(-1)},-1) for x,y in host.values()];crev=[e.plus(after[roles[j]],{roles[j]:F(1),roles[j+112]:F(-1)},-1) for j in U]
    hrank=rank([[r.get(k,F(0)) for k in range(400)] for r in rev]);crank=rank([[r.get(k,F(0)) for k in range(400)] for r in crev]);jrank=rank([[r.get(k,F(0)) for k in range(400)] for r in rev+crev]);need((hrank,crank,jrank)==(58,3,61),'exact hosted58/coupled3/joint61 residual ranks')
    dm={k:bill['moves'].get(k,0)-oldbill['moves'].get(k,0) for k in bill['moves'].keys()|oldbill['moves'].keys()};dm={k:v for k,v in dm.items() if v};need(dm=={1:6,2:3,4:4,5:-2,7:3,8:-4,9:-1},'complete raw/owned movement invoice')
    need(bill['lifetimes']==oldbill['lifetimes']==402 and bill['peak']==29,'four snapshots replace exactly four entry lifetimes, peak29')
    controls=[]
    for kind in ['miss_physical_half','wrong_lane_sign','miss_late_inverse']:
        z=copy.deepcopy(w)
        if kind=='miss_physical_half':ix=next(k for k,o in enumerate(z['program']) if o[0]=='ADD' and o[1]==roles[17] and o[2]==roles[131]);z['program'][ix][3]='-1'
        elif kind=='wrong_lane_sign':ix=next(k for k,o in enumerate(z['program']) if o==['ADD',roles[131],451,'-1',EA]);z['program'][ix][3]='1'
        else:ix=next(k for k,o in enumerate(z['program']) if o==['SCALE',roles[131],'-1',CB]);z['program'][ix][2]='1'
        rr,rl,_=e.run(z['program'],w['initial'],400,w['owned_fields'],spaces,basis);need(rr!=after,'semantic negative control rejected '+kind);controls.append({'name':kind,'event':ix,'rejected':True})
    oldpairs={(o[2],o[3]) for o in q['program'] if o[0]=='MOVE'};newpairs={(o[2],o[3]) for o in ops if o[0]=='MOVE'};pairs=sorted(newpairs-oldpairs)
    den=sorted({F(o[3] if o[0] in ['ADD','COPY'] else o[2]).denominator for o in ops if o[0] in ['ADD','COPY','SCALE']})
    w['scope']='Actual partial400-input two-lane preconditioner. Four outside entries remain; reverse rank61 and all4569 forward coefficients remain owed. No complete supplier.'
    payload=(json.dumps(e.clean(w),sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0);a.output.mkdir(parents=True,exist_ok=True);(a.output/'rail-two-lane.json.gz').write_bytes(blob)
    result={'status':'PASS_ACTUAL_TWO_LANE_PRECONDITIONER','native_sha256':e.SOURCE_PIN,'parent_rail_sha256':sha(qb),'word_sha256':sha(blob),'payload_sha256':sha(payload),'input_directions':400,'bill':bill,'ordinary_increment':{k:bill['counts'].get(k,0)-oldbill['counts'].get(k,0) for k in bill['counts'].keys()|oldbill['counts'].keys()},'paid_move_increment':dm,'new_charts':decl,'new_chart_pairs':pairs,'packet_basis':T,'packet_basis_inverse':Ti,'pair_charts':w['two_lane']['pair_charts'],'first_X_move_events':first_moves,'scalar_denominators':den,'forward_residual_a_basis':4569,'new_forward_residual_original_inputs':sum(map(len,errors.values())),'hosted_reverse_rank':hrank,'coupled_reverse_rank':crank,'joint_reverse_rank':jrank,'completed_coupled_reverse_ports':[j for j,row in zip(U,crev) if not row],'negative_controls':controls,'scope':w['scope']+' Hosted/coupled cross acquisitions, mixed reverse observations, compiler precision and both strict suppliers remain open.'}
    (a.output/'RESULT.json').write_text(json.dumps(e.clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps(e.clean({k:result[k] for k in ['status','word_sha256','bill','ordinary_increment','paid_move_increment','scalar_denominators','new_forward_residual_original_inputs','hosted_reverse_rank','coupled_reverse_rank','joint_reverse_rank']}),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
