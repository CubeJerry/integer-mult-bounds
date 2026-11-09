"""Independent A review of C's local scans and long-key/short-Count boundary.

Imports reviewed routines, no author fixture, oracle, encoder or Tape.
Prepared with substantial OpenAI assistance; not a numerical-service review.
"""
from pathlib import Path
import hashlib
import json
import sys

PACKAGE=Path(__file__).resolve().parents[1]
FILES=('PROOF.md','union_bits.py','union_catalogue.py','union_fields.py','physical_router.py')
SNAPSHOT={f:(PACKAGE/f).read_bytes() for f in FILES}
sys.path.insert(0,str(PACKAGE))
from runtime_sources import physical_runtime


def need(ok,message):
    if not ok:raise ValueError(message)


class Sparse:
    """Separate absolute-coordinate hardware and primitive action counter."""
    def __init__(self,body=(),origin=5,warm=0,at_end=False):
        self.origin=origin
        self.storage={i:i%2 for i in range(origin)}
        self.storage[origin]=2
        self.storage.update({origin+1+i:x for i,x in enumerate(body)})
        self.storage.update({origin+1+len(body)+i:4 for i in range(warm)})
        self.head=origin+1+(len(body) if at_end else 0)
        self.actions=0;self.floor=origin;self.low=self.head;self.high=self.head
    def read(self):
        self.actions+=1;self.low=min(self.low,self.head);self.high=max(self.high,self.head)
        need(self.head>=self.floor,'local scan crossed protected prefix')
        return self.storage.get(self.head,4)
    def write(self,value):
        self.actions+=1;self.high=max(self.high,self.head)
        need(self.head>=self.floor and value in range(8),'local write boundary/alphabet')
        self.storage[self.head]=value
    def step(self,direction):
        need(direction in (-1,1),'unit physical movement')
        self.actions+=1;self.head+=direction;self.low=min(self.low,self.head);self.high=max(self.high,self.head)
        need(self.head>=self.floor,'local move crossed protected prefix')
    def append(self,value):
        need(self.read()==4,'append at first blank');self.write(value);self.step(1)
    def rewind(self):
        self.step(-1)
        while self.read()!=2:self.step(-1)
        self.step(1)
    def clear(self):
        self.rewind()
        while self.read()!=4:self.write(4);self.step(1)
        self.rewind()
    def body(self):
        out=[];p=self.origin+1
        while self.storage.get(p,4)!=4:out.append(self.storage[p]);p+=1
        return tuple(out)


def run():
    report={}
    with physical_runtime():
        import union_bits as bits
        from union_fields import Geometry
        from cardinal_counts import Count
        from scratch_pool import ScratchPool
        from session import OuterScope,borrowed_tape
        # No Count operation is available to these raw scans.
        class ForbiddenCount:
            def __init__(self,*a,**k):raise ValueError('long stream became a Count')
            @classmethod
            def literal(cls,*a,**k):raise ValueError('long stream became a Count')
        original=bits.Count;bits.Count=ForbiddenCount
        blocks=[];contexts=[]
        try:
            for prefix in (0,17,8191,65537):
                for length in (0,1,9,257):
                    parent=(6,)+tuple(i%2 for i in range(prefix))+(7,)
                    payload=tuple((i//2)%2 for i in range(length))
                    t=Sparse(parent+(6,)+payload+(7,),warm=4097,at_end=True)
                    cut=t.origin+1+len(parent);t.floor=cut
                    before={i:x for i,x in t.storage.items() if i<cut}
                    start=t.actions;bits.top_block(t);top=t.actions-start
                    need(top==3*length+7,'independent top-block action formula')
                    for x in payload:need(t.read()==x,'complete local block');t.step(1)
                    start=t.actions;bits.pop_block(t);pop=t.actions-start
                    need(pop==4*length+5,'independent pop-block action formula')
                    need(t.head==cut and t.low==cut,'local pop ends at its own append origin')
                    need(all(t.storage[i]==x for i,x in before.items()),'older block unchanged')
                    need(all(x==4 for i,x in t.storage.items() if i>=cut),'complete child erasure')
                    blocks.append(dict(parent_bits=prefix,child_bits=length,top=top,pop=pop))
            for length in (0,17,4097,65537):
                key=tuple((3*i//7)%2 for i in range(length))
                s,c,o=Sparse(key+(5,),warm=8191),Sparse(key+(5,),warm=65537),Sparse(warm=131071)
                bits.same_context(s,c,o)
                need(s.actions+c.actions+o.actions==8*length+8,'raw-context linear invoice')
                need(o.body()==key+(5,),'complete raw key retained exactly')
                s.rewind();start=s.actions;bits.skip_context(s)
                need(s.actions-start==3*length+3,'raw context skip has no arithmetic count')
                contexts.append(dict(key_bits=length,copy_actions=8*length+8,skip_actions=3*length+3))
        finally:bits.Count=original
        report['local_block_cases']=blocks;report['raw_context_cases']=contexts

        def decode_count(value):
            raw=borrowed_tape(value.tape).cells
            end=raw.index(3,1)
            return sum(int(x)<<i for i,x in enumerate(raw[1:end]))

        prefixes=[]
        for g,h in ((17,7),(65,7),(257,9)):
            t=g.bit_length();axis=g-1;width=7
            descriptors=tuple(Count.literal(x) for x in (g,h,t,width,axis*h))
            pool=ScratchPool(256);scope=OuterScope(pool)
            # All coordinates/ordinals are legal at L=2^h. The long all-one
            # coordinate prefix would be enormous if interpreted as an integer.
            big=lambda n,k:tuple((n>>j)&1 for j in reversed(range(k)))
            header=(0,1)+(1,)*(g*h)+(1,)*g+(1,)*(g*h)+big(g,t)+big(axis,t)+(0,)*(2*width)
            source=Sparse(header,warm=97);saved=Sparse(warm=8191)
            try:
                with scope.installed():
                    shape=Geometry(*descriptors[:4])
                    try:
                        result,equal=shape.key(source,descriptors[4],saved=saved)
                        need(equal and decode_count(result)==2**h-1,'only active ordinal becomes Count')
                        result.close();need(source.head==source.origin+1,'key restores exact input head')
                        need(saved.body()==(1,)*(axis*h),'long prefix stays raw')
                        saved.rewind()
                        result,equal=shape.key(source,descriptors[4],equal=saved)
                        need(equal and decode_count(result)==2**h-1,'raw prefix equality');result.close()
                        saved.storage[saved.origin+1]=0
                        result,equal=shape.key(source,descriptors[4],equal=saved)
                        need(not equal,'one raw prefix bit changes equality');result.close()
                    finally:shape.close()
                pool.empty()
                ell=(2**h+g+width+2).bit_length()+1
                extent=max(len(x.cells) for x in pool.tapes)
                need(extent<=4*ell+5,'Count backing remains short despite long raw prefix')
                prefixes.append(dict(axes=g,coordinate_bits=h,prefix_bits=axis*h,
                                     maximum_count_tape_cells=extent,pool_peak=pool.peak))
            finally:
                for value in descriptors:value.close()
        report['raw_prefix_cases']=prefixes
        # A direct bad conversion of the raw prefix visibly violates the same
        # short-metadata criterion; this discriminates the rejected alternative.
        width=Count.literal(448);pool=ScratchPool(256);scope=OuterScope(pool)
        try:
            with scope.installed():
                value=bits.big(Sparse((1,)*448),width);value.close()
            extent=max(len(x.cells) for x in pool.tapes)
            need(extent>4*10+5,'bad raw-prefix-to-Count control must exceed short backing')
            report['negative_raw_prefix_count_cells']=extent
        finally:width.close()
    need(all((PACKAGE/f).read_bytes()==b for f,b in SNAPSHOT.items()),'reviewed source changed during replay')
    report['source_sha256']={f:hashlib.sha256(b).hexdigest() for f,b in SNAPSHOT.items()}
    report['status']='PASS_A_INDEPENDENT_LOCAL_SCANS_AND_PREFIX_BOUNDARY'
    return report


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
