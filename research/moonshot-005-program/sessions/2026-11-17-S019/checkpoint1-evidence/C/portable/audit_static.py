#!/usr/bin/env python3
"""Independent finite source-space and reset checks for recovered cp6 BIT data."""
import argparse,hashlib,json
from pathlib import Path
from audit_cp6 import CP,N,replay,insist,binary_basis,in_span

def mask(row):return sum(1<<i for i in row)

def separating_delta(rows,i):
    # Solve row.delta=0, delta_i=1 independently from a pivoted augmented system.
    system=[(mask(r),0)for r in rows]+[(1<<i,1)];piv={}
    for a,b in system:
        while a:
            c=(a&-a).bit_length()-1
            if c in piv:
                z,t=piv[c];a^=z;b^=t
            else:piv[c]=(a,b);break
        else:insist(b==0,'unexpected decodability in terminal witness')
    out=0
    for c,(a,b)in sorted(piv.items(),reverse=True):
        if ((a&out).bit_count()&1)!=b:out|=1<<c
    insist(out>>i&1 and all((mask(r)&out).bit_count()%2==0 for r in rows),'direct separating witness check')
    return [j for j in range(N)if out>>j&1]

def closure(v,known,fields,R):
    known=set(known);globalrows=[v[n]for n in fields];waves=[]
    while True:
        new=[]
        for i in set(range(N))-known:
            local=[{j}for j in range(N)if sum(a*b for a,b in zip(R[i],R[j]))==0]
            obs=globalrows+[{j}for j in known]+local
            if in_span({i},binary_basis(obs)):new.append(i)
        if not new:break
        waves.append(sorted(new));known|=set(new)
    witnesses={}
    for i in set(range(N))-known:
        local=[{j}for j in range(N)if sum(a*b for a,b in zip(R[i],R[j]))==0]
        witnesses[i]=separating_delta(globalrows+[{j}for j in known]+local,i)
    return {'known':sorted(known),'waves':waves,'terminal_count':len(known),'nonlinear_indistinguishability_witnesses':witnesses,'granted_fields':fields}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();cache={}
    def state(path):
        if path not in cache:
            w=json.loads((a.evidence/path).read_text());source=json.loads((a.repo/w['source_path']).read_text());cut=w['carrier_interface_before_operation'];stats,snaps,C,events=replay(w,source,[cut]);cache[path]=(w,source,stats,snaps[cut],C)
        return cache[path]
    w,source,stats,(v,loc),C=state('A/ascending-canonical3/WORD.json');R=source['native_roots'];modes=['ZFIRST3','ZFIRST4','ZFIRST5'];old=['KEEP_C0','KEEP_C1','KEEP_C2'];groups=sorted(n for n in v if n.startswith('ASC_GROUP_'));insist(len(groups)==7,'actual seven group owners')
    cases={}
    for label,fields,expected in [('three',modes,46),('six',modes+old,48),('groups',modes+old+groups,49)]:
        c=closure(v,w['targets'],fields,R);insist(c['terminal_count']==expected,('actual static closure',label));cases[label]=c
    oldv,oldloc=v,loc
    nw,_,_,(nv,nloc),NC=state('A/ascending-canonical3-native65/WORD.json')
    extra=set(nv)-set(oldv);insist(len(extra)==65,'exact native65 extra fields')
    for n,z in oldv.items():insist(nv[n]==z and NC[nloc[n]]==C[oldloc[n]],('old source unchanged under native65',n))
    unknown=set(range(N))-set(w['targets'])
    for i in unknown:insist(any(nv[n]=={i}and NC[nloc[n]]==NC[f'L{i}']for n in extra),('actual native65 input',i))
    # Full named-interface covariance, not merely common source span equality.
    mw,_,_,(mv,mloc),MC=state('C/canonical3-reset-source/MATCHED-CUT-WORD.json');S=set(w['targets'])|{61,67};named=[]
    for n,z in oldv.items():
        insist(n in mv and (set(mv[n])^set(z))<=S and MC[mloc[n]]==C[oldloc[n]],('matched old name and all nonknown columns',n));named.append(n)
    insist(len(named)==323,'all323 old cut records compared')
    fw,_,_,(fv,floc),FC=state('C/canonical3-reset-source/LIBERATED-CACHED48-WORD.json')
    fresh=closure(fv,fw['targets'],modes+sorted(n for n in fv if n.startswith('ASC_GROUP_')),R);insist(fresh['waves']==[[5]]and fresh['terminal_count']==49,'fresh48 code has exactly one new static demand')
    # Check supplied12-color certificate directly from source roots and actual native custody.
    partition=[[5,15,18,68,71,81,85],[13,17,31,53,84,101,103],[14,25,91,94,96,102],[24,26,66,72,90,92],[32,52,62,87,99,109],[34,58,60,82,97,105],[51,55,59,70,95,100],[33,56,57,63,83],[35,54,86,107],[88,93,106,108],[47,69,89],[98,104,110]]
    insist(sorted(i for g in partition for i in g)==sorted(set(range(N))-set(fw['targets'])),'12 groups exactly partition unknown63')
    for g in partition:
        for i in g:
            insist(any(z=={i}and FC[floc[n]]==FC[f'L{i}']for n,z in fv.items()),('actual unknown native field',i))
            for j in g:
                if i!=j:insist(sum(a*b for a,b in zip(R[i],R[j]))==0,'actual group orthogonality')
    report={'status':'PASS_FRESH_STATIC_DUALS_AND_ALL_NAMED_RESET_COVARIANCE','ascending_static_cases':cases,'independent_terminal_witness_count':sum(len(c['nonlinear_indistinguishability_witnesses'])for c in cases.values()),'all323_old_cut_record_names':named,'native65_old_cut_values_and_charts_preserved':True,'fresh48_static_case':fresh,'acyclic_witness_cover':partition,'scope':'Every witness is recomputed from actual replay rows. Fixed observations only; new measurements/histories remain outside this static bound.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'STATIC-RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(report['status']);print('190 witnesses',report['independent_terminal_witness_count'],'fresh closure',fresh['terminal_count'],'matched records',len(named))
if __name__=='__main__':main()
