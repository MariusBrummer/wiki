from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown

from . import util


def convert_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    entries = util.list_entries()
    non_empty_entries = [entry for entry in entries if entry.strip()]  # Filter out entries with empty titles
    return render(request, "encyclopedia/index.html", {
        "entries": non_empty_entries
    })


def entry(request, title):
    html = convert_to_html(title)
    if html is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "message": f"The requested page for '{title}' was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })


def search(request):
    if request.method == "POST":
        entry_search = request.POST.get("q")
        html_content = convert_to_html(entry_search)

        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            # partial search
            matching_entries = []
            all_entries = util.list_entries()
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    matching_entries.append(entry)
            if matching_entries:
                return render(request, "encyclopedia/search.html", {
                    "query": entry_search,
                    "entries": matching_entries
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "query": entry_search,

                })


def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]

        if util.get_entry(title) is None:
            util.save_entry(title, content)
            html = convert_to_html(title)

            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "title": title,
                "message": f"The page for '{title}' already exists."
            })


def edit(request):
    if request.method == "POST":
        title = request.POST["edit_title"]
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })


def save_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.edit_entry(title, content)
        html = convert_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })


def random_page(request):
    import random
    entries = util.list_entries()
    random_entry = random.choice(entries)
    html = convert_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html
    })
