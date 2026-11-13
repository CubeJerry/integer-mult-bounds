#!/usr/bin/env python3
"""Executed optimized-mode equivalence and in-memory corruption controls."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import importlib.util,json,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=Path('/workspace/scratch/19b21bdb3d72')
def need(ok,label):
    if not ok:raise ValueError(label)
def semantic(data,drop):return {k:v for k,v in data.items() if k not in drop}
def run():
    names=('PILOT.json','RESULT.json','REFINED.json');saved={n:(HERE/n).read_bytes() for n in names};normal={n:json.loads(b) for n,b in saved.items()}
    optdir=HERE/'optimized';optdir.mkdir(exist_ok=True)
    commands=[[sys.executable,'-I','-B','-O',str(HERE/'pilot.py'),'--limit','16384'],[sys.executable,'-I','-B','-O',str(HERE/'refine.py')]]
    try:
        for index,command in enumerate(commands):
            result=subprocess.run(command,cwd=HERE,check=True,text=True,capture_output=True,timeout=60);(optdir/f'run-{index}.log').write_text(result.stdout+result.stderr)
        optimized={n:json.loads((HERE/n).read_text()) for n in ('RESULT.json','REFINED.json')}
        for n,data in optimized.items():(optdir/n).write_text(json.dumps(data,indent=2)+'\n')
        need(semantic(normal['RESULT.json'],{'seconds'})==semantic(optimized['RESULT.json'],{'seconds'}),'all16384 normal/optimized records identical apart from runtime')
        need(semantic(normal['REFINED.json'],{'full_census_sha256'})==semantic(optimized['REFINED.json'],{'full_census_sha256'}),'normal/optimized refined theorem identical')
        need(normal['PILOT.json']['records']==normal['RESULT.json']['records'][:256],'pilot agrees with full census prefix')
    finally:
        for n,b in saved.items():(HERE/n).write_bytes(b)
    # Semantic fault injections leave all frozen input files untouched. The
    # normal byte pins remain intact, while parsed mathematical data is corrupted.
    spec=importlib.util.spec_from_file_location('funding_refine_controls',HERE/'refine.py');module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    rowpath=ROOT/'worker-b/helper-graph/ROWS.json';targetpath=ROOT/'independent-temporal-result.json';rows=json.loads(rowpath.read_text());targets=json.loads(targetpath.read_text())
    bad_rank=deepcopy(rows);next(r for r in bad_rank['records'] if r['event']==45706)['rank']=9
    bad_zero=deepcopy(rows);next(r for r in bad_zero['records'] if r['event']==58936)['row']={}
    bad_target=deepcopy(targets);next(r for r in bad_target['records'] if r['event']==45656)['target']={'0':'1'}
    bad_weight=deepcopy(rows);bad_weight['targets']['1344']=1
    faults=[('zero_credit_exceeds_support_weight',rowpath,bad_rank),('dependent_zero_row',rowpath,bad_zero),('wrong_cache_target',targetpath,bad_target),('wrong_R4_target_weight',rowpath,bad_weight)]
    original_read=Path.read_text;outcomes=[]
    for label,path,data in faults:
        encoded=json.dumps(data)
        def read(p,*args,**kwargs):return encoded if p==path else original_read(p,*args,**kwargs)
        try:
            with patch.object(Path,'read_text',read):module.run()
        except ValueError as error:outcomes.append({'control':label,'rejected':True,'reason':str(error)})
        else:raise ValueError('corruption accepted: '+label)
    need(all((HERE/n).read_bytes()==b for n,b in saved.items()),'normal frozen receipts restored unchanged')
    out={'status':'PASS_NORMAL_OPTIMIZED_AND_FOUR_FAILURE_CONTROLS','normal_and_optimized_census_masks':16384,'normal_and_optimized_refinement_equivalent':True,'pilot256_matches_full_prefix':True,'ignored_nondeterministic_fields':['census.seconds','refined.full_census_sha256 (depends on seconds)'],'executed_optimized_commands':commands,'failure_controls':outcomes,'normal_receipt_sha256':{n:sha256(b).hexdigest() for n,b in saved.items()},'frozen_primary_inputs_changed':False}
    (HERE/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':run()
