"""Reuse only the previously independent root geometry and price engines."""
import argparse,hashlib,json,sys
from pathlib import Path
from decimal import Decimal,localcontext
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
p.add_argument('--engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
for k in ['history-twelve','fifteen','history-fifteen']:p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();sys.path.insert(0,str(a.engine));from check import replay
from budget import budget,combine,moment
specs=[('history_twelve','f9c1e4518f5dbc79d14eab2be4539ed6a70894938b89c4be34e85e8b05e4d4a8',[63,671,365,63]),('fifteen','ad5ee926df808054a05bff8b2db5f2eb4c70e6e4713f1419fcf02a211eb14f64',[19,426,359,19]),('history_fifteen','a82d3f9283fb770377981b9f20b384639aaf135dbdc0046db4852f7f0df6f46d',[63,673,380,63])]
reports={}
for key,pin,counts in specs:
 data=getattr(a,key).read_bytes();assert hashlib.sha256(data).hexdigest()==pin;w=json.loads(data)
 raw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['source_sha256']
 r=replay(w,json.loads(raw)['native_roots']);assert [r['counts'][k]for k in ['INIT','ADD','MOVE','CLEAR']]==counts
 r['word_sha256']=pin;r['budget']=budget(r['movement_profile'])
 delta=moment(combine((1,{7:222,8:8,1:len(w['targets'])}),(-1,r['movement_profile'])))
 assert delta[0]>0
 with localcontext() as ctx:
  ctx.prec=50
  r['same_S8_direct_control_saving']={'lower':str(Decimal(delta[0].numerator)/delta[0].denominator),'upper':str(Decimal(delta[1].numerator)/delta[1].denominator),'exact':[str(x)for x in delta]}
 reports[key]=r
out={'status':'PASS_ROOT_FORK_HISTORY_WORDS_AND_PRICES','reports':reports,'history_and_visibility_review':'separate independent-C proof and snapshot interpreter','new_complete_kappa':False}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:{'counts':v['counts'],'Q':v['budget']['moment']['display_lower'],'first_even_m':v['budget']['first_positive_even_m']}for k,v in reports.items()}))
