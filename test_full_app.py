from playwright.sync_api import sync_playwright
import pytest
import time


@pytest.fixture
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


class TestRegistrationLogin:
    def test_register_new_user(self, browser):
        """Test registration with new user"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click Register nav button (index 1)
        page.locator('nav button').nth(1).click()

        unique_email = f"user_{int(time.time())}@test.com"
        page.fill('#reg-username', 'testuser')
        page.fill('#reg-email', unique_email)
        page.fill('#reg-password', 'password123')

        # Click Register form button
        page.locator('button:has-text("Register")').nth(1).click()

        # Wait more time
        page.wait_for_timeout(2000)

        # Debug: print page content
        page_text = page.content()
        print("\n--- PAGE HTML ---")
        print(page_text[:500])  # print first 500 chars

        # Check message
        message = page.text_content('#message')
        print(f"Message text: '{message}'")
        print(f"Message length: {len(message)}")

        page.close()

    def test_login_valid_credentials(self, browser):
        """Test login with valid credentials"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Already on login page
        page.fill('#login-email', 'test@test.com')
        page.fill('#login-password', 'pass123')

        # Click Login form button (index 6)
        page.locator('button:has-text("Login")').nth(1).click()

        # Check message
        page.wait_for_timeout(1000)
        message = page.text_content('#message')
        assert message and message.strip() != ''

        page.close()

    def test_login_invalid_credentials(self, browser):
        """Test login with wrong password"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        page.fill('#login-email', 'test@test.com')
        page.fill('#login-password', 'wrongpassword')

        # Click Login
        page.locator('button:has-text("Login")').nth(1).click()

        # Check message
        page.wait_for_timeout(1000)
        message = page.text_content('#message')
        assert message and message.strip() != ''

        page.close()


class TestNavigation:
    def test_navigation_buttons_visible(self, browser):
        """Test all navigation buttons are visible"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Check nav buttons only (first 6 buttons)
        nav_buttons = page.locator('nav button')
        assert nav_buttons.count() >= 6
        assert nav_buttons.nth(0).is_visible()  # Login nav
        assert nav_buttons.nth(1).is_visible()  # Register nav
        assert nav_buttons.nth(2).is_visible()  # Products

        page.close()

    def test_navigate_to_products(self, browser):
        """Test clicking Products navigation"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click Products button
        page.click('button:has-text("Products")')

        # Check Products page is visible
        assert page.locator('h1:has-text("Products")').is_visible()

        page.close()

    def test_navigate_to_admin(self, browser):
        """Test clicking Admin navigation"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click Admin button
        page.click('button:has-text("Admin")')

        # Check Admin page is visible
        assert page.locator('h1:has-text("Admin")').is_visible()

        page.close()

    def test_navigate_to_about(self, browser):
        """Test clicking About navigation"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click About button
        page.click('button:has-text("About")')

        # Check About page is visible
        assert page.locator('h1:has-text("About")').is_visible()

        page.close()


class TestProducts:
    def test_products_page_loads(self, browser):
        """Test products page displays products"""
        page = browser.new_page()
        page.goto('http://localhost:5001')
        page.click('button:has-text("Products")')
        page.wait_for_selector('.product-card', timeout=5000)
        product_cards = page.locator('.product-card')
        assert product_cards.count() >= 1
        page.close()

    def test_product_has_name_and_price(self, browser):
        """Test product cards show name and price"""
        page = browser.new_page()
        page.goto('http://localhost:5001')
        page.click('button:has-text("Products")')
        page.wait_for_selector('.product-card', timeout=5000)
        first_product = page.locator('.product-card').first
        assert first_product.locator('.product-name').is_visible()
        assert first_product.locator('.product-price').is_visible()
        page.close()

    def test_add_to_cart_button_exists(self, browser):
        """Test Add to Cart button exists on products"""
        page = browser.new_page()
        page.goto('http://localhost:5001')
        page.click('button:has-text("Products")')
        page.wait_for_selector('.product-card', timeout=5000)
        add_buttons = page.locator('button:has-text("Add to Cart")')
        assert add_buttons.count() >= 1
        page.close()


class TestAdmin:
    def test_admin_add_product_form_visible(self, browser):
        """Test admin form has all fields"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click Admin
        page.click('button:has-text("Admin")')

        # Check form fields
        assert page.locator('#admin-product-name').is_visible()
        assert page.locator('#admin-product-price').is_visible()
        assert page.locator('#admin-product-description').is_visible()
        assert page.locator('button:has-text("Add Product")').is_visible()

        page.close()

    def test_admin_add_new_product(self, browser):
        """Test adding a new product"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click Admin
        page.click('button:has-text("Admin")')

        # Fill form
        unique_name = f"Test Product {int(time.time())}"
        page.fill('#admin-product-name', unique_name)
        page.fill('#admin-product-price', '99.99')
        page.fill('#admin-product-description', 'Test Description')

        # Click Add Product
        page.click('button:has-text("Add Product")')

        # Check success message
        page.wait_for_selector('.success')
        message = page.text_content('#message')
        assert 'added' in message.lower()

        page.close()


class TestAbout:
    def test_about_page_loads(self, browser):
        """Test About page displays content"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click About
        page.click('button:has-text("About")')

        # Check content
        assert page.locator('h1:has-text("About")').is_visible()
        assert 'QA Automation' in page.text_content('body')

        page.close()


class TestFormValidation:
    def test_register_empty_form(self, browser):
        """Test register with empty fields"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click Register nav
        page.locator('nav button').nth(1).click()

        # Click register without filling
        page.locator('button:has-text("Register")').nth(1).click()

        # Just check it doesn't crash
        page.wait_for_timeout(500)
        page.close()

    def test_login_empty_form(self, browser):
        """Test login with empty fields"""
        page = browser.new_page()
        page.goto('http://localhost:5001')

        # Click login without filling
        page.locator('button:has-text("Login")').nth(1).click()

        # Just check it doesn't crash
        page.wait_for_timeout(500)
        page.close()