"""Bounded source, bridge, semantics and independent endpoint review.

The multi-hour actual physical command is verify.py, explicitly separate.
The default hook requires and reviews its completed retained receipt.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def scientific(record):
    return {k: v for k, v in record.items() if k != 'seconds'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prephysical-only', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    records = []
    for manifest in ('EXECUTION-SOURCES.json', 'INDEPENDENT-SOURCES.json'):
        for row in json.loads((HERE/manifest).read_text())['files']:
            path = HERE/row['path']
            need(path.is_file() and not path.is_symlink(), 'regular checked body '+row['path'])
            raw = path.read_bytes()
            need(len(raw) == row['bytes'] and sha256(raw).hexdigest() == row['sha256'],
                 'unchanged execution/reviewer bytes '+row['path'])
    physical = HERE/'PHYSICAL-RESULT.json'
    if not args.prephysical_only:
        need(physical.is_file(), 'completed extended physical receipt required')
        observed = json.loads(physical.read_text())
        need(observed['status'] == 'PASS_ACTUAL_COMPLETE_CORE_HALO_JOIN',
             'actual complete physical receipt, not semantic replacement')
        need(observed['complete_dense_events'] == 477
             and observed['allocation']['labels'] == 2
             and observed['allocation']['side'] == 8
             and observed['complete_sparse_calls'] == [2, 2],
             'complete declared original-layout physical fixture')
        completion_path = HERE/'PHYSICAL-EXIT.json'
        need(completion_path.is_file(), 'observed successful exit after trailing teardown required')
        completion = json.loads(completion_path.read_text())
        need(completion['status'] == 'OBSERVED_PROCESS_EXIT_ZERO_AFTER_TEARDOWN'
             and completion['exit_code'] == 0
             and completion['receipt_written_before_teardown'] is True
             and completion['teardown_completed'] is True,
             'separate observed process-completion gate')
        for key, filename in (('driver', 'verify.py'), ('receipt', physical.name),
                              ('log', 'PHYSICAL-EXECUTION.log')):
            path = HERE/filename
            need(path.is_file() and completion[key]['path'] == filename
                 and completion[key]['sha256'] == sha256(path.read_bytes()).hexdigest(),
                 'process-completion record binds exact '+key)
        need(completion['source_parameters'] == observed['source']['parameters']
             and completion['reference_sha256'] == observed['source']['reference_sha256'],
             'same completed source identity')
    with tempfile.TemporaryDirectory(prefix='actual-core-halo-review-') as work:
        work = Path(work)

        def run(name, *arguments):
            cache = work/('bytecode-'+str(len(records)))
            argv = [sys.executable, '-B', '-X', 'pycache_prefix='+str(cache)]
            if sys.flags.optimize:
                argv += ['-O' if sys.flags.optimize == 1 else '-OO']
            argv += [str(HERE/name), *(str(x) for x in arguments)]
            before = time.monotonic()
            result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, check=False)
            if result.returncode:
                sys.stderr.write(result.stdout+result.stderr)
                raise ValueError('failed source-bound Core/halo check: '+name)
            records.append(dict(check=name, seconds=time.monotonic()-before,
                                stdout_sha256=sha256(result.stdout.encode()).hexdigest()))
            print('PASS '+name, flush=True)

        run('review/a4-analytic-cross-review/verify_hashes.py', '--package', HERE)
        preflight = work/'preflight.json'
        run('verify.py', '--preflight', '--output', preflight)
        fresh = json.loads(preflight.read_text())
        retained = json.loads((HERE/'PROBE.json').read_text())
        for key in ('allocation', 'source', 'halo', 'complete_dense_events',
                    'setup_source_inventory', 'blocks'):
            need(fresh[key] == retained[key], 'same admitted physical preflight '+key)

        bridge = work/'bridge.json'
        run('review/bridge_review.py', '--package', HERE, '--output', bridge)
        need(json.loads(bridge.read_text()) ==
             json.loads((HERE/'review/bridge-review-normal.json').read_text()),
             'independent bridge science and operation counts unchanged')

        axes = work/'axes.json'
        run('review/axis_binding_review.py', '--package', HERE, '--output', axes)
        need(json.loads(axes.read_text()) ==
             json.loads((HERE/'review/axis-binding-normal.json').read_text()),
             'independent original-axis and source binding unchanged')

        semantic = work/'semantic.json'
        run('semantic_halo.py', '--output', semantic)
        need(scientific(json.loads(semantic.read_text())) ==
             scientific(json.loads((HERE/'SEMANTIC-RESULT.json').read_text())),
             'all semantic, bridge, halo and machine fields agree')
        observations = [semantic]
        if not args.prephysical_only:
            observations.append(physical)
        periodic = work/'periodic.json'
        run('review/periodic_review.py', '--package', HERE,
            '--observed', *observations, '--output', periodic)
        report = json.loads(periodic.read_text())
        need(report['status'] == 'INDEPENDENT_ORIGINAL_CORE_HALO_OBSERVER_PASS'
             and len(report['observations']) == len(observations),
             'all actual original-matrix endpoint assertions executed')
        observation_keys = ('observed_status', 'observed_scope', 'observation_file',
                            'observation_sha256', 'period', 'side', 'precision', 'q',
                            'kept', 'discarded', 'all_original_addresses_checked',
                            'bit_exact_merge_and_rounding',
                            'kept_halo_substitution_numerically_distinguished',
                            'adversarial_observation_controls')
        answer = dict(status=('PASS_PREPHYSICAL_CORE_HALO_CHECKS' if args.prephysical_only
                              else 'PASS_ACTUAL_CORE_HALO_PACKAGE'),
                      optimization=sys.flags.optimize,
                      actual_extended_physical_replayed=False,
                      retained_actual_physical_reviewed=not args.prephysical_only,
                      retained_process_exit_record_checked=not args.prephysical_only,
                      complete_semantic_fixture_replayed=True,
                      analytic_review_hashes_checked_only=True,
                      independent_observations=[{k: item[k] for k in observation_keys}
                                                for item in report['observations']],
                      periodic_report_sha256=sha256(periodic.read_bytes()).hexdigest(),
                      checks=records,
                      seconds=time.monotonic()-started, no_new_kappa=True)
        encoded = json.dumps(answer, indent=2, sort_keys=True)+'\n'
        if args.output is not None:
            args.output.write_text(encoded)
        print(encoded)


if __name__ == '__main__':
    main()
