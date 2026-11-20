"""Read or regenerate all 1,041 native H-only source and actual terminal panels."""
from pathlib import Path
import hashlib,importlib.util,json,sys
from collections import defaultdict
import numpy as np
def module(path,name):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def obtain(a,atlas,inverse):
    root=a.packed_endpoint
    expected=json.loads((root/'output/RESULT.json').read_text())
    hs=expected['native_centres'];ld={};zd={};live=defaultdict(list)
    if a.cache:
        with np.load(a.cache)as z:
            for key in z.files:
                kind,i,h,k=key.split('-');i,h,k=int(i),int(h),int(k)
                (ld if kind=='L'else zd)[i,h,k]=z[key]
                if kind=='L'and k==3:live[i].append(h)
    else:
        sys.path.insert(0,str(root));m=module(root/'check.py','old_packed_end')
        m.N,m.pack,_=m.prepare(a.repo,a.packing_review,a.field_review,a.parameters);m.a=atlas;m.inverse=inverse
        for i in range(111):
            for h in hs:
                if i not in m.pack[h,3][0].receivers:continue
                live[i].append(h)
                for k in (3,12):ld[i,h,k],zd[i,h,k]=m.one(h,k,i)
    digest=hashlib.sha256();L={};Z={}
    for i in range(111):
        if not live[i]:continue
        for k in (3,12):
            pts=sorted(live[i]);L[i,k]=np.hstack([ld[i,h,k]for h in pts]);Z[i,k]=np.hstack([zd[i,h,k]for h in pts])
            for h in pts:
                digest.update(bytes([i]));digest.update(h.to_bytes(2,'little'));digest.update(bytes([k]));digest.update(ld[i,h,k].tobytes());digest.update(zd[i,h,k].tobytes())
    assert digest.hexdigest()==expected['native_panel_stream_sha256'] and len(ld)==len(zd)==2082
    return hs,dict(live),L,Z
