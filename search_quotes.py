import json
import os
import re

import redis

from models import Author, Quote

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    db=int(os.getenv("REDIS_DB", "0")),
    decode_responses=True,
)


def format_quotes(quotes):
    return [
        {
            "author": quote.author.fullname,
            "quote": quote.quote,
        }
        for quote in quotes
    ]


def print_results(results):
    if not results:
        print("Нічого не знайдено.")
        return

    for item in results:
        print(f'{item["author"]}: {item["quote"]}')


def get_cache(key):
    try:
        value = redis_client.get(key)
        if value:
            print("(результат із Redis)")
            return json.loads(value)
    except redis.RedisError:
        pass

    return None


def set_cache(key, value):
    try:
        redis_client.set(
            key,
            json.dumps(value, ensure_ascii=False),
            ex=300,
        )
    except redis.RedisError:
        pass


def search_by_name(value):
    key = f"name:{value.lower()}"

    cached = get_cache(key)
    if cached is not None:
        return cached

    regex = f"^{re.escape(value)}"
    authors = Author.objects(fullname__iregex=regex)

    quotes = []
    for author in authors:
        quotes.extend(Quote.objects(author=author))

    result = format_quotes(quotes)
    set_cache(key, result)
    return result


def search_by_tag(value):
    key = f"tag:{value.lower()}"

    cached = get_cache(key)
    if cached is not None:
        return cached

    regex = f"^{re.escape(value)}"
    quotes = Quote.objects(tags__iregex=regex)

    result = format_quotes(quotes)
    set_cache(key, result)
    return result


def search_by_tags(values):
    quotes = Quote.objects(tags__in=[value.lower() for value in values])
    return format_quotes(quotes)


def main():
    print("Пошук цитат. Приклади команд:")
    print("name:Steve Martin")
    print("name:st")
    print("tag:life")
    print("tag:li")
    print("tags:life,live")
    print("exit")

    while True:
        command = input("\n>>> ").strip()

        if command.lower() == "exit":
            print("Програму завершено.")
            break

        if ":" not in command:
            print("Невірний формат. Використовуйте команда: значення")
            continue

        command_name, value = command.split(":", 1)
        command_name = command_name.lower().strip()
        value = value.strip()

        if not value:
            print("Значення для пошуку не може бути порожнім.")
            continue

        if command_name == "name":
            results = search_by_name(value)
            print_results(results)

        elif command_name == "tag":
            results = search_by_tag(value)
            print_results(results)

        elif command_name == "tags":
            tags = [tag.strip().lower() for tag in value.split(",")]
            tags = [tag for tag in tags if tag]

            if not tags:
                print("Потрібно вказати хоча б один тег.")
                continue

            results = search_by_tags(tags)
            print_results(results)

        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()
