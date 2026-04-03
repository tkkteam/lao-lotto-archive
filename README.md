# lao-lotto-archive
Archive of winning Lao lottery numbers. All data are sourced from official Lao lottery websites, sanook.com, and other sources.

## File structure
Each file in `lottonumbers` directory consists of winning numbers from each lotto drawing day, shown in a file name. The first line is a URL of website as a source for winning numbers data on the corresponding day. One string precedes each line from the second line onwards, which labels other numbers on the line to each corresponding prize as follows:

* `SIX`: Six Digit Prize (1st Prize), 1 number
* `FIVE`: Five Digit Prize (2nd Prize), 1 number
* `FOUR`: Four Digit Prize (3rd Prize), 1 number
* `THREE`: Three Digit Prize, 1 number
* `TWO`: Two Digit Prize, 1 number

## `lottoscrape.py` and `lottoscrape-sanook.py`
This repo also contains two python scripts which are used to scrape all data from lottery checking pages at various Lao lottery websites, and put them in a nice format under the directory `lottonumbers`. `lottoscrape.py` is tailored for official Lao lottery websites, while `lottoscrape-sanook.py` is for web page format seen in sanook.com. You will need Python 3 and [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) in order to run the scripts.

## Archive in other formats
* pandas DataFrame containing winning numbers can be obtained via `lottodataframe.py`. To obtain the DataFrame:
    ```python
    import lottodataframe
    lottodataframe.get_lotto_df()
    ```
    *Winning numbers in this DataFrame will include six digit, five digit, four digit, three digit, and two digit winning numbers.*
* If you would like to provide code for other formats, you may submit a pull request with provided code. Please keep in mind that the code must be able to generate the latest winning numbers according to the archive.

## Some information about Lao lottery
Lao Lottery is operated by the Ministry of Finance of Lao PDR (Lottery Development Enterprise). The lottery draws take place three times per week on Monday, Wednesday, and Friday at 20:30 (8:30 PM) local time, broadcast live on Lao National Television Channel 1.

Each Lao lottery ticket contains six digits. The prize structure is based on matching the last digits of the winning number, with prizes awarded as follows:

* **Six Digit Prize (1st Prize)** - Match all 6 digits in exact order
* **Five Digit Prize (2nd Prize)** - Match the last 5 digits in exact order
* **Four Digit Prize (3rd Prize)** - Match the last 4 digits in exact order
* **Three Digit Prize** - Match the last 3 digits in exact order
* **Two Digit Prize** - Match the last 2 digits in exact order

The ticket price is 1,000 LAK (Lao Kip) per bet, and all purchases are made exclusively online through the official lottery system.

For more information, see https://today.line.me/th/v3/article/nX5yxjM

## Drawing Schedule
Lao Lottery draws occur on the following schedule:

* **Days:** Monday, Wednesday, and Friday every week
* **Time:** 20:30 (8:30 PM) Lao time (same as Thailand time)
* **Broadcast:** Live on Lao National Radio and Lao National Television Channel 1

The Lao lottery operates year-round without the special holiday rescheduling that affects Thai lottery.
