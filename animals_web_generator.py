import json


def load_data(file_path):
    """Load and return JSON data from a file."""
    with open(file_path, "r") as handle:
        return json.load(handle)


def load_template(file_path):
    """Read and return the HTML template as text."""
    with open(file_path, "r") as handle:
        return handle.read()


def serialize_animal(animal):
    """Return one animal serialized as an HTML list item."""
    lines = []

    name = animal.get("name")
    if name:
        lines.append(f"Name: {name}")

    characteristics = animal.get("characteristics", {})

    diet = characteristics.get("diet")
    if diet:
        lines.append(f"Diet: {diet}")

    locations = animal.get("locations", [])
    if locations:
        lines.append(f"Location: {locations[0]}")

    animal_type = characteristics.get("type")
    if animal_type:
        lines.append(f"Type: {animal_type}")

    if not lines:
        return ""

    lines_html = "<br/>\n".join(lines) + "<br/>"
    return f"<li class=\"cards__item\">\n{lines_html}\n</li>"


def serialize_animals(animals_data):
    """Return all animals as HTML list items."""
    animal_blocks = [serialize_animal(animal) for animal in animals_data]
    return "\n".join(block for block in animal_blocks if block)


def main():
    animals_data = load_data("animals_data.json")
    template_html = load_template("animals_template.html")

    animals_info = serialize_animals(animals_data)
    final_html = template_html.replace("__REPLACE_ANIMALS_INFO__", animals_info)

    with open("animals.html", "w") as output_file:
        output_file.write(final_html)


if __name__ == "__main__":
    main()
