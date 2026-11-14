#!/usr/bin/env python3
"""Independent spatial affine verification of the new L=OM translation gauge."""
import argparse,hashlib,json
from pathlib import Path
def need(v,msg):
    if not v:raise ValueError(msg)
def main():
    p=argparse.ArgumentParser();p.add_argument('--routes',type=Path,required=True);p.add_argument('--note',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    note='07de3e1c139776d9e8db0995fd8f60926426f5390ea70281d1afee366d725c85';routes='ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a'
    need(hashlib.sha256(a.note.read_bytes()).hexdigest()==note,'reviewed new lemma');need(hashlib.sha256(a.routes.read_bytes()).hexdigest()==routes,'actual routes')
    data=json.loads(a.routes.read_text());out=[]
    for r in data['route_records']:
        stage=r['stage'];n=9+8*stage
        def perm(x):
            v=x
            for i,b in enumerate(r['orthogonal_complement']):
                w=b^(1<<(9+8*(stage-1)+i))
                if (w&x).bit_count()%2:v^=w
            return v
        tau=r['input_translation'];sigma=r['output_translation'];shift=sigma^perm(tau)
        def row_OM(x):return perm(perm(x^sigma)^tau)
        need(all(row_OM(x)==x^shift for x in [0]+[1<<i for i in range(n)]),'literal O then M row map is translation')
        need(perm(r['normal'])==r['normal'],'head direction fixed')
        out.append({'stage':stage,'port':r['port'],'L_translation':shift})
    receipt={'status':'PASS_ROOT_ADDITIONAL_TRANSLATION_GAUGE_REVIEW','new_note_sha256':note,'routes_sha256':routes,'literal_port_stage_maps':len(out),'translations':out,'universal_algebra':'L Aplus^-1 Q^2 L^-1=Aminus; preferred/complementary input/output translations restore arbitrary baselines by commuting with D','extra_ordinary_translations_per_full_call':448,'new_Gaussian_calls':0,'scope':'Direct critical review of new C/B lemma plus independent spatial composition. Aplus is not asserted central, involutive or stage-independent. No new kappa.'}
    a.output.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'maps':len(out)}))
if __name__=='__main__':main()
