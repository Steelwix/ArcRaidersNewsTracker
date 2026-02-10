from playwright.sync_api import sync_playwright
import requests
import sys
import os


try:
    with open("webhook.txt", "r") as f:
        WEBHOOK_URL = f.read().strip()
except FileNotFoundError:
    print("Webhook file missing")
    sys.exit(1)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://arcraiders.com/fr/news", timeout=60000)

    page.wait_for_selector(".news-article-card_container__xsniv")

    cards = page.query_selector_all(".news-article-card_container__xsniv")


    lastArticle = cards[0]

    title_div = lastArticle.query_selector(".news-article-card_title__7LpPs")
    href = lastArticle.get_attribute("href")
    title = title_div.inner_text()

    if not title_div:
        print("Titre non trouvé")
    else:
        browser.close()
    
try:
    with open("article_count.txt", "r") as file:
        old_count = file.read()
except FileNotFoundError:
    old_count = ""


# Comparaison
if old_count == "" or old_count == len(cards):
    sys.exit()
    die()

with open("article_count.txt", "w") as file:
    file.write(str(len(cards)))

try:
    with open("last_article.txt", "r") as file:
        storedArticle = file.read()
except FileNotFoundError:
    storedArticle = ""

if storedArticle == "" or storedArticle == title:
    sys.exit()
    die()

with open("last_article.txt", "w") as file:
    file.write(title)


WEBHOOK_URL = "https://discord.com/api/webhooks/1470860272116830387/E1ZZDJB9dO5USxrdOdCYVBXHQZuA5pSoxUPtvEf3h3VJyFH-ZFm5QJDe1jkTpW5zWZlj"
payload = {
"content": "🚨 NEW ARC RAIDERS INFOS : "+ title + " https://arcraiders.com/fr" + href
}

requests.post(WEBHOOK_URL, json=payload)

