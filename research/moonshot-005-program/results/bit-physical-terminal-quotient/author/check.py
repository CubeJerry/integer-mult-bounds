#!/usr/bin/env python3
"""Reconstruct a rectangular return minor from the actual GF(64) words."""
import argparse
from collections import Counter,defaultdict
import gzip,hashlib,json
from pathlib import Path
import sys

import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from algebra import MUL,INV,POWER,cauchy,echelon,jet,mm,need

PINS = {
    "layout": ("bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz",
               "9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72"),
    "routes": ("bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz",
               "6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036"),
    "phases": ("bit-asymmetric-balanced-atlas/author/output/PLANE-PHASES.json",
               "bae4a03a923abfc840e0d030093bdb635eb948de312697b5a08d0338bcc83cf6"),
    "spread": ("bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz",
               "7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab"),
}
H_WORD=("WORDS.json.gz","bda9d599f8c17fd04993a96994fca0d6c8e20ea9951fd55c21e6431b82f3cd84")
D_CHARTS=("CHARTS.json.gz","9e2fbdb0a1ec95926903b65acea48b7428f1a2bf0c8233271ac655d76e630e15")
K_WORD={"spread":("SPREAD-OWNERS.json.gz","513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0"),
        "mixed":("MIXED-OWNERS.json.gz","8b2428093a2c432ebcc2770679574213c1ae45c57baa57900fd92d7eaf2b9f4a")}
F_WORD=("WORDS.json.gz","282f16cd16f99f71fe0d2ad6c97c3138e3263be4adf8e46ad9182ebd12146f01")
SCALES_X={49:(3,2),97:(1,1),53:(1,2),77:(7,1),93:(1,7),8:(1,2),82:(3,1),58:(2,1),106:(1,1),31:(1,1),105:(1,2)}
SCALES_Y={49:(2,1,2),97:(2,1,2),53:(1,1,3),77:(1,2,1),93:(1,1,1),8:(1,1,2),82:(1,1,1),58:(1,1,2),106:(4,1,1),31:(1,1,1),105:(1,1,1)}
BEFORE=[(49,39),(87,107),(85,0),(60,43)]
AFTER=[(23,98),(34,94),(108,31),(36,79)]
ROWS=[27,30]
COLS=[28,48,50,99]

def read_pin(folder,pair):
    name,digest=pair
    raw=(folder/name).read_bytes()
    if name.endswith(".gz"): raw=gzip.decompress(raw)
    need(hashlib.sha256(raw).hexdigest()==digest,name)
    return raw

def fid(route):
    return (53280 if route[0]=="Y" else 0)+480*route[1]+route[2]

ZERO=np.zeros(480,dtype=np.uint8)

def at(d,owners):
    return np.stack([d.get(t,ZERO) for t in owners])

class Native:
    def __init__(self,args):
        base=args.repo/"research/moonshot-005-program/results"
        z=json.loads(read_pin(base,PINS["layout"]))
        self.H=z["A2"];self.D=z["D4"];self.dual=z["dual_D4"]
        roots=np.asarray(z["root_table"][:111]);self.orth=roots@roots.T==0
        self.p={int(h):v for h,v in json.loads(read_pin(base,PINS["phases"])).items()}
        self.mark=set(json.loads(read_pin(base,PINS["spread"]))["selected_D"])
        self.hword={int(n):v for n,v in json.loads(read_pin(args.h_words,H_WORD)).items()}
        self.dword=json.loads(read_pin(args.d_words,D_CHARTS))
        self.kwords={k:{int(h):q for h,q in json.loads(read_pin(args.k_words,v)).items()} for k,v in K_WORD.items()} if getattr(args,"k_words",None) else {}
        self.fwords={k.lower():dict(v) for k,v in json.loads(read_pin(args.f_words,F_WORD)).items()} if getattr(args,"f_words",None) else {}
        self.rt={};self.byh=defaultdict(lambda:defaultdict(list));self.byd=defaultdict(lambda:defaultdict(list))
        for line in read_pin(base,PINS["routes"]).splitlines():
            r=json.loads(line);w=fid(r);self.rt[w]=r
            if r[3] is not None: self.byh[r[3]][r[0],r[4]].append(w)
            if r[4] is not None: self.byd[r[4]][r[0]].append(w)
        for per in (*self.byh.values(),*self.byd.values()):
            for v in per.values(): v.sort()
        self.planes={x:[h for h,g in enumerate(self.H) if x in g] for x in range(111)}
        self.half={x:{h for h in [h for h in hs if self.p[h]["donor_early"][str(x)]==15][:12]}
                   for x,hs in self.planes.items()}
        self.node={(x,h):s+1 for x,hs in self.planes.items() for s,h in enumerate(hs)}

    def scaffold(self):
        levels=[([r],[c]) for r,c in BEFORE]+[(ROWS,COLS)]+[([r],[c]) for r,c in AFTER]
        rr=[i for rs,cs in levels for i in rs];cc=[j for rs,cs in levels for j in cs]
        need(len(set(rr+cc))==len(rr+cc),"disjoint native roles")
        for k,(rs,cs) in enumerate(levels):
            need(self.orth[np.ix_(rs,cs)].all(),"proper diagonal or core")
            for rprev,cprev in levels[:k]:
                need(not self.orth[np.ix_(rs,cprev)].any(),"strictly lower zero")
        return list(map(int,self.orth[np.ix_(rr,cc)].sum(axis=1)))

    def source_in(self,j,h,phase,n,stripe):
        p=self.p[h];donors=sorted(x for x in self.H[h] if x<111)
        size=len(donors);k=n//3;early=phase=="X"
        quot={x:p["donor_early"][str(x)] for x in donors}
        if size==3:
            labels=sum(([x]*k for x in donors),[])
        elif size==2:
            big=next(x for x in donors if quot[x]==30);small=next(x for x in donors if x!=big)
            labels=[big]*(2*k)+[small]*k if early else [small]*k+[None]*(2*k)
        else:
            labels=[j if early else None]*n
        mat=np.zeros((n,480),dtype=np.uint8)
        for t,x in enumerate(labels):
            if x!=j: continue
            der=False;scale=1
            if size==3 and p["early"]==2:
                c=t%k+stripe*k
            elif size==2 and quot[j]==30:
                c=t
            elif size==1:
                der=t>=2*k;c=t-2*k if der else t
                scale=SCALES_X[j][n==36] if der else 1
            else:
                first=(h in self.half[j])==early
                c=t%k+(0 if first else k)
            s=16*((0 if n==9 else 6)+c)
            mat[t,s:s+16]=jet(self.node[j,h],der,scale)
        return mat

    def through_d(self,j,rows,marked=None):
        ds={d for d,v in enumerate(self.D) if j in v and any(i in self.D[self.dual[d]] for i in rows)}
        if marked is not None:
            ds={d for d in ds if (d in self.mark)==marked}
        hv={}
        for h in self.planes[j]:
            p=self.p[h];outs=self.byh[h];all_d=sorted({d for phase,d in outs})
            for n,sub in ((9,[d for d in all_d if d in self.mark]),(36,[d for d in all_d if d not in self.mark])):
                if marked is not None and (n==9)!=marked:
                    continue
                need(len(sub)==n,"true source H partition")
                V=np.asarray(self.hword[n]["V"],dtype=np.uint8)
                stored={}
                for phase,tag in (("X","early"),("Y","late")):
                    for stripe in range(p[tag]):
                        s=self.source_in(j,h,phase,n,stripe)
                        v=mm(V,s)
                        if phase=="X": stored[stripe]=s
                        if phase=="Y" and p["m"]<3:
                            variant="two" if p["m"]==2 else "singleton"
                            dV=np.asarray(self.hword[n][variant]["cross_coefficients"],dtype=np.uint8)
                            v ^= mm(dV,stored[stripe])
                        for z,d in enumerate(sub):
                            if d in ds: hv[outs[phase,d][stripe]]=v[z]
        dv={}
        for d in sorted(ds):
            idx,m,n,w=self.dword[d]
            need(idx==d,"D word owner index")
            es,ls=self.byd[d]["X"],self.byd[d]["Y"]
            need(len(es)==m and len(ls)==n,"actual D arrivals")
            e,l=at(hv,es),at(hv,ls)
            out_e=mm(cauchy(range(m),range(m)),e)
            out_l=mm(cauchy(range(n),range(n)),l)
            r=len(w)
            if r:
                sg=mm(cauchy(range(m,m+r),range(m)),e)
                sg=MUL[np.asarray(w,dtype=np.uint8)[:,None],sg]
                out_l ^= mm(cauchy(range(n),range(n,n+r)),sg)
            dv.update(zip(es,out_e));dv.update(zip(ls,out_l))
        return dv

    def facet(self,dv,i,mode):
        physical={};table=[];ecols=[];ycols=[]
        for h in self.planes[i]:
            kw=self.kwords[mode][h];count=Counter()
            size=self.p[h]["m"];q=self.p[h]["donor_early"][str(i)];selected=[]
            for phase,src,dst in kw["stripes"]:
                n=len(src);k=n//3;stripe=count[phase,n];count[phase,n]+=1
                v=np.asarray(POWER[1:n+1,:n].T,order="C")
                v=mm(v,at(dv,src));physical.update(zip(dst,v))
                if phase=="Y": selected.extend(dst[:2*k])
                for t,owner in enumerate(dst):
                    r=self.rt[owner];receiver=r[1] if phase=="Y" else r[7]
                    if receiver!=i: continue
                    der=False;scale=1
                    if size==3 and q==30:
                        c=t%k+stripe*k
                    elif size==2 and q==30:
                        c=t
                    elif size==1:
                        der=t>=2*k;c=t-2*k if der else t
                        scale=SCALES_Y[i][{9:0,36:1,45:2}[n]] if der else 1
                    else:
                        first=(h in self.half[i])==(phase=="Y")
                        c=t%k+(0 if first else k)
                    s=16*((6 if n==36 else 0)+c)
                    table.append((owner,s,jet(self.node[i,h],der,scale)))
            for x,y in kw["early_cache_to_late"]:
                physical[y] ^= physical[x]
            early,late=[],[]
            for phase,src,dst in kw["stripes"]:
                for owner in dst:
                    r=self.rt[owner]
                    if phase=="X" and r[7]==i: early.append(owner)
                    if phase=="Y" and r[1]==i: late.append(owner)
            early.sort();late.sort()
            if early:
                need(len(early)==15,"early K-F arrivals")
                ecols.append(early)
            if len(late)==45:
                base=sorted(selected);extra=sorted(set(late)-set(base))
                need(len(base)==30 and len(extra)==15,"singleton row bands")
                ycols.extend([base[:15],base[15:],extra])
            else:
                ycols.extend([late[t:t+15] for t in range(0,len(late),15)])
        eowners=[owner for col in ecols for owner in col]
        rawE=at(physical,eowners)
        owners_y=list(range(53280+480*i,53280+480*(i+1)))
        rawY=at(physical,owners_y)
        rs=np.zeros((480,480),dtype=np.uint8)
        for owner,s,coeff in table:
            rs[s:s+16] ^= MUL[coeff[:,None],physical[owner][None,:]]
        w=self.fwords[mode][i];r=len(w)
        capture=mm(cauchy(range(r),range(len(ecols))),rawE.reshape(len(ecols),15*480))
        delivery=mm(MUL[cauchy(range(32),range(r)),np.asarray(w,dtype=np.uint8)[None,:]],capture)
        minimum=rawY.copy()
        for s,band in enumerate(ycols):
            for t,owner in enumerate(band):
                minimum[owner-owners_y[0]] ^= delivery[s,480*t:480*(t+1)]
        return rawE[np.argsort(eowners)],rawY,rs,minimum

def self_diagonal(native):
    """Eight known self diagonals surrounding a rectangular foreign observation."""
    before = [71, 4, 52, 9, 66]
    after = [13, 54, 88]
    rows = [73, 12, 56]
    donors = [15, 20, 33, 34, 39, 44]
    need(len(set(before + after + rows + donors)) == 17, "self-diagonal distinct roles")
    need(not native.orth[np.ix_(before + after, before + after)].any(), "isolated diagonal pivots")
    need(not native.orth[np.ix_(rows, before)].any(), "zero lower-left corner")
    need(not native.orth[np.ix_(after, donors)].any(), "zero lower-right corner")
    need(native.orth[np.ix_(rows, donors)].all(), "the complete rectangular center")
    result = {"before": before, "after": after, "core_rows": rows, "core_columns": donors, "variants": {}}
    values = {}
    for j in donors:
        dv = native.through_d(j, rows)
        for mode in K_WORD:
            for i in rows:
                values[mode,i,j] = native.facet(dv,i,mode)
    for mode in K_WORD:
        e = np.block([[values[mode,i,j][0] for j in donors] for i in rows])
        y = np.block([[values[mode,i,j][1] for j in donors] for i in rows])
        a = np.concatenate((e,y))
        re = len(echelon(e)[0])
        ra = len(echelon(a)[0])
        need((re,ra) == (1035,2430), "three receivers and six donors")
        result["variants"][mode] = {
            "early_shape": list(e.shape), "late_shape": list(y.shape),
            "early_payload_sha256": hashlib.sha256(e.tobytes()).hexdigest(),
            "late_payload_sha256": hashlib.sha256(y.tobytes()).hexdigest(),
            "rank_early": re, "rank_all": ra, "free_facet_field_rank_lower": ra-re,
            "replacement_bank_lower": 8*(8*480+ra-re), "replacement_excess_lower": 8*(ra-re-480),
        }
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ("repo","h-words","d-words","k-words","f-words","out"):
        p.add_argument("--"+n,type=Path,required=True)
    p.add_argument("--arrays",type=Path)
    p.add_argument("--independent-arrays",type=Path)
    args=p.parse_args();native=Native(args)
    result={"lower_support_row_weights":native.scaffold(),"before":BEFORE,"after":AFTER,
            "central_rows":ROWS,"central_cols":COLS,"body":480,"copies":8,"field_poly":67,"variants":{}}
    blocks={}
    for j in COLS:
        dv=native.through_d(j,ROWS)
        for mode in K_WORD:
            for i in ROWS:
                blocks[mode,i,j]=native.facet(dv,i,mode)
    if args.arrays:
        args.arrays.mkdir(parents=True,exist_ok=True)
        for (mode,i,j),v in blocks.items():
            for k,m in zip(("E","Y","RS","minimum"),v):
                np.save(args.arrays/f"{mode}-{i}-{j}-{k}.npy",m)
    if args.independent_arrays:
        for i in ROWS:
            for j in COLS:
                z=np.load(args.independent_arrays/f"pre-{i}-{j}.npz")
                e,y,rs,minimum=blocks["spread",i,j]
                for first,other,label in [(e,z["E"],"E"),(y,z["Y"],"Y"),(rs,np.load(args.independent_arrays/f"B-{i}-{j}.npy"),"RS")]:
                    need(np.array_equal(first,other),f"independent {label} {i}/{j}")
    for mode in K_WORD:
        def slab(which,cs=COLS):
            return np.block([[blocks[mode,i,j][which] for j in cs] for i in ROWS])
        e=slab(0);y=slab(1)
        re=len(echelon(e)[0]);rey=len(echelon(np.concatenate((e,y)))[0])
        out={"rank_E":re,"rank_EY":rey,"free_facet_field_rank_lower":rey-re,
             "raw_E_shapes":[blocks[mode,i,COLS[0]][0].shape[0] for i in ROWS],
             "proper_fullrank":{},"four_block_core_rank":{},"matrix_pins":{}}
        for z,key in enumerate(("E","Y","RS","minimum")):
            out["matrix_pins"][key]={f"{i}/{j}":hashlib.sha256(blocks[mode,i,j][z].tobytes()).hexdigest() for i in ROWS for j in COLS}
            if z<2: continue
            ranks={f"{i}/{j}":len(echelon(blocks[mode,i,j][z])[0]) for i in ROWS for j in COLS}
            out["proper_fullrank"][key]=ranks
            out["four_block_core_rank"][key]=len(echelon(slab(z,COLS[:2]))[0])
        result["variants"][mode]=out
        print(mode,re,rey,rey-re,out["four_block_core_rank"],flush=True)
    from price import caps
    result["return_caps_at_one_over_200"] = caps()
    result["native_self_diagonal"] = self_diagonal(native)
    result["source_pins"] = {k:v[1] for k,v in PINS.items()}
    result["word_pins"] = {"H":H_WORD[1], "D":D_CHARTS[1], "K":{k:v[1] for k,v in K_WORD.items()}, "minimum_F":F_WORD[1]}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")

if __name__=="__main__": main()
