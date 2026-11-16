#!/usr/bin/env python3
"""Independent endpoint-only review of the reduced41 word."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,importlib.util,json
BASE='07ed37cf9dfa1da24d3518e25e46d7b29141582f71f32da1191f13fbc9b1971f'
WORD='b18c138efaf2d771197c46ef3ae2a5fc312c322694ef020e41cace70d7662e11'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
 p=argparse.ArgumentParser()
 for name in ['repo','base','word','author-price','engine','price-engine','out']:p.add_argument('--'+name,type=Path,required=True)
 a=p.parse_args();assert sha(a.base)==BASE and sha(a.word)==WORD;old=json.loads(a.base.read_text());w=json.loads(a.word.read_text());assert w['base_word_sha256']==BASE and w['targets']==old['targets'] and w['source_sha256']==old['source_sha256'];src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine,'e');price=load(a.price_engine,'price');C,H,before=e.replay(old,R);C,H,after=e.replay(w,R)
 assert after['counts']=={'INIT':118,'ADD':798,'MOVE':452,'CLEAR':118}and after['dirty_CLEAR']==118
 assert not any(k in w for k in ['milestones','source_cut','seed_rows_hex','history_cache_metadata'])
 deleted=sorted({o[1]for o in old['operations']if o[0]=='INIT'}-{o[1]for o in w['operations']if o[0]=='INIT'});assert len(deleted)==11
 delta={d:after['movement_profile'].get(d,0)-before['movement_profile'].get(d,0)for d in set(after['movement_profile'])|set(before['movement_profile'])};delta={d:n for d,n in delta.items()if n};assert delta=={1:-6,2:-2,5:-5,7:5}
 Q=price.moment(after['movement_profile']);B={127:37,64:74,1:-74}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
 limit=tuple(x/6 for x in price.moment(B));room=(limit[0]-Q[1],limit[1]-Q[0]);ap=json.loads(a.author_price.read_text())
 for label,interval in [('moment',Q),('limiting_allowance',limit),('limiting_room',room)]:assert interval[0]<=Fraction(ap[label]['lower_fraction'])<=Fraction(ap[label]['upper_fraction'])<=interval[1]
 essential=[['ADD','X40','RAW40'],['ADD','P4','P4_RET'],['MOVE','Y2','L29'],['ADD','RAW29','Y2'],['ADD','P5_RAW48','Y45'],['CLEAR','P5_RET']];controls=[]
 for op in essential:
  assert op in w['operations'];bad=copy.deepcopy(w);bad['operations'].remove(op)
  try:e.replay(bad,R)
  except (AssertionError,KeyError)as ex:controls.append({'removed':op,'rejected':str(ex)})
  else:raise AssertionError(('accepted omitted essential operation',op))
 out={'status':'PASS_INDEPENDENT_REDUCED41_ENDPOINT_ONLY','base_word_sha256':BASE,'word_sha256':WORD,'native_source_sha256':w['source_sha256'],'before':before,'after':after,'deleted_owners':deleted,'exact_profile_difference':delta,'price':{'method':'Independent exact200th roots at scale10^32','moment':price.display(Q),'limiting_room':price.display(room),'difference_from_parent':price.display(price.moment(delta))},'author_price_intervals_contained':True,'semantic_controls_without_invoice_or_source_metadata':controls,'source_metadata_deliberately_not_inherited':True,'not_claimed':['preservation of old principal or all-record histories','old source-cut or common-space ranks','source availability of deleted owners','old fixed-information closure certificates'],'scope':'Formal all222 endpoint/geometry/ownership and partial movement invoice only. No complete supplier, new kappa or foundational discharge.'};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k]for k in ['status','after','deleted_owners','price']}))
if __name__=='__main__':main()
