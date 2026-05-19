#!/usr/bin/env python3
"""
生成日报 HTML 的脚本（渲染模板）。
工作方式：
 - 优先调用 scrapers.scrape_data.get_report_data()（如果仓库提供 scrapers/scrape_data.py）
 - 或者读取 tools/data.json（如果存在）
 - 否则输出一个带占位符的静态报告，避免失败阻断 workflow（便于调试）
输出：index.html（或 --output 指定的文件）
"""

import os
import sys
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import argparse

ROOT = os.path.dirname(os.path.dirname(__file__))  # repo root
TEMPLATES_DIR = os.path.join(ROOT, 'templates')

def load_from_scraper():
    try:
        # 如果仓库提供 scrapers/scrape_data.py，则调用其 get_report_data()
        import importlib
        scraper = importlib.import_module('scrapers.scrape_data')
        if hasattr(scraper, 'get_report_data'):
            return scraper.get_report_data()
    except Exception as e:
        print(f"[scraper] no scraper available or scraper failed: {e}")
    return None

def load_from_json():
    path = os.path.join(ROOT, 'tools', 'data.json')
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[json] load failed: {e}")
    return None

def placeholder_data():
    today = datetime.utcnow().strftime('%Y-%m-%d')
    return {
        "date": today,
        "summary": "占位：未检测到可用数据源。请在仓库中添加 scrapers/scrape_data.py 或 tools/data.json。",
        "outer": [
            "外围市场震荡，科技股相对活跃（占位）。",
            "政策与行业事件：创新药、矿业论坛（占位）"
        ],
        "hot_themes": [
            {"name":"AI/光通信","notes":"占位逻辑"},
            {"name":"矿业/锂","notes":"占位逻辑"},
            {"name":"创新药","notes":"占位逻辑"}
        ],
        "top_stocks": {
            "AI": {"mid":["光迅科技","沪硅产业","立昂微"], "sentiment":["光迅科技","彩讯股份","立昂微"]},
            "mining": {"mid":["洛阳钼业","赣锋锂业","天齐锂业"], "sentiment":["洛阳钼业","赣锋锂业","天齐锂业"]},
            "pharma": {"mid":["前沿生物","贝泰妮","昂利康"], "sentiment":["前沿生物","贝泰妮","昂利康"]}
        },
        "conclusion": "请部署或提供爬虫/数据以获得实时报告。"
    }

def render(data, output_path):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    tpl = env.get_template('report_template.html')
    html = tpl.render(data=data)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[ok] wrote {output_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='index.html')
    args = parser.parse_args()

    # 1. 优先 scraper
    data = load_from_scraper()
    if data:
        print("[info] data loaded from scrapers.scrape_data.get_report_data()")
    else:
        # 2. 尝试本地 json
        data = load_from_json()
        if data:
            print("[info] data loaded from tools/data.json")
        else:
            # 3. 占位
            data = placeholder_data()
            print("[warn] using placeholder data")

    # ensure date
    if 'date' not in data:
        data['date'] = datetime.utcnow().strftime('%Y-%m-%d')

    out = args.output
    render(data, out)

if __name__ == '__main__':
    main()
