"""Python entry point for the retained Node scientific verifier."""
from pathlib import Path
import shutil
import subprocess

node = shutil.which("node")
if node is None:
    raise SystemExit("Node 18 or newer is required; see VALIDATION.md")
subprocess.run([node, str(Path(__file__).with_name("verify.js"))], check=True)
