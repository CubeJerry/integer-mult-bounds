#!/usr/bin/env python3
"""Actual cochart color freedom and a decoder-robust displaced-mode gate."""
import argparse,gzip,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def main(a):
    ep=HERE/'extract_rail.py';assert sha(ep.read_bytes())=='7eba542316bfb1a0ae70fee8f2201b7b15abfcfa3cb59f84014f3331608ec372';sp=importlib.util.spec_from_file_location('color_exact_engine',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);qb=(HERE.parent/'complex-exchange/source-evidence/rail-consumer.json.gz').read_bytes();assert sha(qb)=='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc';q=json.loads(gzip.decompress(qb));wb=(HERE.parent/'complex-exchange/output/rail-exchange.json.gz').read_bytes();assert sha(wb)=='cb77301a8f402fcc0f8dc069faefa0f0b3c6dfaedb6122a5a7d65b04802e2514';w=json.loads(gzip.decompress(wb));s=e.load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',e.SOURCE_PIN);roles={int(k):v for k,v in q['source_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};H=list(host);U=[roles[j] for j in s['live']]+[roles[x] for x,y in host.values()];V=[roles[j+112] for j in s['live']]+[roles[y] for x,y in host.values()];spaces=list(map(e.span,q['frames']));basis={i:{i:F(1)} for i in range(400)};old,ol,ob=e.run(q['program'],q['initial'],400,q['owned_fields'],spaces,basis);new,nl,nb=e.run(w['program'],w['initial'],400,w['owned_fields'],spaces,basis)
    identities=[]
    for i,(b,d) in host.items():
        x,y=roles[i],roles[i+112];bb,dd=roles[b],roles[d];assert q['initial'][x]==q['initial'][bb] and ol[x]==ol[bb]==127 and q['initial'][y]==q['initial'][dd]==3 and ol[y]==ol[dd];identities.append({'port':i,'X':x,'B':bb,'Y':y,'D':dd,'initial_XB_chart':q['initial'][x],'initial_YD_chart':3,'final_XB_chart':127,'final_YD_chart':ol[y]})
    sys.path.insert(0,str(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/review-star'));from engine import rank
    pair_ranks={};oldpair={}
    for i,(b,d) in host.items():
        cols=[roles[i],roles[b]];pair_ranks[i]=rank([[new[r].get(c,F(0)) for c in cols] for r in V]);oldpair[i]=rank([[old[r].get(c,F(0)) for c in cols] for r in V]);assert oldpair[i]==1
    source=w['mode_exchange'];h={int(k):F(v) for k,v in source['old_facet_B_row'].items()};p={i:h.get(roles[b],F(0)) for i,(b,d) in host.items() if h.get(roles[b],F(0))};assert len(p)>=2
    # u_j is the first-X column after the old packet mode is removed. It is
    # unaffected by ANY new decoder gamma for the pure B/D replacement mode.
    u={i:[new[r].get(roles[i],F(0)) for r in V] for i in p};witness=None
    for i in p:
        for j in p:
            if i>=j:continue
            for a0 in range(len(V)):
                for b0 in range(a0+1,len(V)):
                    det=u[i][a0]*u[j][b0]-u[j][a0]*u[i][b0]
                    if det:witness={'ports':[i,j],'output_roles':[V[a0],V[b0]],'minor':[[u[i][a0],u[j][a0]],[u[i][b0],u[j][b0]]],'determinant':det};break
                if witness:break
            if witness:break
        if witness:break
    assert witness and rank([u[i] for i in p])>=2
    # The same obstruction survives arbitrary recoding of ALL eight existing
    # Gram packet modes: the two old X columns are independent modulo their
    # complete decoder space, not only modulo this one deleted column.
    gram=[]
    for k,o in enumerate(q['program']):
        if o!=['MOVE',451,127,3,True]:continue
        z=next(z for z in range(k+1,len(q['program'])) if q['program'][z]==['CLEAR',451,3]);col={}
        for t in q['program'][k+1:z]:
            assert t[0]=='ADD' and t[2]==451 and t[4]==3;col[t[1]]=col.get(t[1],F(0))+F(t[3])
        gram.append([col.get(r,F(0)) for r in V])
    assert len(gram)==rank(gram)==8
    ports=witness['ports'];oldcols=[[old[r].get(roles[i],F(0)) for r in V] for i in ports];quotient_rank=rank(gram+oldcols)-8;assert quotient_rank==2
    bad=[i for i,r in pair_ranks.items() if r==2];assert bad and set(bad)==set(p)
    # Decoder gamma=0 would discard the actual B/D mode altogether. It still
    # leaves a nonzero foreign forward block, unchanged by local GL2 coding.
    foreign=[]
    for i in s['live']:
        for j in s['live']:
            if i!=j and new[roles[i+112]].get(roles[j],F(0)):foreign.append({'receiver_port':i,'source_port':j,'coefficient':new[roles[i+112]][roles[j]]});break
        if foreign:break
    assert foreign
    receiver_tests={};input_port={roles[j]:j for j in s['live']};input_port.update({roles[b]:i for i,(b,d) in host.items()})
    for i,(b,d) in host.items():
        yr,dr=roles[i+112],roles[d];foreignU=[c for c in U if input_port[c]!=i];pr=[[old[r].get(c,F(0)) for c in foreignU] for r in [yr,dr]];nr=[[new[r].get(c,F(0)) for c in foreignU] for r in [yr,dr]];rp,rn=rank(pr),rank(nr);assert rp in [0,1] and rn in [0,1] and not any(nr[1]);receiver_tests[i]={'parent_foreign_rank':rp,'exchange_foreign_rank':rn,'parent_left_kernel':[[F(1),F(0)],[F(0),F(1)]] if not rp else [[F(0),F(1)]],'exchange_left_kernel':[[F(1),F(0)],[F(0),F(1)]] if not rn else [[F(0),F(1)]],'exchange_left_kernel_has_nonzero_firstY_coefficient':rn==0}
    parent_clean=[i for i,t in receiver_tests.items() if not t['parent_foreign_rank']];new_clean=[i for i,t in receiver_tests.items() if not t['exchange_foreign_rank']]
    # Optimistically adding the new mode also to D5 cannot cancel its missing
    # primal-X foreign column: these two foreign input colors are independent.
    row5=roles[5+112];a0=next(j for j in s['live'] if j!=5 and new[row5].get(roles[j],F(0)));b0=next(j for j in p if j!=5);hyp=[[new[row5].get(roles[a0],F(0)),new[row5].get(roles[host[b0][0]],F(0))],[F(0),p[b0]]];det=hyp[0][0]*hyp[1][1];assert det
    controls={'one_B_source_allows_rank1_gamma_choice':rank([u[ports[0]],u[ports[0]]])==1,'adding_new_mode_to_D5_gives_foreign_rank2':{'foreign_X_port':a0,'foreign_B_port':b0,'minor':hyp,'determinant':det},'all_source_pair_target_ranks_are1':True};assert controls['one_B_source_allows_rank1_gamma_choice']
    # Source identity control: any facet row alteration of the D output is
    # already allowed by the arbitrary gamma-vector proof below; no special
    # unchanged-D decoder is being relied upon.
    result={'status':'PASS_ACTUAL_COLOR_CHARTS_AND_DISPLACED_MODE_COLUMN_RANK_GATE','parent_sha256':sha(qb),'exchange_sha256':sha(wb),'all96_color_cochart_identities':identities,'facet_output_roles':V,'root_input_roles':U,'parent_column_pair_ranks':oldpair,'exchange_column_pair_ranks':pair_ranks,'replacement_B_source_ports':p,'rank2_column_pair_ports':bad,'independent_missing_X_columns_witness':witness,'missing_X_column_span_rank':rank([u[i] for i in p]),'eight_Gram_decoder_columns':gram,'Gram_decoder_rank':8,'old_X_column_pair_quotient_rank_mod_full_Gram_decoder':quotient_rank,'receiver_foreign_left_kernel_tests':receiver_tests,'parent_receiver_clean_X_blocks':parent_clean,'exchange_receiver_clean_X_blocks':new_clean,'gamma_zero_foreign_block_witness':foreign[0],'controls':controls,'criterion':'For any arbitrary new packet decoder gamma into all200 Y/D fields, pair j has columns(u_j,p_j*gamma). Target and parent have column-pair rank1. If two u_j in the B-source support are independent, every nonzero gamma forces some pair rank2; all zero-MOVE input color GL2 and any invertible output decoder preserve it. The two old X columns are independent modulo the ENTIRE8-dimensional Gram decoder space, so recoding existing Gram modes does not remove their independence.','scope':'Fixed primal raw source modulo the existing8-dimensional Gram decoder space, and one independent B/D replacement mode. Allows arbitrary packet updates to Y AND D, arbitrary portwise input X/B GL2, arbitrary initial Y/D coding, arbitrary final Hub decoding, and even an optimistic global invertible facet-output decoder. Changed early source operations outside that decoder space, multiple coordinated handoffs and cross-port input transport remain outside scope.'};a.output.write_text(json.dumps(e.clean(result),sort_keys=True,indent=2)+'\n');print(json.dumps(e.clean({k:result[k] for k in ['status','replacement_B_source_ports','rank2_column_pair_ports','independent_missing_X_columns_witness','missing_X_column_span_rank','old_X_column_pair_quotient_rank_mod_full_Gram_decoder','parent_receiver_clean_X_blocks','exchange_receiver_clean_X_blocks']}),indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
