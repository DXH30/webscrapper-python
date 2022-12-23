# webscrapper-python
Flask webscrapper for analyze website data, using flask and beautifulsoup4

# Feature
## Current Feature
- Word Count
- Page title
- Meta Description
- Keywords on page
- Number of Internal Links
- Number of External Links
- Number of Broken links
- Sitemap grapper

## Upcoming Feature
- Sitemap generator
- Popular keywords analyzer

# How to run via venv
Clone the repository to your machine
```
git clone https://github.com/dxh30/webscrapper-python
```
cd to directory
```
cd webscrapper-python/src && source bin/activate
```
Install requirements using pip
```
pip install -r requirements.txt
```
Run application with flask
```
flask run
```
Open url in browser
```
http://127.0.0.1:5000
```

# How to run via docker-compose
Clone the repository to your machine
```
git clone https://github.com/dxh30/webscrapper-python
```
cd to directory
```
cd webscrapper-python
```
Run docker-compose up
```
docker-compose up -d
```
If access denied, run by sudo
```
sudo docker-compose up -d
```

# Screenshot
![Screenshot of scanning process](./screenshot.png)
