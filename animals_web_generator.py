import os
from html import escape

import requests
from dotenv import load_dotenv


API_URL = "https://api.api-ninjas.com/v1/animals"


def fetch_animals_data(name, api_key):
    """Fetch and return animal data from API Ninjas."""
    response = requests.get(
        API_URL,
        headers={"X-Api-Key": api_key},
        params={"name": name},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def load_template(file_path):
    """Read and return the HTML template as text."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return handle.read()


def normalize_animal_name(name):
    """Normalize known mojibake/unicode apostrophe issues in animal names."""
    if not name:
        return name

    normalized = name.replace("â€™", "'").replace("’", "'")
    if normalized.lower() == "darwin's fox":
        return "Darwin's Fox"
    return normalized


def serialize_animal(animal):
    """Return one animal serialized as a styled HTML card item."""
    details = []

    name = normalize_animal_name(animal.get("name"))

    characteristics = animal.get("characteristics", {})

    diet = characteristics.get("diet")
    if diet:
        details.append(f"<strong>Diet:</strong> {diet}")

    locations = animal.get("locations", [])
    if locations:
        details.append(f"<strong>Location:</strong> {locations[0]}")

    animal_type = characteristics.get("type")
    if animal_type:
        details.append(f"<strong>Type:</strong> {animal_type}")

    if not name and not details:
        return ""

    details_html = "<br/>\n      ".join(details)
    if details_html:
        details_html += "<br/>"

    return (
        "<li class=\"cards__item\">\n"
        f"  <div class=\"card__title\">{name}</div>\n"
        "  <p class=\"card__text\">\n"
        f"      {details_html}\n"
        "  </p>\n"
        "</li>"
    )


def serialize_animals(animals_data):
    """Return all animals as HTML list items."""
    animal_blocks = [serialize_animal(animal) for animal in animals_data]
    return "\n".join(block for block in animal_blocks if block)


def build_message_card(message):
    """Return a single card item with an informational message."""
    return (
        "<li class=\"cards__item\">\n"
        "  <div class=\"card__title\">Notice</div>\n"
        "  <p class=\"card__text\">\n"
        f"      {message}<br/>\n"
        "  </p>\n"
        "</li>"
    )


def build_not_found_message(animal_name):
    """Return a formatted not-found message for unknown animal names."""
    safe_name = escape(animal_name)
    return (
        "<li class=\"cards__item\">\n"
        f"  <h2>The animal \"{safe_name}\" doesn't exist.</h2>\n"
        "</li>"
    )


def get_user_animal_name():
    """Prompt until the user enters a non-empty animal name."""
    while True:
        name = input("Enter a name of an animal: ").strip()
        if name:
            return name
        print("Animal name cannot be empty. Please try again.")


def main():
    load_dotenv()

    template_html = load_template("animals_template.html")
    name = get_user_animal_name()
    api_key = os.getenv("API_NINJAS_API_KEY")

    if not api_key:
        animals_info = build_message_card(
            "Set API_NINJAS_API_KEY to fetch animals from API Ninjas."
        )
    else:
        try:
            animals_data = fetch_animals_data(name, api_key)
            animals_info = (
                serialize_animals(animals_data)
                if animals_data
                else build_not_found_message(name)
            )
        except requests.RequestException as error:
            animals_info = build_message_card(f"API request failed: {error}")

    final_html = template_html.replace("__REPLACE_ANIMALS_INFO__", animals_info)

    with open("animals.html", "w", encoding="utf-8") as output_file:
        output_file.write(final_html)

if __name__ == "__main__":
    main()
