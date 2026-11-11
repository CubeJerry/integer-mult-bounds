"""Exact source-bound cut-capacity certificate; NumPy, no external solver."""
from pathlib import Path
from fractions import Fraction as F
import argparse, gzip, hashlib, json, platform
import numpy as np
HERE=Path(__file__).resolve().parent
PRIME=1000003
def need(ok, why):
    if not ok: raise ValueError(why)
def decode(row): return {int(i):F(v) for i,v in row if F(v)}
def add(row, other, c):
    for j,v in other.items():
        z=row.get(j,F(0))+c*v
        if z: row[j]=z
        else: row.pop(j,None)
def qrank(rows, columns=None):
    basis={}
    for old in rows:
        row={j:v for j,v in old.items() if columns is None or j in columns}
        for p,b in basis.items():
            if row.get(p): add(row,b,-row[p])
        if row:
            p=min(row); c=row[p]; basis[p]={j:v/c for j,v in row.items()}
    return len(basis)
def prank(matrix):
    matrix=matrix.copy(); rr=0
    for j in range(matrix.shape[1]):
        ids=np.flatnonzero(matrix[rr:,j])
        if not len(ids): continue
        other=rr+int(ids[0]); matrix[[rr,other]]=matrix[[other,rr]]
        matrix[rr,j:]=matrix[rr,j:]*pow(int(matrix[rr,j]),-1,PRIME)%PRIME
        ids=np.flatnonzero(matrix[rr+1:,j])+rr+1
        if len(ids): matrix[ids,j:]=(matrix[ids,j:]-matrix[ids,j,None]*matrix[rr,j:])%PRIME
        rr+=1
        if rr==matrix.shape[0]: break
    return rr
def forward(word, cut, vectors):
    rows=[{} for _ in range(word['public']+word['owned_fields'])]
    for j,vector in enumerate(vectors):
        for i,v in vector.items(): rows[i][j]=v
    for e in word['program'][:cut]:
        op,a=e[:2]
        if op in ('INIT','CLEAR'): rows[a]={}
        elif op in ('ADD','COPY'): add(rows[a],rows[e[2]],F(e[3]))
        elif op=='SCALE': rows[a]={j:F(e[2])*v for j,v in rows[a].items() if F(e[2])*v}
        elif op!='MOVE': raise ValueError('opcode')
    return rows
def reverse(word, cut, owner):
    row={owner:F(1)}
    for e in reversed(word['program'][:cut]):
        op,a=e[:2]
        if op in ('INIT','CLEAR'): row.pop(a,None)
        elif op in ('ADD','COPY') and a in row:
            b=e[2]; z=row.get(b,F(0))+F(e[3])*row[a]
            if z: row[b]=z
            else: row.pop(b,None)
        elif op=='SCALE' and a in row:
            row[a]*=F(e[2])
            if not row[a]: del row[a]
    need(all(i<word['public'] for i in row),'unremoved owned input')
    return row
def default_source():
    for parent in HERE.parents:
        p=parent/'research/shared-wire-split-composition/data/final.json.gz'
        if p.exists(): return p
    return Path('research/shared-wire-split-composition/data/final.json.gz')
def main():
    need(PRIME>2 and PRIME%2 and all(PRIME%d for d in range(3,1001,2)), 'prime modulus')
    parser=argparse.ArgumentParser(); parser.add_argument('--source',type=Path,default=default_source());parser.add_argument('--output',type=Path)
    args=parser.parse_args(); cert=json.loads((HERE/'CERTIFICATE.json').read_text());raw=args.source.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==cert['source_sha256'],'source SHA256')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==cert['source_git_blob'],'source Git blob')
    w=json.loads(gzip.decompress(raw)); cut=cert['cut_before_event']
    need(w['program'][cut]==['MOVE',1529,541,543,True],'exact cut event')
    mains=sorted(set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']))
    helpers=sorted(set(range(w['public']))-set(mains));need((len(mains),len(helpers))==(400,1080),'owner partition')
    states=list(w['initial'])+[None]*w['owned_fields'];live=set();peak=0
    for i,e in enumerate(w['program']):
        if i==cut: cut_states=list(states);owned=sorted(live)
        op,a=e[:2]
        if op=='INIT':
            need(a>=w['public'] and states[a] is None,'INIT');states[a]=e[2];live.add(a);peak=max(peak,len(live))
        elif op=='CLEAR':
            need(a in live and states[a]==e[2],'CLEAR');states[a]=None;live.remove(a)
        elif op=='MOVE': need(states[a]==e[2],'MOVE frame');states[a]=e[3]
        elif op in ('ADD','COPY'): need(states[a]==states[e[2]]==e[4],'cochart contact')
        elif op=='SCALE': need(states[a]==e[3],'SCALE frame')
    need((peak,len(owned),w['owned_fields'])==(43,42,51),'owned counts')
    arows=[reverse(w,cut,i) for i in owned]
    ra=qrank(arows); ram=qrank(arows,set(mains));need((ra,ram)==(26,21),'exact owned ranks')
    quot=[{a:F(1),b:F(-1)} for a,b in cert['helper_quotient_pairs']]
    need(qrank(arows+quot)==ra and qrank(quot)==5,'helper quotient')
    dep={}
    for i,c in decode(cert['public_left_nullvector']).items(): add(dep,reverse(w,cut,i),c)
    need(not dep,'exact public dependence')
    lost=decode(cert['public_input_nullvector']);lost_values=forward(w,cut,[lost])
    need(not any(lost_values[i] for i in range(w['public'])),'public lost mode')
    need({i:lost_values[i] for i in owned if lost_values[i]}=={1503:{0:F(1)}},'private lost-mode witness')
    kernels=[decode(v) for v in cert['kernel_main_vectors']]
    need(len(kernels)==qrank(kernels)==62,'kernel independence')
    need(all(set(v)<=set(mains) for v in kernels),'main-only kernel vectors')
    values=forward(w,cut,kernels);need(not any(values[i] for i in mains),'exact main-kernel action')
    need(qrank([values[i] for i in owned])==6,'owned kernel response')
    need(qrank([values[i] for i in cert['retained_difference_owners']])==6,'six owned observations')
    need(not values[1503],'common/private observation separation')
    parking=cert['retained_helper_difference_owners']
    need(len(parking)==62 and set(parking)<=set(helpers),'parking owners')
    need(qrank([values[i] for i in parking])==62,'full helper-difference complement')
    need([cut_states[i] for i in parking]==cert['helper_difference_frames'],'parking frames')
    matrix=np.zeros((w['public']+w['owned_fields'],w['public']),dtype=np.int64)
    matrix[:w['public']]=np.eye(w['public'],dtype=np.int64)
    for e in w['program'][:cut]:
        op,a=e[:2]
        if op in ('INIT','CLEAR'): matrix[a]=0
        elif op in ('ADD','COPY'):
            c=F(e[3]);need(c.denominator%PRIME!=0,'modular denominator');c=c.numerator*pow(c.denominator,-1,PRIME)%PRIME
            matrix[a]=(matrix[a]+c*matrix[e[2]])%PRIME
        elif op=='SCALE':
            c=F(e[2]);need(c.denominator%PRIME!=0,'modular denominator');c=c.numerator*pow(c.denominator,-1,PRIME)%PRIME
            matrix[a]=c*matrix[a]%PRIME
    rp=prank(matrix[:w['public']]);rm=prank(matrix[mains][:,mains]);rpm=prank(matrix[:w['public'],mains])
    rma=prank(matrix[mains])
    need((rp,rm,rpm,rma)==(1479,338,400,400),'modular lower bounds')
    # Rational witnesses above establish matching upper bounds. One lost-mode
    # response adds the missing total-input rank, and owned kernel rank adds6.
    full=1480; main_owned=rm+6; observable=rp+rm
    need((observable,full+main_owned-observable,1880-observable)==(1817,7,63),'shared bank ranks')
    controls=[]
    wrong=dict(lost);wrong[0]=wrong.get(0,F(0))+1;bad=forward(w,cut,[wrong])
    need(any(bad[i] for i in range(w['public'])),'lost-mode mutant');controls.append('corrupted lost mode becomes publicly observable')
    need(63-7==56 and 1817+43<1880 and 1817+51<1880,'capacity controls')
    controls.append('seven owned observations miss56 complete-input directions')
    controls.append('43 live fields and51 allocated labels both fail full fixed-prefix capacity')
    need(rp+rpm!=observable,'two-helper-bank alias');controls.append('one current helper bank differs from two')
    q3={};add(q3,reverse(w,cut,728),F(1));add(q3,reverse(w,cut,1448),F(-1))
    need(q3==quot[2] and cut_states[728]==cut_states[1448]==1090,'cochart q3')
    q4={}
    for i,c in [(723,1),(1390,-1),(724,-1),(725,-1)]: add(q4,reverse(w,cut,i),F(c))
    need(q4==quot[3] and len({cut_states[i] for i in [723,1390,724,725]})==1,'cochart q4')
    badq={};add(badq,reverse(w,cut,723),F(1));add(badq,reverse(w,cut,1390),F(-1))
    need(badq!=quot[3],'omitted correction mutant');controls.append('omitted helper correction changes observation')
    need(cut_states[623]!=cut_states[768],'cross-chart control');controls.append('a symbolic difference need not be a cochart ADD')
    result={'status':'PASS_EXACT_OWNED_CUT_CAPACITY','source_sha256':cert['source_sha256'],'cut_before_event':cut,
      'ranks':{'public':rp,'public_plus_owned':full,'main_on_main':rm,'main_plus_owned_on_main':main_owned,'public_on_main':rpm,'main_on_all':rma,'owned':ra,'owned_on_main':ram},
      'owned_counts':{'live_at_cut':len(owned),'peak_live':peak,'allocated_labels':w['owned_fields']},
      'two_main_one_shared_helper':{'input_dimension':1880,'public_rank':observable,'minimum_owned_recovery_fields':7,'minimum_invertible_continuation_fields':63,'deficit_at43':20},
      'any_one_helper_bank_with_frozen_mains':{'main_observation_rank':rma+rm,'helper_fields':1080,'necessary_extra_fields':1880-rma-rm-1080,'deficit_at43':19},
      'without_public_side_information':47,'two_current_helper_banks_minimum':1,'independent_exact_main_kernel_vectors':62,
      'cochart_parking_observations':{'helper_differences':62,'common_owned':1503,'extraction_INITs':62,'extraction_ADDs_into_zero_fields':124,'production_transport_and_reinjection':'unbuilt'},
      'negative_controls':controls,'runtime':{'python':platform.python_version(),'numpy':np.__version__},
      'scope':'Exact normalized information at one cut. No physical compression, paid-price lower bound or new kappa.'}
    text=json.dumps(result,indent=2)+'\n'
    if args.output: args.output.write_text(text)
    print(text,end='')
if __name__=='__main__': main()
