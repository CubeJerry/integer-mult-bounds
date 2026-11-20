"""All-original-input and all-baseline replay of the two star channels."""
import argparse
from array import array
from collections import defaultdict
import gzip,hashlib,json
from pathlib import Path


def need(x,why):
    if not x:raise ValueError(why)


def source(p):
    q=p/'research/moonshot-005-program/results'
    lp=gzip.decompress((q/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    rp=gzip.decompress((q/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes())
    need(hashlib.sha256(lp).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout')
    need(hashlib.sha256(rp).hexdigest()=='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','routes')
    r={}
    for line in rp.splitlines():
        row=json.loads(line);f=480*row[1]+row[2]+53280*(row[0]=='Y')
        need(f not in r,'physical owner uniqueness');r[f]=row
    roots=json.loads(lp)['root_table']
    adj=lambda i,j:sum(a*b for a,b in zip(roots[i],roots[j]))==0
    return r,[j for j in range(111) if adj(j,80)][:48],[i for i in range(111) if adj(i,10)][:48]


def check(word,axes,ctx,fault=None):
    routes,jset,iset=ctx;words=word['field_swap_words'];n=111*3840
    def order(tag):
        output=[]
        for key,pairs in sorted(words[tag].items(),key=lambda x:int(x[0])):
            key=int(key)
            for p,q in pairs:
                a=routes[p//8];b=routes[q//8]
                if tag=='source_X':need(a[0]==b[0]=='X' and a[1]==b[1]==key,'source swizzle')
                elif tag=='K_X':need(a[0]==b[0]=='X' and a[5]==b[5]==key,'early K swizzle')
                elif tag=='K_Y':need(a[0]==b[0]=='Y' and a[5]==b[5]==key,'late K swizzle')
                else:need(a[0]==b[0]=='Y' and a[1]==b[1]==key,'terminal swizzle')
                need(p!=q,'swap');output.append((p,q))
        return output
    xp=order('source_X')+order('K_X');yp=order('K_Y')+order('F_Y')
    if fault=='K_X':xp.pop()
    if fault=='K_Y':yp.pop(0)
    x=array('I',range(n));y=array('I',range(n))
    def swaps(buf,seq,base):
        for a,b in seq:
            a-=base;b-=base;buf[a],buf[b]=buf[b],buf[a]
    swaps(x,xp,0);captures=defaultdict(set)
    for holder,c in word['F80_capture_owner_to_central_position']:
        need(routes[holder//8][0]=='X' and routes[holder//8][7]==80,'actual F80')
        captures[c].symmetric_difference_update((x[holder],))
    swaps(x,reversed(xp),0);need(all(i==f for i,f in enumerate(x)),'all original X')
    swaps(y,reversed(yp),n)
    # Baselines are independent labels. Actual cross-contributions are sparse sets of X IDs.
    start={};expect={}
    for c,holder in word['line10_central_position_to_Y_owner']:
        need(routes[holder//8][0]=='Y' and routes[holder//8][6]==10,'real late line tap')
        need(holder-n not in start,'distinct injection');start[holder-n]={10*3840+c}
    for p,q in yp:
        a=p-n;b=q-n;va=start.pop(a,None);vb=start.pop(b,None)
        if va:start[b]=va
        if vb:start[a]=vb
    swaps(y,yp,n);need(all(i==f for i,f in enumerate(y)),'all original Y baselines')
    for c,v in captures.items():start[80*3840+c]=start.get(80*3840+c,set()) ^ v
    for s in range(16):
        for t in axes:
            c=4*s+t;expect[80*3840+c]={j*3840+64*ell+c for ell,j in enumerate(jset,1)}
            for ell,i in enumerate(iset,1):expect[i*3840+64*ell+c]={10*3840+c}
    return start==expect,len(start),sum(len(v) for v in start.values())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--certs',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    p=ap.parse_args();ctx=source(p.repo);res={}
    for label,axes in [('cross',[0]),('half',[0,1]),('three_quarters',[0,1,2])]:
        word=json.loads(gzip.decompress((p.certs/(label+'-word.json.gz')).read_bytes()))
        yes,outs,edges=check(word,axes,ctx);need(yes,'entire proper transfer')
        faults={}
        for fault in ['K_X','K_Y']:
            fails=not check(word,axes,ctx,fault)[0];need(fails,'inverse-normalized control changes target');faults[fault]=fails
        res[label]={'correct':yes,'nonzero_output_rows':outs,'nonzero_proper_coefficients':edges,
                    'independent_X_fields':426240,'independent_Y_baselines':426240,'reroute_controls':faults}
    p.out.mkdir(parents=True,exist_ok=True)
    (p.out/'REPLAY.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');print(res)


if __name__=='__main__':main()
