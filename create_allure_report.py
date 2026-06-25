import os
import json
from datetime import datetime

# יצור allure-results directory
os.makedirs('allure-results', exist_ok=True)

# קרא את JSON report
with open('report.json', 'r') as f:
    data = json.load(f)

# צור Allure result לכל טסט
for i, test in enumerate(data.get('tests', [])):
    result = {
        "name": test['nodeid'],
        "status": "passed" if test['outcome'] == 'passed' else "failed",
        "stage": "finished",
        "start": int(datetime.now().timestamp() * 1000),
        "stop": int(datetime.now().timestamp() * 1000),
        "duration": int(test.get('duration', 0) * 1000),
    }

    # שמור בformat של Allure
    with open(f'allure-results/{i}-result.json', 'w') as f:
        json.dump(result, f)

print("✅ Allure results created!")
print("Run: allure serve allure-results")