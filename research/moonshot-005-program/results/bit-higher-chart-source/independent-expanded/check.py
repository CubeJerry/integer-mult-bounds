#!/usr/bin/env python3
"""Independent72-parameter acquisition-family reconstruction and symbolic proof."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
BASE='5566738ce7b2706c0094654fce0e4c1c438e82395dee2e6885ef917f2d4498f3'
WORD='6a1eef8ef1f620914b3f014c9ba129bbe389c6fd5a010872f3e5cca88f5cb52f'
def load(path,name):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def extra_specs(base):
    out=[]
    for group,(z,ch,target)in enumerate([(3,'C1',4),(4,'C4',74),(5,'C3',78),(6,'Extra6',None)],6):
        roles=next(q['roles']for q in base['cache_metadata']if q['chart']==ch)if group<9 else base['history_extra_query_roles']
        out.append({'group':group,'packet':z,'chart':ch,'roles':sorted(roles),'targets':[target]if target is not None else[],
                    'owner':f'PAIR{z}'if group<9 else'EXTRA_AFF','retention':f'ZFIRST{z}'if group<9 else'P6'})
    return out
def extra_rebuild(base,selected,prior_captures):
    ss=[s for s in extra_specs(base)if selected[s['group']]];ops=[['INIT',s['owner'],s['chart']]for s in ss];marks={};mapping={};captures={};seen=set();queries=set()
    for step,o in enumerate(base['operations'],1):
        op,name,*args=o
        if op=='MOVE'and name.startswith('Y'):
            i=int(name[1:])
            for s in ss:
                if i in s['targets']and args[0]==f'F{i}':ops +=[['MOVE',name,s['chart']],['ADD',s['owner'],name]]
        ops.append(o)
        if step in prior_captures:captures[len(ops)]=prior_captures[step]
        if op=='MOVE':
            for s in ss:
                if args[0]!=s['chart']:continue
                g=s['group']
                if name.startswith('X'):
                    j=int(name[1:])
                    if j in selected[g]and(g,j)not in seen:seen.add((g,j));ops.append(['ADD',name,s['owner']]);captures[len(ops)]=(g,j)
                if name==f"P{s['packet']}"and g not in queries:queries.add(g);ops.append(['ADD',s['owner'],name])
        mapping[step]=len(ops)
    ops +=[['CLEAR',s['owner']]for s in ss];assert seen=={(g,j)for g in range(6,10)for j in selected[g]}
    out=copy.deepcopy(base);out['operations']=ops;out['milestones']={k:mapping[v]for k,v in base['milestones'].items()};out['seed_rows_hex'][6]=hex(int(out['seed_rows_hex'][6],16)^sum(1<<j for j in selected[9]));return out,captures
def symbolic(w,base_run,e,captures,ss):
    C=base_run['C'];v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owners=set();born=set();directions={}
    keys=sorted(captures.values());assert len(keys)==len(set(keys))==72;idx={key:222+k for k,key in enumerate(keys)};masks={s['group']:sum(1<<idx[s['group'],j]for j in s['roles'])for s in ss};acq=[];cut=None
    for step,o in enumerate(w['operations'],1):
        op,name,*q=o
        if op=='INIT':assert name not in v and name not in born;owners.add(name);born.add(name);at[name]=q[0];v[name]=0
        elif op=='ADD':
            dest=q[0];assert C[at[name]]==C[at[dest]]
            if step in captures:
                g,j=captures[step];s=ss[g];assert name==f'X{j}'and dest==s['owner']and at[name]==s['chart']and v[name]==1<<j
                v[dest]^=1<<idx[g,j];acq.append({'group':g,'original':j,'capture_step':step,'chart':s['chart'],'formal_column':idx[g,j]})
            else:v[dest]^=v[name]
        elif op=='MOVE':
            dest=q[0];key=(at[name],dest,name in owners)
            if key not in directions:directions[key]=e.contained(C[dest],C[at[name]])if name in owners else e.contained(C[at[name]],C[dest])
            assert directions[key]and len(C[dest])!=len(C[at[name]]);at[name]=dest
        elif op=='CLEAR':assert name in owners;owners.remove(name);del at[name],v[name]
        else:raise AssertionError(op)
        if step==w['milestones']['seed8_before_Y']:
            old=base_run['cuts']['seed']['values'];oldat=base_run['cuts']['seed']['charts'];shift={}
            for s in ss:shift[s['retention']]=shift.get(s['retention'],0)^masks[s['group']]
            for name,row in old.items():assert v[name]==row^shift.get(name,0)and at[name]==oldat[name],name
            for s in ss:assert v[s['owner']]==masks[s['group']]and at[s['owner']]==s['chart']
            cut={'changed_old_fields':[{ 'name':name,'base_row_hex':hex(old[name]),'formal_shift_hex':hex(mask)}for name,mask in shift.items()],
                 'all_other_old_fields_and_positions_unchanged':True}
    assert cut and len(acq)==72 and not owners
    for i in range(111):assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub';assert v[f'Y{i}']==((1<<(111+i))^((1<<i)if i in w['targets']else 0))and at[f'Y{i}']==f'F{i}'
    return {'formal_columns':294,'original_columns':222,'parameter_product_columns':72,'actual_captures':acq,**cut,'all72_parameter_columns_absent_from_final_X_Y':True}
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    br=a.base.read_bytes();wr=a.word.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE and hashlib.sha256(wr).hexdigest()==WORD;base=json.loads(br);w=json.loads(wr)
    root=Path(__file__).with_name('retained');e=load(root/'source_history_engine.py','independent_chart_engine');pr=load(root/'private_review_engine.py','independent_private_rebuild')
    source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots'];S0=[int(x,16)for x in base['seed_rows_hex']];S=[int(x,16)for x in w['seed_rows_hex']]
    base_run=e.replay(base,R,S0,15,False);run=e.replay(w,R,S,15,False)
    selected=[[]for _ in range(10)]
    for s in w['affine_injections']:selected[s['packet']]=s['roles']
    for s in w['higher_shared_injections']:selected[s['parameter_group']]=s['roles']
    pw,pc=pr.rebuild(base,selected[:6]);rebuilt,cc=extra_rebuild(pw,selected,pc);assert rebuilt['operations']==w['operations']and rebuilt['milestones']==w['milestones']and rebuilt['seed_rows_hex']==w['seed_rows_hex']
    ss=[dict(s,group=z)for z,s in enumerate(pr.specs(base))]+extra_specs(base);fullsel=[s['roles']for s in ss];pw,pc=pr.rebuild(base,fullsel[:6]);full,fc=extra_rebuild(pw,fullsel,pc);sy=symbolic(full,base_run,e,fc,ss)
    rank=lambda rows:len(e.basis(rows));E=[1<<j for j in base['history_extra_query_roles']];assert rank(S0)==8 and rank(E)==6 and rank(S0+E)==14
    assert not any(o[0]=='ADD'and o[1]=='P6'and o[2].startswith('Y')for o in base['operations'])
    assert run['count']=={'INIT':108,'ADD':877,'MOVE':430,'CLEAR':108}and run['profile']=={1:106,2:64,3:56,4:13,5:71,6:23,7:96,8:1}and run['dirty_CLEAR']==108
    tests=[('omit_pair3_injection',['ADD','PAIR3','P3']),('omit_pair4_injection',['ADD','PAIR4','P4']),('omit_pair5_injection',['ADD','PAIR5','P5']),('omit_Y4_pair_correction',['ADD','PAIR3','Y4']),('omit_Y74_pair_correction',['ADD','PAIR4','Y74']),('omit_Y78_pair_correction',['ADD','PAIR5','Y78']),('omit_actual_C1_visit',['MOVE','Y4','C1']),('omit_EXTRA_retirement',['CLEAR','EXTRA_AFF'])];rejected=[]
    for name,op in tests:
        m=copy.deepcopy(w);ix=m['operations'].index(op);m['operations'].pop(ix);m['milestones']={k:-1 for k in w['milestones']};m.pop('source_cut',None)
        try:e.replay(m,R,S,15,False)
        except AssertionError:rejected.append(name)
        else:raise AssertionError('accepted mutant '+name)
    m=copy.deepcopy(w);ix=m['operations'].index(['ADD','EXTRA_AFF','P6']);m['operations'].pop(ix);m['milestones']={k:v-(v>ix)for k,v in w['milestones'].items()}
    try:e.replay(m,R,S,15,False)
    except AssertionError:rejected.append('omit_EXTRA_query_fails_new_terminal_contract')
    else:raise AssertionError('oldP6 incorrectly accepted as newP6')
    r={'status':'PASS_INDEPENDENT_EXPANDED_AFFINE_72_FAMILY','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],
       'counts':run['count'],'profile':run['profile'],'dirty_CLEAR':108,'targets':w['targets'],'concrete_parameters':selected,
       'independent_operation_rebuild_matches':True,'symbolic_family':sy,
       'terminal_rank_certificate':{'base_rank':8,'Extra6_raw_rank':6,'joint_rank':14,'intersection_rank':0,'all_Extra6_binary_shifts_preserve_eight_terminal_rank':True},
       'P6_new_value_is_old_value_plus_actual_Extra6_row':True,'old_P6_value_not_also_granted':True,
       'general_invoice':{'INIT_CLEAR':'102+a0+a1+c+e','ADD':'858+s+3*a0+2*a1+2*c+e','MOVE':'425+2*a0+c','moment_increment':'a0*(4-2[2])+c*(2-[2])','definitions':'a0,h0 nonempty private groups; a1,h1 nonempty private groups; c,nonempty pair groups; e,nonempty Extra6 group; s,totalselectedcaptures'},
       'semantic_negative_controls':rejected,'scope':'Actual72-parameter acquisition family with30unchanged endpoints, changedP6groundcode and exactphysicalinvoice. No complete supplier or new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(a.out/'SYMBOLIC-TEMPLATE.json').write_text(json.dumps({'operations':full['operations'],'capture_map':{str(k):list(v)for k,v in fc.items()}},indent=2)+'\n');print(json.dumps({k:r[k]for k in ['status','counts','profile','terminal_rank_certificate','semantic_negative_controls']}))
if __name__=='__main__':main()
