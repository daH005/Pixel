import json
import os

base_path = '../assets/levels/'
for filename in os.listdir(base_path):
    with open(base_path + filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['is_completed'] = False

    if filename == '0.json':
        data['is_available'] = True
    else:
        data['is_available'] = False

    data['extra_data'] = {
        'ids': [],
    }

    with open(base_path + filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


with open('../assets/save.json', 'w', encoding='utf-8') as f:
    json.dump({'coins_count': 0}, f, indent=4, ensure_ascii=False)
