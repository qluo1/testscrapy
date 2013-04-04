from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Remote("http://localhost:4444",{}) # Get local session of firefox
browser.get("http://www.google.com") # Load page
assert "Google" in browser.title
elem = browser.find_element_by_name("q") # Find the query box
elem.send_keys("seleniumhq" + Keys.RETURN)
time.sleep(0.2) # Let the page load, will be added to the API
browser.get_screenshot_as_file("dump.png")
try:
    browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
except NoSuchElementException:
    assert 0, "can't find seleniumhq"
browser.close()