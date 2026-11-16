#!/usr/bin/env python3
"""Independent source, geometry, cost, and endpoint review of the36 word."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse, copy, hashlib, importlib.util, json
BASE='e4d451886a134c648f71fadac5b7f6f8693e5495b60416d137cfe0d0e563e050'
NEW='af51d0d7c872dbf3fa3744b582769d4c7763e0747e57c74005d091d19b7da474'
SOURCE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
    s=importlib.util.spec_from_file_location('independent_leaf_engine',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def cut(word):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
    at={f'X{i}':f'L{i}' for i in range(111)}|{f'Y{i}':'zero' for i in range(111)}
    cuts={};events=[]
    for step,o in enumerate(word['operations'],1):
        op,n,*q=o
        if op=='INIT':v[n]=0;at[n]=q[0]
        elif op=='MOVE':at[n]=q[0]
        elif op=='CLEAR':del v[n],at[n]
        else:
            assert op=='ADD'
            if q[0] in ['RAW41','CAP46'] or (q[0]=='P3' and n in ['CAP46','RAW41']):events.append({'step':step,'operation':o,'source_value_hex':hex(v[n]),'source_chart':at[n],'destination_chart':at[q[0]]})
            v[q[0]]^=v[n]
        if step==word['milestones']['source_cut']:
            for n,r in word['source_cut'].items():assert v[n]==int(r['row_hex'],16) and at[n]==r['chart']
            cuts['source']=(v.copy(),at.copy())
        if step==word['milestones']['seed8_before_Y']:
            assert [hex(v[f'P{i}']) for i in range(8)]==word['seed_rows_hex']
            cuts['seed']=(v.copy(),at.copy())
        if step==word['milestones']['all_X_restored']:
            assert all(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub' for i in range(111))
    return cuts,events

def root_floor(n,k):
    if n<2:return n
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//pow(x,k-1))//k
        if y>=x:break
        x=y
    while pow(x,k)>n:x-=1
    while pow(x+1,k)<=n:x+=1
    assert pow(x,k)<=n<pow(x+1,k)
    return x

SCALE=10**32
CACHE={}
def bracket(d):
    if d not in CACHE:
        y=pow(d,199)*pow(SCALE,200);n=root_floor(y,200)
        CACHE[d]=(Fraction(n,SCALE),Fraction(n if pow(n,200)==y else n+1,SCALE))
    return CACHE[d]
def moment(profile):
    lo=hi=Fraction(0)
    for d,c in profile.items():
        a,b=bracket(int(d));lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi
def display(bounds):
    with localcontext() as ctx:
        ctx.prec=48
        return {'lower':str(Decimal(bounds[0].numerator)/Decimal(bounds[0].denominator)), 'upper':str(Decimal(bounds[1].numerator)/Decimal(bounds[1].denominator)), 'lower_fraction':str(bounds[0]),'upper_fraction':str(bounds[1])}
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--author-price',type=Path,required=True);p.add_argument('--closure',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert sha(a.base)==BASE and sha(a.word)==NEW
    old=json.loads(a.base.read_text());new=json.loads(a.word.read_text());source=a.repo/new['source_path'];assert sha(source)==SOURCE==new['source_sha256'];R=json.loads(source.read_text())['native_roots'];e=load(a.engine)
    OC,OH,orep=e.replay(old,R);C,H,rep=e.replay(new,R);oc,_=cut(old);nc,events=cut(new);ov,oa=oc['seed'];nv,na=nc['seed']
    assert C['M1']==C['C2'] and e.sub(C['L41'],C['F46'])
    assert rep['counts']=={'INIT':117,'ADD':916,'MOVE':437,'CLEAR':117} and rep['dirty_CLEAR']==117
    assert rep['peak_owned']==117
    assert set(new['targets'])-set(old['targets'])=={41,46} and set(old['targets'])<=set(new['targets'])
    old_x=[o for o in old['operations'] if o[0]=='MOVE' and o[1].startswith('X')]
    new_x=[o for o in new['operations'] if o[0]=='MOVE' and o[1].startswith('X')]
    assert old_x==new_x
    assert set(nv)-set(ov)=={'RAW41','CAP46'} and set(ov)<=set(nv)
    changes={n:[hex(ov[n]),hex(nv[n])] for n in ov if ov[n]!=nv[n]}
    assert set(changes)=={'P3','ZKEEP2'}
    assert all(na[n]==oa[n] for n in ov)
    assert ov['P3']==ov['ZRAW0']^ov['E6']
    assert nv['P3']==(1<<41)^(1<<6) and na['P3']=='zero'
    assert nv['ZKEEP2']==nv['CAP46']==1<<46 and na['ZKEEP2']=='L41' and na['CAP46']=='M1'
    assert nv['RAW41']==1<<41 and na['RAW41']=='L41'
    oldg=[v for n,v in ov.items() if oa[n]=='zero' and v>>111==0];newg=[v for n,v in nv.items() if na[n]=='zero' and v>>111==0]
    assert len(e.bb(oldg))==14 and len(e.bb(newg))==15 and len(e.bb(oldg+newg))==15
    assert len(events)==4 and [x['source_value_hex'] for x in events]==[hex(1<<41),hex(1<<46),hex(1<<46),hex(1<<41)]
    profile=orep['movement_profile'].copy();profile[1]+=1;profile[6]+=1;profile[7]-=1;assert rep['movement_profile']==profile
    # Price uses fresh exact integer200th roots at a different fixed-point scale.
    price=moment(profile);bprofile={127:37,64:74,1:-74}
    for j in range(1,9):bprofile[1+7*j]=bprofile.get(1+7*j,0)+74;bprofile[7*j]=bprofile.get(7*j,0)-74
    lim=tuple(v/6 for v in moment(bprofile));room=(lim[0]-price[1],lim[1]-price[0]);delta=moment({1:1,6:1,7:-1})
    ap=json.loads(a.author_price.read_text())
    for tag,bounds in [('moment',price),('limiting_allowance',lim),('limiting_room',room)]:
        al=Fraction(ap[tag]['lower_fraction']);ah=Fraction(ap[tag]['upper_fraction']);assert bounds[0]<=al<=ah<=bounds[1],tag
    closure=json.loads(a.closure.read_text());assert closure['word_sha256']==NEW
    assert set(closure['optimistic_closure'])==set(new['targets'])
    assert {d['receiver'] for d in closure['outsider_duals']}==set(range(111))-set(new['targets'])
    assert len(closure['outsider_duals'])==75
    dual_checks=[];xmask=(1<<111)-1
    for d in closure['outsider_duals']:
        i=d['receiver'];z=int(d['dual_hex'],16);assert z>>i&1 and z>>111==0
        rows=[value&xmask for _,_,ch,value in H if e.sub(C[ch],C[f'F{i}'])]
        rows +=[1<<j for j in range(111) if sum(x*y for x,y in zip(R[i],R[j]))==0]
        rows +=[1<<j for j in new['targets']]
        assert all((r&z).bit_count()%2==0 for r in rows),(i,'closure dual')
        dual_checks.append({'receiver':i,'dual_hex':hex(z),'independently_checked_measurements':len(rows)})
    rejected=[]
    for op in [['ADD','X41','RAW41'],['ADD','X46','CAP46'],['ADD','CAP46','P3'],['ADD','RAW41','P3'],['ADD','P3','Y41'],['ADD','E6','Y41'],['ADD','ZKEEP2','Y46'],['MOVE','Y46','L41'],['ADD','ZRAW0','Y2'],['ADD','E6','Y2'],['CLEAR','RAW41'],['CLEAR','CAP46']]:
        bad=copy.deepcopy(new);bad['operations'].remove(op)
        # Independent interpreter has no cost/source/milestone acceptance checks.
        try:e.replay(bad,R)
        except (AssertionError,KeyError) as ex:rejected.append({'removed':op,'failure':str(ex)})
        else:raise AssertionError(('accepted semantic omission',op))
    out={'status':'PASS_INDEPENDENT_ACTUAL36_SOURCE_AND_PRICE','base_word_sha256':BASE,'new_word_sha256':NEW,'native_source_sha256':SOURCE,'independent_engine_sha256':sha(a.engine),'replay':rep,'all_original_X_MOVE_operations_identical':True,'old_seed_cut_value_changes':changes,'old_seed_cut_charts_unchanged':True,'new_actual_source_events':events,'common_rank_before':14,'common_rank_after':15,'old_common_space_retained':True,'exact_profile_delta':{'1':1,'6':1,'7':-1},'new_endpoints':[41,46],'independent_directed_price':{'method':'integer200th roots, scale10^32, exact fractions','moment':display(price),'limiting_allowance':display(lim),'limiting_room':display(room),'increment':display(delta)},'author_price_interval_contained_in_independent_interval':True,'independently_checked_75_closure_duals':dual_checks,'closure_scope':'Even all record histories with original-Y X-parts, geometric raw locals and free decoded-point feedback remain closed at36.','semantic_omissions_rejected_without_invoice_or_metadata_checks':rejected,'scope':'Exact all222-column formal whole-record identities and rational geometry, all characteristic-two fields/widths. Physical erasure applicability, compiler, precision, complete suppliers and recursion remain open. No new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'counts':rep['counts'],'moment':display(price),'room':display(room),'controls':len(rejected)}))
if __name__=='__main__':main()
