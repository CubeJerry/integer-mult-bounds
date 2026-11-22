#!/usr/bin/env python3
"""Universal fixed-H isolation gate, including arbitrary full source tuples."""
from pathlib import Path
import argparse, hashlib, importlib.util, json
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('isolation_gf64',HERE.parent/'check.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def main(repo,out):
    root=repo/'research/moonshot-005-program/results';four=root/'bit-simultaneous-d1509-s032/output'
    files=[root/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',four/'D-WORD.json.gz',
           four/'PROPER.json.gz',four/'CONSTRAINED-GAUGES.json.gz',four/'SOURCES.json.gz',
           four/'H-PHYSICAL.json.gz',root/'bit-fifth-receiver-quotient-s032/WITNESS.json',
           root/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz']
    z,dw,proper,gauges,sources,physical,old_witness,fibres=map(m.read,files)
    layout_path=root/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    layout=m.read(layout_path);files.append(layout_path)
    roots=layout['root_table'];charts=list(map(set,layout['D4']));planes=list(map(set,layout['A2']))
    adjacency={r:{j for j,y in enumerate(roots) if j!=r and sum(a*b for a,b in zip(roots[r],y))==0}
               for r in range(len(roots))}
    L=np.array(z['common_frames'],dtype=np.uint8);W=np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8);K=m.mm(L,W)
    m.need(not np.any(W[:16]) and m.rank(W[16:24])==m.rank(W[24:32])==4,'two full-rank coefficient blocks')
    Hby={tuple(x[:3]):int(h) for h,v in physical.items() for name in ['X_owners','Y_owners'] for x in v[name]}
    records=[];matrices={}
    for j in z['donors']:
        parents={int(k.split('/')[1]) for k in z['systems'] if k.startswith(str(j)+'/')}
        labels=[tuple(x) for x in proper[str(j)]['95']['labels']]
        input_labels={tuple(dw['owners'][q][:3]) for q in z['D_inputs'][str(j)]}
        ix=[q for q,label in enumerate(labels) if Hby[label] in parents and label not in input_labels]
        A=m.mm(np.array(proper[str(j)]['95']['matrix'],dtype=np.uint8),np.array(gauges['gauges'][str(j)],dtype=np.uint8))
        C=m.mm(A[ix],L[:,16:32]);N=m.null(C)
        m.need(len(ix)==16 and C.shape==(16,16),'sixteen parent offD rows')
        record=dict(donor=j,rank=m.rank(C),kernel_dimension=N.shape[1],
                    first_projection_rank=m.rank(N[:8]),second_projection_rank=m.rank(N[8:]))
        records.append(record);matrices[j]=(C,N,A,labels,ix)
    bad=[32,35,38,45,68,69,90,100]
    for record in records:
        if record['donor'] in bad:
            m.need(record['rank']==12 and record['kernel_dimension']==4 and
                   record['first_projection_rank']==record['second_projection_rank']==2,'universal obstruction profile')
    C,N,A32,labels32,ix32=matrices[32]
    # Direct full-30-input H reconstruction avoids assuming that new sources
    # continue to use only the old six protected record coordinates.
    protected=list(range(48))+list(range(240,288));prows=[0,1,2,15,16,17]
    factors=[]
    parents=sorted({int(k.split('/')[1]) for k in z['systems'] if k.startswith('32/')})
    for h in parents:
        physical_h=physical[str(h)];xs=physical_h['X_owners'];ys=physical_h['Y_owners']
        Q=np.array(sources['frames'][f'32/{h}'],dtype=np.uint8)
        xx=[q for q,x in enumerate(xs) if x[1]==32];yy=[q for q,x in enumerate(ys) if x[6]==32]
        m.need(len(xx)+len(yy)==30 and m.rank(Q)==30,'literal full source phase frame')
        XE=np.zeros((len(xs),30),dtype=np.uint8);YL=np.zeros((len(ys),30),dtype=np.uint8)
        XE[xx]=Q[:len(xx)];YL[yy]=Q[len(xx):]
        early=np.array(physical_h['early'],dtype=np.uint8);late=np.array(physical_h['late'],dtype=np.uint8)
        cross=np.array(physical_h['cross'],dtype=np.uint8)
        full=np.vstack([m.mm(early,XE),m.mm(cross,XE)^m.mm(late,YL)])
        full_labels=[tuple(x[:3]) for x in xs+ys]
        sections={}
        for r in [6,9,48,73,95]:
            labels=[tuple(x) for x in proper['32'][str(r)]['labels']]
            chosen=[label for label in labels if Hby[label]==h]
            section=full[[full_labels.index(label) for label in chosen]]
            m.need(section.shape==(6,30) and m.rank(section)==6,'full-input proper section')
            sections[r]=section
        D=sections[48][:,prows]
        projection=m.mm(m.inverse(D),sections[48])
        m.need(np.array_equal(projection[:,prows],np.eye(6,dtype=np.uint8)),'effective quotient normalization')
        for r,section in sections.items():
            factor=section[:,prows]
            m.need(m.rank(factor)==6 and np.array_equal(m.mm(factor,projection),section),
                   'all thirty input rows factor through one common quotient')
        source=np.array(sources['paired_maps']['32'][str(h)],dtype=np.uint8)[:,protected]
        rows=[q for q,label in enumerate(labels32) if Hby[label]==h]
        m.need(np.array_equal(m.mm(sections[95],source),A32[rows]),'full physical map reproduces frozen proper rows')
        whole_sections={}
        for r in [48,73]:
            positions=[q for q,owner in enumerate(xs+ys) if charts[owner[4]]<=adjacency[r]]
            whole=full[positions]
            m.need(whole.shape==(30,30) and m.rank(whole)==30,'whole thirty-row H section')
            whole_labels=[full_labels[q] for q in positions]
            inputs=[tuple(dw['owners'][q][:3]) for q in z['D_inputs']['32']]
            E=np.zeros((30,8),dtype=np.uint8)
            for q,label in enumerate(whole_labels):
                if label in inputs:E[q,inputs.index(label)]=1
            Sr=np.array(dw['matrix'],dtype=np.uint8)[np.ix_(z['D_outputs'][str(r)],z['D_inputs']['32'])]
            Lr=L[:,16:24] if r==48 else L[:,24:32]
            m.need(np.array_equal(m.mm(m.mm(m.mm(whole,source),Lr),Sr),E),
                   'full thirty-row retained isolation and readout identity')
            whole_sections[str(r)]=dict(output_labels=whole_labels,matrix=whole.tolist(),D_insertion=E.tolist())
        factors.append(dict(H=h,full_input_projection=projection.tolist(),
                            source_phase_frame=Q.tolist(),
                            full_thirty_by_thirty_sections=whole_sections,
                            receiver_factors={str(r):section[:,prows].tolist() for r,section in sections.items()},
                            full_sections={str(r):section.tolist() for r,section in sections.items()}))
    # K is forced at every one of donor61's sixteen visible quotients by
    # retained H observations alone. The earlier reviewed visibility labels
    # identify actual H generators; no D generator is used in this check.
    source61=[]
    expected_h=sorted(int(h) for h in sources['paired_maps']['61'] if planes[int(h)]<=adjacency[95])
    m.need(sorted(item['H'] for item in old_witness['quotient_decompositions'])==expected_h,
           'all and only source61 quotients visible at95')
    for item in old_witness['quotient_decompositions']:
        cols=[];labels=[]
        for typ,h,r,q in item['generator_labels']:
            if typ!='H':continue
            m.need(r<111 and h in [263,642],'native retained H generator')
            m.need(61 in planes[h] and planes[item['H']]<=adjacency[r],
                   'actual source61 native H observation geometry')
            C0=np.array(fibres[str(h)][str(r)]['kernel'],dtype=np.uint8)[:48,:3]
            zero=np.zeros_like(C0);C2=np.block([[C0,zero],[zero,C0]])
            cols.append(C2[:,q]);labels.append([typ,h,r,q])
        all_columns=np.column_stack(cols);pivots=m.rref(all_columns)[1]
        basis=all_columns[:,pivots];coeff=m.solve(basis,K)
        m.need(m.rank(basis)==(60 if item['H'] in [263,642] else 54),'H-only forced-space rank')
        source61.append(dict(H=item['H'],generator_labels=[labels[q] for q in pivots],K_coefficients=coeff.tolist()))
    m.need(len(source61)==16,'every source61 visible quotient')
    C61,N61,A61,labels61,ix61=matrices[61]
    input61={tuple(dw['owners'][q][:3]) for q in z['D_inputs']['61']}
    off61=[q for q,label in enumerate(labels61) if label not in input61]
    m.need(not np.any(m.mm(A61[off61],K)),'all88 old source61 offD rows vanish')
    m.need(not np.any(m.mm(C61,W[16:])), 'real source61 positive control')
    # Projection obstruction controls.
    needrows=np.flatnonzero(np.any(N,axis=1));corrupt=C.copy();corrupt[0,int(needrows[0])]^=1
    m.need(np.any(m.mm(corrupt,N)),'kernel matrix corruption rejected')
    m.need(not np.any(m.mm(C,N)) and m.rank(N[:8])==2,'rank-two kernel-block positive control')
    result=dict(status='PASS_UNIVERSAL_FIXED_H_RECEIVER95_ISOLATION_GATE',
        kernel_projection_profiles=records,obstructed_donors=bad,uniform_forced_leakage_lower_rank=2,
        arbitrary_full_30_row_source_tuples_covered=True,common_invertible_D_readout_rebasings_covered=True,
        independently_checked_full_H_sections=8,full_source_tuple_witness_donor=32,
        arbitrary_changed_D_word_covered=True,fixed_affine_rectangle_required=False,
        retained_D_subspaces_needed=[48,73],source61_H_only_quotients=16,
        literal_H_words_and_H_interfaces_fixed=True,changed_H_processing_excluded=False,
        changed_retained_D_subspaces_excluded=False,new_complete_kappa=False,
        controls=['real source61 isolated four-space','rank-two projected kernel','corrupted kernel matrix'])
    certificate=dict(donor32_parent_rows=ix32,donor32_parent_labels=[labels32[q] for q in ix32],
        donor32_matrix=C.tolist(),donor32_kernel=N.tolist(),W48=W[16:24].tolist(),W73=W[24:32].tolist(),
        full30_source_factors=factors,source61_H_only_decompositions=source61)
    pins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    expected=HERE/'ISOLATION-SOURCE-PINS.json'
    if expected.exists():m.need(pins==m.read(expected),'isolation source pins')
    out.mkdir(parents=True,exist_ok=True)
    for name,value in [('RESULT',result),('CERTIFICATE',certificate),('SOURCE-PINS',pins)]:
        (out/(name+'.json')).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
