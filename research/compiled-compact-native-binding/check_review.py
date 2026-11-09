"""Replay the unmodified independent review in an isolated temporary directory."""
from pathlib import Path
import hashlib
import json
import marshal
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / 'review/independent_native_codec.py'
SCRIPT_SHA256 = '827491e62d6288720ce54aec4791b34d500cd3edaa126f66b6a770fa82261120'
ORIGINAL_RECEIPT_SHA256 = '55975729a6cf56c60d0e7abdc962e4173bc71b4047a3c8dffb304435a042090d'
RECEIPT_SHA256 = 'c7737d83a48fc522036db751b3391b3724a168bfd444418d0fc7fa3fa92a4960'


def main():
    if hashlib.sha256(SCRIPT.read_bytes()).hexdigest() != SCRIPT_SHA256:
        raise ValueError('independent review copy differs')
    name = 'normal' if __debug__ else 'optimized'
    original = HERE / ('review/independent-native-codec-' + name + '.json')
    if hashlib.sha256(original.read_bytes()).hexdigest() != ORIGINAL_RECEIPT_SHA256:
        raise ValueError('original independent receipt copy differs')
    recorded = HERE / ('review/independent-native-codec-current-' + name + '.json')
    if hashlib.sha256(recorded.read_bytes()).hexdigest() != RECEIPT_SHA256:
        raise ValueError('current independent review receipt differs')
    old_report, new_report = json.loads(original.read_text()), json.loads(recorded.read_text())
    old_report.pop('codec_sha256'); new_report.pop('codec_sha256')
    if old_report != new_report:
        raise ValueError('noncosmetic difference from independent frozen receipt')
    refinement = json.loads((HERE / 'review/WHITESPACE-REFINEMENT.json').read_text())
    for row in refinement['files']:
        after = (HERE / row['path']).read_bytes()
        before = after + b'\n' * row['removed_final_newlines']
        if (hashlib.sha256(before).hexdigest() != row['before_sha256']
                or hashlib.sha256(after).hexdigest() != row['after_sha256']):
            raise ValueError('whitespace-only source refinement differs')
        for mode in row['compiled']:
            left = marshal.dumps(compile(before, row['path'], 'exec', optimize=mode['optimize']))
            right = marshal.dumps(compile(after, row['path'], 'exec', optimize=mode['optimize']))
            if left != right:
                raise ValueError('whitespace refinement changes compiled module')
    with tempfile.TemporaryDirectory(prefix='compiled-compact-codec-review-') as directory:
        output = Path(directory) / 'receipt.json'
        flags = [] if __debug__ else ['-O']
        subprocess.run([sys.executable, '-I', *flags, '-B', str(SCRIPT),
                        '--package', str(HERE), '--output', str(output)], check=True)
        if json.loads(output.read_text()) != json.loads(recorded.read_text()):
            raise ValueError('independent codec receipt differs')
    print('PASS_PORTABLE_INDEPENDENT_NATIVE_CODEC_' + name.upper())


if __name__ == '__main__':
    main()
