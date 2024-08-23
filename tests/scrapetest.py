from jolescraper import JoleScraper

url = "https://budibase.com/blog/data/microsoft-access-alternatives/"
tags = ["h1", 'h2', 'h3', 'h4', 'p', 'li', 'ul', 'ol']

scrape = JoleScraper(url, tags)

response = scrape.request_data()
data = scrape.process_data(response)

print(data)