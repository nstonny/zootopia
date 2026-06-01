# Zootopia API Generator

This project fetches animal data from the API Ninjas Animals API and generates `animals.html` from `animals_template.html`.

`animals_web_generator.py` handles user input and HTML rendering, while `data_fetcher.py` handles API communication.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example env file and fill in your API key:

```bash
cp .env.example .env
```

Then edit `.env`:

```bash
API_NINJAS_API_KEY="your_api_key"
```

Generate the page:

```bash
python animals_web_generator.py
```

When prompted, enter an animal name (for example, `Fox` or `Monkey`).

Example:

```bash
$ python animals_web_generator.py
Enter a name of an animal: Fox
Website was successfully generated to the file animals.html.
```

## Output behavior

- If results are found, `animals.html` contains cards for all matching animals.
- If no results are found, `animals.html` shows a friendly message like: `The animal "<name>" doesn't exist.`
- If the API key is missing or the request fails, `animals.html` shows a notice card with the error/context.

The output is written to `animals.html`.

