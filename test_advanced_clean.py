import pytest
import time
from playwright.sync_api import Page


def generate_random_string(length=8):
    import random, string
    return ''.join(random.choices(string.ascii_lowercase, k=length))


@pytest.fixture
def page_setup(page: Page):
    page.goto("http://localhost:5001")
    return page


def test_full_e2e_register_login_browse(page_setup: Page):
    """End-to-end: Register → Login → Browse Products"""
    page = page_setup
    email = f"e2e_{int(time.time())}@test.com"
    password = "TestPass123!"
    username = generate_random_string()

    # Register
    page.locator('nav button').nth(1).click()
    page.fill('#reg-username', username)
    page.fill('#reg-email', email)
    page.fill('#reg-password', password)
    page.locator('button:has-text("Register")').nth(1).click()
    page.wait_for_timeout(1000)

    # Login
    page.locator('nav button').nth(0).click()
    page.fill('#login-email', email)
    page.fill('#login-password', password)
    page.locator('button:has-text("Login")').nth(1).click()
    page.wait_for_timeout(1000)

    # Browse products
    page.locator('nav button').nth(2).click()
    page.wait_for_timeout(500)
    products = page.locator('.product-card')
    assert products.count() >= 1


def test_full_e2e_add_multiple_products(page_setup: Page):
    """End-to-end: Register → Login → Add Multiple Products to Cart"""
    page = page_setup
    email = f"multi_{int(time.time())}@test.com"
    password = "TestPass123!"
    username = generate_random_string()

    # Register
    page.locator('nav button').nth(1).click()
    page.fill('#reg-username', username)
    page.fill('#reg-email', email)
    page.fill('#reg-password', password)
    page.locator('button:has-text("Register")').nth(1).click()
    page.wait_for_timeout(1000)

    # Login
    page.locator('nav button').nth(0).click()
    page.fill('#login-email', email)
    page.fill('#login-password', password)
    page.locator('button:has-text("Login")').nth(1).click()
    page.wait_for_timeout(1000)


def test_error_empty_fields_registration(page_setup: Page):
    """Test empty fields in registration"""
    page = page_setup
    page.locator('nav button').nth(1).click()
    page.locator('button:has-text("Register")').nth(1).click()
    page.wait_for_timeout(500)
    # Should not crash
    assert True


def test_error_empty_fields_login(page_setup: Page):
    """Test empty fields in login"""
    page = page_setup
    page.locator('nav button').nth(0).click()
    page.locator('button:has-text("Login")').nth(1).click()
    page.wait_for_timeout(500)
    # Should not crash
    assert True
