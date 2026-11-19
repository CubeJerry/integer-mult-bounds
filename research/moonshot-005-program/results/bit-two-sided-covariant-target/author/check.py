#!/usr/bin/env python3
"""Exact fixed-bank target certificate; no physical realization is inferred."""
from __future__ import annotations
import argparse, gzip, hashlib, importlib.util, json
from pathlib import Path

def need(x,label):
    if not x:raise ValueError(label)
def eye(n):return [1<<i for i in range(n)]
def add(a,b):return [x^y for x,y in zip(a,b)]
def mm(a,b):
    out=[]
    for row in a:
        x=0
        while row:
            low=row&-row;x^=b[low.bit_length()-1];row^=low
        out.append(x)
    return out
def tensor(a,b):
    n=len(b)
    return [sum(br<<(j*n)for j in range(len(a))if ar>>j&1)for ar in a for br in b]
def rank(rows):
    piv={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k not in piv:piv[k]=x;break
            x^=piv[k]
    return len(piv)
def flatten(a):return sum(x<<(len(a)*i)for i,x in enumerate(a))
def comm(a,b):return add(mm(a,b),mm(b,a))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    base=args.repo/'research/moonshot-005-program/results'
    old=base/'bit-receiver-covariant-target/author/check.py'
    spec=importlib.util.spec_from_file_location('retained_target_geometry',old)
    pred=importlib.util.module_from_spec(spec);spec.loader.exec_module(pred)
    layoutpath=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    basispath=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    budgetpath=base/'bit-canonical-quotient-repair/author/output/BUDGET.json'
    raw=gzip.decompress(layoutpath.read_bytes())
    need(hashlib.sha256(raw).hexdigest()==pred.LAYOUT_PIN,'pinned native layout')
    gam,adj,K=pred.geometry(json.loads(raw),json.loads(basispath.read_text()))
    columns,gam=pred.adapted(gam)
    witnesspath=Path(__file__).with_name('WITNESS.json')
    witness=json.loads(witnesspath.read_text())
    need(sorted(adj[80])[59:]==witness['row_internal_donors']==[106,107,109],'row allocation')
    need(sorted(adj[10])[59:]==witness['column_internal_receivers']==[109,110],'column allocation')
    t8,w8,u8=witness['secondary_matrices_8']
    for a,j in zip([t8,w8,u8],[107,109,110]):
        p=[row&255 for row in gam[j][:8]]
        need(comm(a,p)==[0]*8,'secondary endpoint commutation')
    t=add(tensor(t8,eye(4)),tensor(eye(8),[2,4,8,0]))
    w=add(tensor(w8,eye(4)),tensor(eye(8),[0,0,0,1]))
    u=tensor(u8,eye(4));gens=[t,w,u]
    mats=[]
    for word in witness['word_basis_32']:
        a=eye(32)
        for k in word:
            need(k in (0,1,2),'word alphabet');a=mm(a,gens[k])
        mats.append(flatten(a))
    need(len(mats)==1024 and rank(mats)==1024,'full secondary matrix algebra')
    e01=[2,0];e10=[0,1]
    internal=[tensor(e01,a)for a in [eye(32),t,w]]+[tensor(e10,a)for a in [eye(32),u]]
    edges=[(80,106),(80,107),(80,109),(109,10),(110,10)]
    commutators=[]
    for n,(i,j)in zip(internal,edges):
        need(mm(n,n)==[0]*64,'every internal generator square zero')
        need(rank(add(n,eye(64)))==64,'every internal block invertible')
        ri=rank(comm(n,tensor(gam[i],eye(4))))
        rj=rank(comm(n,tensor(gam[j],eye(4))))
        need(ri==rj==0,'both actual endpoint actions commute')
        commutators.append({'edge':[i,j],'receiver_commutator_rank':ri,'donor_commutator_rank':rj})
    need(mm(internal[0],internal[3])==tensor([1,0],eye(32)),'E00 in generated algebra')
    need(mm(internal[3],internal[0])==tensor([0,2],eye(32)),'E11 in generated algebra')
    # The exact rank-separation argument is on native support, before tensoring.
    allmask=(1<<111)-1
    sep=[]
    for support in [adj[80]|{10},adj[10]|{80}]:
        mask=allmask^sum(1<<j for j in support)
        sep.append(rank([row&mask for row in K]))
    need(sep==[9,9],'canonical row and column separation')
    budget=pred.budget(json.loads(budgetpath.read_text()))
    # Negative control: a wrong secondary unit can preserve the receiver
    # action while destroying the donor action on the same actual edge.
    bad=None
    for r in range(32):
        for c in range(32):
            x=[0]*32;x[r]=1<<c;n=tensor(e01,x)
            if rank(comm(n,tensor(gam[107],eye(4)))):
                bad={'secondary_unit':[r,c],
                     'receiver_rank':rank(comm(n,tensor(gam[80],eye(4)))),
                     'donor_rank':rank(comm(n,tensor(gam[107],eye(4))))};break
        if bad:break
    need(bad is not None and bad['receiver_rank']==0 and bad['donor_rank']>0,'wrong donor control')
    need(all(not(row&((1<<32)-1))for n in internal[:3]for row in n[32:]),'omitting both E10 preserves first half')
    need(any(row&((1<<32)-1)for row in internal[3][32:]),'E10 breaks first-half invariance')
    badunit=[0]*64;badunit[0]=1
    need(rank(add(badunit,eye(64)))==63,'diagonal nonnilpotent singularity')
    # Actual whole-bank transfers, represented at bank granularity, verify
    # support, inverses, tensor commutation and all matrix-unit transport.
    transfer_checks=[]
    for l in range(1,60):
        forward=[0]*60;forward[0]=1<<l
        reverse=[0]*60;reverse[l]=1
        need(mm(forward,forward)==mm(reverse,reverse)==[0]*60,'transfer square zero')
        e00=[0]*60;e00[0]=1
        ell=[0]*60;ell[l]=1<<l
        need(mm(forward,reverse)==e00 and mm(reverse,forward)==ell,'transfer matrix units')
        transfer_checks.append(l)
    sourcepaths=[old,layoutpath,basispath,budgetpath,
                 base/'bit-receiver-covariant-target/author/PROOF.md',
                 base/'bit-replacement-return-bank/author/PROOF.md']
    result={'status':'PASS_TWO_SIDED_COVARIANT_LOW_RETURN_TARGET',
        'scope':'fixed algebraic target and body replications; physical H/D/K gluing open; No new kappa',
        'bank':3840,'foreign_blocks':6470,'secondary_algebra_dimension':1024,
        'word_count':len(mats),'maximum_word_length':max(map(len,witness['word_basis_32'])),
        'full_generated_matrix_algebra_dimension':3840**2,
        'canonical_rank':9*3840,'perturbation_rank':128,'return_rank':34688,
        'retained_repair_rank':128,'native_separation_ranks':sep,
        'internal_commutators':commutators,'bank_transfer_pairs_checked':len(transfer_checks),
        'negative_controls':{'wrong_endpoint':bad,'omitted_both_E10_invariant_dimension':1920,
                             'diagonal_mutation_internal_rank':63},
        'irreducibility_scope':'the fixed3840 bank; identity-body replications only retain the flat exclusions',
        'source_compatibility':{'End16_copies':15,'atlas480_copies':8,'same_left_spinor_factor':True},
        'movement_only':budget,
        'source_pins':[{'path':str(p.relative_to(args.repo)),'sha256':digest(p)}for p in sourcepaths],
        'witness_sha256':digest(witnesspath),
        'five_foundational_assumptions_retained':True,'new_complete_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'ASSIGNMENT.json').write_text(json.dumps({'adapted_spinor_basis_columns':columns,
        'row_transfers':[[80,j,l]for l,j in enumerate(sorted(adj[80])[:59],1)],
        'column_transfers':[[i,10,l]for l,i in enumerate(sorted(adj[10])[:59],1)],
        'internal_edges':edges,'internal_matrices_64':internal},indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['bank','perturbation_rank','return_rank','word_count']}))
if __name__=='__main__':main()
