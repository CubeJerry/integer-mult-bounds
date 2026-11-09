#!/usr/bin/env python3
"""Separate endpoint, literal-flow and rational-majorant replay.

The endpoint engine was written by the lead agent independently of the
construction author and this package's signature checker. Apache-2.0.
"""
from pathlib import Path
from hashlib import sha256, sha1
import copy
import json
import endpoint_oracle as endpoint
import flow_check
import ambient_bounds

HERE=Path(__file__).resolve().parent


def need(condition,message):
    if not condition:raise ValueError(message)


def main():
    for record in json.loads((HERE/'RETAINED.json').read_text())['files']:
        b=(HERE/record['path']).read_bytes()
        need(len(b)==record['bytes'] and sha256(b).hexdigest()==record['sha256'],'exact retained source')
        need(sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==record['git_blob'],'exact Git blob')
    word_path=HERE/'retained/native-word.json.gz';caller_path=HERE/'retained/caller.json'
    word,caller=endpoint.read(word_path),endpoint.read(caller_path)
    saved=json.loads((HERE/'ENDPOINT-RECEIPT.json').read_text())
    need(saved['word_sha256']==sha256(word_path.read_bytes()).hexdigest() and saved['caller_sha256']==sha256(caller_path.read_bytes()).hexdigest(),'endpoint receipt input pins')
    native=endpoint.native_dual(word);formal=endpoint.caller_dual(caller)
    need(native==saved['native'] and formal==saved['caller'],'complete reverse native and polynomial caller receipts')
    controls={}
    for op in ('QUERY','IDLE_ONE','LAMBDA','HOST2'):
        changed=copy.deepcopy(caller);del changed['events'][next(i for i,e in enumerate(changed['events']) if e[0]==op)]
        controls['delete_'+op]=endpoint.fails(lambda:endpoint.caller_dual(changed))
    changed=copy.deepcopy(caller);i=next(i for i,e in enumerate(changed['events']) if e[0]=='LAMBDA');changed['events'][i][2]*=-1
    controls['flip_lambda']=endpoint.fails(lambda:endpoint.caller_dual(changed))
    changed=copy.deepcopy(caller);changed['diagonal'][0][2]^=1
    controls['wrong_target_mask']=endpoint.fails(lambda:endpoint.caller_dual(changed))
    need(all(controls.values()) and controls==saved['controls'],'six genuine endpoint controls')
    flow=flow_check.verify()
    need(flow==json.loads((HERE/'FLOW-RECEIPT.json').read_text()),'literal word-labelled ambient-cap flow receipt')
    bound=ambient_bounds.verify()
    need(bound==json.loads((HERE/'RESULT.json').read_text())['ambient_majorant'],'independent rational-log inequalities')
    print(json.dumps(dict(native_coefficients=native['endpoint_coefficients'],caller_coefficients=formal['matrix_coefficients'],endpoint_controls=len(controls),literal_flow_cases=flow['cases'],wrong_ambient_rejected=flow['wrong_geometry_control']),sort_keys=True))
    print('PASS_ENDPOINT_AND_AMBIENT_AUDIT')


if __name__=='__main__':main()
