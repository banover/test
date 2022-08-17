from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Route to input entry if it exists
def entry(request, entry):
    if request.method == "GET":

        # Checking whether input entry exists or not
        entries = util.list_entries()
        if entry in entries:
            input_entry = entry
        else:
            input_entry = None

        # Rendering Entry page
        return render(request, "encyclopedia/entry.html", {
            #"entries": util.list_entries()                   /wiki/ 는 가능, /wiki/css(etc.) 가 구현못함
            "input_entry": input_entry,
            "contents": util.get_entry(input_entry)
        })
