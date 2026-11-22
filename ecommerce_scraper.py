# -*- coding: utf-8 -*-
"""
MAMUNIX E-Commerce Product Scraper
-----------------------------------
Scrapes product names, prices, old prices, image URLs and product links
from an e-commerce category page and saves them to a CSV file.

Usage:
    pip install -r requirements.txt
    python scraper.py

Note: For educational purposes only. Please respect the target website's
terms of service and robots.txt.
"""

import csv
import os 
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

# ============================================================
# Configuration (easy to customize)
# ============================================================

# Category page to scrape (use a category URL, not the homepage)
BASE_URL = "https://www.startech.com.bd/laptop-notebook/laptop"

# Maximum number of pages to scrape
MAX_PAGES = 3

# Delay between page requests in seconds (reduces load on the server)
DELAY_SECONDS = 1

# Name of the output CSV file
OUTPUT_FILE = "ecommerce_products_sample.csv"

# Browser-like User-Agent header to mimic standard web traffic
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


def fetch_page(session, url, page):
    """Fetch one page and return a BeautifulSoup object.
    Returns None if the request fails."""

    try:
        # The page number is sent as a query parameter, e.g. ?page=2
        response = session.get(url, params={"page": page}, headers=HEADERS, timeout=15)
        # Raise an exception for HTTP errors such as 404 or 500
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch page {page} -> {e}")
        return None

    # Make sure special characters and currency symbols are decoded correctly
    response.encoding = "utf-8"
    print(f"Page {page} | Status Code: {response.status_code}")

    return BeautifulSoup(response.text, "html.parser")


def parse_product(item, base_url):
    """Extract product details from a single product card.
    Returns None if the product name cannot be found."""

    # ---------- Product name ----------
    name_tag = item.select_one(".p-item-name")
    if not name_tag:
        return None
    name = name_tag.get_text(strip=True)

    # ---------- Product link ----------
    # name_tag may itself be an <a> tag, or may contain one - handle both cases
    a_tag = name_tag if name_tag.name == "a" else name_tag.find("a")
    if a_tag and a_tag.has_attr("href"):
        product_link = urljoin(base_url, a_tag["href"])
    else:
        product_link = "No Link"

    # ---------- Current price ----------
    price_tag = (
        item.select_one(".price-new")
        or item.select_one(".price")
        or item.select_one(".p-item-price")
    )
    price = price_tag.get_text(strip=True) if price_tag else "No Price"

    # ---------- Old price (only present when discounted) ----------
    old_price_tag = item.select_one(".price-old")
    old_price = old_price_tag.get_text(strip=True) if old_price_tag else ""

    # ---------- Image URL (handles lazy-loaded images) ----------
    img_tag = item.select_one(".p-item-img img") or item.find("img")
    image_url = "No Image"
    if img_tag:
        raw_src = img_tag.get("data-src") or img_tag.get("src")
        # Skip inline placeholder images that start with "data:"
        if raw_src and not raw_src.startswith("data:"):
            image_url = urljoin(base_url, raw_src)

    return [name, price, old_price, image_url, product_link]


def save_to_csv(data):
    """Save the scraped data to a CSV file and return the file path."""

    # Save the CSV in the same directory as this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, OUTPUT_FILE)

    # utf-8-sig ensures currency symbols display correctly in Excel
    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        # Header row
        writer.writerow(["Product Name", "Price", "Old Price", "Image URL", "Product Link"])
        # Product rows
        writer.writerows(data)

    return csv_file


def scrape_ecommerce_products():
    """Main function: loop through pages, collect products and save to CSV."""

    print("--- MAMUNIX E-COMMERCE PRODUCT SCRAPER (WITH IMAGES) ---")
    print(f"Target URL: {BASE_URL}")

    scraped_data = []   # Collected product rows
    seen_links = set()  # Used to detect duplicate products

    # A Session reuses the connection, which makes repeated requests faster
    with requests.Session() as session:

        for page in range(1, MAX_PAGES + 1):
            soup = fetch_page(session, BASE_URL, page)

            # Stop if the page could not be fetched
            if soup is None:
                break

            # Select all product cards on the page
            products = soup.select("div.p-item")
            print(f"Page {page}: found {len(products)} product cards")

            # No products means we reached the last page or the CSS selectors changed
            if not products:
                if page == 1:
                    print("No products found. Please inspect the page structure for updated CSS selectors.")
                break

            for item in products:
                row = parse_product(item, BASE_URL)
                if row is None:
                    continue

                # Skip products that were already collected
                product_link = row[4]
                if product_link != "No Link":
                    if product_link in seen_links:
                        continue
                    seen_links.add(product_link)

                scraped_data.append(row)
                print(f"Scraped: {row[0][:40]} | Price: {row[1]}")

            # Short pause before requesting the next page
            time.sleep(DELAY_SECONDS)

    # Do not create an empty file if nothing was scraped
    if not scraped_data:
        print("No data to save.")
        return

    csv_file = save_to_csv(scraped_data)
    print(f"\n--- SUCCESS: {len(scraped_data)} items saved to {csv_file} ---")


# Run the scraper only when this file is executed directly
if __name__ == "__main__":
    scrape_ecommerce_products()