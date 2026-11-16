"""Audit the inherited live Hub cut; do not construct a new recipe word."""
from pathlib import Path
import argparse,hashlib,json,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();P=a.repo.resolve()/'research/moonshot-005-program';sys.path.insert(0,str(P/'results/bit-shared-meet-funnel/root-review'));from check import rr,null,rank
path=P/'results/bit-cross-bank-recoding/author/output/WORD.json';w=json.loads(path.read_text());assert hashlib.sha256(path.read_bytes()).hexdigest()=='f17fb4bb7cc9dbe2c3a1725f1b24586b0e97262b98c7e2cff07e25df35ad35a5'
v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
for step,o in enumerate(w['operations'],1):
 if o==['INIT','P7','Hub']:break
 op,n,*q=o
 if op=='INIT':v[n]=0;at[n]=q[0]
 elif op=='MOVE':at[n]=q[0]
 elif op=='ADD':v[q[0]]^=v[n]
 elif op=='CLEAR':del v[n];del at[n]
fields={n:hex(z)for n,z in v.items()if at[n]=='Hub'and not(z>>111)};H=[int(x,16)for x in fields.values()];assert len(fields)==rank(H)==102
C={n:rr(c['rows'])if c['kind']=='span'else null(c['rows'])for n,c in w['charts'].items()};vis={str(i):{c:len(rr(C[c]+C[f'F{i}']))==len(C[f'F{i}'])for c in ['C0','D3_21']}for i in [24,42,69]};assert not any(z for row in vis.values()for z in row.values())
end=next(i for i in range(step,len(w['operations']))if w['operations'][i][0]=='MOVE'and w['operations'][i][1]=='P7');queries=[o for o in w['operations'][step:end]if o[0]=='ADD'and o[2]=='P7'];assert len(queries)==59
src=a.repo.resolve()/w['source_path'];assert hashlib.sha256(src.read_bytes()).hexdigest()==w['source_sha256'];R=json.loads(src.read_text())['native_roots'];K=[(1<<i)^sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)];assert(rank(K),rank(H+K))==(9,109)
o={'status':'PASS_EXACT_SOURCE_SELECTION_CUT_ONLY','word_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'cut_before_P7_INIT':step,'actual_Hub_fields':fields,'field_count':102,'rank':102,'old_P7_preload_queries':59,'receiver_retained_chart_visibility':vis,'canonical_rank':9,'joint_Hub_canonical_rank':109,'Hub_canonical_intersection_rank':2,'scope':'Exact finite source audit. Hubrank102 was already proved in predecessor packages. No selected new recipe word or inherited history/decoder claim.'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(o,indent=2)+'\n');print(o['status'])
