#!/usr/bin/env python3
"""Independent full rational frozen-D1 response and direct pinned quotient review."""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import gzip
import json


def need(ok, why):
    if not ok:
        raise ValueError(why)


def add(row, other, scale=F(1)):
    for j, x in other.items():
        y = row.get(j, 0) + scale*x
        if y:
            row[j] = y
        else:
            row.pop(j, None)


ap = ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()
pkg = Path(__file__).resolve().parent
for path, digest in json.loads((pkg/'SOURCE-PINS.json').read_text())['files'].items():
    need(sha256((args.repo/path).read_bytes()).hexdigest() == digest, 'pin '+path)
base = args.repo/'research/moonshot-005-program/results'
raw = gzip.decompress((base/'complex-native-funded-donor-cuts/inputs/DOUBLE-CANDIDATE.json.gz').read_bytes())
need(sha256(raw).hexdigest() == '7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48', 'unpacked source')
w = json.loads(raw)
n = len(w['initial'])
need(n == len(w['final']) == 1289, 'complete endpoint inventory')
old_forms = {e: {j: F(x) for j, x in row} for e, row in w['forms']}
forms = {e: row.copy() for e, row in old_forms.items()}
schedule = [e for e in w['schedule'] if e != 95914]
del forms[95914]
routes = {e: (u, v) for e, u, v in w['moves'] if e != 95914}
routes.update({94019: (3, 278), 90369: (3, 304), 88: (278, 127)})
observer = max(schedule)+1
schedule.insert(schedule.index(90369)+1, observer)
routes[observer] = (3, 282)
forms[94019] = {~1288: F(1)}
forms[90369] = old_forms[94019].copy()
forms[88] = {**old_forms[95914], 94019: F(-845660160)}
forms[observer] = old_forms[90369].copy()
for e in schedule:
    if e in (94019, 90369, 88, observer):
        continue
    if 94019 in forms[e]:
        forms[e][90369] = forms[e].pop(94019)
    if 90369 in old_forms[e]:
        forms[e][observer] = forms[e].pop(90369)
ends = [w['first_output']+i for i in range(n)]
terminal_chart = dict(zip(ends, w['final']))
holders = {~j: chart for j, chart in enumerate(w['initial'])}
for e in schedule:
    chart = routes[e][0] if e in routes else terminal_chart[e]
    need(all(holders.get(j) == chart for j in forms[e]), 'actual local operands '+str(e))
    if e in routes:
        holders[e] = routes[e][1]
candidates = [86, 89777, 97232, 97241, 97320, 97323, 99064, 94019]
pos = {e: j for j, e in enumerate(candidates)}


def backward(slot, rows, order, capture=True):
    weights = {slot: F(1)}
    exposures = [F(0)]*len(candidates)
    for e in reversed(order):
        q = weights.pop(e, 0)
        if e in pos and capture:
            exposures[pos[e]] = q
        if q:
            add(weights, rows[e], q)
    need(all(j < 0 for j in weights), 'complete backwards source expansion')
    return {~j: q for j, q in weights.items()}, exposures


E, B = [], []
for slot in ends:
    row, response = backward(slot, forms, schedule)
    old, _ = backward(slot, old_forms, w['schedule'], False)
    need(row == old, 'compensated full target '+str(slot))
    E.append(row)
    B.append(response)
print('Reconstructed all 1289 endpoints by reverse DAG expansion.', flush=True)
# Sparse elimination of the complete target, without component inversion.
pivots = {}
for i, entry in reversed(list(enumerate(E))):
    row, right = entry.copy(), {i: F(1)}
    while row:
        j = min(row)
        q = row[j]
        if j not in pivots:
            pivots[j] = ({k: x/q for k, x in row.items()}, {k: x/q for k, x in right.items()})
            break
        left, previous = pivots[j]
        add(row, left, -q)
        add(right, previous, -q)
    else:
        raise ValueError('singular complete endpoint')
need(set(pivots) == set(range(n)), 'all source pivots')
inverse = [{} for _ in range(n)]
for j in reversed(range(n)):
    row, right = pivots[j]
    inverse[j] = right.copy()
    for k, x in row.items():
        if k != j:
            add(inverse[j], inverse[k], -x)


def product(left, right):
    out = []
    for row in left:
        value = {}
        for j, q in row.items():
            add(value, right[j], q)
        out.append(value)
    return out


identity = [{j: F(1)} for j in range(n)]
need(product(E, inverse) == product(inverse, E) == identity, 'two complete inverse identities')

# Work directly in all 1289 terminal coordinates; no author arithmetic is imported.
X = [j for j,c in enumerate(w['initial']) if c==3]
Y = [j for j,c in enumerate(w['initial']) if c!=3]
A = [i for i,c in enumerate(w['final']) if c!=127]
Xset,Yset,Aset=set(X),set(Y),set(A)
D=candidates[:-1]
frozen={e:({} if e in D else row) for e,row in forms.items()}
E0,B0=[],[]
for slot in ends:
    row,response=backward(slot,frozen,schedule)
    E0.append(row);B0.append(response)
print('Reconstructed frozen endpoints and eight independent impulse responses.',flush=True)
P=[backward(e,forms,schedule,False)[0] for e in D]
for i in range(n):
    row=E0[i].copy()
    for k in range(7):add(row,P[k],B0[i][k])
    need(row==E[i],'full exact deletion identity '+str(i))

def basis_add(basis,row):
    row=row.copy()
    while row:
        j=max(row);q=row[j]
        if j not in basis:
            basis[j]={k:v/q for k,v in row.items()}
            return row
        add(row,basis[j],-q)
    return {}

def residue(basis,row):
    row=row.copy();rem={}
    while row:
        j=max(row);q=row[j]
        if j in basis:add(row,basis[j],-q)
        else:rem[j]=row.pop(j)
    return rem

def rank(rows):
    b={}
    for r in rows:basis_add(b,r)
    return len(b)

def columns(rows,width):
    out=[{}for _ in range(width)]
    for i,row in enumerate(rows):
        for j,q in row.items():out[j][i]=q
    return out

Ecols=columns(E,n);Ncols=columns(E0,n)
v0={i:B0[i][-1]for i in range(n)if B0[i][-1]}
vg={i:B[i][-1]for i in range(n)if B[i][-1]}
controls=[e for e,(u,v)in routes.items()if u==3]
Frows=[]
for e in controls:
    need(all(j<0 and ~j in Xset for j in forms[e]),'source export locality')
    row={~j:q for j,q in forms[e].items()}
    if e==94019:row[n]=F(1)
    Frows.append(row)
need(len(controls)==909 and rank(Frows)==909,'invertible natural export-control basis')
Ccols=[Ncols[j]for j in X]+[v0]
Cbasis={}
for c in Ccols:basis_add(Cbasis,c)
need(len(Cbasis)==909,'direct rational full control rank')

outside_ranks=[];zero_rows=[]
for label,rows,v in [('genuine_paid',E,vg),('frozen_D1',E0,v0)]:
    CA=[{j:q for j,q in rows[i].items()if j in Xset} for i in A]
    for r,i in zip(CA,A):
        if v.get(i):r[n]=v[i]
    need(rank(CA)==376,'direct rational outside control rank '+label)
    z=[ends[i]for i,r in zip(A,CA)if not r]
    need(len(z)==11,'eleven exact zero outside control rows')
    outside_ranks.append({'baseline':label,'exact_rank':376,'zero_terminal_rows':z})
    zero_rows.append(z)
need(zero_rows[0]==zero_rows[1],'same fixed outside rows')
ancestor=set(zero_rows[0])
for e in reversed(schedule):
    if e in ancestor:ancestor.update(j for j in forms[e]if j>=0)
need(not(set(D+[94019])&ancestor),'ancestor-independent exact zero rows')

Delta=[]
for i in A:
    row={j:q for j,q in E[i].items()if j in Yset}
    add(row,{j:q for j,q in E0[i].items()if j in Yset},F(-1));Delta.append(row)
Ds={ends[i]:r for i,r in zip(A,Delta)if r}
Js=sorted(set().union(*(r.keys()for r in Delta)))
need(len(Ds)==75 and len(Js)==73 and rank(Delta)==2,'exact external defect dimensions')
need(w['initial'][29]==w['initial'][691]==27,'actual chart27 initial axes')
need(29 in Js and 691 not in Js and len(set(Js)-{29,691})==72,'chart27 input support')
for j in Js:
    aa=2*Ds[154885].get(j,F(0));bb=2*Ds[154880].get(j,F(0))-aa
    need(all(r.get(j,F(0))==r.get(0,F(0))*aa+r.get(4,F(0))*bb for r in Delta),'explicit rank-two factorization')
minor=[[Ds[e].get(j,F(0))for j in (0,4)]for e in (154880,154885)]
need(minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0]==F(-1,4),'outside rational rank-two minor')

# Direct pinned residues in the 1289-dimensional observation space.
Rcols=columns(inverse,n)
eligible=[i for i in A if set(Rcols[i])&Xset]
fixed=[i for i in A if i not in eligible]
need(len(eligible)==376 and len(fixed)==11,'pinned coordinate populations')
pinned=[];fail=[];pure=[];purefail=[]
for i in eligible:
    f={i:F(1)}
    for j,q in Rcols[i].items():
        if j in Yset:add(f,Ncols[j],-q)
    r=residue(Cbasis,f);pinned.append(r)
    if r:fail.append(ends[i])
    if not(set(Rcols[i])&Yset):
        pure.append(r)
        if r:purefail.append(ends[i])
need(rank(pinned)==5 and len(fail)==103,'direct full-observation pinned defect')
need(len(pure)==272 and rank(pure)==1 and purefail==[155100],'external-source-independent subgate')
for i in fixed:
    f={i:F(1)}
    for j,q in Rcols[i].items():
        if j in Yset:add(f,Ncols[j],-q)
    need(not f,'eleven fixed equations hold exactly')
print('Direct rational ranks: C909, Ca376, outside defect2, pinned quotient5.',flush=True)

# Review the smaller eight-variable explanation against independent full responses.
BR=[{k:q for k,q in enumerate(row)if q}for row in B0]
TH=product(inverse,BR)
K0=[{k:q if k<7 else -q for k,q in TH[j].items()}for j in Y]
need(rank(K0)==7,'small external block rank seven')
ker={4:F(1,4),5:F(1)}
need(all(not sum((r.get(j,0)*q for j,q in ker.items()),F(0))for r in K0),'exact small null vector')
Z=[]
for k in range(7):
    row={k:F(1)}
    for j,q in P[k].items():
        if j in Xset:
            add(row,{a:(-v if a<7 else v)for a,v in TH[j].items()},q)
    Z.append(row)
g=[sum((r.get(j,0)*q for j,q in ker.items()),F(0))for r in Z]
need(g==[F(0),F(0),F(0),F(0),F(1,4),F(0),F(0)],'small quotient image')
qcols=[];qproject=[]
for i in eligible:
    q=[sum((P[k].get(j,F(0))*v for j,v in Rcols[i].items()),F(0))for k in range(7)]
    qcols.append(q);qp={k:v for k,v in enumerate(q)if v and k!=4};qproject.append(qp)
    need(bool(qp)==(ends[i]in fail),'small and full-dimensional membership agree')
need(rank(qproject)==5,'exact small quotient rank')
i=eligible.index(ends.index(154897));need(qcols[i]==[F(0),F(0),F(-1,4),F(1,4),F(0),F(0),F(0)],'pinned explicit negative control')

result={'status':'PASS_ROOT_EXACT_FROZEN_SOURCE_GATES','direct_rational_endpoint_fields':1289,'actual_export_control_basis_rank':909,'frozen_full_control_rank':909,'outside_control_ranks':outside_ranks,'outside_external_defect_rank':2,'outside_external_affected_rows':75,'outside_external_affected_columns':73,'affected_columns_unavailable_at_chart27':72,'outside_rank_two_minor_determinant':'-1/4','pinned_quotient_rank':5,'failed_pinned_memberships':103,'pure_source_only_outside_coordinates':272,'pure_source_only_quotient_rank':1,'pure_source_only_failed_terminals':purefail,'fixed_outside_equations_verified':11,'small_external_block_rank':7,'small_external_kernel':[str(ker.get(j,0))for j in range(8)],'small_quotient_image':[str(q)for q in g],'negative_control_terminal':154897,'negative_control_pairing':'-1/4','fixed_common_acyclic_scalar_form_edit_lower_bound':5,'new_author_code_imported':False,'retained_independent_reverse_DAG_method_reused':True,'complete_repaired_word':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],909,376,2,73,5,103,1,flush=True)
