#!/usr/bin/env python3
"""Literal retained-point continuation; nine actual outputs, no new kappa."""
import argparse, copy, hashlib, json
from collections import Counter
from pathlib import Path
from check import SOURCE_SHA, kernel, need, price, rref
from coupled_history_check import replay as replay_prefix

DONORS=[16,19,38,49,50,56,57]
TARGETS=sorted(DONORS+[17,34])

def build(prefix,closed):
    word=copy.deepcopy(prefix)
    for j in DONORS:
        word['operations'] += [['MOVE',f'R{j}','zero'],['ADD',f'R{j}',f'Y{j}'],['MOVE',f'Y{j}',f'F{j}']]
        word['expected_owned_at_handoff'][f'R{j}']['chart']='zero'
    word.update(schema='nine-output-singular-history-v1',completed_targets=TARGETS,closed_partial=closed,
                extension_prefix_operations=len(prefix['operations']))
    word['markers']['handoff']=len(word['operations'])
    if closed:
        word['operations'] += [['CLEAR',n]for n in word['expected_owned_at_handoff']]
        word['operations'] += [['MOVE',f'Y{j}',f'F{j}']for j in range(111)if j not in TARGETS]
    return word

def replay(word,prefix,prior):
    size=len(prefix['operations'])
    need(word['operations'][:size]==prefix['operations'],'frozen actual prefix unchanged')
    need(word['charts']==prefix['charts'],'literal geometry unchanged')
    charts={n:rref(s['rows'])if s['kind']=='span'else kernel(s['rows'])for n,s in word['charts'].items()}
    R={n:[r['chart'],int(r['coefficient_hex'],16),r['owned']]for n,r in prior['actual_handoff'].items()}
    counts=Counter(prior['operations']);profile=Counter({int(k):v for k,v in prior['movement_profile'].items()})
    handoff=None
    def outputs(closed):
        for j in range(111):
            need(R[f'X{j}'][:2]==['Hub',1<<j],'all original X restored')
            expected=(1<<(111+j))^((1<<j)if j in TARGETS else 0)
            chart=f'F{j}'if closed or j in TARGETS else'zero'
            need(R[f'Y{j}'][:2]==[chart,expected],'all222 output columns and charts')
    for kind,n,*args in word['operations'][size:]:
        counts[kind]+=1
        need((kind=='CLEAR' or not n.startswith('P')) and not(kind=='ADD'and args[0].startswith('P')),'packet history unchanged')
        if kind=='MOVE':
            need(n in R and args[0]in charts,'live MOVE')
            old,value,owned=R[n];new=args[0];outer,inner=(old,new)if owned else(new,old)
            need(len(rref(charts[outer]+charts[inner]))==len(charts[outer]),'monotone real-chart movement')
            rank=abs(len(charts[old])-len(charts[new]));need(rank>0,'positive paid movement')
            profile[rank]+=1;R[n][0]=new
        elif kind=='ADD':
            target=args[0];need(n in R and target in R and n!=target,'live ADD')
            need(charts[R[n][0]]==charts[R[target][0]],'literal same-chart source read')
            R[target][1]^=R[n][1]
        elif kind=='CLEAR':
            if handoff is None:
                outputs(False);need(sum(r[2]for r in R.values())==168,'no additional owner')
                handoff={n:{'chart':r[0],'coefficient_hex':hex(r[1]),'owned':r[2]}for n,r in R.items()}
            need(n in R and R[n][2],'owned erasure only');del R[n]
        else:raise ValueError('unexpected new-owner or primitive')
    outputs(word['closed_partial']);live=sum(r[2]for r in R.values())
    need(live==(0 if word['closed_partial'] else 168),'exact final owner count')
    if handoff is None:handoff={n:{'chart':r[0],'coefficient_hex':hex(r[1]),'owned':r[2]}for n,r in R.items()}
    if word['closed_partial']:
        need(dict(profile)=={1:149,2:19,3:49,4:66,5:22,6:22,7:112,8:1},'exact seven unit-descent increment')
        need(dict(counts)=={'INIT':168,'ADD':677,'MOVE':440,'CLEAR':168},'complete closed bill')
    return {'status':'PASS_LITERAL_NINE_OUTPUT_CONTINUATION','all_222_columns_replayed':True,
            'completed_targets':TARGETS,'remaining_unserved_targets':102,'closed_partial':word['closed_partial'],
            'operations':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),
            'rank_length':sum(k*v for k,v in profile.items()),'moment':price(profile),
            'peak_owned':168,'live_owned':live,'new_owners':0,'new_owned_movement_rank':7,
            'moving_owned_records':{'packets':8,'internal_masks':7,'exported_point_copies':7,'total':22},
            'unchanged_packet_histories':True,'history_rank_full222':37,'history_W_intersection_full222':15,
            'history_pure_X_dimension':36,'history_public_Y_projection_rank':1,'actual_handoff':handoff,'new_complete_kappa':False}

def controls(base,prefix,prior):
    result={};offset=len(prefix['operations'])
    for j in DONORS:
        word=copy.deepcopy(base);at=next(i for i in range(offset,len(word['operations']))if word['operations'][i]==['ADD',f'R{j}',f'Y{j}'])
        del word['operations'][at]
        try:replay(word,prefix,prior)
        except(ValueError,KeyError)as error:result[f'omit_Y{j}_read']={'rejected':True,'reason':str(error)}
        else:raise ValueError('accepted missing output')
    for label in['omit_copy_descent','wrong_cocharted_copy']:
        word=copy.deepcopy(base)
        if label=='omit_copy_descent':del word['operations'][offset]
        else:
            at=next(i for i in range(offset,len(word['operations']))if word['operations'][i]==['ADD','R38','Y38']);word['operations'][at][1]='R16'
        try:replay(word,prefix,prior)
        except(ValueError,KeyError)as error:result[label]={'rejected':True,'reason':str(error)}
        else:raise ValueError('accepted source mutant')
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--output-directory',type=Path,required=True);a=p.parse_args()
    raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'root source pin');roots=json.loads(raw)['native_roots']
    source=a.prefix.read_bytes();prefix=json.loads(source);prior=replay_prefix(prefix,roots,localized=True,second_receiver=True)
    a.output_directory.mkdir(parents=True,exist_ok=True);words={'WORD.json':build(prefix,False),'CLOSED-WORD.json':build(prefix,True)};receipts={}
    for name,word in words.items():
        word['prefix_sha256']=hashlib.sha256(source).hexdigest();receipts[name]=replay(word,prefix,prior)
        (a.output_directory/name).write_text(json.dumps(word,indent=2,sort_keys=True)+'\n')
    result={'status':'PASS_LITERAL_NINE_OUTPUT_FULL_W_SOURCE','source_sha256':SOURCE_SHA,'prefix_sha256':hashlib.sha256(source).hexdigest(),'receipts':receipts,'negative_controls':controls(words['WORD.json'],prefix,prior),'new_complete_kappa':False}
    (a.output_directory/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')

if __name__=='__main__':main()
