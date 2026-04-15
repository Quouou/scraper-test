from flask import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

import boto3
import time


chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")         
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

s3 = boto3.client('s3')

try:
    master_quotes = []
    driver.get("http://quotes.toscrape.com/search.aspx")


    author_names = []

    select_author = Select(driver.find_element(By.ID, "author"))
    # print(f"Amount of authors: {len(select_author.options) - 1}")
    for option in select_author.options:
        if option.text != "----------":
            author_names.append(option.text)
    # print('Finished collecting author names')

    for author in author_names:
        selectAuthor = Select(driver.find_element(By.ID, "author"))
        selectAuthor.select_by_visible_text(author)

        time.sleep(1)

        tags_dropdown = Select(driver.find_element(By.ID, "tag"))
        currentAuthorTags = []
        for tag in tags_dropdown.options:
            if tag.text != "----------":
                currentAuthorTags.append(tag.text)
        # print(f"Finished collecting tags for author: {author} - Tags found: {currentAuthorTags}")

        for tag in currentAuthorTags:
            tagsDropDown = Select(driver.find_element(By.ID, "tag"))
            tagsDropDown.select_by_visible_text(tag)

    
            time.sleep(1)

            submit = driver.find_element(By.NAME, "submit_button")
            submit.click()
            time.sleep(1)

            content = driver.find_elements(By.CLASS_NAME, "quote")
            for q in content:
                quote_text = q.find_element(By.CLASS_NAME, "content").text
                isDuplicate = False

                for saved_quote in master_quotes:
                    if saved_quote["quote"] == quote_text:
                        saved_quote["tag"].append(tag)
                        isDuplicate = True
                        break
                
                if not isDuplicate:
                    master_quotes.append({
                            "author": author,
                            "tag": [tag],
                            "quote": q.find_element(By.CLASS_NAME, "content").text
                        
                    })
        # print(f"Finished collecting quotes for author: {author}")

    s3.put_object(
        Bucket='scraper-output-bucket-chris-test',
        Key='quotes.json',
        Body=json.dumps(master_quotes)
    )
finally:
    driver.quit()