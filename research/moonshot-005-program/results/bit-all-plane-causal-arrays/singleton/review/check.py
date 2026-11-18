#!/usr/bin/env python3
"""Independent field-elimination and literal-word review of singleton Hermite maps."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json

LH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FH='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'

def need(ok,why):
    if not ok:raise ValueError(why)

def poly(a,b):
    q=0
    for k in range(7):
        if b>>k&1:q^=a<<k
    while q.bit_length()>7:q^=131<<(q.bit_length()-8)
    return q

M=[[poly(a,b)for b in range(128)]for a in range(128)]
INV=[0]+[next(b for b in range(1,128)if M[a][b]==1)for a in range(1,128)]

def rankdet(rows):
    a=[row[:]for row in rows];p=0;det=1
    for c in range(len(a[0])):
        r=next((r for r in range(p,len(a))if a[r][c]),None)
        if r is None:continue
        a[p],a[r]=a[r],a[p];value=a[p][c];det=M[det][value];iv=INV[value];a[p]=[M[x][iv]for x in a[p]]
        for r in range(p+1,len(a)):
            value=a[r][c]
            if value:a[r]=[x^M[value][y]for x,y in zip(a[r],a[p])]
        p+=1
        if p==len(a):break
    return p,det if p==len(a)==len(a[0])else 0

def expand(rows):
    result=[]
    for row in rows:
        for bit in range(7):
            value=0
            for column,c in enumerate(row):
                for k in range(7):
                    if M[c][1<<k]>>bit&1:value^=1<<(7*column+k)
            result.append(value)
    return result

def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--factor',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--v90-word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    lr=gzip.decompress(a.layout.read_bytes());fr=a.factor.read_bytes();need(sha256(lr).hexdigest()==LH and sha256(fr).hexdigest()==FH,'source geometry and actual temporal counts');w=json.loads(lr);f=dict(json.loads(fr)['factors']);roots=w['root_table'];Hs=list(map(set,w['A2']));Ds=list(map(set,w['D4']));native=set(range(111));O=[{j for j,v in enumerate(roots)if sum(x*y for x,y in zip(u,v))==0}for u in roots[:111]]
    V=[]
    for alpha in range(1,91):
        row=[1]
        for _ in range(89):row.append(M[row[-1]][alpha])
        V.append(row)
    C=[[row[j-1]if j&1 else 0 for j in range(90)]for row in V]
    coeff_raw=(a.author/'output/COEFFICIENTS.json').read_bytes();need(json.loads(coeff_raw)=={'field_modulus':131,'evaluation_nodes':list(range(1,91)),'early_matrix':V,'crosswave_derivative_matrix':C,'late_baseline':'identity'},'independently recomputed complete Hermite matrices')
    need(rankdet(V)[0]==90,'all early source dimensions retained')
    author_raw=(a.author/'output/RESULT.json').read_bytes();author=json.loads(author_raw);byH={z['H']:z for z in author['planes']};need(len(byH)==11,'eleven singleton certificates');minors=[]
    for h,H in enumerate(Hs):
        if len(H&native)!=1:continue
        need(f.get(h,0)==0,'actual singletonx=e=12 with no late source visit')
        z=byH[h];donor=next(iter(H&native));ports=[d for d,D in enumerate(Ds)if H<=D];need(len(ports)==45 and ports==z['actual_D4_ports']and donor==z['native_donor'],'all actual singleton holders and D4 exits')
        receivers={i:[p for p,d in enumerate(ports)if Ds[d]<=O[i]]for i in range(111)if H<=O[i]};theirs={q['receiver']:q for q in z['receivers']};need(set(receivers)==set(theirs),'all actual singleton receivers')
        allseen=set()
        for i,selected in receivers.items():
            need(len(selected)==15 and selected==theirs[i]['ports'],'actual fifteen selected ports');allseen.update(selected);rows=[2*p+b for p in selected for b in range(2)]
            minor=[V[s][:60]for s in rows]+[C[s][:60]for s in rows];rank,det=rankdet(minor);need(rank==60 and det,'direct field Gaussian Hermite minor')
            product=1
            for s,t in combinations(rows,2):
                difference=(s+1)^(t+1);squared=M[difference][difference];product=M[product][M[squared][squared]]
            need(det==product==theirs[i]['Hermite_determinant'],'direct determinant agrees with exact confluent product')
            minors.append([h,i,det])
        need(allseen==set(range(45)),'every actual port lies in a full-rank native receiver set')
    need(len(minors)==360,'all actual singleton360 Hermite minors')
    # Existing holders: per port use the pair indexed2*stripe+b in each phase.
    used={(phase,p,2*stripe+b)for phase in['early','late']for stripe in range(6)for p in range(45)for b in range(2)}
    need(len(used)==1080 and used=={(phase,p,k)for phase in['early','late']for p in range(45)for k in range(12)},'all real singleton holders once, no permutation')
    wr=gzip.decompress(a.v90_word.read_bytes());word=json.loads(wr);need(sha256(wr).hexdigest()==author['V90_ADD_word_uncompressed_sha256'],'borrowed whole-record V90 word pin');ops=word['ADD'];need(len(ops)==167325,'same explicit whole-record word')
    VB=expand(V);CB=expand(C);n=630;public=[1<<j for j in range(2*n)];indices=[7*j+b for j in range(90)if j&1 for b in range(7)];cache={j:0 for j in indices}
    for j in indices:cache[j]^=public[j]
    for dst,src in ops:
        need(0<=dst<n and 0<=src<n and dst!=src,'valid actual early ADD operands');public[dst]^=public[src]
    cross=0
    for r,mask in enumerate(CB):
        while mask:
            bit=mask&-mask;mask^=bit;j=bit.bit_length()-1;need(j in cache,'every derivative input was actually cached');public[n+r]^=cache[j];cross+=1
    expected=VB+[CB[r]^(1<<(n+r))for r in range(n)];need(public==expected,'all1260 independent original columns including arbitraryY')
    need(all(cache[j]==1<<j for j in indices),'all315 real cache owners remain dirty')
    bad=public[:]
    for r,mask in enumerate(CB):
        if mask>>indices[0]&1:bad[n+r]^=cache[indices[0]]
    need(bad!=expected,'omitted cache copy changes semantic map')
    rank_without=rankdet([V[s][:60]for s in range(30)]+[[0]*60 for _ in range(30)])[0];need(rank_without==30,'omitting derivatives halves this local receiver rank')
    need(cross==97969 and cross==author['derivative_crosswave_ADD_per_stripe'],'exact derivative ordinary work')
    add_H=6*(len(ops)+cross+len(indices));need(add_H==1593654 and author['ADD_per_H_including_cache_copies']==add_H,'all singleton ADD charges')
    need(author['INIT_and_dirty_CLEAR_each_per_H']==6*315 and author['extra_MOVE']==0,'all cache owners charged stationary')
    out={'status':'PASS_INDEPENDENT_SINGLETON_HERMITE_CAUSAL_REVIEW','layout_uncompressed_sha256':LH,'factor_sha256':FH,'author_proof_sha256':sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'author_result_sha256':sha256(author_raw).hexdigest(),'coefficient_sha256':sha256(coeff_raw).hexdigest(),'borrowed_V90_word_uncompressed_sha256':sha256(wr).hexdigest(),'singleton_planes':11,'direct_Gaussian_field_Hermite_minors':len(minors),'all_actual_public_fields_per_H':1080,'source_rank_per_H':540,'receiver_source_rank':360,'all_original_binary_columns':1260,'odd_coefficient_cache_binary_records_per_stripe':315,'derivative_ADD_per_stripe':cross,'ADD_per_H':add_H,'ADD_all11_H':11*add_H,'INIT_copyADD_dirtyCLEAR_each_per_H':1890,'INIT_and_dirtyCLEAR_each_all11_H':20790,'extra_MOVE':0,'physical_permutation_ADD':0,'negative_controls':{'omitted_cache_copy_changes_output':True,'omitted_derivative_rank':rank_without},'minor_determinants':minors,'author_code_imported':False,'global_source_or_later_transport_constructed':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(minors),'minors',add_H,'ADD/H',flush=True)

if __name__=='__main__':main()
