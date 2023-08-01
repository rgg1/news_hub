from django.shortcuts import render
from .forms import SearchForm
import requests
from bs4 import BeautifulSoup, Comment
import json
import os

from dotenv import load_dotenv
load_dotenv()

from django.conf import settings

# Create your views here.

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            # Fetch news articles
            if settings.DEBUG:
                subscription_key = os.getenv('SUBSCRIPTION_KEY')
            else:
                subscription_key = os.environ.get('SUBSCRIPTION_KEY')
            search_url = "https://api.bing.microsoft.com/v7.0/news/search"
            headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
            params  = {"q": query, "textDecorations": True, "textFormat": "HTML", "count": 25}
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()
            search_results = response.json()

            excluded_domains = ["msn.com", "newyorker.com", "wsj.com", "newsweek.com", "nytimes.com", "ft.com", "geekwire.com",
                                "bloomberg.com", "thestreet.com"]

            articles = [
                {'url': article["url"], 'title': BeautifulSoup(article["name"], 'html.parser').get_text()}
                for article in search_results["value"]
                if not any(domain in article["url"] for domain in excluded_domains)
            ]


            # Pass the articles to the template
            return render(request, 'search/results.html', {'articles': articles})
    else:
        form = SearchForm()

    return render(request, 'search/search.html', {'form': form})

def aggregate(request):
    url = request.GET.get('url')
    # Scrape the article
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for tag in soup(['header', 'footer', 'nav', 'aside']):
        tag.decompose()

    for element in soup.findAll(string=lambda text: isinstance(text, Comment)):
        element.extract()

    article_text = "\n".join([p.get_text(strip=True, separator='\n') for p in soup.select('p') if len(p.get_text(strip=True, separator='\n').split()) > 10 and p.get_text(strip=True, separator='\n').count('<a') < 3])
    article_text2 = 'summarize: ' + article_text
    
    # Summarize the article
    if settings.DEBUG:
        summary_url = os.getenv('SUMMARY_URL')
    else:
        summary_url = os.environ.get('SUMMARY_URL')
    summary_data = {"text": article_text2}
    input_data = json.dumps(summary_data)
    headers = {'Content-Type': 'application/json'}
    summary_response = requests.post(summary_url, input_data, headers=headers)
    summary = summary_response.json()

    # Analyze the sentiment
    if settings.DEBUG:
        sentiment_url = os.getenv('SENTIMENT_URL')
    else:
        sentiment_url = os.environ.get('SENTIMENT_URL')
    sentiment_data = {"text": summary}
    input_data = json.dumps(sentiment_data)
    sentiment_response = requests.post(sentiment_url, input_data, headers=headers)
    sentiment = sentiment_response.json()

    # Pass all the data to the template
    return render(request, 'search/aggregate.html', {
        'url': url,
        'article_text': article_text,
        'summary': summary,
        'sentiment': sentiment
    })
