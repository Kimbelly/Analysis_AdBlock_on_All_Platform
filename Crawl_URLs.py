# Crawl URLs to Get Many Websites (Test Set) 
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
import socket

internal_urls = set()  # Initialize the set of links (unique links)
total_urls_visited = 0
error_count = 0


def is_valid(url):  # Checks whether 'url' is a valid URL.
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    # Returns all URLs that is found on 'url' in which it belongs to the same website

    urls = set()  # All URLs of 'url'
    domain_name = urlparse(url).netloc

    try:
        r = requests.get(url, timeout=20).content
        soup = BeautifulSoup(r, "html.parser")

        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue

            href = urljoin(url, href)  # Join the URL if it's relative
            parsed_href = urlparse(href)
            # Remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

            if not is_valid(href):
                continue
            if href in internal_urls:  # Already in the set
                continue
            if domain_name not in href:  # External link
                continue

            urls.add(href)
            internal_urls.add(href)

        return urls
    except requests.exceptions.RequestException as e:
        return None


def crawl(url, max_urls):
    global error_count
    global total_urls_visited
    total_urls_visited += 1

    try:
        links = get_all_website_links(url)
        for link in links:
            if total_urls_visited > max_urls:
                break
            crawl(link, max_urls)
    except:
        print("Error... continue try next. Error site: " + url)
        error_count += 1


if __name__ == "__main__":
    max_urls = 1

    for i in range(4, 5):  
        domain_file = open('/home/kimbelly/Experiment/Crawl_TestURLs/TestDomain/test.txt', 'r')
        lines = domain_file.read().splitlines()
        domain_file.close()

        crawl_result_file = open('/home/kimbelly/Experiment/Crawl_TestURLs/Crawl_Result/Crawl_Result_'
                  + str(i) + '.txt', 'w')  # a+ ?

        crawl_count = 1
        for ele in lines:
            url = "https://" + ele
            print(str(crawl_count) + ". Crawl: " + url)
            try:
                requests.get(url, timeout=10)
                crawl(url, max_urls)
            except requests.exceptions.SSLError as e:  # Maybe not https site
                print("Catch requests.exceptions.SSLError, and try again:")
                url = "http://" + ele
                print(str(crawl_count) + ". Crawl: " + url)
                try:
                    requests.get(url, timeout=10)
                    crawl(url, max_urls)
                except requests.exceptions.ConnectionError as e:
                    print("Try again, add 'www':")
                    url = "http://www." + ele
                    print(str(crawl_count) + ". Crawl: " + url)
                    try:
                        requests.get(url, timeout=10)
                        crawl(url, max_urls)
                    except:
                        print("Maybe No address associated with hostname, give up.")
                except:
                    print("Just give up...")
            except requests.exceptions.ConnectionError as e:  # Maybe need to add 'www'
                print("Catch requests.exceptions.ConnectionError, and try again:")
                url = "https://www." + ele
                print(str(crawl_count) + ". Crawl: " + url)
                try:
                    requests.get(url, timeout=10)
                    crawl(url, max_urls)
                except:
                    print("Try again, use http://www:")
                    url = "http://www." + ele
                    print(str(crawl_count) + ". Crawl: " + url)
                    try:
                        requests.get(url, timeout=10)
                        crawl(url, max_urls)
                    except:
                        print("Maybe No address associated with hostname, give up.")
            except:
                print("Final exception(another problem)..., give up.")

            crawl_count += 1

        print("\n[+] Total Internal links in ALL:", len(internal_urls))
        print("# of error domains: " + str(error_count) + "\n")
        # Save the internal links to a file
        for internal_link in internal_urls:
            crawl_result_file.write(internal_link + "\n")

        crawl_result_file.close()
        internal_urls.clear()

# except requests.exceptions.RequestException:
#    print("Catch requests.exceptions.RequestException, give up: " + url)

