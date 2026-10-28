# Brazil Toll Plaza Scraper

A small Python scraper that extracts toll-plaza details from a public web page and exports a structured spreadsheet.

## Data collected

The script parses highway, kilometer marker, location, axle count, and listed toll-fee information from its configured source.

## Stack

Python, Requests, BeautifulSoup, Pandas, and OpenPyXL.

## Run locally

Install dependencies from `requirements.txt`, then run `python pedagiomg.py`. The source website can change its page structure or terms, so verify the output before relying on it.


## Snapshot review

The original Minas Gerais entry point is preserved. The `states/` folder additionally groups the source collectors by state; no scraped workbooks are included. Run a selected collector explicitly, for example `python states/ba.py`, after reviewing its public source URL and output path. Extraction against live pages was not run during this review.

Git-triggered Vercel deployment is disabled in the included web configurations. This update publishes source and documentation only.

## License

No new distribution license is granted for this corporate source edition. Public visibility does not grant reuse rights; obtain permission from the relevant rights holder. Existing third-party notices remain applicable.

## Verification record

See [snapshot checks and remaining limitations](docs/VERIFICATION.md).
