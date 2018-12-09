# Web-Scraper Projects

1. Tennis Data:
Las Vegas Opening and Closing Lines of Tennis from www.donbest.com

2. MLB Data:
Pitchers and Batters Matchup Data from www.mlb.com

2. Houses for Rent Data:
Rental Data from www.58.com

4. Teacher Employment Information Data: 
Using multiprocessing Module to Aggregate Information from Several Websites

### Questions
* Why multiprocessing? Why threading? Differences between multiprocessing & threading.

----------
Depending on the application, two common approaches in parallel programming are either to run code via threads or multiple processes, respectively. If we submit “jobs” to different threads, those jobs can be pictured as “sub-tasks” of a single process and those threads will usually have access to the same memory areas (i.e., shared memory). This approach can easily lead to conflicts in case of improper synchronization, for example, if processes are writing to the same memory location at the same time.

A safer approach (although it comes with an additional overhead due to the communication overhead between separate processes) is to submit multiple processes to completely separate memory locations (i.e., distributed memory): Every process will **_run completely independent_** from each other (just like what happened when we used _apply_ and _map_ functions in the Pool class).

Reference: https://sebastianraschka.com/Articles/2014_multiprocessing.html

----------

* Can we use GPU for web scraping? LOL
* What is the best way to build an "exe"(application) file using Python? (Tried "py2exe", "PyInstaller" and "cx-freeze". All have their own flaws if I imported many modules).

### Thoughts
* DataFrame & Series objects have a nice feature about handling the missing data than list, array and dict.
* Exception handlings are important in web scraping.
* To avoid blocking by servers (Eg: hit limits & robot detectors), try to include a sleep time, a fake dynamic ip or a fake header in the crawler...
