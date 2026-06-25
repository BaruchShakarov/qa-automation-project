from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://localhost:5001')

    # Print all buttons in nav
    nav_buttons = page.locator('nav button')
    print(f"Nav buttons count: {nav_buttons.count()}")
    for i in range(nav_buttons.count()):
        text = nav_buttons.nth(i).text_content()
        print(f"Button {i}: {text}")

    # Print all inputs
    inputs = page.locator('input')
    print(f"\nInputs count: {inputs.count()}")
    for i in range(inputs.count()):
        id_attr = inputs.nth(i).get_attribute('id')
        print(f"Input {i}: id={id_attr}")

    # Print all buttons in page
    all_buttons = page.locator('button')
    print(f"\nTotal buttons: {all_buttons.count()}")
    for i in range(all_buttons.count()):
        text = all_buttons.nth(i).text_content()
        print(f"Button {i}: {text}")

    browser.close()