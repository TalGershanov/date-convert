# Hebrew Date Converter

Converts a Gregorian date to a Hebrew date using the
[Hebcal converter API](https://www.hebcal.com/home/219/hebrew-date-converter-rest-api).

## Structure

- `front/index.html` - single page (vanilla JS/CSS): pick a date, convert, start over.
- `api/app.py` - FastAPI app with `POST /api/convert` (`{"date": "YYYY-MM-DD"}`); also serves the page.
- `logic/converter.py` - validates the date and calls Hebcal (`cfg=json`).
- `config.py` - Hebcal URL and request timeout.

## Run

From the project root (the `.venv` with all dependencies is already there):

```bash
.venv/bin/uvicorn api.app:app
```

Open http://localhost:8000/

On a fresh machine without `.venv`, first run
`python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

