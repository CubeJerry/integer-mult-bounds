#!/usr/bin/env python3
"""Exact arithmetic audit of the illustrative target-bootstrap bridge only."""
from fractions import Fraction as Q
from pathlib import Path
import argparse, hashlib, json

def need(condition, message):
    if not condition:
        raise AssertionError(message)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--bootstrap', type=Path, required=True)
    p.add_argument('--strict-price', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()

    proof_path = a.bootstrap / 'PROOF.md'
    boot = json.loads((a.bootstrap / 'RESULT.json').read_text())
    uniform = json.loads((a.strict_price / 'author-uniform/RESULT.json').read_text())
    two = json.loads((a.strict_price / 'author-two-prices/RESULT.json').read_text())
    q8 = json.loads((a.strict_price.parent / 'author/RESULT.json').read_text())

    target = Q(1, 200)
    b0 = Q(12039, 3125000)
    C = Q(50001, 10000000)
    rho = Q(51, 10000)
    b1 = Q(15607, 3125000)
    B = Q(500007, 100000000)
    def A(b):
        return (1-rho)*C + rho*b
    A1, A2 = A(b0), A(b1)
    gaps = {
        'stage1_improvement': b1-b0,
        'stage1_A_minus_b1': A1-b1,
        'stage1_rho_minus_A': rho-A1,
        'stage1_stock': 1-A1-rho,
        'stage2_improvement': B-b1,
        'stage2_A_minus_B': A2-B,
        'stage2_rho_minus_A': rho-A2,
        'stage2_stock': 1-A2-rho,
    }
    expected = {
        'stage1_improvement': Q(446,390625),
        'stage1_A_minus_b1': Q(3569,500000000000),
        'stage1_rho_minus_A': Q(52876431,500000000000),
        'stage1_stock': Q(494952876431,500000000000),
        'stage2_improvement': Q(583,100000000),
        'stage2_A_minus_B': Q(57,500000000000),
        'stage2_rho_minus_A': Q(49964943,500000000000),
        'stage2_stock': Q(494949964943,500000000000),
    }
    need(gaps == expected, 'illustrative stage gaps differ from exact source receipt')
    need(b0 < b1 < A1 < rho < 1-A1, 'stage1 strict-separator inequalities')
    need(b1 < B < A2 < rho < 1-A2, 'stage2 strict-separator inequalities')
    need(B > target and C > B, 'two-stage witness does not exceed target below C')

    threshold = Q(3112961,621875000)
    kmax = Q(2503,500000)
    kmin = Q(1,200)
    one_stage_overhang = kmax-threshold
    two_stage_witness_overhang = kmax-C
    need(one_stage_overhang == Q(581,2487500000), 'one-stage threshold difference')
    need(two_stage_witness_overhang == Q(59,10000000), 'two-stage sufficient-C difference')
    need(kmin == target and threshold > target and kmax > threshold,
         'movement interval / target / one-stage threshold ordering')
    # The root theorem's exact h=2 reachability inequality is checked for the
    # displayed witness, but this is entirely conditional on covered C.
    lhs = C*C*(C-b0)/(1-b0)
    rhs_target = (C-target)/(1-target)
    need(lhs < rhs_target, 'two-stage D criterion fails for target 1/200')

    need(boot['selected_ordinary'] == str(b0), 'selected ordinary seed mismatch')
    need(boot['hypothetical_covered'] == str(C), 'hypothetical covered C mismatch')
    need(boot['one_stage_C_strict_threshold'] == str(threshold), 'one-stage threshold mismatch')
    need(uniform['kappa_interval'] == ['1/200','2503/500000'], 'uniform movement interval mismatch')
    need(uniform['scope'].startswith('Analytic uniform movement profile lemma') or
         'movement' in uniform['scope'].lower(), 'uniform result scope does not identify movement only')
    need(two['cases']['C0050001']['covered_C'] == str(C), 'strict-price two-price C mismatch')
    need(two['cases']['C0050001']['first_profitable_even_m'] == 6, 'm6 receipt mismatch')
    need(q8['Q_target_paid'] == {'1':1618}, 'q8 Q is not the unit-rank movement profile')
    need(q8['complete_source_constructed'] is False, 'q8 source unexpectedly claimed complete')
    need(q8['m6_affordable_extra_unit_calls'] == 1 and
         q8['all_finite_m_affordable_extra_unit_calls_at_most'] == 3,
         'q8 movement slack mismatch')

    # Explicitly do not assert any relation between tested movement k and C.
    out = {
        'status':'PASS_EXACT_CONDITIONAL_TARGET_BRIDGE_ARITHMETIC',
        'selected_seed_b0':str(b0), 'hypothetical_covered_C':str(C),
        'atom_rho':str(rho), 'stage_b1':str(b1), 'completed_B_witness':str(B),
        'target':str(target), 'strict_gaps':{k:str(v) for k,v in gaps.items()},
        'two_stage_D_at_target':{'lhs':str(lhs),'rhs':str(rhs_target),'strict':True},
        'one_stage_threshold':str(threshold),
        'illustrative_if_kmax_were_pre_loss':{
            'kmax':str(kmax),
            'loss_budget_for_C_above_one_stage_threshold':f'< {one_stage_overhang}',
            'loss_budget_for_sufficient_two_stage_C':f'<= {two_stage_witness_overhang}',
        },
        'movement_receipt':{
            'k_interval':uniform['kappa_interval'],
            'q_profile':q8['Q_target_paid'],
            'm6_extra_unit_moves':q8['m6_affordable_extra_unit_calls'],
            'all_finite_m_extra_unit_moves_at_most':q8['all_finite_m_affordable_extra_unit_calls_at_most'],
            'complete_source_constructed':q8['complete_source_constructed'],
        },
        'explicit_nonclaim':'No k-to-C conversion inequality, completed Q source, covered supplier, or ordinary supplier is provided or inferred.',
    }
    a.output.mkdir(parents=True, exist_ok=True)
    (a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
