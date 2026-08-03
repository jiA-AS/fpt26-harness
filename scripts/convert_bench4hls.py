#!/usr/bin/env python3
"""Convert Bench4HLS to fpt26-harness tasks_all with mixed task types.

Type allocation (competition requirement):
  Prob001-050: "generate"  — empty skeleton
  Prob051-100: "optimize" — pragmas removed
  Prob101-150: "repair"   — subtle bug introduced
  Prob151-170: "optimize" — pragmas stripped
"""

import json
import os
import re
import shutil
from pathlib import Path

BENCH_DIR = Path(r"E:\FPGA\project\FPT\Bench4HLS\benchmark")
TASKS_DIR = Path(r"E:\FPGA\project\FPT\fpt26-harness\tasks_all")
TOP_FN = "TopModule"

def parse_prototype(ref_code: str) -> str:
    """Extract function signature from reference C++ code."""
    lines = ref_code.split("\n")
    sig_lines = []
    in_sig = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if f"void {TOP_FN}(" in stripped or f"void {TOP_FN} (" in stripped:
            in_sig = True
        if in_sig:
            sig_lines.append(stripped)
            if ")" in stripped and not stripped.startswith("//"):
                break
    return " ".join(sig_lines).replace("  ", " ")


def generate_skeleton(signature: str) -> str:
    """Generate empty skeleton C++ from function signature."""
    return f"""#include "ap_int.h"

{signature}
    // TODO: implement
}}
"""


def generate_header(signature: str) -> str:
    """Generate header file."""
    semicolon = re.sub(r"\s*\{.*", ";", signature) if "{" in signature else signature.rstrip()
    if not semicolon.endswith(";"):
        semicolon = semicolon.rstrip() + ";"
    return f"""#ifndef TOPMODULE_H
#define TOPMODULE_H

#include "ap_int.h"

{semicolon}

#endif
"""


def estimate_difficulty(prob_num: int) -> int:
    if prob_num <= 50:
        return 1  # very easy
    elif prob_num <= 100:
        return 3  # easy
    elif prob_num <= 150:
        return 5  # medium
    else:
        return 7  # hard


def generate_unoptimized(ref_code: str) -> str:
    """Remove HLS pragmas for 'optimize' tasks."""
    lines = ref_code.split("\n")
    return "\n".join(l for l in lines if "#pragma HLS" not in l)


def generate_buggy(ref_code: str) -> str:
    """Comment out first assignment for 'repair' tasks."""
    lines = ref_code.split("\n")
    result = []
    found = False
    for line in lines:
        s = line.strip()
        if not found and "=" in s and not s.startswith("//") and not s.startswith("#"):
            result.append(f"    // BUG: fix the commented assignment below")
            result.append(f"    // {s}")
            found = True
        else:
            result.append(line)
    return "\n".join(result)


def get_task_type_and_code(prob_num, ref_code, sig):
    """Return (task_type, starting_code, initial_condition)."""
    if prob_num <= 50:
        return ("generate", generate_skeleton(sig),
                "Empty skeleton — write the full kernel from scratch.")
    elif prob_num <= 100:
        return ("optimize", generate_unoptimized(ref_code),
                "Correct but unoptimized — HLS pragmas removed.")
    elif prob_num <= 150:
        return ("repair", generate_buggy(ref_code),
                "Compiles but has a functional bug — find and fix it.")
    else:
        return ("optimize", generate_unoptimized(ref_code),
                "Correct but unoptimized — HLS pragmas stripped.")


def convert():
    # Load metadata
    prompts_json = BENCH_DIR / "input_prompts.json"
    with open(prompts_json) as f:
        data = json.load(f)

    tasks = data  # it's a plain list, not {"value": [...]}
    print(f"Found {len(tasks)} tasks")

    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    type_counts = {}

    for task in tasks:
        prob_id = task["task_n"]  # e.g., "Prob001"
        description = task["input"]
        prob_num = int(prob_id.replace("Prob", ""))

        task_dir = TASKS_DIR / prob_id
        task_dir.mkdir(parents=True, exist_ok=True)

        # --- Reference code ---
        ref_src = BENCH_DIR / "reference_design" / f"{prob_id}_ref.cpp"
        if ref_src.exists():
            ref_code = ref_src.read_text(encoding="utf-8")
            ref_dir = task_dir / "reference"
            ref_dir.mkdir(exist_ok=True)
            shutil.copy(ref_src, ref_dir / f"{TOP_FN}.cpp")
        else:
            ref_code = ""
            print(f"  WARNING: no reference for {prob_id}")

        # --- Testbench ---
        tb_src = BENCH_DIR / "testbenches" / f"{prob_id}_tb.cpp"
        if tb_src.exists():
            shutil.copy(tb_src, task_dir / f"{TOP_FN}_tb.cpp")

        # --- Task type & starting code ---
        sig = parse_prototype(ref_code) if ref_code else f"void {TOP_FN}();"
        task_type, starting_code, initial_condition = get_task_type_and_code(prob_num, ref_code, sig)
        type_counts[task_type] = type_counts.get(task_type, 0) + 1

        (task_dir / f"{TOP_FN}.cpp").write_text(starting_code, encoding="utf-8")
        (task_dir / f"{TOP_FN}.h").write_text(generate_header(sig), encoding="utf-8")
        (task_dir / "description.md").write_text(description, encoding="utf-8")

        # --- task.toml ---
        difficulty = estimate_difficulty(prob_num)
        toml_content = f"""task_id = "{prob_id}"
task_type = "{task_type}"
difficulty = {difficulty}
top = "{TOP_FN}"
kernel_file = "{TOP_FN}.cpp"
header_files = ["{TOP_FN}.h"]
public_tb = "{TOP_FN}_tb.cpp"
budget = 60
initial_condition = "{initial_condition}"

[target]
part = "xcu55c-fsvh2892-2L-e"
clock_ns = 5.0
"""
        (task_dir / "task.toml").write_text(toml_content, encoding="utf-8")

    print(f"Done! Created {len(tasks)} tasks in {TASKS_DIR}")
    print(f"  Type distribution: {type_counts}")


if __name__ == "__main__":
    convert()
