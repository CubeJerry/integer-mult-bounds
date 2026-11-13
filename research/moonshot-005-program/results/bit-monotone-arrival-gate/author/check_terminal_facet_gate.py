#!/usr/bin/env python3
"""Exact geometry premises for terminal normalization of descending packets."""
import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
SP='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
HP='ade07c8fdd0393f22d7a71c994af545c3d1569031b5aa617949105648ed6f77a'
def need(q,m):
    if not q:raise ValueError(m)
def rref(rows):
    a=[[F(x) for x in r] for r in rows];k=0
    for j in range(8):
        p=next((t for t in range(k,len(a)) if a[t][j]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k];c=a[k][j];a[k]=[x/c for x in a[k]]
        for t in range(len(a)):
            if t!=k and a[t][j]:
                c=a[t][j];a[t]=[x-c*y for x,y in zip(a[t],a[k])]
        k+=1
    return tuple(tuple(r) for r in a[:k])
def main(a):
    b=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(b).hexdigest()==SP,'Native pin')
    n=json.loads(gzip.decompress(b));frames={int(k):v for k,v in n['frames'].items()}
    p=a.repo/'research/moonshot-005-program/results/bit-clean-source-cache-gate/SOURCE-SCREEN.json'
    need(hashlib.sha256(p.read_bytes()).hexdigest()==HP,'Previously independently replayed clean-history pin')
    h=json.loads(p.read_text());need(h['pure_X_endpoint_restored'] and len(h['histories'])==1027,'Actual clean source premise')
    roots=[[F(x) for x in frames[n['start'][i]]['B'][0]] for i in range(111)]
    geom={c:rref(f['B']) for c,f in frames.items()}
    history_charts={r['chart'] for r in h['histories'] if r['row']};actual={geom[c]:[] for c in history_charts}
    for c in history_charts:actual[geom[c]].append(c)
    need(len(actual)==len(history_charts)==389,'No source-history geometric duplicates hidden')
    final=[n['final'][i+111] for i in range(111)]
    need(all(len(geom[c])==7 for c in final),'All receiver facets dimension7')
    need(len({geom[c] for c in final})==111,'Distinct geometric receiver facets')
    rows=[];visited=[];missing=[]
    for i,c in enumerate(final):
        S=[j for j in range(111) if i!=j and sum(x*y for x,y in zip(roots[i],roots[j]))==0]
        need(all(all(sum(F(x)*y for x,y in zip(ar,roots[j]))==0 for ar in frames[c]['A']) for j in S),'Foreign roots are inside actual Fi')
        need(any(sum(F(x)*y for x,y in zip(ar,roots[i]))!=0 for ar in frames[c]['A']),'Own root excluded')
        chosen=[];basis=()
        for j in S:
            bb=rref([roots[k] for k in chosen]+[roots[j]])
            if len(bb)>len(basis):chosen.append(j);basis=bb
            if len(basis)==7:break
        need(basis==geom[c],'Foreign support spans full exact rational facet')
        aliases=actual.get(geom[c],[])
        (visited if aliases else missing).append(i)
        rows.append({'receiver':i,'final_facet_chart':c,'foreign_support_size':len(S),'independent_foreign_root_roles':chosen,'foreign_root_span_dimension':7,'actual_source_history_chart_aliases':sorted(aliases)})
    need(len(visited)==57 and len(missing)==54,'Exact missing-final-facet census')
    out={'status':'PASS_EXACT_TERMINAL_NORMALIZATION_GEOMETRY_PREMISES','native_sha256':SP,'clean_history_screen_sha256':HP,
        'method':'Exact Fraction RREF compares geometric subspaces, not chart identifiers; explicit7-root bases for every foreign support.',
        'distinct_receiver_facets':111,'source_history_charts':389,'facets_with_some_actual_X_history':57,
        'facets_without_X_history':54,'covered_receivers':visited,'missing_receivers':missing,'per_receiver':rows,
        'necessary_monotone_packet_paths_in_canonical_terminal_interface':54,
        'nine_packet_coverage_deficit':45,
        'scope':'Finite geometry premises only. Universal terminal-normalization/final-facet proof is separate; nonmonotone packets, discarded global states, changed source and noncanonical terminal codes are excluded.'}
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','facets_with_some_actual_X_history','facets_without_X_history','nine_packet_coverage_deficit']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
