#!/usr/bin/env python3
"""Verify the placement-independent Extra6 source cut and actual chart domains."""
from pathlib import Path
import argparse,hashlib,importlib.util,itertools,json
J=[8,9,36,37]
WORD='af51d0d7c872dbf3fa3744b582769d4c7763e0747e57c74005d091d19b7da474'
def load(path):
    s=importlib.util.spec_from_file_location('leaf_engine',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots'];e=load(a.engine);C,hist,rep=e.replay(w,R);banks=e.make_banks(w);mask=sum(1<<j for j in J)
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));assert all(dot(i,j)!=0 for i in J for j in J);assert set(J).isdisjoint(w['targets'])
    old=[];counts={}
    for i in J:
        vis=[x for x in hist if e.sub(C[x[2]],C[f'F{i}'])];counts[str(i)]=len(vis)
        old +=[v&mask for _,_,_,v in vis]
    assert all(v==0 for v in old)
    others=[row&mask for k,b in enumerate(banks) if k!=6 for row in b]
    b=list(e.bb(others).values());assert b==[(1<<8)^(1<<9)^(1<<37)]
    assert len(e.bb(r&mask for r in banks[6]))==4
    kernel=[(1<<8)^(1<<37),(1<<9)^(1<<37),1<<36]
    assert len(e.bb(kernel))==3 and all((z&b[0]).bit_count()%2==0 for z in kernel)
    pred=['J16','J23','J22','M1','M1','M1','Extra6','D3_21'];domains=[]
    for k,ch in enumerate(pred):
        leaves=[j for j in range(111) if e.sub(C[f'L{j}'],C[ch])]
        assert e.PORTS[k] in leaves
        domains.append({'packet':f'P{k}','preceding_chart':ch,'preceding_chart_rank':len(C[ch]),'current_port':e.PORTS[k],'candidate_native_leaves':leaves})
    counts_changes={}
    for r in range(4):counts_changes[str(r)]=sum(__import__('math').prod(len(domains[k]['candidate_native_leaves'])-1 for k in ks)for ks in itertools.combinations(range(8),r))
    # Two independent new E source directions are necessary to bring the
    # remaining one-record Extra6 contribution within the source-dimension cut.
    current_rank=len(e.bb(others));assert current_rank==1
    added=[1<<8,1<<36];expanded=list(e.bb(others+added).values());assert len(expanded)==3
    full=expanded+[1<<9];assert len(e.bb(full))==4
    # Dropping either fresh direction restores a rank deficit for one E record.
    assert all(len(e.bb(others+[added[k],1<<9]))==3 for k in range(2))
    # Actual Extra6→M1 source transport is one positive owned rank step.
    assert len(C['Extra6'])==6 and len(C['M1'])==5 and e.sub(C['M1'],C['Extra6'])
    out={'status':'PASS_PLACEMENT_INDEPENDENT_EXTRA6_THREE_RECORD_FLOOR','word_sha256':WORD,'native_source_sha256':w['source_sha256'],'all222_replay':rep,'receiver_set':J,'gram_matrix':[[dot(i,j)for j in J]for i in J],'fixed_history_projection_rank':0,'fixed_history_incidence_counts':counts,'all_other_banks_globally_granted_projection_basis_hex':[hex(v)for v in b],'other_bank_projection_rank':1,'Extra6_bank_projection_rank':4,'input_kernel_basis_hex':[hex(v)for v in kernel],'required_Extra6_transcript_symbols':'3V','one_record_Extra6_deficit_symbols':'2V','source_rank_needed_outside_single_Extra6_record':3,'additional_outside_E_directions_needed':2,'domain_scope':'All native leaf assignments in their actual immediately preceding charts; arbitrary placements are also excluded by the same information proof.','source_chart_domains':domains,'configurations_by_exact_number_of_changed_ports':counts_changes,'number_of_configurations_changing_at_most_three_ports':sum(counts_changes.values()),'exact_joint_source_span_repair_example':{'two_new_outside_directions':['X8','X36'],'one_Extra6_message':'X9','existing_globally_granted_direction':'X8+X9+X37','joint_rank':4,'physical_delivery_claimed':False},'actual_geometry_escape':{'from':'Extra6','to':'M1','owned_rank_drop':1,'source_capture_and_decoder_work_still_required':True},'scope':'Frozen actual higher/common histories and fixed bank sources; one finite transcript per bank. Arbitrary port changes and free decoded-point feedback do not create source dimension. New independent E source directions or changed higher/common measurements can escape. No full supplier or new kappa.'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','required_Extra6_transcript_symbols','additional_outside_E_directions_needed','configurations_by_exact_number_of_changed_ports','number_of_configurations_changing_at_most_three_ports']}))
if __name__=='__main__':main()
