# 🛒 MAMUNIX E-Commerce Product Data Scraper

A fast, modular, and production-ready **Python web scraper** built with **Requests** and **BeautifulSoup** to extract structured e-commerce product catalogs across multiple pages—including product titles, active/discounted prices, direct product URLs, and high-resolution image links—into Excel-compatible CSV files.

---

## ✨ Key Features
* **Multi-Page Pagination:** Automatically crawls through configurable category pages (`MAX_PAGES`) with polite request delays (`DELAY_SECONDS`) to prevent server overload.
* **Persistent HTTP Sessions:** Uses `requests.Session()` for faster connection reuse across paginated requests.
* **Duplicate Filtering:** Tracks scraped product URLs in real time to guarantee clean, unique records.
* **Lazy-Load Image Resolution:** Detects both `data-src` and `src` attributes, ignores inline placeholders, and resolves relative paths into full clickable URLs.
* **Excel-Ready CSV Export:** Saves data with `utf-8-sig` encoding so currency symbols render cleanly in Microsoft Excel (`ecommerce_products_sample.csv` included as sample output).

---

## 🛠️ Tech Stack
* **Language:** Python 3.14+
* **HTTP Requests:** `requests`
* **HTML Parsing:** `beautifulsoup4` (`bs4`)
* **Data Export & Utilities:** Built-in `csv`, `os`, `time`, & `urllib.parse` modules

---

## 📂 Repository Files
* `ecommerce_scraper.py` — Modular multi-page Python scraping script.
* `ecommerce_products_sample.csv` — Sample structured dataset demonstrating multi-page product extraction.

---

## 🚀 How to Run Locally

1. **Install required libraries:**
   ```bash
   pip install requests beautifulsoup4
   ```

2. **Run the scraper:**
   ```bash
   python ecommerce_scraper.py
   ```

---

## 👨‍💻 Developed By
**Mamun** — Lead Architect, **MAMUNIX Studios**  
*Specializing in Web Scraping, B2B Lead Generation, and Workflow Automation.*

