#!/usr/bin/env python3
"""Independently recheck every physically changed foreign F block after the D feedback."""
import argparse,ctypes,hashlib,importlib.util,json,sys,tempfile,subprocess
from pathlib import Path
from types import SimpleNamespace
import numpy as np

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('repo','d-feedback','joint','out'):p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();repo=a.repo.resolve();base=repo/'research/moonshot-005-program/results';stream=base/'bit-native-rs-return-distance/stream';source=base/'bit-spread-rs-physical-word/author';spec=importlib.util.spec_from_file_location('word',stream/'check.py');pkg=importlib.util.module_from_spec(spec);spec.loader.exec_module(pkg)
    temp=tempfile.TemporaryDirectory(prefix='foreign-joint-');lib=Path(temp.name)/'gf.so';subprocess.run(['cc','-O3','-march=native','-std=c11','-fPIC','-shared',str(stream/'stream.c'),'-o',str(lib)],check=True);en=pkg.Engine(lib);alg=pkg.load_replay(base/'bit-physical-terminal-quotient/author');alg.mm=en.mm;nat=alg.Native(SimpleNamespace(repo=repo,h_words=source/'output',d_words=base/'bit-minimum-cache-d-atlas/author/output',k_words=base/'bit-gf64-actual-k-atlas/author/output'));cs=pkg.Cascade(nat,alg,en,True);mm=en.mm
    # Independent composition of all twelve cached source rows and their outgoing
    # late actuators. The shared physical kernel controls are checked separately.
    dwords=json.loads((a.d_feedback/'RESULT.json').read_bytes())['chosen_caches'];facet=json.loads((a.joint/'RESULT.json').read_bytes())['facet_words'];k=len(dwords);dvec={};dset={r['D'] for r in dwords};VV=np.asarray(nat.hword[9]['V'],np.uint8)
    for t,r in enumerate(dwords):
        d=r['D'];ys=nat.byd[d]['Y']
        for y,v in zip(ys,r['late_coefficients']):
            delta=np.zeros(k,np.uint8);delta[t]=v;dvec[y]=delta
    post={};zeros=np.zeros(k,np.uint8)
    for ss,cc in cs.word.values():
        for ins,outs in ss:
            v=mm(cs.vandermonde,np.stack([dvec.get(t,zeros)for t in ins]));post.update(zip(outs,v))
        for e,y in cc:post[y]^=post[e]
    outD=np.zeros((111*96,k),np.uint8)
    for (i,ch),(owners,g)in cs.facets.items():outD[96*i+ch*16:96*i+(ch+1)*16]=mm(g,np.stack([post.get(t,zeros)for t in owners]))
    assert all(not post.get(t,zeros).any()for r in facet for t in r['base_early_holder_ids'])
    text=(stream/'check.py').read_text().split('    def columns(self,j):')[1].split('\ndef load_replay(')[0].replace('        return col','        return col,physical');scope={'np':np,'require':pkg.require};exec('def exposed(self,j):'+text,scope);exposed=scope['exposed'];dets={r['facet']:[]for r in facet};vvhash=hashlib.sha256()
    for j in range(111):
        hv={};zero=np.zeros(96,np.uint8)
        for h in nat.planes[j]:
            ports=nat.byh[h];ds=sorted({d for phase,d in ports if d in nat.mark});use=[(s,d) for s,d in enumerate(ds)if d in dset]
            if not use:continue
            for stripe in range(nat.p[h]['early']):
                y=mm(VV,nat.source_in(j,h,'X',9,stripe)[:,:96]);
                for pos,d in use:hv[ports['X',d][stripe]]=y[pos]
        rows=[]
        for r in dwords:
            d=r['D'];_,m,n,weights=nat.dword[d];t=r['early_cache_index'];csrow=alg.cauchy([m+t],range(m));rows.append(mm(csrow,np.stack([hv.get(s,zero)for s in nat.byd[d]['X']]))[0])
        vv=np.stack(rows);vvhash.update(vv.tobytes());original,physical=exposed(cs,j)
        for r in facet:
            i=r['facet']
            if not nat.orth[i,j]:continue
            early=np.stack([physical.get(t,zero)for t in r['base_early_holder_ids']]);B=original[:,96*i:96*(i+1)].T^mm(outD[96*i:96*(i+1)],vv)^mm(np.asarray(r['late_addition_coefficients'],np.uint8),early)
            rk,dk=alg.echelon(B);alg.need(len(rk)==96 and dk!=0,'actual joint proper foreign determinant');dets[i].append([j,dk])
    assert all(len(dets[r['facet']])==r['native_foreign_blocks']for r in facet);a.out.mkdir(exist_ok=True,parents=True);result={'total_changed_facets_foreign_blocks':sum(map(len,dets.values())),'all_foreign_small_block_determinants':dets,'true_early_D_source_rows_sha256':vvhash.hexdigest(),'all_D_actuator_perturbations_zero_at_changed_F_early':True};(a.out/'FOREIGN.json').write_text(json.dumps(result,separators=(',',':'))+'\n');print('full foreign determinants',result['total_changed_facets_foreign_blocks'])
if __name__=='__main__':main()
