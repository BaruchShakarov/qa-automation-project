from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template('dashboard_new.html')  # שנה לשם החדש


@app.route('/api/results')
def get_results():
    results = {}

    if os.path.exists('allure-results'):
        for file in os.listdir('allure-results'):
            if file.endswith('-result.json'):
                try:
                    with open(f'allure-results/{file}', 'r') as f:
                        data = json.load(f)
                        fullName = data.get('fullName', 'Unknown')

                        results[fullName] = {
                            'name': fullName.split('#')[-1] if '#' in fullName else fullName,
                            'status': data.get('status', 'unknown'),
                            'duration': data.get('duration', 0)
                        }
                except:
                    pass

    tests_list = list(results.values())
    total = len(tests_list)
    passed = sum(1 for r in tests_list if r.get('status') == 'passed')
    failed = total - passed

    return jsonify({
        "total": total,
        "passed": passed,
        "failed": failed,
        "tests": tests_list
    })


if __name__ == '__main__':
    app.run(debug=True, port=5002)