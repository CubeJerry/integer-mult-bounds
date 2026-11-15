#!/usr/bin/env python3
"""Actual paired flag source: two shared tails, charged axis duplicates."""
import argparse,json,hashlib,copy
from pathlib import Path
ROOT='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
ROOT_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
def basis(rows):
 B={}
 for r in rows:
  x=r
  while x:
   p=x.bit_length()-1
   if p in B:x^=B[p]
   else:B[p]=x;break
 return B
def rank(rows):return len(basis(rows))
def independent(rows):
 b=[]
 for x in rows:
  if rank(b+[x])>len(b):b.append(x)
 return b
def xor(rows):
 s=0
 for r in rows:s^=r
 return s

def chains(flags,pat):
 qs=[q for q in range(8) if pat>>q&1];sets={};depths={}
 for q in qs:
  s=0
  for x in flags[q]:
   if not pat>>x&1:break
   s|=1<<x
  assert s;sets[q]=s;depths[q]=s.bit_count()
 best=None
 def rec(k,C):
  nonlocal best
  if best is not None and len(C)>=len(best):return
  if k==len(qs):best=[c[:] for c in C];return
  q=qs[k]
  for c in C:
   if all((sets[q]&sets[p]) in (sets[q],sets[p]) for p in c):c.append(q);rec(k+1,C);c.pop()
  C.append([q]);rec(k+1,C);C.pop()
 rec(0,[])
 return sorted([sorted(c,key=lambda q:(-sets[q].bit_count(),q)) for c in best],key=lambda c:(-len(c),c)),sets,depths

def build(roots):
 flags=[[(q+l)%8 for l in range(8)] for q in range(8)]
 for q in [1,3]:p=q-1;flags[q]=[q,p]+[(p+l)%8 for l in range(2,8)]
 def ch(s):
  if not s:return 'Hub'
  if s==255:return 'zero'
  if s.bit_count()==1:return f'F{s.bit_length()-1}'
  if s.bit_count()==7:return f'L{(255^s).bit_length()-1}'
  return f'A{s}'
 charts={'Hub':{'kind':'ann','rows':[]},'zero':{'kind':'span','rows':[]}}
 for i,r in enumerate(roots):charts[f'L{i}']={'kind':'span','rows':[r]};charts[f'F{i}']={'kind':'ann','rows':[r]}
 for s in range(1,255):
  if ch(s) not in charts:charts[ch(s)]={'kind':'ann','rows':[roots[q] for q in range(8) if s>>q&1]}
 K=[sum(1<<j for j,r in enumerate(roots) if j==i or sum(a*b for a,b in zip(roots[i],r))==0) for i in range(111)]
 one=(1<<111)-1;hm=K[0]^K[4];h=[(hm>>i)&1 for i in range(111)];W=[x&(hm if h[i] else one^hm) for i,x in enumerate(K)]
 W0=independent([x&(one^hm) for x in W]);assert len(W0)==7
 # The two unrepaired rank-three/two-run local duals meet in span(88).
 coeff=independent([v for v in range(1,128) if (v&88).bit_count()%2==0]);U0=[xor(W0[j] for j in range(7) if v>>j&1) for v in coeff];assert len(U0)==6
 groups={}
 for i,r in enumerate(roots):groups.setdefault(sum(1<<q for q in range(8) if r[q]==0),[]).append(i)
 cohorts=[];cache={};cachecharts={}
 for pat,S in sorted(groups.items()):
  assert pat and len({h[i] for i in S})==1
  runs,sets,depths=chains(flags,pat);r=len(runs);sm=sum(1<<i for i in S);oldruns,_,_=chains([[(q+l)%8 for l in range(8)] for q in range(8)],pat)
  oldrows=[sm]+[sm^(1<<i) for i in S[1:len(oldruns)]]
  targets=[u&sm for u in U0] if h[S[0]]==0 else oldrows
  rows=independent(targets+oldrows+[1<<i for i in S])[:min(r,len(S))]
  assert len(rows)==min(r,len(S)) and rank([u&sm for u in U0])<=r if h[S[0]]==0 else len(rows)==min(r,len(S))
  pivots=[];p=0
  for col in S:
   hit=next((j for j in range(p,len(rows)) if rows[j]>>col&1),None)
   if hit is None:continue
   rows[p],rows[hit]=rows[hit],rows[p]
   for j in range(len(rows)):
    if j!=p and rows[j]>>col&1:rows[j]^=rows[p]
   pivots.append(col);p+=1
  assert len(pivots)==len(rows)
  helper=None
  if r>len(S):
   assert len(S)==1 and r==2 and S[0] in [0,2]
   rows.append(1<<S[0]);helper=f'AXIS_DUP{S[0]}'
  run_roles=[f'X{i}' for i in pivots]+([helper] if helper else [])
  restore=[(j,i) for i,row in zip(pivots,rows) for j in S if j!=i and row>>j&1]
  assert all(j not in pivots for j,i in restore)
  g={'pattern':pat,'sources':S,'h_class':h[S[0]],'runs':runs,'query_sets':sets,'query_depths':depths,'run_roles':run_roles,'run_rows_hex':[hex(x) for x in rows],'restore_adds':restore,'helper':helper,'old_run_count':len(oldruns)};cohorts.append(g)
  for run,row in zip(runs,rows):
   for q in run:
    n=f'C{q}_{depths[q]}_{h[S[0]]}_g{S[0]}';cache[n]=cache.get(n,0)^row;cachecharts[n]=ch(sets[q])
 cache={n:v for n,v in cache.items() if v};D=list(cache.values());selected=[];BB=D[:]
 for i,row in enumerate(W):
  if rank(BB+[row])>rank(BB):BB.append(row);selected.append(i)
 assert rank(D)==44 and rank(D)+15-rank(D+W)==10 and len(selected)==5
 ops=[];expected={}
 for i in range(111):ops.extend([['INIT',f'R{i}',f'L{i}'],['ADD',f'X{i}',f'R{i}']]);expected[f'R{i}']=[f'L{i}',1<<i]
 for n in sorted(cache):ops.append(['INIT',n,cachecharts[n]]);expected[n]=[cachecharts[n],cache[n]]
 for g in cohorts:
  S=g['sources'];start=ch(g['pattern']);rr=g['run_roles'];restore=g['restore_adds']
  for i in S:
   if start!=f'L{i}':ops.append(['MOVE',f'X{i}',start])
  for j,i in restore:ops.append(['ADD',f'X{j}',f'X{i}'])
  for i in S:
   if f'X{i}' not in rr:ops.append(['MOVE',f'X{i}','Hub'])
  for n,run,row in zip(rr,g['runs'],map(lambda s:int(s,16),g['run_rows_hex'])):
   if n.startswith('AXIS_DUP'):
    i=S[0];assert len(run)==1
    ops.extend([['INIT',n,'Hub'],['ADD',f'X{i}',n],['MOVE',n,ch(g['query_sets'][run[0]])]])
    current=ch(g['query_sets'][run[0]]);expected[n]=[current,row]
   else:current=start
   for q in run:
    dest=ch(g['query_sets'][q])
    if current!=dest:ops.append(['MOVE',n,dest]);current=dest
    ops.append(['ADD',n,f'C{q}_{g["query_depths"][q]}_{g["h_class"]}_g{S[0]}'])
   if n.startswith('X'):ops.append(['MOVE',n,'Hub'])
  for j,i in restore:ops.append(['ADD',f'X{j}',f'X{i}'])
 raw0=[xor(v for n,v in cache.items() if n.startswith('C0_') and n.split('_')[2]==str(a)) for a in [0,1]]
 pre=xor(v for n,v in cache.items() if n.startswith('C0_') and int(n.split('_')[1])<4)
 suffix=xor(v for n,v in cache.items() if n.startswith('C0_') and n.split('_')[2]=='1' and int(n.split('_')[1])>=4)
 targets=[suffix]+[W[i] for i in selected]+[0,0];modes=[xor(v for n,v in cache.items() if n.startswith(f'C{q}_')) for q in range(8)]
 seeds=[1^raw0[0]^pre]+[targets[q]^modes[q] for q in range(1,8)]
 ops.extend([['INIT','YM0','zero'],['ADD','Y0','YM0']]);expected['YM0']=['zero',1<<111];yc='zero'
 for d in range(7,3,-1):
  for n in sorted(cache):
   if not (n.startswith(f'C0_{d}_0_')):continue
   dest=cachecharts[n]
   if yc!=dest:ops.append(['MOVE','Y0',dest]);yc=dest
   ops.append(['ADD',n,'Y0'])
 if yc!='A15':ops.append(['MOVE','Y0','A15'])
 packet_start=len(ops);packet_sections={}
 for q in range(8):
  section_start=len(ops)
  n=f'P{q}';ops.append(['INIT',n,'Hub']);ops.extend([['ADD',f'X{i}',n] for i in range(111) if seeds[q]>>i&1]);pat=0
  for d,x in enumerate(flags[q],1):
   pat|=1<<x;ops.append(['MOVE',n,ch(pat)])
   if q==0 and d==4:
    ops.extend([['ADD','P0','Y0'],['ADD','Y0','P0']]);yc='A15'
    for dep in range(3,0,-1):
     for ca in sorted(cache):
      if not ca.startswith(f'C0_{dep}_0_'):continue
      dest=cachecharts[ca]
      if yc!=dest:ops.append(['MOVE','Y0',dest]);yc=dest
      ops.append(['ADD',ca,'Y0'])
    if yc!='F0':ops.append(['MOVE','Y0','F0'])
   for ca in sorted(cache):
    if ca.startswith(f'C{q}_{d}_'):ops.append(['ADD',ca,n])
   if q==0 and d==8:ops.append(['ADD','YM0','P0'])
  expected[n]=['zero',targets[q]]
  packet_sections[q]=ops[section_start:]
 # Fixed sequential lockstep: every move and ADD is retained, and both
 # paired records are simultaneously present at each shared positive chart.
 scheduled=[];steps={}
 for q in range(8):
  seq=packet_sections[q];cuts=[i for i,o in enumerate(seq) if o[0]=='MOVE' and o[1]==f'P{q}'];assert len(cuts)==8
  scheduled.extend(seq[:cuts[0]]);steps[q]=[seq[cuts[d]:cuts[d+1] if d<7 else len(seq)] for d in range(8)]
 for pair in [(0,1),(2,3)]:
  for d in range(8):
   for q in pair:scheduled.append(steps[q][d][0])
   for q in pair:scheduled.extend(steps[q][d][1:])
 for q in range(4,8):
  for step in steps[q]:scheduled.extend(step)
 ops=ops[:packet_start]+scheduled
 w={'schema':'paired-flag-h9-source-v1','charts':charts,'operations':ops,'expected':expected,'handoff':len(ops),'closed':False,'flags':flags,'cohorts':cohorts,'seeds':seeds,'completed_targets':[0],'terminal_W_roles':[None]+selected+[None,None],'W_rows_hex':[hex(x) for x in W],'W_pivot_h_hex':hex(hm),'kernel_x_hex':hex(1^raw0[0]),'increment_space_dimension':44,'increment_W_intersection':10,'reprogramming':{'h0_W_basis_hex':[hex(x) for x in W0],'annihilator_vector':88,'h0_target_coefficients':coeff,'h0_target_rows_hex':[hex(x) for x in U0]},'new_complete_kappa':False,'source_geometry_sha256':ROOT_SHA}
 closed=copy.deepcopy(w);closed['closed']=True;closed['operations'] += [['CLEAR',n] for n in sorted(expected)]+[['MOVE',f'Y{i}',f'F{i}'] for i in range(1,111)]
 return w,closed

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args();raw=(a.repo/ROOT).read_bytes();assert hashlib.sha256(raw).hexdigest()==ROOT_SHA;roots=json.loads(raw)['native_roots'];a.out.mkdir(parents=True,exist_ok=True)
 for n,w in zip(['WORD','CLOSED-WORD'],build(roots)):(a.out/f'{n}.json').write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
 print('BUILT_PAIRED_FLAG_SOURCE')
if __name__=='__main__':main()
