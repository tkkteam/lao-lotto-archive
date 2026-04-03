from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
from datetime import datetime
import time

# Sanook Lao lottery URLs
ARCHIVE_URL = "https://www.sanook.com/news/archive/laolotto/"
BASE_URL = "https://www.sanook.com/news"

# User-Agent header to avoid being blocked
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def get_archive_links():
    """Get all Lao lottery links from the archive page"""
    try:
        req = Request(ARCHIVE_URL, headers=HEADERS)
        page = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        links = soup.find_all('a', href=True)
        laolotto_links = [a['href'] for a in links if a['href'].startswith('/news/laolotto/')]
        return list(set(laolotto_links))
    except Exception as e:
        print(f"WARNING: Cannot fetch archive page: {e}")
        return []


def get_statistics_links():
    """Get Lao lottery links from statistics pages for more historical data"""
    # Search for Sanook articles with historical Lao lottery data
    stats_urls = [
        "https://www.sanook.com/news/9680038/",  # Statistics page
    ]
    
    links = []
    for url in stats_urls:
        try:
            req = Request(url, headers=HEADERS)
            page = urlopen(req).read().decode('utf-8')
            soup = BeautifulSoup(page, 'html.parser')
            all_links = soup.find_all('a', href=True)
            for link in all_links:
                href = link['href']
                if '/news/laolotto/' in href or (href.startswith('/news/') and any(str(year) in href for year in range(2560, 2570))):
                    links.append(href)
        except Exception as e:
            print(f"WARNING: Cannot fetch statistics page {url}: {e}")
            continue
    
    return list(set(links))


def convert_be_to_ce(be_year):
    """Convert Buddhist Era year to Christian Era year"""
    return be_year - 543


def parse_date_from_url(url):
    """Extract date from URL like /news/laolotto/02042569/"""
    match = re.search(r'/(\d{2})(\d{2})(\d{4})/', url)
    if match:
        day = int(match.group(1))
        month = int(match.group(2))
        year_be = int(match.group(3))
        year_ce = convert_be_to_ce(year_be)
        return f"{year_ce:04d}-{month:02d}-{day:02d}"
    return None


def scrape_lao_lottery_page(url):
    """Scrape a single Lao lottery result page"""
    try:
        full_url = url if url.startswith('http') else f"https://www.sanook.com{url}"
        req = Request(full_url, headers=HEADERS)
        page = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(page, 'html.parser')
        
        # Try to find lottery numbers in the page
        # Format 1: 4 ตัว, 3 ตัว, 2 ตัว (newer format)
        four_match = re.search(r'เลข\s*4\s*ตัว\s*[:\s]\s*(\d{4})', page)
        three_match = re.search(r'เลข\s*3\s*ตัว\s*[:\s]\s*(\d{3})', page)
        two_match = re.search(r'เลข\s*2\s*ตัว\s*[:\s]\s*(\d{2})', page)
        
        # Format 2: 6 ตัว, 5 ตัว, 4 ตัว, 3 ตัว, 2 ตัว (older format with 6 digits)
        six_match = re.search(r'เลข\s*6\s*ตัว\s*[:\s]\s*(\d{6})', page)
        five_match = re.search(r'เลข\s*5\s*ตัว\s*[:\s]\s*(\d{5})', page)
        
        if four_match or six_match:
            result = {}
            if six_match:
                result['SIX'] = six_match.group(1)
            if five_match:
                result['FIVE'] = five_match.group(1)
            if four_match:
                result['FOUR'] = four_match.group(1)
            if three_match:
                result['THREE'] = three_match.group(1)
            if two_match:
                result['TWO'] = two_match.group(1)
            
            # Extract date from page
            date_match = re.search(r'งวดประจำวันที่\s*(\d+)\s*(\S+)\s*(\d+)', page)
            if date_match:
                day = int(date_match.group(1))
                month_thai = date_match.group(2)
                year_be = int(date_match.group(3))
                year_ce = convert_be_to_ce(year_be)
                
                # Thai month mapping
                thai_months = {
                    'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4,
                    'พฤษภาคม': 5, 'มิถุนายน': 6, 'กรกฎาคม': 7, 'สิงหาคม': 8,
                    'กันยายน': 9, 'ตุลาคม': 10, 'พฤศจิกายน': 11, 'ธันวาคม': 12
                }
                month = thai_months.get(month_thai, 1)
                
                result['date'] = f"{year_ce:04d}-{month:02d}-{day:02d}"
                return result
        
        return None
        
    except Exception as e:
        print(f"WARNING: Cannot scrape {url}: {e}")
        return None


def save_to_file(result, output_dir='lottonumbers'):
    """Save lottery result to file"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = result.get('date')
    if not date_str:
        return False
    
    filename = f"{output_dir}/{date_str}.txt"
    
    # Skip if file already exists
    if os.path.exists(filename):
        print(f"SKIP: {date_str} already exists")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        source_url = f"https://www.sanook.com/news/laolotto/{date_str.replace('-', '')[:2]}{date_str.replace('-', '')[2:4]}{int(date_str[:4]) + 543}/"
        f.write(f"{source_url}\n")
        
        if 'SIX' in result:
            f.write(f"SIX {result['SIX']}\n")
        if 'FIVE' in result:
            f.write(f"FIVE {result['FIVE']}\n")
        if 'FOUR' in result:
            f.write(f"FOUR {result['FOUR']}\n")
        if 'THREE' in result:
            f.write(f"THREE {result['THREE']}\n")
        if 'TWO' in result:
            f.write(f"TWO {result['TWO']}\n")
    
    print(f"SAVED: {filename}")
    return True


def main():
    """Main function to scrape Lao lottery data"""
    print("=" * 60)
    print("Lao Lottery Scraper - Sanook.com")
    print("=" * 60)
    
    # Get links from archive
    print("\n[1] Fetching archive page...")
    archive_links = get_archive_links()
    print(f"Found {len(archive_links)} links from archive")
    
    # Get links from statistics pages
    print("\n[2] Fetching statistics pages...")
    stats_links = get_statistics_links()
    print(f"Found {len(stats_links)} links from statistics")
    
    # Combine and deduplicate
    all_links = list(set(archive_links + stats_links))
    print(f"\n[3] Total unique links: {len(all_links)}")
    
    # Scrape each link
    print("\n[4] Scraping lottery results...")
    success_count = 0
    for i, link in enumerate(all_links, 1):
        print(f"\n[{i}/{len(all_links)}] Processing: {link}")
        result = scrape_lao_lottery_page(link)
        if result:
            if save_to_file(result):
                success_count += 1
        time.sleep(0.5)  # Be polite to the server
    
    print("\n" + "=" * 60)
    print(f"Done! Successfully scraped {success_count} lottery results")
    print("=" * 60)


if __name__ == "__main__":
    main()
