from redis_decor import get_quotes_by_author, get_quotes_by_tag, get_quotes_by_tags


def find_name_tag():
    while True:
        command = input("Enter command: ").strip()

        if command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            quotes = get_quotes_by_author(author_name)
            if quotes:
                print("\n".join(quotes))
            else:
                print(f"No quotes found for author: {author_name}")

        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = get_quotes_by_tag(tag)
            if quotes:
                print("\n".join(quotes))
            else:
                print(f"No quotes found for author: {tag}")

        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(",")
            quotes = get_quotes_by_tags(tags)
            if quotes:
                print("\n".join(quotes))
            else:
                print(f"No quotes found for author: {tags}")

        elif command == "exit":
            print("Goodbye, my friend")
            break

        else:
            print("Invalid command")

find_name_tag()
