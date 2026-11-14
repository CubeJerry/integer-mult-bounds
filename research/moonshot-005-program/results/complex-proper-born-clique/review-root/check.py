#!/usr/bin/env python3
"""Independent rational whole-source review; no author replay imported.

Reuses the previously independently authored root replay kernel, credited in
REVIEW.md. @CubeJerry with OpenAI assistance. Apache-2.0.
"""
import argparse, copy, gzip, hashlib, importlib.util, json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def rank(rows):
    basis = {}
    for original in rows:
        row = dict(original)
        for j in sorted(basis):
            if j in row:
                c = row[j]
                for k, value in basis[j].items():
                    v = row.get(k, F(0)) - c * value
                    if v: row[k] = v
                    else: row.pop(k, None)
        if row:
            j = min(row); c = row[j]
            basis[j] = {k: v / c for k, v in row.items()}
    return len(basis)

def determinant(matrix):
    a = [[F(v) for v in row] for row in matrix]; answer = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None: return F(0)
        if pivot != j: a[j], a[pivot] = a[pivot], a[j]; answer = -answer
        x = a[j][j]; answer *= x
        a[j] = [v/x for v in a[j]]
        for i in range(j+1, len(a)):
            c = a[i][j]
            a[i] = [v-c*w for v,w in zip(a[i], a[j])]
    return answer

def root_vector(bits):
    on = [i for i in range(9) if bits >> i & 1]
    if len(on) == 3: return [2 if i in on else -1 for i in range(9)]
    off = [i for i in range(9) if not (bits >> i & 1)]
    need(len(off) == 2, 'native real root type')
    return [3*(int(i == off[0])-int(i == off[1])) for i in range(9)]

def main():
    parser = argparse.ArgumentParser()
    for name in ['package', 'native', 'seed', 'output']:
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location('independent_source_replay', Path(__file__).with_name('engine.py'))
    eng = importlib.util.module_from_spec(spec); spec.loader.exec_module(eng)
    def read_gz(path, expected=None):
        raw = path.read_bytes()
        if expected: need(hashlib.sha256(raw).hexdigest() == expected, 'source byte pin')
        return json.loads(gzip.decompress(raw))
    native = read_gz(args.native, '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883')
    seed = read_gz(args.seed, '6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc')
    need(hashlib.sha256((args.package/'PROOF.md').read_bytes()).hexdigest() == '283856e52457e1b62fcfc7d8afe42b61d7d601af81bba00baef5e5746abecc93', 'frozen proof pin')
    parent = eng.replay(seed); role = {int(k): v for k,v in seed['source_role_map'].items()}
    live = native['live']; pairs = {live[i]:(role[b], role[d]) for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    roots = {h:root_vector(native['frames'][native['initial'][h]][0]) for h in live}
    gram = {(h,j):F(sum(x*y for x,y in zip(roots[h], roots[j])),18) for h in live for j in live}
    omitted = [root_vector(v) for v in seed['duplex']['omitted_frame']]
    g = [{h:F(sum(x*y for x,y in zip(v,roots[h])),18) for h in live} for v in omitted]
    small = [[F(int(i==j))-sum(g[i][h]*g[j][h] for h in pairs) for j in range(8)] for i in range(8)]
    det = determinant(small)
    need(det == F(415068771,2), 'exact inherited nonzero determinant reproduced')
    seed_profile = {r:parent[2].get(r,0)+parent[3].get(r,0) for r in set(parent[2])|set(parent[3])}
    answers = []
    for k in (2,4,8):
        path = args.package/'output'/('k'+str(k))/'WORD.json.gz'; w = read_gz(path)
        m = w['clique_compiler']; J = m['clique']; need(J == [48,50,71,80,87,98,103,105][:k], 'actual native cohort')
        spaces = [eng.span(f) for f in w['frames']]
        labels = {h:native['frames'][native['initial'][h]][0] for h in J}
        need(all(((labels[h]&labels[j]).bit_count()%2)==int(h==j) for h in J for j in J), 'binary orthonormal cohort')
        need(all(gram[h,j] for h in J for j in J), 'real pairwise nonorthogonal cohort')
        need(all(h in pairs for h in J), 'all selected ports hosted')
        P = eng.span(list(labels.values())); need(len(w['frames'][m['plane']])==k and spaces[m['plane']]==P, 'authentic birth plane')
        geom_checks = 0
        for ii,h in enumerate(J):
            for length in range(k):
                frame = [labels[J[(ii+l)%k]] for l in range(1,length+1)]
                c = m['interval_charts'][str(h)][length]
                need(spaces[c] == eng.span(frame), 'actual cyclic receiver flag')
                need(spaces[c] < spaces[parent[1][role[h+112]]], 'receiver chart remains proper')
                geom_checks += 1
        expected = copy.deepcopy(parent[0])
        for h in J:
            expected[role[h+112]] = eng.plus({role[h+112]:F(1)}, parent[0][role[h]], F(1))
        for j,(b,d) in pairs.items():
            for h in J:
                expected[b] = eng.plus(expected[b], {pairs[h][1]:F(1)}, gram[h,j]-F(int(h==j)))
        sum_a = {}; sum_d = {}
        for h in J:
            sum_a = eng.plus(sum_a, parent[0][role[h]], F(1))
            sum_d = eng.plus(sum_d, {pairs[h][1]:F(1)}, F(1))
        r_expected = [{} for _ in range(8)]; f_expected = [{} for _ in range(8)]
        for i in range(8):
            for h in live: f_expected[i] = eng.plus(f_expected[i], parent[0][role[h]], g[i][h])
            for h in pairs:
                if h not in J: r_expected[i] = eng.plus(r_expected[i], {pairs[h][1]:F(1)}, g[i][h])
        need(rank(f_expected+[sum_a])==9, 'independent ninth global row')
        moving=set(); generations={}; old_checks=[]; source_reads=0; dirty=[]
        cache_pair={int(value):tuple(map(int,key.split(','))) for key,value in m['cache_roles'].items()}
        private_dir={}; private_mass=Counter()
        def hook(t,when,o,rows,loc):
            nonlocal source_reads
            if when=='before':
                if t in m['events']['source_cache_copies']:
                    need(o[0]=='ADD' and o[1] in cache_pair,'explicit stationary cache write')
                    h,j=cache_pair[o[1]]
                    need(o[2]==role[j] and rows[o[2]]==parent[0][role[j]], 'cache reads authentic unaltered X')
                    source_reads+=1
                if o[0]=='CLEAR' and o[1]>=408:
                    if o[1]==m['new_q_role']: want=sum_d
                    elif o[1]==m['new_W_role']: want=sum_a
                    else: want=parent[0][role[cache_pair[o[1]][1]]]
                    need(rows[o[1]]==want and bool(want),'every new nonzero retirement recorded')
                    dirty.append(o[1])
                return
            if o[0]=='INIT': generations[o[1]]=t
            if o[0]=='MOVE':
                i,c,d,owned=o[1:]
                if owned:
                    moving.add((i,generations[i]))
                    if i==m['new_q_role']:need(rows[i]==sum_d and spaces[c]==frozenset({0}) and spaces[d]==P, 'true paired reverse sum transfer')
                    if i==m['new_W_role']:need(rows[i]==sum_a and spaces[c]==P and spaces[d]==frozenset({0}), 'true forward sum transfer')
                    need(i not in cache_pair,'no cache secretly moves')
                else:
                    sign=1 if spaces[c]<spaces[d] else -1
                    need(private_dir.get(i,sign)==sign, 'all private routes monotone')
                    private_dir[i]=sign;private_mass[i]+=abs(len(w['frames'][d])-len(w['frames'][c]))
            if t==m['markers']['old_reverse_modes_acquired_without_selected_D']:
                need(all(rows[400+i]==r_expected[i] for i in range(8)), 'all old reverse payloads omit exactly selected D')
                old_checks.append('reverse_modes')
            if t==m['markers']['old_forward_modes_at_lines']:
                need(all(rows[400+i]==f_expected[i] for i in range(8)), 'all old forward modes preserved')
                old_checks.append('forward_modes')
            if t==m['markers']['all_D_original_at_final_facets']:
                need(all(rows[d]=={d:F(1)} and loc[d]==parent[1][d] for b,d in pairs.values()), 'all D authentic at final facets')
                old_checks.append('D_endpoints')
            if t==m['markers']['selected_Y_exactly_completed']:
                need(all(rows[role[h+112]]==expected[role[h+112]] for h in J), 'selected Y complete before old mode usage')
                old_checks.append('selected_Y')
        result=eng.replay(w,hook=hook)
        need(result[0]==expected and result[1]==parent[1], 'all400 exact output rows and final endpoint IDs')
        need(rank(result[0].values())==400,'all400 independent inputs retained')
        need(source_reads==k*(k-1) and len(dirty)==k*(k-1)+2, 'all new cache reads and dirty retirements')
        need(len(moving)==26 and result[6]==26+k*(k-1) and result[5]==9+k*(k-1), 'exact moving/total lifetime and peak counts')
        need(sum(private_mass.values())==3200 and len(private_mass)==400, 'all original private rank mass')
        paired=0
        for h in pairs:
            for j in pairs:
                need(result[0][pairs[j][0]].get(pairs[h][1],F(0))+result[0][role[h+112]].get(role[j],F(0))==0,'full hosted transpose identity')
                paired+=1
        residual=[eng.plus(eng.plus(result[0][b],{b:F(1)},-1),{d:F(1)},1) for b,d in pairs.values()]
        need(rank(residual)==96-k,'exact residual rank')
        codecs=0
        for before,after,receipt in zip(seed['duplex']['groups'],m['old_groups'],m['codec_determinants']):
            ports=before['ports']; pivots={ports[i] for i in before['pivots']}
            need(not (pivots&set(J)), 'no old pivot deleted')
            for matrix_name,det_name in [('M_D','D_determinant'),('M_Y','Y_determinant')]:
                # D matrices index hosted ports; Y matrices index every class port.
                original_ports=before['hosted'] if matrix_name=='M_D' else ports
                keep=[i for i,h in enumerate(original_ports) if h not in J]
                original=before[matrix_name]
                reduced=[[original[i][j] for j in keep] for i in keep]
                need(reduced==after[matrix_name], 'codec is literal row/column deletion')
                need(determinant(original)==determinant(reduced)==F(receipt[det_name])!=0, 'original and reduced exact determinant')
                codecs+=1
        for o in w['program']:
            if o[0] in ['ADD','SCALE']:
                denominator=F(o[3] if o[0]=='ADD' else o[2]).denominator
                need(denominator&(denominator-1)==0,'every coefficient dyadic')
        author=json.loads((args.package/'output'/('k'+str(k))/'RESULT.json').read_text())
        need({str(r):n for r,n in result[2].items()}==author['raw_histogram'] and {str(r):n for r,n in result[3].items()}==author['owned_histogram'],'independent complete movement profile')
        need(result[4]==author['source_bill']['counts'],'all ordinary operations counted')
        negatives=[]
        for key in ['W_sources','new_q_sources','local_B_adds','local_Y_subtractions','old_reverse_consumers']:
            idx=m['events'][key][0];bad=copy.deepcopy(w)
            need(bad['program'][idx][0]=='ADD','targeted semantic mutation')
            bad['program'][idx][3]='0';changed=eng.replay(bad)
            need(changed[0]!=expected,'omission must change public map: '+key);negatives.append(key)
        answers.append(dict(size=k,word_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),all400_rows=True,all_endpoint_ids=True,input_rank=400,paired_entries=paired,residual_rank=96-k,global_history_rank=9,raw=result[2],owned=result[3],counts=result[4],peak=result[5],lifetimes=result[6],moving_lifetimes=len(moving),stationary_lifetimes=k*(k-1),nonzero_new_retirements=len(dirty),cyclic_chart_checks=geom_checks,codec_determinants=codecs,old_source_checks=old_checks,seed_profile=seed_profile,negative_controls=negatives))
    report=dict(status='PASS_INDEPENDENT_PAIRED_CLIQUE_SOURCE_REVIEW',proof_sha256=hashlib.sha256((args.package/'PROOF.md').read_bytes()).hexdigest(),hosted_determinant=str(det),variants=answers,scope='Exact native rational source and reviewed all-volume chronology; owned erasure and all other foundations retained. Partial words only; no new kappa.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'])
if __name__=='__main__': main()
