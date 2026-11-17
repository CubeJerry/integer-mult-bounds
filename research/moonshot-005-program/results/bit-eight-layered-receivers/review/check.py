#!/usr/bin/env python3
"""Independent cohort, chart-chain and local-span audit for both layered words."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util, itertools, json, sys
from pathlib import Path

ENGINE="7d5ecd497ddd86d9b25cb5485c271d6ccad5bef3f3a1e962b0aef3a23dff95f6"
PINS={"seven":"0efee1eba69dabe5f7357522a16217b9b1bcff97cd983bf4b211561d1e47bafe",
      "eight":"57603fff38645768b6ffa0047ed693484c448ef899eadb0f3038f4add92009e7"}


def group_data(w,roots,eng):
    core,outer=set(w["core_roles"]),set(w["outer_roles"]);allroles=core|outer
    masks={j:frozenset(i for i in allroles if sum(a*b for a,b in zip(r,roots[i]))==0)
           for j,r in enumerate(roots)}
    atom=defaultdict(set)
    for i,s in masks.items():atom[s].add(i)
    common=atom[frozenset(allroles)];core_only=atom[frozenset(core)]
    for i,s in masks.items():
        if core<=s:assert s in (frozenset(core),frozenset(allroles))
    raw=w["common_mask_originals"];old=w["old_common_mask_originals"]
    assert len(set(raw))==len(raw) and len(set(old))==len(old)
    assert set(raw)<=common and set(old)<=core_only and set(raw).isdisjoint(old)
    taps={frozenset(x["signature"]):x for x in w["tap_sites"]}
    wanted={s for s in atom if s&outer and s!=frozenset(allroles)}
    assert set(taps)==wanted
    for s,rec in taps.items():assert set(rec["donors"])==atom[s]
    net=set();routes={};antichains={}
    for target in sorted(outer):
        tracks=[p for p in w["tracks"] if p["receiver"]==target]
        mysets={s for s in wanted if target in s}
        acquired=[];rawowners=[]
        for tr in tracks:
            seq=list(map(frozenset,tr["sites"]));acquired.extend(seq)
            assert all(prev>cur for prev,cur in zip(seq,seq[1:]))
            if tr["carrier_role"] is not None:
                assert tr["carrier_role"] in common;rawowners.append(tr["carrier_role"])
            for s in seq:assert [target,tr["carrier_role"]] in taps[s]["readers"]
        assert len(acquired)==len(mysets) and set(acquired)==mysets
        assert len(rawowners)==len(tracks)-1 and not set(rawowners)&net
        net.update(rawowners);routes[target]=len(tracks)
        # A matching antichain explicitly proves that the shown physical chain count is minimal.
        ant=next((subset for subset in itertools.combinations(sorted(mysets,key=lambda s:sorted(s)),len(tracks))
                  if all(not (a<=b or b<=a) for a,b in itertools.combinations(subset,2))),None)
        assert ant is not None
        antichains[target]=[sorted(s) for s in ant]
    assert net==set(raw)
    return {"core_normal_rank":eng.rational_rank(tuple(roots[i] for i in sorted(core))),
            "collective_normal_rank":eng.rational_rank(tuple(roots[i] for i in sorted(allroles))),
            "common_donors":len(common),"core_only_donors":len(core_only),
            "outer_taps":len(taps),"outer_tapped_originals":sum(len(atom[s]) for s in taps),
            "taps_shared_across_outer_receivers":sum(1 for s in taps if len(s&outer)>1),
            "actual_distinct_new_mask_originals":len(raw),"actual_disjoint_old_mask_originals":len(old),
            "minimum_exact_signature_chain_counts":routes,"matching_antichain_certificates":antichains}


def global_gate(roots,eng):
    # Bit masks and the popcount identity |U\\V|=|U|-|U∩V| give an implementation
    # independent of the author's set-difference enumerator.
    masks=[]
    for r in roots:
        masks.append(sum(1<<j for j,v in enumerate(roots) if sum(map(int.__mul__,r,v))==0))
    degrees=[m.bit_count() for m in masks]
    d_min=min(degrees);ov_min=min((a&b).bit_count() for a,b in itertools.combinations(masks,2))
    diffs=[(degrees[i]-(a&b).bit_count(),i,j) for i,a in enumerate(masks) for j,b in enumerate(masks) if i!=j]
    diff_min,i,j=min(diffs)
    deleted=[k for k in range(111) if (masks[i]>>k)&1 and not (masks[j]>>k)&1]
    assert sum(degrees)==6470 and (d_min,ov_min,diff_min)==(55,23,21)
    assert len(deleted)==21
    rem=((1<<111)-1)^sum(1<<k for k in deleted)
    assert (masks[i]&rem) & ~(masks[j]&rem)==0
    ov,ii,jj=min(((a&b).bit_count(),i,j) for i,a in enumerate(masks) for j,b in enumerate(masks) if i<j)
    common=[k for k in range(111) if (masks[ii]&masks[jj])>>k &1]
    rm=common[:-2];assert len(rm)==21
    checks={}
    for s in (91,100,111):
        checks[s]=str(Fraction(111)-Fraction(s+111,s-56))
    baseline,room=eng.intervals({7:222,8:9})
    assert 11<room[0] and room[1]<12
    return {"foreign_incidences":sum(degrees),"minimum_degree":d_min,"minimum_ordered_signature_difference":diff_min,
            "minimum_pair_intersection":ov_min,"ordered_pairs":len(diffs),
            "universal_arbitrary_deletions_at_most":20,"minimum_scalar_raw_backups_in_restricted_model":110,
            "exact_multicopy_raw_dimension_lower_bounds_per_copy":checks,
            "base_movement_before_raw_information":list(map(str,baseline)),"remaining_limiting_room":list(map(str,room)),
            "twenty_one_delete_comparability_witness":{"roles":[i,j],"delete":deleted},
            "twenty_one_delete_two_common_witness":{"roles":[ii,jj],"delete":rm,"remaining":common[-2:]}}


def run(eng,wordpath,label,roots,exhaustive):
    raw=wordpath.read_bytes();assert sha256(raw).hexdigest()==PINS[label]
    w=json.loads(raw);assert w["native_sha256"]==eng.NATIVE_SHA
    n=set(w["all_completed_roles"]);g=eng.geometry(w["charts"],roots);rows=eng.basis_from_roots(roots)
    a=eng.simulate(w,rows,g,n);q,room=eng.intervals(a["movement_profile"])
    ref=json.loads((wordpath.parent/"RESULT.json").read_bytes())
    rr=ref["ordinary_counts_and_routes"]
    assert rr["counts"]==a["opcodes"] and rr["peak_owned"]==a["peak_owners"] and rr["dirty_CLEAR"]==a["dirty_clears"]
    assert {int(k):v for k,v in rr["movement_profile"].items()}==a["movement_profile"]
    for own,theirs in ((q, ref["moment_at_199_over_200"]), (room, ref["necessary_limiting_room"])):
        l,h=map(Fraction,theirs["rational"]);assert l<=own[0]<=own[1]<=h
    assert a["unfinished_target_flats_missing_own_output_before_retirement"]==111-len(n)
    assert a["unfinished_target_flats_missing_own_output_after_retirement"]==111-len(n)
    assert a["owned_movement_profile"]=={8:9}
    reject=Counter();survivors=[]
    for i in (range(len(w["operations"])) if exhaustive else range(0,len(w["operations"]),85)):
        try:eng.simulate(w,rows,g,n,omit=i,collect=False)
        except (eng.Invalid,KeyError):reject[w["operations"][i][0]]+=1
        else:survivors.append(i)
    return {"literal_word_sha256":PINS[label],"all_original_input_columns":222,**a,**group_data(w,roots,eng),
            "moment":list(map(str,q)),"necessary_limiting_room":list(map(str,room)),
            **eng.finite_threshold(a["movement_profile"]),"single_omissions_rejected":dict(reject),
            "single_omissions_retaining_same_public_source":survivors}


if __name__=="__main__":
    p=ArgumentParser();p.add_argument("--engine",type=Path,required=True);p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--seven",type=Path,required=True);p.add_argument("--eight",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True);p.add_argument("--sample",action="store_true");a=p.parse_args()
    assert sha256(a.engine.read_bytes()).hexdigest()==ENGINE
    s=importlib.util.spec_from_file_location("independent_bit_engine",a.engine)
    eng=importlib.util.module_from_spec(s);sys.modules[s.name]=eng;s.loader.exec_module(eng)
    ns=(a.repo/eng.NATIVE).read_bytes();assert sha256(ns).hexdigest()==eng.NATIVE_SHA
    roots=[tuple(x) for x in json.loads(ns)["native_roots"]]
    res={"status":"PASS_LAYERED_WORDS_AND_RESTRICTED_SINGLE_STAGE_CAPACITY_REVIEW","engine_sha256":ENGINE,
         "single_stage_restriction":global_gate(roots,eng),"seven":run(eng,a.seven,"seven",roots,not a.sample),
         "eight":run(eng,a.eight,"eight",roots,not a.sample)}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/"RESULT.json").write_text(json.dumps(res,indent=2)+"\n")
    print(res["status"],res["seven"]["single_omissions_retaining_same_public_source"],res["eight"]["single_omissions_retaining_same_public_source"])
