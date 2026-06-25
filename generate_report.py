import subprocess
import json
import os

# הרץ pytest עם JSON report
subprocess.run([
    "pytest", "test_full_app.py",
    "-v",
    "--json-report",
    "--json-report-file=report.json"
])

print("✅ Report generated at report.json")