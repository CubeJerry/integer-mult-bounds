#!/usr/bin/env python3
"""Native singular-pivot cover specialization; source acquisition unassumed."""
import argparse,copy,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
RECOVERY='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
RECOVERY_PIN='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
FULL='research/moonshot-005-program/results/bit-proper-flat-cubic-generators/author/RESULT.json'
FULL_PIN='4ac3933fb2393c62a96ec9e931ef4936e61d0e6c912c7ce0a94398a5f19addfc'
FRAME=[0,1,2,4,8,14,30,59]
def need(value,message):
    if not value:raise ValueError(message)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def bitset(indices):return sum(1<<i for i in indices)
def support(row):return [i for i in range(111)if row>>i&1]
def rank2(rows):
    b={}
    for row in rows:
        while row:
            k=row.bit_length()-1
            if k in b:row^=b[k]
            else:b[k]=row;break
    return len(b)
def rankq(rows):
    b={}
    for source in rows:
        row=list(map(F,source))
        for k in sorted(b):
            if row[k]:
                q=row[k];row=[x-q*y for x,y in zip(row,b[k])]
        if any(row):
            k=next(i for i,x in enumerate(row)if x);q=row[k]
            b[k]=[x/q for x in row]
    return len(b)
def authenticated(repo,path,pin):
    raw=(repo/path).read_bytes();need(hashlib.sha256(raw).hexdigest()==pin,'source SHA256 changed: '+path)
    return json.loads(raw)
def geometry(repo):
    rec=authenticated(repo,RECOVERY,RECOVERY_PIN);full=authenticated(repo,FULL,FULL_PIN)
    roots=rec['native_roots'];allroots=full['full_roots'];native_map=rec['native_to_full']
    need(len(roots)==111 and len(allroots)==120,'root cardinalities')
    need([allroots[i]for i in native_map]==roots,'native/full root map')
    need(all(dot(r,r)==4 for r in allroots),'normalization')
    gram=[bitset(k for k,j in enumerate(FRAME)if (dot(roots[i],roots[j])//2)&1)for i in FRAME]
    polar=lambda a,b:sum(((a>>i)&1)*((row&b).bit_count()&1)for i,row in enumerate(gram))&1
    q=lambda a:(a.bit_count()+sum(((a>>i)&1)*((a>>j)&1)*((gram[i]>>j)&1)for i in range(8)for j in range(i+1,8)))&1
    patterns={tuple(polar(1<<i,a)for i in range(8)):a for a in range(256)}
    need(len(patterns)==256,'nondegenerate polar frame')
    labels=[patterns[tuple((dot(r,roots[i])//2)&1 for i in FRAME)]for r in allroots]
    need(len(set(labels))==120 and all(q(a)==1 for a in labels),'full anisotropic quadric')
    native=[labels[i]for i in native_map]
    need(all(native[i]==1<<j for j,i in enumerate(FRAME)),'binary frame coordinates')
    need(all(polar(native[i],native[j])==int(bool(dot(roots[i],roots[j])))for i in range(111)for j in range(111)if i!=j),'native polar/orthogonality identity')
    return roots,allroots,native_map,native,labels,polar,q
def validate_cover(item,roots):
    i=item['receiver'];foreign=item['foreign_support'];row=int(item['fitting_row_hex'],16)
    need(row>>i&1,'missing own coefficient')
    need(support(row^(1<<i))==foreign,'foreign support mismatch')
    need(all(dot(roots[i],roots[j])==0 for j in foreign),'nonlocal fitting coefficient')
    total=set()
    for part in item['cover']:
        ids=part['support'];normals=part['chart']['rows']
        if part['chart']['kind']=='ann':
            dimension=8-rankq(normals)
            need(dimension<7,'carrier is not proper')
            need(rankq(normals+[roots[i]])==rankq(normals),'carrier outside receiver facet')
            need(all(dot(roots[j],normal)==0 for j in ids for normal in normals),'support outside actual ann chart')
        else:
            dimension=rankq(normals)
            need(dimension<7,'span carrier is not proper')
            need(all(dot(x,roots[i])==0 for x in normals),'span carrier outside receiver facet')
            need(all(rankq(normals+[roots[j]])==dimension for j in ids),'support outside actual span chart')
        need(part['dimension']==dimension,'carrier dimension metadata');total.update(ids)
    need(total==set(foreign),'cover misses foreign coordinate')
    whole=rankq([roots[j]for j in foreign])
    need(whole==item['foreign_span_rank'],'foreign rank metadata')
    need(whole in(6,7),'unexpected local support rank')
    minimum=1 if whole==6 else 2
    need(len(item['cover'])==minimum,'not a minimal cover certificate')
    need(item['charge']==minimum-1,'wrong proper-cover charge')
def singular_cover(s,roots,allroots,native_map,native,labels,polar,q):
    need(s!=0 and q(s)==0,'pivot is not nonzero singular')
    pairs=[(i,j)for i in range(8)for j in range(i+1,8)if native[i]^native[j]==s]
    need(len(pairs)==4,'singular axis pivot does not pair all eight axes')
    a,b=pairs[0];need(dot(roots[a],roots[b])==0,'carrier axes not orthogonal')
    h=[polar(s,x)for x in native];hm=bitset(i for i,value in enumerate(h)if value)
    C=[bitset(j for j,r in enumerate(roots)if i==j or dot(roots[i],r)==0)for i in range(111)]
    W=[row&(hm if h[i]else((1<<111)-1)^hm)for i,row in enumerate(C)]
    Cs=[row for i,row in enumerate(C)if not h[i]];hC=[row&hm for row in C]
    need(rank2(C)==9 and rank2(W)==15 and rank2(C+W)==16,'global fitting/code ranks')
    need(rank2(Cs)==8 and rank2(hC)==8 and rank2(Cs+hC)==15 and rank2(Cs+hC+W)==15,'singular code identity')
    covers=[]
    for i,row in enumerate(W):
        foreign=support(row^(1<<i));whole=rankq([roots[j]for j in foreign]);parts=[];pf=pn=None
        if not h[i]:
            pf=labels.index(native[i]^s);p=allroots[pf]
            need(dot(p,roots[i])==0,'singular partner not actually orthogonal')
            pn=native_map.index(pf)if pf in native_map else None
            common=[j for j in foreign if dot(roots[j],p)==0]
            exceptional=[j for j in foreign if dot(roots[j],p)!=0]
            need(exceptional==([]if pn is None else[pn]),'unexpected partner exception')
            parts.append({'chart':{'kind':'ann','rows':[roots[i],p]},'dimension':6,'support':common})
            if exceptional:parts.append({'chart':{'kind':'span','rows':[p]},'dimension':1,'support':exceptional})
        else:
            left=[j for j in foreign if dot(roots[j],roots[a])==0]
            right=[j for j in foreign if j not in left]
            need(all(dot(roots[j],roots[b])==0 for j in right),'two actual carrier facets do not cover')
            parts=[{'chart':{'kind':'ann','rows':[roots[i],roots[a]]},'dimension':6,'support':left},
                   {'chart':{'kind':'ann','rows':[roots[i],roots[b]]},'dimension':6,'support':right}]
        item={'receiver':i,'h':h[i],'fitting_row_hex':hex(row),'foreign_support':foreign,'foreign_span_rank':whole,
              'partner_full_index':pf,'partner_native_index':pn,'cover':parts,'charge':len(parts)-1}
        validate_cover(item,roots);covers.append(item)
    return {'status':'PASS_INDEPENDENT_SINGULAR_NATIVE_PROPER_COVERS','h_coordinates':s,'pivot_binary_frame':s,
            'h_mask_hex':hex(hm),'actual_axis_pairs':pairs,'chosen_carriers':[a,b],
            'native_class_sizes':[111-sum(h),sum(h)],'full_class_sizes':[sum(not polar(s,x)for x in labels),sum(polar(s,x)for x in labels)],
            'W_rank':15,'canonical_joint_rank':16,'canonical_intersection':8,
            'proper_cover_charge':sum(item['charge']for item in covers),
            'one_chart_receivers':[item['receiver']for item in covers if item['charge']==0],
            'foreign_rank_histogram':dict(Counter(item['foreign_span_rank']for item in covers)),
            'covers':covers,'new_complete_kappa':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    args=geometry(a.repo);roots,allroots,native_map,native,labels,polar,q=args
    a.out.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS_INDEPENDENT_AXIS_PIVOT_PROPER_COVERS','source_recovery_sha256':RECOVERY_PIN,'full_geometry_sha256':FULL_PIN,
            'singular_pivots':{},'anisotropic_pivots_not_claimed_by_singular_theorem':[],'negative_controls':{},'new_complete_kappa':False}
    saved={}
    for s in range(1,16):
        if q(s):result['anisotropic_pivots_not_claimed_by_singular_theorem'].append(s);continue
        rec=singular_cover(s,*args)
        path=a.out/f'PIVOT-{s}-COVERS.json';path.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n');saved[s]=rec
        result['singular_pivots'][s]={k:v for k,v in rec.items()if k!='covers'}
        result['singular_pivots'][s]['certificate_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    base=saved[3];muts={}
    bad=copy.deepcopy(base['covers'][0]);bad['fitting_row_hex']=hex(int(bad['fitting_row_hex'],16)^(1<<bad['receiver']));muts['erase_own_entry']=bad
    good=next(row for row in base['covers']if row['h']==1)
    bad=copy.deepcopy(good);bad['cover'][1]['chart']['rows']=[roots[bad['receiver']],roots[0]];muts['reuse_first_carrier_for_both_halves']=bad
    bad=copy.deepcopy(next(row for row in base['covers']if row['charge']==1));bad['charge']=0;muts['pretend_rank7_support_needs_one_chart']=bad
    for name,bad in muts.items():
        try:validate_cover(bad,roots)
        except ValueError as error:result['negative_controls'][name]={'rejected':True,'reason':str(error)}
        else:raise ValueError('accepted cover mutation '+name)
    try:singular_cover(4,*args)
    except ValueError as error:result['negative_controls']['apply_singular_theorem_to_anisotropic_mask4']={'rejected':True,'reason':str(error)}
    else:raise ValueError('anisotropic negative control accepted')
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'singular_pivots':{s:{'chi':r['proper_cover_charge'],'one_chart_receivers':r['one_chart_receivers'],'carriers':r['chosen_carriers']}for s,r in result['singular_pivots'].items()},'negative_controls':len(result['negative_controls']),'scope':'proper-cover specialization only; full-eight acquisition unassumed'},sort_keys=True))
if __name__=='__main__':main()
