"""Read-only exact-source/geometry gate; no physical or payload execution.
Apache-2.0. Prepared with substantial OpenAI Codex assistance.
"""
from pathlib import Path
from hashlib import sha256, sha1
import argparse
import gzip
import json
import os
import subprocess

HERE = Path(__file__).resolve().parent
MAIN = 'e54523517d0f03e58352e647c403a5af3e525a57'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def gamma_length(n):
    need(n > 0, 'positive Gamma integer')
    return 2*n.bit_length()-1

def build(repo):
    sources = json.loads((HERE/'SOURCES.json').read_text())
    blobs = {}
    for pin in sources['canonical_files']:
        raw = subprocess.check_output(['git', 'show', MAIN+':'+pin['path']],
            cwd=repo, env={**os.environ, 'GIT_NO_LAZY_FETCH': '1'})
        need(len(raw) == pin['bytes'] and sha256(raw).hexdigest() == pin['sha256'],
             'source byte/hash drift: '+pin['path'])
        blob = sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        need(blob == pin['git_blob'], 'source Git blob drift')
        blobs[pin['path']] = raw
    word = json.loads(gzip.decompress(blobs['research/shared-wire-split-composition/data/final.json.gz']))
    canonical = json.dumps(word, sort_keys=True, separators=(',', ':')).encode()
    need(sha256(canonical).hexdigest() == '91429a6b96729292a8764836e00c87a6f7cd3b76f05159033f4867f69a98d097', 'word drift')
    caller = json.loads(blobs['research/shared-wire-split-composition/data/caller.json'])
    ci, event = next((i,e) for i,e in enumerate(caller['events']) if e[0] == 'J')
    move = word['program'][28141]
    need((ci,event) == (21,['J',1,[1,0,19,20],[39,38,'-1','1/2']]), 'first actual invocation')
    need(caller['ambient_rank'] == 153 and word['public'] == 1480 and word['owned_fields'] == 51, 'actual inventory')
    need(move == ['MOVE',1526,601,470,True], 'actual MOVE')
    need(word['frames'][601] == [137] and word['frames'][470] == [75,137,265], 'actual full frames')

    # Functional geometry fixture, not a selected asymptotic family or DATA run.
    P0,S0,r,K,rho = 3,5,2,3,0
    Dtotal,q0,qF,qB,W = 309,1,1,1,3
    Droot = Dtotal-q0-qF-qB
    L = (Dtotal-q0)*K
    row_stock = W**2
    row_initial = 1 << (q0*K)
    row_padded = ((row_initial+row_stock-1)//row_stock)*row_stock
    Rj = row_padded//W
    need(row_initial == 8 and row_padded == 9 and Rj == 3, 'nonbinary ROW fixture')
    need(row_initial <= row_padded < 2*row_initial, 'single padding bound')
    need(sorted(W*g+role for role in range(W) for g in range(Rj)) == list(range(row_padded)), 'whole ROW reassembly')
    p0 = 512
    Q0 = q0+qF+qB
    w = p0+2*Dtotal+4
    need((p0+Q0)+(Q0+1)+2*Droot+3 == w, 'current-root signed width')
    need((p0+Q0)+Droot == p0+Dtotal, 'current-root fractional width')

    def coordinates(f, wrong=False):
        need(153*f <= Droot, 'raw caller fits complete root')
        selected = [(qF+a*f+j)*K+(rho if wrong else K-1-rho)
                    for a in range(9) for j in range(f)]
        remaining = [i for i in range(L) if i not in set(selected)]
        need(len(set(selected)) == 9*f and sorted(selected+remaining) == list(range(L)), 'complete coordinate permutation')
        return selected, remaining

    def pack(x,f,wrong=False):
        selected, remaining = coordinates(f,wrong)
        bits = format(x, '0'+str(L)+'b')
        return int(''.join(bits[i] for i in selected+remaining),2)

    def unpack(y,f):
        selected, remaining = coordinates(f)
        bits = format(y, '0'+str(L)+'b')
        out = ['0']*L
        for i,b in zip(selected+remaining,bits):
            out[i] = b
        return int(''.join(out),2)

    def chunk_oracle(x,f):
        key = 0
        for a in range(9):
            for j in range(f):
                chunk = qF+a*f+j
                value = (x >> ((Dtotal-q0-1-chunk)*K)) & ((1<<K)-1)
                key = 2*key+((value>>rho)&1)
        return key

    cases = 0
    mixed = sum(1<<i for i in range(0,L,3))
    for f in (1,2):
        selected, remaining = coordinates(f)
        samples = [0,(1<<L)-1,mixed,((1<<L)-1)^mixed]
        samples += [1<<i for i in range(L)]
        # Every nine-bit native pattern, with opaque spectator bits present.
        for key in range(512):
            y = (key << (L-9*f)) | ((1<<(L-9*f))-1)
            samples.append(unpack(y,f))
        for x in samples:
            y = pack(x,f)
            need(unpack(y,f) == x, 'full complement roundtrip')
            need(y >> (L-9*f) == chunk_oracle(x,f), 'independent chunk-LSB/native-MSB oracle')
            cases += 1
    witness = 1 << (L-1-coordinates(1)[0][0])
    need(pack(witness,1) != pack(witness,1,True), 'wrong rho convention must be detected')

    headers = []
    volume = 2*P0*Rj*S0*r*(1<<L)*w
    for f in (1,2):
        P = P0*Rj
        S = S0 << (L-9*f)
        cutoff = 4  # Syntax/control only; no selected cutoff policy asserted.
        theta = [f,r,P,S,w,cutoff]
        v = 2*P*S*r*(1<<(9*f))*w
        E = sum(map(gamma_length,theta))
        need(v == volume, 'all spectator and coefficient DATA retained')
        headers.append({'f':f,'r':r,'P':P,'S_form':'5*2^'+str(L-9*f),
            'w':w,'cutoff_fixture_only':cutoff,'E':E,'volume_bit_length':v.bit_length()})
    need(headers[0]['E']-headers[1]['E'] == 16, 'unequal native header length control')
    need((headers[0]['E']+volume)-(headers[1]['E']+volume) == 16, 'combined body would change; DATA-only body does not')
    naive = 2*P0*Rj*S0*r*(1<<Droot)*w
    dropped = 2*P0*Rj*S0*r*(1<<(L-Droot+9))*w
    need(volume == naive*(1<<(L-Droot)), 'unselected/compact omission control')
    need(volume == dropped*(1<<(Droot-9)), 'completed selected-root omission control')
    guard_cases = 0
    for p in range(2,10):
        for D in range(13):
            for n in (-(1<<p),-1,0,1,1<<p):
                width = p+2*D+4
                target = n<<D
                need(-(1<<(width-1)) <= target < (1<<(width-1)), 'guard fit')
                need(target == n*(1<<D), 'unchanged exact quantum value')
                guard_cases += 1
    return {
        'marker':'PASS_SELECTED_COMMON_ROOT_HEADER_GATE',
        'actual_occurrence':{'caller_event_index':ci,'event':event,'native_index':28141,
            'native_event':move,'owner':['owned',ci,1526-word['public']],
            'frames':[[137],[75,137,265]],'ambient':153},
        'functional_fixture':{'K':K,'rho':rho,'D_total':Dtotal,'D_root':Droot,
            'within_row_bits':L,'initial_rows':row_initial,'padded_rows':row_padded,
            'role_rows':Rj,'P0':P0,'S0':S0,'r':r,'root_p':p0,
            'fractional_bits':p0+Dtotal,'root_w':w,
            'scope':'Functional geometry analogue, not an admitted selected family or scientific DATA run.'},
        'coordinate_roundtrips':cases,'guard_component_cases':guard_cases,
        'native_headers':headers,'header_length_difference':16,
        'lost_dimensions_if_compact_unselected_omitted':L-Droot,
        'lost_dimensions_if_selected_complement_omitted':Droot-9,
        'controls':['wrong rho MSB/LSB','omitted compact/unselected coordinates',
            'omitted completed selected-root complement','unequal Gamma6 E with identical DATA volume'],
        'verdict':'DATA-only F_HOME=v is source-compatible; source-indexed producer/packed-view wrapper remains unimplemented.',
        'runtime_claim':'None: host integer operations are verifier calculations only.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source-repo',type=Path,required=True)
    p.add_argument('--write',action='store_true')
    a = p.parse_args()
    result = build(a.source_repo.resolve())
    dest = HERE/'CHECK.json'
    if a.write:
        dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        need(result == json.loads(dest.read_text()), 'receipt drift')
    print('PASS_SELECTED_COMMON_ROOT_HEADER_GATE: exact source and complete geometry; no physical producer claimed.')
