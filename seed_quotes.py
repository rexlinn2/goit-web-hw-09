import json

from models import Author, Quote


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def seed_authors():
    authors_data = load_json("authors.json")

    for data in authors_data:
        author = Author.objects(fullname=data["fullname"]).first()

        if author:
            author.born_date = data.get("born_date", "")
            author.born_location = data.get("born_location", "")
            author.description = data.get("description", "")
            author.save()
        else:
            Author(
                fullname=data["fullname"],
                born_date=data.get("born_date", ""),
                born_location=data.get("born_location", ""),
                description=data.get("description", ""),
            ).save()

    print("Авторів завантажено.")


def seed_quotes():
    quotes_data = load_json("quotes.json")

    for data in quotes_data:
        author = Author.objects(fullname=data["author"]).first()

        if not author:
            print(f"Автор не знайдений: {data['author']}")
            continue

        existing = Quote.objects(
            author=author,
            quote=data["quote"],
        ).first()

        if not existing:
            Quote(
                tags=data.get("tags", []),
                author=author,
                quote=data["quote"],
            ).save()

    print("Цитати завантажено.")


if __name__ == "__main__":
    seed_authors()
    seed_quotes()
    print("Імпорт завершено.")
