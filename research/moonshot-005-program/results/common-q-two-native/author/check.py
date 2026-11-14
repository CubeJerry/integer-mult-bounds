#!/usr/bin/env python3
"""Complete four-input common-Q control over Q(i)[q,D1,D2,D3]/(q^4-1).
No author checker imported. @CubeJerry/OpenAI.
"""
import argparse,copy,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
def need(x,m):
    if not x:raise ValueError(m)
def cmul(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def plus(a,b):
    r=a.copy()
    for k,(x,y)in b.items():
        u,v=r.get(k,(F(0),F(0)));r[k]=(u+x,v+y)
        if r[k]==(0,0):del r[k]
    return r
def times(a,c=(F(1),F(0)),q=0,stage=None):
    r={}
    for (i,e,d1,d2,d3),v in a.items():
        ds=[d1,d2,d3]
        if stage is not None:ds[stage-1]+=1
        k=(i,(e+q)%4,*ds);z=cmul(c,v)
        if z!=(0,0):r[k]=z
    return r
def replay(program):
    rows=[{(i,0,0,0,0):(F(1),F(0))}for i in range(4)];counts=Counter();stages=[]
    for o in program:
        tag=o[0];counts[tag]+=1
        if tag=='LAMBDA':
            _,i,s=o;need(s in(-1,1),'lambda unit orientation');rows[i]=plus(times(rows[i],(F(1,2),F(s,2))),times(rows[i],(F(1,2),F(-s,2)),q=2))
        elif tag=='SCALE':_,i,c=o;need(F(c)!=0,'invertible scalar');rows[i]=times(rows[i],(F(c),F(0)))
        elif tag=='SWAP':_,i,j=o;need(i!=j,'nontrivial swap');rows[i],rows[j]=rows[j],rows[i]
        elif tag=='QUERY':_,i,j,e=o;need(i!=j and e in(-1,1),'literal nonself rank-one query');rows[i]=plus(rows[i],times(rows[j],q=e))
        elif tag=='HOST2':
            _,s,args=o;need(sorted(args)==list(range(4))and s in(1,2,3),'all four independent fields active in one true stage');x,y,u,v=args;old=copy.deepcopy(rows)
            rows[x]=times(old[x],stage=s);rows[y]=times(plus(old[y],times(old[x],q=-1)),stage=s)
            rows[u]=times(plus(old[u],times(old[v],c=(F(-1),F(0)),q=1)),stage=s);rows[v]=times(old[v],stage=s);stages.append(s)
        else:raise ValueError('unsupported or unpriced instruction '+tag)
    return rows,dict(counts),stages

def lower_native(stage):
    return [['LAMBDA',1,-1],['LAMBDA',2,-1],['SCALE',3,'-1'],['HOST2',stage,[0,1,3,2]],['SCALE',3,'-1'],['LAMBDA',1,1],['LAMBDA',2,1]]
def upper_native(stage):
    return [['LAMBDA',0,-1],['LAMBDA',3,-1],['SCALE',0,'-1'],['HOST2',stage,[1,0,2,3]],['SCALE',0,'-1'],['LAMBDA',0,1],['LAMBDA',3,1]]
def final():return [['SWAP',0,1],['SCALE',1,'-1'],['SWAP',2,3],['SCALE',3,'-1']]+[['LAMBDA',i,-1]for i in range(4)]
def words():
    pre=lower_native(1)+upper_native(2)
    queries=[['LAMBDA',0,1],['QUERY',1,0,-1],['LAMBDA',0,-1],['LAMBDA',2,1],['QUERY',3,2,-1],['LAMBDA',2,-1]]
    return {'two_native_two_query':pre+queries+final(),'three_native_zero_query':pre+lower_native(3)+final()}
def expected(stages):
    ds=tuple(stages.count(j)for j in (1,2,3));return[{(i,3,*ds):(F(1),F(0))}for i in range(4)]

def serialize(rows):return[[{'input':k[0],'q_power':k[1],'D_powers':list(k[2:]),'coefficient':[str(v[0]),str(v[1])]}for k,v in sorted(row.items())]for row in rows]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path(__file__).parent);p.add_argument('--receipt',default='RESULT.json');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True);out={}
    W=words()
    for name,program in W.items():
        rows,counts,stages=replay(program);need(rows==expected(stages),'all four independent inputs exact '+name)
        need(stages==([1,2]if name.startswith('two')else[1,2,3]),'all body stages retained once')
        need(counts.get('QUERY',0)==(2 if name.startswith('two') else 0),'complete paid query census')
        word={'schema':'common-Q-four-role-positive-control-v1','roles':4,'all_inputs_arbitrary':True,'coefficient_ring':'Q(i)[q,D1,D2,D3]/(q^4-1)','ordinary_lambda_service_retained':True,'no_R0_admission':True,'program':program}
        (a.output/(name+'.json')).write_text(json.dumps(word,sort_keys=True,indent=2)+'\n')
        out[name]={'instructions':len(program),'counts':counts,'native_stages':stages,'all_input_columns':4,'outputs':serialize(rows),'idle_calls':0,'new_helper_roles':0}
    base=W['two_native_two_query'];controls=[]
    for label in ['omit_one_query','wrong_second_native_sign','omit_query_source_restoration','wrong_query_orientation','repeat_fresh_stage','self_query']:
        bad=copy.deepcopy(base)
        if label=='omit_one_query':bad.pop(next(i for i,o in enumerate(bad)if o[0]=='QUERY'))
        elif label=='wrong_second_native_sign':next(o for o in bad[7:14]if o[0]=='SCALE')[2]='1'
        elif label=='omit_query_source_restoration':bad.pop(next(i for i,o in enumerate(bad)if o[0]=='QUERY')+1)
        elif label=='wrong_query_orientation':next(o for o in bad if o[0]=='QUERY')[3]=1
        elif label=='repeat_fresh_stage':next(o for o in bad if o[0]=='HOST2'and o[1]==2)[1]=1
        else:o=next(o for o in bad if o[0]=='QUERY');o[2]=o[1]
        try:rejected=replay(bad)[0]!=expected([1,2])
        except ValueError:rejected=True
        need(rejected,'negative control '+label);controls.append(label)
    receipt={'status':'PASS_FULL_FOUR_INPUT_COMMON_Q_CALLERS','constructions':out,'negative_controls':controls,'scope':'Exact formal common-Q identity with retained ordinary lambda service. All D variables remain unrestricted; no D inverse, idle, helper or input promise. Actual R0 variable port couplings are not admitted. No new kappa.'}
    (a.output/a.receipt).write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'counts':{n:r['counts']for n,r in out.items()},'controls':controls}))
if __name__=='__main__':main()
