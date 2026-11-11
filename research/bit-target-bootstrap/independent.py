"""Independent exact bootstrap audit: matrix iteration and feasible intervals."""
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent

def check(v, label):
    if not v:
        raise ValueError(label)

def matrix_step(C, num, den):
    return C*den, (1+C)*den-num

def attained_interval(C, b, target):
    # Solve the source separators directly, without an optimizer routine.
    d = C-b
    lower = C/(1+d)
    upper = min((C-target)/d, (1-C)/(1-d))
    return lower, upper

def sep(C, b, rho, target):
    main = C-rho*(C-b)
    return (target-b, main-target, rho-main, 1-rho-main)

def log_interval(r):
    # Independent logarithm enclosure by repeated halving and atanh expansion.
    e = r.bit_length()-1
    vals = []
    for a,b in ((r,2**e),(2,1)):
        z = F(a-b,a+b)
        power = z
        total = F(0)
        for n in range(64):
            total += 2*power/(2*n+1)
            power *= z*z
        err = 2*power/(129*(1-z*z))
        vals.append((total,total+err))
    return vals[0][0]+e*vals[1][0], vals[0][1]+e*vals[1][1]

def power_lower(r,k):
    # Bernoulli: r*exp(-k ln r) >= r*(1-k*upper(ln r)).
    return r*(1-k*log_interval(r)[1])

def run(package=None, source_roots=None):
    if package is None:
        package=OUT if (OUT/'SOURCES.json').is_file() else ROOT/'work-interface/research/bit-target-bootstrap'
    if source_roots is None:
        source_roots=[package.parents[1],ROOT/'work-interface/source',ROOT/'source']
    cases = rho_cases = 0
    for C in (F(1,200),F(1,100),F(1,8),F(1,3),F(49,100)):
        for part in range(10):
            b=C*part/10
            top=C/(1+C-b)
            check(b<top<C,'strict order')
            lo,hi=attained_interval(C,b,(b+top)/2)
            check(lo<hi and min(sep(C,b,(lo+hi)/2,(b+top)/2))>0,'witness')
            lo,hi=attained_interval(C,b,top)
            check(lo>=hi,'supremum equality must fail')
            for ir in range(1,101):
                rho=F(ir,101)
                main=C-rho*(C-b)
                check(min(rho,main,1-rho)<=top,'independent full-cost ceiling')
                rho_cases+=1
            num,den=b,F(1)
            for h in range(9):
                value=num/den
                cross=C**h*(C-b)/(1-b)
                check((C-value)/(1-value)==cross,'matrix/cross-ratio agreement')
                num,den=matrix_step(C,num,den)
                cases+=1
    k=F(1,200)
    old=F('0.00385248')
    threshold=k*(1-old)/(1-k)
    check(threshold==F(3112961,621875000),'target threshold')
    C=F('0.0050001')
    n1,d1=matrix_step(C,old,F(1))
    n2,d2=matrix_step(C,n1,d1)
    check(n1/d1<k<n2/d2,'exact two-stage barrier')
    controls={}
    test_C=F('.00501')
    a=test_C-F('.004')*(test_C-old)
    check(a>k and min(sep(test_C,old,F('.004'),k))<0,'adapter omission control')
    controls['omit_adapter']='would falsely admit target'
    lo,hi=attained_interval(C,old,n1/d1)
    check(lo==hi,'strict supremum equality control')
    controls['allow_supremum_equality']='zero atom/main gap'
    check(min(sep(C,old,F('.999'),F('.003853')))<0,'stock omission control')
    controls['omit_stock']='negative stock gap'
    check(C*(1-C+old)<n1/d1,'tied recurrence differs')
    controls['reuse_tied_affine_law']='different source optimization'
    stages=[]
    for target in (F('.00499424'),F('.00500007')):
        gaps=sep(C,old,F('.0051'),target)
        check(min(gaps)>0,'complete hypothetical witness')
        stages.append(list(map(str,gaps)))
        old=target
    cap=F(51,10000)
    deriv=sum(power_lower(r,cap)*log_interval(r)[0] for r in (9,4))
    deriv-=sum(r*log_interval(r)[1] for r in (7,3,5))
    check(deriv>F(19,200),'independent Bernoulli derivative bound')
    pins={}
    sources=json.loads((package/'SOURCES.json').read_text())
    for entry in sources['files']:
        candidates=[source_root/entry['path'] for source_root in source_roots]
        path=next(p for p in candidates if p.is_file())
        raw=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        sha=hashlib.sha256(raw).hexdigest()
        check(blob==entry['git_blob'] and sha==entry['sha256'],'source identity')
        pins[entry['path']]=dict(git_blob=blob,sha256=sha)
    return dict(status='PASS_INDEPENDENT_BOOTSTRAP_REVIEW',matrix_cases=cases,
                rho_grid_cases=rho_cases,one_stage_threshold=str(threshold),
                stage_gaps=stages,lift_derivative_lower='19/200',
                lift_interval='[0,51/10000]',negative_controls=controls,sources=pins)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--package',type=Path)
    parser.add_argument('--source-root',type=Path,action='append')
    args=parser.parse_args()
    result=run(args.package,args.source_root)
    print(json.dumps(result,indent=2))
