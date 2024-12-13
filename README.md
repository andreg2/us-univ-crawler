# **Software Usage:**

### Running the Software
For executing and initializing the crawlers and the database for this project first you must check if you have the following dependencies:
- playwright
- scrapy
- sqlite3

After installing all the required dependencies you will be able to successfully execute the project.
For executing the project you must execute `python3 init_crawler.py` from the `univs` folder right under the `us-univ-crawler`

Running the above command the crawlers will be triggered one by one and the following will happen: 
1) Some crawlers will crawl the universities sites for data related to the undergraduate programs they have available and add it to a sqlite database in your machine.
2) One of the crawlers also will crawl the shanghai ranking site to get information about universities rankings and also save this to the sqlite3 db locally.
3) After having the data about the universities ready the system will create documents in a certain format for being queried later by NLP tools.

Ps.: Be aware that sometimes the crawler for Shanghai ranking fails due to internet instability or due to their server, so you might have to try again in that case.

You also can run each crawler individually by running the following code: `python3 -m scrapy crawl {crawler_name}` so if one of the crawlers fails to execute when running you can run any of them individually in order to get data from there.
Here is a list of the crawlers names you can use:
- Universities Crawlers:
  - harvard
  - yale
  - stanford
  - uiuc
- Rankings Crawlers:
  - shanghai

# **Software Implementation:**

### Main Libraries
For this project I used 3 main libraries for development and did all the development in Python:
- SQLite3
  - This lib was used for building a database with the information collected by the crawlers and create an easy to use local database with it.
- Scrapy
  - This lib was used for creating the "spiders", the crawlers that will collect the data the spiders can be found on the folder `univs/univs/spiders/rankings` and `univs/univs/spiders/universities`. They crawl the websites and saves the data collected into the db using sqlite3.
- Playwirght
  - This lib was needed due to some sites that had dynamic html/css by using javascript, so this lib was used along with the spiders from scrpy to some websites such as the harvard university and shanghai. This way I was able to dynamically scrape data going through a list of information.

When a crawler is triggered it will reach the webpage related to the university or ranking site and it will collect data and save to a sqlite3 database. After collecting data from all the crawlers, the system will use it for creating text documents for each of the universities that will be used in the future for creating an index and to be queried by another NLP tool for providing recommendations to users.

# **Future Work:**
- Unfortunately I was able yet to develop the part of the system that query the university documents using NLP since I faced more challanges than expected for getting the crawlers to work and to create the documents for each university.
- So for the future I would like to develop this part for using Pyserini for reading the documents and creating an index for querying data from there and providing recommendations to the users.
- Besides not having this ready yet, the database with data collected by the crawlers can be used for now for querying aggragated data about the universities courses, addresses and rankings.
- Also for the future I will work on a better fault tolerance for the crawlers, having a retry method and improved logs.
