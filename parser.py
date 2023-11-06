import csv
import os
from dataclasses import dataclass

from bs4 import BeautifulSoup


@dataclass
class Post:
    text: str


def parse_single_post(post) -> Post:
    return Post(
        text=post.text.strip().strip("\n"),
    )


def parse_page(page_name, dirname="", multiple=False) -> list[Post]:
    path = os.path.join("pages",
                        dirname,
                        page_name) if multiple else os.path.join("pages",
                                                                 page_name)

    with open(path, "rb") as target_file:
        target_page_decoded = target_file.read().decode("utf-8")

        target_page = BeautifulSoup(target_page_decoded, "html.parser")
        page_raw = target_page.select(".text:not([class*='bold'])")
    return [parse_single_post(post) for post in page_raw]


def write_to_csv(csv_path, posts, multiple=False) -> None:
    mode = "a" if multiple else "w"
    with open(csv_path, mode) as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["text"])
        for post in posts:
            writer.writerow([post.text])


def main() -> None:
    for file in os.listdir("pages"):
        if file.endswith(".gitkeep"):
            continue
        if not file.endswith(".html"):
            for part in os.listdir(os.path.join("pages", file)):
                parsed_page = parse_page(part, dirname=file, multiple=True)
                write_to_csv(os.path.join(os.path.join("csv"), f"{file}.csv"),
                             parsed_page,
                             multiple=True)
            continue

        filename = file.split(".")[0]
        parsed_page = parse_page(file)
        write_to_csv(os.path.join(os.path.join("csv"),
                                  f"{filename}.csv"), parsed_page)


if __name__ == "__main__":
    main()
