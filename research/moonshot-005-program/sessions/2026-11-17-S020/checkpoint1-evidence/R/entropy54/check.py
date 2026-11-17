"""Exact entropy dual; standard-library rational arithmetic, no LP solver."""
import argparse, copy, hashlib, json
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
NATIVE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
NATIVE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PARENT='research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint5-evidence/R/initial-chart-cut/control/NATIVE-CACHED57-WORD.json'
PARENT_SHA='7df1fc8f696545185c417c6df4161b324869bf084b503138506425510e841fa2'
def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def row(label,adj,n):
    kind,*args=label
    if kind=='empty':
        need(not args,'empty arity');return {0:Q(1)},Q(0),'equality'
    need(kind in ['mono','unit','decode','submod'],'known Shannon row')
    s,i,*tail=args
    need(isinstance(s,int) and 0<=s<1<<n and isinstance(i,int) and 0<=i<n and not(s>>i&1),'valid entropy set/index')
    si=s|(1<<i)
    if kind=='submod':
        need(len(tail)==1,'submod arity');j=tail[0]
        need(isinstance(j,int) and 0<=j<n and i!=j and not(s>>j&1),'distinct missing submod index')
        return {s:Q(1),si:Q(-1),s|(1<<j):Q(-1),si|(1<<j):Q(1)},Q(0),'inequality'
    need(not tail,'row arity')
    if kind=='mono':return {s:Q(1),si:Q(-1)},Q(0),'inequality'
    if kind=='decode':
        need(s&adj[i]==0,'decoder knows all actual side information')
        return {s:Q(-1),si:Q(1)},Q(1),'equality'
    return {s:Q(-1),si:Q(1)},Q(1),'inequality'
def verify(cert,roots,unknown):
    roles=cert['roles'];isolates=cert['isolates'];n=len(roles)
    need(n==11 and len(isolates)==3 and len(set(roles+isolates))==14,'exact14 distinct roles')
    need(set(roles+isolates)<=unknown,'witness roles unfinished')
    dot=lambda i,j:sum(a*b for a,b in zip(roots[i],roots[j]))
    adj=[sum(1<<j for j,q in enumerate(roles) if i!=j and dot(p,q)==0) for i,p in enumerate(roles)]
    need(adj==cert['adjacency_masks'],'geometry-derived graph')
    for x in isolates:need(all(dot(x,y)!=0 for y in roles+isolates if x!=y),'isolates have no side information in14-role graph')
    total=defaultdict(Q);rhs=Q(0);types=defaultdict(int)
    for term in cert['terms']:
        coeff=Q(term['weight']);vector,b,typ=row(term['row'],adj,n)
        need(typ==term['kind'],'row classification')
        if typ=='inequality':need(coeff<=0,'nonpositive inequality multiplier')
        for index,value in vector.items():total[index]+=coeff*value
        rhs+=coeff*b;types[term['row'][0]]+=1
    total={k:v for k,v in total.items() if v}
    need(total=={(1<<n)-1:Q(1)},'exact dual residual')
    need(rhs==Q(cert['core_bound'])==Q(11,2),'exact core entropy lower bound')
    need(rhs+len(isolates)==Q(cert['full_bound'])==Q(17,2),'three decoded isolates add3')
    return {'terms':len(cert['terms']),'row_types':dict(types),'core_bound':str(rhs),'witness_bound':str(rhs+len(isolates)),'remaining_entropy_coefficients':{str(k):str(v) for k,v in total.items()}}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--certificate',type=Path,default=Path(__file__).with_name('CERTIFICATE.json'))
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    src=a.repo/NATIVE;parent=a.repo/PARENT
    need(sha(src)==NATIVE_SHA and sha(parent)==PARENT_SHA,'exact source and known-set pins')
    roots=json.loads(src.read_text())['native_roots'];known=set(json.loads(parent.read_text())['targets']);unknown=set(range(111))-known
    need(len(known)==57 and len(unknown)==54,'source partition')
    cert=json.loads(a.certificate.read_text());result=verify(cert,roots,unknown);controls=[];candidates=[]
    bad=copy.deepcopy(cert);j=next(i for i,t in enumerate(bad['terms']) if t['kind']=='inequality');bad['terms'][j]['weight']=str(-Q(bad['terms'][j]['weight']));candidates.append(('wrong inequality sign',bad))
    bad=copy.deepcopy(cert);bad['terms'].pop();candidates.append(('missing dual term',bad))
    bad=copy.deepcopy(cert);bad['core_bound']='6';candidates.append(('unproved larger bound',bad))
    bad=copy.deepcopy(cert);bad['adjacency_masks'][0]^=2;candidates.append(('mutated source graph',bad))
    bad=copy.deepcopy(cert);bad['isolates'][0]=4;candidates.append(('wrong isolated source role',bad))
    for label,bad in candidates:
        try:verify(bad,roots,unknown)
        except ValueError as ex:controls.append({'mutation':label,'rejected':str(ex)})
        else:raise ValueError('bad certificate accepted: '+label)
    result.update(status='PASS_EXACT_NONLINEAR_BROADCAST_17_OVER_2',certificate_sha256=sha(a.certificate),native_sha256=sha(src),known_set_sha256=sha(parent),known=sorted(known),unknown=sorted(unknown),negative_controls=controls,scope='Every deterministic zero-error finite-alphabet static code with independent uniform whole-record messages has broadcast entropy at least17/2 record units. Integral whole-record transcripts need9 messages. Physical applications require separately audited source simulation premises.')
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'],result['witness_bound'],'with',result['terms'],'exact dual terms')
if __name__=='__main__':main()
