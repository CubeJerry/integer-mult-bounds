"""Independent combinatorial audit; does not import the author's checker."""
import argparse, hashlib, itertools, json
from fractions import Fraction
from pathlib import Path

def word_for_transposition(a, b, h):
    path = [a]
    for bit in range(h):
        if (a ^ b) >> bit & 1:
            path.append(path[-1] ^ (1 << bit))
    edges = list(zip(path, path[1:]))
    return edges + edges[-2::-1]

def apply_edge(x, edge):
    a, b = edge
    return b if x == a else a if x == b else x

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    source=args.source.read_bytes()
    assert hashlib.sha256(source).hexdigest() == '71383358c9b38e91f827932dda429c165fb0bce934b14b6da83e44f30efff98d'
    gray_cases=0
    for g in range(1,8):
        gray=[k^(k>>1) for k in range(1<<g)]
        assert len(set(gray))==1<<g
        edges=[gray[i]^gray[(i+1)%len(gray)] for i in range(len(gray))]
        assert all(e and e&(e-1)==0 for e in edges)
        for u,x in itertools.product(range(1<<g),repeat=2):
            value=0
            for eps in gray:
                value ^= int((u^(eps&x))==(1<<g)-1)
            assert value==int(x==(1<<g)-1);gray_cases+=1
    transpositions=0;negative=0
    for h in range(1,7):
        for a,b in itertools.combinations(range(1<<h),2):
            word=word_for_transposition(a,b,h)
            assert len(word)<=2*h-1
            for x in range(1<<h):
                y=x
                for edge in word:y=apply_edge(y,edge)
                assert y==apply_edge(x,(a,b))
            if len(word)>1:
                y=a
                for edge in word[:-1]:y=apply_edge(y,edge)
                # Omission must change some input, even when a is unaffected.
                assert any(replay(x,word[:-1])!=apply_edge(x,(a,b)) for x in range(1<<h))
                negative+=1
            transpositions+=1
    bounds=0
    for g in range(1,65):
        for p0 in range(1,65):
            ell=(p0-1).bit_length();G=4*ell+6;K=G+4*ell+10
            delta=p0*((g+1)*Fraction(1,2**G)+8*Fraction(2**G,2**K))
            assert delta<=Fraction(2*g+3,128*p0**3);bounds+=1
    args.out.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS_ROOT_FIXED_MONOMIAL_REVIEW','gray_cases':gray_cases,
            'hypercube_transpositions':transpositions,'omitted_return_controls':negative,
            'exact_guard_bounds':bounds,'proof_sha256':hashlib.sha256(source).hexdigest(),
            'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

def replay(x,word):
    for edge in word:x=apply_edge(x,edge)
    return x

if __name__=='__main__':main()
