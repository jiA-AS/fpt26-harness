#!/usr/bin/env python3
"""Convert Xilinx Vitis-HLS-Introductory-Examples to fpt26-harness tasks format."""

import os, re, shutil, json
from pathlib import Path

SRC = Path(r"E:\FPGA\project\FPT\xilinx_hls_examples")
DST = Path(r"E:\FPGA\project\FPT\fpt26-harness\tasks_xilinx")

# Categories -> difficulty + task_type mapping
CATEGORY_META = {
    "Modeling": (3, "optimize"),
    "Pipelining": (5, "optimize"),
    "Array": (5, "optimize"),
    "DSP": (7, "optimize"),
    "Interface": (5, "optimize"),
    "Task_level_Parallelism": (7, "structural"),
    "Misc": (3, "generate"),
    "Images": (7, "optimize"),
    "Migration": (3, "generate"),
}

def parse_tcl(tcl_path: str) -> dict:
    """Extract top function, kernel files, tb files from run_hls.tcl."""
    text = Path(tcl_path).read_text(encoding="utf-8", errors="ignore")
    top = ""
    kernel_files = []
    tb_files = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("set_top"):
            top = line.split()[-1].strip()
        elif line.startswith("add_files") and "-tb" not in line:
            f = line.replace("add_files", "").strip()
            if f and not f.startswith("#"):
                kernel_files.append(f)
        elif "add_files -tb" in line:
            f = line.replace("add_files -tb", "").strip()
            if f and not f.startswith("#"):
                tb_files.append(f)
    return {"top": top, "kernels": kernel_files, "tb": tb_files}

def convert():
    DST.mkdir(parents=True, exist_ok=True)
    count = 0

    for cat_dir in sorted(SRC.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        cat_name = cat_dir.name
        diff, task_type = CATEGORY_META.get(cat_name, (3, "generate"))

        # Recursively find all run_hls.tcl
        for tcl in sorted(cat_dir.rglob("run_hls.tcl")):
            ex_dir = tcl.parent
            # Build unique task ID from full relative path
            rel = ex_dir.relative_to(SRC)
            task_id = str(rel).replace("/", "_").replace("\\", "_")

            info = parse_tcl(str(tcl))
            if not info["top"]:
                continue

            task_id = f"{cat_name}_{ex_dir.name}"
            task_dir = DST / task_id
            task_dir.mkdir(parents=True, exist_ok=True)
            top = info["top"]

            # Copy all source files (preserve original names)
            kernel_file = ""
            header_files = []
            for kf in info["kernels"]:
                src = ex_dir / kf
                if src.exists() and src.is_file():
                    shutil.copy(src, task_dir / kf)
                    if not kernel_file:
                        kernel_file = kf  # first kernel file is the main one
            # Copy all headers
            for h in ex_dir.glob("*.h"):
                if h.is_file():
                    shutil.copy(h, task_dir / h.name)
                    header_files.append(h.name)

            # Copy testbench + data directory
            tb_file = ""
            for tb in info["tb"]:
                src = ex_dir / tb
                if src.exists() and src.is_file():
                    shutil.copy(src, task_dir / tb)
                    if not tb_file:
                        tb_file = tb
            # Copy data directory if exists (needed by some DSP examples)
            data_dir = ex_dir / "data"
            if data_dir.is_dir():
                shutil.copytree(data_dir, task_dir / "data", dirs_exist_ok=True)

            if not kernel_file:
                continue

            # Description from README
            readme = ex_dir / "README"
            desc = readme.read_text(encoding="utf-8", errors="ignore")[:500] if readme.exists() else cat_name

            # task.toml
            hdr_list = str(header_files).replace("'", '"')
            toml = f"""task_id = "{task_id}"
task_type = "{task_type}"
difficulty = {diff}
top = "{top}"
kernel_file = "{kernel_file}"
header_files = {hdr_list}
public_tb = "{tb_file}"
budget = 60
initial_condition = "Xilinx HLS introductory example: {cat_name}/{ex_dir.name}"

[target]
part = "xcu55c-fsvh2892-2L-e"
clock_ns = 5.0
"""
            (task_dir / "task.toml").write_text(toml, encoding="utf-8")
            (task_dir / "description.md").write_text(desc, encoding="utf-8")
            count += 1

    print(f"Converted {count} tasks to {DST}")


if __name__ == "__main__":
    convert()
