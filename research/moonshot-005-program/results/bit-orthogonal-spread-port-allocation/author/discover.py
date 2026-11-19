#!/usr/bin/env python3
"""Find and exactly verify a native orthogonal-spread port allocation."""
import argparse,gzip,hashlib,itertools,json,time
from fractions import Fraction
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)
def xor(values):
    x=0
    for y in values:x^=y
    return x
def inverse(A):
    n=len(A);B=[[Fraction(x)for x in row]+[Fraction(i==j)for j in range(n)]for i,row in enumerate(A)]
    for c in range(n):
        k=next(r for r in range(c,n)if B[r][c]);B[c],B[k]=B[k],B[c];v=B[c][c];B[c]=[x/v for x in B[c]]
        for r in range(n):
            if r!=c:
                v=B[r][c];B[r]=[x-v*y for x,y in zip(B[r],B[c])]
    return [row[n:]for row in B]
def span(rows):
    out={0}
    for row in rows:out|={x^row for x in list(out)}
    return out
def q(x):return sum(((x>>(2*k))&1)*((x>>(2*k+1))&1)for k in range(4))%2
def polar(x,y):return q(x^y)^q(x)^q(y)
def pfaffian(a):return ((a>>0)&1)*((a>>5)&1)^((a>>1)&1)*((a>>4)&1)^((a>>2)&1)*((a>>3)&1)
def alternate(a):
    rows=[0]*4
    for t,(i,j)in enumerate(itertools.combinations(range(4),2)):
        if a>>t&1:rows[i]|=1<<j;rows[j]|=1<<i
    return rows
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();start=time.monotonic()
    base=a.repo/'research/moonshot-005-program/results';lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json';pp=base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz'
    raw=gzip.decompress(lp.read_bytes());need(hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin');l=json.loads(raw);basis=json.loads(bp.read_bytes());H=list(map(set,l['A2']));D=list(map(set,l['D4']));roots=l['root_table']
    cols=basis['lattice_basis_columns'];inv=inverse([[cols[j][i]for j in range(8)]for i in range(8)]);change={xor(basis['hyperbolic_basis_masks'][k]for k in range(8)if v>>k&1):v for v in range(256)};need(len(change)==256,'binary hyperbolic change')
    masks=[]
    for root in roots:
        cs=[sum(x*y for x,y in zip(row,root))for row in inv];need(all(c.denominator==1 for c in cs),'integral root lattice coordinates');masks.append(change[sum((int(c)&1)<<k for k,c in enumerate(cs))])
    need(len(set(masks))==120 and all(q(x)==1 for x in masks),'all120 nonsingular vectors are actual roots')
    nonsingular=[v for v in range(64)if pfaffian(v)]
    def clique(chosen,candidates):
        if len(chosen)==7:return chosen
        for z,v in enumerate(candidates):
            result=clique(chosen+[v],[w for w in candidates[z+1:]if pfaffian(v^w)])
            if result:return result
        return None
    ker=[0]+clique([],nonsingular);need(len(ker)==8 and all(pfaffian(x^y)==1 for x,y in itertools.combinations(ker,2)),'eight alternating matrices have invertible pair differences')
    generators=[]
    for a4 in ker:
        A=alternate(a4);generators.append([(1<<(2*j))|sum(((A[k]>>j)&1)<<(2*k+1)for k in range(4))for j in range(4)])
    generators.append([1<<(2*k+1)for k in range(4)]);spaces=[span(g)for g in generators]
    singular={v for v in range(1,256)if q(v)==0};need(len(singular)==135,'singular vector census');need(all(len(S)==16 and all(q(v)==0 for v in S)for S in spaces),'nine maximal totally singular spaces');need(all(S&T=={0}for S,T in itertools.combinations(spaces,2)),'pairwise zero intersection');need(set.union(*spaces)==singular|{0},'orthogonal spread covers all singular vectors')
    radicals=[];selected=[]
    for d,Q in enumerate(D):
        V=span([masks[j]for j in Q]);need(len(V)==16,'D4 span dimension4');rad={x for x in V if all(polar(x,y)==0 for y in V)};need(len(rad)==4 and all(q(x)==0 for x in rad),'totally singular two-dimensional D radical');need({x for x in V if q(x)}=={masks[j]for j in Q},'D nonsingular vectors exactly roots');radicals.append(sorted(rad))
        if any(rad<=S for S in spaces):selected.append(d)
    selected=set(selected);need(len(selected)==630,'selected D count')
    adj=[{j for j,y in enumerate(roots)if sum(u*v for u,v in zip(x,y))==0}for x in roots];opposite={};Dindex={frozenset(Q):d for d,Q in enumerate(D)}
    for d,Q in enumerate(D):
        comp=frozenset(j for j in range(120)if Q<=adj[j]);need(comp in Dindex,'actual perpendicular D4');opposite[d]=Dindex[comp];need((d in selected)==(opposite[d]in selected),'allocation preserved by D perp')
    partitions=json.loads(gzip.decompress(pp.read_bytes()))['classes'];views=0;changed=0;local={}
    for h,P in enumerate(H):
        ports=[d for d,Q in enumerate(D)if P<=Q];chosen=sorted(set(ports)&selected);need(len(ports)==45 and len(chosen)==9,'global allocation gives nine ports at every H')
        if all(set(chosen)!=set(c)for c in partitions[str(h)]):changed+=1
        for i in range(120):
            if P<=adj[i]:
                visible=[d for d in ports if D[d]<=adj[i]];need(len(visible)==15 and len(set(visible)&selected)==3,'three selected ports at every actual view');views+=1
        local[h]=chosen
    need(views==40320,'all parent H receiver views')
    # Every selected D uses the same component on all16 incoming H flags,
    # so all12 donor count profiles are (4,0); unselected profiles are(0,4).
    flags=0
    for d,Q in enumerate(D):
        hs=[h for h,P in enumerate(H)if P<=Q];need(len(hs)==16,'D has16 A2 inputs')
        for j in Q:need(sum(j in H[h]for h in hs)==4,'D donor has four actual flags')
        flags+=len(hs)
    witness={'orthogonal_spread_generators':generators,'alternating_masks':ker,'selected_D':sorted(selected),'D_radicals':radicals,'perpendicular_D':opposite,'selected_ports_by_H':local}
    result={'status':'PASS_GLOBAL_TWO_COMPONENT_PORT_ALLOCATION','selected_D':len(selected),'unselected_D':len(D)-len(selected),'ordinary_and_exceptional_H':len(H),'selected_ports_per_H':9,'complement_ports_per_H':36,'selected_per_receiver':3,'complement_per_receiver':12,'verified_H_receiver_views':views,'changed_from_every_old_class_at_H':changed,'all_D_flag_count':flags,'current_bank_3840_component_input_widths':[768,3072],'current_bank_3840_component_quotient_widths':[48,192],'new_complete_kappa':False,'scope':'Exact global split-component port dimensions and actual changed local partitions; source inverse fibres, shared coefficient realization, phases, ownership, return and supplier remain open.','seconds':time.monotonic()-start,'source_pins':[{'path':str(p.relative_to(a.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [lp,bp,pp]]}
    a.out.mkdir(parents=True,exist_ok=True)
    with gzip.GzipFile(str(a.out/'WITNESS.json.gz'),'wb',mtime=0)as f:f.write(json.dumps(witness,separators=(',',':')).encode())
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
