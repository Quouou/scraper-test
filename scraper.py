from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import time

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

try:
    master_quotes = []
    driver.get("http://quotes.toscrape.com/search.aspx")


    author_names = ['Albert Einstein']

    select_author = Select(driver.find_element(By.ID, "author"))
    print(f"Amount of authors: {len(select_author.options) - 1}")
    # for option in select_author.options:
    #     if option.text != "----------":
    #         author_names.append(option.text)
    # print('Finished collecting author names')

    for author in author_names:
        select_author = Select(driver.find_element(By.ID, "author"))
        select_author.select_by_visible_text(author)

        time.sleep(1)

        tags_dropdown = Select(driver.find_element(By.ID, "tag"))
        current_author_tags = []
        for tag in tags_dropdown.options:
            if tag.text != "----------":
                current_author_tags.append(tag.text)
        # print(f"Finished collecting tags for author: {author} - Tags found: {current_author_tags}")

        for tag in current_author_tags:
            tags_dropdown = Select(driver.find_element(By.ID, "tag"))
            tags_dropdown.select_by_visible_text(tag)

            time.sleep(1)

            submit = driver.find_element(By.NAME, "submit_button")
            submit.click()
            time.sleep(1)

            content = driver.find_elements(By.CLASS_NAME, "quote")
            for q in content:
                master_quotes.append({
                    "author": author,
                    "tag": tag,
                    "quote": q.find_element(By.CLASS_NAME, "content").text
                })
        print (f"Finished collecting quotes for author: {author} - All Quotes: {master_quotes}")
finally:
    driver.quit()