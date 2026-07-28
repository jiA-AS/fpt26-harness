# FPT26 赛道一（Track A）正确率提升方案 — 执行蓝图

## 背景判断
- 用户目标：复现/超越截图中的跑分（DeepSeek V4 Pro 147/150、Qwen3.5 122B 146/150、Qwen3.6 27B 132/150）
- 本地仓库 `E:\FPGA\project\FPT\fpt26-harness` = 官方参考实现（仅 3 个示例 task、单任务 runner）
- 截图报告含 `FINAL_SUMMARY.md` / `retry_ids` / `real_api_only` / 150 task 批量评测 —— 这些功能官方仓库**没有**，需要自建
- 沙箱无法访问用户 Windows 本地磁盘 → 交付物 = 可直接拷贝落地的代码 + 操作方案

## 阶段
1. **调研（已完成，由主 agent 执行）**：通读 fpt26-harness 全部源码（agent/llm/harness/budget/task/scoring/config），定位与截图报告的差距
2. **代码产出（本阶段）**：编写 3 个可直接替换/新增的文件
   - `llm.py`（替换）：OpenRouter 调用加指数退避重试 + 调用审计（real_api_only 依据）
   - `agent.py`（替换）：修复/优化轮数分离、低温度修复、错误行提取反馈、免费 preflight（省 credit）
   - `run_batch.py`（新增）：多模型 × 多任务批量 runner，断点续跑、失败补跑（retry_ids）、FINAL_SUMMARY.md 生成
3. **方案文档**：README_提升方案.md —— 环境（Vitis 2025.2 Docker/WSL2）、150 任务集获取（官方发布 or Bench4HLS 转换）、运行命令、调参表、正确率杠杆排序
4. **交付**：打包 zip，附 KIMI_REF

## 交付物路径
/mnt/agents/output/fpt26_trackA/
  plan.md / README_提升方案.md / llm.py / agent.py / run_batch.py / fpt26_trackA_solution.zip
