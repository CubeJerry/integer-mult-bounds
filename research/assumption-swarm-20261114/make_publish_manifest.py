"""Serialize only a verified new research package for GitHub tree creation."""
from pathlib import Path
import json
import subprocess
import sys

worktree, slug, stem = sys.argv[1:]
base = 'e54523517d0f03e58352e647c403a5af3e525a57'
base_tree = '1199c3d7a31fffa5ba5d41f10f1b933aacc797aa'
def git(*args):
    return subprocess.check_output(['git', '-C', worktree, *args])
changes = git('diff', '--name-status', base, 'HEAD').decode().splitlines()
if not changes or any(not row.startswith('A\tresearch/' + slug + '/') for row in changes):
    raise ValueError('Publication must add only the intended package')
entries = []
for line in git('ls-tree', '-r', 'HEAD', '--', 'research/' + slug).decode().splitlines():
    info, path = line.split('\t')
    mode, typ, sha = info.split()
    row = {'path': path, 'mode': mode, 'type': typ}
    if '/inputs/' in path or path.endswith('/LICENSE'):
        row['sha'] = sha
    else:
        row['content'] = git('cat-file', 'blob', sha).decode('utf-8')
    entries.append(row)
result = {'base': base, 'base_tree': base_tree,
          'local_commit': git('rev-parse', 'HEAD').decode().strip(),
          'expected_tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
          'branch': 'research/' + slug + '-20261114', 'entries': entries}
raw = json.dumps(result, ensure_ascii=False)
Path(stem + '-publish.json').write_text(raw)
for start in range(0, len(raw), 28000):
    Path(stem + '-segment-' + str(start // 28000) + '.txt').write_text(raw[start:start + 28000])
print(json.dumps({**{k: v for k, v in result.items() if k != 'entries'},
                  'files': len(entries), 'segments': (len(raw) + 27999) // 28000}))
