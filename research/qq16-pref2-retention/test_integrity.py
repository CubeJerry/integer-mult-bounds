"""Fail-closed CLI checks, including optimized and relocated execution.

@CubeJerry with substantial OpenAI Codex assistance. Apache-2.0.
"""

from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[1]


class IntegrityTests(unittest.TestCase):
    def test_relocation_read_only_and_corruptions(self):
        with tempfile.TemporaryDirectory(prefix='qq16-pref2-') as folder:
            root = Path(folder)
            package = root / 'research' / PACKAGE.name
            shutil.copytree(PACKAGE, package, ignore=shutil.ignore_patterns('__pycache__'))
            pins = json.loads((package / 'SOURCES.json').read_text())['files']
            for pin in pins:
                if pin['usage'] == 'input':
                    target = root / pin['path']
                    target.parent.mkdir(parents=True, exist_ok=True)
                    # A source export, with no Git and no reliance on cwd/import paths.
                    shutil.copyfile(ROOT / pin['path'], target)

            def snapshot():
                return {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
                        for p in root.rglob('*') if p.is_file()}

            def run(expected_code, message=None, *extra):
                proc = subprocess.run([sys.executable, '-I', '-O', '-B',
                                       str(package / 'verify.py'), '--repo', str(root), *extra],
                                      cwd=folder, capture_output=True, text=True, timeout=90)
                self.assertEqual(proc.returncode, expected_code, proc.stdout + proc.stderr)
                if message:
                    self.assertIn(message, proc.stdout + proc.stderr)
                return proc

            before = snapshot()
            run(0, 'PASS_QQ16_PREF2_RETENTION')
            self.assertEqual(before, snapshot(), 'normal acceptance must not rewrite evidence')
            receipt = package / 'RESULT.json'
            clean_receipt = receipt.read_bytes()
            altered = json.loads(clean_receipt)
            altered['actual_minor_adapter']['complete_child_calls'] = 23
            receipt.write_text(json.dumps(altered))
            run(1, 'committed result differs')
            receipt.write_bytes(clean_receipt)
            source = root / 'research/joint-query/evidence/CONSERVED-QQ16.md'
            clean_source = source.read_bytes()
            source.write_bytes(clean_source + b'\nchanged\n')
            run(1, 'source hash:')
            source.write_bytes(clean_source)
            run(2, 'unrecognized arguments', '--accept-missing-checkpoint')
            run(1, 'File exists', '--write-result', str(receipt))
            self.assertEqual(before, snapshot(), 'controls must restore their own fixture')


if __name__ == '__main__':
    unittest.main()
