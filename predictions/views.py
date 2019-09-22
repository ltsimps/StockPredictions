from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django import forms
from django.core.exceptions import ValidationError

from django.utils.timezone import now #test
import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame


# Create your views here.

class StockForm(forms.Form):
    stock_name = forms.CharField(label='Enter a Stock to Predict', max_length=50)

    def clean_stock_name(self):
        data = self.cleaned_data['stock_name']

        #if type(data) != str:
        #  raise ValidationError(_('Bad Stock Name'))

        return data


class HomePageView(TemplateView):
    template_name = 'home.html'

    def post(self, request):
        print("In FORM")
        print(request.POST.get('stock_name', ""))
        stock_name = request.POST.get('stock_name', "")
        if type(stock_name) == str:
            print("string")
        start = datetime.datetime(2010, 1, 1)
        end = datetime.datetime(2019, 1, 11)
        
        df = web.DataReader(stock_name, 'yahoo', start, end)
        
        print(df.tail())
        print(df[:1])
        
        return render(request, 'home.html') 


    
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        
        if now().weekday() < 5 and 8 < now().hour < 18:
            context['open'] = True
        else:
            context['open'] = False
            
            #context['open'] = df.item(1)
        return context