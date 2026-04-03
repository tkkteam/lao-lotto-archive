from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime, timedelta

# Lao lottery results URL pattern (from sanook.com)
# Example: http://news.sanook.com/lotto/check/13022569/ (for 13 Feb 2026)
metaurl = "http://news.sanook.com/lotto/check/{:02d}{:02d}{}/"

'''
# Generate links for Lao lottery draws (Monday, Wednesday, Friday)
def generate_lao_lottery_links(start_date, end_date):
    """Generate Lao lottery drawing dates between start_date and end_date
    Lao lottery draws on Monday, Wednesday, Friday at 20:30"""
    links = []
    current = start_date
    while current <= end_date:
        # Monday=0, Wednesday=2, Friday=4
        if current.weekday() in [0, 2, 4]:
            day = current.day
            month = current.month
            year = current.year + 543  # Convert to Buddhist Era for URL
            links.append(metaurl.format(day, month, year))
        current += timedelta(days=1)
    return links

links = generate_lao_lottery_links(
    datetime(2024, 1, 1),  # Start date
    datetime(2026, 12, 31)  # End date
)
'''

# Manual list of links to scrape (update with actual Lao lottery dates)
links = [
    "http://news.sanook.com/lotto/check/13022569/",  # 13 Feb 2026 (Friday)
    "http://news.sanook.com/lotto/check/11022569/",  # 11 Feb 2026 (Wednesday)
    "http://news.sanook.com/lotto/check/09022569/",  # 9 Feb 2026 (Monday)
    # Add more links as needed
]

for link in links:
    print("Scraping numbers from link {}".format(link))
    try:
        pagename = link.split('/')[-2]
        # Convert from BE year back to CE year for filename
        # Format: DDMMYYYY (BE) -> YYYY-MM-DD (CE)
        day = int(pagename[0:2])
        month = int(pagename[2:4])
        year = int(pagename[4:8]) - 543  # Convert BE to CE
        pagename = '{:04d}-{:02d}-{:02d}'.format(year, month, day)
        
        page = urlopen(link).read()
        soup = BeautifulSoup(page, "html.parser")
        
        # Lao lottery structure from Sanook.com
        # The page shows: 6 digits, 5 digits, 4 digits, 3 digits, 2 digits
        numbers = [num.string for num in soup.find_all(class_="lotto__number")]
        
        # Adjust based on actual Sanook Lao lottery page structure
        # Typically: [6-digit, 5-digit, 4-digit, 3-digit, 2-digit]
        six = numbers[0]
        five = numbers[1]
        four = numbers[2]
        three = numbers[3]
        two = numbers[4]

        outfile = open("lottonumbers/" + pagename + ".txt", 'w')
        outfile.write(link + '\n')
        outfile.write("SIX " + str(six) + '\n')
        outfile.write("FIVE " + str(five) + '\n')
        outfile.write("FOUR " + str(four) + '\n')
        outfile.write("THREE " + str(three) + '\n')
        outfile.write("TWO " + str(two) + '\n')
        outfile.close()
        
        print("Scraped data from {} into lottonumbers/{}.txt".format(link, pagename))
    except Exception as e:
        print("WARNING: " + link + " cannot be scraped with exception " + str(e) + ". Skipping.")
        continue
