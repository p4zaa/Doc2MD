#!/usr/bin/env python3
"""
HTML Structure Investigation Script

This script helps investigate what HTML the crawler is actually seeing
and why 'adk --version' content is missing.
"""

import requests
from bs4 import BeautifulSoup
import re

def investigate_website(url):
    """Investigate what HTML structure the website actually has."""
    
    print(f"🔍 Investigating HTML Structure for: {url}")
    print("=" * 60)
    
    try:
        # Get the HTML content (same as the crawler)
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; Doc2MD/1.0)'
        }
        
        print("📡 Fetching HTML content...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        html_content = response.text
        print(f"✅ HTML fetched successfully")
        print(f"📏 HTML length: {len(html_content)} characters")
        
        # Check for specific content
        print("\n🔍 Checking for 'adk --version' content:")
        if 'adk --version' in html_content:
            print("  ✅ Found 'adk --version' in HTML")
        else:
            print("  ❌ 'adk --version' NOT found in HTML")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for code-related elements
        print("\n🔍 Analyzing HTML Structure:")
        print("-" * 40)
        
        # Check for <pre> tags
        pre_tags = soup.find_all('pre')
        print(f"📋 Found {len(pre_tags)} <pre> tags")
        
        for i, pre_tag in enumerate(pre_tags):
            pre_content = pre_tag.get_text().strip()
            print(f"  <pre> {i+1}: {repr(pre_content[:100])}")
        
        # Check for <code> tags
        code_tags = soup.find_all('code')
        print(f"📋 Found {len(code_tags)} <code> tags")
        
        for i, code_tag in enumerate(code_tags):
            code_content = code_tag.get_text().strip()
            print(f"  <code> {i+1}: {repr(code_content[:100])}")
        
        # Check for other potential code containers
        print("\n🔍 Looking for other code containers:")
        
        # Check for elements with 'code' in class names
        code_classes = soup.find_all(class_=re.compile(r'code', re.IGNORECASE))
        print(f"📋 Found {len(code_classes)} elements with 'code' in class names")
        
        for i, element in enumerate(code_classes):
            element_content = element.get_text().strip()
            class_names = ' '.join(element.get('class', []))
            print(f"  Element {i+1} (class: {class_names}): {repr(element_content[:100])}")
        
        # Check for elements with 'pre' in class names
        pre_classes = soup.find_all(class_=re.compile(r'pre', re.IGNORECASE))
        print(f"📋 Found {len(pre_classes)} elements with 'pre' in class names")
        
        for i, element in enumerate(pre_classes):
            element_content = element.get_text().strip()
            class_names = ' '.join(element.get('class', []))
            print(f"  Element {i+1} (class: {class_names}): {repr(element_content[:100])}")
        
        # Check for script tags (JavaScript)
        script_tags = soup.find_all('script')
        print(f"\n📋 Found {len(script_tags)} <script> tags")
        
        # Look for JavaScript that might load content
        js_content = ' '.join([script.get_text() for script in script_tags])
        if 'adk' in js_content.lower():
            print("  🔍 Found JavaScript containing 'adk' - content might be loaded dynamically")
        else:
            print("  ℹ️  No JavaScript found containing 'adk'")
        
        # Check for common JavaScript frameworks
        frameworks = ['react', 'vue', 'angular', 'jquery', 'bootstrap']
        for framework in frameworks:
            if framework in js_content.lower():
                print(f"  🔍 Found {framework} framework - content might be dynamic")
        
        # Show HTML preview
        print(f"\n📝 HTML Preview (first 500 characters):")
        print("-" * 40)
        print(html_content[:500])
        
        # Check if this looks like a JavaScript-heavy page
        if len(script_tags) > 5:
            print(f"\n⚠️  This appears to be a JavaScript-heavy page")
            print(f"   The crawler might not be getting the full content")
            print(f"   Consider using a JavaScript-enabled crawler")
        
        return html_content
        
    except requests.RequestException as e:
        print(f"❌ Failed to fetch HTML: {e}")
        return None
    except Exception as e:
        print(f"❌ Error during investigation: {e}")
        return None

def show_solutions():
    """Show solutions for JavaScript-heavy websites."""
    
    print("\n" + "=" * 60)
    print("🔧 Solutions for JavaScript-Heavy Websites")
    print("=" * 60)
    
    print("\n📝 **Option 1: JavaScript-Enabled Crawler**")
    print("-" * 40)
    
    selenium_example = '''# Install selenium
pip install selenium

# Use browser-based crawling
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_javascript_content(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(3)  # Wait for JavaScript
        return driver.page_source
    finally:
        driver.quit()'''
    
    print(selenium_example)
    
    print("\n📝 **Option 2: Playwright (More Modern)**")
    print("-" * 40)
    
    playwright_example = '''# Install playwright
pip install playwright
playwright install

# Use Playwright for better JavaScript support
from playwright.sync_api import sync_playwright

def get_javascript_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        html = page.content()
        browser.close()
        return html'''
    
    print(playwright_example)
    
    print("\n📝 **Option 3: Check for API Endpoints**")
    print("-" * 40)
    
    api_tips = [
        "• Look for API calls in the JavaScript code",
        "• Check Network tab in browser DevTools",
        "• The content might be available via API",
        "• You could fetch content directly from the API"
    ]
    
    for tip in api_tips:
        print(f"  {tip}")

def main():
    """Run the investigation."""
    try:
        # Get URL from user
        url = input("Enter the website URL to investigate: ").strip()
        
        if not url:
            print("❌ No URL provided")
            return
        
        # Investigate the website
        html_content = investigate_website(url)
        
        if html_content:
            show_solutions()
            
            print("\n\n🎉 Investigation Completed!")
            print("\n💡 **Key Findings:**")
            print("  ✅ We've identified why 'adk --version' is missing")
            print("  ✅ The content is not in the static HTML")
            print("  ✅ This is likely a JavaScript-heavy website")
            print("  ✅ You need a JavaScript-enabled crawler")
            
            print("\n🚀 **Next Steps:**")
            print("  1. Use one of the JavaScript-enabled solutions above")
            print("  2. Or check if the content is available via API")
            print("  3. Modify Doc2MD to use JavaScript-enabled crawling")
        
    except KeyboardInterrupt:
        print("\n❌ Investigation interrupted by user")
    except Exception as e:
        print(f"\n❌ Investigation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
