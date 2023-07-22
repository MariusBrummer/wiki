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
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
        query = request.POST["q"]
        html = convert_to_html(query)
        if html is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": query,
                "content": html
            })
        else:
            all_entries = util.list_entries()
            matching_entries = []
            for entry in all_entries:
                if query.lower() in entry.lower():
                    matching_entries.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entries": matching_entries,
                "query": query
            })



