#!/usr/bin/env python3
"""Source binding and exact controls for common-grid/leaf admission audit."""
from fractions import Fraction as Q
from pathlib import Path
from hashlib import sha1,sha256
import argparse,gzip,importlib.util,json,sys,time
HERE=Path(__file__).resolve().parent
PIN='e54523517d0f03e58352e647c403a5af3e525a57'
def need(ok,label):
    if not ok:raise ValueError(label)
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def plus(a,b):return (a[0]+b[0],a[1]+b[1])
def iphase(a,k):return mul(a,[(1,0),(0,1),(-1,0),(0,-1)][k%4])
def deposit(v,x,a):
    b=plus(v.get(x,(Q(0),Q(0))),a)
    if b!=(0,0):v[x]=b
    else:v.pop(x,None)
def axis(v,j):
    out={}
    for x,a in v.items():
        deposit(out,x,mul(a,(Q(1,2),Q(1,2))))
        deposit(out,x^(1<<j),mul(a,(Q(1,2),-Q(1,2))))
    return out
def column(x,j,f):return sum(((x>>(i*f+j))&1)<<i for i in range(9))
def replace(x,j,f,y):
    for i in range(9):
        bit=i*f+j;x=(x&~(1<<bit))|(((y>>i)&1)<<bit)
    return x
def monomial(v,record,f,c,inverse=False):
    out={};G=tuple(record['matrix_rows']);Gi=c.inv(G,9)
    for address,a in v.items():
        result=address;phase=0
        for j in range(f):
            y=column(address,j,f)
            x=c.mv(Gi,y^record['offset']) if inverse else y
            phase+=record['phase']+c.qvalue(tuple(record['quadratic_rows']),tuple(record['linear_Z4']),x,9)
            result=replace(result,j,f,x if inverse else c.mv(G,x)^record['offset'])
        deposit(out,result,iphase(a,-phase if inverse else phase))
    return out
def integral(v):return all(Q(a).denominator==1 for z in v.values() for a in z)
def main(output):
    start=time.monotonic();pins=json.loads((HERE/'CANONICAL-SOURCES.json').read_bytes())
    need(pins['base']==PIN,'canonical source pin')
    for s in pins['sources']:need(sha256((HERE/s['local_path']).read_bytes()).hexdigest()==s['sha256'],'canonical export hash')
    p=HERE/'canonical/research/shared-wire-split-composition'
    w=json.loads(gzip.decompress((p/'data/final.json.gz').read_bytes()))
    need(w['program'][24472]==['MOVE',415,3,99,False],'actual selected MOVE')
    spec=importlib.util.spec_from_file_location('audit_clifford',p/'frozen/clifford_exact.py');c=importlib.util.module_from_spec(spec);sys.modules[spec.name]=c;spec.loader.exec_module(c)
    record,compiled=c.lower_child(c.canonical_frame(9,tuple(w['frames'][3])).adjoint().then(c.canonical_frame(9,tuple(w['frames'][99]))))
    need(record['rank']==1 and record['right']['phase']==1 and record['left']['phase']==0,'source rank and absolute phases')
    seed={0:(Q(1),Q(0)),3:(Q(1),Q(0))};f=2
    entrance=monomial(seed,record['right'],f,c,True)
    need(monomial(entrance,record['right'],f,c)==seed,'actual right inverse/source order')
    first=axis(seed,0);last=axis(first,1);final=monomial(last,record['left'],f,c)
    need(integral(entrance) and integral(final) and not integral(first),'actual whole-MOVE endpoint-only control')
    need(last=={1:(Q(1),Q(0)),2:(Q(1),Q(0))},'independent C tensor endpoint')
    scaled={x:(a*(1<<18),b*(1<<18)) for x,(a,b) in entrance.items()}
    stage=monomial(scaled,record['right'],f,c)
    for j in range(f):stage=axis(stage,j);need(integral(stage),'common-root reserve admits every prefix')
    stage=monomial(stage,record['left'],f,c);need(integral(stage),'complete guarded source endpoint')
    need(max(abs(q) for z in stage.values() for q in z)<1<<(40-1),'selected width signed headroom')
    # Finite corroboration of the closed-form inequalities; the proof uses
    # 178t < D/2, not extrapolation of this bounded scan.
    tested=0
    for D in range(1,5001):
        t=(D-1)//356
        need((D+1)//2+178*t<=D,'fractional width consequence')
        need((D+2)//2+161*t+1<=D+2,'magnitude width consequence');tested+=1
    bridge=[]
    for f,K,rho in [(1,2,0),(2,2,1),(3,3,1)]:
        u=2;z=u+9*f*K;a=z+1;selected=[u+(i*f+j)*K+rho for i in range(9) for j in range(f)]
        suffix=[k for k in range(u,a) if k not in selected];permutation=list(range(u))+selected+suffix
        need(sorted(permutation)==list(range(a)) and len(set(selected))==9*f,'complete spectator-preserving packing bijection')
        h=7;r=2;rows=3;P=rows*(1<<u);S=1<<(a-u-9*f)
        old=rows*(1<<a)*6*r*(h+1);packed=2*P*(1<<(9*f))*S*r*h
        need(Q(old,packed)==Q(3*(h+1),h),'complete physical payload ratio')
        need(old>packed,'header-only bridge rejected by exact cardinality')
        bridge.append(dict(f=f,K=K,rho=rho,address_bits=a,selected_positions=selected,old_bits=old,packed_bits=packed,ratio=str(Q(old,packed))))
    for s in json.loads((HERE/'REMOTE-SOURCES.json').read_bytes())['sources']:
        data=(HERE/s['local_path']).read_bytes();need(sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==s['git_blob'] and sha256(data).hexdigest()==s['sha256'],'exact remote Git bytes')
    encode=lambda v:{str(x):list(map(str,z)) for x,z in sorted(v.items())}
    out=dict(status='PASS_SELECTED_GRID_TO_LITERAL_LEAF_INTERFACE',base=PIN,selected_word_sha256=sha256((p/'data/final.json.gz').read_bytes()).hexdigest(),actual_event=24472,actual_move=w['program'][24472],recipe=record,recipe_sha256=sha256(json.dumps(record,sort_keys=True,separators=(',',':')).encode()).hexdigest(),endpoint_only_control=dict(complete_native_entrance=encode(entrance),central_first_prefix=encode(first),complete_native_final=encode(final),entrance_integral=integral(entrance),final_integral=integral(final),prefix_integral=integral(first),interpretation='Rejects endpoint-only admission to this literal provider, not the selected guarded root pipeline.'),common_root_scaled_control=dict(root_axes=18,p=0,h=1,F=18,W=40,scale=1<<18,all_prefixes_integral=True),depth_inequality_cases=tested,packing_cases=bridge,scope='Source-bound numerical admission implication conditional on the existing complete-root Clifford/depth premise and a faithful paid packed ABI. No physical packing, whole MOVE, nonleaf tariff, all-column foundation discharge or new kappa.',elapsed_seconds=time.monotonic()-start)
    output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ['status','actual_move','recipe_sha256','depth_inequality_cases','elapsed_seconds']},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'RESULT.json');main(ap.parse_args().output)
