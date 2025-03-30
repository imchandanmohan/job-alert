from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Use your real Chrome profile path here
chrome_options = Options()
chrome_options.add_argument("user-data-dir=/tmp/LinkedInBotProfile")
chrome_options.add_argument("profile-directory=Default")
chrome_options.add_argument("--start-maximized")

# Correct way to pass the chromedriver path
service = Service(ChromeDriverManager().install())

# Now create the driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Your job search URL
url = "https://www.linkedin.com/jobs/search/?currentJobId=4148461667&distance=50&f_E=2%2C3&f_TPR=r3600&geoId=106233382&keywords=(flutter%20OR%20react%20OR%20%20mobile%20OR%20full-stack%20OR%20backend%20OR%20frontend)%20AND%20(enginner%20OR%20developer)&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"

driver.get(url)

time.sleep(60)  # So you can see it running
