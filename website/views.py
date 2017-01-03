from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django import forms
import logging
logger = logging.getLogger(__name__)

# Create your views here.


class NameForm(forms.Form):
    firstname = forms.CharField(label='Your name', max_length=100)
    lastname = forms.CharField(label='Your lastname', max_length=100)


def thepost(request):
    print "thepost request", request
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            print "thepost form is valid--->", firstname, ":", lastname
            print "current form is ", form            
            # redirect to a new URL:
            return render(request, 'mat.html', {'firstname': firstname, 'lastname': lastname})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, 'mat.html', {'form': form})
