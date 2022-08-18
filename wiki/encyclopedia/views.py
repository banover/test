from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Route to input entry if it exists
def entry(request, entry):
    if request.method == "GET":

        # Checking whether entry is in entries or not 
        entries = util.list_entries()        
        for i in range(len(entries)):
            if entry.upper() == entries[i].upper():          
                key = i
                break

        # Assigning entries[i] to input entry
        if not key == None:
            input_entry = entries[key]
        else:
            input_entry = None

        # Rendering Entry page
        return render(request, "encyclopedia/entry.html", {
            #"entries": util.list_entries()                   
            "input_entry": input_entry,
            "contents": util.get_entry(input_entry)
        })
