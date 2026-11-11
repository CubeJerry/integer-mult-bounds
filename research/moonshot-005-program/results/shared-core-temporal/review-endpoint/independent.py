"""Independent backward exact E/R extraction and enumerated-subspace cohorts."""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import argparse,gzip,hashlib,json

HERE=Path(__file__).resolve().parent
def need(ok,why):
    if not ok:raise ValueError(why)
def add(row,other,c):
    for j,v in other.items():
        a=row.get(j,F(0))+c*v
        if a:row[j]=a
        else:row.pop(j,None)
def rank(rows):
    b={}
    for source in rows:
        row=dict(source)
        for j,p in b.items():
            if row.get(j):add(row,p,-row[j])
        if row:
            j=min(row);c=row[j];b[j]={k:v/c for k,v in row.items()}
    return len(b)
def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,default=HERE/'RESULT.json');args=p.parse_args()
    raw=args.source.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    need(sha=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source')
    w=json.loads(gzip.decompress(raw));mains=sorted(set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));ms=set(mains)
    events=[];skeleton=[]
    for e in w['program']:
        op=e[0]
        if op in ('ADD','COPY'): e=(op,e[1],e[2],F(e[3]))
        elif op=='SCALE':e=(op,e[1],F(e[2]))
        events.append(e)
        if e[1] in ms and (op not in ('ADD','COPY') or e[2] in ms):
            need(op not in ('INIT','CLEAR','COPY'),'main skeleton opcode')
            need(op!='SCALE' or e[2]!=0,'invertible main scale')
            skeleton.append(e)
    def backwards(owner,program):
        q={owner:F(1)}
        for e in reversed(program):
            op,a=e[:2]
            if op in ('INIT','CLEAR'):q.pop(a,None)
            elif op in ('ADD','COPY') and a in q:
                b=e[2];v=q.get(b,F(0))+e[3]*q[a]
                if v:q[b]=v
                else:q.pop(b,None)
            elif op=='SCALE' and a in q:
                q[a]*=e[2]
                if not q[a]:q.pop(a,None)
        need(not any(i not in ms for i in q),'main endpoint has helper coefficient')
        return q
    full={i:backwards(i,events) for i in mains};silent={i:backwards(i,skeleton) for i in mains}
    groups={};frames={}
    for i in mains:
        f=w['final'][i]
        if f not in frames:
            space={0}
            for v in w['frames'][f]:space|={a^v for a in tuple(space)}
            need(len(space)==2**len(w['frames'][f]),'frame independence')
            frames[f]=tuple(sorted(space))
        groups.setdefault(frames[f],[]).append(i)
    results=[]
    for space,ids in groups.items():
        rows=[silent[i] for i in ids];r=rank(rows);joint=rank(rows+[full[i] for i in ids]);d=joint-r
        need(r==len(ids),'skeleton cohort independence')
        results.append({'roles':ids,'frame_dimension':len(space).bit_length()-1,'rank_R':r,'joint_rank':joint,'deficit':d})
    deficit=sum(z['deficit'] for z in results);need(deficit==208,'total deficit')
    need(len(groups)==105,'cohort count')
    need(rank(list(silent.values()))==400,'all-cohort negative control')
    # The full rank of R makes the global merged-chart deficit zero; an
    # arbitrary cross-chart correction would therefore destroy the premise.
    histogram=dict(sorted(Counter(z['deficit'] for z in results).items()))
    need(histogram=={1:93,2:11,93:1},'cohort deficit histogram')
    upper=F(1771183386,1000000)-18*deficit
    need(upper==F(-1972816614,1000000) and upper<0,'complete raw bound')
    out={'status':'PASS_INDEPENDENT_EXACT_ENDPOINT_DEFICIT','source_sha256':sha,'cohorts':len(groups),'deficit':deficit,'deficit_histogram':histogram,'groups':results,'complete_margin_upper':str(upper),'scope':'Literal common-chart scalar correction with positive-rank charged MOVE arrivals; no changed initial coding/targets or free chart-changing primitive.','method':'Independent backward Fraction E/R interpreter; full binary subspace enumeration; exact sparse rational elimination; no author imports.'}
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='groups'},indent=2))
if __name__=='__main__':main()
