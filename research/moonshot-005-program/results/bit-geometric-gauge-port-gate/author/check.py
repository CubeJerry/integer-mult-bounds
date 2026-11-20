#!/usr/bin/env python3
"""Exact all-width field-linear geometric source port gate certificate."""
from pathlib import Path
from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
import importlib.util,json
import numpy as np

def need(ok, message):
    if not ok: raise ValueError(message)

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True);base=args.repo/'research/moonshot-005-program/results'
    for name,digest in json.loads(Path(__file__).with_name('SOURCE-PINS.json').read_text())['files'].items():
        need(sha256((args.repo/name).read_bytes()).hexdigest()==digest,'source pin '+name)
    spec=importlib.util.spec_from_file_location('s031_geometry',base/'bit-coupled-native-geometric-h-source/review-b/construct.py')
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    ctx=helper.context(args.repo,args.out/'arithmetic');F,f=ctx.field,ctx.arith
    data=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
    nodes=data['H_nodes'];ps={int(j):{int(i):v for i,v in row.items()}for j,row in data['receiver_parameters'].items()}
    h=263;c=nodes[h];donors=sorted(ctx.H[h]);receivers=[i for i in range(111)if ctx.H[h]<=ctx.perp[i]]
    need(c==49 and donors==[0,61,62]and len(receivers)==33 and 80 not in receivers,'identity target interface')
    exits=defaultdict(list)
    for line in ctx.payload['routes'].splitlines():
        phase,role,coordinate,hid,did,*_=json.loads(line)
        if hid==h:
            need(phase=='X','actual fully early H')
            exits[did].extend((role*480+coordinate)*8+lane for lane in range(8))
    need(len(exits)==45 and {len(v)for v in exits.values()}=={16},'actual exit capacities')
    need(len({x for v in exits.values()for x in v})==720,'distinct actual owners')
    need(all(sum(len(v)for d,v in exits.items()if ctx.D[d]<=ctx.perp[i])==240 for i in receivers),'tight receiver H capacities')
    bits=lambda v:np.array([v>>p&1 for p in range(6)],dtype=np.uint8)
    U=np.array([f.U(1<<p,c)for p in range(6)],dtype=np.uint8).T
    need(F.rank(U)==6,'six-dimensional fibre core')
    need(all(np.array_equal(F.mm(U,bits(v)[:,None])[:,0],f.U(v,c))for v in range(64)),'binary-linear geometric fibres')
    local=[]
    for other in donors[1:]:
        vv=[ps[0][i]for i in receivers];ww=[ps[other][i]for i in receivers]
        piv=F.reduce(np.array([bits(v)for v in vv],dtype=np.uint8).T)[2]
        X=np.array([bits(vv[p])for p in piv],dtype=np.uint8).T;Y=np.array([bits(ww[p])for p in piv],dtype=np.uint8).T
        J=F.mm(Y,F.solve(X,np.eye(6,dtype=np.uint8)))
        need(F.rank(J)==6 and set(np.unique(J))<={0,1},'binary parameter isomorphism')
        need(all(np.array_equal(F.mm(J,bits(v)[:,None])[:,0],bits(w))for v,w in zip(vv,ww)),'all native parameter pairs')
        graph={v:{w for w in vv if v!=w and v^w in vv}for v in vv};seen={vv[0]};todo=list(seen)
        while todo:
            new=graph[todo.pop()]-seen;seen.update(new);todo.extend(new)
        need(len(seen)==len(vv)and f.binary_rank(vv)==6,'connected additive parameter graph')
        local.append({'donor':other,'J':J.tolist(),'pairs':list(zip(receivers,vv,ww)),'graph_edges':sum(map(len,graph.values()))//2})
    eye=np.eye(16,dtype=np.uint8);shift=np.zeros((16,16),dtype=np.uint8)
    for p in range(16):shift[(p+1)%16,p]=1
    pencils=[]
    for node in sorted(set(nodes)):
        core=np.array([f.U(1<<p,node)for p in range(6)],dtype=np.uint8).T;N=shift^F.product[node,eye]
        exceptional=int(F.inverse[1^node]);minor=F.mm(eye^F.product[exceptional,N],core)
        need(F.rank(core)==F.rank(minor)==6,'exceptional scalar pencil injective')
        e=np.array([[f.power(node,p)for p in range(16)]],dtype=np.uint8);a=f.power(node,16)^1
        dr=np.array([[f.power(1<<p,8)^f.MUL[f.power(node,4)][f.power(1<<p,4)]for p in range(6)]],dtype=np.uint8)
        need(np.array_equal(F.mm(e,core),dr),'central derivative readout')
        need(not np.any(F.mm(e,F.mm(N,core))^F.product[a,core[15:16]]),'linear feedback coefficient cancels')
        need(not np.any(F.mm(N,core)[15]),'quadratic feedback coefficient cancels')
        pencils.append([node,exceptional,6])
    derivative=lambda v:f.power(v,8)^f.MUL[f.power(c,4)][f.power(v,4)]
    reads={i:[derivative(ps[j][i])for j in donors]for i in receivers}
    need(all(all(r)for r in reads.values()),'every native H readout invertible')
    ratios={i:f.MUL[r[0]][f.INV[r[1]]]for i,r in reads.items()}
    need(108 in exits and all(ctx.D[108]<=ctx.perp[i]for i in (5,7)),'shared actual D108')
    need([ratios[5],ratios[7]]==[26,49],'incompatible exact ratios')
    A=np.array([[0,1,0],[0,0,1],[1,0,0]],dtype=np.uint8);N=shift^F.product[c,eye]
    core=np.kron(U,np.eye(3,dtype=np.uint8))^np.kron(F.mm(N,U),A)
    e=np.array([[f.power(c,p)for p in range(16)]],dtype=np.uint8);sel=np.zeros((1,16),dtype=np.uint8);sel[0,15]=f.power(c,16)^1
    Q=np.kron(e,np.eye(3,dtype=np.uint8))^np.kron(sel,A)
    need(F.rank(core)==18,'non-diagonal matrix feedback core')
    for i in receivers:
        K=F.mm(core,np.kron(bits(ps[0][i])[:,None],np.eye(3,dtype=np.uint8)))
        need(np.array_equal(F.mm(Q,K),F.product[reads[i][0],np.eye(3,dtype=np.uint8)]),'matrix-valued source readout')
    rows=lambda i:np.hstack([F.product[f.INV[reads[i][0]],np.eye(3,dtype=np.uint8)],F.product[f.INV[reads[i][1]],A]])
    need(F.rank(np.vstack([rows(5),rows(7)]))==6,'zero common two-donor row space')
    need(ratios[4]==ratios[7]and F.rank(np.vstack([rows(4),rows(7)]))==3,'equal-ratio positive control')
    need(F.rank(np.vstack([rows(5),rows(5)]))==3,'same-receiver positive control')
    controls={'wrong_shared_receiver':not(ctx.D[108]<=ctx.perp[0]),'wrong_parameter_identity':ps[0][5]!=ps[61][5],'wrong_readout_scalar':not np.array_equal(F.mm(Q,K),F.product[reads[i][0]^1,np.eye(3,dtype=np.uint8)])}
    need(all(controls.values()),'mutation controls reject')
    witness={'H':h,'node':c,'donors':donors,'receivers':receivers,'transport':local,'pencils':pencils,'readouts':reads,'D':108,'receiver_pair':[5,7],'ratios':[26,49]}
    raw=(json.dumps(witness,sort_keys=True,separators=(',',':'))+'\n').encode();(args.out/'WITNESS.json').write_bytes(raw)
    result={'status':'PASS_GEOMETRIC_FIELD_LINEAR_GAUGE_PORT_GATE','H':h,'receivers':33,'exit':108,'witness_receivers':[5,7],'ratios':[26,49],'exceptional_pencils':28,'all_feedback_widths':True,'arbitrary_field_linear_gauges':True,'arbitrary_binary_linear_gauges':False,'nonlinear_downstream':True,'controls':controls,'witness_sha256':sha256(raw).hexdigest(),'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
