# Web-Scraper Projects

1. Tennis Data:
Las Vegas Opening and Closing Line of Tennis from donbest.com

2. MLB Data:
Pitcher and Batter Matchup Data from mlb.com

2. Houses for Rent Data:
Houses for Rent Data from http://www.58.com

4. Teacher Employment Information Data: 
Using multiprocessing Module to Aggregate Information from Several Websites

### Questions
* Why multiprocessing? Why threading? Differences between multiprocessing & threading.
* Can we use GPU for web scraping?
* What is the best way to build an "exe"(application) file by Python? (Tried "py2exe", "PyInstaller" and "cx-freeze". All have their own flaws if I imported many modules).

### Thoughts
* DataFrame & Series objects have a nice feature about handling the missing data than list, array and dict.
* Exception handlings are important in web scraping.
* To avoid blocking by servers (Eg: hit limits & robot detectors), try to include a sleep time, a fake dynamic ip or a fake header in the crawler...
