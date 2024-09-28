from django.shortcuts import render,redirect
from django.http import HttpResponseNotFound
from . import util
import markdown2
from django import forms
import random


class EditPageForm(forms.Form):
    title=forms.CharField(label="Page Title",widget=forms.TextInput(attrs={'class':'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10}))

class NewPageForm(forms.Form):
    title=forms.CharField(label="Page Title",widget=forms.TextInput(attrs={'class':'form-control'}))
    content=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':10}))

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

def create(request):
    if request.method=='POST':
        form=NewPageForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            if util.get_entry(title) is not None:
                return render(request,"encyclopedia/create.html",{
                    "form":form,
                    "error":"An entry with this title already exists."
                })
            
            util.save_entry(title, content)
            return redirect('entry',title=title)
    else:
        form=NewPageForm()
    return render(request,"encyclopedia/create.html",{
                  "form":form
                  })
def edit(request,title):
    entry_content = util.get_entry(title)
    print(f"Editing entry: {title}, Current content: {entry_content}")
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('entry', title=title)
        
    else:
        form = EditPageForm(initial={'content': entry_content,'title':title})

    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)