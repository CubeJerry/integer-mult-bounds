"""Replay all one-equality relaxations against the companion chart package."""
import argparse,gzip,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--chart',type=Path,default=HERE.parent/'complex-clifford-chart-rank-cut');p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out.resolve()
    if not a.repo.is_dir()or out.exists()and any(out.iterdir()):raise ValueError('repository and fresh output required')
    for f,h in json.loads((HERE/'MANIFEST.json').read_text())['sha256'].items():
        if hashlib.sha256((HERE/f).read_bytes()).hexdigest()!=h:raise ValueError(f)
    for f,h in json.loads((HERE/'COMPANION.json').read_text()).items():
        if hashlib.sha256((a.chart/f).read_bytes()).hexdigest()!=h:raise ValueError('companion '+f)
    subprocess.run([sys.executable,'-I','-B',str(HERE/'engine/incidence.py'),'--chart',str(a.chart.resolve()),'--out',str(out)],check=True)
    output=json.loads((out/'RESULT.json').read_text());expected=json.loads(gzip.decompress((HERE/'output/RESULT.json.gz').read_bytes()))
    if expected!=output:raise ValueError('all 1,382 nine-flow records')
    print('PASS_ALL_SINGLE_ORDINARY_INCIDENCES',output['minimum_certified_numerator'])
if __name__=='__main__':main()
