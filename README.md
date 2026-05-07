## 50legs Scraper
The function of this application is to grab the page https://50legs.org/application-for-assistance/
and make a local copy in /var/www/html. This was done due to flakiness trying to read it in with
BeautifulSoup in Python.

It then scans the contents of the local web page and scans for the target_text

If found it sends (via email) one message if it is not found it sends a different message 
