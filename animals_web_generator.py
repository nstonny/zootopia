import json


def load_data(file_path):
    """Load and return JSON data from a file."""
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


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


def main():
    animals_data = load_data("animals_data.json")
    template_html = load_template("animals_template.html")

    animals_info = serialize_animals(animals_data)
    final_html = template_html.replace("__REPLACE_ANIMALS_INFO__", animals_info)

    with open("animals.html", "w", encoding="utf-8") as output_file:
        output_file.write(final_html)


if __name__ == "__main__":
    main()
