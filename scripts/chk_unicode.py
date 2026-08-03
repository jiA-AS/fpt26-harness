import sys
sys.path.insert(0, r'e:\FPGA\project\FPT\fpt26-harness')
from llm4hls.task import load_task
t = load_task(r'e:\FPGA\project\FPT\fpt26-harness\tasks_xilinx_manual\fixed_point_sqrt')
# Check for non-ASCII in description
for name, content in [('desc', t.description), ('kernel', t.kernel_code)]:
    bad = [(i, hex(ord(c))) for i, c in enumerate(content) if ord(c) > 127]
    if bad:
        print(f'{name}: NON-ASCII at {bad[:5]}')
    else:
        print(f'{name}: OK')
