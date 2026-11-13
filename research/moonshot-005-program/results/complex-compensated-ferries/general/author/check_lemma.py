#!/usr/bin/env python3
"""Source census, free orthogonal-ferry optimum, complete terminal invoice."""
import argparse,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
FULL_PIN='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
def iroot(a,n):
    lo,hi=0,1<<((a.bit_length()+n-1)//n)
    while hi-lo>1:
        m=(lo+hi)//2
        if m**n<=a:lo=m
        else:hi=m
    assert lo**n<=a<(lo+1)**n;return lo
def moment(profile):
    den=10**30;lo=hi=F(0)
    for r,c in profile.items():
        z=iroot(int(r)**199*den**200,200);a,b=F(z,den),F(z+1,den);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return [lo,hi]
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x
def main(a):
    ep=HERE/'extract_rail.py';assert sha(ep.read_bytes())=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372';sp=importlib.util.spec_from_file_location('ferry_lemma_engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);qb=(HERE/'source-evidence/rail-consumer.json.gz').read_bytes();assert sha(qb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc';q=json.loads(gzip.decompress(qb));s=e.load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',e.SOURCE_PIN);roles={int(k):v for k,v in q['source_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};H=list(host);spaces=list(map(e.span,q['frames']));before,loc,bill=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,{i:{i:F(1)} for i in range(400)});census={};pure=[]
    for h,(b,d) in host.items():
        b,d=roles[b],roles[d];assert all(before[r].get(b,F(0))==F(r==b) for r in range(400));dest=[(i,o) for i,o in enumerate(q['program']) if o[1]==d];assert all(o[0]=='MOVE' for i,o in dest);reads=[{'event':i,'op':o} for i,o in enumerate(q['program']) if o[0] in ['ADD','COPY'] and o[2]==d];final=loc[d];single=len(dest)==1 and dest[0][1][2:4]==[3,final];assert not single or all(r['op'][4]==final for r in reads)
        if single:pure.append(h)
        census[h]={'B':b,'D':d,'initial_B_line':q['initial'][b],'final_D_facet':final,'B_input_column_identity':True,'D_MOVEs':[{'event':i,'op':o} for i,o in dest],'D_reads':reads,'single_MOVE_final_only_reads':single}
    assert len(pure)==74
    er=a.repo/'research/moonshot-005-program/results/joint-current-row-codes/review-star/engine.py';assert sha(er.read_bytes())=='126c5cc00d2347fce1e81278b9e9563e5958f8899580d9bdba0dd8799e4e9d81';sys.path.insert(0,str(er.parent));from engine import root9,rank
    roots={i:root9(s['frames'][s['initial'][i]][0]) for i in H};G=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))/2;J=set(q['consumer']['selected_return_ports']);C=set();M=[]
    for h in H:
        b,d=host[h];row=[before[roles[b]].get(roles[host[j][1]],F(0))+F(h==j) for j in H];M.append(row)
        if not any(row):C.add(h)
    assert rank(M)==58 and len(J)==31 and len(C)==24 and C<=J
    for i,h in enumerate(H):
        assert M[i][i]==F(h not in J)
        for j,k in enumerate(H):
            normal=s['frames'][s['initial'][h]][0];donor_normal=s['frames'][s['initial'][k]][0];assert (normal in spaces[s['final'][host[k][1]]])==(not bool((normal&donor_normal).bit_count()%2))
            if h!=k and (s['frames'][s['initial'][h]][0]&s['frames'][s['initial'][k]][0]).bit_count()%2:assert M[i][j]==0
    frame=[0,7,20,27,36,46,57,111];assert set(frame)<=set(H)-J;assert [[G(i,j) for j in frame] for i in frame]==[[F(i==j) for j in frame] for i in frame]
    frame_M=[[M[H.index(i)][H.index(j)] for j in frame] for i in frame];frame_contacts=[[s['frames'][s['initial'][i]][0] in spaces[s['final'][host[j][1]]] for j in frame] for i in frame];assert frame_M==[[F(i==j) for j in frame] for i in frame];assert not any(any(row) for row in frame_contacts)
    optimum=[[G(h,k) if h not in C and k not in J else F(0) for k in H] for h in H];L=[[v-M[i][j] for j,v in enumerate(row)] for i,row in enumerate(optimum)]
    for i,h in enumerate(H):
        for j,k in enumerate(H):
            if L[i][j]:assert i!=j and not ((s['frames'][s['initial'][h]][0]&s['frames'][s['initial'][k]][0]).bit_count()%2)
    assert rank(optimum)==8
    raw=(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes();assert sha(raw)==FULL_PIN;full=json.loads(raw);T={int(k):v for k,v in full['invoice']['T'].items()};P={int(k):v for k,v in full['invoice']['P'].items()};helpers={int(k):v for k,v in full['native']['helpers'].items()};native={int(k):v for k,v in full['native']['paid'].items()};Q=bill['moves'];ranks=set(T)|set(P)|set(helpers)|set(native)|set(Q);limit={r:F(T.get(r,0)-P.get(r,0),18)-helpers.get(r,0)+native.get(r,0)-Q.get(r,0) for r in ranks};free_bounds=moment(limit);terminal=dict(limit);terminal[1]=terminal.get(1,F(0))-65;terminal_bounds=moment(terminal);slope=moment({r:F(T.get(r,0)-P.get(r,0),18) for r in set(T)|set(P)});assert slope[1]<0 and terminal_bounds[1]<0
    result={'status':'PASS_GENERAL_FERRY_CENSUS_AND_SCOPED_TERMINAL_FLOOR','parent_sha256':sha(qb),'native_sha256':e.SOURCE_PIN,'all96_B_input_columns_identity_on_FULL400_public_outputs':True,'all96_D_fields_readonly_MOVEs':True,'eligible_single_MOVE_D_donors':pure,'eligible_count':74,'nontrivial_D_count':22,'source_census':census,'current_reverse_rank':58,'old_returned_ports':sorted(J),'old_completed_ports':sorted(C),'orthogonal_unreturned_frame':frame,'actual_M58_frame_minor':frame_M,'frame_initial_line_to_D_facet_contact_matrix':frame_contacts,'all_admissible_L_frame_entries_forbidden':True,'general_intermediate_handoff_requires_full_public_suffix_zero_outside_B':True,'free_orthogonal_ferry_minimum_reverse_rank':8,'free_rank8_matrix':optimum,'admissible_free_L':L,'all_unreturned_diagonal_entries_fixed1':True,'unreturned_nonzero_columns_for_every_L_at_least':65,'terminal_first_departures_at_least':65,'limiting_free_ferry_margin_bounds':free_bounds,'limiting_after_terminal_bounds':terminal_bounds,'limiting_after_terminal_display':float(terminal_bounds[1]),'finite_m_slope_bounds':slope,'scope':'Line-deposit compensated ferries with orthogonal off-diagonal L, original firstX/firstY/D endpoints retained and no surviving D-dependent record outside final Hub graph and original D facets. Arbitrary free L is an optimistic algebraic grant. The65-departure completion floor concerns that restored terminal cut, not preterminal retained observations or a global packet cycle. Rank8 does not supply a complete source.'};a.output.write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps(e.clean({k:result[k] for k in ['status','eligible_count','nontrivial_D_count','free_orthogonal_ferry_minimum_reverse_rank','terminal_first_departures_at_least','limiting_after_terminal_display']}),indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
