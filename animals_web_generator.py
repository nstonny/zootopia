import json

def load_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return json.load(handle)

animals_data = load_data('animals_data.json')

for animal in animals_data:
    if 'name' in animal:
        print(f"Name: {animal['name']}")
    characteristics = animal.get('characteristics', {})
    if 'diet' in characteristics:
        print(f"Diet: {characteristics['diet']}")
    if animal.get('locations'):
        print(f"Location: {animal['locations'][0]}")
    if 'type' in characteristics:
        print(f"Type: {characteristics['type']}")
    print()
