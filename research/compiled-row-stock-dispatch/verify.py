"""Read-only stdlib replay of the scoped current row/occurrence dispatcher."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import importlib.util
import json
import re
import sys
import tempfile


ROOT=Path(__file__).resolve().parent


def need(ok,message):
    if not ok:raise ValueError(message)


def digest(data):return hashlib.sha256(data).hexdigest()


def authenticate(root=ROOT):
    manifest=json.loads((root/"DEPENDENCIES.json").read_text())
    need(manifest['schema_version']==1,"dependency schema")
    seen=set();report=[]
    for row in manifest['files']:
        relative=PurePosixPath(row['local_path'])
        need(not relative.is_absolute() and '..' not in relative.parts
             and relative.parts[0]=='vendor',"exact local export path")
        need(str(relative) not in seen,"unique frozen export")
        seen.add(str(relative));path=root/str(relative)
        need(path.is_file() and not path.is_symlink(),"real frozen export")
        raw=path.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        need(blob==row['git_blob'],"frozen Git blob drift: "+str(relative))
        need(digest(raw)==row['sha256'],"frozen SHA256 drift: "+str(relative))
        commit=row.get('published_commit',row.get('local_commit'))
        need(isinstance(commit,str) and re.fullmatch('[0-9a-f]{40}',commit),"exact dependency commit")
        need(row['repository'] in ('CrocSwap/integer-mult-bounds','CubeJerry/integer-mult-bounds'),
             "exact retained canonical/fork source repository")
        report.append(dict(path=str(relative),git_blob=blob,sha256=digest(raw),commit=commit,
                           provenance="published" if 'published_commit' in row else "local-review-export"))
    return report


def authentication_control():
    row=json.loads((ROOT/"DEPENDENCIES.json").read_text())['files'][0]
    with tempfile.TemporaryDirectory(prefix="row-source-control-") as directory:
        temp=Path(directory);(temp/"vendor").mkdir()
        (temp/"DEPENDENCIES.json").write_text(json.dumps(dict(schema_version=1,files=[row])))
        (temp/row['local_path']).write_bytes((ROOT/row['local_path']).read_bytes()+b'\n# actual altered export\n')
        try:authenticate(temp)
        except ValueError:return "altered_export_rejected_before_import"
    raise ValueError("changed dependency bytes accepted")


def load(name):
    path=ROOT/(name+".py")
    spec=importlib.util.spec_from_file_location("dispatch_verify_"+name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module
    exec(compile(path.read_bytes(),str(path),"exec"),module.__dict__)
    return module


def check():
    frozen=authenticate()
    selected=json.loads((ROOT/"vendor/SELECTED-RESULT.json").read_text())
    assumptions=[x['id'] for x in selected['assumptions']]
    need(selected['kappa']=='781451/250000000' and 6030 in selected['source_prs'],"selected source binding")
    need(set(assumptions)=={'native_all_columns','owned_erasure','compiler','precision_tape','analytic_recovery'},
         "all five selected assumptions retained")
    current=json.loads((ROOT/"vendor/LIFECYCLE-RESULT.json").read_text())['current_source']
    raw_targets={int(rank):count for rank,count in current['raw_targets'].items()}
    need(max(raw_targets)==145 and sum(raw_targets.values())==current['public_count']==13444,
         "actual selected complete ambient equals maximum target")
    source_binding=dict(raw_ambient=145,maximum_raw_target=max(raw_targets),
                        productive_fields=current['public_count'],raw_paid=sum(current['raw_paid'].values()),
                        scope="Authenticated lifecycle receipt binding only; native algebra is retained")
    negative=authentication_control()
    names=("check_core","check_padding","check_geometry","check_compiler","check_controls","check_join")
    results={name:load(name).check() for name in names}
    runtime=("row_programs.py","services.py","pattern_padding.py","compiler_routes.py")
    own={name:digest((ROOT/name).read_bytes()) for name in (*runtime,*(x+".py" for x in names),
                                                          "fixture_tools.py","verify.py")}
    return json.loads(json.dumps(dict(schema_version=1,status="PASS_SCOPED_ROW_OCCURRENCE_DISPATCH",
                selected_kappa=selected['kappa'],retained_assumptions=assumptions,
                fixed_row_work_ports=40,encoded_header_fields=23,
                selected_source_binding=source_binding,
                frozen_exports=frozen,own_program_sha256=own,
                source_control=negative,checks=results),sort_keys=True))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-result',action='store_true')
    args=parser.parse_args()
    result=check()
    serialized=json.dumps(result,indent=2,sort_keys=True)+"\n"
    target=ROOT/"RESULT.json"
    if args.write_result:
        target.write_text(serialized)
    else:
        need(json.loads(target.read_text())==result,"scientific receipt drift; inspect before explicit regeneration")
    print(json.dumps(dict(status=result['status'],exports=len(result['frozen_exports']),
                          retained_assumptions=result['retained_assumptions'],
                          result_sha256=digest(serialized.encode())),sort_keys=True))
    print("PASS_COMPILED_ROW_STOCK_DISPATCH")


if __name__=="__main__":main()
