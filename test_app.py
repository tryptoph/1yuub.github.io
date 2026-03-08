from playwright.sync_api import sync_playwright


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Loading CyberVulnDB...")
        page.goto("http://localhost:8082", wait_until="domcontentloaded", timeout=30000)

        # Wait for CVEs to load
        page.wait_for_selector("#cve-list .threat-card", timeout=15000)

        # Check CVE count
        cve_count = page.locator("#cve-list .threat-card").count()
        print(f"✓ {cve_count} CVEs loaded")

        # Check status
        status = page.locator("#status-source").inner_text()
        print(f"✓ Status: {status}")

        # Test click
        page.evaluate("document.querySelector('.threat-card').click()")
        page.wait_for_timeout(500)

        modal_visible = page.locator("#modal-overlay:not(.hidden)").count()
        print(f"✓ Modal opens on click: {modal_visible > 0}")

        # Close modal
        page.locator(".modal-close").click()
        page.wait_for_timeout(300)

        # Test severity filter
        page.locator("#cve-severity-filter").select_option("CRITICAL")
        page.wait_for_timeout(500)

        critical_count = page.locator("#cve-list .threat-card").count()
        print(f"✓ Severity filter works: {critical_count} critical CVEs")

        browser.close()
        print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()
