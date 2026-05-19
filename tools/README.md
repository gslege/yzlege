# 自动化日报工具说明

目标：
- 在 GitHub Actions 中运行 tools/generate_report.py，生成 index.html 并提交回仓库。

数据源优先级：
1. scrapers/scrape_data.py -> 函数 get_report_data() 返回 dict（推荐）
2. tools/data.json -> 本地 JSON 文件（测试时可用）
3. 无以上则使用占位模板（避免失败）

scrapers/scrape_data.py 示例接口：
```python
def get_report_data():
    return {
        "date": "2026-05-15",
        "outer": ["...","..."],
        "hot_themes": [{"name":"AI","notes":"..."}, ...],
        "top_stocks": { "AI": {"mid":[...], "sentiment":[...]} },
        "conclusion": "..."
    }
