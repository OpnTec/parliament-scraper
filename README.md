# parliament-scaper

Public Data Scraper for Parliament Data for the EU and other Parliaments

## Ruby Based Crawler Setup
1. Install git (if not present already)
2. Clone project using `git clone https://github.com/sampritipanda/simple_app.git`
3. Install Ruby (version >= 2.1) and Bundler
4. Run `bundle install` to install the required gems
5. Run the script using `ruby eu_scraper.rb` or `./eu_scraper.rb`
6. Find the scraped questions in the docs/ folder

### Technologies Used in Ruby crawler:
1. Ruby - The Language
2. Nokogiri - For HTML Parsing

##Scala-based Asynchronous crawler Setup
1. Install sbt, git and latest version of scala(sbt will do the update for you)
2. ```git clone https://github.com/DengYiping/parliament-scaper.git```
3. ```sbt run```
4. sbt will first automatically download the necessary dependencies, and it will run the script.

###Technologies Used in Scala crawler:
1. Scala: a functional programming language on JVM
2. Akka: a effective framework for asynchronous, non-blocking and event-driven programming in Scala
3. Spray-client: a light-weighted HTTP client based on Akka Actor model.

##Python Based Crawler Setup
1. Install the requirements for this crawler `pip install -r requirements.txt`
2. Run `$ python eu_scraper.py`

###Technologies Used in Python Crawler:
1. Requests library
2. lxml library for DOM traversal
