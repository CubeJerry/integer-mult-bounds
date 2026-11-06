"""Deterministic unsigned connector schedules; @CubeJerry + OpenAI Codex.

Apache-2.0. Complete physical costs are outside this abstract schedule model.
"""
from dataclasses import dataclass


def require(ok, message):
    if not ok:
        raise ValueError(message)


@dataclass(frozen=True)
class Block:
    groups: int
    width: int
    characteristic: int

    def __post_init__(self):
        require(all(type(v) is int for v in (self.groups,self.width,self.characteristic)), 'integer parameters')
        require(self.groups >= 1 and self.width >= 1, 'positive dimensions')
        require(self.characteristic >= self.groups+1, 'output read budget')
        require(self.groups*((1<<self.width)-1) <= self.characteristic, 'subset round budget')

    @property
    def sources(self):
        return self.groups*self.width

    def round_for(self, group, subset):
        require(0 <= group < self.groups and 1 <= subset < (1<<self.width), 'subset index')
        return group*((1<<self.width)-1)+subset-1

    def word(self):
        k=self.sources
        used=self.groups*((1<<self.width)-1)
        for r in range(self.characteristic):
            if r < used:
                group,index=divmod(r,(1<<self.width)-1)
                chosen=[group*self.width+j for j in range(self.width) if (index+1)>>j&1]
            else:
                chosen=[]
            selected=[False]*k
            for j in chosen:
                selected[j]=True
            yield from chosen
            yield from (j for j in range(k) if not selected[j])

    def reads(self, mask):
        require(type(mask) is int and 0 <= mask < (1<<self.sources), 'mask range')
        if not mask:
            return ()
        rounds=[]; times=[]
        for group in range(self.groups):
            subset=mask>>(group*self.width)&((1<<self.width)-1)
            if subset:
                r=self.round_for(group,subset)
                rounds.append(r)
                times.append(r*self.sources+subset.bit_count())
        times.append((-sum(rounds)%self.characteristic)*self.sources)
        return tuple(sorted(times))


def concatenated_reads(block, copies, mask):
    require(type(copies) is int and copies >= 1, 'positive copy count')
    require(copies*(block.groups+1) <= block.characteristic, 'total depth budget')
    require(type(mask) is int and 0 <= mask < (1<<(copies*block.sources)), 'global mask range')
    result=[]
    for copy in range(copies):
        local=mask>>(copy*block.sources)&((1<<block.sources)-1)
        result.extend(copy*block.sources*block.characteristic+t for t in block.reads(local))
    return tuple(result)


def capacity_parameters(c):
    require(type(c) is int and c >= 2, 'characteristic')
    D=c.bit_length()-1
    b=(c//D+1).bit_length()-1
    block=Block(D,b,c)
    copies=c//(D+1)
    return block,copies,block.sources*copies
