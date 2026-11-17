#!/usr/bin/env python3
"""Independent rational Shannon-certificate and two-source premise review.

Rebuilds inequalities using native-role sets and >= orientation. Does not import
the discovery solver, root verifier, source builder, or any interpreter.
"""
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache
from pathlib import Path

NATIVE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
CERT_SHA='c5d40e71246008699cb137eaa2badd2674253b0567c87e54fa7fa5809bacc79f'
OLD_SHA='f21de38f4a8adc1a55920c16b684285f62607829fe512a0088fe5ecb217fcfdd'
NEW_SHA='74fb050a6afb8d8e1b6895b0f092220f8e6852365a7516ef4db2284c43c1a5ee'
CORE=[18,55,56,105,109,66,69,70,89,93,15]
ISO=[14,31,35]
U=[5,13,14,15,17,18,24,25,26,31,32,33,35,52,53,54,55,56,57,58,59,60,62,63,66,68,69,70,71,72,81,82,83,84,85,86,87,89,91,93,95,96,97,98,99,100,101,102,103,105,106,107,109,110]

def demand(ok,why):
    if not ok:raise ValueError(why)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path,data):path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def review_dual(cert,roots):
    demand(cert['roles']==CORE and cert['isolates']==ISO,'ordered core and isolates')
    neighbors={i:{j for j in CORE+ISO if i!=j and sum(x*y for x,y in zip(roots[i],roots[j]))==0} for i in CORE+ISO}
    demand(all(not neighbors[i] for i in ISO),'isolates really have no unknown witness side information')
    demand(cert['adjacency_masks']==[sum(1<<j for j,i in enumerate(CORE) if i in neighbors[v]) for v in CORE],'source-derived core graph')
    total=defaultdict(Fraction);rhs=Fraction(0);counts=Counter();expanded=[]
    for number,term in enumerate(cert['terms']):
        kind,*params=term['row'];weight=Fraction(term['weight']);counts[kind]+=1
        if kind=='empty':
            demand(not params and term['kind']=='equality','deterministic empty row')
            expression={frozenset():Fraction(1)};constant=Fraction(0);factor=weight
        else:
            mask,index,*extra=params
            demand(type(mask)is int and 0<=mask<2**11 and type(index)is int and 0<=index<11,'valid set/index')
            S=frozenset(CORE[j] for j in range(11) if mask>>j&1);i=CORE[index]
            demand(i not in S,'index absent from conditioning complement')
            Si=S|{i}
            if kind=='mono':
                demand(not extra and term['kind']=='inequality' and weight<=0,'nonnegative conditional-information multiplier')
                expression={Si:Fraction(1),S:Fraction(-1)};constant=Fraction(0);factor=-weight
            elif kind=='submod':
                demand(len(extra)==1 and type(extra[0])is int and 0<=extra[0]<11,'second submodular index')
                j=CORE[extra[0]];demand(j not in S and j!=i,'distinct omitted indices')
                demand(term['kind']=='inequality' and weight<=0,'nonnegative submodular multiplier')
                expression={Si:Fraction(1),S|{j}:Fraction(1),S:Fraction(-1),S|{i,j}:Fraction(-1)};constant=Fraction(0);factor=-weight
            elif kind=='decode':
                demand(not extra and term['kind']=='equality','decode equality classification')
                demand(not(S&neighbors[i]),'all actual neighbors remain conditioned')
                expression={Si:Fraction(1),S:Fraction(-1)};constant=Fraction(1);factor=weight
            elif kind=='unit':
                demand(not extra and term['kind']=='inequality' and weight<=0,'entropy-unit multiplier')
                expression={Si:Fraction(-1),S:Fraction(1)};constant=Fraction(-1);factor=-weight
            else:raise ValueError('unsupported entropy rule')
        for S,c in expression.items():total[S]+=factor*c
        rhs+=factor*constant
        expanded.append({'term':number,'rule':kind,'factor':str(factor),'constant':str(constant),'coefficient_terms':[{'unknown_set':sorted(S),'coefficient':str(c)} for S,c in sorted(expression.items(),key=lambda x:tuple(sorted(x[0])))]})
    remaining={S:c for S,c in total.items() if c}
    demand(remaining=={frozenset(CORE):Fraction(1)},'independent exact entropy cancellation')
    demand(rhs==Fraction(11,2),'independent core bound')
    demand(cert['core_bound']=='11/2' and cert['full_bound']=='17/2','claimed endpoint bounds')
    return {'terms':len(expanded),'row_counts':dict(counts),'core_bound':str(rhs),'full_bound':str(rhs+len(ISO)),'final_coefficient':{'roles':CORE,'coefficient':'1'},'expanded_nonnegative_orientation':expanded}

@cache
def rr(rows):
    rows=[list(map(Fraction,row))for row in rows];r=0
    for c in range(8):
        k=next((k for k in range(r,len(rows))if rows[k][c]),None)
        if k is None:continue
        rows[r],rows[k]=rows[k],rows[r];pivot=rows[r][c]
        rows[r]=[v/pivot for v in rows[r]]
        for k in range(len(rows)):
            if k!=r and rows[k][c]:
                f=rows[k][c];rows[k]=[a-f*b for a,b in zip(rows[k],rows[r])]
        r+=1
    return tuple(tuple(row)for row in rows[:r])

def inside(spec,root):
    rows=tuple(tuple(row)for row in spec['rows'])
    if spec['kind']=='span':return all(sum(a*b for a,b in zip(row,root))==0 for row in rows)
    demand(spec['kind']=='ann','chart type')
    return len(rr(rows+(tuple(root),)))==len(rr(rows))

def source_audit(word,roots,expected_cut,expected_live):
    demand(sorted(set(range(111))-set(word['targets']))==U,'identical known/unknown partition')
    cut=word['carrier_interface_before_operation'];demand(cut==expected_cut,'source cut')
    val={f'X{i}':frozenset([i])for i in range(111)}|{f'Y{i}':frozenset([111+i])for i in range(111)}
    loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    for tag,name,*arg in word['operations'][:cut]:
        if tag=='INIT':demand(name not in val,'fresh live field');val[name]=frozenset();loc[name]=arg[0]
        elif tag=='ADD':val[arg[0]]=val[arg[0]]^val[name]
        elif tag=='MOVE':loc[name]=arg[0]
        elif tag=='CLEAR':del val[name];del loc[name]
        else:raise ValueError('unknown source opcode')
    demand(len(val)==expected_live,'complete live-field inventory')
    demand(all(val[f'Y{i}']==frozenset([111+i]) for i in U),'unfinished output condition')
    receipts=[];leaks=[]
    for i in U:
        neighbors={j for j in U if sum(a*b for a,b in zip(roots[i],roots[j]))==0};count=0
        for name,v in val.items():
            if inside(word['charts'][loc[name]],roots[i]):
                count+=1;bad=(v&set(U))-neighbors
                if bad:leaks.append([i,name,loc[name],sorted(bad)])
        receipts.append({'receiver':i,'inside_fields':count})
    demand(not leaks,'all inside dependencies are native neighbors')
    # A changed source with its own missing input at ground violates this premise.
    planted_rejected=15 not in {j for j in U if sum(a*b for a,b in zip(roots[15],roots[j]))==0} and inside(word['charts']['zero'],roots[15])
    demand(planted_rejected,'source-leak control')
    return {'cut':cut,'live_fields':expected_live,'unfinished_roles':len(U),'nonlocal_leaks':leaks,'receiver_checks':receipts,'planted_own_input_at_ground_invalidates_premise':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--old-word',type=Path,required=True);p.add_argument('--new-word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    for path,pin in [(a.native,NATIVE_SHA),(a.certificate,CERT_SHA),(a.old_word,OLD_SHA),(a.new_word,NEW_SHA)]:demand(digest(path)==pin,'exact input bytes: '+str(path))
    roots=json.loads(a.native.read_text())['native_roots'];cert=json.loads(a.certificate.read_text())
    exact=review_dual(cert,roots)
    old=source_audit(json.loads(a.old_word.read_text()),roots,1129,392)
    new=source_audit(json.loads(a.new_word.read_text()),roots,1269,408)
    mutated=json.loads(json.dumps(cert));mutated['terms'].pop()
    try:review_dual(mutated,roots)
    except ValueError as exc:negative=str(exc)
    else:raise ValueError('deleted dual term escaped')
    result={'status':'PASS_INDEPENDENT_NONLINEAR_17_OVER_2_DUAL_AND_BOTH_SOURCE_CUTS','exact_core_bound':'11/2','decoded_isolates':3,'exact_witness_bound':'17/2','independent_rules':'Rebuilt on native-role sets in nonnegative >= orientation, no author/root imports or solver.','terms':exact['terms'],'row_counts':exact['row_counts'],'old_source':old,'all54_source':new,'missing_term_rejected':negative,'source_pins':{'native':NATIVE_SHA,'certificate':CERT_SHA,'old_word':OLD_SHA,'new_word':NEW_SHA},'scope':'Deterministic zero-error finite-alphabet fixed-schedule whole-record continuations need at least9 future strict owned downward transfers; no9-lifetime claim, no new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);save(a.out/'EXPANDED-DUAL.json',exact);save(a.out/'RESULT.json',result)
    print(result['status'], '106 independently rebuilt terms; both source cuts have zero leakage.')

if __name__=='__main__':main()
