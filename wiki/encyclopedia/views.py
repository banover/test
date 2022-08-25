from django.shortcuts import render
from . import util
import markdown
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
import os
from random import seed
from random import randint
from datetime import datetime

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Route to input entry if it exists
def entry(request, entry):
    if request.method == "GET":

        # Checking whether entry is in entries or not
        key = None 
        entries = util.list_entries()        
        for i in range(len(entries)):
            if entry.upper() == entries[i].upper():          
                key = i
                break

        # Assigning entries[i] to input entry
        contents = None
        if not key == None:
            input_entry = entries[key]
            contents = markdown.markdown(util.get_entry(input_entry))            
        else:        
            input_entry = None

        # Rendering Entry page        
        return render(request, "encyclopedia/entry.html", {
            #"entries": util.list_entries()                   
            "input_entry": input_entry,
            "contents": contents   #util.get_entry(input_entry)
        })


# Making a entries list in html based on searching
def search(request):

    # Checking whether request method is get or not
    if request.method == "GET":

        # Setting variable for compare search and entries
        search = request.GET.get('q')        
        entries = util.list_entries()
        key = None     

        # Finding proper entries by comparing
        for i in range(len(entries)):
            if search.upper() == entries[i].upper():          
                key = i
                break

        # if no proper entries exist, render search_result_page
        if key == None:
            search_result = util.compare(search, entries)                                     
            
            return render(request, "encyclopedia/search_result_page.html", {                         
                "search_result": search_result                    
            })

        # if proper entries exist, changing markdown file to html file
        contents = None
        if not key == None:
            input_entry = entries[key]
            contents = markdown.markdown(util.get_entry(input_entry))            
        else:
            input_entry = None

        return render(request, "encyclopedia/entry.html", {
            "input_entry": input_entry,
            "contents": contents
        })

def create(request):

    # Making a form class
    class NewTaskForm(forms.Form):        
        form = forms.CharField(label="Page Title", max_length="31")        

    # When the method is get
    if request.method == "GET":

        # Getting list of entries
        entries = util.list_entries()     

        # Rendering create.html file with a form
        return render(request, "encyclopedia/create.html", {
            "form": NewTaskForm()            
        })

    # When the method is post
    else:
        
        # Store data from post in title
        title = NewTaskForm(request.POST)

        # Preparing data from post to check duplication of entries
        if title.is_valid():            
            entry = title.cleaned_data["form"]

            # Checking validation of title
            if '/' in entry:
                messages.warning(request, 'title is unvalid.')
                return render(request,"encyclopedia/create.html", {
                    "form": NewTaskForm()
                })

            content = request.POST.get("content")
            entries = util.list_entries()

            # Checking whether entry is already exist in entries
            for i in range(len(entries)):
                if entry.upper() == entries[i].upper():

                    # Making a message opened when there is duplication
                    messages.warning(request, 'Your title already exists.')

                    # Rendering create.html with duplicated form data
                    return render(request,"encyclopedia/create.html", {
                        "form" : title                        
                    })
            # Open new markdown file and write content data from post 
            #with open(f'entries/{entry}.md', "w") as f:
            with open('entries/%s.md' % entry, "w") as f:
                f.write(content)

            # Redirecting to maked new page
            return HttpResponseRedirect(f'/wiki/{entry}')
        
        #  When title is not valid
        else:
            messages.warning(request, 'title is unvalid.')
            return render(request,"encyclopedia/create.html", {
                "form": NewTaskForm()
            })


def update(request, entry):

    # Making form class used in create function
    class NewTaskForm(forms.Form):
        form = forms.CharField(label="Page Title", max_length="31", initial=f"{entry}")

    # When the method is get
    if request.method == "GET":

        # Rendering update.html file with initialed title and content
        title = entry
        content = util.get_entry(title)
        return render(request, "encyclopedia/update.html", {
            "title" : title,
            "content" : content,
            "form" : NewTaskForm()
        })
    
    # When the method is post
    else:

        # Storing updated title and content in valuables
        title = NewTaskForm(request.POST)
        content = request.POST.get("update_content")

        if title.is_valid():            
            entry_title = title.cleaned_data["form"]

            # Checking validation of title
            if '/' in entry_title:
                messages.warning(request, 'title is unvalid.')
                return render(request,"encyclopedia/update.html", {
                    "form": title,
                    "content": content
                })
        
        # Open the updated file and rewrite content
        with open('entries/%s.md' % entry, "w") as f:
            f.write(content)
        
        # Changing old file name to new name
        old_name = f'entries/{entry}.md'
        new_name = f'entries/{entry_title}.md'
        os.rename(old_name, new_name)

        # Redirect to updated page
        return HttpResponseRedirect(f'/wiki/{entry_title}')


def random(request):
    if request.method == "GET":

        entries = util.list_entries()
        number_of_entries = len(entries) - 1

        seed(datetime.now())
        random_value = randint(0, number_of_entries)
        random_entry = entries[random_value]

        return HttpResponseRedirect(f'/wiki/{random_entry}')





