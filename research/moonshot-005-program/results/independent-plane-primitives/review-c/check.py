#!/usr/bin/env python3
"""Independent224-input plane replay and exact conditional invoice.
No author builder/replay imported. @CubeJerry/OpenAI assistance.
"""
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
BASE=Path(__file__).resolve().parents[2];AUTHOR=BASE/'worker-b/independent-plane-primitives'
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def span(B):
    s={0}
    for b in B:
        need(b not in s,'actual independent chart frame');s|={x^b for x in tuple(s)}
    return frozenset(s)
def add(a,b,c=F(1)):
    out=a.copy()
    for k,v in b.items():
        z=out.get(k,F(0))+c*v
        if z:out[k]=z
        else:out.pop(k,None)
    return out

def replay(w,inverse,rows=None,loc=None):
    n=w['public'];need(n==224 and w['owned_fields']==0,'224 arbitrary public inputs and no owner');S=list(map(span,w['frames']));rows={i:{i:F(1)}for i in range(n)}if rows is None else copy.deepcopy(rows);loc=list(w['initial'])if loc is None else loc.copy();need(loc==w['initial'],'exact plane input boundary')
    counts=Counter();profile=Counter();pairs=set();paths={i:[loc[i]]for i in range(n)}
    for o in w['program']:
        tag,i=o[:2];need(0<=i<n,'self-contained local public role');counts[tag]+=1
        if tag=='MOVE':
            _,_,a,b,owned=o;need(owned is False and loc[i]==a,'actual raw departure');need(S[b]<S[a]if inverse else S[a]<S[b],'true plane direction');loc[i]=b;profile[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1;pairs.add((a,b));paths[i].append(b)
        elif tag=='ADD':
            _,_,j,c,at=o;need(0<=j<n and i!=j and loc[i]==loc[j]==at,'nonself actual cochart read');need(F(c)in(F(1,2),F(-1,2)),'dyadic source half coefficients');rows[i]=add(rows[i],rows[j],F(c))
        else:raise ValueError('new lifetime or unsupported source opcode '+tag)
    need(loc==w['final'],'all224 output chart endpoints');need(all(len(p)==3 for p in paths.values()),'every original input has both actual movements')
    return rows,loc,dict(profile),dict(counts),pairs

def source_review(f,iv):
    d=f['logical_involution'];P=d['ports'];roles={k:{int(h):i for h,i in m.items()}for k,m in d['role_map'].items()};R={int(h):{int(j):F(c)for j,c in row.items()}for h,row in d['R_rows'].items()};index={h:i for i,h in enumerate(P)}
    outputs={};words={};rec=[]
    for name in ['forward-XY','inverse-XY','forward-UV','inverse-UV']:
        inverse=name.startswith('inverse');xy=name.endswith('XY');source=iv if inverse else f;first,second=('X','Y')if xy else('B','D');orig=[roles[first][h]for h in P]+[roles[second][h]for h in P];mapping={old:i for i,old in enumerate(orig)}
        w=load(AUTHOR/f'output/{name}/WORD.json.gz');words[name]=w;need(w['plane']['local_to_original_fields']==orig and w['frames']==source['frames'],'literal source embedding and every chart retained')
        ops=[]
        for o in source['program']:
            if o[1]not in mapping:continue
            z=o.copy();z[1]=mapping[o[1]]
            if o[0]=='ADD':need(o[2]in mapping,'no read from the omitted plane');z[2]=mapping[o[2]]
            ops.append(z)
        need(w['program']==ops,'exact filtered and renamed original chronology');need(w['initial']==[source['initial'][i]for i in orig]and w['final']==[source['final'][i]for i in orig],'authentic224 input/output boundaries')
        rows,loc,profile,counts,pairs=replay(w,inverse);want={i:{i:F(1)}for i in range(224)}
        for h in P:
            for j,c in R[h].items():
                if xy:dest=112+index[h];src=index[j];coef=-c if inverse else c
                else:dest=index[j];src=112+index[h];coef=c if inverse else -c
                want[dest]=add(want[dest],{src:F(1)},coef)
        need(rows==want,'every224-input endpoint coefficient');need(profile=={2:112,3:112,5:112,6:112}and counts=={'MOVE':448,'ADD':448},'complete per-plane invoice')
        cert=load(AUTHOR/f'source/{"INVERSE"if inverse else"FORWARD"}-PHASES.json');known={(z['source'],z['target']):z for z in cert['recipes']};need(pairs==set(known)and len(pairs)==280,'all280 inherited signed map pairs actually used')
        need(all(known[a,b]['source_frame']==w['frames'][a]and known[a,b]['target_frame']==w['frames'][b]and known[a,b]['rank']==abs(len(w['frames'][a])-len(w['frames'][b]))for a,b in pairs),'all literal map frames and paid ranks match signed certificates')
        bad=copy.deepcopy(w);z=next(z for z in bad['program']if z[0]=='ADD');z[3]=str(-F(z[3]));need(replay(bad,inverse)[0]!=want,'wrong plane ADD sign rejected')
        outputs[name]=(rows,loc);rec.append({'name':name,'input_columns':224,'signal_coefficients':12544,'counts':counts,'profile':profile,'signed_map_pairs':280,'owners':0,'wrong_sign_rejected':True})
    I={i:{i:F(1)}for i in range(224)}
    for plane in ['XY','UV']:
        for first,second in [('forward','inverse'),('inverse','forward')]:
            rows,loc=outputs[f'{first}-{plane}'];need(replay(words[f'{second}-{plane}'],second=='inverse',rows,loc)[0]==I,'both literal plane inverse compositions')
    return rec

def power_bracket(n):
    D=10**36;target=n**199*D**200;a,b=0,n*D+1
    while b-a>1:
        m=(a+b)//2
        if m**200<=target:a=m
        else:b=m
    need(a**200<=target<b**200,'independent integer200th-root bracket');return F(a,D),F(b,D)
def moment(profile):
    lo=hi=F(0)
    for r,c in profile.items():
        a,b=power_bracket(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi

def budget_review():
    given=load(AUTHOR/'output/PRICE.json');profile={2:112,3:112,5:112,6:112};half=moment(profile);target={24:224,25:224};paid={1:112,2:336,3:336,5:336,6:336,8:672};gap=target.copy()
    for r,c in paid.items():gap[r]=gap.get(r,0)-c
    g=moment(gap);record=given['conditional_three_half_caller'];need({int(k):v for k,v in record['paid'].items()}==paid and {int(k):v for k,v in record['productive_targets'].items()}==target,'all hypothetical idles, head query, sources and independent targets are counted')
    need(g[0]>0 and g[1]-112<0,'positive conditional room and extra complete query negative control')
    for ours,theirs in [(half,given['half_moment']),(g,record['gap'])]:
        x,y=map(F,theirs);need(max(ours[0],x)<=min(ours[1],y),'independent rational invoice agrees')
    return {'half_profile':profile,'half_moment_interval':list(map(str,half)),'half_moment_display':float(half[0]),'conditional_three_half_profile':paid,'conditional_targets':target,'conditional_gap_interval':list(map(str,g)),'conditional_gap_display':float(g[0]),'extra_query_gap_display':float(g[1]-112),'physical_caller_constructed':False,'scope':'Exact arithmetic implication only, retaining coefficient/body alignment and physical final-head service assumptions.'}

def extraction_control():
    rows=[{(i,0):F(1)}for i in range(4)]
    def shear(i,j,p=0,c=F(1)):
        rows[i]=add(rows[i],{(k,e+p):v for(k,e),v in rows[j].items()},c)
    rows[0],rows[2]=rows[2],rows[0];shear(2,3);rows[1],rows[2]=rows[2],rows[1];shear(2,0)
    shear(0,1,1);shear(2,0,c=F(-1));shear(1,2,-1);shear(2,0);shear(3,1,c=F(-1));shear(2,3,1);shear(3,1);shear(0,2,c=F(-1))
    expected=[{(0,1):F(1)},{(1,-1):F(1)},{(2,0):F(1),(3,1):F(1)},{(3,0):F(1)}];need(rows==expected,'three-shear extraction on every arbitrary input, with true P inverse')
    shear(2,3,1,F(-1));need(rows==[{(0,1):F(1)},{(1,-1):F(1)},{(2,0):F(1)},{(3,0):F(1)}],'fourth P shear closes residual without disturbing arbitrary baseline')
    return {'all_four_inputs_checked':True,'operator_ring':'Q[P,P^-1]','three_half_shears':3,'remaining_P_shear':1,'physical_alignment_or_rank_one_P_not_asserted':True}

PIN='e741e3cb2a091052efee4548ff4f7cab6271826f6aa3d63b81af5967c23748d1'
def main():
    global AUTHOR
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();AUTHOR=a.author
    need(hashlib.sha256((AUTHOR/'MANIFEST.json').read_bytes()).hexdigest()==PIN,'frozen author manifest');manifest=load(AUTHOR/'MANIFEST.json')
    for name,pin in manifest['files'].items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen file pin '+name)
    f=load(AUTHOR/'source/FORWARD.json.gz');iv=load(AUTHOR/'source/INVERSE.json.gz');planes=source_review(f,iv)
    out={'status':'PASS_INDEPENDENT_FOUR_PLANE_SOURCE_REVIEW','author_manifest':PIN,'author_proof':manifest['files']['PROOF.md'],'planes':planes,'literal_inverse_compositions':4,'ordinary_embedded_plane_inventory':{'entry_routes':224,'native_input_normalizers':112,'native_output_normalizers':112,'exit_routes':224,'total':672,'extra_inverse_signs':224,'extra_inverse_body_square_translations':224},'invoice':budget_review(),'universal_extraction_control':extraction_control(),'interleaving_status':'Proved for disjoint register sets and order-preserving interleavings. Reuse on the same caller bank requires a new actual history proof.','scope':'Four actual independent224-input source interfaces and complete tariffs. Signed maps and A± embedding inherited from independently reviewed exact predecessors. No common P/body alignment, new caller, supplier, or kappa.'}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'planes':[{'name':z['name'],'inputs':z['input_columns'],'profile':z['profile']}for z in planes],'half_moment':out['invoice']['half_moment_display'],'conditional_gap':out['invoice']['conditional_gap_display']}))
if __name__=='__main__':main()
