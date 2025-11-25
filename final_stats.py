import json
from pathlib import Path

json_path = Path(__file__).parent / 'hydrobench-eval' / 'hydrobench' / 'data' / 'hydrobench.json'

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

names = {
    'BK': 'Background Knowledge (背景知识)',
    'IS': 'Industry Standard (行业标准)',
    'HWR': 'Hydrology and Water Resources (水文水资源)',
    'GE': 'Geotechnical Engineering (岩土工程)',
    'HSE': 'Hydraulic Structures and Equipment (水工结构与设备)',
    'ESM': 'Engineering Safety and Management (工程安全与管理)',
    'HRD': 'Hydraulics and River Dynamic (水力学与河流动力学)',
    'M': 'Meteorology (气象学)',
    'PS': 'Power System (电力系统)'
}

order = ['HWR', 'GE', 'HSE', 'ESM', 'HRD', 'M', 'PS', 'BK', 'IS']

print('\n'.join([
    f"| **{cat}** | {names[cat]} | {cats[cat]['total']} | {cats[cat]['single']} | {cats[cat]['multiple']} | {cats[cat]['basic']/cats[cat]['total']*100:.1f}% | {cats[cat]['app']/cats[cat]['total']*100:.1f}% | {cats[cat]['calc']/cats[cat]['total']*100:.1f}% |"
    for cat in order
]))

