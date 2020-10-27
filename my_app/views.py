import requests
from django.http import HttpResponse
from django.shortcuts import render
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from . import models

BASE_CRGS_URL = 'https://losangeles.craigslist.org/search/sss?query={}'

# Create your views here.
def home(request):
    return render(request, 'base.html', {})

def new_search(request):

    # get the value from POST dictionary by name attribute in HTML
    search = request.POST.get('search-data')

    # Store the search in the DB
    models.Search.objects.create(search=search)

    #Format the final URL with parameters that we need based on BASE_CRGS_URL
    final_url = BASE_CRGS_URL.format(quote_plus(search))

    #Get the response of the get request from craigslist.org
    response = requests.get(final_url)

    data = response.text

    # Get the <a> tag with class result-title from craigslist.org PARSING
    soup = BeautifulSoup(data, features='html.parser')

    # The list of posts scraped from the site
    post_listing = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    # Iterating over the list of <li> tags (ads)
    for post in post_listing:
        # Parsing the info-s that we need to store and transfer to front-end
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price ='N/A'

        BASE_IMG_URL = 'https://images.craigslist.org/{}_300x300.jpg'

        # Find the image if it exists
        if post.find(class_='result-image').get('data-ids'):
            # Get the data-ids attribute in <a> tag
            url_id = post.find(class_='result-image').get('data-ids')

            # Make the list of ids then, split 2 times by ',' and by ':'
            # make the working url of img. You can access it by using the [1] index
            parsed_url = url_id.split(',')[0].split(':')[1]

            # Insert into the BASE_IMG_URL with those info we got above
            post_img = BASE_IMG_URL.format(parsed_url)

        # If the card doesn't have an image return the default image used by craigslist
        else:
            post_img = 'https://craigslist.org/images/peace.jpg'

        # Storing the post info-s in the list to give it to the frontend
        final_postings.append((post_title, post_url, post_price, post_img ))



    context = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', context)
