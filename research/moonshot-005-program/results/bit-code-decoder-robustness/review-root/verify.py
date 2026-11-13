#!/usr/bin/env python3
"""Independent reversed-basis/Gray-code review of the punctured BIT code."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(q,m):
    if not q:raise ValueError(m)
def main(a):
    b=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    need(hashlib.sha256(b).hexdigest()==PIN,'Native source')
    w=json.loads(gzip.decompress(b));frames={int(k):v for k,v in w['frames'].items()}
    roots=[]
    for i in range(111):
        v=[Fraction(x) for x in frames[w['start'][i]]['B'][0]]
        need(len(v)==8 and sum(x*x for x in v) in (1,4),'Actual root line')
        roots.append(v)
    rows=[]
    for i in range(111):
        rows.append(sum(1<<j for j in range(111) if j==i or sum(x*y for x,y in zip(roots[i],roots[j]))==0))
    echelon={};base=[];roles=[]
    for i in reversed(range(111)):
        q=rows[i]
        while q:
            p=(q&-q).bit_length()-1
            if p not in echelon:echelon[p]=q;base.append(rows[i]);roles.append(i);break
            q^=echelon[p]
    need(len(base)==9,'Source fitting rank9')
    minima=[112]*111;witness=[None]*111;counts=[0]*111;weights=Counter();seen=set();word=last=0
    for t in range(1,512):
        gray=t^(t>>1);change=gray^last;need(change and change&(change-1)==0,'Gray edge')
        word^=base[change.bit_length()-1];last=gray
        need(word and word not in seen,'Distinct nonzero word');seen.add(word);weights[word.bit_count()]+=1
        for i in range(111):
            if not(word>>i&1):
                counts[i]+=1;weight=(word&~rows[i]).bit_count()
                if weight<minima[i]:minima[i]=weight;witness[i]=hex(word)
    need(len(seen)==511 and min(weights)==48,'Complete code/minimum weight')
    need(set(counts)=={255} and min(minima)==18 and max(minima)==23,'All punctured distances')
    author=json.loads((a.author/'CODE-CERTIFICATE.json').read_text())
    need(minima==[r['minimum_noncontact_weight_with_diagonal_zero'] for r in author['per_receiver']],'Independent111 distances')
    for i,r in enumerate(author['per_receiver']):
        q=int(r['attaining_word_hex'],16)
        need(q in seen and not(q>>i&1) and (q&~rows[i]).bit_count()==minima[i],'Author attainment verified')
    need(all(r in seen and (r&~r)==0 and r>>i&1 for i,r in enumerate(rows)),'Zero-diagonal hypothesis essential')
    need(any(v==18 for v in minima),'False distance19 claim rejected')
    cp=a.repo/'research/moonshot-005-program/results/bit-clean-source-cache-gate/review-root/RESULT.json'
    need(hashlib.sha256(cp.read_bytes()).hexdigest()=='4ad1cd42d404684ff0084702bd3a73bc9fa268ef39d9039830f318f63a390ff0','Independently reviewed root path premise')
    prior=json.loads(cp.read_text())
    gaps=[r['minimum_private_ports_outside_any_one_suffix_chain'] for r in prior['per_receiver']]
    need([r['receiver'] for r in prior['per_receiver']]==list(range(111)),'Receiver indexing')
    qualified=[i for i in range(111) if minima[i]>=19 and gaps[i]>=19]
    need(len(qualified)==39 and len(qualified)>18,'Pigeonhole strengthens exception support requirement to19')
    caps={1:1,2:2,4:9,6:12,7:13}
    possible=[]
    for a1 in range(8):
      for a2 in range(4):
       for a4 in range(2):
        for a6 in range(2):
         for a7 in range(2):
          count={1:a1,2:a2,4:a4,6:a6,7:a7};mass=sum(r*c for r,c in count.items())
          if mass<=7:possible.append(sum(caps[r]*c for r,c in count.items()))
    need(max(possible)==13 and max(possible)<19,'At least total birth dimension8 for support19')
    bp=a.repo/'research/moonshot-005-program/results/bit-clean-source-cache-gate/fresh-budget/RESULT.json'
    need(hashlib.sha256(bp.read_bytes()).hexdigest()=='49dd9f4746e4cceed378726a7ae4dbf3da97a1ced9bafaffde3479135419aa51','Complete old budget receipt')
    oldroom=json.loads(bp.read_text())['maximum_additional_allowance']
    den=10**55;v=8**199*den**200;lo=0;hi=8*den+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=v:lo=mid
        else:hi=mid
    need(lo**200<=v<(lo+1)**200,'Directed rank8 price')
    deficit=[Fraction(lo,den)-Fraction(oldroom['upper']),Fraction(lo+1,den)-Fraction(oldroom['lower'])]
    need(deficit[0]>Fraction(22100976731661684,10**16),'Strict complete limiting movement deficit')
    out={'status':'PASS_INDEPENDENT_PUNCTURED_CODE_AND_DECODER_THEOREM_PREMISES','source_sha256':PIN,
        'independent_method':'Direct rational-contact rows; reversed role order, least-bit elimination, Gray-code traversal.',
        'basis_source_roles':roles,'nonzero_words':511,'minimum_code_weight':48,
        'per_receiver_minimum_noncontact_weight_with_zero_diagonal':minima,
        'independent_attaining_word_hex':witness,'distance_histogram':dict(sorted(Counter(minima).items())),
        'minimum_distance':18,'maximum_distance':23,'negative_controls':['Removing zero-diagonal condition admits every K row with noncontact weight0.','Uniform distance19 is contradicted by exact attained18.'],
        'root_strengthening':{'qualified_receivers_with_both_bounds_at_least19':qualified,'qualified_count':39,
            'extra_support_sizes_excluded_through':18,'necessary_extra_input_support':19,
            'maximum_input_support_with_total_fresh_birth_dimension_at_most7':13,
            'necessary_total_fresh_birth_dimension':8,'movement_lower_bound':'8^(199/200)',
            'complete_limiting_movement_deficit_exact_bounds':list(map(str,deficit)),
            'scope':'Uses per-receiver punctured distance plus independently reviewed exception gap, not a uniform code distance19.'},
        'scope':'Finite code premises. Separate review proves all-field/block and arbitrary-decoder/timing extension; no arbitrary tour tariff is inferred.'}
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
