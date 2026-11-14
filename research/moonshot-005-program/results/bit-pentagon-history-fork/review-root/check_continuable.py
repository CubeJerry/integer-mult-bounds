#!/usr/bin/env python3
"""Review the live-source companion using the separate root replay engine."""
import argparse,gzip,hashlib,json
from pathlib import Path
from check import IDS,PIN,need,replay
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');n=json.loads(gzip.decompress(raw));load=lambda name:json.loads(gzip.decompress((a.package/name).read_bytes()))
    core=load('PREFIX.json.gz');live=load('CONTINUABLE-PREFIX.json.gz');closed=load('CONTINUABLE-CLOSED-PARTIAL.json.gz');untouched=set(range(111))-set(IDS)
    filtered=[e for e in core['program']if not(e[0]=='MOVE'and e[1]in untouched)]
    need(live['program']==filtered and len(core['program'])-len(filtered)==106,'only106 unused original ascents omitted')
    need(all(not(e[0]=='ADD'and any(r in untouched for r in e[1:3]))for e in core['program']),'omitted sources never read by module')
    old,ol,_=replay(core);r,l,b=replay(live);rr,ll,bb=replay(closed)
    for i in range(111):
        need(r[i]==rr[i]=={i}and l[i]==(n['start'][i]if i in untouched else n['final'][i]),'live actual X interface')
        need(ll[i]==n['final'][i],'closed X endpoint')
        target={111+i}^({i}if i in IDS else set());need(r[111+i]==rr[111+i]==target,'five exact arbitrary Y targets')
        need(l[111+i]==(n['start'][111+i]if i in untouched else n['final'][111+i])and ll[111+i]==n['final'][111+i],'Y charts')
    need(all(r[i]==old[i]and l[i]==ol[i]for i in range(222,229)),'all retained histories unchanged')
    need(b['operations']=={'INIT':7,'MOVE':23,'ADD':32}and bb['movement']=={1:9,2:2,5:2,6:7,7:215},'actual companion invoice')
    need(set(rr)==set(range(222))and bb['dirty_clears']==7,'owned closure')
    need(all(not(row&untouched)for i,row in old.items()if core['frames'][str(ol[i])]['dim']<8),'old proper-region106-column observation is zero')
    need(all(live['frames'][str(l[i])]['dim']==1 and r[i]=={i}for i in untouched),'live proper region has106 independent original coordinates')
    d={'status':'PASS_INDEPENDENT_CONTINUABLE_PENTAGON_SOURCE','source_sha256':PIN,'prefix_sha256':hashlib.sha256((a.package/'CONTINUABLE-PREFIX.json.gz').read_bytes()).hexdigest(),'closure_sha256':hashlib.sha256((a.package/'CONTINUABLE-CLOSED-PARTIAL.json.gz').read_bytes()).hexdigest(),'unserved_originals_retained_on_source_lines':106,'prefix_operations':b['operations'],'closed_profile':bb['movement'],'old_all_hub_future_entry_dimension_lower_bound':'106V','live_variant_has_no_such106V_deficit':True,'all_remaining_acquisition_paid_separately':True,'no_new_kappa':True}
    a.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
if __name__=='__main__':main()
