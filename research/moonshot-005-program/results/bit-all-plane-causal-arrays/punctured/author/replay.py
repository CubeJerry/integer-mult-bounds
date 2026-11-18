#!/usr/bin/env python3
"""Replay the actual causal local word and supply a common-F128 full-H word."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import gzip,json
from build import DEG,MOD,binary_rows,compile_rows,mul,need,power

def main():
    p=ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    coeff=json.loads((a.out/'COEFFICIENTS.json').read_text());base=json.loads(gzip.decompress((a.out/'ADD-WORD.json.gz').read_bytes()));result=json.loads((a.out/'RESULT.json').read_text());e=coeff['planes'][0]
    C=[[int(row[2*j:2*j+2],16)for j in range(90)]for row in e['C_hex_rows']]
    V=[[power(i+1,j)for j in range(90)]for i in range(90)];A=binary_rows(V);CB=binary_rows(C);n=630;original=[1<<j for j in range(2*n)];expected=A+[CB[i]^(A[i]<<n)for i in range(n)]
    def run(skip_copy=None):
        public=list(original);cache=[0]*n
        for i in range(n):
            if i!=skip_copy:cache[i]^=public[i]
        for i,j in base['ADD']:public[i]^=public[j]
        for i,j in base['ADD']:public[n+i]^=public[n+j]
        cross_count=0
        for i,row in enumerate(CB):
            while row:
                bit=row&-row;j=bit.bit_length()-1;row^=bit;public[n+i]^=cache[j];cross_count+=1
        return public,cache,cross_count
    actual,cache,cross=run();need(actual==expected,'all1260 original binary columns, arbitrary early and late inputs')
    need(cache==[1<<j for j in range(n)],'each cache owner remains dirty and can retire')
    bad,_,_=run(0);need(bad!=expected,'omitted early cache copy is rejected')
    need(any(CB),'nonzero crosswave map');zero_cross=A+[a<<n for a in A];need(zero_cross!=expected,'omitted crosswave stage is rejected')
    # A single common field is available for both ordinary H families.
    V45=[[power(i+1,j)for j in range(45)]for i in range(45)];M45=binary_rows(V45);word45=compile_rows(M45)
    raw=json.dumps({'schema':'F128-V45-binary-ADD-v1','field_modulus':MOD,'binary_records':315,'ADD':word45},separators=(',',':')).encode()+b'\n';(a.out/'FULL-H-ADD-WORD.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    full_cost=881*24*(len(word45)+44*3*DEG)
    out={'status':'PASS_LITERAL_CAUSAL_WORD_AND_COMMON_FIELD','field_modulus':MOD,'field_degree':DEG,'sample_H':e['H'],'original_binary_columns_replayed':1260,'early_cache_binary_owners_per_stripe':630,'sample_crosswave_ADD_per_stripe':cross,'sample_ADD_per_stripe_without_holder_permutation':2*len(base['ADD'])+cross+630,'dirty_CACHE_CLEAR_per_stripe':630,'negative_controls':{'omitted_early_cache_copy_rejected':True,'omitted_crosswave_stage_rejected':True,'zero_crosswave_projection_rank_upper_bound':45,'required_source_projection_rank':60},'uniform_F128_full_H_V45_binary_records':315,'uniform_F128_full_H_V45_ADD':len(word45),'uniform_F128_full_H_word_uncompressed_sha256':sha256(raw).hexdigest(),'uniform_F128_all_881_full_H_ADD_with_permutation_bound':full_cost,'uniform_F128_all_1108_ordinary_H_ADD_with_permutation_bound':full_cost+result['full_ADD_count_all_227_H_including_permutation_bound'],'all_227_two_donor_H_extra_INIT_and_dirty_CLEAR_each':227*540*DEG,'global_source_or_later_transport_claimed':False}
    (a.out/'REPLAY-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
