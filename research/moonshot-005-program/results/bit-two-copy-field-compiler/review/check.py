#!/usr/bin/env python3
"""Separate F4 algebra/compiler review, paired with C's physical replay."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

PIN = '9cda39e27c2416a4eac6dbb714bc53239f1cb1c83ba4423ee50a704fc14df550'
NATIVE = 'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
PARENT = 'research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint5-evidence/A/full-half-reservoir/WORD.json'
A, B = [14,17,19,20], [96,99,101,102]

def mul(a,b):
    z = 0
    for j in range(2):
        if b >> j & 1: z ^= a << j
    if z & 4: z ^= 7
    return z

def inv(a):
    return next(b for b in range(1,4) if mul(a,b) == 1)

def need(ok,msg):
    if not ok: raise ValueError(msg)

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--word',type=Path,required=True);p.add_argument('--cut',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(sha256(a.word.read_bytes()).hexdigest()==PIN,'word pin')
    native=(a.repo/NATIVE).read_bytes();parent_raw=(a.repo/PARENT).read_bytes()
    need(sha256(native).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native pin')
    need(sha256(parent_raw).hexdigest()=='6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980','parent pin')
    roots=json.loads(native)['native_roots'];parent=json.loads(parent_raw);w=json.loads(a.word.read_bytes())
    # Authenticate the literal two complete parent prefixes independently.
    inherited=[]
    for c in range(2):
        for op,n,*q in parent['operations'][:parent['carrier_interface_before_operation']]:
            inherited.append([op,f'C{c}__{n}']+([f'C{c}__{q[0]}'] if op=='ADD' else q))
    need(w['operations'][:len(inherited)]==inherited,'both actual separately paid source prefixes')
    need(w['construction']['parent_copy_prefix_cut']==len(inherited)==3786,'parent prefix boundary')
    seed=[(i+1)%4 for i in range(4)]+[4+(i-1)%4 for i in range(4)]
    payload=[[int(j==seed[i]) for j in range(8)] for i in range(8)]
    network=[[int(i==j) for j in range(8)] for i in range(8)]
    matrices=[];programs=w['construction']['local_ADD_programs'];controls=0
    for r in range(3):
        for i in range(4):
            j=4+(i+r)%4;p_i,q_i=((1,2) if i%2==0 else (2,1))
            matrix=([[1,p_i],[1,q_i]] if r==0 else [[1,0],[1,1]] if r==1 else [[1,1],[inv(p_i),inv(q_i)]])
            matrices.append(matrix)
            need(mul(matrix[0][0],matrix[1][1])^mul(matrix[0][1],matrix[1][0]),'invertible F4 edge')
            for rows in (payload,network):
                left,right=rows[i][:],rows[j][:]
                rows[i]=[mul(matrix[0][0],x)^mul(matrix[0][1],y)for x,y in zip(left,right)]
                rows[j]=[mul(matrix[1][0],x)^mul(matrix[1][1],y)for x,y in zip(left,right)]
            binary=[sum(((mul(matrix[x//2][y//2],1<<(y%2))>>(x%2))&1)<<y for y in range(4))for x in range(4)]
            program=programs[4*r+i];row=[1<<x for x in range(4)]
            for source,target in program: row[target]^=row[source]
            need(row==binary,'literal four-record ADD compiler')
            for source,target in reversed(program): row[target]^=row[source]
            need(row==[1<<x for x in range(4)],'literal inverse')
            for omitted in range(len(program)):
                row=[1<<x for x in range(4)]
                for k,(source,target)in enumerate(program):
                    if k!=omitted: row[target]^=row[source]
                need(row!=binary,'local omission negative control');controls+=1
    need(matrices==w['construction']['local_F4_matrices'],'edge-dependent coefficient record')
    need(sum(map(len,programs))==72,'full forward ordinary bill')
    for i,row in enumerate(payload):
        frame=range(4) if i<4 else range(4,8)
        need(row[i]==0 and all(row[j]==1 for j in frame if j!=i),'identity own-frame triples')
        need(sum(bool(z)for z in row)==6,'exactly six nonzero native blocks')
    native_rows=[sum(1<<j for j,s in enumerate(roots)if sum(x*y for x,y in zip(r,s))==0)for r in roots]
    expected={str(c):[(1<<i if i<8 else native_rows[i]&255)<<(222*c)for i in range(111)]for c in range(2)}
    for i,role in enumerate(A+B):
        for j,source in enumerate(A+B):
            coefficient=payload[i][j]
            need(not coefficient or native_rows[role]>>source&1,'native source geometry')
            for c in range(2):
                for d in range(2):
                    if mul(coefficient,1<<d)>>c&1: expected[str(c)][role]^=1<<(222*d+source)
    need({c:list(map(hex,rows))for c,rows in expected.items()}==w['Y_correction_rows_hex'],'all444 declared source columns independently derived')
    cut=json.loads(a.cut.read_bytes());V={z['name']:int(z['row_hex'],16)for z in cut}
    need(len(V)==812,'independently replayed full current inventory')
    for c in range(2):
        for i in range(111):
            need(V[f'C{c}__Y{i}']==(1<<(222*c+111+i))^expected[str(c)][i],'independent physical replay matches derived all-column algebra')
            need(V[f'C{c}__X{i}']==1<<(222*c+i),'all current original X restored')
    result={'status':'PASS_SEPARATE_F4_ALGEBRA_AND_WHOLE_RECORD_COMPILER','word_sha256':PIN,
            'source_cut_sha256':sha256(a.cut.read_bytes()).hexdigest(),'all_original_columns':444,
            'current_fields':812,'forward_ADDs':72,'inverse_ADDs':72,'seed_ADDs':16,
            'local_ADD_omission_controls':controls,'payload_F4_matrix':payload,'network_F4_matrix':network,
            'scope':'Independent coefficient, compiler and parent-prefix review, composed with C\'s separate complete physical replay. No new complete supplier or kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],'444 columns,72 local omission controls')

if __name__=='__main__':main()
