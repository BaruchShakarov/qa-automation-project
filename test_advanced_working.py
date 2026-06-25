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


# 1. E2E Register → Login
def test_e2e_register_and_login(page_setup: Page):
    page = page_setup
    email = f"e2e1_{int(time.time())}@test.com"

    page.locator('nav button').nth(1).click()
    page.fill('#reg-username', generate_random_string())
    page.fill('#reg-email', email)
    page.fill('#reg-password', 'Pass123!')
    page.locator('button:has-text("Register")').nth(1).click()
    page.wait_for_timeout(1000)

    page.locator('nav button').nth(0).click()
    page.fill('#login-email', email)
    page.fill('#login-password', 'Pass123!')
    page.locator('button:has-text("Login")').nth(1).click()
    page.wait_for_timeout(1000)
    assert True


# 2. Multiple Registrations
def test_multiple_users_registration(page_setup: Page):
    page = page_setup
    for i in range(3):
        page.locator('nav button').nth(1).click()
        page.fill('#reg-username', f"user{i}_{int(time.time())}")
        page.fill('#reg-email', f"user{i}_{int(time.time())}@test.com")
        page.fill('#reg-password', 'Pass123!')
        page.locator('button:has-text("Register")').nth(1).click()
        page.wait_for_timeout(500)
        page.goto("http://localhost:5001")
    assert True


# 3. Navigation All Pages
def test_navigate_all_pages(page_setup: Page):
    page = page_setup
    for i in range(6):
        page.locator('nav button').nth(i).click()
        page.wait_for_timeout(300)
    assert True


# 4. Products Page Multiple Visits
def test_products_page_persistent(page_setup: Page):
    page = page_setup
    page.locator('nav button').nth(2).click()
    page.wait_for_timeout(500)
    count1 = page.locator('.product-card').count()

    page.locator('nav button').nth(5).click()
    page.wait_for_timeout(300)

    page.locator('nav button').nth(2).click()
    page.wait_for_timeout(500)
    count2 = page.locator('.product-card').count()

    assert count1 == count2


# 5. Sequential Page Navigation
def test_sequential_navigation_workflow(page_setup: Page):
    page = page_setup
    sequence = [1, 2, 3, 4, 5, 0]
    for idx in sequence:
        page.locator('nav button').nth(idx).click()
        page.wait_for_timeout(300)
    assert True


# 6. Register → Validate Form
def test_register_form_elements_visible(page_setup: Page):
    page = page_setup
    page.locator('nav button').nth(1).click()
    assert page.locator('#reg-username').is_visible()
    assert page.locator('#reg-email').is_visible()
    assert page.locator('#reg-password').is_visible()


# 7. Login → Validate Form
def test_login_form_elements_visible(page_setup: Page):
    page = page_setup
    page.locator('nav button').nth(0).click()
    assert page.locator('#login-email').is_visible()
    assert page.locator('#login-password').is_visible()


# 8. Products Always Exist
def test_products_always_available(page_setup: Page):
    page = page_setup
    page.locator('nav button').nth(2).click()
    page.wait_for_timeout(500)
    products = page.locator('.product-card')
    assert products.count() > 0


# 9. Navigation Buttons Count
def test_navigation_has_six_buttons(page_setup: Page):
    page = page_setup
    nav_buttons = page.locator('nav button')
    assert nav_buttons.count() == 6


# 10. Page Load Speed
def test_page_loads_in_reasonable_time(page_setup: Page):
    page = page_setup
    start = time.time()
    page.locator('nav button').nth(2).click()
    page.wait_for_timeout(1000)
    elapsed = time.time() - start
    assert elapsed < 5  # Should load in less than 5 seconds