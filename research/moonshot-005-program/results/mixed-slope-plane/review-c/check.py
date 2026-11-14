#!/usr/bin/env python3
"""Independent mixed-slope chronology and exact physical route interface.
Only the credited Worker C Fourier helper is reused; no author checker imported.
"""
import argparse,copy,gzip,hashlib,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
import fourier_review as v
BASE=Path(__file__).resolve().parents[2];AUTHOR=BASE/'worker-a/mixed-slope-plane'
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def span(B):
    S={0}
    for b in B:
        need(b not in S,'independent source frame');S|={x^b for x in tuple(S)}
    return frozenset(S)
def add(a,b,c):
    r=a.copy()
    for k,x in b.items():
        z=r.get(k,F(0))+c*x
        if z:r[k]=z
        else:r.pop(k,None)
    return r

def replay(w,up):
    need(w['public']==224 and w['owned_fields']==0,'224 arbitrary public fields, no owners');rows={i:{i:F(1)}for i in range(224)};loc=list(w['initial']);S=list(map(span,w['frames']));profile=Counter();counts=Counter();orient=Counter();pairs=set();reads=[]
    for t,o in enumerate(w['program']):
        tag,i=o[:2];need(0<=i<224,'no extra field');counts[tag]+=1
        if tag=='MOVE':
            _,_,a,b,owner=o;need(owner is False and loc[i]==a,'actual public departure');asc=(i<112)==up;need(S[a]<S[b]if asc else S[b]<S[a],'declared mixed public slope');loc[i]=b;profile[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1;orient['ascending'if asc else'descending']+=1;pairs.add((a,b))
        elif tag=='ADD':
            _,_,j,c,C=o;need(i>=112 and j<112 and loc[i]==loc[j]==C,'actual original donor and receiver cocharted');need(F(c)in(F(1,2),F(-1,2)),'literal dyadic contact');need(rows[j]=={j:F(1)},'actual original donor retained');rows[i]=add(rows[i],rows[j],F(c));reads.append((i,j,F(c),C))
        else:raise ValueError('new source opcode '+tag)
    need(loc==w['final'],'every actual final chart');need(counts=={'MOVE':448,'ADD':448}and profile=={2:112,3:112,5:112,6:112}and orient=={'ascending':224,'descending':224},'complete per-plane invoice and both directions')
    return rows,dict(profile),dict(counts),dict(orient),pairs,reads

def source_review(parent):
    d=parent['logical_involution'];P=d['ports'];ix={h:i for i,h in enumerate(P)};roles={k:{int(h):x for h,x in row.items()}for k,row in d['role_map'].items()};R={int(h):{int(j):F(c)for j,c in row.items()}for h,row in d['R_rows'].items()};known={}
    for name in ['FORWARD','INVERSE']:
        for z in load(AUTHOR/f'source/{name}-PHASES.json')['recipes']:known[z['source'],z['target']]=z
    expected={(112+ix[h],ix[j],c)for h in P for j,c in R[h].items()};rec=[]
    for name,up in [('X-up-Y-down',True),('X-down-Y-up',False)]:
        w=load(AUTHOR/f'output/{name}/WORD.json.gz');need(w['frames']==parent['frames'],'all exact source charts retained');rows,profile,counts,orient,pairs,reads=replay(w,up)
        want={i:{i:F(1)}for i in range(224)}
        for i,j,c in expected:want[i]=add(want[i],{j:F(1)},c)
        need(rows==want and {(i,j,c)for i,j,c,C in reads}==expected and len(reads)==448,'all224 arbitrary inputs and exact448 original R0 contacts')
        for h in P:
            i=ix[h];X=roles['X'][h];Y=roles['Y'][h]
            need((w['initial'][i],w['final'][i])==((parent['initial'][X],parent['final'][X])if up else(parent['final'][X],parent['initial'][X])),'actual donor boundary direction')
            need((w['initial'][112+i],w['final'][112+i])==((parent['final'][Y],parent['initial'][Y])if up else(parent['initial'][Y],parent['final'][Y])),'actual receiver boundary direction')
        need(len(pairs)==280 and pairs<=set(known),'all280 inherited signed map pairs bound')
        need(all(known[a,b]['source_frame']==w['frames'][a]and known[a,b]['target_frame']==w['frames'][b]and known[a,b]['rank']==abs(len(w['frames'][a])-len(w['frames'][b]))for a,b in pairs),'actual frames and ranks agree with signed predecessor certificates')
        controls=[]
        for label in ['wrong_departure_direction','missing_contact']:
            bad=copy.deepcopy(w)
            if label=='wrong_departure_direction':z=next(z for z in bad['program']if z[0]=='MOVE');z[2],z[3]=z[3],z[2]
            else:bad['program'].pop(next(i for i,z in enumerate(bad['program'])if z[0]=='ADD'))
            try:rejected=replay(bad,up)[0]!=want
            except ValueError:rejected=True
            need(rejected,'negative control '+label);controls.append(label)
        rec.append({'variant':name,'all_input_columns':224,'literal_contacts':448,'profile':profile,'counts':counts,'orientations':orient,'signed_pairs':280,'controls':controls})
    return P,R,rec

def interface(parent,P,R):
    p=Path(__file__).with_name('fourier_review.py');need(hashlib.sha256(p.read_bytes()).hexdigest()=='82063edce04db372ba93e19a4cb194116d7a090c454a9095f116a5dad4803b89','credited frozen independent Fourier helper')
    p=Path(__file__).parent/'source/ROUTES.json';need(hashlib.sha256(p.read_bytes()).hexdigest()=='ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a','actual route source pin');records={(x['stage'],x['port']):x for x in load(p)['route_records']};q={int(h):x for h,x in parent['logical_involution']['normals'].items()};M={};Mi={};O={};Oi={};n=0;UP={};DN={};AP={};AM={}
    for s in (1,2):
        for h in P:
            z=records[s,h];cols=v.route(z['orthogonal_complement'],s);tau=z['input_translation'];sigma=z['output_translation'];M[s,h]=v.op(cols,((tau,2),));Mi[s,h]=v.op(cols,((v.apply(cols,tau),2),));O[s,h]=v.op(cols,((sigma,2),));Oi[s,h]=v.op(cols,((v.apply(cols,sigma),2),))
            v.eq(v.product(O[s,h],v.H(),v.Q(q[h],-1),M[s,h]),v.D(s),'actual positive baseline')
            v.eq(v.product(Mi[s,h],v.Q(q[h]),v.H(-1),Oi[s,h]),v.D(s,-1),'actual negative baseline')
            v.eq(v.product(v.D(s,-1),v.D(s,2)),v.D(s),'actual even square corrects the negative diagonal')
    for s in (1,2):
        for h in P:
            for j,c in R[h].items():
                up=v.product(Mi[s,h],v.Q(q[j],-1),M[s,j]);Api=v.product(Mi[s,h],v.Q(q[j],-1),M[s,j]);down=v.product(O[s,h],v.Q(q[h],-1),Oi[s,j]);Ami=v.product(v.Q(q[h],-1),O[s,h],Oi[s,j])
                UP[s,h,j]=up;DN[s,h,j]=down;AP[s,h,j]=v.product(v.Q(q[h]),Mi[s,h],M[s,j]);AM[s,h,j]=v.product(O[s,h],Oi[s,j],v.Q(q[j]))
                v.eq(down,Ami,'down/up cross commutes Q only through its own actual route')
                need(v.key(up)!=v.key(v.product(v.D(s),Api))and v.key(down)!=v.key(v.product(v.D(s),Ami)),'neither mixed cross contains a hidden leading body Gaussian');n+=1
    for s in (1,2):
        for left,right in [(AP,UP),(AM,DN)]:
            total=defaultdict(F)
            for h in P:
                for k,a in R[h].items():
                    for j,b in R[k].items():total[h,j,v.key(v.product(left[s,h,k],right[s,k,j]))]+=a*b
            total={k:c for k,c in total.items()if c}
            need(total=={(h,h,v.key(v.op())):F(1)for h in P},'entire physical source cross bank is the inverse of its advertised A coefficient')
    return {'full112_bank_inverse_products':4,'actual_diagonal_ports':224,'cross_blocks_each_variant':n,'ordinary_boundary_occurrences':672,'extra_single_bank_square_translations':112,'old_HOST2_body_factor_rejected_blocks_each_variant':n,'method':'Direct canonical normalization proof plus independently constructed transvection routes and complete Z4 phase polynomials.'}

def bracket(n):
    D=10**36;target=n**199*D**200;a,b=0,n*D+1
    while b-a>1:
        m=(a+b)//2
        if m**200<=target:a=m
        else:b=m
    need(a**200<=target<b**200,'exact integer200th-root bound');return F(a,D),F(b,D)
def budget():
    recorded=load(AUTHOR/'BUDGET.json');profile={17:224,1:-112,2:-224,3:-224,5:-224,6:-224};lo=hi=F(0)
    for r,c in profile.items():
        a,b=bracket(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    a,b=map(F,recorded['strict_remaining_moment_interval']);need(max(a,lo)<=min(b,hi)and lo>0 and hi-112<0,'optimistic exact room and one-extra-query negative control')
    return {'optimistic_moment_gap':[str(lo),str(hi)],'display':float(lo),'one_extra_head_query_gap_upper':str(hi-112),'complete_actual_caller':False}
PIN='e0bc347e6a90ca212337c95a1b7b47bdeaa6f8bf7fa607da3ea93670e53866f4'
def main():
    global AUTHOR
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();AUTHOR=a.author
    need(hashlib.sha256((AUTHOR/'FREEZE.json').read_bytes()).hexdigest()==PIN,'frozen author package');freeze=load(AUTHOR/'FREEZE.json')
    for name,pin in freeze['files'].items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen file '+name)
    parent=load(AUTHOR/'source/R0-MINIMAL-WORD.json.gz');P,R,source=source_review(parent)
    out={'status':'PASS_INDEPENDENT_ACTUAL_MIXED_SLOPE_REVIEW','author_freeze':PIN,'author_proof':freeze['files']['PROOF.md'],'source_words':source,'physical_interface':interface(parent,P,R),'optimistic_budget':budget(),'scope':'Actual opposite public slopes and complete arbitrary-input source maps are established. Cross terms genuinely omit the leading body factor. No assembled extraction, supplier or kappa; the separately proved formal even-body obstruction is not an actual-route impossibility.'}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'sources':[{'name':z['variant'],'inputs':z['all_input_columns'],'profile':z['profile']}for z in source],'interface':out['physical_interface'],'optimistic_gap':out['optimistic_budget']['display']}))
if __name__=='__main__':main()
