#!/usr/bin/env python3
"""Independent exact aggregate P104 relay and monetary-census review."""
from collections import defaultdict,Counter
from fractions import Fraction as Q
from functools import reduce,cache
from math import gcd,lcm
import argparse,gzip,hashlib,json,subprocess
from pathlib import Path

HEAD="14c74c6a67108f675ac1196a5f2415ead0920e71"
SOURCE="research/p104-chart306-chain/"
WORD="7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48"
EARLIER_HEAD="89a67c404226d51028e135de2b9169e9020d57af"
EARLIER_WORD="c447b6d5ba956fbe40834fe3c1bc69af2f225736f1b97ecd84b57bab9dd283cb"
APP="1b2d87e93ae023f5ffd464546af53281b6cb4963dfd76ae4742e0a5540b752fa"

def rank(rows):
    """Sparse fraction-free elimination using primitive integer pivot rows."""
    piv={}
    for row in rows:
        v={k:x for k,x in row.items() if x}
        while v:
            s=min(v);p=piv.get(s)
            if p is None:
                g=reduce(gcd,v.values())
                if v[s]<0:g=-g
                if g not in (0,1):v={k:x//g for k,x in v.items()}
                piv[s]=v;break
            if len(p)==1:
                del v[s];continue
            a,b=v[s],p[s];g=gcd(a,b);a//=g;b//=g
            new={k:x*b for k,x in v.items()}
            for k,x in p.items():new[k]=new.get(k,0)-a*x
            v={k:x for k,x in new.items() if x}
            if v:
                g=reduce(gcd,v.values())
                if g>1:v={k:x//g for k,x in v.items()}
    return len(piv)

def orig_data(repo,name):
    # Packaging adapter. Prefer the upstream object when the checkout has it.
    # An offline checkout uses the exact indexed bytes from the staged package.
    root=Path(__file__).resolve().parent.parent
    spec=json.loads((root/'history/INDEX.json').read_text())[name]
    cmd=['git','-C',str(repo),'cat-file']
    have=subprocess.run(cmd+['-e',spec['commit']],capture_output=True).returncode==0
    if have:
        raw=subprocess.check_output(cmd+['blob',spec['commit']+':'+spec['path']])
    else:
        raw=(root/spec['local']).read_bytes()
        if spec['decompress']:raw=gzip.decompress(raw)
    assert hashlib.sha256(raw).hexdigest()==spec['sha256']
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()==spec['git_blob']
    return raw

def sparse_structure(src,word,app):
    m={e:(a,b) for e,a,b in word['moves']}; n=word['first_output'];dims=list(map(len,word['frames']))
    arriving=defaultdict(list);leaving=defaultdict(list);byedge=defaultdict(list)
    for e,(a,b) in m.items():
        arriving[b].append(e);leaving[a].append(e);byedge[a,b].append(e)
    for i,(a,b) in enumerate(zip(word['initial'],word['final'])):
        arriving[a].append(~i);leaving[b].append(n+i)
    F={};QF={};cl=defaultdict(list)
    for f,lst in word['forms']:
        qq={e:Q(q) for e,q in lst}
        den=lcm(*(x.denominator for x in qq.values()));F[f]={e:x.numerator*(den//x.denominator) for e,x in qq.items()}
        QF[f]=qq
        for e in qq:cl[e].append(f)
    ready=set(~i for i in range(1289));incoming={i:set(v) for i,v in arriving.items()}
    for f in word['schedule']:
        here=m[f][0] if f in m else word['final'][f-n]
        assert F[f].keys()<=ready&incoming[here]
        ready.add(f)
    hs=Counter();arc=set();private=set()
    for f,(a,b) in m.items():
        for e in F[f]:
            if e in m and m[e][1]==a and (dims[m[e][0]]-dims[a])*(dims[a]-dims[b])>0:
                arc.add((e,f))
                if len(cl[e])==1 or len(F[f])==1:private.add((e,f))
    complex_counts=Counter()
    for (a,b),X in byedge.items():
        os={m[t][1] for t in leaving[b] if t in m}
        X=set(X)
        for c in os:
            if (dims[a]-dims[b])*(dims[b]-dims[c])<=0:continue
            Y=set(byedge[b,c]);Z=set(arriving[b])-X;W=set(leaving[b])-Y
            A=[{x:v for x,v in F[f].items() if x in X} for f in W]
            D=[{z:v for z,v in F[f].items() if z in Z} for f in Y]
            C=[{x:v for x,v in F[f].items() if x in X} for f in Y]
            ra=rank(A);rd=rank(D)
            live=rank(A+[F[f] for f in Y])
            assert rank(A+C)==len(X) and rank([F[f] for f in Y])==len(Y),(a,b,c,'boundary')
            assert live==ra+rd,(a,b,c,'rational bypass',live,ra,rd)
            complex_counts['all']+=1
            complex_counts['A_has_kernel']+=ra<len(X)
            complex_counts['A_and_D_have_kernels']+=(ra<len(X) and rd<len(Y))
    def hist(arcs):
        next0=dict(arcs);old={f for e,f in arcs};assert len(old)==len(next0)==len(arcs)
        seen=set();result=Counter()
        for e0 in m.keys()-old:
            e=e0;s=0
            while True:
                assert e not in seen;seen.add(e);a,b=m[e];s+=abs(dims[a]-dims[b])
                if e not in next0:break
                e=next0[e]
            assert s==abs(dims[m[e0][0]]-dims[m[e][1]]);result[s]+=1
        assert seen==m.keys();return result
    extra=[tuple(t) for t in json.loads((src/'contested-witness.json').read_text())]
    assert len(extra)==152 and set(extra)<=arc-private
    costs=[hist(q) for q in ([],private,private|set(extra),private|set(extra[:-1]))]
    assert costs[0]=={int(k):v for k,v in app['native']['paid_native_ranks'].items()}
    return complex_counts,(len(arc),len(private)),costs,QF

GRID=10**40
def rounded(x,y):return Q((x*GRID).__floor__(),GRID),Q((y*GRID).__ceil__(),GRID)
def total(v):return sum(x for x,y in v),sum(y for x,y in v)
def difference(x,y):return x[0]-y[1],x[1]-y[0]
def scale(a,r):return (a*r[0],a*r[1]) if a>=0 else (a*r[1],a*r[0])
def prod(x,y):return rounded(x[0]*y[0],x[1]*y[1])
def recip(x):return rounded(1/x[1],1/x[0])
@cache
def ln_unit(x):
    v=(x-1)/(x+1);t=2*sum(v**(2*i+1)/(2*i+1) for i in range(48))
    return rounded(t,t+2*v**97/(97*(1-v*v)))
@cache
def log(x):
    x=Q(x);s=0
    while x>=2:x/=2;s+=1
    return total([ln_unit(x),scale(s,ln_unit(Q(2)))])
@cache
def power(x,k):
    x=Q(x);k=Q(k)
    lo,hi=scale(k,log(x))
    def bounds(t):
        z=Q(1);tot=z
        for i in range(1,24):z*=-t/i;tot+=z
        return tot,tot-z*t/24
    return rounded(x*bounds(hi)[0],x*bounds(lo)[1])
def positive_exp(x,s):return recip(scale(1/Q(x),power(x,s)))
def moment(h,k):return total([scale(n,power(r,k)) for r,n in h.items()])
def rates(costs,app,cert):
    census=app['caller_census']
    def h(r):return Counter({int(k):v for k,v in r.items()})
    m=census['calls'];assert m==48
    H=h(app['native']['positive_helper_ranks']);P=h(census['fixed_caller_paid']);T=h(census['fixed_root_targets'])
    T.update({r:m*n for r,n in H.items()})
    def profile(n):
        p=P.copy();p.update({r:m*v for r,v in n.items()});return p
    k=Q(1,200);trial=Q('0.0050005')
    def gap(h,p):return difference(moment(T,p),moment(profile(h),p))
    d0=gap(costs[0],k);private=gap(costs[1],k);witness=gap(costs[2],k);trunc=gap(costs[3],k)
    extra=difference(total([power(4,k),power(5,k)]),power(9,k))
    residual=scale(Q(-1,m),private)
    assert 126*extra[1]<residual[0] and residual[1]<127*extra[0]
    assert d0[1]<0< witness[0] and trunc[1]<0
    assert gap(costs[2],Q('.00500109954083'))[0]>0 and gap(costs[2],Q('.00500109954084'))[1]<0
    p=profile(costs[2]);pt=moment(p,trial);tt=moment(T,trial);p1=sum(r*n for r,n in p.items());v=2**30
    d1=scale(1/Q(sum(T.values())),total([scale(n,log(r)) for r,n in T.items()]))
    d2=scale(1/Q(p1),total([scale(r*n,log(r)) for r,n in p.items()]))
    assert difference(d1,d2)[0]>log(2)[1]/8
    n={int(k):v for k,v in cert['mode'].items()}
    W={r:scale(t,power(r,trial)) for r,t in T.items()}
    assert sum(n.values())==v and all(W[i][0]/n[i]>W[j][1]/(n[j]+1) for i in n for j in n)
    low=Q(239,10);high=Q(49,2);s=Q(1,1000)
    assert total([scale(t,log(r)) for r,t in n.items()])[0]>v*log(low)[1]
    delta=min(1-pt[1]/tt[0],1-p1/(tt[0]*positive_exp(70,trial/2)[0]))
    assert v*delta>689 and len(T)==16 and 16*31+3==499
    assert tt[1]*70**5 < low**10*power(low,trial)[0]
    assert prod(pt,positive_exp(high,s))[0]>moment(T,trial-s)[1]
    assert p1>tt[1]*positive_exp(8,trial)[1]
    assert pt[0]>power(high,trial)[1]*Q(31,10)**9 and high/8<Q(31,10)
    return {'original_gap':float(d0[0]),'private_gap':float(private[0]),'witness_gap':float(witness[0]),'remove_last_gap':float(trunc[0]),
            'raw_trial_gap':float(difference(tt,pt)[0]),'native_hist':costs[2],'floor_v_delta':int(v*delta),
            'degree10_funds':True,'homogeneous_degree9_excluded':True}

def arithmetic(w,qq):
    # A separate base-power identity test for all 1,289 arbitrary originals.
    # First bound every possible digit magnitude via the scalar L1 path mass.
    n=len(w['initial']);order=w['schedule'];m=w['first_output']
    den={~i:1 for i in range(n)};mass={~i:1 for i in range(n)};coeff={}
    for f in order:
        d=lcm(*(den[e]*s.denominator for e,s in qq[f].items()))
        vv={e:s.numerator*(d//(den[e]*s.denominator)) for e,s in qq[f].items()}
        den[f]=d;coeff[f]=vv
        mass[f]=sum(abs(a)*mass[e] for e,a in vv.items())
    bits=512
    assert (2*max(max(mass.values()),max(den.values()))+1).bit_length()+2<=bits
    vals={~i:1<<(bits*i) for i in range(n)}
    use=Counter(e for f in order for e in qq[f])
    wrong=[];ends=[]
    for f in order:
        vals[f]=sum(c*vals[e] for e,c in coeff[f].items())
        if f>=m:
            ends.append((f,vals[f],den[f]))
            identity=den[f]<<(bits*(f-m))
            if vals[f]!=identity:wrong.append(f)
        for e in coeff[f]:
            use[e]-=1
            if not use[e]:vals.pop(e,None)
    return sorted(ends),{'exact_terminal_rows':n,'own_coordinate_identities':n-len(wrong),'integer_pack_bits_per_digit':bits,
            'integer_bound_signal_bits':max(mass.values()).bit_length(),'max_denominator_bits':max(den.values()).bit_length()}

def main():
    p=argparse.ArgumentParser()
    for n in ('canonical','author','out'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();src=a.author/'sources'
    blob=orig_data(a.canonical,'DOUBLE-CANDIDATE.json.gz')
    appblob=orig_data(a.canonical,'DOUBLE-APPLICATION.json')
    assert blob==(src/'DOUBLE-CANDIDATE.json.gz').read_bytes()
    assert appblob==gzip.decompress((src/'DOUBLE-APPLICATION.json.gz').read_bytes())
    raw=gzip.decompress(blob);assert hashlib.sha256(raw).hexdigest()==WORD and hashlib.sha256(appblob).hexdigest()==APP
    word=json.loads(raw);app=json.loads(appblob);ref=json.loads((a.author/'output/RESULT.json').read_text())
    cut,arcs,costs,qq=sparse_structure(src,word,app)
    print('cut',cut,'arcs',arcs,flush=True)
    prices=rates(costs,app,ref['conditional_complex_compiler']);print('prices',prices,flush=True)
    terminal,coeff=arithmetic(word,qq)
    before=json.loads(gzip.decompress(orig_data(a.canonical,'CANDIDATE.json.gz')))
    pterms={f:{e:Q(s) for e,s in inputs} for f,inputs in before["forms"]}
    old,prior=arithmetic(before,pterms)
    assert all(i==j and x*b==y*a0 for (i,x,a0),(j,y,b) in zip(terminal,old))
    coeff["exact_equal_to_pre_second_contraction_terminals"]=len(old)
    initial_raw=orig_data(a.canonical,'ORIGINAL-WORD.json.gz')
    raw0=gzip.decompress(initial_raw)
    assert hashlib.sha256(raw0).hexdigest()==EARLIER_WORD
    first=json.loads(raw0)
    old0,firstbound=arithmetic(first,{f:{e:Q(s) for e,s in terms} for f,terms in first['forms']})
    assert len(terminal)==len(old)==len(old0)==1289
    # The base encoding is injective even after clearing two independently
    # computed rational denominators in a comparison of signed digit vectors.
    cross_bits=max(max(coeff['integer_bound_signal_bits']+b['max_denominator_bits'],
                       b['integer_bound_signal_bits']+coeff['max_denominator_bits'])+1 for b in (prior,firstbound))
    assert cross_bits<coeff['integer_pack_bits_per_digit']
    coeff['cross_difference_coefficient_upper_bits']=cross_bits
    assert all(i==j and x*b==y*d for (i,x,d),(j,y,b) in zip(terminal,old0))
    coeff['exact_equal_to_pre_first_contraction_terminals']=len(old0)
    coeff['original_word_decompressed_sha256']=EARLIER_WORD
    print("arith",coeff,flush=True)
    out={'source_head':HEAD,'word':WORD,'application':APP,'source_literal_count':sum(len(v) for v in qq.values()),
         'exact_rational_relay_counts':cut,'monotone_arcs':arcs[0],'private_arcs':arcs[1],'dyadic_independent_rates':prices,
         'exact_arithmetic':coeff}
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
