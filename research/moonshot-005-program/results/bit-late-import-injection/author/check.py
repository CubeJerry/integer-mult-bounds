#!/usr/bin/env python3
"""Exact projection hypotheses for late-import injection rigidity."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,importlib.util,json
WITNESSES={8:(43,29,45),9:(41,42,48),36:(43,29,48)}
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 p=argparse.ArgumentParser()
 for n in ['repo','engine','history-engine','out']:p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--word',action='append',nargs=2,metavar=('SHA256','PATH'),required=True)
 a=p.parse_args();e=load(a.engine,'e');h=load(a.history_engine,'h');reports=[]
 for pin,path in a.word:
  raw=Path(path).read_bytes();assert hashlib.sha256(raw).hexdigest()==pin;w=json.loads(raw)
  src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots']
  C,H,rep=e.replay(w,R);PH,events=h.parametrized_history(w,C);maskX=(1<<111)-1
  fixed=[(s,n,c,r&maskX)for s,n,c,r in H];expected=[(s,n,c,r)for s,n,c,r,t in PH]
  for event in reversed(events):expected.remove((event['before_step'],event['principal'],'M1',int(event['pre_injection_row_hex'],16)))
  assert expected==fixed,'Zero-load history disagrees with full replay'
  cases=[]
  for q,D in WITNESSES.items():
   assert set(D)<=set(w['targets']);J=(*D,q);mask=sum(1<<j for j in J);checked=[]
   for i in J:
    tags=Counter();count=0
    for step,n,c,r,t in PH:
     if not e.sub(C[c],C[f'F{i}']):continue
     expected=sum(1<<D[k]for k in range(3)if t>>k&1)
     assert r&mask==expected,('projection failure',pin,q,D,i,step,n,c,hex(r&mask),t)
     tags[t]+=1;count+=1
    assert all(sum(x*y for x,y in zip(R[i],R[j]))!=0 for j in J)
    checked.append({'receiver':i,'actual_history_observations_checked':count,'tag_counts':dict(sorted(tags.items()))})
   for k,P in enumerate(['P3','P4','P5']):assert any(n==P and c=='zero'and t==1<<k and r&mask==1<<D[k]for _,n,c,r,t in PH)
   cases.append({'import_coordinate':q,'old_demand_tuple_in_P3_P4_P5_order':list(D),'slice_coordinates':list(J),'receiver_checks':checked,'fixed_untagged_observations_all_zero':True,'every_tagged_observation_is_exact_channel_combination':True,'all_three_common_channels_present':True,'new_common_raw_import_or_threatened_old_demand_breaks_hypothesis':bool((1<<q)&mask and (1<<D[0])&mask)})
  reports.append({'word_sha256':pin,'native_source_sha256':w['source_sha256'],'original_targets':w['targets'],'all222_base_replay':rep,'injection_sites':events,'witnesses':cases})
 out={'status':'PASS_LATE_IMPORT_INJECTION_RIGIDITY_HYPOTHESES','checked_words':reports,'conclusion':'Preserving all old targets forces source-only payload additions to be constant in imports8,9,36. Homogeneous linear and zero-preserving additive payloads must vanish.','scope':'Fixed source/record routes and induced histories, arbitrary local decoding, causal native decoded-point feedback. Source-wide substitutions, new lower deliveries, and unconditionally granting threatened old demands are excluded. No movement lower bound.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'checked_word_count':len(reports),'witness_count':3*len(reports)}))
if __name__=='__main__':main()
