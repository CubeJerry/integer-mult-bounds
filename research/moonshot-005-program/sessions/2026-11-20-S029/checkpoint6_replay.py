"""Replay the native RS determinants, regional cut and local rank-distance accounts.

Default checks use both recorded elimination directions and replay the structural arithmetic.
Use --heavy to regenerate the original-source coefficient streams and their pivots as well.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--heavy',action='store_true')
    ap.add_argument('--only',help='Comma-separated named heavy jobs (e.g. stream-small,cut-review-large)')
    ap.add_argument('--jobs',type=int,default=1)
    args=ap.parse_args()
    repo=args.repo.resolve()
    out=args.out.resolve()
    out.mkdir(parents=True,exist_ok=True)
    R=repo/'research/moonshot-005-program/results'
    N=R/'bit-native-rs-return-distance'
    C=R/'bit-physical-regional-prefix-cut'
    T=R/'bit-spread-rs-physical-word/author'
    H=T/'output'
    D=R/'bit-minimum-cache-d-atlas/author/output'
    K=R/'bit-gf64-actual-k-atlas/author/output'
    replay=R/'bit-physical-terminal-quotient/author'
    digest={}
    def get(p):
        raw=p.read_bytes()
        return json.loads(gzip.decompress(raw) if p.suffix=='.gz' else raw)
    def execute(script,flags):
        subprocess.run([sys.executable,'-B',script,*flags],check=True,stdout=subprocess.DEVNULL,
                       env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'))
    def verify(condition,why):
        if not condition:
            raise ValueError(why)
    cgate=C/'author/output/19'
    for sec,sz,fdet,dsize,ddet,csz,cdet in [('small',10656,29,5280,41,7218,22),('large',42624,33,21120,52,28872,34)]:
        nm=sec.upper()+'.json'
        s=get(N/'stream/output'/nm)
        verify(s['size']==s['rank']==sz and s['determinant_GF64']==fdet,'global determinant')
        native=N/'author/output'/(sec+'-all.json.gz')
        if native.exists():
            u=get(native)
            verify(u['size']==u['rank']==sz and u['pivot_minor_determinant_GF64']==fdet,'dense native determinant')
        u=get(N/'author/output'/(sec+'-55.json.gz'))
        d=get(N/'review/output'/nm)
        verify(u['size']==u['rank']==d['rank']==dsize and u['pivot_minor_determinant_GF64']==d['determinant_in_native_GF64']==ddet,'disjoint restriction')
        verify(set(u['columns']).isdisjoint(u['rows']) and len(set(u['selected_rows']))==len(set(u['pivot_columns']))==dsize,'disjoint native pivots')
        b=get(cgate/nm)
        r=get(C/'review/output'/nm)
        piv=gzip.decompress((cgate/(sec.upper()+'-PIVOTS.json.gz')).read_bytes())
        verify(sha256(piv).hexdigest()==b['selected_columns_sha256'] and len(set(json.loads(piv)))==csz,'regional native pivot transcript')
        verify(b['rank']==r['submitted_square_minor_rank']==csz and b['certificate_minor_determinant']==r['independent_determinant']==cdet,'pre-K region')
        digest[sec]=dict(global_determinant=fdet,global_size=sz,disjoint_determinant=ddet,disjoint_size=dsize,
                         region_determinant=cdet,region_pivots=csz)
    execute(N/'author/cost.py',['--repo',repo,'--out',out/'distance'])
    execute(C/'author/gate.py',['--repo',repo,'--cut',cgate,'--out',out/'cut'])
    for path,ref in [(out/'distance/RESULT.json',N/'author/output/RESULT.json'),(out/'cut/GATE.json',C/'author/output/GATE.json')]:
        verify(path.read_bytes()==ref.read_bytes(),'structural gate '+ref.name)
        digest[path.parent.name]=sha256(path.read_bytes()).hexdigest()
    if args.heavy or args.only:
        def compile(src,target):
            subprocess.run(['cc','-O3','-march=native','-std=c11','-fPIC','-shared',src,'-o',target],check=True)
        stream=out/'stream.so'
        mult=out/'mult.so'
        compile(N/'stream/stream.c',stream)
        compile(T/'gf64_matmul.c',mult)
        jobs=[]
        common=['--repo',repo,'--replay',replay,'--h-words',H,'--d-words',D,'--stream-lib',stream]
        for sec in ('small','large'):
            nm=sec.upper()+'.json'
            jobs.extend([
              ('stream-'+sec,N/'stream/check.py',common+['--k-words',K],N/'stream/output'/nm),
              ('disjoint-'+sec,N/'review/verify.py',common+['--k-words',K,'--canonical',N/'stream'],N/'review/output'/nm),
              ('cut-'+sec,C/'author/check.py',common+['--engine',N/'stream','--rows','19'],cgate/nm),
              ('cut-review-'+sec,C/'review/check.py',['--repo',repo,'--transfer',T,'--engine',N/'stream','--k-words',K,'--d-words',D/'CHARTS.json.gz','--stream-lib',stream,'--mult',mult,'--cut',cgate],C/'review/output'/nm)
            ])
        if args.only:
            names=set(args.only.split(','))
            verify(names<={j[0] for j in jobs},'unknown heavy job')
            jobs=[j for j in jobs if j[0] in names]
        def run(job):
            key,script,flags,reference=job
            sector=key.split('-')[-1]
            execute(script,flags+['--sector',sector,'--out',out/key])
            result=get(out/key/reference.name)
            expected=get(reference)
            if key.startswith('stream-'):
                # The retained author run used additional external spot checks in scratch.
                # Replay from the committed operators has no external blocks. Rank and all
                # original-source stream digests, checkpoints and native field data must match.
                verify(result.pop('external_blocks_digest') is None,'unexpected external input')
                expected.pop('external_blocks_digest')
            verify(result==expected,'native coefficient-stream mismatch '+key)
            return key,sha256(json.dumps(result,sort_keys=True).encode()).hexdigest()
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            digest['recomputed_native_streams']=dict(pool.map(run,jobs))
    (out/'VALIDATION.json').write_text(json.dumps(digest,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
