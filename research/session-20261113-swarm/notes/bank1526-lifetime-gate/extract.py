"""Read-only normalized source gate; no physical lifetime execution.
Apache-2.0. Prepared with substantial OpenAI Codex assistance.
"""
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
from bisect import bisect_right
import argparse, gzip, hashlib, json, subprocess

MAIN = 'e54523517d0f03e58352e647c403a5af3e525a57'
ARCHIVE = '172f4535ce8dcff79f626410af845f757c1563be'
ARCHIVE_PATH = 'research/literal-native-quadratic-phase/reference/selected-native.json.gz'
ARCHIVE_SHA = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
WORD_SHA = '91429a6b96729292a8764836e00c87a6f7cd3b76f05159033f4867f69a98d097'
OWNER, BIRTH, DEATH = 1526, 28037, 37618
POSITIONS = {'INIT': (1,), 'CLEAR': (1,), 'MOVE': (1,),
             'ADD': (1, 2), 'SCALE': (1,), 'COPY': (1, 2)}
EXPECTED = [
 (28037, ['INIT', 1526, 601]), (28041, ['ADD', 1526, 1349, '-1', 601]),
 (28129, ['ADD', 1526, 728, '-1', 601]),
 (28135, ['ADD', 1526, 729, '-1', 601]),
 (28139, ['ADD', 1526, 730, '-1', 601]),
 (28141, ['MOVE', 1526, 601, 470, True]),
 (28159, ['ADD', 1515, 1526, '1', 470]), (37618, ['CLEAR', 1526, 470])]

def need(ok, message):
 if not ok: raise ValueError(message)

def canonical(value): return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()

def pin(raw, commit, path):
 return {'commit': commit, 'path': path, 'bytes': len(raw),
         'sha256': hashlib.sha256(raw).hexdigest(),
         'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()}

def build(repo):
 def read(commit, path):
  return subprocess.check_output(['git', 'show', commit+':'+path], cwd=repo)
 raw = read(ARCHIVE, ARCHIVE_PATH)
 need(len(raw) == 350722 and hashlib.sha256(raw).hexdigest() == ARCHIVE_SHA, 'archive drift')
 word = json.loads(gzip.decompress(raw)); program = word['program']
 need(hashlib.sha256(canonical(word)).hexdigest() == WORD_SHA, 'canonical source drift')
 need(len(program) == 71261, 'program length')
 paths = ['docs/research/pr-intake-evidence/pr7000-application/PROOF-REVIEW.md',
          'docs/research/pr-intake-evidence/pr7000-admission/PROOF-REVIEW.md',
          'research/owned-ascent-contract/PROOF.md',
          'research/owned-ascent-contract/verify.py',
          'research/owned-ascent-contract/RECIPES.json']
 main_sources = [pin(read(MAIN, p), MAIN, p) for p in paths]
 recipes = json.loads(read(MAIN, paths[-1]))
 recipe, = [r for r in recipes if r['start'] == 601 and r['end'] == 470]
 need(recipe['rank'] == 2, 'rank2 recipe')
 touches = defaultdict(list)
 for i, event in enumerate(program):
  for owner in set(event[j] for j in POSITIONS[event[0]]): touches[owner].append(i)
 need([(i, program[i]) for i in touches[OWNER]] == EXPECTED, 'not exactly eight owner contacts')
 peers = {1349, 728, 729, 730, 1515}
 values = {i: Fraction(i == 4) for i in range(word['public'])}
 frames = dict(enumerate(word['initial']))
 provenance = {i: {'initial_frame': frame} for i, frame in frames.items()}
 previous = {}; trace = []; changes = []
 for i, event in enumerate(program[:DEATH+1]):
  op, target = event[:2]; before = values.get(OWNER); entry = None
  if i in touches[OWNER]:
   entry = {'index': i, 'event': event, 'bank_before': str(before),
            'bank_frame_before': frames.get(OWNER)}
   if op == 'ADD':
    peer = event[2] if target == OWNER else target
    at = bisect_right(touches[peer], i)
    entry['peer'] = {'owner': peer, 'frame': frames[peer],
      'normalized_input4_coefficient_before': str(values[peer]),
      'chart_provenance': provenance[peer], 'previous_contact': previous.get(peer),
      'next_contact': ({'index': touches[peer][at], 'event': program[touches[peer][at]]}
                       if at < len(touches[peer]) else None)}
  old_chart = frames.get(target)
  if op in ('ADD', 'COPY'):
   need(frames[target] == event[4] == frames[event[2]], 'scalar current-chart mismatch')
   if op == 'COPY': need(values[target] == 0, 'COPY guard in one-column witness')
   values[target] = (Fraction(0) if op == 'COPY' else values[target])+Fraction(event[3])*values[event[2]]
  elif op == 'SCALE':
   need(frames[target] == event[3], 'SCALE current chart')
   values[target] *= Fraction(event[2])
  elif op == 'MOVE':
   need(frames[target] == event[2], 'MOVE current chart')
   need(bool(event[4]) == (target >= word['public']), 'MOVE private/owned flag')
   frames[target] = event[3]; provenance[target] = {'index': i, 'event': event}
  elif op == 'INIT':
   need(target not in values and target >= word['public'], 'fresh owned INIT')
   values[target] = Fraction(0); frames[target] = event[2]
   provenance[target] = {'index': i, 'event': event}
  elif op == 'CLEAR':
   need(target >= word['public'] and frames[target] == event[2], 'live owned CLEAR')
   del values[target]; del frames[target]; provenance.pop(target)
  if target in peers and BIRTH <= i <= DEATH and op in ('MOVE', 'INIT', 'CLEAR'):
   changes.append({'index': i, 'event': event, 'before': old_chart, 'after': frames.get(target)})
  if entry is not None:
   entry.update(bank_after=str(values.get(OWNER)), bank_frame_after=frames.get(OWNER))
   trace.append(entry)
  for owner in set(event[j] for j in POSITIONS[op]): previous[owner] = {'index': i, 'event': event}
 need(trace[-1]['bank_before'] == '-3/4', 'forward nonzero witness')
 # Independent reverse covector: combination of all original public entrances.
 row = {OWNER: Fraction(1)}
 for event in reversed(program[:DEATH]):
  op, target = event[:2]; coefficient = row.get(target, Fraction(0))
  if op in ('INIT', 'CLEAR'): row.pop(target, None)
  elif op in ('ADD', 'COPY'):
   if op == 'COPY':
    need(coefficient == 0, 'this bank covector depends on the COPY interpretation')
    row.pop(target, None)
   source = event[2]; value = row.get(source, Fraction(0))+coefficient*Fraction(event[3])
   if value: row[source] = value
   else: row.pop(source, None)
  elif op == 'SCALE':
   value = coefficient*Fraction(event[2])
   if value: row[target] = value
   else: row.pop(target, None)
  elif op != 'MOVE': raise ValueError(op)
 need(len(row) == 259 and row.get(4) == Fraction(-3, 4), 'reverse nonzero witness')
 need(all(i < word['public'] for i in row), 'owned term reached raw entrance')
 receiver_prefix = [{'index': i, 'event': program[i]} for i in touches[1515] if 28153 <= i <= 28159]
 return {'marker': 'PASS_BANK1526_LIFETIME_GATE',
  'scope': 'Normalized source algebra and interface gate; no physical lifetime execution.',
  'archive': pin(raw, ARCHIVE, ARCHIVE_PATH), 'canonical_word_sha256': WORD_SHA,
  'main_sources': main_sources, 'program_length': len(program), 'public': word['public'],
  'owner': OWNER, 'birth': BIRTH, 'death': DEATH, 'complete_owner_contacts': trace,
  'frames': {str(i): word['frames'][i] for i in (3, 470, 601)},
  'peer_chart_changes_during_lifetime': changes, 'receiver_prefix': receiver_prefix,
  'rank2_recipe': {'old_role': recipe['role'], 'old_event': recipe['event'],
    'start': recipe['start'], 'end': recipe['end'], 'rank': recipe['rank'],
    'left_records': len(recipe['left_records']), 'right_records': len(recipe['right_records']),
    'canonical_sha256': hashlib.sha256(canonical(recipe)).hexdigest(),
    'binding': 'Exact e545 admission checks owned-offset/frame/per-owner-order matching to the current word; old event number is not current28141.'},
  'nonzero_witness': {'initial_logical_public_input': 4, 'other_public_inputs': 0,
    'clear_coefficient_forward': trace[-1]['bank_before'], 'clear_coefficient_reverse': str(row[4]),
    'reverse_public_support': len(row),
    'reverse_row_sha256': hashlib.sha256(canonical([(i, str(v)) for i, v in sorted(row.items())])).hexdigest(),
    'all_f_interpretation': 'For a nonzero complete array a, bank before CLEAR is T_470^(tensor f)(-3a/4), nonzero for every positive f.'},
  'semantic_guards': ['Every operation touching1526 was selected by opcode operand positions over the entire word.',
    'MOVE final Boolean is private ownership, not an inverse flag.',
    'CLEAR permits dirty discard under retained owned_erasure; zero-at-CLEAR is not asserted.',
    'Matching scalar charts do not implement binary packet geometry, grid or field-length production.']}

if __name__ == '__main__':
 parser = argparse.ArgumentParser(); parser.add_argument('--source-repo', required=True)
 parser.add_argument('--write', action='store_true'); args = parser.parse_args()
 result = build(args.source_repo); destination = Path(__file__).with_name('EXTRACTION.json')
 if args.write: destination.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
 else: need(json.loads(destination.read_text()) == result, 'retained extraction changed')
 print('PASS_BANK1526_LIFETIME_GATE: 8 contacts; independent -3/4 coefficient; dirty retirement remains physical.')
