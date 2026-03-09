# CVCreator

A web application built with [Flask](https://flask.palletsprojects.com/) that allows you to generate a PDF CV/resume directly from your browser. It takes your personal information, education, work experience, and projects through an HTML form, and uses [Playwright](https://playwright.dev/python/) to render a PDF.

## Features

- **Form Interface:** Fill out a web form to input your personal information, skills, education, work experience, and projects.
- **Dynamic Content:** Add multiple entries for education, experience, and projects.
- **PDF Generation:** Uses Playwright's headless Chromium browser to convert an HTML resume into an A4 PDF document.
- **File Download:** The generated CV is downloaded to your device as `YourName_CV.pdf`.

## Tech Stack

- **Backend:** Python + Flask
- **PDF Generation:** Playwright (Chromium Headless)
- **Frontend:** HTML5, CSS3, Jinja2 Templates
- **Package Management:** `uv`

## Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [`uv`](https://github.com/astral-sh/uv) (Python package installer)

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Alexargyros00/CVCreator
   cd CVCreator
   ```

2. **Setup the Virtual Environment & Dependencies:**
   Since the project uses `uv`, you can install dependencies by running:
   ```bash
   uv sync
   ```

3. **Install Playwright Browsers:**
   Playwright requires its own browser binaries to render the PDF. Install the required Chromium browser by running:
   ```bash
   uv run playwright install chromium
   ```

## Usage

1. **Start the Flask Application locally:**
   ```bash
   uv run app.py
   ```
   *(Alternatively, if your `.venv` is activated, you can execute `python app.py`)*

2. **Open the Web Interface:**
   Navigate in your browser to [http://127.0.0.1:5000](http://127.0.0.1:5000).

3. **Generate your CV:**
   - Complete the form with your personal details, education, work history, etc.
   - Submit the form.
   - The application will assemble your CV and serve the final PDF file to you.

## Project Structure

- `app.py`: The application handling web routes, form processing, and headless PDF generation.
- `templates/form.html`: The web interface for data entry.
- `templates/cv_template.html`: The Jinja HTML layout that gets populated with your details before being converted to PDF.
- `pyproject.toml` and `uv.lock`: Project metadata and locked dependency tree managed by `uv`.
- `README.md`: Project documentation.
