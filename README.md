# Python Job Finder
### Turn a job-results page into a shortlist you can read locally.

Searching through job listings is easier when irrelevant skills are filtered out first. This Python scraper reads TimesJobs Python listings, keeps recent posts, excludes skills entered by the user, and saves each matching offer as a readable text file.

For example, enter `java,php` at the prompt to skip offers listing those skills. Open the saved files to see the company, role, posting date, skills, and original job link.

## Small details that make the output useful

- **Filtering happens before writing.** The scraper parses posting dates and compares normalized skill names against the exclusion list, so the saved folder reflects the requested shortlist. `DAYS_FILTER_LIMIT` is set to 10 in the script.
- **Files stay readable and separate.** Company and role form the filename, invalid filename characters are replaced, and numeric suffixes avoid overwriting previous results. Requests have a timeout and HTTP errors are handled before parsing.

### A real saved record

From [the collected examples](offres_emploi_python/):

```text
Compagnie: Datagrid Solutions
Poste: Python Developer
Date de publication: 10 days ago
Compétences: python, database, django, mysql, api
```

These are saved examples from collection time, not current vacancies. Each full record also includes the source URL.

## Try it

Use Python 3 and run commands from the repository root:

```bash
git clone https://github.com/Jabour-Salahddine/Web-Scraping-Intro.git
cd Web-Scraping-Intro
python -m venv venv
source venv/bin/activate
python -m pip install beautifulsoup4 requests lxml
python "Scraping A Production Website/main.py"
```

On Windows Git Bash, activate with `source venv/Scripts/activate` instead. Enter comma-separated skills to exclude, or press Enter for no exclusions. Results are written to `offres_emploi_python/`. The script repeats after a 400-second wait; press **Ctrl+C** to stop. Later runs create additional files rather than deduplicating earlier scans.

For a quick offline introduction to the HTML parser:

```bash
python "Test With Local File/main.py"
deactivate
```

The local exercise reads [home.html](Test%20With%20Local%20File/home.html). The live scraper depends on TimesJobs' HTML structure and network availability. Use it in line with the source site's access rules.

## Follow the implementation

Start with [the scraper](Scraping%20A%20Production%20Website/main.py): fetch → parse → date filter → skill filter → text files. The local HTML exercise demonstrates BeautifulSoup selection separately from network requests.
