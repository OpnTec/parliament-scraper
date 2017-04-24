# parliament-scaper

Public Data Scraper for Parliament Data for the EU and other Parliaments

## Ruby Based Crawler Setup
1. Install git (if not present already)
2. Clone project using `git clone https://github.com/fossasia/parliament-scaper.git`
3. Install Ruby (version >= 2.1) and Bundler
4. Run `bundle install` to install the required gems
5. Run the script using `ruby eu_scraper.rb` or `./eu_scraper.rb`
6. Find the scraped questions in the docs/ folder

### Technologies Used in Ruby crawler:
1. Ruby - The Language
2. Nokogiri - For HTML Parsing

## Scala-based Asynchronous crawler Setup
1. Install sbt, git and latest version of scala(sbt will do the update for you)
2. ```git clone https://github.com/DengYiping/parliament-scaper.git```
3. ```sbt run```
4. sbt will first automatically download the necessary dependencies, and it will run the script.

### Technologies Used in Scala crawler:
1. Scala: a functional programming language on JVM
2. Akka: a effective framework for asynchronous, non-blocking and event-driven programming in Scala
3. Spray-client: a light-weighted HTTP client based on Akka Actor model.

## Python Based Crawler Setup
1. Install the requirements for this crawler `pip install -r requirements.txt`
2. Run `$ python eu_scraper.py`

### Technologies Used in Python Crawler:
1. Requests library
2. lxml library for DOM traversal

## Python-async parser setup

 1. Create a virtual environment inside `python-async` folder with
    `virtualenv --python=python3.4 venv`
 2. Activate you virtual environment with `source venv/bin/activate`
 3. Install all appropriate requirements with `pip install -r
    requirements.txt`
 4. Run the parser with `$ python parser.py`

**Changing the parser behavior**

 - Change `YEARS_TO_PARSE `  in order to parse data from different years
 - Change `FOLDER_TO_DOWNLOAD` in order to change the name of the folder to download the data into.

### Technologies Used in Python-async parser:
1. Requests + requests-futures for async requests
2. threading for async downloading
3. beautifulsoup4 for DOM parsing
4. tqdm for progress bar

## Python-Based Scraper (pol's scraper)
This scraper uses the BeautifulSoup package to parse and extract data from parliament's site. The script can also calculate how many pages it has to download based on the number of questions to be scraped.

1. Install the requirements `pip install -r requirements.txt`
2. Run `$ python scraper.py`


## Scrape it all - Generic Scraper(pol's scraper 2)
This scraper uses the BeautifulSoup package to parse and extract data from parliament's site. The script can also calculate how many pages it has to download based on the number of docs to be scraped.

Generic Scraper - All years, All languages. Scrapes entire database.

1. Install the requirements `pip install -r requirements.txt`
2. Run `$ python scrape_it_all.py`
