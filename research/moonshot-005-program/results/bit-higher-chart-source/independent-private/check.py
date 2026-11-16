#!/usr/bin/env python3
"""Independent rebuild and symbolic39-parameter audit of higher private acquisition."""
import argparse,copy,hashlib,importlib.util,json
from collections import Counter
from pathlib import Path
BASE='5566738ce7b2706c0094654fce0e4c1c438e82395dee2e6885ef917f2d4498f3'
WORD='7c5165a225e70e74181ac01c76dcde156c724aeb1e708309b146b7f174be723c'

def specs(base):
    out=[]
    for z in range(6):
        if z<3:
            f=base['forks'][z];i,q=[3,76,80][z],[21,64,65][z];chart=f'D{i}_{q}';roles=f['group'];targets=[i,q];ret=f'KEEP_C{z}'
        else:
            i=[4,74,78][z-3];chart=f'F{i}';roles=base['h1_private_roles'][str(i)];targets=[i];ret=f'ZFIRST{z}'
        out.append({'packet':z,'chart':chart,'roles':sorted(roles),'targets':targets,'owner':f'AFF{z}','retention':ret})
    return out

def rebuild(base,selected):
    # Independently derive every edit from pinned source events. No author
    # builder is imported, and the source field must be raw at each capture.
    ss=[s for s in specs(base)if selected[s['packet']]];ops=[['INIT',s['owner'],s['chart']]for s in ss];marks={};captures={};seen=set();queries=set();corrections=set()
    for step,op in enumerate(base['operations'],1):
        code,name,*args=op
        if code=='MOVE'and name.startswith('Y'):
            i=int(name[1:])
            for s in ss:
                if s['packet']<3 and i in s['targets']and args[0]==f'F{i}':
                    ops +=[['MOVE',name,s['chart']],['ADD',s['owner'],name]];corrections.add((s['packet'],i))
        ops.append(op)
        if code=='MOVE':
            for s in ss:
                z=s['packet']
                if args[0]!=s['chart']:continue
                if name.startswith('X'):
                    j=int(name[1:])
                    if j in selected[z]and(z,j)not in seen:
                        seen.add((z,j));ops.append(['ADD',name,s['owner']]);captures[len(ops)]=(z,j)
                if name==f'P{z}'and z not in queries:queries.add(z);ops.append(['ADD',s['owner'],name])
                if z>=3 and name.startswith('Y')and int(name[1:])in s['targets']:
                    ops.append(['ADD',s['owner'],name]);corrections.add((z,int(name[1:])))
        for mark,index in base['milestones'].items():
            if index==step:marks[mark]=len(ops)
    ops +=[['CLEAR',s['owner']]for s in ss]
    assert seen=={(z,j)for z in range(6)for j in selected[z]}
    assert queries=={s['packet']for s in ss}and corrections=={(s['packet'],i)for s in ss for i in s['targets']}
    word=copy.deepcopy(base);word['operations']=ops;word['milestones']=marks
    return word,captures

def symbolic(w,base_run,roots,e,captures,group_specs):
    C=base_run['C'];v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owned=set();born=set();cache={};parameters=sorted(captures.values());assert len(parameters)==39 and len(set(parameters))==39
    index={key:222+k for k,key in enumerate(parameters)};pmask={z:sum(1<<index[z,j]for j in s['roles'])for z,s in enumerate(group_specs)};source_evidence=[];cut=None
    for step,op in enumerate(w['operations'],1):
        code,name,*args=op
        if code=='INIT':assert name not in v and name not in born;owned.add(name);born.add(name);v[name]=0;at[name]=args[0]
        elif code=='ADD':
            dest=args[0];assert name in v and dest in v and C[at[name]]==C[at[dest]],(step,op)
            if step in captures:
                z,j=captures[step];assert name==f'X{j}'and dest==f'AFF{z}'and v[name]==1<<j
                assert at[name]==group_specs[z]['chart']
                v[dest]^=1<<index[z,j];source_evidence.append({'parameter':f'a{z}_{j}','formal_column':index[z,j],'source':name,'chart':at[name],'capture_step':step})
            else:v[dest]^=v[name]
        elif code=='MOVE':
            dest=args[0];key=(at[name],dest,name in owned)
            if key not in cache:cache[key]=e.contained(C[dest],C[at[name]])if name in owned else e.contained(C[at[name]],C[dest])
            assert cache[key]and len(C[dest])!=len(C[at[name]]);at[name]=dest
        elif code=='CLEAR':assert name in owned;owned.remove(name);del v[name],at[name]
        else:raise AssertionError(code)
        if step==w['milestones']['seed8_before_Y']:
            original=base_run['cuts']['seed']['values'];positions=base_run['cuts']['seed']['charts']
            shifted={s['retention']:pmask[z]for z,s in enumerate(group_specs)}
            for name,row in original.items():assert v[name]==row^shifted.get(name,0)and at[name]==positions[name],('unexpected_param_effect',name)
            for z,s in enumerate(group_specs):assert v[s['owner']]==pmask[z]and at[s['owner']]==s['chart']
            cut={'first_retention_formula':[{**s,'base_row_hex':hex(original[s['retention']]),'formal_parameter_mask_hex':hex(pmask[z])}for z,s in enumerate(group_specs)],'all_other_seedcut_fields_identical_to_base':True}
    assert cut and len(source_evidence)==39 and not owned
    for i in range(111):
        assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
        assert v[f'Y{i}']==((1<<(111+i))^((1<<i)if i in w['targets']else 0))and at[f'Y{i}']==f'F{i}'
    return {'columns':261,'base_columns':222,'formal_product_columns':39,'parameters':source_evidence,**cut,'all_parameter_columns_cancel_at_every_endpoint':True}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    br=a.base.read_bytes();wr=a.word.read_bytes();assert hashlib.sha256(br).hexdigest()==BASE and hashlib.sha256(wr).hexdigest()==WORD;base=json.loads(br);w=json.loads(wr)
    path=Path(__file__).with_name('retained')/'source_history_engine.py';sp=importlib.util.spec_from_file_location('exact',path);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
    source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']]
    base_run=e.replay(base,R,S,15,False);run=e.replay(w,R,S,15,False)
    selected=[[]for _ in range(6)]
    for s in w['affine_injections']:selected[s['packet']]=s['roles']
    independently_built,captures=rebuild(base,selected)
    assert independently_built['operations']==w['operations']and independently_built['milestones']==w['milestones']
    ss=specs(base);full,allcaptures=rebuild(base,[s['roles']for s in ss]);sym=symbolic(full,base_run,R,e,allcaptures,ss)
    assert run['count']=={'INIT':104,'ADD':866,'MOVE':427,'CLEAR':104}and run['dirty_CLEAR']==104
    assert run['profile']=={1:100,2:67,3:56,4:13,5:71,6:23,7:96,8:1}
    original=base_run['cuts']['seed']['values'];v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];C=run['C']
    for s in w['affine_injections']:
        r=sum(1<<j for j in s['roles']);assert v[s['owner']]==r and at[s['owner']]==s['chart'];assert v[s['first_retention']]==original[s['first_retention']]^r
    for i in range(111):assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{i}']==[o for o in base['operations']if o[0]=='MOVE'and o[1]==f'X{i}']
    tests=[('omit_actual_P0_injection',['ADD','AFF0','P0']),('omit_Y3_compensation',['ADD','AFF0','Y3']),('omit_Y21_compensation',['ADD','AFF0','Y21']),('omit_actual_P3_injection',['ADD','AFF3','P3']),('omit_Y4_compensation',['ADD','AFF3','Y4']),('omit_D3_correction_visit',['MOVE','Y3','D3_21']),('omit_affine_retirement',['CLEAR','AFF0'])]
    rejected=[]
    for label,op in tests:
        m=copy.deepcopy(w);ix=[j for j,o in enumerate(m['operations'])if o==op];assert len(ix)==1;m['operations'].pop(ix[0]);m['milestones']={key:-1 for key in w['milestones']};m.pop('source_cut',None)
        try:e.replay(m,R,S,15,False)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('semantic mutant accepted '+label)
    # Missing a whole affine source can leave endpoints correct; what it
    # violates is the promised acquisition. Test that obligation explicitly.
    m=copy.deepcopy(w);ix=m['operations'].index(['ADD','X10','AFF0']);m['operations'].pop(ix);m['milestones']={key:value-(value>ix)for key,value in w['milestones'].items()}
    mr=e.replay(m,R,S,15,False);assert mr['cuts']['seed']['values']['AFF0']!=1<<10;rejected.append('omit_raw_capture_fails_promised_acquisition')
    # Independent symbolic negative control: remove one correction; a formal
    # parameter survives an output even though all other39 rules remain.
    bad=copy.deepcopy(full);ix=bad['operations'].index(['ADD','AFF0','Y3']);bad['operations'].pop(ix);bad['milestones']={key:value-(value>ix)for key,value in full['milestones'].items()};shifted_captures={step-(step>ix):key for step,key in allcaptures.items()}
    try:symbolic(bad,base_run,R,e,shifted_captures,ss)
    except AssertionError:rejected.append('symbolic_uncancelled_parameter_at_Y3')
    else:raise AssertionError('symbolic mutant accepted')
    result={'status':'PASS_INDEPENDENT_HIGHER_AFFINE_SOURCE_AND_SYMBOLIC_FAMILY','word_sha256':WORD,'base_word_sha256':BASE,
            'native_source_sha256':w['source_sha256'],'concrete_input_columns':222,'targets':w['targets'],'counts':run['count'],'profile':run['profile'],'dirty_CLEAR':104,
            'independent_operation_rebuild_matches':True,'all_original_X_MOVE_routes_unchanged':True,'all_ground_seed_values_unchanged':True,
            'concrete_parameters':selected,'general_family':sym,
            'family_operation_formula':{'INIT':'102+a0+a1','ADD':'858+s+3*a0+2*a1','MOVE':'425+2*a0','CLEAR':'102+a0+a1','movement_increment':'a0*(4[1]-2[2])','definitions':'a0=#nonempty h0 groups, a1=#nonempty h1 groups, s=total selected raw source roles'},
            'semantic_negative_controls':rejected,'physical_mutants_disable_all_milestones_source_cut_and_invoice':True,
            'scope':'Actual private-row acquisition and source-preserving affine preload family. Old and new preload are not both granted. No additional endpoint, complete supplier or new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'FULL-SYMBOLIC-TEMPLATE.json').write_text(json.dumps({'operations':full['operations'],'capture_parameter_map':{str(k):list(v)for k,v in allcaptures.items()}},indent=2)+'\n')
    print(json.dumps({k:result[k]for k in ['status','counts','profile','family_operation_formula','semantic_negative_controls']}))
if __name__=='__main__':main()
