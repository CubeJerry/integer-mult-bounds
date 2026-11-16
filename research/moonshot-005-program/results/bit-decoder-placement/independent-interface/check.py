#!/usr/bin/env python3
"""Independent bank-cut certificates and complete fixed-port stock domination."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def xor(rows,c):
    assert c>>len(rows)==0
    out=0
    for j,r in enumerate(rows):
        if c>>j&1:out^=r
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--envelope',type=Path,required=True);p.add_argument('--compression',type=Path,required=True);p.add_argument('--ports',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    path=Path(__file__).with_name('retained')/'source_history_engine.py';s=importlib.util.spec_from_file_location('independent',path);e=importlib.util.module_from_spec(s);s.loader.exec_module(e)
    assert sha(a.word)=='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e'
    assert sha(a.envelope)=='5bd89e3a32a0649fd3b3c1adf68ebd857100aa653aa2ee4cb1273cfd3f1fc5f0'
    assert sha(a.compression)=='9032709325131c05a50a0474d0213c2ad96f7fb39c124beddba9a9c6ebf7a118'
    w=json.loads(a.word.read_text());D=json.loads(a.envelope.read_text());Q=json.loads(a.compression.read_text());A=json.loads(a.ports.read_text());native=a.repo/w['source_path'];assert sha(native)==w['source_sha256'];R=json.loads(native.read_text())['native_roots']
    rank=lambda rows:len(e.basis(rows));dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));locals=[[1<<j for j in range(111)if dot(i,j)==0]for i in range(111)];K=[(1<<i)^sum(locals[i])for i in range(111)];assert rank(K)==9
    B=[int(x,16)for x in D['reconstructed_common_bank_rows_hex']]+[1<<j for g in D['private_groups']for j in g];U=[[int(x,16)for x in g]for g in D['actual_remaining_filter_rows_hex']];E=B+[1<<i for i in D['all_six_bank_case']['feedback_closure']];assert rank(B)==80 and rank(E)==88
    summaries=[];duals=0;canonical=0;mutants=0
    for z,(side,ds)in enumerate([(B,[3,3,3,4]),(E,[2,2,2,3])]):
        case=Q['cases'][z];assert side==[int(x,16)for x in case['side_rows_hex']];assert rank(side+K)-rank(side)==4-z
        for j,d in enumerate(ds):
            other=side+[r for k,bank in enumerate(U)if j!=k for r in bank];c=case['cut_certificates'][j];assert rank(other)==c['other_bank_plus_side_rank'];assert rank(other+K)==c['plus_C9_rank'];assert rank(other+K)-rank(other)==d
            chosen=[K[i]for i in c['separated_canonical_indices']];assert len(chosen)==d
            for t,h in enumerate(c['dual_hex']):
                lam=int(h,16);assert all(not((lam&r).bit_count()%2)for r in other);assert[(lam&r).bit_count()%2 for r in chosen]==[int(k==t)for k in range(d)];duals+=1
        messages=[]
        for bank,masks,rows in zip(U,case['bank_message_original_row_masks'],case['bank_messages_hex']):
            mm=[xor(bank,int(m,16))for m in masks];assert mm==[int(x,16)for x in rows];messages.append(mm)
        assert[rank(x)for x in messages]==ds;flat=sum(messages,[]);assert len(flat)==sum(ds)
        for k,c in zip(K,case['all111_canonical_witnesses_hex']):assert xor(side+flat,int(c,16))==k;canonical+=1
        for j in range(len(flat)):assert rank(side+flat[:j]+flat[j+1:]+K)>rank(side+flat[:j]+flat[j+1:]);mutants+=1
        summaries.append({'side_rank':rank(side),'conditional_dimensions':ds,'optimum':sum(ds)})
    run=e.replay(w,R,[int(x,16)for x in w['seed_rows_hex']],15,False);v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];C=run['C'];h=w['singular_h'];extra=w['history_extra_query_roles'];banks={'h0':([7,11,12],[1<<j for j in range(111)if h[j]==0]),'h1':([0,28,44],[1<<j for j in range(111)if h[j]==1 and j not in extra]),'extra':([19],[1<<j for j in extra]+[v['HKEEP_E6']]),'D3':([27],[1<<j for j in range(111)if h[j]==0]+[v['HKEEP_D7']])}
    assert[rank(rows)for ports,rows in banks.values()]==[52,53,7,53]
    for name,(ports,rows)in banks.items():assert ports==A['bank_description'][name]['ports']and rows==[int(x,16)for x in A['bank_description'][name]['rows_hex']]
    ground=[1<<i for i in w['targets']];base=[];field_count=0;history_count=0;positive=[]
    for i in range(111):
        rows=ground+locals[i]+[r for ports,bank in banks.values()if any(dot(i,j)==0 for j in ports)for r in bank];b=e.basis(rows)
        def has(r):
            while r:
                k=r.bit_length()-1
                if k not in b:return False
                r^=b[k]
            return True
        F=C[f'F{i}'];visible_charts={name for name,chart in C.items()if e.contained(chart,F)}
        for name,r in v.items():
            if not name.startswith('Y')and at[name]in visible_charts:assert r>>111==0 and has(r),(i,name);field_count+=1
        for q in run['snapshots']:
            if q['chart']in visible_charts:assert has(int(q['row_hex'],16)),(i,q);history_count+=1
        if has(1<<i):positive.append(i)
        base.append(rows)
    known=set(w['targets']);waves=[]
    while True:
        nxt={i for i,rows in enumerate(base)if e.solve(rows+[1<<j for j in sorted(known)],1<<i)is not None};assert known<=nxt
        if nxt==known:break
        waves.append(sorted(nxt-known));known=nxt
    assert sorted(known)==A['closure']and len(known)==108 and positive==A['closure']
    for rec in A['excluded']:
        i=rec['receiver'];lam=int(rec['dual_hex'],16);assert lam>>i&1 and all(not((lam&r).bit_count()%2)for r in base[i]+[1<<j for j in known])
    out={'status':'PASS_INDEPENDENT_COMPRESSION_AND_FIXED_PORT','word_sha256':sha(a.word),'compression_certificate_sha256':sha(a.compression),'native_source_sha256':sha(native),'compression_cases':summaries,'cut_dual_identity_count':duals,'canonical_witness_count':canonical,'single_message_deletion_controls':mutants,'complete_222_column_replay':True,'actual_visible_pure_X_field_incidences_dominated':field_count,'actual_visible_principal_history_incidences_dominated':history_count,'bank_ranks':[rank(rows)for ports,rows in banks.values()],'closure':sorted(known),'waves':waves,'excluded':A['excluded'],'scope':'Fixed separated banks and point-terminal span; coded terminals or actual cross-bank interactions can escape. Compression has fixed side information, direct canonical recovery, no new feedback, no physical price claim.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:x for k,x in out.items()if k not in ['closure','waves']}))
if __name__=='__main__':main()
