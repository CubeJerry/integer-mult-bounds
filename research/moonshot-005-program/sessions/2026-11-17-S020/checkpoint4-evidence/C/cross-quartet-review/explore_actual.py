"""Exploratory source-expiry screen for the two literal cross-quartet cuts."""
from pathlib import Path
from collections import defaultdict,Counter
from itertools import combinations
import importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=module('source',BASE/'workers/C/proper-query-export-review/check.py')
m.geo=m.load_arithmetic(BASE/'workers/C/four-plane-review/check.py')
b=module('algebra',BASE/'workers/C/direct-pair-review/check.py')
R=json.loads((BASE/'workers/C/native.json').read_text())['native_roots']
parent=json.loads((BASE/'workers/A/low-retention-corrections/WORD.json').read_text())
oldD=[int(x,16)for x in parent['Y_correction_rows_hex']]
N=[{j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0}for i in range(111)]
K=[(1<<i)^sum(1<<j for j in N[i])for i in range(111)]
oldE=set(range(8))|set(range(22,46))|set(range(88,96))
groups=defaultdict(list)
for i,r in enumerate(R):
    if i not in oldE:groups[tuple(j for j,x in enumerate(r)if x)].append(i)
halves=[]
for support,I in groups.items():
    for a,c in combinations(support,2):
        for sign in [1,-1]:halves.append(sum(1<<i for i in I if R[i][a]==sign*R[i][c]))
out={}
for name in ['cross-quartet-export-1','cross-quartet-exports-greedy']:
    w=json.loads((BASE/'workers/A'/name/'WORD.json').read_text())
    charts={n:m.geo.chart(c)for n,c in w['charts'].items()}
    stats,V,P=m.replay(w,charts,[int(x,16)for x in w['Y_correction_rows_hex']],check_cut=False)
    E=[i for i in range(111)if len(charts[P[f'X{i}']])>1]
    L={i:[v&((1<<111)-1)for n,v in V.items()if not n.startswith('NATIVE_')and m.geo.contained(charts[P[n]],charts[f'F{i}'])]for i in range(111)}
    payloads=[sum(1<<i for i in z['sources'])for z in w['construction']['fresh_cross_quartet_exports']]
    cases={}
    for label,extra in [('actual',payloads),('all_fresh_halves',halves)]:
        G=list(b.basis(K+oldD+extra).values());forced={}
        for i in range(111):
            obs=b.basis(G+L[i]);target=b.residual(1<<i,obs)
            J=sorted(set(E)&N[i]);cols={j:b.residual(1<<j,obs)for j in J}
            assert not b.residual(target,b.basis(cols.values()))
            forced[i]=[j for j in J if b.residual(target,b.basis(cols[k]for k in J if k!=j))]
        obligations={}
        for j in E:
            I=[i for i in range(111)if j in forced[i]]
            rank=len(m.geo.basis(tuple(tuple(R[i])for i in I)))
            obligations[j]={'receivers':I,'rank':rank,'exits':2 if rank==7 else 1 if I else 0}
        exits=sum(z['exits']for z in obligations.values());ground=[i for i in range(111)if not charts[P[f'Y{i}']]]
        cases[label]={'bank_rank':len(G),'expired_count':len(E),'rank_histogram':dict(Counter(z['rank']for z in obligations.values())),
                      'old_histogram':dict(Counter(z['rank']for j,z in obligations.items()if j in oldE)),
                      'fresh_histogram':dict(Counter(z['rank']for j,z in obligations.items()if j not in oldE)),
                      'native_exits':exits,'owned_upward_lower_bound':max(0,exits-len(ground)),
                      'ground_Y_roles':ground,'obligations':obligations,'forced':forced}
        print(name,label,{k:v for k,v in cases[label].items()if k not in ['obligations','forced']},flush=True)
    out[name]={'stats':stats,'cases':cases}
(Path(__file__).resolve().parent/'EXPLORATORY-SOURCE-EXPIRY.json').write_text(json.dumps(out,indent=2)+'\n')
