from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import os
import time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

THAI_MONTHS = {
    'มกราคม': 1, 'กุมภาพันธ์': 2, 'มีนาคม': 3, 'เมษายน': 4,
    'พฤษภาคม': 5, 'มิถุนายน': 6, 'กรกฎาคม': 7, 'สิงหาคม': 8,
    'กันยายน': 9, 'ตุลาคม': 10, 'พฤศจิกายน': 11, 'ธันวาคม': 12
}

def convert_be_to_ce(be_year):
    return be_year - 543

def scrape_lao_lottery(url):
    """Scrape Lao lottery from Sanook laolotto page"""
    try:
        full_url = url if url.startswith('http') else f"https://www.sanook.com{url}"
        
        # Extract date from URL first (more reliable)
        # URL format: /news/laolotto/DDMMYYYY/
        url_date_match = re.search(r'/laolotto/(\d{2})(\d{2})(\d{4})/', full_url)
        if url_date_match:
            day = int(url_date_match.group(1))
            month = int(url_date_match.group(2))
            year_be = int(url_date_match.group(3))
            year_ce = convert_be_to_ce(year_be)
            expected_date_str = f"{year_ce:04d}-{month:02d}-{day:02d}"
        
        req = Request(full_url, headers=HEADERS)
        html = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get full text
        text = soup.get_text()
        
        # Extract lottery numbers using patterns
        # Format: "เลขท้าย X ตัวNNNN" or "เลข X ตัว : NNNN"
        four_match = re.search(r'เลขท้าย\s*4\s*ตัว\s*[:\s]*(\d{4})', text)
        three_match = re.search(r'เลขท้าย\s*3\s*ตัว\s*[:\s]*(\d{3})', text)
        two_match = re.search(r'เลขท้าย\s*2\s*ตัว\s*[:\s]*(\d{2})', text)
        
        # Also try alternative format with 6 digits
        six_match = re.search(r'เลข\s*6\s*ตัว\s*[:\s]*(\d{6})', text)
        five_match = re.search(r'เลข\s*5\s*ตัว\s*[:\s]*(\d{5})', text)
        
        if not (four_match or six_match):
            print(f"  WARNING: No lottery numbers found")
            return None
        
        result = {'date': expected_date_str}
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
        
        return result
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

def save_result(result, output_dir='lottonumbers'):
    os.makedirs(output_dir, exist_ok=True)
    date_str = result.get('date')
    if not date_str:
        return False
    
    filename = os.path.join(output_dir, f"{date_str}.txt")
    if os.path.exists(filename):
        print(f"  SKIP: {date_str} already exists")
        return False
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Source URL (reconstruct from date)
        year_be = int(date_str[:4]) + 543
        month = date_str[5:7]
        day = date_str[8:10]
        f.write(f"https://www.sanook.com/news/laolotto/{day}{month}{year_be}/\n")
        
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
    
    print(f"  SAVED: {date_str} - FOUR:{result.get('FOUR', 'N/A')} THREE:{result.get('THREE', 'N/A')} TWO:{result.get('TWO', 'N/A')}")
    return True

def get_archive_links():
    """Get Lao lottery links from archive page"""
    try:
        req = Request('https://www.sanook.com/news/archive/laolotto/', headers=HEADERS)
        html = urlopen(req).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/news/laolotto/')]
        return list(set(links))
    except Exception as e:
        print(f"ERROR fetching archive: {e}")
        return []

def main():
    print("=" * 70)
    print("Lao Lottery Scraper - Sanook.com")
    print("Source: https://www.sanook.com/news/archive/laolotto/")
    print("=" * 70)
    
    # Get links from archive
    print("\n[1] Getting archive links...")
    archive_links = get_archive_links()
    print(f"Found {len(archive_links)} links")
    
    # Scrape each link
    print("\n[2] Scraping lottery results...")
    success = 0
    for i, link in enumerate(archive_links, 1):
        print(f"\n[{i}/{len(archive_links)}] {link}")
        result = scrape_lao_lottery(link)
        if result:
            if save_result(result):
                success += 1
        time.sleep(0.5)
    
    print("\n" + "=" * 70)
    print(f"Done! Scraped {success} new results")
    print("=" * 70)

if __name__ == "__main__":
    main()
