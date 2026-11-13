#!/usr/bin/env python3
"""Source-exact rank-nine BIT lead; not a completed native or supplier."""
import argparse, collections, gzip, hashlib, json
from fractions import Fraction as F
from pathlib import Path

PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'

def need(test,message):
    if not test:raise ValueError(message)

def insert(basis,value,witness):
    while value:
        p=value.bit_length()-1
        if p not in basis:basis[p]=(value,witness);return True
        old,mask=basis[p];value^=old;witness^=mask
    return False

def solve(basis,value):
    witness=0
    while value:
        p=value.bit_length()-1
        if p not in basis:return None
        old,mask=basis[p];value^=old;witness^=mask
    return witness

def main(args):
    raw=(args.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'BIT source pin')
    s=json.loads(gzip.decompress(raw));frames={int(k):v for k,v in s['frames'].items()}
    need(s['public']==659,'Source public count')
    roots=[[F(x) for x in frames[s['start'][i]]['B'][0]] for i in range(111)]
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    need(all(dot(r,r) in (1,4) for r in roots),'Root normalization')
    g2=[[int(x*(2 if dot(r,r)==1 else 1)) for x in r] for r in roots]
    need(all(dot(r,r)==4 for r in g2),'Unit source root coordinates')
    krows=[];brows=[]
    for i in range(111):
        f=frames[s['final'][111+i]]
        need(f['dim']==7 and all(dot(roots[i],[F(x) for x in row])==0 for row in f['B']),'Actual final receiver facet')
        kr=br=0
        for j in range(111):
            inner=dot(g2[i],g2[j]);need(inner.denominator==1 and int(inner)%2==0,'Integral doubled root Gram')
            bit=(int(inner)//2)&1
            if bit:br|=1<<j
            else:kr|=1<<j
            need((i==j) or ((not bit)==(inner==0)),'Fitting support equals actual foreign contact')
        need(kr>>i&1,'Fitting identity diagonal');krows.append(kr);brows.append(br)
    kb={};selected=[]
    for i,row in enumerate(krows):
        if insert(kb,row,1<<len(selected)):selected.append(i)
    bb={}
    for i,row in enumerate(brows):insert(bb,row,1<<i)
    need(len(kb)==9 and len(bb)==8,'Exact binary fitting ranks')
    coordinates=[solve(kb,row) for row in krows];encoders=[krows[i] for i in selected]
    for i,mask in enumerate(coordinates):
        need(mask is not None,'Factor coordinates');row=0
        for j,encoder in enumerate(encoders):
            if mask>>j&1:row^=encoder
        need(row==krows[i],'Factored fitting identity')

    rows=[1<<i for i in range(111)];where=s['start'][:111]
    histories=[];seen=set();xpaid=collections.Counter();arithmetic=0
    def observe(event,field):
        key=(where[field],rows[field])
        if key not in seen:
            seen.add(key);histories.append({'event':event,'field':field,'chart':where[field],'row':rows[field]})
    for i in range(111):observe(-1,i)
    for event,e in enumerate(s['program']):
        op,a=e[:2]
        if a>=111:continue
        if op in ('ADD','SWAP'):
            b=e[2]
            if b>=111:continue
            need(where[a]==where[b]==e[3],'Actual pure X/X cochart')
            if op=='ADD':rows[a]^=rows[b]
            else:rows[a],rows[b]=rows[b],rows[a]
            arithmetic+=1;observe(event,a)
            if op=='SWAP':observe(event,b)
        elif op=='MOVE':
            need(where[a]==e[2],'Actual X route continuity')
            r=frames[e[3]]['dim']-frames[e[2]]['dim'];need(r>0,'Monotone X route')
            xpaid[r]+=1;where[a]=e[3];observe(event,a)
        else:raise ValueError('Unexpected main-X instruction '+str(e))
    need(rows==[1<<i for i in range(111)] and where==s['final'][:111],'Pure X skeleton endpoint')
    contain={frame:[i for i,r in enumerate(roots) if all(dot(r,[F(x) for x in row])==0 for row in record['B'])]
             for frame,record in frames.items()}
    exact=[{} for _ in roots];permissive=[{} for _ in roots]
    for j,record in enumerate(histories):
        for i in contain[record['chart']]:insert(permissive[i],record['row'],1<<j)
        for i in range(111):
            if record['chart']==s['final'][111+i]:insert(exact[i],record['row'],1<<j)
    tests=[]
    for i in range(111):
        wanted=krows[i]^(1<<i);a=solve(exact[i],wanted);b=solve(permissive[i],wanted)
        tests.append({'receiver':i,'exact_final_facet_history_rank':len(exact[i]),'all_subchart_history_rank':len(permissive[i]),
                      'desired_offdiagonal_terms':wanted.bit_count(),'exact_final_facet_recoverable':a is not None,'all_subchart_recoverable':b is not None,
                      'exact_witness_history_indices':[j for j in range(len(histories)) if a is not None and a>>j&1],
                      'permissive_witness_history_indices':[j for j in range(len(histories)) if b is not None and b>>j&1]})
    result={'status':'EXACT_SOURCE_LEAD_SCREEN_NOT_COMPLETE_NATIVE','native_sha256':PIN,
            'binary_Gram_rank':8,'fitting_rank':9,'fitting_identity_diagonal':True,'fitting_rows':krows,
            'encoder_source_rows':selected,'encoder_rows':encoders,'decoder_coordinate_masks':coordinates,
            'all_foreign_nonzero_fitting_coefficients_are_actual_contacts':True,
            'pure_X_main_ADD_SWAP_count':arithmetic,'pure_X_paid_profile':dict(sorted(xpaid.items())),
            'pure_X_history_count':len(histories),'pure_X_endpoint_restored':True,
            'exact_final_facet_complete_receiver_count':sum(t['exact_final_facet_recoverable'] for t in tests),
            'all_subchart_complete_receiver_count':sum(t['all_subchart_recoverable'] for t in tests),
            'receiver_tests':tests,'histories':histories,
            'scope':'Actual F2 fitting factor and pure main skeleton only. Permissive subchart span ignores simultaneous receiver path compatibility. No missing coefficient or extra owned transport is waived; no supplier or kappa.'}
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','binary_Gram_rank','fitting_rank','pure_X_main_ADD_SWAP_count','pure_X_paid_profile','pure_X_history_count','exact_final_facet_complete_receiver_count','all_subchart_complete_receiver_count']}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args())
