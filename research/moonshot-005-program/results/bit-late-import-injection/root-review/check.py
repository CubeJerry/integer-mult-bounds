#!/usr/bin/env python3
"""Independent225-column provenance controls for the fixed late-injection cut."""
from pathlib import Path
import argparse,hashlib,json
from optimize_word import independent_replay
from review_leaf_capacity import chart_basis,echelon

WITNESSES={8:[43,29,45],9:[41,42,48],36:[43,29,48]}
MARKERS={'P3':'K46_PAIR','P4':'P4_K','P5':'P5_K'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--word',nargs=2,action='append',required=True);a=p.parse_args();reports=[]
    for pin,path in a.word:
        raw=Path(path).read_bytes();assert hashlib.sha256(raw).hexdigest()==pin;w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];roots=json.loads(source)['native_roots'];ordinary=independent_replay(w)
        C={n:tuple(tuple(row)for row in chart_basis(r))for n,r in w['charts'].items()};memo={}
        def sub(x,y):
            if (x,y)not in memo:memo[x,y]=len(echelon(C[x]+C[y])[0])==len(C[y])
            return memo[x,y]
        for i in range(111):
            assert len(C[f'L{i}'])==1 and len(echelon(list(C[f'L{i}'])+[roots[i]])[0])==1
            assert len(C[f'F{i}'])==7 and all(sum(x*y for x,y in zip(row,roots[i]))==0 for row in C[f'F{i}'])
        v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
        history=[(n,at[n],r)for n,r in v.items()];events=[]
        for step,op in enumerate(w['operations']):
            kind,n,*q=op
            if kind=='MOVE'and n in MARKERS and q==[MARKERS[n]]:
                assert sub(at[n],'M1')and sub('M1',at[n])and not v[n]>>222
                for j in [8,9,36]:assert v[f'IMPORT_E{j}']==1<<j and sub(at[f'IMPORT_E{j}'],'M1')and sub('M1',at[f'IMPORT_E{j}'])
                tag=int(n[1:])-3;v[n]^=1<<(222+tag);history.append((n,at[n],v[n]));events.append({'principal':n,'old_zero_based_step':step,'payload_column':222+tag})
            if kind=='INIT':v[n]=0;at[n]=q[0];history.append((n,at[n],0))
            elif kind=='ADD':v[q[0]]^=v[n];history.append((q[0],at[q[0]],v[q[0]]))
            elif kind=='MOVE':at[n]=q[0];history.append((n,at[n],v[n]))
            elif kind=='CLEAR':del v[n],at[n]
        assert len(events)==3
        witnesses=[]
        for q,demands in WITNESSES.items():
            indices=demands+[q];mask=sum(1<<j for j in indices);counts=[]
            assert set(demands)<=set(w['targets'])
            for i in indices:
                assert all(sum(x*y for x,y in zip(roots[i],roots[j]))!=0 for j in indices)
                assert not sub('M1',f'F{i}')
                visible=[(n,c,r)for n,c,r in history if sub(c,f'F{i}')]
                for n,c,r in visible:
                    tags=r>>222;assert tags<8
                    assert r&mask==sum(1<<demands[k]for k in range(3)if tags>>k&1),(pin,q,i,n,c)
                counts.append({'receiver':i,'visible_actual_observations':len(visible)})
            for k in range(3):assert any(c=='zero'and r>>222==1<<k and r&mask==1<<demands[k]for n,c,r in history)
            # Either a new raw input or a threatened old output, if granted
            # unconditionally, violates the exact untagged-row hypothesis.
            assert (1<<q)&mask!=0 and (1<<demands[0])&mask!=0
            witnesses.append({'input':q,'old_demands':demands,'receiver_checks':counts,'M1_invisible_to_all_four':True,'common_channels_present':3,'raw_grant_controls_break_projection':True})
        reports.append({'word_sha256':pin,'source_sha256':w['source_sha256'],'all222_replay':ordinary,'injection_sites':events,'witnesses':witnesses})
    output={'status':'PASS_ROOT_INDEPENDENT_LATE_INJECTION_HYPOTHESES','method':'Independent Fraction-chart replay and one225-column provenance stream; no author source/tag engine imported.','words':reports,'universal_scope':'Separate indistinguishability proof covers arbitrary block-linear payloads and source-only nonlinear payload functions in the declared fixed-route interface. It excludes neither changed source-wide codes nor added common measurements.','new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(output,indent=2)+'\n');print(output['status'])

if __name__=='__main__':main()
