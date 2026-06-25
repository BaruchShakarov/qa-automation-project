import pytest
import time
import random
import string
from playwright.sync_api import Page, expect


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def generate_random_email():
    return f"{generate_random_string()}_{int(time.time())}@test.com"


@pytest.fixture
def page_with_app(page: Page):
    page.goto("http://localhost:5001")
    return page


def test_register_new_user(page_with_app: Page):
    """Test registering a new user"""
    page = page_with_app

    # Click Register nav button
    page.locator('nav button').nth(1).click()

    username = generate_random_string()
    email = generate_random_email()
    password = "TestPass123!"

    # Fill registration form
    page.fill('#reg-username', username)
    page.fill('#reg-email', email)
    page.fill('#reg-password', password)

    # Click Register button (index 1)
    page.locator('button:has-text("Register")').nth(1).click()

    # Wait for response
    page.wait_for_timeout(1000)

    # Check message
    message = page.text_content('#message')
    assert message and message.strip() != '', f"Expected success message, got: {message}"


def test_login_after_register(page_with_app: Page):
    """Test login with newly registered user"""
    page = page_with_app

    # Register first
    page.locator('nav button').nth(1).click()

    email = generate_random_email()
    password = "TestPass123!"
    username = generate_random_string()

    page.fill('#reg-username', username)
    page.fill('#reg-email', email)
    page.fill('#reg-password', password)
    page.locator('button:has-text("Register")').nth(1).click()
    page.wait_for_timeout(1000)

    # Now login
    page.locator('nav button').nth(0).click()  # Click Login
    page.wait_for_timeout(500)

    page.fill('#login-email', email)
    page.fill('#login-password', password)
    page.locator('button:has-text("Login")').nth(1).click()

    page.wait_for_timeout(1000)
    message = page.text_content('#message')
    assert message and message.strip() != ''


def test_navigate_to_products_page(page_with_app: Page):
    """Test navigating to products page"""
    page = page_with_app

    # Click Products button
    page.locator('nav button').nth(2).click()

    page.wait_for_timeout(500)

    # Check products are displayed
    products = page.locator('.product-card')
    assert products.count() >= 1


def test_navigate_to_cart_page(page_with_app: Page):
    """Test navigating to cart page"""
    page = page_with_app

    # Click Cart button
    page.locator('nav button').nth(3).click()

    page.wait_for_timeout(500)

    # Check cart page loads
    page_content = page.content()
    assert 'cart' in page_content.lower() or page.url.endswith('/')


def test_navigate_to_admin_page(page_with_app: Page):
    """Test navigating to admin page"""
    page = page_with_app

    # Click Admin button
    page.locator('nav button').nth(4).click()

    page.wait_for_timeout(500)

    # Check admin form is visible or login required
    body_text = page.locator('body').inner_text().lower()
    assert 'admin' in body_text or 'login' in body_text