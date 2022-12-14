from flask import Flask, redirect, url_for, request 
from flask_sse import sse
import requests
from jinja2 import Environment, FileSystemLoader
import validators
from bs4 import BeautifulSoup
from collections import Counter
import re
from urllib.parse import urlparse, urljoin
import xml.etree.cElementTree as ET
import datetime
import sys
import logging
from pysitemap import crawler
import asyncio

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
environment = Environment(loader=FileSystemLoader("templates/"))

@app.route('/')
def index():
    template = environment.get_template("default.j2")
    return template.render(
            streamlink = url_for('sse.stream')
            )

@app.route('/analyze', methods = ['POST'])
def analyze():
    site_url = str(request.form['site_url'])
    url = re.compile(r"https?://(www\.)?")
    url = url.sub('', site_url).strip().strip('/')
    site_url = 'http://' + url

    error = environment.get_template("error.j2")
    result = environment.get_template("result.j2")

    if not validators.url(site_url):
        return template.render(
                message=site_url+" is not an url", 
                previous_url=request.referrer
                )

    response = requests.get(site_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    word_count = len(soup.get_text().split())
    meta=soup.find("meta", attrs={"name": "description"})
    meta_description = meta["content"] if (meta) else "Nothing" 
    page_title=soup.title.text
    keywords_on_page=dict(Counter(soup.get_text().split()))
    missing_image_alt_text='abc'
    number_of_internal_links=len(set(soup.find_all("a", href=lambda href: href and url in href and not href.startswith('#'))))
    number_of_external_links=len(set(soup.find_all("a", href=lambda href: href and url not in href and not href.startswith('#'))))
    number_of_broken_links="Loading..."
    sitemap="Sitemap not found"
    sse.publish({
        "word_count": word_count,
        "meta_description": meta_description,
        "page_title": page_title,
        "keywords_on_page": keywords_on_page,
        "missing_image_alt_text": missing_image_alt_text,
        "number_of_internal_links": number_of_internal_links,
        "number_of_external_links": number_of_external_links,
        "number_of_broken_links": number_of_broken_links
    }, type="status")

    return result.render(
            word_count=word_count,
            page_title=page_title,
            meta_description=meta_description,
            keywords_on_page=keywords_on_page,
            missing_image_alt_text=missing_image_alt_text,
            number_of_internal_links=number_of_internal_links,
            number_of_external_links=number_of_external_links,
            number_of_broken_links=number_of_broken_links,
            previous_url = request.referrer,
            streamlink = url_for('sse.stream')
            )

@app.route('/brokenlink')
def get_broken_links():
    site_url = request.args.get('site_url')
    url = re.compile(r"https?://(www\.)?")
    url = url.sub('', site_url).strip().strip('/')
    site_url = 'http://' + url
    response = requests.get(site_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    broken_links = []
    links = set(soup.find_all("a", href=lambda href: href and not href.startswith('#')))
    for link in links:
        url = link["href"] if (urlparse(link["href"]).netloc) else urljoin(site_url, link["href"]) 
        try:
            lr = requests.head(url, timeout=0.5)
            if lr.status_code != 200:
                broken_links.append(link["href"])
            print("URL: "+link['href']+"Status Code : "+str(lr.status_code))
        except Exception as e:
            broken_links.append(link["href"])
            print("URL: "+link['href']+"Status Code : "+str(lr.status_code))
            pass
        sse.publish({"message": "Loading", "status": str(len(broken_links))+" out of "+str(len(links))}, type="progress")
    sse.publish({"message": "Complete", "status": str(len(broken_links))+" out of "+str(len(links))}, type="progress")
    return broken_links

@app.route('/getsitemap')
def get_sitemap():
    site_url = request.args.get('site_url')
    url = re.compile(r"https?://(www\.)?")
    url = url.sub('', site_url).strip().strip('/')
    site_url = 'http://' + url
    response = requests.get(site_url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    sitemap_exists = 0
    try:
        sitemap_url = urljoin(site_url, 'sitemap.xml')
        sitemap_response = requests.get(sitemap_url)
        xml = BeautifulSoup(sitemap_response, 'lxml-xml', from_encoding=response.info().get_param('charset'))
        return xml
        sitemap_exists = 1
    except Exception as e:
        sitemap_exists = 0
        pass
    return "Sitemap not found"
