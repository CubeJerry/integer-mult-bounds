#!/usr/bin/env python3
"""Independent affine spatial composition and all-path support certificate.
No author checker or builder imported. @CubeJerry/OpenAI.
"""
import argparse,gzip,hashlib,json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parents[2];AUTHOR=BASE/'worker-a/interstage-normalizer-screen'
def need(x,m):
    if not x:raise ValueError(m)
def parity(x):return x.bit_count()%2
def dot(x,y):return parity(x&y)
def apply(cols,x):
    ans=0
    for i,c in enumerate(cols):
        if x>>i&1:ans^=c
    return ans
def transpose_apply(cols,x):return sum(dot(c,x)<<i for i,c in enumerate(cols))
def route(B,s,x):
    out=x
    for i,b in enumerate(B):
        w=b^(1<<(9+8*(s-1)+i))
        if dot(w,x):out^=w
    return out
def affine_term(records,s,t,h,k,j):
    def p(stage,port,x):return route(records[stage,port]['orthogonal_complement'],stage,x)
    def tau(stage,port):return records[stage,port]['input_translation']
    # Direct physical row-map composition, without Fourier path formulas.
    def actual(x):
        x=p(s,h,x)^tau(s,h)
        x=p(s,k,x^tau(s,k))
        x=p(t,k,x)^tau(t,k)
        return p(t,j,x^tau(t,j))
    offset=actual(0);cols=tuple(actual(1<<i)^offset for i in range(25))
    need(all(dot(a,b)==int(i==j)for i,a in enumerate(cols)for j,b in enumerate(cols)),'each complete physical path is orthogonal affine')
    need(all(actual((1<<i)^(1<<j))==apply(cols,(1<<i)^(1<<j))^offset for i in range(25)for j in range(i)),'direct affine row-map composition on every quadratic coordinate control')
    return cols,offset
def all_blocks(R,records,s,t):
    blocks={}
    for h,row in R.items():
        for k,a in row.items():
            for j,b in R[k].items():
                key=affine_term(records,s,t,h,k,j);terms=blocks.setdefault((h,j),defaultdict(F));terms[key]+=a*b
    return{ij:{key:c for key,c in terms.items()if c}for ij,terms in blocks.items()if any(terms.values())}
def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def review(w,r,claimed):
    m=w['logical_involution'];P=m['ports'];q={int(h):x for h,x in m['normals'].items()};R={int(h):{int(j):F(c)for j,c in row.items()}for h,row in m['R_rows'].items()};rec={(x['stage'],x['port']):x for x in r['route_records']}
    for h in P:
        b1=rec[1,h]['orthogonal_complement'];b2=rec[2,h]['orthogonal_complement'];need(b1==b2 and all(dot(x,y)==int(i==j)for i,x in enumerate([q[h]]+b1)for j,y in enumerate([q[h]]+b1)),'same actual orthonormal basis at both stages')
        t1=rec[1,h]['input_translation'];t2=rec[2,h]['input_translation'];need(t1<1<<17 and t2==((t1&511)|((t1>>9)<<17)),'input translations are exact fresh-axis renamings')
    blocks=all_blocks(R,rec,1,2);need(len(blocks)==448 and all(len(x)==4 and all(abs(c)==F(1,4)for c in x.values())for x in blocks.values()),'sum all actual intermediate paths before support checks')
    same=all_blocks(R,rec,1,1);identity=(tuple(1<<i for i in range(25)),0);need(same=={(h,h):{identity:F(1)}for h in P},'all same-stage paths really cancel to the full112 bank identity')
    cov=[]
    for z in claimed['covariance_failures']:
        h,j,f=z['output'],z['input'],z['frequency'];summed={}
        for (cols,offset),c in blocks[h,j].items():
            ell=transpose_apply(cols,offset);target=apply(cols,f);summed[target]=summed.get(target,F(0))+c*((-1)**dot(ell,f))
        bad={a:c for a,c in summed.items()if c and dot(q[h],f)!=dot(q[j],a)}
        need(bad and bad=={int(a):F(c)for a,c in z['remaining_wrong_phase_outputs'].items()},'entire four-path Fourier row has a surviving covariance defect')
        cov.append({'output':h,'input':j,'frequency':f,'remaining':{str(a):str(c)for a,c in bad.items()}})
    need(len(cov)==448,'every nonzero block covariance certificate')
    support=[]
    for z in claimed['support_separators']:
        h=z['output_port'];x=z['spatial_row'];allplanes=[]
        for one in z['input_blocks']:
            j=one['input_port'];got=[];union=set()
            for (cols,offset),c in blocks[h,j].items():
                base=apply(cols,x)^offset;u=apply(cols,q[h]);v=q[j];plane=tuple(sorted({base,base^u,base^v,base^u^v}))
                need(len(plane)==4 and not(union&set(plane)),'actual affine Gaussian term planes are disjoint after path summation');union.update(plane);got.append((plane,str(c)));allplanes.append((j,plane,c))
            expected=[(tuple(a),b)for a,b in zip(one['term_supports'],one['term_coefficients'])];need(sorted(got)==sorted(expected)and len(union)==16,'source-bound support separator and coefficient certificate')
        need(len(allplanes)==16 and len({j for j,p,c in allplanes})==4 and sum(c*c for j,p,c in allplanes)==1,'entire output row has all sixteen disjoint terms')
        support.append({'output':h,'spatial_row':x,'planes':[(j,list(p),str(c))for j,p,c in allplanes]})
    need(len(support)==112 and {z['output']for z in support}==set(P),'every output port has a complete row certificate')
    return blocks,support,cov

def controls(w,blocks,support):
    q={int(h):x for h,x in w['logical_involution']['normals'].items()};h=support[0]['output'];x=support[0]['spatial_row'];terms=[]
    for (hh,j),data in blocks.items():
        if hh!=h:continue
        for (cols,offset),c in data.items():
            b=apply(cols,x)^offset;u=apply(cols,q[h]);v=q[j]
            gaussian={b:(F(1,2),F(0)),b^v:(F(0),F(1,2)),b^u:(F(0),F(-1,2)),b^u^v:(F(1,2),F(0))};terms.append((j,c,gaussian))
    def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def emit(selected,wrong=False):
        row={}
        for j,c,g in selected:
            for a,ga in g.items():
                for b,gb in g.items():
                    v=mul(ga,gb);coef=c*c if wrong else c;key=(j,a,b);old=row.get(key,(F(0),F(0)));row[key]=(old[0]+coef*v[0],old[1]+coef*v[1])
        return{k:v for k,v in row.items()if v!=(0,0)}
    row=emit(terms);deleted=emit(terms[1:]);wrong=emit(terms,True);norm=lambda r:sum(a*a+b*b for a,b in r.values())
    need(len(row)==256 and norm(row)==1 and all(a*a+b*b==F(1,256)for a,b in row.values()),'full actual two-column row coefficients and normalization')
    need(norm(deleted)==F(15,16),'removing one complete actual path loses one sixteenth norm')
    need(norm(wrong)==F(1,16),'tensoring whole-bank scalar coefficients gives wrong width-two norm')
    return {'exact_width_two_row_entries':len(row),'exact_width_two_norm':'1','deleted_actual_path_norm':'15/16','wrong_tensor_scalar_norm':'1/16'}

PINS={'FREEZE.json':'38b1c6795c625da4fd06214e8602a8a81f138cee266581978b25889d8759dbb2','PROOF.md':'65ab1163df3eefb6684439ee2f4eec7f24db5fbbfa5a59ab2e22d6e828a080b6','RESULT.json':'1713004e9da3193fa5c27a0a1aff07cfdf1f74a76e44fa47e761bee4594f681a','source/R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','source/ROUTES.json':'ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a'}
def main():
    global AUTHOR
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();AUTHOR=a.author
    for name,pin in PINS.items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen interstage source pin '+name)
    w=load(AUTHOR/'source/R0-WORD.json.gz');r=load(AUTHOR/'source/ROUTES.json');claimed=load(AUTHOR/'RESULT.json');blocks,support,cov=review(w,r,claimed)
    out={'status':'PASS_INDEPENDENT_ACTUAL_INTERSTAGE_ORIENTATION_REVIEW','source_pins':PINS,'ordinary_positive_orientation':'A_s^-1 A_t=R_s R_t; genuine fixed ordinary bank operations with their ordinary cost retained','restricted_expanding_orientation':'A_s A_t^-1=Q R_s R_t Q^-1 for the retained forward routes only','nonzero_blocks':len(blocks),'actual_paths_per_block':4,'covariance_witnesses':cov,'full_row_support_certificates':support,'same_stage_identity_blocks':112,'all_width_support':'16*4^V at every certified repeated row','fixed_template_addition_bound':'L>=2V+4','controls':controls(w,blocks,support),'scope':'Positive ordinary reverse orientation preserved. Actual four-path sums and affine translations checked before support conclusions. No general paid-service, changed-adapter or redesigned-caller impossibility; no new kappa.'}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'blocks':len(blocks),'separators':len(support),'controls':out['controls']}))
if __name__=='__main__':main()
