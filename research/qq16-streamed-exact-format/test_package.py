#!/usr/bin/env python3
"""Source/export/failure controls; no Git, network, or predecessor imports.

@CubeJerry, substantial OpenAI Codex assistance; Apache-2.0.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RELATIVE = HERE.relative_to(ROOT)


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fingerprint(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob("*") if p.is_file()}


def export(root):
    destination = root / RELATIVE
    shutil.copytree(HERE, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for row in json.loads((HERE / "SOURCES.json").read_bytes())["files"]:
        if row["usage"] == "input":
            target = root / row["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / row["path"], target)
    return destination


def run(root, script="verify.py", optimized=False, arguments=()):
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.pop("PYTHONOPTIMIZE", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    with tempfile.TemporaryDirectory(prefix="qq16-pyc-") as cache:
        # -B alone does not prevent reading preexisting bytecode.
        env["PYTHONPYCACHEPREFIX"] = cache
        argv = [sys.executable, "-B"] + (["-O"] if optimized else [])
        argv += [str(root / RELATIVE / script), *arguments]
        return subprocess.run(argv, cwd=root, env=env, capture_output=True,
                              text=True, timeout=180)


def main():
    controls = 0
    with tempfile.TemporaryDirectory(prefix="qq16-format-export-") as work:
        work = Path(work)
        readonly = work / "read-only-without-git"
        package = export(readonly)
        require(not (readonly / ".git").exists(), "Git-free export")
        before = fingerprint(readonly)
        for path in sorted(readonly.rglob("*"), reverse=True):
            path.chmod(0o555 if path.is_dir() else 0o444)
        readonly.chmod(0o555)
        try:
            for optimized in (False, True):
                for script, marker in (("verify.py", "PASS_QQ16_STREAMED_EXACT_FORMAT"),
                                       ("independent.py", "PASS_INDEPENDENT_STREAMED_FORMAT"),
                                       ("test_numerical.py", "PASS_STREAMED_FORMAT_NUMERICAL")):
                    result = run(readonly, script, optimized)
                    require(result.returncode == 0 and marker in result.stdout,
                            f"export replay {script} -O={optimized}: {result.stderr}")
            require(fingerprint(readonly) == before, "replay changed exported bytes")
        finally:
            readonly.chmod(0o755)
            for path in readonly.rglob("*"):
                path.chmod(0o755 if path.is_dir() else 0o644)

        target_root = work / "mutation"
        target = export(target_root)

        def reject(path, change, message, *, script="verify.py"):
            nonlocal controls
            original = path.read_bytes()
            try:
                path.write_bytes(change(original))
                for optimized in (False, True):
                    result = run(target_root, script, optimized)
                    require(result.returncode != 0 and message in result.stderr,
                            f"control did not fail correctly: {message}: {result.stderr}")
                controls += 1
            finally:
                path.write_bytes(original)

        def edited(fn):
            def change(raw):
                value = json.loads(raw)
                fn(value)
                return (json.dumps(value) + "\n").encode()
            return change

        reject(target / "retained/PR4015-WORD.json", lambda b: b + b" ", "retained source hash")
        reject(target / "retained/PR4015-PROOF.md", lambda b: b + b" ", "retained source hash")
        reject(target_root / "research/qq16-line-normalized-decoder/WORD.json",
               lambda b: b + b" ", "canonical source hash")
        reject(target / "RETAINED.json", lambda b: b + b" ", "retained manifest changed")
        reject(target / "SOURCES.json", lambda b: b + b" ", "source manifest changed")
        reject(target / "RESULT.json", edited(lambda x: x["streamed"].update(events=True)),
               "complete typed result differs")
        reject(target / "RESULT.json", edited(lambda x: x["streamed"].update(private_fields_zero=1)),
               "complete typed result differs")
        reject(target / "RESULT.json", edited(lambda x: x.update(unchecked_extra="must reject")),
               "complete typed result differs")
        reject(target / "RESULT.json", edited(lambda x: x["streamed"]["final_outputs"]["Z0"].update(poly=["0"])),
               "complete typed result differs")
        reject(target / "TRACE.json", edited(lambda x: x["streamed"][1][2].update(grid=[[1, 0]])),
               "complete typed cut trace differs")
        reject(target / "TRACE.json", edited(lambda x: x["streamed"].pop()),
               "trace receipt binding", script="independent.py")
        reject(target / "retained/PR4015-WORD.json", lambda b: b + b" ",
               "retained byte pin", script="independent.py")
        reject(target / "LOWERING.json", edited(lambda x: x["rows"][1]["paired"].update(clear=5)),
               "complete typed lowering receipt", script="test_numerical.py")
        before = fingerprint(target_root)
        result = run(target_root, arguments=("--write",))
        require(result.returncode != 0 and "generation refuses overwrite" in result.stderr,
                "generation must not overwrite certificates")
        require(fingerprint(target_root) == before, "refused generation changed bytes")
        controls += 1
    print("PASS_STREAMED_FORMAT_EXPORT", "git_free=1 permission_read_only=1 unchanged_bytes=1",
          "normal_and_optimized=1 corruptions=" + str(controls - 1),
          "overwrite_rejection=1 no_new_kappa")


if __name__ == "__main__":
    main()
