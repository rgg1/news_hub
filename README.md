# News Hub

## Description

News Hub is a news aggregator website hosted at https://news-hub.azurewebsites.net.
This website allows users to search for any news they want and be provided with a summary
of the article as well as a predicted sentiment of it (positive/negative).

This website was made using Django with HTML and CSS on the frontend. This project makes
use of various tools. It uses the Bing News Search API to get recent news articles pertaining
to the user's search query. I then use the BeautifulSoup library to scrape these url's for the
artcle's actual content. After that, I make use of models that I trained and deployed on Azure.

The first model is the summarization model. It was fine-tuned on a dataset of over 2000
BBC News summaries: https://www.kaggle.com/datasets/pariza/bbc-news-summary. The pretrained
model is the Text-To-Text Transfer Transformer (T5) used for NLP using the t5-small checkpoint 
available through Hugging Face. Because of compute constraints, the summaries at times cut off
at around 450 tokens to avoid timing out.

The second model is the sentiment analysis model. It was fine-tuned on a dataset of over 1200 news summaries.
The original dataset came from https://www.kaggle.com/datasets/hoshi7/news-sentiment-dataset, which originally had
around 850 news articles with sentiment values. I then used back-translation and synonym replacement to augment this data.
After that, I ran the articles through my summary model to generate summaries for them. In this way, I now had a news summary
sentiment dataset to train this model on. This model is pretrained with BERT - source: https://huggingface.co/bert-base-cased. I was able to obtain an accuracy of over 96% on our test dataset. 

Disclaimer: While the sentiment analysis aims to accurately classify the news as positive or negative, it might not always align with individual perspectives. It attempts to gauge the general mood conveyed by the article, such as whether the news is uplifting or disheartening. However, please bear in mind that interpretations can vary, and the analysis might not always hit the mark.

## Important Notice:

This application relies on Azure ML endpoints for its core functionality. Please be aware that due to computing cost considerations, these endpoints are not left running continuously. Consequently, attempting to aggregate an article without activating the services may result in a Server Error.

If you wish to test the website or need further assistance, feel free to contact me at rgg1@mit.edu, and I will activate the services for you.

## Installation

### Prerequisites
- Python
- Azure ML models
- Bing News Search API

### Steps
1. Clone the repository: `git clone https://github.com/rgg1/news_hub.git`
2. Create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
4. Install required packages: `pip install -r requirements.txt`
5. Apply database migrations: `python manage.py migrate`
6. Run the server: `python manage.py runserver`

## Local Configuration Guide

To run this project locally or in your own production environment, you'll need to make some changes to the `settings.py` and `views.py` files:

### 1. **Django Secret Key**:
   - Generate a new secret key for Django. You can use [Django's Secret Key Generator](https://djecrety.ir/) or another tool.
   - Add it as an environment variable named `'DJANGO_SECRET_KEY'`, or modify `SECRET_KEY` in `settings.py` directly.

### 2. **Allowed Hosts**:
   - Update the `ALLOWED_HOSTS` list with your domain name, IP address, or other hosts as needed.

### 3. **views Configuration**:
   - In views.py, an environment variable is needed to allow the Search API to work, which is:
     - 'SUBSCRIPTION_KEY': API Subscription Key
   - In my case, I had the model services deployed using Azure. If you're using the same method, you have to change these two envionment variables:
     - SUMMARY_URL: The URL of your summary model endpoint.
     - SENTIMENT_URL; The URL of your sentiment model endpoint.

By configuring these settings, you should be able to run the project in a local or custom production environment.

Note that the Azure ML integration was crucial for the project to function. If you wish to use another service for
hosting your models, further configuration would be needed.

## Usage

This section provides a general guide on how to navigate and interact with News Hub.

### Making a Query
1. Visit the page at [News Hub](https://news-hub.azurewebsites.net).
2. Type in any topic you want to search news for and press "Search". For example: "Inflation".
3. Find an interesting article and click "Aggregate". Doing so will bring up a page
showing the original article content, the summary, and the predicted sentiment (positive/negative).
4. Click on the "New Search" button to conduct another search.