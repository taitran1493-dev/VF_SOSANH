with open('build_new_15_cars_database.py', encoding='utf-8') as f:
    text = f.read()
import re
car_ids = re.findall(r"'id':\s*'([^']+)'", text)
print('Current car IDs in builder:', len(car_ids), car_ids)
