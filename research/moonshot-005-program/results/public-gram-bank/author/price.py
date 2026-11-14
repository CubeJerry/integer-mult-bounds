#!/usr/bin/env python3
"""Exact source budgets for closed public retention and open owner retention."""
import argparse,gzip,hashlib,importlib.util,json
from pathlib import Path
ENGINE='82634fc558ec4eef0bb675b44c2eacb88f2e551d8093262ccbb004b7ef86eff1'
FULL='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
CHANGED='8a79133829b3329a9493e3cf1eb2218798903247fad7d2f2b53e24ae29f2831f'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main(args):
    if sha(args.engine)!=ENGINE or sha(args.full)!=FULL or sha(args.changed)!=CHANGED:raise ValueError('whole price source pins')
    sp=importlib.util.spec_from_file_location('public_Gram_interval',args.engine);p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
    full=json.loads(args.full.read_text());changed=json.loads(args.changed.read_text())
    slope=p.add((p.F(1,18),full['invoice']['T']),(-p.F(1,18),full['invoice']['P']))
    allowance=p.add((1,slope),(1,full['native']['paid']),(-1,full['native']['helpers']))
    oldpenalty=p.moment(p.add((-1,slope)));new=next(z for z in changed['complete_conversions']if z['variant']=='allhosted')
    newpenalty=tuple(p.F(x)for x in new['finite_m_penalty']);records=[]
    for variant in('retained','allhosted','open-retained'):
        r=json.loads((args.results/variant/'RESULT.json').read_text());p.need(sha(args.results/variant/'WORD.json.gz')==r['word_sha256'],'actual source word pin')
        Q={int(k):v for k,v in r['source_bill']['moves'].items()};outer={8:16}if variant=='allhosted'else{}
        penalty=newpenalty if variant=='allhosted'else oldpenalty
        room=p.moment(p.add((1,allowance),(1,outer),(-1,Q)))
        m=next(m for m in range(2,100000)if room[0]-penalty[1]/(m-1)>0)
        row={'variant':variant,'word_sha256':r['word_sha256'],'actual_Q':Q,'limiting_MOVEmargin':room,
            'finite_m_penalty':penalty,'first_positive_MOVEmargin_m':m,'original_D_unrestored':76,
            'reverse_residual_rank':8,'all_forward_work_unfinished':True,
            'open_owned_outputs':8 if variant=='open-retained'else 0,'owned_peak':r['source_bill']['peak']}
        records.append(row)
    old=next(r for r in records if r['variant']=='retained');opened=next(r for r in records if r['variant']=='open-retained')
    p.need(p.add((1,old['actual_Q']),(-1,opened['actual_Q']))=={1:8},'exact eight paid pivot reads distinguish the closed400 word')
    continuation={2:7,8:1};cost=p.moment(continuation);future=[]
    nativepath=Path(__file__).resolve().parent/'dependencies'/'native-retained.json.gz'
    p.need(sha(nativepath)=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','actual next-basis native pin')
    native=json.loads(gzip.decompress(nativepath.read_bytes()));I=[0,7,20,27,36,46,57,111];M=[19,30,38,40,47,52,60]
    def root(h):
        v=native['frames'][native['initial'][h]][0];one=[i for i in range(9)if v>>i&1]
        if len(one)==3:return [p.F(2 if i in one else -1)for i in range(9)]
        z=[i for i in range(9)if i not in one];p.need(len(z)==2,'actual root normal')
        return [p.F(3*(int(i==z[0])-int(i==z[1])))for i in range(9)]
    roots={h:root(h)for h in native['live']}
    def G(h,j):return sum(x*y for x,y in zip(roots[h],roots[j]))/18
    matrix=[[G(u,i)for i in I]for u in M]+[[p.F(i==0)for i in I]]
    A=[row[:]+[p.F(i==j)for j in range(8)]for i,row in enumerate(matrix)];det=p.F(1)
    for j in range(8):
        k=next(k for k in range(j,8)if A[k][j])
        if k!=j:A[k],A[j]=A[j],A[k];det=-det
        a=A[j][j];det*=a;A[j]=[x/a for x in A[j]]
        for k in range(8):
            if k!=j:
                a=A[k][j];A[k]=[x-a*y for x,y in zip(A[k],A[j])]
    p.need(det==-p.F(1,16),'seven actual modes plus q0 have unit dyadic determinant')
    inverse=[row[8:]for row in A];gamma={h:[sum(G(h,I[i])*inverse[i][j]for i in range(8))for j in range(8)]for h in native['live']}
    p.need(all(z.denominator&(z.denominator-1)==0 for row in gamma.values()for z in row),'every proposed B consumer is dyadic')
    p.need(all(G(h,j)==sum(gamma[h][i]*G(u,j)for i,u in enumerate(M))+gamma[h][7]*G(0,j)
               for h in native['live']for j in native['live']),'all actual full Gram duties in the retained bank-plus-q0 basis')
    for r in records[:2]:
        residual=(r['limiting_MOVEmargin'][0]-cost[1],r['limiting_MOVEmargin'][1]-cost[0])
        p.need(residual[0]>0,'seven actual bank continuations plus one genuine q pickup fit the incomplete-source allowance')
        future.append({'variant':r['variant'],'continuation_profile':continuation,'remaining_after_reverse_only_extension':residual,
            'status':'Source-bound constructive next mechanism; separate extended word not emitted.76 D restorations and full forward endpoint still unresolved.'})
    freshforward=p.moment({8:8})
    p.need(all(r['limiting_MOVEmargin'][1]<freshforward[0]for r in records),
           'even eight fresh full-route forward modes alone exceed these retained source allowances')
    out={'status':'PASS_PUBLIC_AND_OPEN_GRAM_RETENTION_WHOLE_PRICES','exponent':'199/200',
        'full_receipt_sha256':FULL,'changed_interface_price_sha256':CHANGED,'interval_engine_sha256':ENGINE,
        'variants':records,'reverse_only_continuation_cost':cost,'source_bound_next_continuations':future,
        'reverse_continuation_basis':{'stationary_mode_ports':M,'additional_public_pivot':0,'determinant':det,'actual_consumer_coefficients':gamma},
        'fresh_eight_full_rank8_forward_modes_cost':freshforward,
        'separated_completion_scope':'A completion adding eight fresh full rank8 forward mode routes cannot fit, even if every other missing operation is free. Reusing/changing funded histories or other geometry is not excluded.',
        'scope':'Incomplete sources only. The open interface retains eight live owned outputs; eventual transport, storage, correction and closure remain paid obligations. No supplier and no new kappa.'}
    args.output.write_text(json.dumps(p.enc(out),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'sources':[{'variant':r['variant'],'room':float(r['limiting_MOVEmargin'][0]),'m':r['first_positive_MOVEmargin_m']}for r in records],
        'reverse_only_next_cost':float(cost[0]),'fresh_forward_cost':float(freshforward[0])},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--full',type=Path,required=True);p.add_argument('--changed',type=Path,required=True)
    p.add_argument('--engine',type=Path,required=True);p.add_argument('--results',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
