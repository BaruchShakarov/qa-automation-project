import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app_info = """
QA Automation Web App at http://localhost:5001

Features:
- Login/Register: email, password, username
- Products Page: displays 3 products, Add to Cart button
- Cart Page: view items, quantity, total, Checkout button
- Admin Page: add new products with name, price, description
- About Page: static content
- Navigation: 6 buttons (Login, Register, Products, Cart, Admin, About)

Current tests: 15 (all passing)
"""

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": f"""Write 10 NEW Playwright pytest tests for this app:

{app_info}

Write tests for:
1. Cart functionality (add product, remove item, checkout)
2. User workflows (register → login → browse → add to cart)
3. Admin workflows (add product → see in product list)
4. Edge cases and error handling

Return ONLY Python code, no explanations.
Use pytest fixtures and Playwright syntax."""
        }
    ]
)

tests_code = message.content[0].text
tests_code = tests_code.replace("```python", "").replace("```", "").strip()

with open("test_claude_new.py", "w") as f:
    f.write(tests_code)

print("✅ Claude generated 10 new tests!")
print("\nFirst 300 chars:")
print(tests_code[:300])