from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
        page.goto("http://localhost:5000/")
        page.click("a:has-text('Register')")
        username = f"e2e_user_{int(time.time())}"
        page.locator("div.max-w-md:has(h2:has-text('Register')) >> input[type='text']").fill(username)
        page.locator("div.max-w-md:has(h2:has-text('Register')) >> input[type='password']").fill("secret123")
        page.locator("div.max-w-md:has(h2:has-text('Register')) >> button[type='submit']").click()
        page.wait_for_selector("text=Registration successful.", timeout=5000)

        page.click("a:has-text('Login')")
        page.locator("div.max-w-md:has(h2:has-text('Login')) >> input[type='text']").fill(username)
        page.locator("div.max-w-md:has(h2:has-text('Login')) >> input[type='password']").fill("secret123")
        page.locator("div.max-w-md:has(h2:has-text('Login')) >> button[type='submit']").click()

        page.wait_for_selector(f"text=Hello, {username}", timeout=5000)

        page.wait_for_selector("text='No pending goals. Great job!'", timeout=5000)

        print("Emitting join explicitly via console just in case")
        page.evaluate("""() => {
            import('/src/store.ts').then(s => {
               s.getSocket().emit('join', { user_id: s.user.user_id })
            })
        }""")
        time.sleep(1)

        page.fill("input[placeholder='New daily goal...']", "E2E Test Goal")

        page.click("button:has-text('Add Goal')")

        # Give JS/WS a sec to run
        time.sleep(2)

        try:
            page.wait_for_selector("text=E2E Test Goal", timeout=5000)
            print("FOUND ADDED GOAL VIA WS")
        except:
            print("FAILED TO FIND ADDED GOAL VIA WS")

        # Complete goal
        try:
            page.click("li:has-text('E2E Test Goal') button:has-text('Complete')")
            time.sleep(2)
            page.wait_for_selector("text='No pending goals. Great job!'", timeout=5000)
            print("SUCCESSFULLY COMPLETED GOAL AND SAW IT VANISH")
        except Exception as e:
            print("Could not complete goal", e)
        browser.close()

run()
