#!/usr/bin/env python3
"""Independent rational whole-source review; no author replay imported.

Reuses the previously independently authored root replay kernel, credited in
REVIEW.md. @CubeJerry with OpenAI assistance. Apache-2.0.
"""
import argparse, copy, gzip, hashlib, importlib.util, json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def rank(rows):
    basis = {}
    for original in rows:
        row = dict(original)
        for j in sorted(basis):
            if j in row:
                c = row[j]
                for k, value in basis[j].items():
                    v = row.get(k, F(0)) - c * value
                    if v: row[k] = v
                    else: row.pop(k, None)
        if row:
            j = min(row); c = row[j]
            basis[j] = {k: v / c for k, v in row.items()}
    return len(basis)

def determinant(matrix):
    a = [[F(v) for v in row] for row in matrix]; answer = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None: return F(0)
        if pivot != j: a[j], a[pivot] = a[pivot], a[j]; answer = -answer
        x = a[j][j]; answer *= x
        a[j] = [v/x for v in a[j]]
        for i in range(j+1, len(a)):
            c = a[i][j]
            a[i] = [v-c*w for v,w in zip(a[i], a[j])]
    return answer

def root_vector(bits):
    on = [i for i in range(9) if bits >> i & 1]
    if len(on) == 3: return [2 if i in on else -1 for i in range(9)]
    off = [i for i in range(9) if not (bits >> i & 1)]
    need(len(off) == 2, 'native real root type')
    return [3*(int(i == off[0])-int(i == off[1])) for i in range(9)]

from engine import replay,span,plus
from itertools import combinations

BASE=Path(__file__).resolve().parents[2]
AUTHOR=BASE/'worker-b/public-gram-bank'
REPO=BASE/'programme'

def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def comb(coef,rows):
    r={}
    for c,a in zip(coef,rows):r=plus(r,a,F(c))
    return r

def ff_data(matrix,p):
    """Fresh prime-field elimination; return an explicit right-kernel basis."""
    a=[[F(x).numerator*pow(F(x).denominator,-1,p)%p for x in row]for row in matrix]
    n=len(a[0])if a else 0;piv=[];k=0
    for j in range(n):
        z=next((i for i in range(k,len(a))if a[i][j]),None)
        if z is None:continue
        a[k],a[z]=a[z],a[k];s=pow(a[k][j],-1,p);a[k]=[s*v%p for v in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                t=a[i][j];a[i]=[(u-t*v)%p for u,v in zip(a[i],a[k])]
        piv.append(j);k+=1
        if k==len(a):break
    null=[]
    for j in range(n):
        if j in piv:continue
        x=[0]*n;x[j]=1
        for i,col in enumerate(piv):x[col]=-a[i][j]%p
        null.append(x)
    original=[[F(x).numerator*pow(F(x).denominator,-1,p)%p for x in row]for row in matrix]
    need(all(sum(x*y for x,y in zip(row,v))%p==0 for row in original for v in null),'explicit finite-field kernel certificate')
    return {'rank':k,'pivots':piv,'kernel':null}

def context(native,w):
    live=native['live'];nh={live[i]:(b,d)for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])};original=sorted(live+[h+112 for h in live]+[j for pair in nh.values()for j in pair]);role={int(k):v for k,v in w['source_role_map'].items()}
    need(role==dict(zip(original,range(len(original))))and w['public']==len(original),'all original independent main roles')
    need(w['initial']==[native['initial'][j]for j in original]and w['final']==[native['final'][j]for j in original],'exact full source interface')
    need(w['frames'][:len(native['frames'])]==native['frames'],'native ordered chart prefix')
    X={h:role[h]for h in live};Y={h:role[h+112]for h in live};H={h:(role[b],role[d])for h,(b,d)in nh.items()};U=set(live)-set(H);m=w['public_Gram_bank'];I=m['pivot_ports'];M=m['bank_modes']
    need(I==[0,7,20,27,36,46,57,111]and M==[19,30,38,40,47,52,60]and set(I)<=set(H),'actual native pivot and bank identities')
    vv={h:native['frames'][native['initial'][h]][0]for h in live};rr={h:root_vector(vv[h])for h in live};G={h:{j:F(dot(rr[h],rr[j]),18)for j in live}for h in live}
    need([[G[i][j]for j in I]for i in I]==[[F(a==b)for b in range(8)]for a in range(8)],'genuine native orthogonal frame')
    need(all(G[h][j]==sum(G[h][i]*G[i][j]for i in I)for h in live for j in live),'full104 Gram factors through actual public pivots')
    q={i:{d:G[i][h]for h,(b,d)in H.items()if G[i][h]}for i in I};r={h:plus({d:-F(1)},{dj:G[h][j]for j,(bj,dj)in H.items()if G[h][j]},1)for h,(b,d)in H.items()}
    mu={u:{d:G[u][h]for h,(b,d)in H.items()if G[u][h]}for u in M};payload={h:q[h]if h in I else r[h]for h in H}
    aa={h:plus({X[h]:F(1)},{Y[h]:F(1)},-1)if h in U else{X[h]:F(1)}for h in live};spaces=[span(f)for f in w['frames']];C=m['bank'];oldU=[17,19,30,38,40,47,52,60]
    bank={0}
    for u in oldU:bank|={x^vv[u]for x in tuple(bank)}
    need(spaces[C]==frozenset(bank)and len(bank)==128,'actual rank7 old-coupled span')
    T=m['restored_targets'];S=m['unrestored_targets'];perm={int(k):v for k,v in m['permutation'].items()};inv={v:k for k,v in perm.items()};stops={int(k):v for k,v in m['stops'].items()}
    need(set(T)=={h for h in H if vv[h]in bank}and len(T)==(20 if len(H)==96 else 28),'complete target family in actual bank')
    need(len({h for h in live if vv[h]in bank})==28 and set(I).isdisjoint(T),'pivot frame disjoint from full28 target family')
    need(set(T).isdisjoint(S)and set(T+S)==set(H)and len(S)==76,'complete hosted partition with76 unfinished D')
    for cycle in[T,S]:need(all(perm[h]==cycle[(k+1)%len(cycle)]for k,h in enumerate(cycle)),'actual public two-cycle assignment')
    need(inv=={int(k):v for k,v in m['inverse_permutation'].items()},'actual inverse carrier permutation')
    facets={h:native['final'][h+112]for h in live};finalspaces={spaces[facets[h]]for h in H}
    need(spaces[C]not in finalspaces,'bank is not any hosted final facet')
    for h in H:need(vv[perm[h]]in spaces[facets[h]],'assigned public payload line fits actual final facet')
    for h in T:
        st=stops[h];need(spaces[st]==spaces[C]&spaces[facets[h]]and len(spaces[st])==64 and vv[perm[h]]in spaces[st]and vv[h]not in spaces[st],'actual proper rank6 relay stop')
        beta=list(map(F,m['beta'][str(h)]));need([sum(beta[k]*rr[u][j]for k,u in enumerate(M))for j in range(9)]==rr[h],'exact real target reconstruction')
        need(comb(beta,[mu[u]for u in M])==plus(r[h],{H[h][1]:F(1)},1),'pure actual bank modes decode original D')
    return dict(role=role,live=live,X=X,Y=Y,H=H,U=U,I=I,M=M,G=G,q=q,r=r,mu=mu,payload=payload,aa=aa,spaces=spaces,C=C,T=T,S=S,perm=perm,inv=inv,stops=stops,facets=facets,finalspaces=finalspaces)

def audit(w,c,full=True):
    H=c['H'];I=c['I'];M=c['M'];T=c['T'];X=c['X'];Y=c['Y'];q=c['q'];r=c['r'];mu=c['mu'];payload=c['payload'];perm=c['perm'];inv=c['inv'];n=w['public'];m=w['public_Gram_bank'];ev=m['events'];marks=m['markers'];active=m['active_owner'];C=c['C']
    need(active==n+7,'one actual distinct active owner');expected={}
    for h in c['live']:expected[X[h]]=c['aa'][h];expected[Y[h]]={Y[h]:F(1)}
    for h,(b,d)in H.items():expected[b]=plus({b:F(1)},r[h],1);expected[d]={d:F(1)}if h in T else payload[perm[h]]
    decode={z['step']:z['port']for z in ev['decoded_owner']};restore={z['step']:(z['port'],z['next'])for z in ev['public_restoration']};seen=[];reads=Counter();Bports={b:h for h,(b,d)in H.items()};Dports={d:h for h,(b,d)in H.items()};pivot_reads=set(ev['pivot_correction']);qreads=set(ev['q_acquisition']);rreads=set(ev['r_acquisition']);bread=set(ev['B_reads']);mreads=set(ev['bank_acquisition'])
    first_bank_clear=next(t for t,o in enumerate(w['program'])if t>marks['relay_start']and o[:2]==['CLEAR',n]);next_service={}
    def after(t,rows,loc):
        if t==marks['all_public_q_ready']:
            need(all(rows[H[i][1]]==q[i]and loc[H[i][1]]==3 for i in I),'all public Gram pivots genuinely acquired')
            need(all(rows[d]=={d:F(1)}for h,(b,d)in H.items()if h not in I),'nonpivot D untouched during complete q formation');seen.append('q')
        if t==marks['ground_preload_and_bank_ready']:
            need(all(rows[d]==payload[h]and loc[d]==3 for h,(b,d)in H.items()),'actual public triangular q/r preload')
            need(all(rows[n+k]==mu[u]and loc[n+k]==3 for k,u in enumerate(M)),'pure bank modes acquired from retained public q');seen.append('preload')
        if t==marks['public_permutation_complete']:
            need(all(rows[d]==payload[perm[h]]and loc[d]==3 for h,(b,d)in H.items()),'actual whole public carrier permutation');seen.append('permutation')
        if t==marks['all_B_duties_complete']:
            need(all(rows[b]==expected[b]and loc[b]==127 for b,d in H.values()),'every actual B duty including eight pivot compensations');seen.append('B')
        if t==marks['relay_start']:
            need(rows[active]==r[T[0]]and loc[active]==C and all(rows[n+k]==mu[u]and loc[n+k]==C for k,u in enumerate(M)),'actual funded relay handoff');seen.append('relay')
        if t in decode:
            h=decode[t];need(rows[active]=={H[h][1]:F(1)}and loc[active]==C,'actual original D decoded at bank');seen.append(('decode',h))
        if t in restore:
            h,j=restore[t];need(j==perm[h]and rows[H[h][1]]=={H[h][1]:F(1)}and rows[active]==r[j],'actual singular swap restores public D and next r')
            need(loc[H[h][1]]==loc[active]==c['stops'][h],'actual proper cochart');seen.append(('restore',h))
        if t==marks['relay_complete']:
            need(all(rows[H[h][1]]=={H[h][1]:F(1)}and loc[H[h][1]]==c['facets'][h]for h in T),'all target D at prescribed final facets');seen.append('done')
    def hook(t,phase,o,rows,loc):
        if phase=='after':
            need(all(c['spaces'][ch]not in c['finalspaces']for owner,ch in loc.items()if owner>=n),'no owned visit to any hosted final facet');after(t,rows,loc);return
        if o[0]=='MOVE'and not o[-1]:need(c['spaces'][o[2]]<c['spaces'][o[3]],'all public moves strictly upward')
        if t in pivot_reads:
            h=Bports[o[1]];need(h in I and F(o[3])==-1 and rows[o[2]]=={H[h][1]:F(1)}and rows[H[h][1]]=={H[h][1]:F(1)}and loc[o[2]]==w['initial'][X[h]],'genuine paid original pivot-D subtraction before overwrite');reads['pivot']+=1
        if t in qreads:
            i=Dports[o[1]];j=Dports[o[2]];need(i in I and j not in I and rows[o[2]]=={H[j][1]:F(1)}and F(o[3])==c['G'][i][j],'original nonpivot D used to form q');reads['q']+=1
        if t in rreads:
            h=Dports[o[1]];i=Dports[o[2]];need(h not in I and i in I and rows[o[2]]==q[i]and F(o[3])==c['G'][h][i],'actual retained q used to form r');reads['r']+=1
        if t in mreads:
            u=M[o[1]-n];i=Dports[o[2]];need(i in I and rows[o[2]]==q[i]and F(o[3])==c['G'][u][i],'bank reads pure actual q, not new r_u');reads['mu']+=1
        if t in bread:
            h=Bports[o[1]];need(o[2]==H[inv[h]][1]and rows[o[2]]==payload[h]and F(o[3])==1 and loc[o[1]]==w['initial'][X[h]],'actual original-line B read of its assigned payload');reads['B']+=1
        if t==first_bank_clear:
            carrier=H[inv[I[0]]][1];need(rows[carrier]==q[I[0]]and loc[carrier]==w['initial'][X[I[0]]],'next-service q0 still at its actual original line')
            need(all(rows[n+k]==mu[u]and loc[n+k]==C for k,u in enumerate(M))and all(loc[b]==127 for b,d in H.values()),'seven funded bank modes and all B duties concurrently available')
            next_service.update({'cut':t,'q0_carrier':carrier,'q0_line':loc[carrier],'bank':C,'bank_payloads':7})
    rows,loc,raw,owned,counts,peak,life,tr,retire=replay(w,mode='public_pivot_review',hook=hook)
    need(rows==expected and [loc[i]for i in range(n)]==w['final'],'entire arbitrary-input public map and endpoint charts')
    need(reads['pivot']==8 and reads['B']==len(H)and len(seen)==6+2*len(T),'all required source chronology and duties')
    want_raw={1:len(H),2:len(T),5:len(T),7:76,8:304 if n==400 else 312};want_owned={1:55 if n==400 else 63,6:1,7:7}
    need(raw==want_raw and owned==want_owned and peak==8 and life==(24 if n==400 else 16),'complete funded source ledger')
    need(len(retire)==life and all(row for t,i,ch,row in retire),'all actual nonzero retirements retained')
    for o in w['program']:
        if o[0]in('ADD','SCALE'):
            v=F(o[3]if o[0]=='ADD'else o[2]);need(v.denominator&(v.denominator-1)==0,'every source coefficient dyadic')
    if not full:return True
    need(rank(list(rows.values()))==n,'complete rational input rank')
    return {'variant':m['variant'],'public_rank':n,'restored_D':len(T),'unfinished_D':76,'counts':counts,'raw':raw,'owned':owned,'Q':dict(Counter(raw)+Counter(owned)),'peak':peak,'lifetimes':life,'dirty_retirements':len(retire),'chronology_checks':len(seen),'actual_reads':dict(reads),'next_service_cut':next_service},rows,loc

def recovery(w,c,rows):
    H=c['H'];I=c['I'];T=c['T'];inv=c['inv'];G=c['G'];m=w['public_Gram_bank'];qi={i:{H[inv[i]][1]:F(1)}for i in I};formula={}
    for h,(b,d)in H.items():
        if h in I:continue
        formula[h]={d:F(1)}if h in T else plus(comb([G[h][i]for i in I],[qi[i]for i in I]),{H[inv[h]][1]:F(1)},-1)
    for i in I:formula[i]=plus(qi[i],comb([G[i][h]for h in H if h not in I],[formula[h]for h in H if h not in I]),-1)
    stored={int(h):{int(j):F(a)for j,a in v.items()}for h,v in m['final_D_abstract_inverse'].items()};need(formula==stored,'independently derived final-output dyadic inverse equals literal certificate')
    for h,(b,d)in H.items():
        value=comb(formula[h].values(),[rows[j]for j in formula[h]]);need(value=={d:F(1)},'exact final-output inverse recovers each original D')
        need(all(a.denominator&(a.denominator-1)==0 for a in formula[h].values()),'entire inverse is dyadic')
    for i in I:
        z=m['final_pivot_payload_locations'][str(i)];need(z=={'carrier_port':inv[i],'chart':w['final'][H[inv[i]][1]],'field':H[inv[i]][1]},'literal surviving public q carrier location')
    Ds=[d for b,d in H.values()];matrix=[[rows[d].get(j,F(0))for j in Ds]for d in Ds];det=determinant(matrix);need(det==-1,'exact terminal D determinant minus one')
    ranks={p:ff_data(matrix,p)['rank']for p in[3,5,7,127]};need(all(v==len(H)for v in ranks.values()),'all old residue defects repaired')
    bad=[dict(rows[d])for d in Ds]
    for i in I:bad[Ds.index(H[inv[i]][1])]=c['r'][i]
    oldrank=ff_data([[r.get(j,F(0))for j in Ds]for r in bad],3)['rank'];need(oldrank==len(H)-2,'replacing saved q by old r recreates mod3 loss')
    reverse=rank([plus(rows[b],{b:F(1),d:-F(1)},-1)for b,d in H.values()]);need(reverse==8,'actual remaining B residual is rank8 Gram')
    need(sum(rows[d]!={d:F(1)}for b,d in H.values())==76,'exact76 original D outputs remain unfinished')
    debt=sum(len(comb([F(1,2)if h in c['U']else F(1)],[c['aa'][h]]))for h in c['live']);need(debt==(112 if c['U'] else 104),'actual original-coordinate forward debt')
    return {'determinant':str(det),'inverse_rows':len(formula),'inverse_ring':'Z[1/2]','prime_D_ranks':ranks,'old_r_replacement_mod3_rank':oldrank,'reverse_residual_rank':8,'original_coordinate_forward_debt':debt,'scope':'Algebraic inverse from literal final outputs; future cochart acquisition and complete endpoint remain unpaid.'}

def source_controls(w,c):
    ev=w['public_Gram_bank']['events'];jobs=[('omit_paid_pivot_subtraction',ev['pivot_correction'][0]),('corrupt_public_q',ev['q_acquisition'][0]),('corrupt_public_r',ev['r_acquisition'][0]),('corrupt_pure_bank_mode',ev['bank_acquisition'][0]),('omit_actual_B_read',ev['B_reads'][0]),('corrupt_original_D_decode',ev['decoded_owner'][0]['step']-1),('break_singular_swap',ev['public_restoration'][0]['first_swap'])];out=[]
    for name,t in jobs:
        bad=copy.deepcopy(w);need(bad['program'][t][0]=='ADD','actual read mutation');bad['program'][t][3]='0'
        try:audit(bad,c,False)
        except (ValueError,KeyError)as e:out.append({'mutation':name,'instruction':t,'rejected_by':str(e)})
        else:raise ValueError('source mutation passed '+name)
    return out

def open_review(native,old,w):
    n=old['public'];need(n==400 and w['frames']==old['frames']and w['initial']==old['initial'],'literal retained open source interface')
    start=old['relay']['markers']['ground_preload'];removed=set(range(start,start+8));need(old['program'][start:start+8]==[['CLEAR',400+i,3]for i in range(8)],'exact deferred eight actual q retirements')
    begin=next(t for t,o in enumerate(old['program'])if t>old['relay']['markers']['all_B_reads']and o[:2]==['INIT',400]);expected=[];origins=[]
    for t,o in enumerate(old['program']):
        if t in removed:continue
        e=o.copy()
        if t>=begin:
            if e[1]==400:e[1]=415
            if e[0]=='ADD'and e[2]==400:e[2]=415
        expected.append(e);origins.append(t)
    need(w['program']==expected and w['source_program_events']==origins,'only eight CLEAR deletions and actual active lifetime rename')
    terminal={int(i):v for i,v in w['terminal_owned'].items()};need(terminal=={i:3 for i in range(400,408)}and w['owned_fields']==16,'exact eight live ground outputs and capacity16')
    rr,loc,raw,owned,counts,peak,life,tr,retire=replay(w,mode='open_public_gram_review',terminal_owned=terminal)
    oldrows,oldloc,oraw,oowned,ocount,opeak,olife,otr,oretire=replay(old,mode='old_closed')
    need({i:rr[i]for i in range(400)}==oldrows and{j:loc[j]for j in range(400)}==oldloc,'all actual public values and locations preserved')
    need(raw==oraw and owned==oowned and life==olife==24 and peak==16 and opeak==15 and len(retire)==16,'unchanged paid movements and exact open liveness')
    need([o[2:]for o in w['program']if o[0]=='MOVE']==[o[2:]for o in old['program']if o[0]=='MOVE'],'all ordered signed maps unchanged')
    roles={int(k):v for k,v in old['source_role_map'].items()};live=native['live'];H={live[i]:(roles[b],roles[d])for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])};Z=old['relay']['ground_Gram_frame'];roots={h:root_vector(native['frames'][native['initial'][h]][0])for h in live};g=[{h:F(dot(root_vector(z),roots[h]),18)for h in live}for z in Z]
    for i in range(8):need(rr[400+i]=={d:g[i][h]for h,(b,d)in H.items()if g[i][h]}and loc[400+i]==3,'all genuine original Gram values actually retained')
    T=set(old['relay']['restored_ports']);inv={v:int(k)for k,v in old['relay']['permutation'].items()};cert=w['open_preservation']['abstract_original_D_recovery']
    for h,(b,d)in H.items():
        form={d:F(1)}if h in T else plus({400+i:g[i][h]for i in range(8)if g[i][h]},{H[inv[h]][1]:F(1)},-1)
        need(form=={int(j):F(v)for j,v in cert[str(h)].items()},'independently reconstructed open inverse')
        need(comb(form.values(),[rr[j]for j in form])=={d:F(1)},'exact original D recovered from actual augmented endpoint')
    bad=copy.deepcopy(w)
    for o in bad['program']:
        if o[1]==415:o[1]=400
        if o[0]=='ADD'and o[2]==415:o[2]=400
    try:replay(bad,mode='bad_open_alias',terminal_owned=terminal)
    except ValueError as e:alias=str(e)
    else:raise ValueError('colliding retained q0/active lifetime accepted')
    return {'variant':'open-retained','public_rank_over_Q':400,'open_owned_outputs':8,'open_owned_chart':3,'peak':peak,'lifetimes':life,'actual_retirements':len(retire),'raw':raw,'owned':owned,'Q':dict(Counter(raw)+Counter(owned)),'counts':counts,'inverse_rows':96,'all_source_maps_inherited':True,'negative_control':{'unrenamed_active_owner':alias},'native_admissible':False,'scope':'Open continuation with eight extra correlated outputs; future storage, transport and closure remain real obligations.'}

def next_service(c,receipt,price):
    I=c['I'];M=c['M'];G=c['G'];basis=[[G[u][i]for i in I]for u in M]+[[F(i==I[0])for i in I]];det=determinant(basis);need(det==-F(1,16),'actual7-bank plus public q0 is a dyadic basis')
    coefs=price['reverse_continuation_basis']['actual_consumer_coefficients'];need(set(map(int,coefs))==set(c['live']),'all104 stated consumer rows')
    for h in c['live']:
        a=list(map(F,coefs[str(h)]));need(len(a)==8 and all(v.denominator&(v.denominator-1)==0 for v in a),'actual dyadic consumer coefficients')
        need([sum(a[j]*basis[j][i]for j in range(8))for i in range(8)]==[G[h][i]for i in I],'all104 genuine Gram functions reconstructed')
        if h in c['H']:
            delivered=comb(a,[c['mu'][u]for u in M]+[c['q'][I[0]]]);b,d=c['H'][h]
            need(plus(plus({b:F(1)},c['r'][h],1),delivered,-1)=={b:F(1),d:-F(1)},'source-bound shared delivery completes actual B endpoint')
    need(len(c['spaces'][c['C']])==128 and len(c['spaces'][receipt['next_service_cut']['q0_line']])==2 and len(c['spaces'][127])==512,'actual bank-to-Hub rank2 and q0-line-to-Hub rank8')
    return {'actual_cut':receipt['next_service_cut'],'basis_determinant':str(det),'consumer_rows':104,'additional_paid_profile':{2:7,8:1},'source_bound_B_service_proved':True,'extended_literal_word_emitted':False,'scope':'Existing paid seven bank modes extend to Hub; actual public q0 is copied at its line before final ascent. Forward and76 D restorations remain open.'}

def phase_review(w,parent,path):
    need(w['frames'][:len(parent['frames'])]==parent['frames'],'phase parent exact chart prefix')
    inherited={(o[2],o[3])for o in parent['program']if o[0]=='MOVE'};used={(o[2],o[3])for o in w['program']if o[0]=='MOVE'};new=used-inherited
    data=load(path);recs=data['recipes'];need({(r['source'],r['target'])for r in recs}==new and len(recs)==len(new),'all and only introduced ordered maps certified')
    engine=REPO/'research/moonshot-005-program/results/complex-omitted-line-gram/author/dependencies/native_verify.py';pin='3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38';need(hashlib.sha256(engine.read_bytes()).hexdigest()==pin,'retained independent phase interpreter')
    sp=importlib.util.spec_from_file_location('repartition_review_phase',engine);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
    for r in recs:
        a,b=r['source'],r['target'];need((r['source_frame'],r['target_frame'])==(w['frames'][a],w['frames'][b]),'actual literal recipe frames')
        need(r['rank']==r['recipe']['rank']==abs(len(w['frames'][a])-len(w['frames'][b])),'true nested rank in recipe')
        v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(w['frames'][a],9))+v.frame(w['frames'][b],9),'exact signed map')
    rejected=None
    if recs:
        r=copy.deepcopy(recs[0]);r['recipe']['left']['phase']=(r['recipe']['left']['phase']+1)%4
        try:v.equal(v.recipe(r['recipe']),v.adjoint(v.frame(r['source_frame'],9))+v.frame(r['target_frame'],9),'wrong phase')
        except ValueError:rejected=True
        else:raise ValueError('wrong phase accepted')
    return {'introduced_maps':len(new),'inherited_used_maps':len(used&inherited),'phase_mutation_rejected':rejected,'scope':'Retained-interpreter certificate reproduction; zero-new-map case inherits exact pinned parent evidence.'}

def invoices(full,native_review,receipts):
    def combine(*terms):
        out={}
        for c,d in terms:
            for k,v in d.items():out[int(k)]=out.get(int(k),F(0))+F(c)*F(v)
        return {k:v for k,v in out.items()if v}
    B=10**35;cache={}
    def bound(n):
        if n not in cache:
            N=n**199*B**200;lo=0;hi=n*B+1
            while hi-lo>1:
                a=(lo+hi)//2
                if a**200<=N:lo=a
                else:hi=a
            need(lo**200<=N<hi**200,'exact integer200th-root tariff');cache[n]=(F(lo,B),F(hi,B))
        return cache[n]
    def moment(d):
        lo=hi=F(0)
        for n,c in d.items():
            a,b=bound(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
        return lo,hi
    allhosted=next(r for r in native_review['complete_conversions']if r['variant']=='allhosted');newN=allhosted['physical']['paid'];newH=allhosted['physical']['helpers'];newT=allhosted['caller_T'];newP=allhosted['caller_P']
    service=moment({2:F(7),8:F(1)});fresh=moment({8:F(8)});out=[]
    for r in receipts:
        new=r['variant']=='allhosted';T=newT if new else full['invoice']['T'];P=newP if new else full['invoice']['P'];N=newN if new else full['native']['paid'];H=newH if new else full['native']['helpers']
        slope=combine((F(1,18),T),(-F(1,18),P));room=moment(combine((1,slope),(1,N),(-1,H),(-1,r['Q'])));penalty=moment(combine((-1,slope)))
        need(penalty[0]>0 and room[0]>0,'finite penalty and remaining limiting allowance')
        m=2
        while room[0]-penalty[1]/(m-1)<=0:m+=1
        if m>2:need(room[1]-penalty[0]/(m-2)<0,'preceding multiplicity fails exactly')
        need(m==(3 if new else 2),'first certified fixed multiplicity')
        need(fresh[0]>room[1],'separated eight full rank8 forward modes exceed entire remaining allowance')
        z={'variant':r['variant'],'limiting_room':room,'finite_m_penalty':penalty,'first_positive_fixed_m':m}
        if r['variant']!='open-retained':z['after_source_bound_B_service']=(room[0]-service[1],room[1]-service[0])
        out.append(z)
    return {'exponent':'199/200','formula':'remaining_room(m)=limiting_room-finite_m_penalty/(m-1), fixed integer m>=2','variants':out,'shared_B_service_increment':service,'eight_fresh_full_rank8_forward_modes':fresh,'separated_completion_excluded':True,'scope':'Incomplete sources only. The shared B service has no separately emitted extended word. Open owner storage/transport/closure and every remaining paired endpoint stay unpaid.'}

PINS={'PROOF.md':'9f840d32c9176762beaf2f3a3d124da6b544842187bc5d95f9ce728bdb10698a','MANIFEST.json':'a339abf1a41f52cb9158bdaa235791793bffcadbcaebd8afb47104d9680ef75b','dependencies/native-retained.json.gz':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','dependencies/native-allhosted.json.gz':'3dec380d820ed631636bdc77adb4a4c3e35abdb31d2b312f8f41edadff389d96','dependencies/old-relay-20.json.gz':'0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c','dependencies/full-receipt.json':'d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','output/retained/WORD.json.gz':'8157c7c8a2e64c179ef0ae7afab2c94bb44b69f1fc9e03c8d24096e4bfc9e540','output/allhosted/WORD.json.gz':'bf2956313fc0bbbcade57f557eac7791b771b1b46444df804704baa2c8e09b62','output/open-retained/WORD.json.gz':'35f0cdf91e5abce2d7bfb05b4af521fe4019f16d09347f288d3b31f6cc27e389'}

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v)for v in x]
    return x

def main():
    global AUTHOR,REPO
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--repo',type=Path,default=REPO);p.add_argument('--native-review',type=Path,default=BASE/'worker-c/native-repartition-review/RESULT.json');p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));p.add_argument('--skip-phases',action='store_true');a=p.parse_args();AUTHOR=a.author;REPO=a.repo
    for name,pin in PINS.items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen source pin '+name)
    np='c293166010b906749a48afb6828909b5b83a6679bfb89eece05c36d0d67fd6f9';need(hashlib.sha256(a.native_review.read_bytes()).hexdigest()==np,'independently reviewed complete changed interface')
    seedpath=REPO/'research/moonshot-005-program/results/complex-omitted-line-gram/author/output/WORD.json.gz';need(hashlib.sha256(seedpath.read_bytes()).hexdigest()=='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc','exact phase parent');seed=load(seedpath)
    price=load(AUTHOR/'output/PRICE.json');receipts=[]
    for name in['retained','allhosted']:
        n=load(AUTHOR/'dependencies'/('native-'+name+'.json.gz'));w=load(AUTHOR/'output'/name/'WORD.json.gz');c=context(n,w);r,rows,loc=audit(w,c);r['recovery']=recovery(w,c,rows);r['negative_controls']=source_controls(w,c);r['source_bound_B_service']=next_service(c,r,price)
        if not a.skip_phases:r['phase_certificates']=phase_review(w,seed,AUTHOR/'output'/name/'PHASES.json')
        receipts.append(r);print(json.dumps({'variant':name,'status':'PASS','restored':r['restored_D'],'determinant':r['recovery']['determinant'],'controls':len(r['negative_controls'])}),flush=True)
    r=open_review(load(AUTHOR/'dependencies/native-retained.json.gz'),load(AUTHOR/'dependencies/old-relay-20.json.gz'),load(AUTHOR/'output/open-retained/WORD.json.gz'));receipts.append(r);print('PASS: literal open retention and exact dyadic augmented inverse',flush=True)
    result={'status':'PASS_INDEPENDENT_PUBLIC_PIVOT_AND_OPEN_OWNER_REPAIR_REVIEW','pins':PINS,'independent_native_review_sha256':np,'variants':receipts,'invoice':invoices(load(AUTHOR/'dependencies/full-receipt.json'),load(a.native_review),receipts),'scope':'Exact closed-owned partial public repairs and a deliberately open-owned alternative. No completed paired source or new kappa.'}
    a.output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n');print('PASS: all source histories, dyadic recovery, open boundary and complete prices')

if __name__=='__main__':main()
