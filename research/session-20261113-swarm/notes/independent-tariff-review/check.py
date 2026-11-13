"""Exact source hashes and rational review comparisons; no graph replay.
Apache-2.0. Prepared with substantial OpenAI Codex assistance.
"""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json, subprocess

HERE = Path(__file__).resolve().parent
def need(ok, message):
 if not ok: raise ValueError(message)

def check(repo):
 pins = json.loads((HERE/'SOURCES.json').read_text()); source = {}
 for item in pins['files']:
  b = subprocess.check_output(['git','show',item['commit']+':'+item['path']],cwd=repo)
  need(len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'], 'source drift: '+item['path'])
  source[item['path']] = b.decode()
 manifest = json.loads(source['research/shared-wire-split-composition/INDEPENDENT-SOURCES.json'])
 k = F(manifest['claim']); delta = (F(manifest['tested'])-k)/7
 need(k==F('.00363005817') and delta==F(1,10**14), 'selected binding')
 epsilon=1-delta; beta=1-3*delta; eta=delta
 a=k+4*delta; b=k+5*delta; q=k+3*delta
 tau=1-a; sigma=1-b; leaf=sigma+eta*(1-sigma)
 positive = {'epsilon_minus_beta':epsilon-beta,'one_minus_epsilon':1-epsilon,
  'one_minus_beta':1-beta,'eta':eta,'one_minus_eta':1-eta,
  'one_minus_tau':1-tau,'one_minus_sigma':1-sigma,'q':q,
  'group_nonleaf_record_ratio_power':beta*eta*(1-tau),
  'generic_full_width_nonleaf_record_ratio_power':epsilon*eta*(1-tau),
  'group_root_vs_larger_d_layer_target':beta-epsilon*(1-q),
  'group_root_vs_grouped_gaussian_row':beta-(epsilon-q*beta),
  'group_root_vs_global_target':beta-(1-k),
  'direct_leaf_slack':1-q-leaf,'stock_sublinearity':beta*(1-F(1,250))}
 need(all(x>0 for x in positive.values()), 'closed asymptotic comparison')
 need(positive['group_root_vs_larger_d_layer_target']==epsilon*q-2*delta, 'layer exponent identity')
 need(positive['group_root_vs_grouped_gaussian_row']==beta*q-2*delta, 'group row exponent identity')
 need(positive['group_root_vs_global_target']==k-3*delta, 'global exponent identity')
 return {'marker':'PASS_SELECTED_TARIFF_FAMILY_REVIEW','canonical_main':pins['canonical_main'],
  'kappa':str(k),'margin_delta':str(delta),'epsilon':str(epsilon),'group_beta':str(beta),
  'eta_stop':str(eta),'tau':str(tau),'sigma':str(sigma),'q':str(q),
  'direct_leaf_exponent':str(leaf),'logarithmic_compatibility_threshold':str(tau/(1-tau)),
  'positive_exact_margins':{k:str(v) for k,v in positive.items()},
  'H_C':14174600000000000000,'carrier':'N=2^H_C, fixed before p varies',
  'conclusion':'Approve per-record failure and the conditional unchanged-schedule layer comparison. Do not infer a lower bound for optimized suppliers or multiplication.',
  'limitations':['Actual group width is Theta(p^beta), not an unproved scheduled h=d.',
    'Whole-schedule comparison assumes a retained nontrivial serial adapter on a fixed positive role-volume fraction.',
    'No independent mapping of an emitted full completed-carrier word or graph body-write proof is supplied by this review.',
    'Only exact source hashes and rational exponent arithmetic are executable checks; asymptotic fit and normalization arguments are in REVIEW.md.']}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--source-repo',required=True)
 parser.add_argument('--write',action='store_true');args=parser.parse_args()
 result=check(args.source_repo);dest=HERE/'EXACT-COMPARISONS.json'
 if args.write:dest.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 else:need(json.loads(dest.read_text())==result,'review comparison drift')
 print('PASS_SELECTED_TARIFF_FAMILY_REVIEW: exact source pins and all rational margins agree.')
