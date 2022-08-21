from django.shortcuts import render
from . import util
import markdown
#from django.urls import reverse
#from django.http import HttpResponseRedirect

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
