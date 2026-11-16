"""Independent literal word, changed-code witness and exact price audit."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse, hashlib, json, sys

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--closure',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    sys.path.insert(0,str(a.engine));from check import replay,rank,need
    from budget import budget,moment
    data=a.word.read_bytes();pin=hashlib.sha256(data).hexdigest();assert pin=='1da8ac07063da93aaf002fa6feeb6de4ec1aa327a7740f3f61747abd559d14d0'
    w=json.loads(data);source=json.loads(a.source.read_text());raw=(a.repo/w['source_path']).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==w['source_sha256']==source['native_source_sha256'];R=json.loads(raw)['native_roots']
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));mask=lambda js:sum(1<<j for j in js)
    L=[mask(j for j in range(111) if dot(i,j)==0) for i in range(111)];C=[L[i]^(1<<i) for i in range(111)]
    h=[int((i!=72 and dot(72,i)!=0)^(sum(x*y for x,y in zip([0,0,1,1,0,0,1,-1],r))!=0)) for i,r in enumerate(R)]
    W=[C[i]&mask(j for j in range(111) if h[j]==h[i]) for i in range(111)]
    U=[W[i] for i in [3,76,80,4,74,78]]+[int(x,16) for x in source['canonical_pair_hex']]
    assert rank(U)==8 and rank(U+C)==12 and rank(U+W)==16
    assert all(rank(C+[u])==9 for u in U[-2:])
    I=source['frame'];P=source['optional_point_set'];lam=mask(source['functional_support']);s=int(source['baseline_unit_source_row'],16)
    assert len(I)==len(set(I))==8 and all(dot(i,j)!=0 for i in I for j in I)
    assert rank([u&mask(I) for u in U])==5 and rank(U+[s])==8 and s&mask(I)==1
    assert not(lam&L[0]) and lam&1 and not(lam&mask(P)) and not(mask(I)&mask(P))
    assert all((u&lam).bit_count()%2==0 for u in U)
    assert [rank(U+[1<<j for j in Q])+9-rank(U+[1<<j for j in Q]+C) for Q in [[],P]]==[5,5]
    closure=json.loads(a.closure.read_text());assert closure['first_fitting_set']==closure['second_fitting_set']==P
    for grants in [source['early_point_grants'],P]:
        BB=U+[1<<j for j in grants];got=[]
        for i in range(111):
            nl=((1<<111)-1)^L[i];restricted=[v&nl for v in BB]
            if rank(restricted+[1<<i])==rank(restricted):got.append(i)
        assert got==P
    assert len(closure['outside_dual_witnesses'])==87
    for d in closure['outside_dual_witnesses']:
        i=d['receiver'];v=int(d['annihilator'],16)
        assert v==mask(d['support']) and v>>i&1 and not(v&L[i]) and not(v&mask(P))
        assert all((v&u).bit_count()%2==0 for u in U)
    def seedcut(word):
        vals={f'X{j}':1<<j for j in range(111)}|{f'Y{j}':1<<(111+j) for j in range(111)}
        for op in word['operations']:
            if op[0]=='INIT':vals[op[1]]=0
            elif op[0]=='ADD':vals[op[2]]^=vals[op[1]]
            elif op[0]=='CLEAR':del vals[op[1]]
            # The semantic cut is before the first update of any Y.
            if all(f'P{i}' in vals for i in range(8)) and op[0]=='ADD' and op[2].startswith('Y'):
                rows=[vals[f'P{i}'] for i in range(8)];need(rank(rows)==rank(rows+U)==8,'changed seed code');return rows
        raise ValueError('missing receiver phase')
    report=replay(w,R);rows=seedcut(w)
    assert [report['counts'][k] for k in ['INIT','ADD','MOVE','CLEAR']]==[71,730,381,71]
    assert rows==[int(x,16) for x in w['seed_rows_hex']]
    controls=[]
    predicates=[('new_X8_capture',lambda o:o==['ADD','X8','Hnew11_1']),
                ('new_filter_query',lambda o:o[0]=='ADD' and o[1].startswith('Hnew') and o[2].startswith('P')),
                ('early_point_capture',lambda o:o[0]=='ADD' and o[2].startswith('E')),
                ('held_query',lambda o:o[0]=='ADD' and o[1]in['X21','X64','X65'] and o[2].startswith('P')),
                ('source_compensation',lambda o:o[0]=='ADD' and o[1].startswith('X') and o[2]=='P0'),
                ('retirement',lambda o:o[0]=='CLEAR')]
    for name,pred in predicates:
        z=deepcopy(w);j=next(j for j,o in enumerate(z['operations']) if pred(o));del z['operations'][j]
        try:replay(z,R,False);seedcut(z)
        except (ValueError,AssertionError) as e:controls.append({'mutation':name,'rejected':str(e)})
        else:raise AssertionError('accepted '+name)
    invoice=budget(report['movement_profile']);old={1:58,2:56,3:36,4:35,5:69,6:19,7:106,8:1}
    delta={i:report['movement_profile'].get(i,0)-old.get(i,0) for i in range(1,9)};lo,hi=moment(delta)
    assert 0<lo<hi<Fraction(23,10000)
    four_rank2=moment({2:4})[0];room_hi=Fraction(invoice['limiting_room']['upper_fraction']);assert four_rank2>room_hi
    with localcontext() as ctx:
        ctx.prec=55
        show=lambda x:str(Decimal(x.numerator)/Decimal(x.denominator))
        numbers={'movement_increase_lower':show(lo),'movement_increase_upper':show(hi),'remaining_room_upper':show(room_hi),'four_rank2_arrivals_lower':show(four_rank2)}
    out={'status':'PASS_INDEPENDENT_CHANGED_SEED_SOURCE_AND_EXACT_FOUR','word_sha256':pin,'source_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),
         'all_column_replay':report,'ground_rank':8,'canonical_intersection':5,'frame':I,'frame_rank':5,'functional_support':source['functional_support'],
         'exact_added_dimension_per_width':4,'semantic_mutations':controls,'invoice':invoice,'numbers':numbers,
         'closed_point_set':P,'point_closure_dual_witnesses':87,
         'nonlinear_scope':'Same nine-parameter injection with rank-five baseline; fixed-length finite-field static common broadcast',
         'new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])

if __name__=='__main__':main()
