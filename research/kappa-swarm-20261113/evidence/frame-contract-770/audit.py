#!/usr/bin/env python3
"""Actual Clifford rank/alias audit for h770's pre-first-use source frames."""
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
import gzip,importlib.util,json,sys,time
ROOT=Path('/workspace/scratch/19b21bdb3d72');HERE=Path(__file__).resolve().parent
PIN='acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9'
def need(ok,label):
    if not ok:raise ValueError(label)
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def spankey(U):
    s={0}
    for u in U:need(u not in s,'independent source frame basis');s|={v^u for v in s}
    return tuple(sorted(s))
def run():
    start=time.monotonic();wp=ROOT/'reference/pr7481/WORD.json.gz';raw=wp.read_bytes();need(sha256(raw).hexdigest()==PIN,'source byte pin');w=json.loads(gzip.decompress(raw))
    cp=ROOT/'worker-a/selected/frozen/clifford_exact.py';C=load('retained_clifford',cp);n=9
    keys=list(map(spankey,w['frames']));target=115;Cspan=set(keys[target]);dimC=len(w['frames'][target]);charts={};lagrangian_controls=0;involution_controls=0
    for i,U in enumerate(w['frames']):
        if i%16==0:need(time.monotonic()-start<60,'bounded frame construction and Lagrangian audit')
        F=C.canonical_frame(n,tuple(U));charts[i]=F
        perp=C.nullspace(U,n);abstract=[u|(u<<n) for u in U]+[v<<n for v in perp];actual=[x|(z<<n) for x,z,p in F.tab[n:]]
        need(C.rank(abstract)==n and C.rank(actual)==n and C.rank(abstract+actual)==n,'actual Z-Lagrangian depends on span as claimed');lagrangian_controls+=1
        squared=C.compose(F.tab,F.tab);need(all(a[:2]==b[:2] for a,b in zip(squared,C.identity(n))),'canonical frame symplectic involution');involution_controls+=1
    available={};npublic=w['public'];cur=w['initial'].copy()+[None]*w['owned_fields'];touches=[]
    def mark(frame,event,owner,kind):
        if frame not in available:available[frame]={'event':event,'owner':owner,'kind':kind}
    for a,f in enumerate(w['initial']):
        if a!=770:mark(f,-1,a,'entrance')
    for event,e in enumerate(w['program'][:33814]):
        op,a=e[:2]
        if a==770 or(op in ('ADD','COPY') and e[2]==770):touches.append(event)
        if op=='MOVE':need(cur[a]==e[2],'actual prefix MOVE');cur[a]=e[3];mark(e[3],event,a,'arrival')
        elif op=='INIT':need(a>=npublic and cur[a] is None,'fresh owned prefix INIT');cur[a]=e[2];mark(e[2],event,a,'zero_INIT')
        elif op=='CLEAR':need(cur[a]==e[2],'prefix CLEAR');cur[a]=None
        elif op=='SCALE':need(cur[a]==e[-1],'prefix SCALE')
        else:need(op in ('ADD','COPY') and a!=e[2] and cur[a]==cur[e[2]]==e[-1],'prefix coframed contact')
    need(not touches and w['program'][33814]==['COPY',1525,770,'1',115],'literal first h770 use')
    records=[];rank1=[];nonnested_rank1=[]
    for i in range(len(w['frames'])):
        if i%16==0:need(time.monotonic()-start<60,'bounded actual frame interface census')
        op=charts[i].adjoint().then(charts[target]);rank=C.rank([x for x,z,p in op.tab[n:]])
        inter=len(set(keys[i])&Cspan).bit_length()-1;expected=len(w['frames'][i])+dimC-2*inter
        need(rank==expected,'actual B-rank equals span-distance formula')
        nested=set(keys[i])<=Cspan or Cspan<=set(keys[i]);rec={'frame':i,'dimension':len(w['frames'][i]),'intersection_dimension':inter,'actual_B_rank':rank,'geometric_rank':expected,'nested':nested,'present_before_first_use':i in available,'first_availability':available.get(i)};records.append(rec)
        if rank==1:
            rank1.append(i)
            if not nested:nonnested_rank1.append(i)
    aliases=defaultdict(list)
    for i,k in enumerate(keys):aliases[k].append(i)
    duplicate_classes=[v for v in aliases.values() if len(v)>1];need(duplicate_classes==[[1091,1092]],'actual frame alias census')
    def alias_case(label,left,right):
        op=left.adjoint().then(right);rec,compiled=C.lower_child(op)
        need(rec['rank']==0 and compiled.tab==op.tab and compiled.zero_state()==op.zero_state(),'rankzero exact monomial adapter including absolute phase')
        rawtab=left.tab==right.tab;rawstate=left.zero_state()==right.zero_state()
        return {'label':label,'actual_interface_rank':0,'raw_tableaux_equal':rawtab,'raw_zero_states_equal':rawstate,'raw_operators_identical':rawtab and rawstate,'adapter_recipe':rec,'compiled_absolute_phase_checked':True}
    actual_alias=alias_case('source1091_to1092',charts[1091],charts[1092])
    U=w['frames'][target];changed=[U[0]^U[1],*U[1:]];need(spankey(changed)==keys[target],'synthetic basis change preserves span')
    synthetic_alias=alias_case('115_basis_change_first_plus_second',charts[target],C.canonical_frame(n,tuple(changed)))
    out={'status':'PASS_ACTUAL_FRAME_CONTRACT_RANK_AND_ALIAS_AUDIT','source_sha256':PIN,'clifford_code_sha256':sha256(cp.read_bytes()).hexdigest(),'frame_IDs':len(keys),'distinct_spans':len(aliases),'Lagrangian_identity_checks':lagrangian_controls,'symplectic_involution_checks':involution_controls,'target_frame':target,'prefix_instructions':33814,'actual_frame_IDs_available_before_first_use':len(available),'actual_spans_available_before_first_use':len({keys[f] for f in available}),'all_catalog_rank1_to115':rank1,'available_rank1_to115':[f for f in rank1 if f in available],'nonnested_catalog_rank1_to115':nonnested_rank1,'rank_formula_checks':len(records),'available_actual_B_rank_census':dict(sorted(Counter(r['actual_B_rank'] for r in records if r['present_before_first_use']).items())),'all_frame_records':records,'source_alias_classes':duplicate_classes,'actual_alias':actual_alias,'synthetic_same_span_alias':synthetic_alias,'seconds':time.monotonic()-start,'scope':'Actual canonical_frame/physical MOVE convention. Equal span gives rankzero monomial equivalence, not necessarily identical physical operator; adapters have ordinary cost. Negative history pooling granted normalization free. Universal geometric formula requires the separate algebraic proof; finite census alone is not that proof.'}
    (HERE/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('all_frame_records','actual_alias','synthetic_same_span_alias')},indent=2));print(json.dumps({'actual_alias':actual_alias,'synthetic_alias':synthetic_alias},indent=2))
if __name__=='__main__':run()
