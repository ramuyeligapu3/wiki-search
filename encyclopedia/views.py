from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from . import util
import markdown2



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    entry_content= util.get_entry(title)
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The requested page '{title}' was not found."
        }) 
    else:
        html_content = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    entries=util.list_entries()
    query=request.GET['q']
    if query in entries:
        return redirect("{% url 'entry' q %}" )
    matching_entries=[entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search_result.html", {
            "query": query,
            "entries": matching_entries
        })

