from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template.loader import get_template
from django.shortcuts import render
from ProjectTracker.scrapping import scrapper

def home_page(request): #primera vista


    return render(request, 'index.html')


def scrapping_results(request, search_item='gato'):
    product_list = scrapper(search_item)
    #print(product_list, "-----------> VIEWS\n\n")
    #print({"products_found":product_list},"-----------> RESPONSE\n\n")
    return render(request,"products.html", {"products_found":product_list})