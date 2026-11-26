"""Exact checks for the native root literal and its derived constants."""
import argparse
from fractions import Fraction
import json

def ceil_cube_root_fraction(numerator,denominator):
    lo,hi=0,1
    while hi**3*denominator<numerator:
        hi*=2
    while hi-lo>1:
        mid=(hi+lo)//2
        if mid**3*denominator>=numerator:
            hi=mid
        else:
            lo=mid
    return hi

def screen(word,limit):
    """Execute each forward and return transition of the finite-state guard.

    The integer phase denotes the currently occupied label of the literal
    bounded state chain. It describes the fixed transition function compactly;
    the modeled machine has no integer counter tape for this operation.
    """
    assert word and word[0] in b"01" and (word[0]!=48 or word==b"0")
    head=phase=clock=0
    length=len(word)
    while True:
        letter=word[head] if head<length else None
        clock+=1
        if letter is None:
            adaptive=False
            break
        if phase==limit:
            adaptive=True
            break
        head+=1
        phase+=1
    while head:
        head-=1
        clock+=1
    assert head==0 and clock<=2*length+3
    return adaptive,clock

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--literal",type=int,
                        help="traverse three genuine boundary descriptors for this fixed R")
    args=parser.parse_args()
    notable={}
    for root in range(240,4097):
        coefficient=ceil_cube_root_fraction(39**3*root,64)
        assert 64*(coefficient-1)**3<39**3*root<=64*coefficient**3
        assert (2*coefficient)**3>2**20
        assert 20*(2*coefficient)**3>root*(2**17+2)
        assert root>=2*120 and root>=8*10 and root>=34
        assert root//2>=2**6
        if root in (240,256,512,4096):
            notable[root]=coefficient
    m=2**19
    tail=(m**94+m**88+3*m**60+m**54+2**18*(m**58+m**32))
    assert tail<m**120
    assert 33*Fraction(1,4096)+3/Fraction(31,64)+Fraction(20,17)*Fraction(31,64)**2<Fraction(13,2)
    toy_count=0
    for limit in range(1,65):
        for digits in (1,max(1,limit-1),limit,limit+1,limit+2):
            decision,_=screen(b"1"+b"0"*(digits-1),limit)
            assert decision==(digits>limit)
            toy_count+=1
    output={"root_parameters":4096-240+1,"smooth_coefficients":notable,
            "small_literal_guards":toy_count}
    if args.literal:
        if not 240<=args.literal<=4096:
            parser.error("the established R interval is 240 through 4096")
        limit=args.literal*(2**17+2)
        actual=[]
        for size in (limit-1,limit,limit+1):
            decision,clock=screen(b"1"+b"0"*(size-1),limit)
            assert decision==(size>limit)
            actual.append({"digits":size,"adaptive":decision,"transitions":clock})
        output["literal_boundary"]=actual
    print(json.dumps(output,sort_keys=True))

if __name__=="__main__":
    main()
