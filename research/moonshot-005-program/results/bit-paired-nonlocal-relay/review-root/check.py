#!/usr/bin/env python3
"""Independent full symbolic/real-chart review of the nonlocal relay."""
import argparse,copy,hashlib,json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import sympy as sp

MASK=(1<<111)-1
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def xor(xs):
    z=0
    for x in xs:z^=x
    return z
def echelon(rows):
    out={}
    for i,x in enumerate(rows):
        c=1<<i
        while x:
            p=(x&-x).bit_length()-1
            if p in out:x^=out[p][0];c^=out[p][1]
            else:out[p]=(x,c);break
    return out
def solve(B,x):
    c=0
    for p in sorted(B):
        if x>>p&1:x^=B[p][0];c^=B[p][1]
    assert x==0,'missing linear target'
    return c
def rank(rows):return len(echelon(rows))

class Geometry:
    def __init__(self,charts,roots):
        self.rows={}
        for name,c in charts.items():
            m=sp.Matrix(c['rows']) if c['rows'] else sp.zeros(0,8)
            assert c['kind'] in ('span','ann')
            self.rows[name]=tuple(tuple(x)for x in (m.rowspace() if c['kind']=='span' else m.nullspace()))
        self.dim={n:len(x)for n,x in self.rows.items()}
        for i,r in enumerate(roots):
            L=sp.Matrix([r]);Fi=tuple(tuple(x)for x in L.nullspace())
            assert self.rows[f'L{i}']==tuple(tuple(x)for x in L.rowspace())
            assert self.rows[f'F{i}']==Fi
        assert self.dim['zero']==0 and self.dim['Hub']==8 and self.dim['A15']==4
    @lru_cache(None)
    def sub(self,a,b):
        rows=self.rows[a]+self.rows[b]
        return (sp.Matrix(rows).rank()if rows else 0)==self.dim[b]

def replay(w,roots,G):
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    owners=set();births=set();counts=Counter();profile=Counter();dirty=0
    hist=[];events=[];cache_reads={};arrivals={};cell_coeff={};through={};handoff=None
    kernels={};first_ground={};preload=None;trace=[]
    def restored():
        assert all(at[f'X{i}']=='Hub'and values[f'X{i}']==1<<i for i in range(111)),'X restoration'
    for step,op in enumerate(w['operations']):
        if step==w['handoff']:handoff={n:[at[n],values[n]]for n in sorted(owners)}
        k,n,*args=op;counts[k]+=1;changed=None
        if k=='INIT':
            assert n not in values and n not in births
            at[n]=args[0];values[n]=0;owners.add(n);births.add(n);cell_coeff[n]=0
            if n.startswith('P')and n[1:].isdigit():restored();assert args[0]=='Hub'
        elif k=='ADD':
            dst=args[0];assert n in values and dst in values and n!=dst
            assert G.sub(at[n],at[dst])and G.sub(at[dst],at[n]),'cochart'
            if dst.startswith('P')and at[dst]=='Hub':restored();assert n.startswith('X')
            if [n,dst]==['Y59','YM59']:assert at[n]=='zero'and values[n]==1<<170
            if [n,dst]==['P6','Y59']:
                assert at[n]=='zero'and values[dst]==1<<170
                preload=values[n];trace.append(['preload',step,hex(preload)])
            if [n,dst] in [['P0','Y0'],['P1','Y59']]:
                assert at['P0']==at['P1']=='A15','simultaneous arrivals'
                trace.append(['exchange',n,step,hex(values[n]),hex(values[dst])])
            values[dst]^=values[n];changed=dst
            if at[n]==at[dst]=='A15':cell_coeff[dst]=cell_coeff.get(dst,0)^cell_coeff.get(n,0)
            if n.startswith('C')and dst.startswith('P'):cache_reads[n]=values[n]
        elif k=='MOVE':
            dst=args[0];assert n in values and G.dim[dst]!=G.dim[at[n]]
            assert G.sub(dst,at[n])if n in owners else G.sub(at[n],dst),'MOVE direction'
            profile[abs(G.dim[dst]-G.dim[at[n]])]+=1
            if at[n]=='A15'and n in ('P0','P1'):through[n]=cell_coeff[n]
            at[n]=dst;changed=n
            if dst=='A15':
                cell_coeff[n]=1 if n=='P0'else 2 if n=='P1'else 0
                if n in ('P0','P1'):kernels[n]=values[n]&MASK;arrivals[n]=step
                if n=='Y59':assert preload is not None and values[n]==preload^(1<<170)
            if dst=='zero'and n.startswith('P'):
                assert n not in first_ground;first_ground[n]=values[n]
        elif k=='CLEAR':
            assert n in owners;dirty+=bool(values[n]);owners.remove(n);values.pop(n);at.pop(n)
        else:raise AssertionError(k)
        if changed is not None and changed.startswith('P')and changed[1:].isdigit()and at[changed]!='Hub':
            hist.append(values[changed]);events.append([step,changed,at[changed],hex(values[changed])])
    if handoff is None:handoff={n:[at[n],values[n]]for n in sorted(owners)}
    assert handoff==w['expected'],'handoff'
    restored();completed={0,4,5,6,7,59}
    for i in range(111):
        assert values[f'Y{i}']==(1<<(111+i))^((1<<i)if i in completed else 0),'Y endpoint'
        assert at[f'Y{i}']==(f'F{i}'if w['closed']or i in completed else 'zero')
    assert len(births)==235 and len(owners)==(0 if w['closed']else 235)
    if w['closed']:
        assert counts==Counter(INIT=235,ADD=866,MOVE=490,CLEAR=235)
        assert dirty==234 and dict(profile)=={1:159,2:26,3:128,4:70,5:2,7:105}
    K=[(1<<i)^xor(1<<j for j in range(111)if dot(roots[i],roots[j])==0)for i in range(111)]
    h=K[0]^K[4];W=[x&(h if h>>i&1 else MASK^h)for i,x in enumerate(K)]
    assert [hex(x)for x in W]==w['W_rows_hex']
    D=list(cache_reads.values());assert len(D)==112 and rank(D)==44 and rank(D)+rank(W)-rank(D+W)==10
    B=echelon(hist);targets=W+D;witnesses=[solve(B,x)for x in targets]
    for x,c in zip(targets,witnesses):assert xor(v for j,v in enumerate(hist)if c>>j&1)==x
    assert rank(hist)==52 and rank([x>>111 for x in hist])==2
    T=[handoff[f'P{i}'][1]&MASK for i in range(8)];N=xor(1<<i for i in range(52,59));A=xor(1<<i for i in range(4,8));R=N^A;v=W[59];e=1<<59
    assert T[0]==N and T[1]==v^e and T[6]==v^R^e and T[7]==0
    assert kernels['P1']==v^R and kernels['P1']^preload==e
    assert T[0]^T[1]^T[6]==A
    assert through=={'P0':0,'P1':0}
    assert len(first_ground)==8 and all((first_ground[f'P{i}']&MASK)==T[i]for i in range(8))
    assert rank(T)==7 and rank(T+list(kernels.values()))==9
    out={'counts':dict(counts),'dirty':dirty,'profile':dict(sorted(profile.items())),'rank_length':sum(r*c for r,c in profile.items()),'D_rank':44,'D_W_intersection':10,'history_rank':52,'pure_X_history_rank':50,'terminal_rank':7,'normalized_rank':9,'completed':sorted(completed),'through_matrix':[[0,0],[0,0]],'nonlocal_preload':hex(preload),'kernel_plus_preload':hex(e),'exchange_trace':trace}
    evidence={'events':events,'target_rows_hex':[hex(x)for x in targets],'witnesses_hex':[hex(c)for c in witnesses]}
    return out,evidence,T,kernels

def star_check(cert,roots,T,K):
    E=set(cert['deleted']);assert E==set(range(4,8))|set(range(52,60));keep=MASK^xor(1<<j for j in E)
    assert rank([x&keep for x in T+list(K.values())])==6
    assert T[0]&keep==0 and len({T[1]&keep,T[6]&keep,K['P1']&keep})==1
    Fm=cert['star']['frame'];assert len(Fm)==len(set(Fm))==8 and not E.intersection(Fm)
    assert all(dot(roots[i],roots[j])!=0 for i in Fm for j in Fm)
    edges={}
    for edge in cert['star']['edges']:
        j=edge['role'];pair=tuple(edge['pair']);assert j not in E and j not in Fm
        assert pair==tuple(a for a,i in enumerate(Fm)if dot(roots[i],roots[j])==0)
        assert pair not in edges;edges[pair]=j
    for (a,i),(b,j) in ((x,y)for x in edges.items()for y in edges.items()):
        if a!=b and set(a)&set(b):assert dot(roots[i],roots[j])!=0
    deg=[sum(i in pair for pair in edges)for i in range(8)]
    assert len(edges)==25 and deg==[6,7,7,7,7,5,6,5]
    return {'retained_roles':99,'actual_punctured_rank':6,'arbitrary_seed_upper_per_width':7,'all_field_star_lower_per_width':9,'degrees':deg,'edge_count':25}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    native=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    assert sha(native)=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots=json.loads(native.read_text())['native_roots'];words={n:json.loads((a.package/'output'/f'{n}.json').read_text())for n in ['WORD','CLOSED-WORD']}
    pins={'WORD':'12c176f8621156d571441240329e5defe15c9b4322d5e0a3b2c08133334a7b71','CLOSED-WORD':'e6eea78f02d382bbd2fddd9578dcad45478a84f98ba2c6969c9101ef37b0f389'}
    G=Geometry(words['WORD']['charts'],roots);out={'status':'PASS_INDEPENDENT_NONLOCAL_RELAY','word_pins':pins,'new_complete_kappa':False}
    for n,w in words.items():
        assert sha(a.package/'output'/f'{n}.json')==pins[n]
        out[n],e,T,K=replay(w,roots,G);(a.out/f'{n}-HISTORY.json').write_text(json.dumps(e,indent=2)+'\n')
    cert=json.loads((a.package/'PUNCTURE.json').read_text());out['puncture']=star_check(cert,roots,T,K)
    patterns=[('preload',['ADD','P6','Y59']),('relay_exchange',['ADD','Y59','P1']),('relay_mask',['ADD','YM59','P1']),('axis_bank',['ADD','P6','Y4']),('old_feedback',['ADD','Y0','P0']),('axis_helper',['ADD','X0','AXIS_DUP0']),('spare_retirement',['CLEAR','P7'])]
    controls=[]
    for name,op in patterns:
        w=copy.deepcopy(words['CLOSED-WORD']);i=w['operations'].index(op);w['operations'].pop(i)
        if i<w['handoff']:w['handoff']-=1
        try:replay(w,roots,G)
        except (AssertionError,KeyError)as e:controls.append({'name':name,'rejected':True,'reason':str(e)})
        else:raise AssertionError('mutant survived '+name)
    bad=copy.deepcopy(cert);bad['star']['edges'][0]['role']=bad['star']['frame'][0]
    try:star_check(bad,roots,T,K)
    except AssertionError:controls.append({'name':'false_star_edge','rejected':True})
    else:raise AssertionError('bad star survived')
    out['independent_controls']=controls
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'closed':out['CLOSED-WORD'],'controls':len(controls)}))
if __name__=='__main__':main()
