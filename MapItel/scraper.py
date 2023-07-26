from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

# with open("config.json", "r") as f:
#     config = json.load(f)

TEXT_LIMITATION = 3000


def get_web_content(url):
    """_summary_

    Args:
        url (string): The url with event contents

    Returns:
        list: A list of webpage contents may contains the event informaitons. The content is seperated with the limitation of text lenght.
    """
    # Set up the driver (make sure you have installed the proper driver for your browser)
    options = Options()
    # options.headless = True
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    # initializing webdriver for Chrome with our options
    driver = webdriver.Chrome(options=options)
    # Load the webpage
    driver.get(url)

    # Wait for content to appear using the explicit wait
    wait = WebDriverWait(driver, 10)  # 10 seconds timeout
    content = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Scrape all of the contents on the page
    html = driver.page_source
    # print(html)

    # Close the driver
    driver.quit()

    # Assume the HTML document is stored in a variable called 'html_doc'
    soup = BeautifulSoup(html, "html.parser")

    # Find all paragraphs using the 'p' tag
    paragraphs = soup.find_all("p")

    # Print out the text of each paragraph
    ls_text = []
    text = ""
    for p in paragraphs:
        p_text = p.get_text()
        if len(text) + len(p_text) >= TEXT_LIMITATION:
            ls_text.append(text)
            text = p_text
        else:
            text += p_text
    if len(ls_text) == 0:
        ls_text.append(text)
    elif ls_text[-1] != text:
        ls_text.append(text)
    return ls_text
