from playwright.sync_api import sync_playwright
import pytest
import time


@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


def test_register_success(browser):
    """Test successful registration with unique email"""
    page = browser.new_page()
    page.goto('http://localhost:5001')

    # Create unique email
    unique_email = f"testuser_{int(time.time())}@example.com"

    # Fill form
    page.fill('#reg-username', 'testuser')
    page.fill('#reg-email', unique_email)
    page.fill('#reg-password', 'password123')

    # Click register button
    page.click('button:has-text("Register")')

    # Wait for success message
    page.wait_for_selector('.success')
    success_message = page.text_content('#message')

    assert 'successfully' in success_message.lower()
    page.close()


def test_login_success(browser):
    """Test successful login"""
    page = browser.new_page()
    page.goto('http://localhost:5001')

    # Login with credentials from previous test
    page.fill('#login-email', 'test@example.com')
    page.fill('#login-password', 'password123')

    # Click login button
    page.click('button:has-text("Login")')

    # Wait for success message
    page.wait_for_selector('.success')
    success_message = page.text_content('#message')

    assert 'successful' in success_message.lower()
    page.close()


def test_login_invalid_credentials(browser):
    """Test login with invalid credentials"""
    page = browser.new_page()
    page.goto('http://localhost:5001')

    # Try login with wrong password
    page.fill('#login-email', 'test@example.com')
    page.fill('#login-password', 'wrongpassword')

    # Click login button
    page.click('button:has-text("Login")')

    # Wait for error message
    page.wait_for_selector('.error')
    error_message = page.text_content('#message')

    assert 'invalid' in error_message.lower() or 'error' in error_message.lower()
    page.close()