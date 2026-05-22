import os
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict

BASE_URL = "https://www.democrats.senate.gov"
LISTING_URL = "https://www.democrats.senate.gov/newsroom/trump-transcripts?pagenum_rs={}"

OUTPUT_DIR = "../transcripts"

# https://stackoverflow.com/questions/43440397/requests-using-beautiful-soup-gets-blocked
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}

# delimiter between title and transcript body
DELIMITER = "\n\n===== TRANSCRIPT BEGIN =====\n\n"
# 22 pages of transcripts on site
TOTAL_PAGES = 22


def sanitize_filename(name):
    """
    Remove invalid filename characters.
    """
    return re.sub(r'[<>:"/\\\\|?*]', "", name)


def extract_date_from_title(title):
    """
    Extract date from transcript title.

    Example:
    'TRANSCRIPT: President Trump..., 4.28.26'
    -> 04282026
    """
    match = re.search(r'(\d{1,2})\.(\d{1,2})\.(\d{2,4})', title)

    if not match:
        return None

    month, day, year = match.groups()

    month = month.zfill(2)
    day = day.zfill(2)

    # Convert 2-digit year to 4-digit
    if len(year) == 2:
        year = "20" + year

    return f"{month}{day}{year}"


def get_transcript_links(page_num):
    """
    Get all transcript links from a listing page.
    """
    url = LISTING_URL.format(page_num)

    print(f"[INFO] Fetching listing page {page_num}: {url}")

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    links = []

    for a_tag in soup.select("a.ArticleTitle"):
        href = a_tag.get("href")

        if href:
            full_url = urljoin(BASE_URL, href)
            links.append(full_url)

    print(f"[INFO] Found {len(links)} transcript links")

    return links


def scrape_transcript(url):
    """
    Scrape transcript title and body paragraphs.
    """
    print(f"[INFO] Scraping transcript: {url}")

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title_tag = soup.select_one(
        "div.ArticleBlock.Heading--press h1.Heading__title"
    )

    if not title_tag:
        print(f"[WARNING] No title found for {url}")
        return None

    title = title_tag.get_text(strip=True)

    # transcript body div class
    transcript_div = soup.select_one(
        "div.js-press-release.RawHTML.mb-5"
    )

    if not transcript_div:
        print(f"[WARNING] No transcript body found for {url}")
        return None

    paragraphs = []

    for p in transcript_div.find_all("p"):
        text = p.get_text(" ", strip=True)

        if text:
            paragraphs.append(text)

    body = "\n\n".join(paragraphs)

    return {
        "title": title,
        "body": body
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_links = []

    # get all links
    for page_num in range(1, TOTAL_PAGES + 1):
        try:
            links = get_transcript_links(page_num)
            all_links.extend(links)
            time.sleep(.5)

        except Exception as e:
            print(f"[ERROR] Failed page {page_num}: {e}")

    print(f"\n[INFO] Total transcript links collected: {len(all_links)}\n")

    # track multiple transcripts per date
    date_counts = defaultdict(int)

    for idx, link in enumerate(all_links, start=1):
        try:
            result = scrape_transcript(link)

            if result is None:
                continue

            title = result["title"]
            body = result["body"]

            date_str = extract_date_from_title(title)

            if date_str is None:
                print(f"[WARNING] Could not extract date from title: {title}")
                # fallback
                date_str = "UNKNOWNDATE"

            transcript_num = date_counts[date_str]
            date_counts[date_str] += 1

            filename = f"{date_str}-{transcript_num}.txt"
            filename = sanitize_filename(filename)

            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(title)
                f.write(DELIMITER)
                f.write(body)

            print(f"[SAVED] {filepath}")
            time.sleep(.5)

        except Exception as e:
            print(f"[ERROR] Failed transcript {link} \n\t{e}")

    print("\n\nDone.")


if __name__ == "__main__":
    main()