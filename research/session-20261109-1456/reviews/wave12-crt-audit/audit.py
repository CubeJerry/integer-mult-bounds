"""Exact read-only source-order controls; no native CRT/carry execution."""
from pathlib import Path
import hashlib,importlib.util,itertools,json,math
ROOT=Path(__file__).resolve().parent

def need(ok,message):
    if not ok:raise ValueError(message)

def digits(k,moduli):
    result=[]
    for s in moduli:result.append(k%s);k//=s
    need(k==0,'complete mixed-radix integer');return tuple(result)

def phi(k,moduli):
    prefix=1;result=[]
    for s in moduli:result.append(k*pow(prefix,-1,s)%s);prefix*=s
    return tuple(result)

def colex_rank(y,moduli):
    answer=0;prefix=1
    for digit,s in zip(y,moduli):answer+=digit*prefix;prefix*=s
    return answer

def natural_rank(y,moduli):
    answer=0
    for digit,s in zip(y,moduli):answer=answer*s+digit
    return answer

def carry(coefficients,b,number_of_digits):
    radix=2**b;c=0;out=[]
    for value in coefficients:
        value+=c;out.append(value%radix);c=value//radix
    while c:out.append(c%radix);c//=radix
    need(all(x==0 for x in out[2*number_of_digits:]),'zero excess product digits')
    out=(out+[0]*(2*number_of_digits))[:2*number_of_digits]
    return sum(v*radix**i for i,v in enumerate(out)),''.join(format(v,f'0{b}b') for v in reversed(out))

def main():
    sources=json.loads((ROOT/'SOURCES.json').read_text())['files']
    for row in sources:
        raw=(ROOT/row['checkpoint_path']).read_bytes()
        need(hashlib.sha256(raw).hexdigest()==row['sha256'],'exact source bytes')
        need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==row['git_blob'],'exact source blob')
    spec=importlib.util.spec_from_file_location('pinned_batched_crt',ROOT/'sources/check_batched_crt.py')
    canonical=importlib.util.module_from_spec(spec);spec.loader.exec_module(canonical)
    cases=[]
    for moduli in ((3,5),(5,7),(3,5,7,11)):
        S=math.prod(moduli);inverse={phi(k,moduli):k for k in range(S)}
        need(len(inverse)==S,'scaled CRT bijection')
        field=[None]*S
        for y,k in inverse.items():field[colex_rank(y,moduli)]=k
        wrong=0
        for k in range(S):
            y=phi(k,moduli)
            need(canonical.balanced(y,moduli,reverse=True)==digits(k,moduli),
                 'canonical inverse returns source mixed-radix digits without an axis reversal')
            need(field[colex_rank(y,moduli)]==k,'colex compact consumer agreement')
            wrong+=int(field[natural_rank(y,moduli)]!=k)
        need(wrong>0,'unchanged natural-order consumer detects current colex mismatch')
        # Every literal shear copies all t target blocks in both passes.
        sizes=[1<<(s-1).bit_length() for s in moduli];T=math.prod(sizes);W=37
        for i,t in enumerate(sizes):
            before=math.prod(sizes[:i]);suffix=math.prod(sizes[i+1:])*W
            for offset in (0,moduli[i]-1):
                writes=2*before*(offset+(moduli[i]-offset)+(t-moduli[i]))*suffix
                need(writes==2*T*W,'unskipped full-field literal shear bill')
        cases.append(dict(moduli=moduli,S=S,T=T,natural_order_mismatches=wrong,
                          inverse_shear_output_writes=2*len(moduli)*T*W))
    moduli=(3,5);inverse={phi(k,moduli):k for k in range(15)}
    discriminator=dict(current_ordinal=1,current_coordinate=[1,0],correct_ordinary_index=inverse[(1,0)],
                       old_natural_interpretation=[0,1],wrong_ordinary_index=inverse[(0,1)])
    need(discriminator['correct_ordinary_index']==10 and discriminator['wrong_ordinary_index']==3,'exact source-order discriminator')
    n,b,q=9,4,3;X,Y=363,437;A=digits(X,(16,)*q);B=digits(Y,(16,)*q)
    coeff=[0]*15
    for i,a in enumerate(A):
        for j,bj in enumerate(B):coeff[i+j]+=a*bj
    value,bits=carry(coeff,b,q)
    need(value==X*Y and len(bits)==2*q*b and bits[:2*q*b-2*n]=='0'*(2*q*b-2*n),
         'existing carry output is exactly 2qb bits; zero trim gives promised 2n')
    need(int(bits[-2*n:],2)==X*Y,'exact output-length adapter')
    result=dict(status='PASS_READ_ONLY_CRT_INTERFACE_AUDIT',canonical_sources=len(sources),
                source_order_cases=cases,discriminator=discriminator,
                carry_extent=dict(n=n,b=b,Ndigits=q,returned_bits=len(bits),promised_bits=2*n,
                                  removable_leading_zeros=2*q*b-2*n,product=value),
                native_execution=False,new_theorem=False,new_kappa=False,
                disposition='Canonical written layout join is resolved; unchanged old Converter is superseded for this fine-family port. Full fast physical CRT payload controller remains external.')
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
