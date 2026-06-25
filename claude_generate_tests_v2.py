import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

app_info = """
QA Automation Web App at http://localhost:5001

HTML STRUCTURE (IMPORTANT):
Login Form:
- #login-email (email input)
- #login-password (password input)
- button with text "Login" (index 1)

Register Form:
- #reg-username (username input)
- #reg-email (email input)
- #reg-password (password input)
- button with text "Register" (index 1)

Navigation:
- nav button:nth-of-type(1) = Login
- nav button:nth-of-type(2) = Register
- nav button:nth-of-type(3) = Products
- nav button:nth-of-type(4) = Cart
- nav button:nth-of-type(5) = Admin
- nav button:nth-of-type(6) = About

Products Page:
- .product-card (product container)
- .product-name (product name)
- .product-price (product price)
- button:has-text("Add to Cart") (add to cart button)

Admin Page (when logged in as admin):
- #admin-product-name (name input)
- #admin-product-price (price input)
- #admin-product-description (description input)
- button:has-text("Add Product") (submit button)

Cart Page:
- .cart-item (cart item)
- button:has-text("Checkout") (checkout button)

Messages:
- #message (message div)
"""

message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": f"""Write 5 NEW Playwright pytest tests for this app using EXACT HTML selectors:

{app_info}

Write tests for:
1. Register new user (use #reg-email, #reg-username, #reg-password)
2. Login existing user (use #login-email, #login-password)
3. Add product to cart
4. Navigate to products
5. Admin add product (if user is admin)

Use the EXACT selectors provided above!
Return ONLY Python code, no explanations."""
        }
    ]
)

tests_code = message.content[0].text
tests_code = tests_code.replace("```python", "").replace("```", "").strip()

with open("test_claude_v2.py", "w") as f:
    f.write(tests_code)

print("✅ Claude generated tests with correct selectors!")
print("\nFirst 300 chars:")
print(tests_code[:300])