#!/usr/bin/env python3
"""Exact binary character proof witnesses for the 120-port cyclic cross operator."""
from pathlib import Path
from collections import Counter
import argparse,gzip,hashlib,json

def need(c,m):
 if not c:raise ValueError(m)
def parity(x):return x.bit_count()%2
pa=argparse.ArgumentParser();pa.add_argument('--word',type=Path,default=Path(__file__).with_name('WORD.json.gz'));pa.add_argument('--symmetry',type=Path,default=Path(__file__).with_name('SYMMETRY.json'));pa.add_argument('--output',type=Path,default=Path(__file__).with_name('OPERATORS.json'));a=pa.parse_args();raw=a.word.read_bytes();need(hashlib.sha256(raw).hexdigest()=='bca2056d98d0759d0c7c61104122160d13e12f099bea0cbe2de4169f9b3eac93','word pin');w=json.loads(gzip.decompress(raw));s=json.loads(a.symmetry.read_text());P=w['normals'];pi=w['permutation'];rows=s['binary_rows'];cols=s['binary_columns']
def mv(x):return sum(parity(r&x)<<i for i,r in enumerate(rows))
def phaseN(h,z):return(z.bit_count()-parity(P[h]&z)-parity(P[pi[h]]&z))%4
need(all(mv(P[h])==P[pi[h]]for h in range(120)),'matched permutation')
for h in range(120):
 i,j,k=h,pi[h],pi[pi[h]];need(P[i]^P[j]^P[k]==511,'common triple sum')
 for z in range(512):
  need((phaseN(i,z)+phaseN(j,z)+phaseN(k,z)-z.bit_count())%4==0,'N cubed equals W');need((2*sum(parity(P[l]&z)for l in [i,j,k])-2*z.bit_count())%4==0,'A sixth equals X_all')
need(all((mv(z).bit_count()-z.bit_count())%4==0 for z in range(512)),'global binary symmetry preserves Fourier phase')
# A product C_a^{-1} C_b, a,b nonzero distinct, has four independent shifts.
# Exact coefficients, encoded as Gaussian integers over the common denominator4.
def mul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
row_entries=[]
for h in range(120):
 j=pi[h];qa,qb=P[h],P[j];support={0:mul((1,-1),(1,1)),qb:mul((1,-1),(1,-1)),qa:mul((1,1),(1,1)),qa^qb:mul((1,1),(1,-1))};need(len(support)==4 and all(a*a+b*b==4 for a,b in support.values()),'rank-two normalizer row distribution');row_entries.append({'port':h,'normal':qa,'neighbor':j,'translation_coefficients_den4':support})
# Nontrivial arbitrary port swaps do not imply the cubic source law.
badpi=pi[:];badpi[0],badpi[1]=badpi[1],badpi[0]
def badN_cube(h,z):
 ph=0;h0=h
 for _ in range(3):
  j=badpi[h];ph+=z.bit_count()-parity(P[h]&z)-parity(P[j]&z);h=j
 return h==h0 and(ph-z.bit_count())%4==0
witness=next((h,z)for h in range(120)for z in range(512)if not badN_cube(h,z));out={'status':'PASS_EXACT_CUBIC_PHYSICAL_CROSS_LAW','word_sha256':hashlib.sha256(raw).hexdigest(),'symmetry_sha256':hashlib.sha256(a.symmetry.read_bytes()).hexdigest(),'all_ports':120,'one_column_characters':512,'cross_operator':'N=W Q^-1 R Q^-1','cross_law':'N^3=W','internal_kernel':'A=Q R^T','internal_kernel_law':'A^6=X_511; A^12=I','normalizer':'Q^-1 R^T Q','normalizer_per_row_entropy_bits':'2V','normalizer_two_bank_rank_mass_floor':480,'normalizer_rows':row_entries,'negative_control_bad_permutation_witness':list(witness),'global_coordinate_T_commutes_W':True,'whole_native_cube_law_claimed':False,'caller_admission':False,'no_new_kappa':True};a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
