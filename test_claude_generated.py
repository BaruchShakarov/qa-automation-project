import pytest
from playwright.sync_api import Page, expect, sync_playwright


BASE_URL = "http://localhost:5001"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def test_user():
    return {
        "username": "testuser_playwright",
        "email": "testuser_playwright@example.com",
        "password": "SecurePassword123!",
    }


class TestPageVisibility:
    def test_registration_page_loads(self, page: Page):
        page.goto(f"{BASE_URL}/register")
        expect(page).to_have_title(lambda title: len(title) > 0)
        page.wait_for_load_state("networkidle")
        assert page.url == f"{BASE_URL}/register" or "/register" in page.url

    def test_registration_form_elements_visible(self, page: Page):
        page.goto(f"{BASE_URL}/register")
        page.wait_for_load_state("networkidle")

        username_input = page.locator(
            "input[name='username'], input[id='username'], input[placeholder*='username' i]"
        ).first
        email_input = page.locator(
            "input[name='email'], input[id='email'], input[type='email']"
        ).first
        password_input = page.locator(
            "input[name='password'], input[id='password'], input[type='password']"
        ).first
        submit_button = page.locator(
            "button[type='submit'], input[type='submit']"
        ).first

        expect(username_input).to_be_visible()
        expect(email_input).to_be_visible()
        expect(password_input).to_be_visible()
        expect(submit_button).to_be_visible()

    def test_login_page_loads(self, page: Page):
        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")
        assert "/login" in page.url

    def test_login_form_elements_visible(self, page: Page):
        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")

        email_input = page.locator(
            "input[name='email'], input[id='email'], input[type='email']"
        ).first
        password_input = page.locator(
            "input[name='password'], input[id='password'], input[type='password']"
        ).first
        submit_button = page.locator(
            "button[type='submit'], input[type='submit']"
        ).first

        expect(email_input).to_be_visible()
        expect(password_input).to_be_visible()
        expect(submit_button).to_be_visible()

    def test_home_page_loads(self, page: Page):
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")
        assert page.url.startswith(BASE_URL)

    def test_navigation_links_present(self, page: Page):
        page.goto(BASE_URL)
        page.wait_for_load_state("networkidle")

        login_link = page.locator("a[href*='login']").first
        register_link = page.locator("a[href*='register']").first

        expect(login_link).to_be_visible()
        expect(register_link).to_be_visible()


class TestRegistration:
    def test_successful_registration(self, page: Page, test_user):
        page.goto(f"{BASE_URL}/register")
        page.wait_for_load_state("networkidle")

        username_input = page.locator(
            "input[name='username'], input[id='username'], input[placeholder*='username' i]"
        ).first
        email_input = page.locator(
            "input[name='email'], input[id='email'], input[type='email']"
        ).first
        password_input = page.locator(
            "input[name='password'], input[id='password'], input[type='password']"
        ).first
        submit_button = page.locator(
            "button[type='submit'], input[type='submit']"
        ).first

        username_input.fill(test_user["username"])
        email_input.fill(test_user["email"])
        password_input.fill(test_user["password"])
        submit_button.click()

        page.wait_for_load_state("networkidle")

        success_message = page.locator(
            ".success, .alert-success, .message.success, [class*='success'], .flash-success"
        ).first

        is_redirected_to_login = "/login" in page.url
        is_redirected_to_dashboard = (
            "/dashboard" in page.url or "/home" in page.url or page.url == BASE_URL + "/"
        )

        has_success_message = False
        try:
            success_message.wait_for(timeout=3000)
            has_success_message = success_message.is_visible()
        except Exception:
            pass

        assert (
            is_redirected_to_login
            or is_redirected_to_dashboard
            or has_success_message
        ), f"Registration did not succeed. Current URL: {page.url}"

    def test_registration_duplicate_email(self, page: Page, test_user):
        page.goto(f"{BASE_URL}/register")
        page.wait_for_load_state("networkidle")

        username_input = page.locator(
            "input[name='username'], input[id='username'], input[placeholder*='username' i]"
        ).first
        email_input = page.locator(
            "input[name='email'], input[id='email'], input[type='email']"
        ).first
        password_input = page.locator(
            "input[name='password'], input[id='password'], input[type='password']"
        ).first
        submit_button = page.locator(
            "button[type='submit'], input[type='submit']"
        ).first

        username_input.fill(test_user["username"] + "_dup")
        email_input.fill(test_user["email"])
        password_input.fill(test_user["password"])
        submit_button.click()

        page.wait_for_load_state("networkidle")

        error_message = page.locator(
            ".error, .alert-danger, .alert-error, .message.error, [class*='error'], .flash-error, .danger"
        ).first

        still_on_register = "/register" in page.url
        has_error = False
        try:
            error_message.wait_for(timeout=3000)
            has_error = error_message.is_visible()
        except Exception:
            pass

        assert still_on_register or has_error, (
            f"Expected error for duplicate registration. Current URL: {page.url}"
        )

    def test_registration_invalid_email_format(self, page: Page):
        page.goto(f"{BASE_URL}/register")
        page.wait_for_load_state("networkidle")

        username_input = page.locator(
            "input[name='username'], input[id='username'], input[placeholder*='username' i]"
        ).first
        email_input = page.locator(
            "input[name='email'], input[id='email'], input[type='email']"
        ).first
        password_input = page.locator(
            "input[name='password'], input[id='password'], input[type='password']"
        ).first
        submit_button = page.locator(
            "button[type='submit'], input[type='submit']"
        ).first

        username_input.fill("invaliduser")
        email_