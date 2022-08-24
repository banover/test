from django.shortcuts import render
from . import util
import markdown
from django import forms
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect


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

    class NewTaskForm(forms.Form):        
        form = forms.CharField(label="Page Title")
        

    if request.method == "GET":

        entries = util.list_entries()
        #messages.warning(request, 'Your title already exists.')

        return render(request, "encyclopedia/create.html", {
            "form": NewTaskForm(),
            #"entries": entries
        })

    # post로 create.html에서 title과 textarea 정보 form전달 될 때, 페이지 만들어 주던가 오류페이지 띄우던가
    else:

        #title = request.POST["title"]
        title = NewTaskForm(request.POST)

        if title.is_valid():
            entry = title.cleaned_data["form"]
            content = request.POST.get("content")
            #if len(content) > 0:
            #    return render(request,"encyclopedia/test.html", {
            #        "entry" : content
            #    })
            #content = request.POST["content"]
            entries = util.list_entries()

            for i in range(len(entries)):
                if entry.upper() == entries[i].upper():
                    #messages.warning(request, 'Your title already exists.') 에러메세지만 씀녀 끝
                    return render(request,"encyclopedia/create.html", {
                        "form" : title
                    })
            #
            with open(f'entries/{entry}.md', "w") as f:
                f.write(content)

            #
            return HttpResponseRedirect(f'/wiki/{entry}')
        
        # 여기도 메세지 추가해주면 좋을듯?  
        else:            
            return render(request,"encyclopedia/create.html")


            