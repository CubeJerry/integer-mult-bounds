#!/usr/bin/env python3
"""Exact native shared-port connectivity and identical-stripe information cap."""
from argparse import ArgumentParser
from collections import Counter,deque
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import gzip,json

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FACTOR_HASH='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'
def need(q,msg):
    if not q:raise ValueError(msg)
def rank(rows):
    b={}
    for r in rows:
        while r and r.bit_length()in b:r^=b[r.bit_length()]
        if r:b[r.bit_length()]=r
    return len(b)
def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return r
def controls():
    pairs={(x^y,x^mul(2,y))for x in range(4)for y in range(4)}
    need(len(pairs)==16,'independent plane rows have joint full range')
    left={0};right=set()
    while True:
        rr={b for a,b in pairs if a in left};ll={a for a,b in pairs if b in rr}
        if ll==left and rr==right:break
        left,right=ll,rr
    need(len(left)==len(right)==4,'common deterministic output must be constant')
    proportional={(x^y,mul(2,x^y))for x in range(4)for y in range(4)}
    need(len(proportional)==4,'proportional target lines retain full scalar information')
    private=[{0},{1}];need(not(private[0]&private[1]),'private-port positive control')
    return {'F4_independent_row_pair_values':sorted(pairs),'common_function_components':1,'proportional_row_joint_range':len(proportional),'private_target_components':2,'private_output_dimension':2,'false_connected_private_bound_rejected':True}

def main():
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--factor',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());fb=a.factor.read_bytes()
    need(sha256(raw).hexdigest()==LAYOUT_HASH,'layout pin');need(sha256(fb).hexdigest()==FACTOR_HASH,'factor pin')
    w=json.loads(raw);factor=json.loads(fb);A=[set(h)for h in w['A2']];D=[set(d)for d in w['D4']];R=w['root_table'];N=set(range(111))
    need(len(A)==1120 and len(D)==3150,'actual chart census')
    F=[{j for j in range(120)if sum(x*y for x,y in zip(r,R[j]))==0}for r in R[:111]]
    singleton={h for h,H in enumerate(A)if len(H&N)==1}
    single_by={j:[h for h in singleton if j in A[h]]for j in range(111)}
    need(len(singleton)==11 and all(len(v)<=1 for v in single_by.values()),'singleton exposure scope')
    add=dict(factor['factors']);need(factor['denominator']==2,'factor denominator')
    x=[(12//len(H&N)if H&N else 0)+add.get(h,0)for h,H in enumerate(A)]
    need(all(sum(45*x[h]for h,H in enumerate(A)if j in H)==5760 for j in range(111)),'paid bank size')
    ports=[[d for d,DD in enumerate(D)if H<=DD]for H in A]
    need(all(len(ds)==45 for ds in ports),'45 actual D4 ports per plane')
    receipt=[];hist=Counter();info=0;uncovered_total=0;shared_edge_count=0
    for h,H in enumerate(A):
        if len(H&N)<2:continue
        ns=[i for i in range(111)if H<=F[i]and all(not any(A[g]<=F[i]for g in single_by[j])for j in H&N)]
        need(ns,'ordinary plane has jointly tight receivers')
        visible={i:{d for d in ports[h]if D[d]<=F[i]}for i in ns}
        need(all(len(v)==15 for v in visible.values()),'every tight receiver sees 15 ports')
        all_pairs={}
        for pos,i in enumerate(ns):
            for k in ns[pos+1:]:
                shared=visible[i]&visible[k]
                if shared:all_pairs[i,k]=min(shared)
        shared_edge_count+=len(all_pairs)
        seen={ns[0]};todo=deque([ns[0]]);tree=[]
        while todo:
            i=todo.popleft()
            for k in ns:
                key=tuple(sorted((i,k)))
                if k not in seen and key in all_pairs:
                    d=all_pairs[key];need(d in visible[i]&visible[k],'actual shared-port edge')
                    tree.append([i,k,d]);seen.add(k);todo.append(k)
        need(seen==set(ns),'joint-tight receiver graph connected')
        covered=set.union(*visible.values());uncovered=sorted(set(ports[h])-covered)
        u=len(uncovered);hist[u]+=1;uncovered_total+=u;info+=360+24*u
        receipt.append({'plane':h,'native_donors':sorted(H&N),'joint_tight_receivers':ns,'spanning_tree_with_D4_witnesses':tree,'uncovered_D4_ports':uncovered})
    need(len(receipt)==1108 and dict(hist)=={0:834,5:260,9:4,10:10},'exact uncovered-port census')
    need(uncovered_total==1436 and info==433344,'ordinary H aggregate bound')
    singleton_info=sum(45*x[h]for h in singleton);need(singleton_info==5940,'all singleton information generously retained')
    total=info+singleton_info;need(total==439284,'global output capacity')
    O=[sum(1<<j for j in f&N)for f in F];K=[z^(1<<j)for j,z in enumerate(O)]
    need(rank(K)==9,'canonical rank nine');domain=(111-rank(K))*5760
    need(domain==587520 and domain-total==148236,'strict information deficit')
    res={'status':'PASS_IDENTICAL_SCALAR_STRIPE_INFORMATION_OBSTRUCTION','baseline_programme_sha':'8cf982065bccdd62de2856b16635a6ee06dadb0c','layout_uncompressed_sha256':LAYOUT_HASH,'factor_sha256':FACTOR_HASH,'ordinary_planes':len(receipt),'connected_joint_tight_graphs':len(receipt),'checked_shared_port_edges':shared_edge_count,'uncovered_port_histogram':dict(sorted(hist.items())),'uncovered_ports_total':uncovered_total,'ordinary_information_capacity':info,'singleton_information_capacity':singleton_info,'total_information_capacity':total,'canonical_zero_input_dimension':domain,'strict_deficit':domain-total,'normalized_capacity_in_banks':str(Fraction(total,5760)),'normalized_deficit_in_banks':str(Fraction(domain-total,5760)),'controls':controls(),'scope':'Donor-specific scalar quotient rows identically repeated on 360r stripes in actual input coordinates; nonlinear downstream allowed; arbitrary array maps remain open.','new_complete_kappa':False,'planes':receipt}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(res,indent=2)+'\n');print(res['status'],total,'<',domain,'deficit',domain-total,'sha256',sha256(a.out.read_bytes()).hexdigest())
if __name__=='__main__':main()
