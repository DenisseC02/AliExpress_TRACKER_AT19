import requests, json # , lxml #
from bs4 import BeautifulSoup
import datetime

#search_item = 'perro'

#search_url = 'https://es.aliexpress.com/wholesale?catId=0&initiative_id=SB_20221124083106&SearchText=pantalon&spm=a2g0o.productlist.1000002.0&dida=y'
#search_url = 'https://es.aliexpress.com/wholesale?catId=0&initiative_id=SB_20221124095035&SearchText=perro&spm=a2g0o.productlist.1000002.0&dida=y'
product_url = 'https://es.aliexpress.com/item/4000473310633.html' # the number after item is productID

product_list = []

def scrapper(search_item = 'perro'):
    search_url = 'https://es.aliexpress.com/wholesale?SearchText='+search_item+'&dida=y'
    date_now = datetime.datetime.now()
    print('\n--- Requesting conection... {}'.format(search_url.split('/')[2]))
    page_content = requests.get(search_url)
    print(f'\n--- Conection established on {date_now}\n--- Trying to retrieve content...')
    page_response = page_content.status_code
   
    if page_response == 200:
        print('\n--- Parsing data...')
        soup_parser = BeautifulSoup(page_content.content, 'html.parser')
        print('\n--- Getting products list...')
        product_list = soup_parser.findAll('script')[1].text.strip()[139:-1]

        if product_list:
            product_json = json.loads(product_list)

            partial_result = product_json['data']['root']['fields']['mods']['itemList']['content']

            search_result_list = []
            print(f'\n--- Found {len(partial_result)} items...')
            print(f'\n--- Filtering by rating...\n')

            for index, items in enumerate(partial_result):

                if 'evaluation' in items:
                     search_result_list.append({
                        "productID":items['productId'],
                        "title":items.get('title','product').get('displayTitle') if 'title' in items else 'Producto',
                        "price":items['prices']['salePrice']['minPrice'],
                        "rate":items['evaluation']['starRating'],
                        "image":items['image']['imgUrl']
                     })

            search_result = {"products": search_result_list}
            #search_result = search_result_list
            print(search_result, "-----------> SCRAPPER")
            print(f'\n--- Found {len(search_result)} items.')
        else:
             print('\n--- Something went wrong, here is the content...\n')
             print(product_list)
             print('\n--- Nothing to work with. Quitting.\n')
             return None

    else:
        page_action = input(f'\n--- Error: {page_response}. Conection fails.\nDo you want to Retry (y/n)? ')
        if page_action.lower() == 'y':
            scrapping(search_url)
        else:
            print('\n--- Nothing to work with. Quitting.\n')
            return None
    
    return search_result



scrapper()
