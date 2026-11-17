#!/usr/bin/env python3
"""Stream the globally routed GF64 control as real binary whole-record operations."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from functools import lru_cache
from hashlib import sha256
import gzip,json,struct
from pathlib import Path
import numpy as np

PINS={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'}
ROOTS=111;STRIPES=15;DIM=16;BITS=6;WIDTH=DIM*BITS;ONEBANK=ROOTS*STRIPES*WIDTH;CANON=[0,1,2,4,8,9,14,30,59]


def need(ok,reason):
    if not ok:raise ValueError(reason)


def setbits(a):
    while a:
        bit=a&-a;yield bit.bit_length()-1;a-=bit


def gf(a,b):
    v=0
    while b:
        if b&1:v^=a
        a<<=1
        if a&64:a^=67
        b>>=1
    return v


def powers(a):
    v=1;out=[]
    for _ in range(DIM):out.append(v);v=gf(v,a)
    return tuple(out)


def binary_rows(matrix):
    out=[]
    for gr in matrix:
        for bit in range(BITS):
            out.append(sum(1<<(BITS*j+k) for j,coef in enumerate(gr) for k in range(BITS) if gf(coef,1<<k)>>bit&1))
    return tuple(out)


EVAL=tuple(binary_rows([powers(a)]) for a in range(28))


@lru_cache(None)
def eliminator(nodes,transpose):
    coeff=[powers(a) for a in nodes];rows=list(binary_rows(list(zip(*coeff)) if transpose else coeff))
    v=rows.copy();ops=[]
    def add(i,j):v[j]^=v[i];ops.append((i,j))
    for c in range(WIDTH):
        if not v[c]>>c&1:
            k=next((k for k in range(c+1,WIDTH) if v[k]>>c&1),None);need(k is not None,'full binary Vandermonde rank')
            add(k,c);add(c,k);add(k,c)
        for k in range(WIDTH):
            if k!=c and v[k]>>c&1:add(c,k)
    unit=[1<<j for j in range(WIDTH)];need(v==unit,'inverse elimination')
    # Rows-to-identity is the inverse. Reverse chronology from unit realizes the desired map.
    for i,j in reversed(ops):unit[j]^=unit[i]
    need(unit==rows,'actual forward local elementary action')
    return np.asarray(ops,dtype=np.uint32)


# Stream format: packed unsigned little-endian (opcode u8, first u32, second u32).
# INIT/MOVE carry a chart ID as second word; CLEAR uses zero there.
DTYPE=np.dtype([('op','u1'),('a','<u4'),('b','<u4')]);OP={'INIT':1,'ADD':2,'MOVE':3,'CLEAR':4}
class Emitter:
    def __init__(self,path=None):
        self.fp=path.open('wb') if path else None;self.h=sha256();self.count=Counter();self.purposes=Counter();self.stage='';self.n=0;self.nextid=2*ONEBANK
    def phase(self,name):self.stage=name
    def emit(self,op,a,b=0):
        aa,bb=np.broadcast_arrays(np.asarray(a),np.asarray(b));n=aa.size
        if not n:return
        frame=np.empty(n,dtype=DTYPE);frame['op']=OP[op];frame['a']=aa.flat;frame['b']=bb.flat
        data=frame.tobytes();self.h.update(data)
        if self.fp:self.fp.write(data)
        self.count[op]+=n;self.purposes[self.stage,op]+=n;self.n+=n
    def owner(self,c):
        q=self.nextid;self.nextid+=BITS;self.emit('INIT',np.arange(q,q+BITS),c);return q
    def snapshot(self,c,src):
        q=self.owner(c);self.addbank(src,q);return q
    def addbank(self,src,dst):self.emit('ADD',np.arange(src,src+BITS),np.arange(dst,dst+BITS))
    def movebank(self,src,chart):self.emit('MOVE',np.arange(src,src+BITS),chart)
    def word(self,base,nodes,trans,inverse):
        a=eliminator(tuple(nodes),trans);a=a if inverse else a[::-1];self.emit('ADD',base+a[:,0],base+a[:,1])
    def close(self):
        if self.fp:self.fp.close()


def local(role,stripe,index=0):return (role*STRIPES+stripe)*WIDTH+index*BITS

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def build(native,layout,out,word_path=None):
    nr=native.read_bytes();wr=gzip.decompress(layout.read_bytes());need(sha256(nr).hexdigest()==PINS['native'] and sha256(wr).hexdigest()==PINS['layout'],'frozen inputs')
    R=json.loads(nr)['native_roots'];w=json.loads(wr);rr=w['routes'];n=len(rr)
    # Validate GF64 multiplicative order, link phases to exact source and basis tables.
    xs=[1]
    for _ in range(62):xs.append(gf(xs[-1],2))
    need(len(set(xs))==63 and gf(xs[-1],2)==1,'GF64 modulus is primitive')
    L=lambda j:2+j; H=lambda a:113+a; D=lambda d:1233+d; C=lambda k:4383+k; F=lambda i:5503+i
    zero,hub=0,1
    xin=defaultdict(dict);yin=defaultdict(dict);ytap=defaultdict(dict);xend=defaultdict(dict)
    for route,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if sc is not None:
            alpha,s=sc;(xin if kind=='X' else ytap)[j,s][alpha]=route
        if dc is not None:
            alpha,s=dc;(yin if kind=='Y' else xend)[i,s][alpha]=route
    phys={};srcinfo={};ysystem={};xsystem={}
    for role in range(ROOTS):
        for stripe in range(STRIPES):
            ix=sorted(xin[role,stripe]);iy=sorted(yin[role,stripe]);need(len(ix)==len(iy)==16 and len(ytap[role,stripe])==len(xend[role,stripe])==12,'physical MDS split')
            xsystem[role,stripe]=ix;ysystem[role,stripe]=iy
            for p,alpha in enumerate(ix):phys[xin[role,stripe][alpha]]=local(role,stripe,p)
            for p,alpha in enumerate(iy):phys[yin[role,stripe][alpha]]=ONEBANK+local(role,stripe,p)
    need(len(phys)==n and len(set(phys.values()))==n,'every physical original once')
    K=[sum(1<<j for j,r in enumerate(R) if i==j or dot(R[i],r)==0) for i in range(ROOTS)];code={0:()}
    for i in CANON:
        new={v^K[i]:which+(i,) for v,which in code.items()};need(not set(code)&set(new),'independent canonical rows');code.update(new)
    need(all(v in code for v in K),'full native canonical decomposition')
    em=Emitter(word_path);moves=Counter();initial=np.arange(BITS);snapH={};snapD={};snapC={};snapF={};leftpar={};canon={};cuts={};reaches=defaultdict(set)
    def move(route,chart,gap):em.movebank(phys[route],chart);moves[gap]+=BITS
    def milestone(key):cuts[key]={'operation':em.n,'live_owned':em.nextid-2*ONEBANK,'live_fields':em.nextid}
    em.phase('source_parities_from_raw_X')
    for (j,s),table in sorted(ytap.items()):
        base=local(j,s)
        for alpha,route in sorted(table.items()):
            g=em.owner(L(j));leftpar[route]=g
            off=[(v,b) for b,row in enumerate(EVAL[alpha]) for v in setbits(row)]
            arr=np.asarray(off,dtype=np.uint32);em.emit('ADD',base+arr[:,0],g+arr[:,1])
    em.phase('source_X_Vandermonde_on_actual_lines')
    for (j,s),nodes in sorted(xsystem.items()):em.word(local(j,s),nodes,False,False)
    em.phase('X_line_to_A2_and_pure_snapshot')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='X':move(t,H(h),1);snapH[t]=em.snapshot(H(h),phys[t]);srcinfo[t]=(j,*sc)
    em.phase('X_A2_to_D4_and_pure_snapshot')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='X':move(t,D(d),2);snapD[t]=em.snapshot(D(d),phys[t]);reaches['X_D4'].add(d)
    em.phase('X_D4_to_E6_and_pure_snapshot')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='X' and k is not None:move(t,C(k),2);snapC[t]=em.snapshot(C(k),phys[t])
    em.phase('X_E6_to_terminal_and_pure_snapshot')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='X' and i is not None and i<ROOTS:move(t,F(i),1);snapF[t]=em.snapshot(F(i),phys[t])
    em.phase('X_close_and_restore_at_Hub')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='X':move(t,hub,4 if k is None else 2 if i>=ROOTS else 1)
    for (j,s),nodes in sorted(xsystem.items()):em.word(local(j,s),nodes,False,True)
    milestone('all_159840_X_raw_at_Hub_all_159840_Y_pure_ground')
    em.phase('canonical_formation_and_descent')
    for s in range(STRIPES):
        for p in range(DIM):
            for i in CANON:
                g=em.owner(hub);canon[i,s,p]=g
                for j in setbits(K[i]):em.addbank(local(j,s,p),g)
                em.movebank(g,zero);moves[8]+=BITS
    milestone('all_12960_canonical_binary_records_at_ground_Y_untouched')
    em.phase('canonical_preload_and_inverse_Y_decoder_ground')
    for (i,s),nodes in sorted(ysystem.items()):
        base=ONEBANK+local(i,s)
        for p in range(DIM):
            for b in code[K[i]]:em.addbank(canon[b,s,p],base+p*BITS)
        # D_system acts on Y at the final facet; pre-apply its inverse to Y + KX.
        em.word(base,nodes,True,True)
    em.phase('Y_native_line_visits_and_encoded_source_reads')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='Y' and j is not None and j<ROOTS:
            move(t,L(j),1);em.addbank(leftpar[t],phys[t]);srcinfo[t]=(j,*sc)
    em.phase('Y_A2_arrivals')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='Y' and h is not None:move(t,H(h),1 if j<ROOTS else 2)
    em.phase('Y_D4_arrivals_and_actual_split_X_handoffs')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind!='Y':continue
        move(t,D(d),4 if h is None else 2);reaches['Y_D4'].add(d)
        if h is None:
            mate=rr[t-1];need(mate[0]=='X' and mate[1]==d and mate[4] is None,'matched physical earlier X at same D4')
            em.addbank(snapD[t-1],phys[t]);srcinfo[t]=srcinfo[t-1]
    milestone('all_Y_on_D4_with_retained_X_source_snapshots')
    em.phase('Y_E6_and_facet_arrivals')
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='Y':move(t,C(k),2)
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if kind=='Y':move(t,F(i),1)
    em.phase('physical_Y_systematic_decoder_and_pure_X_injections')
    for (i,s),nodes in sorted(ysystem.items()):
        base=ONEBANK+local(i,s);em.word(base,nodes,True,False)
        for alpha,t in sorted(xend[i,s].items()):
            g=snapF[t];co=powers(alpha)
            for p,v in enumerate(co):
                for b in range(BITS):
                    m=gf(v,1<<b)
                    dest=list(setbits(m))
                    if dest:em.emit('ADD',g+b,base+BITS*p+np.asarray(dest,dtype=np.uint32))
    milestone('all_319680_originals_in_final_charts_before_retirement')
    # Exact pairwise transfer rank uses each distinct Vandermonde vector at most once.
    # For a native related pair every relevant H (and K) is one of sixteen. Thus all
    # source rows and output columns per pair are separately independent at every stripe.
    edge=defaultdict(list)
    for t,(kind,d,h,j,k,i,sc,dc) in enumerate(rr):
        if dc is None or t not in srcinfo:continue
        j,al,s=srcinfo[t];be,z=dc;need(dot(R[i],R[j])==0,'only native foreign message');edge[i,j].append((s,al,z,be))
    ranks=Counter();perrole={};frame=sha256()
    for i in range(ROOTS):
        perrole[i]=0
        for j in range(ROOTS):
            if dot(R[i],R[j])!=0:need((i,j) not in edge,'forbidden coefficient');continue
            terms=edge[i,j];src={(s,al) for s,al,z,be in terms};dst={(z,be) for s,al,z,be in terms}
            need(len(src)==len(dst)==len(terms),'distinct right/left Vandermonde labels')
            need(all(sum(s==q for s,_ in src)<=16 and sum(z==q for z,_ in dst)<=16 for q in range(STRIPES)),'per-stripe independent subsets')
            ranks[len(terms)]+=1;perrole[i]+=len(terms)
            frame.update(struct.pack('<BBB',i,j,len(terms)))
            for row in sorted(terms):frame.update(bytes(row))
    em.phase('all_dirty_retirements');em.emit('CLEAR',np.arange(2*ONEBANK,em.nextid,dtype=np.uint32));em.close()
    need(em.count['INIT']==em.count['CLEAR']==em.nextid-2*ONEBANK,'all ownership retired')
    need(moves==Counter({1:555*1440,2:903*720,4:24*1440,8:9*1440}),'complete binary route invoice')
    need(len(reaches['X_D4'])==len(reaches['Y_D4'])==3150,'real native records in each middle chart at the appropriate phase')
    need(sum(ranks.values())==6470 and sum(k*v for k,v in ranks.items())==42840 and ranks[0]==40,'all native ordered-pair transfer')
    receipt={'status':'PASS_CAUSAL_ALL111_FRACTIONAL_MDS_CONTROL','native_sha256':PINS['native'],'layout_sha256':PINS['layout'],
        'paid_binary_native_copies':1440,'GF64_copies':240,'original_binary_columns':2*ONEBANK,'terminal_rows_classified':2*ONEBANK,
        'word_format':'u8 opcode + little-endian u32 first + u32 second with no padding; opcodes INIT 1, ADD 2, MOVE 3, CLEAR 4',
        'stream_sha256':em.h.hexdigest(),'operation_count':em.n,'primitive_counts':dict(em.count),'binary_movement_profile':dict(sorted(moves.items())),
        'normalized_movement_profile':{'1':'555','2':'903/2','4':'24','8':'9'},'peak_owned':em.nextid-2*ONEBANK,'dirty_CLEAR':em.count['CLEAR'],
        'phase_counts':[{'phase':k,'op':o,'count':v} for (k,o),v in em.purposes.items()],'milestones':cuts,
        'noncanonical_foreign_pair_rank_GF64_histogram':dict(sorted(ranks.items())),'supported_foreign_pairs':6470-ranks[0],
        'sum_individual_foreign_pair_ranks':sum(k*v for k,v in ranks.items()),'required_rank_each_pair':240,'rank_terms_sha256':frame.hexdigest(),
        'per_receiver_sum_ranks_range':[min(perrole.values()),max(perrole.values())],'foreign_GF64_rectangles_rank_240':False,
        'complete_native_output_roles':[],'complete_supplier':False,'new_complete_kappa':False}
    out.mkdir(parents=True,exist_ok=True);(out/'PHYSICAL-RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],receipt['stream_sha256'],receipt['primitive_counts'],receipt['peak_owned'])

if __name__=='__main__':
    p=ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--layout',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--word',type=Path);a=p.parse_args();build(a.native,a.layout,a.out,a.word)
