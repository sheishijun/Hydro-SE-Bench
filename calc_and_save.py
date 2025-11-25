import json
from pathlib import Path

json_path = Path('hydrobench-eval/hydrobench/data/hydrobench.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

examples = data.get('examples', [])

cats = {}
for e in examples:
    cat = e.get('category')
    qtype = e.get('type')
    level = e.get('level')
    if cat not in cats:
        cats[cat] = {'total': 0, 'single': 0, 'multiple': 0, 'basic': 0, 'app': 0, 'calc': 0}
    cats[cat]['total'] += 1
    if qtype == 'single choice':
        cats[cat]['single'] += 1
    elif qtype == 'multiple choice':
        cats[cat]['multiple'] += 1
    if level == 'basic conceptual knowledge':
        cats[cat]['basic'] += 1
    elif level == 'engineering applications':
        cats[cat]['app'] += 1
    elif level == 'reasoning and calculation':
        cats[cat]['calc'] += 1

names = {'BK': 'Background Knowledge (背景知识)', 'IS': 'Industry Standard (行业标准)', 'HWR': 'Hydrology and Water Resources (水文水资源)', 'GE': 'Geotechnical Engineering (岩土工程)', 'HSE': 'Hydraulic Structures and Equipment (水工结构与设备)', 'ESM': 'Engineering Safety and Management (工程安全与管理)', 'HRD': 'Hydraulics and River Dynamic (水力学与河流动力学)', 'M': 'Meteorology (气象学)', 'PS': 'Power System (电力系统)'}
order = ['HWR', 'GE', 'HSE', 'ESM', 'HRD', 'M', 'PS', 'BK', 'IS']

lines = []
for cat in order:
    s = cats[cat]
    total = s['total']
    basic_pct = s['basic'] / total * 100 if total > 0 else 0
    app_pct = s['app'] / total * 100 if total > 0 else 0
    calc_pct = s['calc'] / total * 100 if total > 0 else 0
    line = f"| **{cat}** | {names[cat]} | {total} | {s['single']} | {s['multiple']} | {basic_pct:.1f}% | {app_pct:.1f}% | {calc_pct:.1f}% |"
    lines.append(line)
    print(line)

with open('stats_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

