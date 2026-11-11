"""Independent full-history replay and simultaneous nine-vector adjoint audit.
Uses author certificate only as data, never imports another verifier.
"""
import argparse, collections, gzip, hashlib, json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CUTPIN='57c3eaec1aa281cd2458e9a1071e3e349046b3dca7c992c754d08ad93931c235'
def need(value,message):
    if not value: raise ValueError(message)
def axpy(dst,src,c):
    for j,v in list(src.items()):
        z=dst.get(j,Q(0))+c*v
        if z: dst[j]=z
        else: dst.pop(j,None)
def mul(row,c): return {j:c*v for j,v in row.items() if c*v}
def insert(basis,row):
    r=row.copy()
    while r:
        p=min(r)
        if p not in basis:
            basis[p]=mul(r,1/r[p]); return True
        axpy(r,basis[p],-r[p])
    return False
def space(frame):
    out={0}
    for x in frame: out.update(x^y for y in tuple(out))
    return frozenset(out)
def main(a):
    raw=(a.repository/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin')
    cutraw=(a.cut/'CERTIFICATE.json').read_bytes()
    need(hashlib.sha256(cutraw).hexdigest()==CUTPIN,'reviewed predecessor pin')
    cert_raw=(a.package/'CERTIFICATE.json').read_bytes(); cert=json.loads(cert_raw)
    need(cert['source_sha256']==PIN and cert['cut_certificate_sha256']==CUTPIN,'certificate dependencies')
    w=json.loads(gzip.decompress(raw)); P=w['program']; C=list(map(space,w['frames']))
    stations={C[i] for i in cert['stations']}
    need(stations=={C[i] for i in json.loads(cutraw)['canonical_cut_representatives']},'exact inherited station cut')
    need(len(stations)==220 and (cert['donor'],cert['receiver'])==(77,189),'station and pair census')
    path={C[w['initial'][189]]}|{C[e[3]] for e in P if e[:2]==['MOVE',189]}
    need(not stations&path,'disjoint controller and observer charts')
    states={j:{j:Q(1)} for j in range(w['public'])}; loc=dict(enumerate(w['initial']))
    obs={}; basis={}
    def record(t,j):
        if C[loc[j]] in path:
            obs[t,j]=(loc[j],states[j].copy()); insert(basis,states[j])
    for j in states: record(-1,j)
    for t,e in enumerate(P):
        op,j=e[:2]
        if op=='INIT': need(j not in loc,'fresh owned lifetime'); loc[j]=e[2]; states[j]={}
        elif op=='CLEAR': loc.pop(j); states.pop(j)
        elif op=='MOVE': need(C[loc[j]]==C[e[2]],'source chart'); loc[j]=e[3]; record(t,j)
        elif op in ('ADD','COPY'):
            need(C[loc[j]]==C[loc[e[2]]],'cochart source')
            if op=='COPY': need(not states[j],'source COPY target zero'); states[j]={}
            axpy(states[j],states[e[2]],Q(e[3]))
        elif op=='SCALE': states[j]=mul(states[j],Q(e[2]))
        else: raise ValueError('unknown native instruction')
    need(len(obs)==1065 and len(basis)==1056,'fresh complete-history rank')
    need(states[189].get(77)==1,'actual required endpoint coefficient')
    need(loc==dict(enumerate(w['final'])),'complete native lifetime endpoint')
    weights=collections.defaultdict(list); relation_basis={}; baseline_rows=[]
    for k,rel in enumerate(cert['relations']):
        baseline={}; index={}
        for x in rel:
            key=x['after_event'],x['role']; c=Q(x['coefficient'])
            need(key in obs and obs[key][0]==x['chart'],'registered actual field version')
            axpy(baseline,obs[key][1],c); index[key]=index.get(key,Q(0))+c
            weights[key[0]].append((key[1],k,c))
        need(not baseline,'author relation is not an identity')
        need(insert(relation_basis,index),'independent author relation')
        baseline_rows.append(baseline)
    need(len(relation_basis)==9==len(obs)-len(basis),'full left nullspace')
    # A separate simultaneous adjoint computation. At every cut inspect ALL
    # nonzero adjoint roles, not merely a change list or selected control columns.
    adj={}; loc=dict(enumerate(w['final'])); station_roles={j for j,c in loc.items() if C[c] in stations}
    checked=0; max_support=0; expanded_witness=None
    def inspect(t,phase):
        nonlocal checked,max_support,expanded_witness
        need(not station_roles.intersection(adj),'nonzero station adjoint at cut '+str((t,phase)))
        checked+=1; max_support=max(max_support,len(adj))
        if expanded_witness is None:
            for j,row in adj.items():
                if j in loc and C[loc[j]]==C[3]:
                    expanded_witness={'cut':t,'phase':phase,'role':j,'relation':min(row),'coefficient':str(row[min(row)]),'chart':loc[j]};break
    inspect(len(P),'final')
    for t in range(len(P)-1,-1,-1):
        for j,k,c in weights[t]:
            row=adj.setdefault(j,{}); axpy(row,{k:Q(1)},c)
            if not row: adj.pop(j,None)
        inspect(t+1,'after_observation_impulses')
        e=P[t]; op,j=e[:2]
        if op in ('ADD','COPY'):
            s=e[2]; row=adj.setdefault(s,{}); axpy(row,adj.get(j,{}),Q(e[3]))
            if not row: adj.pop(s,None)
            if op=='COPY': adj.pop(j,None)
        elif op=='SCALE':
            row=mul(adj.get(j,{}),Q(e[2])); adj.pop(j,None)
            if row: adj[j]=row
        elif op=='MOVE':
            loc[j]=e[2]; station_roles.discard(j)
            if C[e[2]] in stations: station_roles.add(j)
        elif op=='CLEAR':
            loc[j]=e[2]; adj.pop(j,None)
            if C[e[2]] in stations: station_roles.add(j)
        elif op=='INIT': loc.pop(j); adj.pop(j,None); station_roles.discard(j)
        inspect(t,'before_instruction')
    for j,k,c in weights[-1]:
        row=adj.setdefault(j,{}); axpy(row,{k:Q(1)},c)
        if not row: adj.pop(j,None)
    inspect(0,'after_initial_observation_impulses')
    need(not adj,'backwards identities on every input')
    need(expanded_witness is not None,'chart3 expansion control must break annihilation')
    # Mutating one coefficient by +1 adds this actual nonzero baseline row.
    first=cert['relations'][0][0]; mutant=obs[first['after_event'],first['role']][1]
    need(bool(mutant),'coefficient mutation control must fail baseline')
    out={'status':'PASS_INDEPENDENT_220_CHART_HISTORY_REVIEW','source_sha256':PIN,'certificate_sha256':hashlib.sha256(cert_raw).hexdigest(),'predecessor_sha256':CUTPIN,'station_charts':220,'observations':len(obs),'rank':len(basis),'relations':len(relation_basis),'relation_term_counts':[len(r) for r in cert['relations']],'simultaneous_adjoint_cut_checks':checked,'maximum_nonzero_adjoint_roles':max_support,'every_control_cut_at_every_station_zero':True,'negative_controls':{'coefficient_mutation_baseline_nonzero':True,'extra_chart3_control_nonzero_adjoint':expanded_witness},'scope':'All jointly chosen q77-only linear additive controls at the 220 fixed station charts; original common baseline and native processing fixed. Complete receiver189 native histories granted. Excludes neither common-dependent encoders nor generalized recoverable encoder R. No new kappa.'}
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--repository',type=Path,required=True); p.add_argument('--package',type=Path,required=True); p.add_argument('--cut',type=Path,required=True); p.add_argument('--output',type=Path,required=True); main(p.parse_args())
