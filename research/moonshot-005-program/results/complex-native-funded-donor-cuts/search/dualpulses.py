"""Build diagonal exact sparse input witnesses for one or two required outputs."""
from pathlib import Path
import argparse,gzip,json,hashlib,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from pulses import load,derive,value

def main():
    p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);p.add_argument('--screen',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();S=load(a.sources);w=S.load_word(a.sources/'DOUBLE-CANDIDATE.json.gz');g=S.compensated(w,True);V=S.all_public_rows(g);cert=[];rows=json.loads(gzip.decompress(a.screen.read_bytes()) if a.screen.suffix=='.gz' else a.screen.read_bytes())['excluded']
    for r in rows:
        d,t,fix=r['donor'],r['terminals'],r['exterior'];vec=[]
        for i,e in enumerate(t):
            other=t[:i]+t[i+1:];piv,rank=derive(S,V,len(w.inputs),fix+other,e);S.require(rank==r['rank']+len(other)and all(not value(V,q,piv)for q in fix+other),'joint exterior and other coordinate vanish');raw=value(V,e,piv);S.require(raw,'claimed output is nonzero')
            vec.append({'original_input':sorted(piv.items()),'diagonal_value':str(raw)})
        cert.append({'donor':d,'available_extra_scalars':r['available_new_scalar'],'terminals':t,'exterior_size':len(fix),'exterior_rank':r['rank'],'exterior_sha256':hashlib.sha256(json.dumps(fix,separators=(',',':')).encode()).hexdigest(),'stimuli':vec})
    S.require(len(rows)==len({x['donor']for x in rows})==181,'all funding arrangements');a.out.write_bytes(gzip.compress((json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
    print('one/two',sum(len(q['stimuli'])==1 for q in cert),sum(len(q['stimuli'])==2 for q in cert),'max support',max(len(z['original_input'])for r in cert for z in r['stimuli']))
if __name__=='__main__':main()
