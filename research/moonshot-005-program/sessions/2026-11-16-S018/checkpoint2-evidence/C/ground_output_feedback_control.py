#!/usr/bin/env python3
"""Positive physical normalization control with transient Y-to-X feedback."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
from ground_output_normalization import build_control, evaluate, normalize
from release_projection import N, replay, require
from price_projection import moment, record


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    p=a.repo/'research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json'
    raw=p.read_bytes()
    require(hashlib.sha256(raw).hexdigest()=='27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd','base pin')
    base=json.loads(raw)
    require(hashlib.sha256((a.repo/base['source_path']).read_bytes()).hexdigest()==base['source_sha256'],'native source pin')
    un,cut,names=build_control(base)
    k=un['operations'].index(['ADD','X0','Y2'])+1
    feedback=[['ADD','Y2','X0'],['ADD','X0','Y3'],['ADD','Y2','X0']]
    un['operations'][k:k]=feedback
    _,_,trace,_=evaluate(un)
    require(trace[k+1][0]['X0']==1<<(N+2),'actual intermediate X0 is arbitrary y2')
    require(trace[k+3][0]['X0']==1,'X0 physically restored before departure')
    word,before=normalize(un,cut,names)
    after,_,_=replay(word)
    _,_,normalized_trace,_=evaluate(word)
    nk=word['operations'].index(['ADD','Y2','X0'])
    intermediate=normalized_trace[nk+1][0]['X0']
    require(intermediate>>N != 0,'normalized physical X0 actually contains y')
    require(normalized_trace[nk+3][0]['X0']==1,'normalized physical X0 restoration')
    require(before['movement_profile']==after['movement_profile'],'no normalization moves')
    require([int(word['ground_normalization']['homogeneous_Y_rows_hex'][i],16)for i in [2,3,4]]==
        [(1<<2)^(1<<3),1<<3,(1<<3)^(1<<4)],'actual Y feedback transfer')
    controls=[]
    for label,event in [('omit first feedback',k),('omit final restoration',k+2)]:
        bad=copy.deepcopy(un);bad['operations'].pop(event)
        try:normalize(bad,cut,names)
        except ValueError as e:controls.append({'label':label,'rejected':True,'reason':str(e)})
        else:raise ValueError(('accepted feedback omission',label))
    result={'status':'PASS_GROUND_NORMALIZATION_WITH_ACTUAL_Y_TO_X_FEEDBACK',
        'source_sha256':base['source_sha256'],'base_sha256':hashlib.sha256(raw).hexdigest(),
        'unnormalized_intermediate_X0':'y2',
        'normalized_intermediate_X0_hex':hex(intermediate),
        'normalized_intermediate_X0_has_arbitrary_y':True,
        'restored_X0_before_departure':'x0',
        'actual_feedback_operations':feedback,'before':before,'after':after,
        'all222_endpoint_columns':True,
        'ground_source_ADDs':len(word['ground_normalization']['preload_operations']),
        'ground_inverse_ADDs':len(word['ground_normalization']['inverse_operations']),
        'moment':record(moment(after['movement_profile'])),'controls':controls,
        'scope':'Positive physical test of the general final-block hypothesis with actual transient Y-to-X feedback. No new output count, source dimension, supplier or kappa.'}
    a.out.mkdir(parents=True,exist_ok=True)
    for name,obj in [('WORD',word),('UNNORMALIZED-WORD',un)]:
        b=(json.dumps(obj,indent=2)+'\n').encode();(a.out/(name+'.json')).write_bytes(b)
        result[name.lower().replace('-','_')+'_sha256']=hashlib.sha256(b).hexdigest()
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['status','after','ground_inverse_ADDs','word_sha256']},indent=2))


if __name__=='__main__':main()
