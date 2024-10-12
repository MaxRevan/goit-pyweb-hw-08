import json
from models import Author, Quote


with open("authors.json", "r", encoding="utf-8") as f:
    authors_data = json.load(f)

for author_data in authors_data:
    author = Author(
        fullname=author_data["fullname"],
        born_date=author_data.get("born_date"),
        born_location=author_data.get("born_location"),
        description=author_data.get("description")
    )
    author.save()


with open("qoutes.json", "r", encoding="utf-8") as f:
    quotes_data = json.load(f)

for quote_data in quotes_data:
    author = Author.objects(fullname=quote_data["author"]).first()
    if author:
        quote = Quote(
            tags=quote_data["tags"],
            author=author,
            quote=quote_data["quote"]
        )
        quote.save()
