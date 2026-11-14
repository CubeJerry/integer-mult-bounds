#!/usr/bin/env python3
"""Independent dense400-input and native-chart review of the paired parity-half layer."""
import argparse,copy,gzip,hashlib,importlib.util,json,math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)
def read(p,pin):
    b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==pin,'source bytes '+p.name);return json.loads(gzip.decompress(b))
def rank(A):
    basis={}
    for row in A:
        v=list(row)
        for p,b in sorted(basis.items()):
            if v[p]:
                x,y=v[p],b[p];v=[y*a-x*c for a,c in zip(v,b)];g=math.gcd(*v)
                if g>1:v=[x//g for x in v]
        p=next((p for p,v in enumerate(v) if v),None)
        if p is not None:basis[p]=v
    return len(basis)
def main(a):
    ep='c4389c80322c875c4739af6ee558619f01da6112682c565e4f638a01750e5ec1';need(hashlib.sha256(a.engine.read_bytes()).hexdigest()==ep,'independent engine pin')
    spec=importlib.util.spec_from_file_location('dense400',a.engine);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
    n=read(a.native,'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883');p=read(a.parent,'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc')
    wp='f72c890e06437c3b6a177c71019f56e60f30712e5c09c1e241c893c1f180e42d';w=read(a.word,wp)
    need(w['initial']==p['initial'] and w['source_role_map']==p['source_role_map'] and w['public']==400 and w['owned_fields']==120,'exact source interface')
    roles={int(k):v for k,v in p['source_role_map'].items()};ports=n['live'];X={h:roles[h] for h in ports};Y={h:roles[h+112] for h in ports};H={n['live'][k]:(roles[b],roles[d]) for k,b,d in zip(n['hosted']['Dports'],n['hosted']['X2'],n['hosted']['Y2'])};U=set(ports)-set(H)
    def root(v):
        on=[i for i in range(9) if v>>i&1]
        if len(on)==3:return [3*int(i in on)-1 for i in range(9)]
        off=[i for i in range(9) if i not in on];need(len(off)==2,'actual E8 normal');return [3*(int(i==off[0])-int(i==off[1])) for i in range(9)]
    vv={h:n['frames'][n['initial'][h]][0] for h in ports};roots={h:root(vv[h]) for h in ports};frame=w['parity_compiler']['omitted_frame'];froot=[root(v) for v in frame]
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    need(frame==[7,25,42,52,76,82,97,127] and not(set(frame)&set(vv.values())),'omitted frame actual source support')
    need(all(dot(froot[i],froot[j])==18*int(i==j) for i in range(8) for j in range(8)),'orthogonal frame')
    g={h:[F(dot(roots[h],f),18) for f in froot] for h in ports};G={(h,j):F(dot(roots[h],roots[j]),18) for h in ports for j in ports}
    need(all(sum(x*y for x,y in zip(g[h],g[j]))==G[h,j] for h in ports for j in ports),'all104 by104 Gram factorization')
    spaces=list(map(e.span,w['frames']));groups=w['parity_compiler']['groups'];m=w['parity_compiler']['markers'];lines=w['parity_compiler']['lines'];cap={}
    halves=w['parity_compiler']['halves'];anchors={int(k):int(v) for k,v in w['parity_compiler']['anchors'].items()}
    for z in groups:cap[z['markers']['D_restored_C3']-1]=('D:'+str(z['C3']),[H[h][1] for h in z['hosted']])
    for z in halves:cap[z['markers']['compiler_cache_ready']-1]=('cache:'+str(z['index']),[408+ports.index(h) for h in z['ports']])
    cap[m['compiler_end']-1]=('localB',[b for b,d in H.values()])
    cap[m['D_waiting_at_C6']-1]=('allD',list(range(400,408))+[d for b,d in H.values()])
    cap[m['forward_modes_ready']-1]=('forward',list(range(400,408))+list(range(512,520)))
    rr,den,loc,bill,snap=e.run(w,spaces,capture_after=cap)
    need(all(loc[roles[j]]==n['final'][j] and spaces[loc[roles[j]]]==e.span(n['frames'][n['final'][j]]) for j in roles),'all400 literal native final charts')
    need(all(w['initial'][roles[j]]==n['initial'][j] and spaces[w['initial'][roles[j]]]==e.span(n['frames'][n['initial'][j]]) for j in roles),'all400 literal native initial charts')
    def current(h):
        v=[F(0)]*400;v[X[h]]=1
        if h in U:v[Y[h]]=-1
        return v
    cls={h:tuple(i for i,x in enumerate(g[h]) if x) for h in ports};cross={(h,j):G[h,j] if cls[h]!=cls[j] else F(0) for h in ports for j in ports}
    aa={h:current(h) for h in ports};want={i:[F(i==j) for j in range(400)] for i in range(400)}
    for h in ports:
        want[X[h]]=aa[h];c=F(1,2) if h in U else F(1)
        for j in ports:
            if h==j or cross[h,j]:want[Y[h]]=[x+c*(int(h==j)+cross[h,j])*y for x,y in zip(want[Y[h]],aa[j])]
    for h,(b,d) in H.items():
        for j,(bj,dj) in H.items():want[b][dj]-=int(h==j)+cross[h,j]
    need(all(rr[i]==[den*x for x in want[i]] for i in range(400)),'all160000 exact original-input coefficients')
    need(rank(rr.values())==400,'all400 independent inputs retained')
    for z in groups:
        C=z['C3'];need(len(spaces[C])==8 and all(spaces[lines[i]]<spaces[C] for i in z['modes']),'proper common C3 containing actual mode lines')
        need(all(spaces[C]<spaces[loc[Y[h]]] for h in z['ports']),'C3 below every actual class facet')
        key='D:'+str(C)
        if key in snap:
            dd,rows,ll=snap[key];need(all(rows[d]==[dd*int(k==d) for k in range(400)] and ll[d]==C for d in [H[h][1] for h in z['hosted']]),'original D restored at common chart')
    dd,rows,ll=snap['allD']
    for d in [d for b,d in H.values()]:need(rows[d]==[dd*int(k==d) for k in range(400)],'all original D restored before compiler')
    for i in range(8):
        v=[F(0)]*400
        for h,(b,d) in H.items():v[d]=g[h][i]
        need(rows[400+i]==[dd*x for x in v] and ll[400+i]==lines[i],'actual pure reverse Gram sum at omitted line')
    dd,rows,ll=snap['forward']
    for i in range(8):
        v=[sum(g[h][i]*aa[h][j] for h in ports) for j in range(400)]
        need(rows[400+i]==[dd*x for x in v] and ll[400+i]==lines[i],'actual full current-a forward Gram sum including coupled Y')
        z=halves[next(k for k,j in anchors.items() if j==i)]
        need(rows[512+i]==[dd*x for x in v] and ll[512+i]==z['C3'],'actual equal forward anchor cache at assigned common C3')
    need(len(halves)==28 and Counter(len(z['ports']) for z in halves)=={4:20,3:8},'complete parity half partition')
    need(set(anchors)=={z['index'] for z in halves if len(z['ports'])==3} and set(anchors.values())==set(range(8)),'eight distinct required anchors')
    for z in halves:
        hh=z['ports'];opp=halves[z['opposite']]['ports'];C=z['C6'];CC=z['C3'];mi=z['modes'];my=[[F(x) for x in row] for row in z['M_Y']]
        need(len(spaces[C])==64 and spaces[CC]<spaces[C],'actual six-dimensional receiver chart')
        need(all(spaces[C]<spaces[loc[Y[h]]] for h in hh),'all actual target facets contain receiver chart')
        need([h for h in ports if vv[h] in spaces[C]]==sorted(opp),'complete source incidence: exactly the opposite parity half')
        need(all(G[h,j]==int(h==j) for h in hh for j in hh),'real orthogonality of each parity half')
        need(rank([[int(4*x) for x in row] for row in my])==len(hh),'every literal weighted Y codec invertible')
        need(my==[[g[h][i]*(F(1,2) if h in U else F(1)) for h in hh] for i in z['basis_modes']],'actual weighted current-a decoding rows')
        if z['anchor'] is not None:
            co=list(map(F,z['anchor_coefficients']));i=z['anchor']
            need(i in mi and all(abs(c)==1 for c in co),'actual anchor support and exact signs')
            need(all(sum(co[a]*my[a][j] for a in range(3))==g[h][i]*(F(1,2) if h in U else F(1)) for j,h in enumerate(hh)),'missing fourth mode reconstructed from three actual rows')
        dd,cr,cl=snap['cache:'+str(z['index'])]
        for h in hh:
            i=408+ports.index(h);c=F(1,2) if h in U else F(1)
            vvrow=[-c*sum(G[h,j]*aa[j][k] for j in opp) for k in range(400)]
            need(cr[i]==[dd*x for x in vvrow] and cl[i]==C,'all104 actual correction caches have declared independent-input values')
    dd,br,bl=snap['localB'];halfof={h:z for z in halves for h in z['ports']}
    for h,(b,d) in H.items():
        vvrow=[F(k==b) for k in range(400)]
        for j in halves[halfof[h]['opposite']]['hosted']:vvrow[H[j][1]]+=G[h,j]
        need(br[b]==[dd*x for x in vvrow],'all actual local hosted corrections have the transpose sign')
    Q=[[int(2*g[h][i]) if cls[h]==tuple(z['modes']) else 0 for h in H] for z in groups for i in z['modes']]
    E=[[int(i==j) for z in groups for j in z['modes']] for i in range(8)]
    need(rank(Q)==56 and all(sum(E[i][k]*E[j][k] for k in range(56))==7*int(i==j) for i in range(8) for j in range(8)),'surjective56-mode class map and E Etranspose=7I')
    J=[[sum(E[k][i]*E[k][j] for k in range(8))-int(i==j) for j in range(56)] for i in range(56)]
    need(rank(J)==56,'class coupling invertible in characteristic zero')
    JQ=[[sum(J[i][k]*Q[k][j] for k in range(56)) for j in range(96)] for i in range(56)]
    need(all(sum(Q[k][i]*JQ[k][j] for k in range(56))==4*cross[h,l] for i,h in enumerate(H) for j,l in enumerate(H)),'all9216 entries of structural rank56 factorization')
    need(rank([[int(18*cross[h,j]) for j in H] for h in H])==56,'exact hosted residual rank56')
    need(sum(bool(v) for v in cross.values())==4608,'exact current-a residual debt')
    need(all(rr[b][dj]+rr[Y[j]][X[h]]==0 for h,(b,d) in H.items() for j,(bj,dj) in H.items()),'all9216 hosted transpose cancellations')
    raw=Counter();owned=Counter()
    for o in w['program']:
        if o[0]=='MOVE':(owned if o[4] else raw)[abs(len(w['frames'][o[3]])-len(w['frames'][o[2]]))]+=1
    need(dict(raw)=={1:160,2:280,3:360,5:280} and dict(owned)=={1:8,2:8,6:8,8:8} and bill['lifetimes']==136 and bill['peak']==120,'full actual movement and owned invoice')
    controls=[]
    halves=w['parity_compiler']['halves'];ev=w['parity_compiler']['events']
    indices=[('missing_D_restore',groups[0]['markers']['D_restored_C3']-1),('missing_Y_restore',halves[0]['markers']['Y_decode_end']-1),('wrong_entry_Y_sign',3),('wrong_forward_read',ev['forward_reads'][0]),('wrong_anchor_read',ev['anchor_reads'][0]),('wrong_correction_read',ev['correction_reads'][0]),('wrong_reverse_read',ev['reverse_moves'][0]+1)]
    for label,t in indices:
        bad=copy.deepcopy(w);o=bad['program'][t]
        if o[0]=='ADD':o[3]='0' if label.startswith('missing') else str(-F(o[3]))
        elif o[0]=='SCALE':o[2]='1'
        else:raise ValueError('chosen control not algebraic')
        r,d,l,b,s=e.run(bad,spaces);need(any(r[i]!=[d*x for x in want[i]] for i in range(400)),'negative control rejected: '+label);controls.append(label)
    out=dict(status='PASS_INDEPENDENT_ACTUAL_PARITY_HALF_COMPILER',word_sha256=wp,independent_engine_sha256=ep,all_original_coefficients=160000,full_rank=400,hosted_transpose_entries=9216,all_native_endpoint_charts=400,exact_Gram_entries=10816,actual_half_charts=28,actual_correction_caches=104,actual_forward_anchors=8,structural_class_factor_rank=56,structural_coupling_rank=56,reverse_residual_rank=56,current_a_debt=4608,bill=bill,raw_profile=dict(raw),owned_profile=dict(owned),negative_controls=controls,scope='An actual paired parity-half layer with all D restored; all within-class offdiagonals removed. Cross-class residual remains and no new complete supplier is proved.',new_kappa=None)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'bill':bill,'controls':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ['engine','native','parent','word','output']:p.add_argument('--'+k,type=Path,required=True)
    main(p.parse_args())
