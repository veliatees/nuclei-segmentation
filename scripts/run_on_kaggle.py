"""Run the whole study on Kaggle with one command: 02 (train) -> 03 (evaluate) -> 03b (Cellpose-SAM baseline).

One-time setup on your computer:
  1. pip install kaggle
  2. kaggle.com -> your profile -> Settings -> API -> "Create New Token".
     This downloads kaggle.json. Move it to ~/.kaggle/kaggle.json and run: chmod 600 ~/.kaggle/kaggle.json

Then, from the repository folder:
  python scripts/run_on_kaggle.py            # all three notebooks, one after the other
  python scripts/run_on_kaggle.py 03 03b     # only some of them (02 must have run once before 03)

Every notebook runs as a private Kaggle notebook with GPU and internet on. Each one gets the output
of the notebook before it as input, so nothing has to be downloaded and uploaded by hand.
The outputs land in runs/<date-time>/<notebook>/ and the key result files are printed at the end.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
STEPS = {  # name: (notebook, kaggle slug, step whose output it needs)
    "02": ("notebooks/02_unet.ipynb", "nuclei-02-unet", None),
    "03": ("notebooks/03_evaluation.ipynb", "nuclei-03-evaluation", "02"),
    "03b": ("notebooks/03b_cellpose_baseline.ipynb", "nuclei-03b-cellpose-baseline", "03"),
}
SHOW = ["by_type.csv", "warning.json", "by_type_cellpose.csv", "compare.csv"]
POLL_SECONDS = 60
MAX_HOURS = 4


def kaggle(*args):
    exe = shutil.which("kaggle")
    cmd = [exe, *args] if exe else [sys.executable, "-m", "kaggle", *args]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"kaggle {' '.join(args)} failed:\n{res.stdout}\n{res.stderr}")
    return res.stdout


def username():
    cfg = Path.home() / ".kaggle" / "kaggle.json"
    if not cfg.exists():
        sys.exit(f"{cfg} not found - see the setup steps at the top of this file")
    return json.loads(cfg.read_text())["username"]


def push(user, step):
    notebook, slug, needs = STEPS[step]
    sources = [f"{user}/{STEPS[needs][1]}"] if needs else []
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(REPO / notebook, Path(tmp) / Path(notebook).name)
        meta = {"id": f"{user}/{slug}", "title": slug, "code_file": Path(notebook).name, "language": "python",
                "kernel_type": "notebook", "is_private": True, "enable_gpu": True, "enable_internet": True,
                "dataset_sources": [], "competition_sources": [], "kernel_sources": sources}
        (Path(tmp) / "kernel-metadata.json").write_text(json.dumps(meta, indent=1))
        print(f"[{step}] {kaggle('kernels', 'push', '-p', tmp).strip()}")
    return f"{user}/{slug}"


def wait(step, kernel_id):
    start = time.time()
    while True:
        out = kaggle("kernels", "status", kernel_id)
        # newer CLI prints: has status "KernelWorkerStatus.RUNNING", older: has status "running"
        m = re.search(r'status\s+"?(?:KernelWorkerStatus\.)?([A-Za-z_]+)', out)
        status = (m.group(1) if m else out.strip()).lower()
        print(f"[{step}] {datetime.now():%H:%M:%S}  {status}")
        if "complete" in status:
            return
        if "error" in status or "cancel" in status:
            sys.exit(f"[{step}] stopped with status {status}; log: https://www.kaggle.com/code/{kernel_id}")
        if time.time() - start > MAX_HOURS * 3600:
            sys.exit(f"[{step}] still running after {MAX_HOURS} h; check https://www.kaggle.com/code/{kernel_id}")
        time.sleep(POLL_SECONDS)


def main():
    steps = sys.argv[1:] or list(STEPS)
    unknown = [s for s in steps if s not in STEPS]
    if unknown:
        sys.exit(f"unknown step(s) {unknown}; choose from {list(STEPS)}")
    user = username()
    run_dir = REPO / "runs" / f"{datetime.now():%Y-%m-%d_%H-%M}"
    for step in steps:
        kernel_id = push(user, step)
        time.sleep(10)
        wait(step, kernel_id)
        target = run_dir / step
        target.mkdir(parents=True, exist_ok=True)
        kaggle("kernels", "output", kernel_id, "-p", str(target))
        print(f"[{step}] output in {target}")
    print()
    for name in SHOW:
        for f in sorted(run_dir.rglob(name)):
            print(f"===== {f.relative_to(run_dir)}")
            print(f.read_text()[:3000])


if __name__ == "__main__":
    main()
