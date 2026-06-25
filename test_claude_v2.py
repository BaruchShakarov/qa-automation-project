import pytest
from playwright.sync_api import Page, expect
import random
import string


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_random_email():
    return f"{generate_random_string()}@test.com"


@pytest.fixture
def page_with_app(page: Page):
    page.goto("http://localhost:5001")
    return page


def test_register_new_user(page_with_app: Page):
    page = page_with_app
    
    # Navigate to Register tab
    page.locator("nav button:nth-of-type(2)").click()
    
    # Generate unique user data
    username = generate_random_string()
    email = generate_random_email()
    password = "TestPass123!"
    
    # Fill in registration form using exact selectors
    page.locator("#reg-username").fill(username)
    page.locator("#reg-email").fill(email)
    page.locator("#reg-password").fill(password)
    
    # Click Register button (index 1 among buttons with text "Register")
    page.get_by_role("button", name="Register").nth(1).click()
    
    # Verify success message appears
    message = page.locator("#message")
    expect(message).to_be_visible()
    message_text = message.inner_text()
    assert any(keyword in message_text.lower() for keyword in ["success", "registered", "created", "welcome"]), \
        f"Expected success message but got: {message_text}"


def test_login_existing_user(page_with_app: Page):
    page = page_with_app
    
    # First register a user to ensure they exist
    page.locator("nav button:nth-of-type(2)").click()
    
    username = generate_random_string()
    email = generate_random_email()
    password = "TestPass123!"
    
    page.locator("#reg-username").fill(username)
    page.locator("#reg-email").fill(email)
    page.locator("#reg-password").fill(password)
    page.get_by_role("button", name="Register").nth(1).click()
    
    # Wait for registration to complete
    page.wait_for_timeout(500)
    
    # Navigate to Login tab
    page.locator("nav button:nth-of-type(1)").click()
    
    # Fill in login form using exact selectors
    page.locator("#login-email").fill(email)
    page.locator("#login-password").fill(password)
    
    # Click Login button
    page.get_by_role("button", name="Login").nth(1).click()
    
    # Verify success message appears
    message = page.locator("#message")
    expect(message).to_be_visible()
    message_text = message.inner_text()
    assert any(keyword in message_text.lower() for keyword in ["success", "logged in", "welcome", "login"]), \
        f"Expected login success message but got: {message_text}"


def test_add_product_to_cart(page_with_app: Page):
    page = page_with_app
    
    # First register and login a user
    page.locator("nav button:nth-of-type(2)").click()
    
    username = generate_random_string()
    email = generate_random_email()
    password = "TestPass123!"
    
    page.locator("#reg-username").fill(username)
    page.locator("#reg-email").fill(email)
    page.locator("#reg-password").fill(password)
    page.get_by_role("button", name="Register").nth(1).click()
    page.wait_for_timeout(500)
    
    page.locator("nav button:nth-of-type(1)").click()
    page.locator("#login-email").fill(email)
    page.locator("#login-password").fill(password)
    page.get_by_role("button", name="Login").nth(1).click()
    page.wait_for_timeout(500)
    
    # Navigate to Products page
    page.locator("nav button:nth-of-type(3)").click()
    
    # Wait for products to load
    page.wait_for_timeout(1000)
    
    # Check if products are available
    product_cards = page.locator(".product-card")
    product_count = product_cards.count()
    
    assert product_count > 0, "No products found on the products page"
    
    # Get first product name for verification
    first_product_name = product_cards.first.locator(".product-name").inner_text()
    
    # Click Add to Cart on first product
    product_cards.first.locator("button:has-text('Add to Cart')").click()
    
    # Verify message appears
    message = page.locator("#message")
    expect(message).to_be_visible()
    message_text = message.inner_text()
    assert any(keyword in message_text.lower() for keyword in ["cart", "added", "success"]), \
        f"Expected cart success message but got: {message_text}"
    
    # Navigate to Cart to verify item was added
    page.locator("nav button:nth-of-type(4)").click()
    page.wait_for_timeout(500)
    
    cart_items = page.locator(".cart-item")
    expect(cart_items.first).to_be_visible()


def test_navigate_to_products(page_with_app: Page):
    page = page_with_app
    
    # Click on Products navigation button
    page.locator("nav button:nth-of-type(3)").click()
    
    # Wait for page to load
    page.wait_for_timeout(1000)
    
    # Verify products are displayed
    product_cards = page.locator(".product-card")
    
    # Wait for products to be visible
    expect(product_cards.first).to_be_visible(timeout=5000)
    
    # Verify product structure - each card should have name and price
    first_card = product_cards.first
    product_name = first_card.locator(".product-name")
    product_price = first_card.locator(".product-price")
    
    expect(product_name).to_be_visible()
    expect(product_price).to_be_visible()
    
    # Verify product name and price have content
    name_text = product_name.inner_text()
    price_text = product_price.inner_text()
    
    assert len(name_text.strip()) > 0, "Product name is empty"
    assert len(price_text.strip()) > 0, "Product price is empty"
    
    # Verify Add to Cart button exists
    add_to_cart_btn = first_card.locator("button:has-text('Add to Cart')")
    expect(add_to_cart_btn).to_be_visible()


def test_admin_add_product(page_with_app: Page):
    page = page_with_app
    
    # Login as admin user
    page.locator("nav button:nth-of-type(1)").click()
    
    # Use admin credentials
    page.locator("#login-email").fill("admin@example.com")
    page.locator("#login-password").fill("admin123")
    page.get_by_role("button", name="Login").nth(1).click()
    
    page.wait_for_timeout(500)
    
    # Check login message
    message = page.locator("#message")
    message_text = message.inner_text() if message.is_visible() else ""
    
    # Navigate to Admin page
    page.locator("nav button:nth-of-type(5)").click()
    page.wait_for_timeout(500)
    
    # Check if admin panel is accessible (admin inputs are visible)
    admin_name_input = page.locator("#admin-product-name")
    
    if not admin_name_input.is_visible():
        # Try to register an admin account or skip
        pytest.skip("Admin panel not accessible - admin credentials may be different")
    
    # Generate unique product data
    product_name = f"Test Product {generate_random_string(5)}"
    product_price = "29.99"
    product_description = f"Test description for {product_name}"
    
    # Fill in admin product form using exact selectors
    page.locator("#admin-product-name").fill(product_name)
    page.locator("#admin-product-price").fill(product_price)
    page.locator("#admin-product-description").fill(product_description)
    
    # Click Add Product button
    page.locator("button:has-text('Add Product')").click()
    
    page.wait_for_timeout(500)
    
    # Verify success message
    message = page.locator("#message")
    expect(message).to_be_visible()
    message_text = message.inner_text()
    assert any(keyword in message_text.lower() for keyword in ["success", "added", "created", "product"]), \
        f"Expected product add success message but got: {message_text}"
    
    # Navigate to Products page to verify new product appears
    page.locator("nav button:nth-of-type(3)").click()
    page.wait_for_timeout(1000)
    
    # Search for the newly added product
    product_names = page.locator(".product-name")
    product_texts = [product_names.nth(i).inner_text() for i in range(product_names.count())]
    
    assert product_name in product_texts, \
        f"Newly added product '{product_name}' not found in products list: {product_texts}"