#!/usr/bin/env python3
"""Paid sign-quotient prefix with all input copies at their source lines. No new kappa."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip
import hashlib
import json
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y):
    return sum(a*b for a, b in zip(x, y))


def rref(rows):
    a = [[F(x) for x in r] for r in rows]
    p = 0
    for c in range(8):
        q = next((i for i in range(p, len(a)) if a[i][c]), None)
        if q is None:
            continue
        a[p], a[q] = a[q], a[p]
        scale = a[p][c]
        a[p] = [x/scale for x in a[p]]
        for j in range(len(a)):
            if j != p:
                scale = a[j][c]
                a[j] = [x-scale*y for x, y in zip(a[j], a[p])]
        p += 1
    return tuple(tuple(row) for row in a[:p])


def perpendicular(basis):
    b = rref(basis)
    pivots = [next(i for i, x in enumerate(row) if x) for row in b]
    out = []
    for f in range(8):
        if f in pivots:
            continue
        v = [F(0)]*8
        v[f] = 1
        for p, row in zip(pivots, b):
            v[p] = -row[f]
        out.append(v)
    return rref(out)


def included(a, b):
    return len(rref(list(a)+list(b))) == len(b)


def encode_basis(basis):
    return [[int(x) if x.denominator == 1 else str(x) for x in row] for row in basis]


def replay(word):
    frames = {int(c): f for c, f in word['frames'].items()}
    spaces = {c: rref(f['B']) for c, f in frames.items()}
    for c, f in frames.items():
        need(len(spaces[c]) == f['dim'], ('chart rank', c))
        a = rref(f['A'])
        need(len(a)+len(spaces[c]) == 8 and all(dot(x, y) == 0 for x in a for y in spaces[c]),
             ('chart orthogonal complement', c))
    where = dict(enumerate(word['start']))
    rows = {i: 1 << i for i in range(222)}
    counts = Counter()
    paid = Counter()
    lifetimes = peak = 0
    clears = []
    snapshots = {}
    selected = set(word.get('snapshot_indices', []))
    move_pairs = set()
    routes = {i: [where[i]] for i in rows}
    for n, op in enumerate(word['program']):
        kind, a = op[:2]
        counts[kind] += 1
        if kind == 'INIT':
            need(a >= 222 and a not in rows, ('zero-born owned field', n, op))
            rows[a], where[a] = 0, op[2]
            routes[a] = [op[2]]
            lifetimes += 1
            peak = max(peak, len(rows)-222)
        elif kind == 'ADD':
            _, a, b, c = op
            need(a != b and a in rows and b in rows and where[a] == where[b] == c,
                 ('cocharted active ADD', n, op))
            rows[a] ^= rows[b]
        elif kind == 'MOVE':
            _, a, c, d = op
            need(a in rows and where[a] == c, ('MOVE source', n, op))
            dc, dd = len(spaces[c]), len(spaces[d])
            need(abs(dc-dd) == 1, ('unit-rank MOVE', n, op))
            small, large = (spaces[c], spaces[d]) if dc < dd else (spaces[d], spaces[c])
            need(included(small, large), ('real chart inclusion', n, op))
            direction = word['directions'].get(str(a), 'up' if a < 222 else 'stationary')
            need((dd > dc if direction == 'up' else dd < dc if direction == 'down' else False), ('declared monotone direction', n, op))
            where[a] = d
            routes[a].append(d)
            paid[abs(dc-dd)] += 1
            move_pairs.add((c, d))
        elif kind == 'CLEAR':
            _, a, c = op
            need(a >= 222 and a in rows and where[a] == c, ('owned CLEAR', n, op))
            clears.append({'operation': n, 'field': a, 'chart': c, 'row_hex': hex(rows[a])})
            del rows[a]
            del where[a]
        else:
            raise ValueError(('unsupported operation', n, op))
        if n in selected:
            snapshots[str(n)] = {'rows': {str(i): hex(rows[i]) for i in (111, 112, 222, 223, 224, 225) if i in rows},
                                 'all_X_restored_at_Hub': all(rows[i] == 1 << i and where[i] == word['hub'] for i in range(111))}
    need(set(rows) == set(range(222)) | set(word.get('end_owned', [])), 'exact live owned set at end')
    need([where[i] for i in range(222)] == word['final'], 'all public endpoint charts')
    return {'rows': [rows[i] for i in range(222)], 'owned_rows': {str(i): hex(rows[i]) for i in rows if i >= 222}, 'owned_where': {str(i): where[i] for i in rows if i >= 222}, 'counts': dict(counts),
            'paid_profile': dict(sorted(paid.items())), 'owned_lifetimes': lifetimes,
            'peak_owned': peak, 'clear_rows': clears, 'snapshots': snapshots,
            'routes': routes, 'exact_nested_move_pairs': len(move_pairs)}


# Exact q9-screened pivot choice; the solver is not imported to reproduce it.
PIVOTS=[10,11,20,21,28,24,36,37,38,39,50,49,55,54,59,65,67,70,79,74,81,84,88,92,101,97,108,107]

def rank(rows):
    piv={}
    for v in rows:
        while v:
            p=v.bit_length()-1
            if p not in piv:piv[p]=v;break
            v ^= piv[p]
    return len(piv)


def analyse(native):
    roots=[[F(x) for x in native['frames'][str(native['start'][i])]['B'][0]] for i in range(111)]
    groups={}
    for i in range(8,111):
        support=tuple(j for j,x in enumerate(roots[i]) if x)
        need(len(support)==4,'four-support source')
        groups.setdefault((support,sum(x<0 for x in roots[i])%2),[]).append(i)
    need(len(groups)==28,'28 source halfclasses')
    G=[]
    for ((support,parity),g),pivot in zip(groups.items(),PIVOTS):
        need(pivot in g,'chosen pivot belongs to actual halfclass')
        need(all(dot(roots[i],roots[j])==0 for i in g for j in g if i!=j),'orthogonal source halfclass')
        span=rref([roots[i] for i in g]);need(len(span)==len(g),'exact minimal group span')
        G.append({'support':support,'parity':parity,'indices':g,'pivot':pivot,'donors':[j for j in g if j!=pivot],
                  'rank':len(span),'B':encode_basis(span),'row':sum(1<<j for j in g)})
    K=[sum(1<<j for j in range(111) if i==j or dot(roots[i],roots[j])==0) for i in range(111)]
    D=[g['row'] for g in G]+[1<<j for j in range(8)]
    E=[]
    for k in K:
        e=k&~255
        for g in G:
            if (k>>g['pivot'])&1:e ^= g['row']
        E.append(e)
    B=[E[i] for i in (8,14,30)]
    table={0:0}
    for mask in range(1,8):
        row=0
        for t,b in enumerate(B):
            if (mask>>t)&1:row ^= b
        table[row]=mask
    need(len(table)==8 and set(E)<=set(table),'three explicit global modes factor every gauged row')
    A=[table[e] for e in E]
    need((rank(K),rank(D),rank(K+D),rank(E))==(9,36,39,3),'exact code dimensions')
    need(all(e&255==0 and all(not((e>>p)&1) for p in PIVOTS) for e in E),'all36 representative columns zero')
    need(all(not((e>>i)&1) for i,e in enumerate(E)),'zero own diagonal')
    donors=[j for g in G for j in g['donors']]
    minor=[];labels=[]
    for j in sorted(donors):
        label=sum(((b>>j)&1)<<t for t,b in enumerate(B))
        if rank(labels+[label])>len(labels):minor.append(j);labels.append(label)
        if len(minor)==3:break
    need(len(minor)==3,'three donor columns with invertible global-mode minor')
    retained=list(range(111))
    need(len(retained)==111,'all111 stationary input copies')
    available=[g['row'] for g in G]+[1<<j for j in retained]+B
    need(rank(available)==111,'all input information retained below Hub')
    need(rank(available+[1<<j for j in range(2,8)])==111,'six remaining coordinate directions fill full input rank')
    return {'groups':G,'K':K,'E':E,'B':B,'A':A,'donors':donors,'minor':minor,'retained':retained,
            'dimensions':{'C':9,'D':36,'C_plus_D':39,'C_intersection_D':6,'gauge':3,'handoff_information':111}}


class Source:
    def __init__(self,native):
        self.native=native;self.frames={int(c):f for c,f in native['frames'].items()}
        self.spaces={c:rref(f['B']) for c,f in self.frames.items()};self.ids={b:c for c,b in self.spaces.items()}
        for c in native['start'][:222]+native['final'][:222]:self.ids[self.spaces[c]]=c
        self.ops=[];self.where=dict(enumerate(native['start'][:222]));self.hub=native['final'][0];self.zero=native['start'][111]
    def chart(self,basis):
        b=rref(basis)
        if b in self.ids:return self.ids[b]
        c=max(self.frames)+1;self.frames[c]={'dim':len(b),'B':encode_basis(b),'A':encode_basis(perpendicular(b))}
        self.spaces[c]=b;self.ids[b]=c;return c
    def move(self,i,target):
        current=self.where[i]
        if current==target:return
        a,b=self.spaces[current],self.spaces[target]
        if len(a)<len(b):
            need(included(a,b),'actual ascending inclusion')
            for v in b:
                nb=rref(list(a)+[v])
                if len(nb)==len(a):continue
                nxt=target if len(nb)==len(b) else self.chart(nb)
                self.ops.append(['MOVE',i,current,nxt]);current,a=nxt,nb
        else:
            need(included(b,a),'actual descending inclusion')
            ids=[target];small=b
            for v in a:
                nb=rref(list(small)+[v])
                if len(nb)==len(small):continue
                ids.append(current if len(nb)==len(a) else self.chart(nb));small=nb
            for nxt in reversed(ids[:-1]):self.ops.append(['MOVE',i,current,nxt]);current=nxt
        need(current==target,'complete flag');self.where[i]=target
    def add(self,a,b,c):
        need(a!=b and self.where.get(a)==self.where.get(b)==c,('cochart availability',a,b,c))
        self.ops.append(['ADD',a,b,c]);return len(self.ops)-1
    def init(self,i,c):
        need(i not in self.where,'new zero-born record');self.ops.append(['INIT',i,c]);self.where[i]=c
    def clear(self,i):
        self.ops.append(['CLEAR',i,self.where[i]]);del self.where[i]
    def word(self,end_owned,scope):
        final=[self.where[i] for i in range(222)];used=set(self.native['start'][:222]+final)
        for op in self.ops:used.update(op[-2:] if op[0]=='MOVE' else [op[-1]])
        return {'schema':'BIT-point-halfclass-gauge-prefix-v2','public':222,'owned_fields':117,
                'hub':self.hub,'start':self.native['start'][:222],'final':final,'frames':{c:self.frames[c] for c in sorted(used)},
                'program':list(self.ops),'directions':{str(i):'down' for i in range(333,336)},'end_owned':end_owned,'scope':scope}

def emit(native,c):
    s=Source(native);copies=[];groups=[];broadcasts=[];core_caches=[]
    # Retain independent information at actual source lines BEFORE any donor
    # leaves. No physical move of any retained owned cache is claimed.
    for t,j in enumerate(c['retained']):
        owned=222+t;chart=s.where[j];s.init(owned,chart);copy=s.add(owned,j,chart)
        copies.append({'field':owned,'input':j,'chart':chart,'copy_operation':copy})
    for g in c['groups']:
        chart=s.chart(g['B']);p=g['pivot'];s.move(p,chart);adds=[]
        for j in g['donors']:
            s.move(j,chart);adds.append(s.add(p,j,chart));s.move(j,s.hub)
        groups.append({'pivot':p,'donors':g['donors'],'chart':chart,'rank':g['rank'],'row_hex':hex(g['row']),'add_operations':adds})
    for j in range(8):s.move(j,s.hub)
    local_ready=len(s.ops)-1
    for t,b in enumerate(c['B']):
        p=333+t;s.init(p,s.hub);birth=len(s.ops)-1;reads=[]
        for j in range(111):
            if (b>>j)&1:reads.append(s.add(p,j,s.hub))
        s.move(p,s.zero);core=336+t;s.init(core,s.zero);copy=s.add(core,p,s.zero)
        core_caches.append({'field':core,'chart':s.zero,'row_hex':hex(b),'copy_operation':copy});deposits=[]
        for i,a in enumerate(c['A']):
            if (a>>t)&1:deposits.append({'receiver':i,'operation':s.add(111+i,p,s.zero)})
        s.clear(p);broadcasts.append({'field':p,'birth':birth,'payload_hex':hex(b),'reads':reads,'deposits':deposits})
    prefix=s.word(list(range(222,333))+list(range(336,339)),
        'Unfinished physical prefix:28 original halfclass pivots held at rank2-4charts;111 stationary input copies,3 pure ground core caches retained;83 originalX atHub; allYs atzero carry y_i+E_i after3globalpackets. No target decoder or kappa.')
    prefix_end=len(s.ops)-1
    restoration=[]
    for g in groups:
        p=g['pivot'];s.move(p,s.hub);restores=[s.add(p,j,s.hub) for j in g['donors']]
        restoration.append({'pivot':p,'restore_operations':restores})
    for j in range(111):s.move(111+j,native['final'][111+j])
    for copy in copies+core_caches:s.clear(copy['field'])
    closed=s.word([], 'Closed PRECONDITIONER only:allXrestoredHub,Y_i=y_i+E_i atnativeFi,allownedcleared. NotY_i+=X_i andnotcomplete supplier.')
    return prefix,closed,{'copies':copies,'groups':groups,'local_ready_cut':local_ready,'broadcasts':broadcasts,
                          'prefix_end':prefix_end,'restoration':restoration,'core_caches':core_caches}


def save_word(path,word):
    raw=json.dumps(word,separators=(',',':'),sort_keys=True).encode();z=gzip.compress(raw,mtime=0);path.write_bytes(z)
    return {'gzip_sha256':hashlib.sha256(z).hexdigest(),'canonical_json_sha256':hashlib.sha256(raw).hexdigest()}


def main(a):
    raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'authenticated native source')
    native=json.loads(gzip.decompress(raw));c=analyse(native);prefix,closed,metadata=emit(native,c)
    pr=replay(prefix);cr=replay(closed)
    expected=[1<<i for i in range(222)]
    for i,e in enumerate(c['E']):expected[111+i]^=e
    need(cr['rows']==expected,'all222 independent public columns of closed preconditioner')
    ep=list(expected)
    for g in c['groups']:ep[g['pivot']]=g['row']
    need(pr['rows']==ep,'all physical prefix values including dirty pivots')
    need(pr['owned_rows']==({str(222+t):hex(1<<j) for t,j in enumerate(c['retained'])}|{str(336+t):hex(b) for t,b in enumerate(c['B'])}),'all111 input copies and3 core caches')
    need(pr['owned_where']=={str(q['field']):q['chart'] for q in metadata['copies']+metadata['core_caches']},'stationary local andcore copies never moved')
    need(pr['paid_profile']=={1:680} and cr['paid_profile']=={1:1578},'exact rank-one MOVE profiles')
    need(pr['owned_lifetimes']==117 and pr['peak_owned']==115,'111 input copies,3 core caches,3 Hub packets')
    need(pr['counts']['ADD']==111+3+75+sum(b.bit_count() for b in c['B'])+sum(v.bit_count() for v in c['A']),'complete prefix ADD invoice')
    need(cr['counts']['ADD']==pr['counts']['ADD']+75,'all original carrier restorations paid')
    need(len(pr['clear_rows'])==3 and len(cr['clear_rows'])==117,'pending versus closed ownership ledger')
    need([q['row_hex'] for q in pr['clear_rows']]==[hex(b) for b in c['B']],'actual global packet erasures')
    controls=[]
    def omitted(word,k):
        bad=json.loads(json.dumps(word));del bad['program'][k];return replay(bad)
    r=omitted(prefix,metadata['copies'][0]['copy_operation']);need(r['owned_rows']!=pr['owned_rows'],'missingretentioncopy')
    controls.append({'name':'omit_retained_copy_ADD','rejected':True})
    r=omitted(prefix,metadata['core_caches'][0]['copy_operation']);need(r['owned_rows']!=pr['owned_rows'],'missing actual global core cache')
    controls.append({'name':'omit_actual_core_cache_copy','rejected':True})
    r=omitted(prefix,metadata['groups'][0]['add_operations'][0]);need(r['rows']!=ep,'missinghalfaggregate')
    controls.append({'name':'omit_halfclass_aggregate_ADD','rejected':True})
    r=omitted(prefix,metadata['broadcasts'][0]['deposits'][0]['operation']);need(r['rows']!=ep,'missingglobalbroadcast')
    controls.append({'name':'omit_one_ground_broadcast','rejected':True})
    r=omitted(closed,metadata['restoration'][0]['restore_operations'][0]);need(r['rows']!=expected,'missingoriginalrestore')
    controls.append({'name':'omit_closed_carrier_restore','rejected':True})
    bad=json.loads(json.dumps(prefix));packet=333;birth=metadata['broadcasts'][0]['birth']
    bad['program'].insert(birth+1,['ADD',packet,PIVOTS[0],prefix['hub']])
    try:replay(bad)
    except ValueError:pass
    else:raise ValueError('fabricated held-pivot Hubread accepted')
    controls.append({'name':'read_unavailable_local_pivot_atHub','rejected':True})
    bad=json.loads(json.dumps(prefix)); copy=metadata['copies'][8]
    bad['program'].append(['ADD',111,copy['field'],prefix['start'][111]])
    try:replay(bad)
    except ValueError:pass
    else:raise ValueError('source-line cache read at ground accepted')
    controls.append({'name':'pretend_source_line_cache_is_at_ground','rejected':True})
    need(rank([g['row'] for g in c['groups']]+c['B'])==31,'unretainedprefix hasonly31properinputrank')
    controls.append({'name':'pretend_retention_is_optional','rejected':True,'unretained_required_total_packets':83})
    need(all(expected[111+i]&(1<<(111+i)) for i in range(111)),'alloriginalYcolumns preserved')
    controls.append({'name':'replace_arbitrary_Y_by_zero_contract','rejected':True})
    a.output.mkdir(parents=True,exist_ok=True)
    wordpins={'PREFIX.json.gz':save_word(a.output/'PREFIX.json.gz',prefix),'CLOSED-WORD.json.gz':save_word(a.output/'CLOSED-WORD.json.gz',closed)}
    certificate={k:v for k,v in c.items() if k not in ('K','E','B','groups')}
    certificate.update({'native_sha256':PIN,'pivots':PIVOTS,'canonical_rows_hex':[hex(x) for x in c['K']],
                        'gauged_rows_hex':[hex(x) for x in c['E']],'global_basis_hex':[hex(x) for x in c['B']],
                        'groups':[{**{k:v for k,v in g.items() if k!='row'},'row_hex':hex(g['row'])} for g in c['groups']]})
    (a.output/'CERTIFICATE.json').write_text(json.dumps(certificate,indent=2,sort_keys=True)+'\n')
    for receipt in (pr,cr):receipt.pop('rows');receipt.pop('routes')
    result={'status':'PASS_PAID_ALL_POINT_COPY_THREE_MODE_PREFIX_NO_LOCAL_DROPS','native_sha256':PIN,'metadata':metadata,
            'prefix_receipt':pr,'closed_preconditioner_receipt':cr,'word_pins':wordpins,'negative_controls':controls,
            'handoff_X_information_rank':111,'remaining_input_information':[],'proper_origin_descending_routes':0,'their_paid_profile':{},
            'minimum_total_Hub_packets_if_no_further_local_descents':9,'additional_packets_at_q9':6,
            'complete_target_decoder_constructed':False,'new_kappa_claimed':False,
            'residual_obligation':'Use6additionalpaidHub-to-zero packets andtheactualretainedlocaldata torestore28pivotoriginals,clear114caches,andcompleteall111Ytargetsatnativefacetswithinwholecallerbudget.'}
    (a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'dimensions':c['dimensions'],'minor':c['minor'],'retained':len(c['retained']),
                      'prefix_counts':pr['counts'],'prefix_peak':pr['peak_owned'],'closed_counts':cr['counts'],
                      'negative_controls':len(controls)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
