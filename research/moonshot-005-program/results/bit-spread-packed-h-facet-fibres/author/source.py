from pathlib import Path
import sys,importlib.util,json,hashlib
import numpy as np
def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def prepare(repo,review,field,pars):
    r=module(review,'packed_native_reader');f=module(field,'gf64_source_review')
    n=r.Native(repo,f);p=json.loads(pars.read_text());cfg=p['complete_31'];fixtures={tuple(v['centres']):v for v in p['pairs']};out={};groups=[]
    for h,q,_ in cfg['pairs']:
        grp=(h,q);groups.append(grp)
        for k in (3,12):
            ch=[r.Chart(n,z,k)for z in grp];maps=r.paired(ch,fixtures[grp][str(k)])
            out.update({(c.h,k):(c,maps,grp)for c in ch})
    for h in cfg['singles']:
        groups.append((h,))
        for k in (3,12):
            c=r.Chart(n,h,k);out[h,k]=(c,c.single(p['one_centre'][str(k)]),(h,))
    return n,out,groups
