#!/usr/bin/env python3
"""Authenticate every single funded-donor obstruction on the public original inputs."""
import argparse,gzip,hashlib,importlib.util,json,subprocess,sys
from collections import Counter,defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
UP='2b3176a88b4c46d4e1dc944843859634baa18b82'
WORD_HEAD='14c74c6a67108f675ac1196a5f2415ead0920e71'

def require(x,msg):
    if not x:raise ValueError(msg)

def blob_match(repo,sha,name,source):
    if subprocess.run(['git','-C',str(repo),'cat-file','-e',sha],capture_output=True).returncode:return False
    actual=subprocess.check_output(['git','-C',str(repo),'cat-file','blob',sha+':'+name])
    require(actual==source.read_bytes(),'authenticated source '+name);return True

def boundary(g,donor,shadow,target):
    inventory=defaultdict(set)
    for e,chart in g.inputs.items():inventory[chart].add(e)
    inventory[282].add(shadow)
    reached=set()
    for e in g.schedule:
        if e==shadow:continue
        if e==donor:reached.add(g.routes[e][1]);continue
        src=g.source(e);active=src in reached
        if e==target:
            require(active,'actual exposed public terminal');return inventory[src]
        if e in g.routes:
            dest=g.routes[e][1]
            if active:
                inventory[dest].update(inventory[src]);reached.add(dest)
            else:inventory[dest].add(e)
    raise ValueError('terminal missing')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out.resolve();require(a.repo.is_dir()and(not out.exists()or not any(out.iterdir())),'repository directory and fresh output');out.mkdir(exist_ok=True,parents=True)
    for fn,d in json.loads((HERE/'MANIFEST.json').read_text())['sha256'].items():require(hashlib.sha256((HERE/fn).read_bytes()).hexdigest()==d,'hash '+fn)
    src=HERE/'inputs';imp=importlib.util.spec_from_file_location('original_p104',src/'7833-construction.py');S=importlib.util.module_from_spec(imp);imp.loader.exec_module(S)
    head=blob_match(a.repo,UP,'research/p104-successor-reader-cuts/funded-legs/construction.py',src/'7833-construction.py');wordhead=blob_match(a.repo,WORD_HEAD,'research/p104-chart306-chain/DOUBLE-CANDIDATE.json.gz',src/'DOUBLE-CANDIDATE.json.gz')
    w=S.load_word(src/'DOUBLE-CANDIDATE.json.gz');g=S.compensated(w,True);shadow,=g.routes.keys()-w.routes.keys();require(g.routes[shadow]==(3,282),'fixed fifth observer')
    all3=[e for e in w.routes if w.routes[e][0]==3];first=w.clock[w.readers(S.OBSERVER)[0]];elig={e for e in all3 if w.clock[e]<first and w.grade(w.routes[e])>=3}-{S.RETARGET,S.OBSERVER};require(len(all3)==908 and len(elig)==181,'entire native funding roster')
    receipts=json.loads(gzip.decompress((HERE/'WITNESSES.json.gz').read_bytes()));require(len(receipts)==len(elig)and{r['donor']for r in receipts}==elig,'all and only eligible donors')
    counts=Counter();values=[]
    for r in receipts:
        d,t=r['donor'],r['terminal'];grade=w.grade(w.routes[d]);require(r['native_clock']==w.clock[d]and r['old_route']==list(w.routes[d])and r['original_grade']==grade and t in w.terminals,'candidate identity');fixed=boundary(g,d,shadow,t)
        h=hashlib.sha256(json.dumps(sorted(fixed),separators=(',',':')).encode()).hexdigest();require(h==r['exterior_sha256']and len(fixed)==r['exterior_size'],'full exterior identification')
        xi=dict(r['original_input']);require(len(xi)==len(r['original_input'])and all(0<=j<len(w.inputs)and type(v)==int and v for j,v in xi.items()),'integral public stimulus')
        v=g.evaluate(xi);true=w.evaluate(xi)[t];require(all(not v.get(e,0)for e in fixed)and true==v[t] and true==S.Q(r['terminal_value'])!=0,'forward scalar evaluation');counts[grade]+=1;values.append((len(xi),len(fixed)))
    same=[e for e in elig if w.grade(w.routes[e])==3 and len(w.frames[w.routes[e][1]])>len(w.frames[3])];require(len(same)==74,'all grade and orientation preserving donors')
    subprocess.run([sys.executable,'-I','-B',str(HERE/'review/check.py'),'--sources',str(src),'--witness',str(HERE/'WITNESSES.json.gz'),'--out',str(out/'review')],check=True,stdout=subprocess.DEVNULL)
    require(json.loads((out/'review/RESULT.json').read_text())==json.loads((HERE/'review/output/RESULT.json').read_text()),'independent backwards review')
    subprocess.run([sys.executable,'-I','-B',str(HERE/'flexible/verify.py'),'--out',str(out/'flexible')],check=True)
    subprocess.run([sys.executable,'-I','-B',str(HERE/'review/flexible.py'),'--sources',str(src),'--witness',str(HERE/'flexible/WITNESSES.json.gz'),'--out',str(out/'review')],check=True,stdout=subprocess.DEVNULL)
    require(json.loads((out/'review/FLEXIBLE.json').read_text())==json.loads((HERE/'review/output/FLEXIBLE.json').read_text()),'independent arbitrary measurement audit')
    bill=json.loads((src/'7833-SUMMARY.json').read_text())['signed_price']
    deficit,credit=S.Q(bill['baseline_deficit'][0]),S.Q(bill['nominal_credit'][1]);calls=bill['native_calls']
    require(calls==48 and credit/calls>1 and deficit-(credit-calls)>S.Q('9.5511294717'),'same-grade fully charged shortfall')
    result={'status':'PASS_ALL_181_FUNDED_DONORS_PUBLIC_ONLY','upstream':UP,'word':S.WORD,'eligible':len(elig),'fixed_grade_orientation':len(same),'by_grade':dict(counts),'max_pulse_support':max(x for x,y in values),'exterior_min_max':[min(y for x,y in values),max(y for x,y in values)],'upstream_objects_present':[wordhead,head]}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result,flush=True)
if __name__=='__main__':main()
