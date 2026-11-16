#!/usr/bin/env python3
"""Compare actual source stocks and scoped frozen-history quotients at46.

Literal stock spans and the quotient granting all46 completed input directions
are separate objects. Neither is a free physical decoder or custody grant.
"""
from pathlib import Path
import argparse,hashlib,json
from source_loader import load

def snapshots(w):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    out={}
    for step,o in enumerate(w['operations'],1):
        op,n,*q=o
        if op=='INIT'and n=='P7':out['before_P7_birth']=(step,v.copy(),at.copy())
        if op=='CLEAR'and 'before_first_CLEAR'not in out:out['before_first_CLEAR']=(step,v.copy(),at.copy())
        if o==['ADD','CAP46','P3']:out['before_P3_CAP46']=(step,v.copy(),at.copy())
        if op=='INIT':v[n]=0;at[n]=q[0]
        elif op=='MOVE':at[n]=q[0]
        elif op=='ADD':v[q[0]]^=v[n]
        elif op=='CLEAR':del v[n],at[n]
    return out

def relation(e,A,B):
    a=list(e.bb(A).values());b=list(e.bb(B).values());u=e.bb(a+b)
    return {'left_rank':len(a),'right_rank':len(b),'union_rank':len(u),
            'left_directions_missing_from_right':len(u)-len(b),
            'right_directions_missing_from_left':len(u)-len(a),
            'left_contained_in_right':len(u)==len(b),
            'right_contained_in_left':len(u)==len(a),
            'left_not_in_right_witnesses_hex':[hex(r)for r in a if not e.fits(b,r)],
            'right_not_in_left_witnesses_hex':[hex(r)for r in b if not e.fits(a,r)]}

def dual(rows,target):
    b={}
    for x,t in[(r,0)for r in rows]+[(1<<target,1)]:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p][0];t^=b[p][1]
            else:b[p]=(x,t);break
        assert x or not t
    z=0
    for p,(r,t)in sorted(b.items()):
        if ((r&z).bit_count()%2)^t:z|=1<<p
    assert z>>target&1 and all(not((r&z).bit_count()%2)for r in rows)
    return z

def main():
    p=argparse.ArgumentParser()
    for n in['repo','raw','engine','price-engine','out']:p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--coded',type=Path,nargs='+',required=True);a=p.parse_args()
    e=load(a.engine,'compare46_geometry');price=load(a.price_engine,'compare46_price')
    words=[]
    for path in[a.raw]+a.coded:
        blob=path.read_bytes();w=json.loads(blob);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];C,H,replay=e.replay(w,R)
        words.append({'path':str(path),'sha256':hashlib.sha256(blob).hexdigest(),'word':w,'C':C,'H':H,'replay':replay,'cuts':snapshots(w)})
    known=set(words[0]['word']['targets']);assert len(known)==46 and all(set(r['word']['targets'])==known for r in words)
    xmask=(1<<111)-1;kmask=sum(1<<i for i in known);remaining=xmask^kmask
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
    def stock(entry,chart,cut):
        _,v,at=entry['cuts'][cut];C=entry['C']
        return {n:r for n,r in v.items()if not r>>111 and C[at[n]]==C[chart]}
    def visible(entry,i,mode):
        C=entry['C'];F=C[f'F{i}']
        if mode=='current':
            _,v,at=entry['cuts']['before_first_CLEAR']
            return [r for n,r in v.items()if not r>>111 and e.sub(C[at[n]],F)]
        return [r&xmask for _,_,ch,r in entry['H']if e.sub(C[ch],F)]
    diagnostics=[]
    for entry in words:
        base=[]
        for i in range(111):base.append([r&remaining for r in visible(entry,i,'history')]+[1<<j for j in range(111)if j not in known and dot(i,j)==0])
        reached=set(known);waves=[]
        while True:
            new={i for i in range(111)if i not in reached and e.fits(base[i]+[1<<j for j in reached-known],1<<i)}
            if not new:break
            reached|=new;waves.append(sorted(new))
        ds=[{'receiver':i,'dual_hex':hex(dual(base[i]+[1<<j for j in reached-known],i))}for i in range(111)if i not in reached]
        diagnostics.append({'word_sha256':entry['sha256'],'path':entry['path'],'replay':entry['replay'],
                            'moment':price.display(price.moment(entry['replay']['movement_profile'])),
                            'source_cut_M1_inventory':{n:hex(r)for n,r in stock(entry,'M1','before_P3_CAP46').items()},
                            'source_cut_M0_inventory':{n:hex(r)for n,r in stock(entry,'M0','before_P7_birth').items()},
                            'ground_inventory':{n:hex(r)for n,r in stock(entry,'zero','before_first_CLEAR').items()},
                            'strong_frozen_history_feedback_closure':sorted(reached),'feedback_waves':waves,'outsider_duals':ds})
    comparisons=[];raw=words[0]
    for coded in words[1:]:
        ground=relation(e,stock(raw,'zero','before_first_CLEAR').values(),stock(coded,'zero','before_first_CLEAR').values())
        m1=relation(e,stock(raw,'M1','before_P3_CAP46').values(),stock(coded,'M1','before_P3_CAP46').values())
        m0=relation(e,stock(raw,'M0','before_P7_birth').values(),stock(coded,'M0','before_P7_birth').values())
        actual=[];quotient=[]
        for i in range(111):
            av=relation(e,visible(raw,i,'current'),visible(coded,i,'current'));actual.append({'receiver':i,**av})
            locals_=[1<<j for j in range(111)if j not in known and dot(i,j)==0]
            ar=[r&remaining for r in visible(raw,i,'history')]+locals_
            cr=[r&remaining for r in visible(coded,i,'history')]+locals_
            quotient.append({'receiver':i,**relation(e,ar,cr)})
        comparisons.append({'raw_word_sha256':raw['sha256'],'coded_word_sha256':coded['sha256'],
                            'relation_orientation':'left=paid raw46, right=coded46',
                            'literal_common_stock':ground,'literal_M1_source_stock':m1,'literal_M0_source_stock':m0,
                            'literal_visible_current_stock':actual,
                            'all_history_Xparts_plus_raw_locals_modulo_46_completed_columns':quotient,
                            'coded_quotient_contained_in_raw_for_all111':all(q['right_contained_in_left']for q in quotient),
                            'raw_quotient_contained_in_coded_for_all111':all(q['left_contained_in_right']for q in quotient),
                            'receivers_with_coded_only_quotient_directions':[q['receiver']for q in quotient if not q['right_contained_in_left']],
                            'receivers_with_raw_only_quotient_directions':[q['receiver']for q in quotient if not q['left_contained_in_right']]})
    i=next(i for i in range(111)if i not in known and not e.fits([r&remaining for r in visible(raw,i,'history')]+[1<<j for j in range(111)if j not in known and dot(i,j)==0],1<<i))
    rows=[r&remaining for r in visible(raw,i,'history')]+[1<<j for j in range(111)if j not in known and dot(i,j)==0]
    assert not relation(e,rows,rows+[1<<i])['right_contained_in_left']
    out={'status':'PASS_LITERAL_SOURCE_AND_FROZEN_QUOTIENT_COMPARISON46','completed_points':sorted(known),
         'quotient_contract':'Only in the explicitly optimistic quotient are all46 completed raw input directions freely granted everywhere; actual original-Y endpoints do not themselves provide those raw directions at arbitrary charts.',
         'words':diagnostics,'comparisons':comparisons,
         'negative_control':{'injected_unresolved_common_point':i,'new_quotient_direction_detected':True},
         'scope':'Actual word-derived source/custody snapshots and linear-space comparisons. Geometric visibility does not supply a nested chronological decoder; quotient inclusion is not literal source-contract or physical algorithm domination.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'closures':[len(d['strong_frozen_history_feedback_closure'])for d in diagnostics],
                      'comparisons':[{'coded_sha':q['coded_word_sha256'],'ground_ranks':(q['literal_common_stock']['left_rank'],q['literal_common_stock']['right_rank']),'coded_quotient_in_raw':q['coded_quotient_contained_in_raw_for_all111'],'raw_quotient_in_coded':q['raw_quotient_contained_in_coded_for_all111'],'raw_extra_receivers':q['receivers_with_raw_only_quotient_directions'],'coded_extra_receivers':q['receivers_with_coded_only_quotient_directions']}for q in comparisons]}))

if __name__=='__main__':main()
