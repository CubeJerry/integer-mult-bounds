"""Exact finite geometry certificate for the all-field immutable-code theorem."""
from pathlib import Path
import argparse, collections, hashlib, importlib.util, json

def module(path, name):
    sp=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source-word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=a.source_word.read_bytes();w=json.loads(raw)
    assert hashlib.sha256(raw).hexdigest()=='74fb050a6afb8d8e1b6895b0f092220f8e6852365a7516ef4db2284c43c1a5ee'
    src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots']
    e=module(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','immutable_native_geometry')
    h=module(a.repo/'research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint3-evidence/A/build_common_carrier_fanout.py','immutable_exact_helpers')
    P=w['construction'];U=P['unknown_roles'];S=P['known_roles'];rows=[int(x,16)for x in P['canonical_unknown_rows_hex']];B=h.binary_basis(rows);assert len(B)==9
    dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));coeffs={};local=[]
    for i in U:
        neighbours=[j for j in U if dot(i,j)==0]
        K=(1<<i)^sum(1<<j for j in neighbours);coef=h.coeff(B,K);coeffs[i]=coef
        nonlocal_mask=sum(1<<j for j in U if j not in neighbours)
        projected=[r&nonlocal_mask for r in rows];r=len(h.binary_basis(projected));assert r==9
        local.append({'receiver':i,'neighbours':neighbours,'canonical_coeff_hex':hex(coef),'nonlocal_projection_rank':r})
    cert=[]
    for z in range(1,512):
        support=[i for i in U if (coeffs[i]&z).bit_count()%2]
        d=len(e.basis(tuple(tuple(R[i])for i in support)));assert d>=7
        witness=[]
        for i in support:
            if len(e.basis(tuple(tuple(R[j])for j in witness+[i])))>len(witness):witness.append(i)
        assert len(witness)==d
        cert.append({'functional':z,'support':support,'normal_rank':d,'independent_root_witness':witness})
    chosen=[];duals=[]
    for c in sorted(cert,key=lambda c:(c['normal_rank'],c['functional'])):
        if len(h.binary_basis(duals+[c['functional']]))>len(duals):duals.append(c['functional']);chosen.append(c)
        if len(duals)==9:break
    assert len(duals)==9 and all(c['normal_rank']==7 for c in chosen)
    # Each chosen dual direction therefore has a real common line for its
    # receiver set. This is sharp only in the idealized static-access model.
    lines=[]
    for c in chosen:
        line=e.chart({'kind':'ann','rows':[R[i]for i in c['support']]});assert len(line)==1
        assert all(sum(line[0][k]*R[i][k]for k in range(8))==0 for i in c['support'])
        lines.append({'functional':c['functional'],'line_basis':[[str(x)for x in row]for row in line]})
    q=h.moment({7:9});base=h.moment({1:165,6:108,7:114});gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in h.moment(gate));excess=(base[0]+q[0]-ceiling[1],base[1]+q[1]-ceiling[0]);assert excess[0]>0
    # Scope control: adding an actual missing own coordinate to a receiver's
    # side information destroys the zero-intersection premise.
    i=U[0];neigh=[j for j in U if dot(i,j)==0];m=sum(1<<j for j in U if j not in neigh and j!=i)
    leaked_dim=9-len(h.binary_basis([r&m for r in rows]));assert leaked_dim>=1
    result={'status':'PASS_IMMUTABLE_CANONICAL_NINE_CHANNEL_GEOMETRY_GATE','source_word_sha256':hashlib.sha256(raw).hexdigest(),'native_source_sha256':hashlib.sha256(src).hexdigest(),'receivers':len(U),'code_rank':9,'all_receiver_local_intersections_zero':True,'nonzero_binary_dual_functionals':511,'normal_rank_histogram':dict(collections.Counter(c['normal_rank']for c in cert)),'sharp_rank7_dual_basis':duals,'minimum_packet_moment':h.record(q),'source_plus_gate_excess':h.record(excess),'scope_control_actual_own_coordinate_leak_intersection_dimension':leaked_dim,'scope':'Nine immutable independent whole-record canonical channels born at Hub; all other unknown-information relay paths are ascending or stationary. Extra downward owners, recoding/changing the packet payloads, other fitting-code spaces, or earlier sources require new analysis.'}
    h.save(a.out/'CERTIFICATE.json',{'source_word_sha256':result['source_word_sha256'],'local_restrictions':local,'binary_dual_supports':cert,'sharp_rank7_dual_basis_lines':lines})
    h.save(a.out/'RESULT.json',result);print(json.dumps(result))

if __name__=='__main__':main()
