#!/usr/bin/env python3
"""Independent arbitrary-boundary inverse/source replay. No author builder import.
Phase evidence is explicitly retained-interpreter reproduction. @CubeJerry/OpenAI.
"""
import argparse,copy,gzip,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
AUTHOR=BASE/'worker-b/inverse-logical-112';REPO=BASE/'programme'
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def span(B):
    S={0}
    for b in B:
        need(b not in S,'independent actual chart frame');S|={x^b for x in tuple(S)}
    return frozenset(S)
def add(a,b,c):
    out=a.copy()
    for j,v in b.items():
        x=out.get(j,F(0))+c*v
        if x:out[j]=x
        else:out.pop(j,None)
    return out
def replay(w,desc,rows=None,locations=None):
    n=w['public'];need(n==448 and w['owned_fields']==0,'all448 inputs public and no owned premise');S=list(map(span,w['frames']))
    rows={i:{i:F(1)}for i in range(n)}if rows is None else copy.deepcopy(rows);loc=list(w['initial'])if locations is None else list(locations)
    need(loc==w['initial']and set(rows)==set(range(n)),'complete literal arbitrary input boundary')
    counts=Counter();profile=Counter();paths={i:[loc[i]]for i in range(n)};pairs=set()
    for op in w['program']:
        tag,i=op[:2];need(0<=i<n,'no hidden field');counts[tag]+=1
        if tag=='MOVE':
            _,_,a,b,owned=op;need(owned is False and loc[i]==a,'actual raw departure')
            need(S[b]<S[a]if desc else S[a]<S[b],'required public orientation')
            profile[abs(len(w['frames'][b])-len(w['frames'][a]))]+=1;loc[i]=b;paths[i].append(b);pairs.add((a,b))
        elif tag=='ADD':
            _,_,j,c,a=op;need(0<=j<n and i!=j and loc[i]==loc[j]==a,'literal nonself cocharted read')
            need(F(c)in(F(1,2),F(-1,2)),'only original dyadic half coefficients');rows[i]=add(rows[i],rows[j],F(c))
        else:raise ValueError('unsupported or irreversible opcode '+tag)
    need(loc==w['final'],'all448 exact endpoint charts')
    return rows,loc,dict(profile),dict(counts),paths,pairs

def root(q):
    if q.bit_count()==3:return [2 if q>>i&1 else -1 for i in range(9)]
    need(q.bit_count()==7,'native root normal');a,b=[i for i in range(9)if not(q>>i&1)];return [3*int(i==a)-3*int(i==b)for i in range(9)]
def source_matrix(f):
    d=f['logical_involution'];P=d['ports'];normal={int(h):q for h,q in d['normals'].items()};rho={h:root(normal[h])for h in P};Z=list(map(root,d['omitted_frame']))
    g={h:[F(sum(x*y for x,y in zip(rho[h],z)),18)for z in Z]for h in P};pattern={h:tuple(i for i,c in enumerate(g[h])if c)for h in P}
    R={h:{}for h in P}
    for h in P:
        for j in P:
            c=F(h==j)-sum(x*y for x,y in zip(g[h],g[j]))if pattern[h]==pattern[j]else F(0)
            if c:R[h][j]=c
    need(R=={int(h):{int(j):F(c)for j,c in row.items()}for h,row in d['R_rows'].items()},'independent native-root reconstruction of actual R0')
    need(all(len(row)==4 for row in R.values())and len(P)==112,'full112 four-neighbor source')
    return P,R,{k:{int(h):i for h,i in row.items()}for k,row in d['role_map'].items()}

def targets(P,R,role,inverse):
    rows={i:{i:F(1)}for i in range(448)};sgn=-1 if inverse else 1
    for h in P:
        for j,c in R[h].items():
            rows[role['Y'][h]]=add(rows[role['Y'][h]],{role['X'][j]:F(1)},sgn*c)
            rows[role['B'][j]]=add(rows[role['B'][j]],{role['D'][h]:F(1)},-sgn*c)
    return rows

def source_review(f,w):
    need(w['frames']==f['frames']and w['initial']==f['final']and w['final']==f['initial'],'literal reversed entire chart boundaries')
    ops=[]
    for op in reversed(f['program']):
        if op[0]=='MOVE':ops.append(['MOVE',op[1],op[3],op[2],False])
        else:need(op[0]=='ADD','no erasure or other opcode to invert');ops.append(['ADD',op[1],op[2],str(-F(op[3])),op[4]])
    need(ops==w['program'],'exact instruction-by-instruction inverse')
    P,R,role=source_matrix(f);a,la,qa,ca,pa,fa=replay(f,False);b,lb,qb,cb,pb,fb=replay(w,True)
    need(a==targets(P,R,role,False)and b==targets(P,R,role,True),'all448 arbitrary-input forward and inverse columns')
    I={i:{i:F(1)}for i in range(448)}
    need(replay(w,True,a,la)[0]==I and replay(f,False,b,lb)[0]==I,'both literal whole-word compositions are identity')
    need(all(b[role['Y'][h]].get(role['X'][j],F(0))+b[role['B'][j]].get(role['D'][h],F(0))==0 for h in P for j in P),'all12544 adjoint entries')
    need(qa==qb=={2:224,3:224,5:224,6:224}and ca==cb=={'MOVE':896,'ADD':896},'complete unchanged movement and ordinary invoice')
    need(all(pa[i]==list(reversed(pb[i]))and len(pa[i])==3 for i in range(448)),'all448 exact two-move public paths reversed')
    need(fb=={(b,a)for a,b in fa}and len(fb)==280,'all280 ordered inverse maps exactly covered')
    controls=[]
    for label in ['wrong_add_sign','wrong_move_direction','wrong_input_boundary','silent_forward_orientation']:
        bad=copy.deepcopy(w)
        if label=='wrong_add_sign':o=next(o for o in bad['program']if o[0]=='ADD');o[3]=str(-F(o[3]))
        elif label=='wrong_move_direction':o=next(o for o in bad['program']if o[0]=='MOVE');o[2],o[3]=o[3],o[2]
        elif label=='wrong_input_boundary':bad['initial']=f['initial']
        try:rr=replay(bad,label!='silent_forward_orientation');rejected=rr[0]!=b
        except ValueError:rejected=True
        need(rejected,'independent negative control '+label);controls.append(label)
    return {'public':448,'all_input_columns':448,'adjoint_entries':12544,'literal_compositions':2,'public_paths_reversed':448,'instructions':1792,'moves':qa,'ordinary_operations':ca,'owned_fields':0,'owner_lifetimes':0,'peak_owned':0,'controls':controls},fb

def module(path,name,pin):
    need(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'retained interpreter pin '+name)
    spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj

def phase_review(w,pairs,repo):
    data=load(AUTHOR/'output/PHASES.json');recs=data['recipes'];need(len(recs)==280 and {(z['source'],z['target'])for z in recs}==pairs,'every actual inverse pair has one signed recipe')
    path=repo/'research/moonshot-005-program/results/complex-omitted-line-gram/author/dependencies/native_verify.py'
    v=module(path,'inverse_review_phase','3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38')
    for r in recs:
        a,b=r['source'],r['target'];need((r['source_frame'],r['target_frame'])==(w['frames'][a],w['frames'][b]),'actual inverse source and target frames')
        need(r['rank']==r['recipe']['rank']==len(w['frames'][a])-len(w['frames'][b]),'descending rank exactly charged')
        actual=v.recipe(r['recipe']);expected=v.adjoint(v.frame(w['frames'][a],9))+v.frame(w['frames'][b],9)
        v.equal(actual,expected,'exact signed inverse map')
        forward=v.adjoint(v.frame(w['frames'][b],9))+v.frame(w['frames'][a],9)
        v.equal(actual+forward,(),'actual signed inverse followed by physical forward map')
        v.equal(forward+actual,(),'physical forward followed by actual signed inverse')
    controls=[]
    for label in ('wrong_global_phase','wrong_rank','reversed_recipe_target'):
        r=copy.deepcopy(recs[0]);expected=v.adjoint(v.frame(r['source_frame'],9))+v.frame(r['target_frame'],9)
        if label=='wrong_global_phase':r['recipe']['left']['phase']=(r['recipe']['left']['phase']+1)%4
        elif label=='wrong_rank':r['recipe']['rank']-=1
        else:expected=v.adjoint(expected)
        try:v.equal(v.recipe(r['recipe']),expected,label);rejected=False
        except ValueError:rejected=True
        need(rejected,'signed inverse phase control '+label);controls.append(label)
    return {'ordered_recipes':280,'signed_inverse_forward_compositions':560,'controls':controls,'scope':'Pinned retained independent-interpreter reproduction, separate from the newly implemented rational source replay.'}

def original_schema_rejection(w,repo):
    d=module(AUTHOR/'dependencies/dynamic-replay.py','original_ascent_replay','3845c44744ee0a05300bc237e9b9d10b45ca1272262f09f11e8a3ac2313a9e04')
    e=module(repo/'research/moonshot-005-program/results/complex-omitted-line-gram/author/dependencies/replay.py','original_replay_kernel','045ec283e41288354bb82d2f1e8a62facfb67c23cd4f6954f4d7a5ae744bd37e')
    try:d.replay(w,w['program'],e);message=None
    except ValueError as err:message=str(err)
    need(message=='nested MOVE','original raw-ascent schema really rejects the inverse')
    return {'original_schema_rejects':True,'actual_error':message,'unchanged_old_validator':True,'scope':'New reversed-boundary service is explicit; rejection is not bypassed or relabelled as old native admission.'}

def price():
    D=10**36;lo=hi=F(0)
    for rank in (2,3,5,6):
        target=rank**199*D**200;a,b=0,rank*D+1
        while b-a>1:
            m=(a+b)//2
            if m**200<=target:a=m
            else:b=m
        need(a**200<=target<b**200,'independent exact integer root bracket');lo+=224*F(a,D);hi+=224*F(b,D)
    recorded=list(map(F,load(AUTHOR/'output/PRICE.json')['exact_moment']));need(max(lo,recorded[0])<=min(hi,recorded[1]),'independent moment enclosure agrees')
    return {'t':'199/200','moment_interval':[str(lo),str(hi)],'display':float(lo),'no_caller_allowance_inferred':True}

PINS={'MANIFEST.json':'7c476ba0f7c2f2032124b9b3a9c54debd233c79bedb912aee635689ae71dc552','PROOF.md':'b0e996addbec83542d329fc3c5a3a5c0b5b1d975a6ef0f9d24a30c3d9963bba4','dependencies/FORWARD.json.gz':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336','output/WORD.json.gz':'3c5e0af6debb0c435520b0711f87f413da35336f6d996e0afea7063dbc4ef948','output/RESULT.json':'9e89ba5a4cd5ee12bbc81e89daef30babf8bbcfb7f28321a4c618b1cc6ad8948','output/PHASES.json':'c2b9e20782d6aa0cdddd9d11e64ec5b03bd14188aebe9cbc2068a918863f8300'}
def main():
    global AUTHOR,REPO
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--repo',type=Path,default=REPO);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();AUTHOR=a.author;REPO=a.repo
    for name,pin in PINS.items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen source pin '+name)
    f=load(AUTHOR/'dependencies/FORWARD.json.gz');w=load(AUTHOR/'output/WORD.json.gz');source,pairs=source_review(f,w)
    out={'status':'PASS_INDEPENDENT_REVERSED_ARBITRARY_BOUNDARY_SOURCE','source_pins':PINS,'independent_source':source,'phase_reproduction':phase_review(w,pairs,REPO),'old_schema':original_schema_rejection(w,REPO),'invoice':price(),'scope':'Literal source inverse for448 arbitrary inputs at reversed physical boundaries. No erasure inverted or clean input assumed. No old native/caller admission and no new kappa; all retained uniform compiler/precision/ordinary hypotheses remain.'}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'source':source,'phase_recipes':out['phase_reproduction']['ordered_recipes'],'old_schema':out['old_schema'],'moment':out['invoice']['display']}))
if __name__=='__main__':main()
