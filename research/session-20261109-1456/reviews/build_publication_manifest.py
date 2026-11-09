"""Create an additions-only, frozen-tree GitHub publication manifest."""
import argparse
import base64
import json
from pathlib import Path
import subprocess

p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('package');p.add_argument('title');a=p.parse_args()
root=Path(a.root);base='7c49fe32c55de02c2c873655c804b16e4c3fef0a'
def git(*args):return subprocess.check_output(['git','-C',str(root),*args]).decode().strip()
assert not git('status','--porcelain'), 'working tree must be clean'
deps_path=root/a.package/'DEPENDENCIES.json'
deps=json.loads(deps_path.read_text()).get('files',[]) if deps_path.exists() else []
deps={(d['path'] if 'path' in d else a.package+'/'+d['local_path']):d for d in deps}
files=[]
for line in git('diff','--name-status',base,'HEAD').splitlines():
    status,path=line.split('\t');assert status=='A' and path.startswith(a.package+'/'),(status,path)
    mode,kind,blob=git('ls-tree','HEAD','--',path).split('\t')[0].split()
    assert kind=='blob' and mode in ('100644','100755')
    data=subprocess.check_output(['git','-C',str(root),'show','HEAD:'+path])
    f=dict(path=path,mode=mode,type='blob',git_blob=blob,bytes=len(data))
    if path in deps:
        assert deps[path]['git_blob']==blob,(path,'dependency blob mismatch')
        f['sha']=blob
    else:
        try:content=data.decode('utf-8')
        except UnicodeDecodeError:content=None
        if content is not None and len(data)<=20000:f['content']=content
        else:
            f['load_file']=str(root/path);f['encoding']='utf-8' if content is not None else 'base64'
    files.append(f)
assert files
print(json.dumps(dict(worktree=str(root),package=a.package,base=base,local_head=git('rev-parse','HEAD'),tree=git('rev-parse','HEAD^{tree}'),title=a.title,files=files)))
