"""Check arbitrary-fifth-field public terminal cuts by physical forward evaluation."""
import argparse,gzip,hashlib,importlib.util,json
from collections import defaultdict,Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(x,why):
    if not x:raise ValueError(why)

def exterior(g,donor,shadow,targets):
    stock=defaultdict(set)
    for e,v in g.inputs.items():stock[v].add(e)
    reached={282};fed={282};borders={};reachable={}
    for e in g.schedule:
        if e==shadow:continue
        if e==donor:reached.add(g.routes[e][1]);continue
        src=g.source(e)
        if e in targets:
            need(src in reached,'affected terminal');borders[e]=stock[src].copy();reachable[e]=src in fed
        if e in g.routes:
            dst=g.routes[e][1]
            if src in reached:
                stock[dst].update(stock[src]);reached.add(dst)
            else:stock[dst].add(e)
            if src in fed:fed.add(dst)
    need(set(borders)==set(targets),'every terminal checked')
    return set.union(*borders.values()),any(reachable.values())

def check(src,wit,out):
    s=importlib.util.spec_from_file_location('p104_actual',src/'7833-construction.py');S=importlib.util.module_from_spec(s);s.loader.exec_module(S)
    w=S.load_word(src/'DOUBLE-CANDIDATE.json.gz');g=S.compensated(w,True);shadow,=g.routes.keys()-w.routes.keys();need(g.routes[shadow]==(3,282),'fifth receiver')
    index=w.clock[w.readers(S.OBSERVER)[0]];all_donors={e for e,rt in w.routes.items()if rt[0]==3 and w.clock[e]<index and w.grade(rt)>=3}-{S.RETARGET,S.OBSERVER}
    roster=json.loads(gzip.decompress(wit.read_bytes()));need(len(roster)==len(all_donors)==181 and {r['donor']for r in roster}==all_donors,'entire independently recovered roster')
    histogram=Counter();cost=Counter();maxwidth=0;ranges=[]
    for r in roster:
        d,ts=r['donor'],r['terminals'];need(ts and len(set(ts))==len(ts)and set(ts)<=set(w.terminals),'distinct true terminals')
        fix,can=exterior(g,d,shadow,ts);n=int(can);need(len(ts)==n+1 and r['available_extra_scalars']==n,'one more independent demand than arbitrary channel capacity')
        h=hashlib.sha256(json.dumps(sorted(fix),separators=(',',':')).encode()).hexdigest();need(len(fix)==r['exterior_size']and h==r['exterior_sha256'],'complete pooled exterior')
        vec=r['stimuli'];need(len(vec)==len(ts),'full square test matrix')
        for j,z in enumerate(vec):
            p=dict(z['original_input']);need(len(p)==len(z['original_input']) and all(type(i)==type(v)==int and 0<=i<len(w.inputs) and v for i,v in p.items()),'public integer pulse')
            v=g.evaluate(p);original=w.evaluate(p);need(all(not v.get(i,0)for i in fix),'every fixed exterior row vanishes')
            need(all(original[t]==v[t] and (v[t]==S.Q(z['diagonal_value'])!=0 if j==k else v[t]==0)for k,t in enumerate(ts)),'forward demand matrix is diagonal nonsingular')
            maxwidth=max(maxwidth,len(p))
        histogram[n]+=1;cost[w.grade(w.routes[d])]+=1;ranges.append(len(fix))
    result={'status':'PASS_ALL_181_ARBITRARY_FUNDED_DONORS','eligible':len(roster),'grade_counts':dict(cost),'one_unreachable_terminal':histogram[0],'two_terminal_rank_two':histogram[1],'maximum_integer_pulse_support':maxwidth,'full_exterior_min_max':[min(ranges),max(ranges)],'generous_new_information':'one arbitrary original scalar freely available to chart 282 before every event','additional_released_source':'all chart-282 sends and their causal descendants from the beginning'}
    out.mkdir(parents=True,exist_ok=True);(out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result,flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,default=HERE.parent/'inputs');p.add_argument('--witnesses',type=Path,default=HERE/'WITNESSES.json.gz');p.add_argument('--out',type=Path,required=True);a=p.parse_args();check(a.sources,a.witnesses,a.out)
