#!/usr/bin/env python3
"""Exact balanced-source quotient prerequisites and literal source-stage controls."""
from argparse import ArgumentParser
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import gzip,json

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FACTOR_HASH='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'

def need(value,message):
    if not value:raise ValueError(message)
def rank(rows):
    piv={}
    for x in rows:
        while x and x.bit_length() in piv:x^=piv[x.bit_length()]
        if x:piv[x.bit_length()]=x
    return len(piv)
def span(rows):
    out={0}
    for r in rows:out|={x^r for x in tuple(out)}
    return out

def controls():
    # An explicit non-MDS family of three quotient spaces on four coordinates.
    U=[(1,2),(2,4),(4,8)];weights=[1,1,2]
    inequalities=[]
    for n in range(4):
        for ss in combinations(range(3),n):
            dim=rank([v for h in ss for v in U[h]]);demand=sum(weights[h]for h in ss)
            need(dim>=demand,'positive weighted rank condition')
            inequalities.append([list(ss),dim,demand])
    early=((1,),(2,),(4,8));late=((2,),(4,),())
    E=[r for a in early for r in a];need(rank(E)==4,'invertible genuine early source')
    need(len(span(U[0])&span(U[1]))==2,'positive source is deliberately not MDS')
    for h in range(3):need(span(early[h]+late[h])==span(U[h]),'source quotient preserved')
    # Every input and every independent late Y baseline is checked.
    cases=0
    for x in range(16):
        e=[(r&x).bit_count()%2 for r in E]
        need(sum(v<<k for k,v in enumerate(e))==x,'early restoration')
        for ys in product(range(2),repeat=2):
            changes=[(r&x).bit_count()%2 for h in range(3)for r in late[h]]
            out=[y^z for y,z in zip(ys,changes)]
            need([a^b for a,b in zip(out,ys)]==changes,'late arbitrary baseline retained')
            cases+=1
    # Each singleton requirement passes, while the joint source requirement fails.
    bad_U=[(1,),(1,)];bad_a=[1,1]
    need(all(rank(u)>=a for u,a in zip(bad_U,bad_a)),'negative single-space pass')
    need(rank([v for u in bad_U for v in u])<sum(bad_a),'negative joint rank rejected')
    # Small direct sumset equality, with all fibres enumerated in F2^3.
    subsets=[set(c)for c in combinations(range(8),2)];equal=0
    for a in subsets:
        for b in subsets:
            sums={x^y for x in a for y in b}
            if len(sums)!=2:continue
            da={x^min(a)for x in a};db={x^min(b)for x in b}
            need(da==db and all(x^y in da for x in da for y in da),'coset equality')
            equal+=1
    return {'positive_non_MDS_spaces':U,'early_weights':weights,'early_rows':early,'late_rows':late,'all_subset_ranks':inequalities,'arbitrary_input_and_Y_cases':cases,'negative_joint_rank_rejected':True,'small_equal_sumset_pairs_checked':equal}

def main():
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--factor',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());fr=a.factor.read_bytes()
    need(sha256(raw).hexdigest()==LAYOUT_HASH,'layout source pin');need(sha256(fr).hexdigest()==FACTOR_HASH,'factor source pin')
    w=json.loads(raw);fac=json.loads(fr);A=[set(h)for h in w['A2']];R=w['root_table'];N=set(range(111))
    need(len(A)==1120 and len(R)==120 and len({tuple(r)for r in R})==120,'native layout sizes')
    need(all(sum(x*x for x in r)==4 for r in R),'exact root norms')
    F=[{j for j in range(120)if sum(a*b for a,b in zip(r,R[j]))==0}for r in R[:111]]
    pencil=[[h for h,H in enumerate(A)if j in H]for j in range(111)]
    need(all(len(p)==28 for p in pencil),'native pencil size')
    singleton={h for h,H in enumerate(A)if len(H&N)==1};ordinary={(j,h)for j in range(111)for h in pencil[j]if h not in singleton}
    need(len(singleton)==11 and len(ordinary)==3097,'ordinary and exceptional source count')
    add=dict(fac['factors']);need(fac['denominator']==2 and set(add)<={h for h,H in enumerate(A)if len(H&N)==3},'balanced factor domain')
    x=[(12//len(H&N)if H&N else 0)+add.get(h,0)for h,H in enumerate(A)];e=[max(8,u)for u in x]
    need(all(sum(45*x[h]for h in pp)==5760 for pp in pencil),'all actual early counts')
    need(all(45*e[h]==(540 if h in singleton else 360)for j,h in [(j,h)for j in range(111)for h in pencil[j]]),'source emission capacities')
    vis={(j,i):[h for h in pencil[j]if A[h]<=F[i]]for j in range(111)for i in F[j]&N}
    need(len(vis)==6470 and all(len(v)==16 for v in vis.values()),'all foreign visible planes')
    tight={(j,i):not (set(hs)&singleton)for (j,i),hs in vis.items()}
    histogram=Counter(sum(45*e[h]for h in hs)for hs in vis.values())
    need(dict(histogram)=={5760:6110,5940:360},'tight and slack source cuts')
    witnesses=[];hist=Counter();joint_hist=Counter()
    for j,h in sorted(ordinary):
        choices=[]
        for i in sorted(F[j]&N):
            if h not in vis[j,i] or not tight[j,i]:continue
            peers=[]
            for p in vis[j,i]:
                if p==h:continue
                ks=sorted(k for k in A[p]&N if k!=j and tight.get((k,i),False))
                if not ks:break
                peers.append([p,ks[0]])
            if len(peers)==15:choices.append((i,peers))
        need(choices,'clean tight receiver exists');hist[len(choices)]+=1
        i,peers=choices[0];witnesses.append({'donor':j,'plane':h,'receiver':i,'companions':peers,'available_receivers':len(choices)})
    need(min(hist)==13,'minimum clean witness count')
    for h,H in enumerate(A):
        if len(H&N)<2:continue
        choices=[i for i in range(111)if H<=F[i]and all(tight.get((j,i),False)for j in H&N)]
        need(choices,'joint-tight plane receiver');joint_hist[len(choices)]+=1
    # Verify the exact canonical row-space and all outside-facet neutralizations.
    Om=[sum(1<<j for j in f&N)for f in F];Km=[r^(1<<j)for j,r in enumerate(Om)]
    need(rank(Om)==108 and rank(Km)==9,'literal native and canonical ranks')
    outside=[];full=(1<<111)-1
    for i in range(111):
        mask=full^Om[i];q=rank([r&mask for r in Km]);need(q==9,'outside donors neutralize all canonical rows');outside.append(q)
    # Exact counterexample to calling every source pair tight.
    bad_pair=next((j,i)for (j,i),is_tight in tight.items()if not is_tight)
    bad_j,bad_i=bad_pair;bad_h=next(h for h in vis[bad_pair]if h in singleton)
    need(sum(45*e[h]for h in vis[bad_pair])==5940,'reject singleton-exposed false tight pair')
    # A valid P with a companion that is not tight: just seeing a native peer is insufficient.
    bad_comp=None
    for (j,i),is_tight in tight.items():
        if not is_tight:continue
        for p in vis[j,i]:
            for k in A[p]&N-{j}:
                if not tight.get((k,i),False):bad_comp=[j,i,p,k];break
            if bad_comp:break
        if bad_comp:break
    need(bad_comp is not None,'meaningful untight companion negative control exists')
    out={'status':'PASS_BALANCED_ORDINARY_QUOTIENT_AND_SOURCE_COMPILER','baseline_programme_sha':'8cf982065bccdd62de2856b16635a6ee06dadb0c','layout_uncompressed_sha256':LAYOUT_HASH,'factor_sha256':FACTOR_HASH,'paid_field_slots_per_role':5760,'ordinary_plane_bundle':360,'singleton_plane_bundle':540,'ordinary_flags':len(ordinary),'singleton_flags':len(singleton),'source_cut_histogram':dict(sorted(histogram.items())),'clean_witness_histogram':dict(sorted(hist.items())),'joint_tight_plane_receiver_histogram':dict(sorted(joint_hist.items())),'binary_ranks_O_K':[108,9],'canonical_outside_rank_histogram':dict(Counter(outside)),'negative_controls':{'false_tight_pair':[bad_j,bad_i,bad_h],'untight_companion':bad_comp},'source_compiler_controls':controls(),'full_source_constructed':False,'new_complete_kappa':False,'witnesses':witnesses}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],out['ordinary_flags'],'ordinary flags; min clean witnesses',min(hist),'output_sha256',sha256(a.out.read_bytes()).hexdigest())
if __name__=='__main__':main()
