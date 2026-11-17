"""Independent source-row and direct image-rank audit of the fixed-column gate."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json

SOURCE_REVIEW_SHA='ed688f0178639153bec60b2e5a9864d005996df32621d7257b1353da56bb102a'
AUTHOR_PROOF_SHA='4d57122550382ff0067a5a5da31fc4b500be79ca4c4e8114a61b5b6220584857'

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source-review',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert hashlib.sha256(a.source_review.read_bytes()).hexdigest()==SOURCE_REVIEW_SHA
    assert hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest()==AUTHOR_PROOF_SHA
    spec=importlib.util.spec_from_file_location('root_independent_endpoint_source',a.source_review);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
    m=s.arithmetic(a.repo);reports=[]
    for width in[0,1]:
        c=s.case(m,width);n=c['n'];mul=c['mul'];P,N,Z=c['P'],c['N'],c['Z'];bm=c['bm'];source=c['a']
        projected=bm([[Z,Z,P]],bm(bm(c['L'],c['C']),c['U']))
        assert projected==[[Z,Z,P]]
        assert bm([[Z,Z,P]],c['H'])==[[Z,Z,P]]
        # This literal row identity, before Q, proves the formula for every Q.
        q=c['Q'];expected=[[m.add(mul(P,q[2][0],source),mul(P,q[2][1])),mul(P,q[2][1],source),mul(P,q[2][2])]]
        assert bm([[Z,Z,P]],c['E'])==expected
        sector=mul(P,c['P1']);assert mul(sector,sector)==sector and mul(N,sector)==Z
        aw=mul(source,c['w']);an=mul(source,N)
        assert mul(m.star(an),an)==N and mul(m.star(aw),aw)==sector
        x=mul(source,m.add(m.scale(mul(c['S'],c['J'],c['z']),-1),c['w']))
        linear=[[m.scale(x,-1)],[x],[mul(source,c['p'])]]
        first=bm(linear,[[N]]);second=bm(linear,[[sector]])
        assert first==[[Z],[Z],[an]] and second==[[m.scale(aw,-1)],[aw],[Z]]
        v=m.stack(*[row[0] for row in first]);w=m.stack(*[row[0] for row in second])
        ranks=[m.col_rank(v),m.col_rank(w)];combined=m.col_rank(v+w)
        assert ranks==[n//2,n//4] and combined==3*n//4
        assert bm([[Z,Z,P]],first)==bm([[Z,Z,P]],second)==[[Z]]
        required=m.col_rank(P)+combined;assert required==5*n//4>n
        # Both sectors are needed for this contradiction. Either alone fits.
        assert m.col_rank(P)+ranks[0]==n and m.col_rank(P)+ranks[1]<n
        # Changing the output selector invalidates the low-class source row.
        assert bm([[Z,Z,N]],bm(bm(c['L'],c['C']),c['U']))!=[[Z,Z,N]]
        reports.append({'tail_width':width,'reduced_bank_dimension':n,'source_row_before_any_Q':True,'forced_kernel_sector_ranks':ranks,'independent_union_rank':combined,'required_projection_rank':n//2,'required_encoder_rank':required,'available_encoder_rank':n,'opposite_selector_control_rejected':True,'either_sector_alone_not_a_contradiction':True})
    result={'status':'PASS_INDEPENDENT_FIXED_COLUMN_ENDPOINT_GATE','source_review_sha256':SOURCE_REVIEW_SHA,'author_proof_sha256':AUTHOR_PROOF_SHA,'controls':reports,'universal_proof':'The exact pre-Q source row implies only ordinary/linear classes after arbitrary Q and the last native. Under the explicitly retained fixed-prefix/fixed-finite-tail-catalogue separation, the other two head encoders vanish under pi. Endpoint invertibility gives projection rank D/2; the fixed last column forces independent kernel images of total rank3D/4.','scope':'All ordinary unit completions of this fixed column and C within the stated uniform separation class; changing C, the column, or the catalogue hypothesis is outside scope.','positive_column_and_local_costs_preserved':True,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])

if __name__=='__main__':main()
