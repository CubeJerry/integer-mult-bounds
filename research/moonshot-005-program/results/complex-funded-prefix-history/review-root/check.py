#!/usr/bin/env python3
"""Independent stream chronology review. Apache-2.0; @CubeJerry/OpenAI."""
import argparse,copy,gzip,hashlib,importlib.util,json
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)

def load_engine():
    p=Path(__file__).with_name('engine.py')
    spec=importlib.util.spec_from_file_location('root_rational_replay',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def rank(rows):
    b={}
    for source in rows:
        row=dict(source)
        for j in sorted(b):
            if j in row:
                c=row[j]
                for k,v in b[j].items():
                    z=row.get(k,F(0))-c*v
                    if z:row[k]=z
                    else:row.pop(k,None)
        if row:
            j=min(row);c=row[j];b[j]={k:v/c for k,v in row.items()}
    return len(b)

def root_vector(bits):
    on=[i for i in range(9) if bits>>i&1]
    if len(on)==3:return [2 if i in on else -1 for i in range(9)]
    off=[i for i in range(9) if not(bits>>i&1)]
    need(len(off)==2,'native root type')
    return [3*(int(i==off[0])-int(i==off[1])) for i in range(9)]

def main():
    p=argparse.ArgumentParser()
    for name in ['package','native','seed','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();eng=load_engine()
    nr=a.native.read_bytes();sr=a.seed.read_bytes()
    need(hashlib.sha256(nr).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native pin')
    need(hashlib.sha256(sr).hexdigest()=='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc','seed pin')
    need(hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest()=='a28667638b3199086f74b9d01af93a24993bfbfdde8c94fe8fb5819c46ec3130','author proof pin')
    native=json.loads(gzip.decompress(nr));seed=json.loads(gzip.decompress(sr));parent=eng.replay(seed)
    raw=(a.package/'output/WORD.json.gz').read_bytes();w=json.loads(gzip.decompress(raw));m=w['funded_prefix']
    role={int(k):v for k,v in seed['source_role_map'].items()};live=native['live']
    pairs={live[i]:(role[b],role[d]) for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    roots={h:root_vector(native['frames'][native['initial'][h]][0]) for h in live}
    omitted=root_vector(7);g={h:F(sum(x*y for x,y in zip(omitted,roots[h])),18) for h in live}
    J=m['donors'];T=m['receiver_class'];P={j:F(m['p'][str(j)]) for j in J};Q={h:F(m['q'][str(h)]) for h in T}
    need(all(P[j]==2*g[j] for j in J) and all(Q[h]==-g[h] for h in T),'native factor coefficients')
    sd={int(k):v for k,v in m['source_dimensions'].items()};rd={int(k):v for k,v in m['receiver_dimensions'].items()}
    spaces=[eng.span(z) for z in w['frames']];K={}
    for h in T:
        for j in J:
            if sd[j]<=rd[h]:
                value=Q[h]*P[j];gram=F(sum(x*y for x,y in zip(roots[h],roots[j])),18)
                need(value==-gram and value,'actual erased Gram coefficient')
                station=m['stations'][str(rd[h])]
                need(spaces[w['initial'][role[j]]]<=spaces[station]<=spaces[parent[1][role[h+112]]],'genuine donor/receiver containment')
                K[h,j]=value
    need(len(K)==52,'fifty-two paired coefficients')
    expected=copy.deepcopy(parent[0]);correction={h:{} for h in T}
    for (h,j),c in K.items():
        expected[role[h+112]]=eng.plus(expected[role[h+112]],parent[0][role[j]],c)
        expected[pairs[j][0]]=eng.plus(expected[pairs[j][0]],{pairs[h][1]:F(1)},-c)
        correction[h][role[j]]=c
    need(rank(correction.values())==3,'exact correction rank')
    minor=[[K.get((h,j),F(0)) for j in [4,2,1]] for h in [57,87,0]]
    need(all(not minor[i][j] for i in range(3) for j in range(i+1,3)) and minor[0][0]*minor[1][1]*minor[2][2]==F(1,8),'explicit rank-three minor')
    gx={};gd={}
    for h in live:gx=eng.plus(gx,parent[0][role[h]],g[h])
    for h in pairs:gd=eng.plus(gd,{pairs[h][1]:F(1)},g[h])
    generations={};moving=set();cross={'reverse':[],'forward':[]};observations=[]
    def hook(t,when,o,rows,loc):
        if when=='before':
            if t in m['events']['reverse_restorations']:
                need(o[0]=='ADD' and rows[o[2]]=={o[2]:F(1)},'authentic local restored D source')
            return
        if o[0]=='INIT':generations[o[1]]=t
        if o[0]=='MOVE' and o[4]:
            moving.add((o[1],generations[o[1]]))
            if o[1]==400:
                if m['markers']['entry_end']<t<=m['markers']['reverse_mode_restored']:cross['reverse'].append(dict(rows[400]))
                elif m['markers']['all_reverse_consumed']<t<=m['markers']['forward_mode_restored']:cross['forward'].append(dict(rows[400]))
        for group in m['groups']:
            if t==group['markers']['D_restored']:
                need(all(rows[d]=={d:F(1)} and spaces[loc[d]]==spaces[group['C']] for d in group['D_roles']),'actual D restoration at each C3')
        if t==m['markers']['D_all_restored']:
            need(all(rows[d]=={d:F(1)} for b,d in pairs.values()),'all96 original D restored')
            observations.append('all_D_restored')
        if t==m['markers']['reverse_mode_restored']:
            need(rows[400]==gd,'old reverse mode duty restored');observations.append('old_reverse_mode')
        if t==m['markers']['forward_mode_restored']:
            need(rows[400]==gx,'old forward mode duty restored');observations.append('old_forward_mode')
        if t==m['markers']['prefix_reverse_complete']:
            for j,(b,d) in pairs.items():
                want={b:F(1)}
                for h in T:want=eng.plus(want,{pairs[h][1]:F(1)},-K.get((h,j),F(0)))
                need(rows[b]==want,'actual changed B after Hub compensation')
            observations.append('all_B_compensated')
        for phase in m['up_phases']:
            dim=phase['dimension']
            if t in [phase['arrival'],phase['D_contribution_restored']]:
                want=dict(gd)
                for h in T:
                    if rd[h]>=dim if t==phase['arrival'] else rd[h]>dim:
                        want=eng.plus(want,{pairs[h][1]:F(1)},Q[h])
                need(rows[400]==want,'ascending actual suffix history')
        for phase in m['down_phases']:
            dim=phase['dimension']
            if t==phase['arrival'] or t==phase.get('after_source_shed'):
                want=dict(gx)
                for j in J:
                    if sd[j]<=dim if t==phase['arrival'] else sd[j]<dim:
                        want=eng.plus(want,parent[0][role[j]],P[j])
                need(rows[400]==want,'descending actual prefix history')
            if 'output_capture' in phase and t==phase['output_capture']+1:
                cache=m['output_caches'][str(dim)];want=dict(gx)
                for j in J:
                    if sd[j]<=dim:want=eng.plus(want,parent[0][role[j]],P[j])
                need(rows[cache]==want,'genuine prefix cache copied before shedding')
    result=eng.replay(w,hook=hook)
    need(result[0]==expected and result[1]==parent[1],'all400 public rows and all final charts')
    need(rank(result[0].values())==400,'all400 independent inputs retained')
    need(len(cross['reverse'])==len(cross['forward'])==7,'seven actual passages in each old lifetime')
    need(rank(cross['reverse'])==5 and rank(cross['forward'])==6,'actual boundary history dimensions')
    need(len(moving)==24,'all24 old moving lifetimes, none newly introduced')
    need(sum(k*v for k,v in result[3].items())==136,'owned rank mass unchanged')
    need(all(F(o[3] if o[0]=='ADD' else o[2]).denominator in [1,2] for o in w['program'] if o[0] in ['ADD','SCALE']),'all source coefficients dyadic')
    class_incidence=0
    for group in m['groups']:
        need(len(w['frames'][group['C']])==3,'actual rank-three reunion')
        for h in live:
            contained=spaces[group['C']]<=spaces[parent[1][role[h+112]]]
            need(contained==(h in group['ports']),'exact same-class C3/facet incidence')
            class_incidence+=1
    paired=0
    for h in pairs:
        for j in pairs:
            need(result[0][pairs[j][0]].get(pairs[h][1],F(0))+result[0][role[h+112]].get(role[j],F(0))==0,'hosted paired transpose identity')
            paired+=1
    residual=[]
    for h,(b,d) in pairs.items():residual.append(eng.plus(eng.plus(result[0][b],{b:F(1)},-1),{d:F(1)},1))
    need(rank(residual)==96,'full hosted residual remains96')
    author=json.loads((a.package/'output/RESULT.json').read_text())
    need({str(k):v for k,v in result[2].items()}==author['raw_histogram'] and {str(k):v for k,v in result[3].items()}==author['owned_histogram'],'independent raw/owned profile')
    need(result[4]==author['source_bill']['counts'] and result[5]==author['source_bill']['peak'] and result[6]==author['source_bill']['lifetimes'],'every ordinary/owner count')
    negatives=[]
    for label,idx in [('Hub_compensation',m['events']['Hub_B_compensation'][0]),('forward_augmentation',m['events']['forward_augmentation'][0]),('source_shedding',m['down_phases'][0]['source_shed'])]:
        bad=copy.deepcopy(w);need(bad['program'][idx][0]=='ADD','targeted mutation opcode');bad['program'][idx][3]='0'
        changed=eng.replay(bad)
        need(changed[0]!=expected,'omission changes actual public map: '+label)
        negatives.append(label+' omission rejected')
    report=dict(mode='output',word_sha256=hashlib.sha256(raw).hexdigest(),all400_rows=True,all_final_charts=True,all400_rank=400,raw=result[2],owned=result[3],ordinary_counts=result[4],peak=result[5],lifetimes=result[6],moving_lifetimes=len(moving),new_stationary_lifetimes=result[6]-24,reverse_passages=7,forward_passages=7,reverse_history_rank=5,forward_history_rank=6,correction_rank=3,paired_coefficients=52,paired_identity_entries=paired,residual_rank=96,class_incidence_checks=class_incidence,seed_profile={k:parent[2].get(k,0)+parent[3].get(k,0) for k in set(parent[2])|set(parent[3])},phase_checks=observations,negative_controls=negatives)
    out=dict(status='PASS_INDEPENDENT_FUNDED_PREFIX_SOURCE_AND_HISTORY',author_proof_sha256=hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest(),variants=[report],scope='Independent sparse rational400-column replay, genuine mode duties and ownership; generic proof reviewed separately. Source remains partial; no new kappa.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
