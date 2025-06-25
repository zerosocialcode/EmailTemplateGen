# EmailTemplateGen

A Flask web app for seamlessly generating professional email templates.

**Developer:** [zerosocialcode](https://github.com/zerosocialcode)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Directory Structure](#directory-structure)
- [Extending and Customization](#extending-and-customization)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**EmailTemplateGen** is a user-friendly web application built with Flask that allows users to quickly generate professional email templates. Designed for productivity and ease of use, the app provides customizable templates for various use cases, making your email communication more efficient.

---

## Features

- Simple and intuitive web interface
- Multiple built-in email templates (business, follow-up, announcement, etc.)
- Customizable fields for personalization
- Download or copy generated emails
- Responsive design

---

## Installation

### Prerequisites

- Python 3.7+
- pip

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/zerosocialcode/EmailTemplateGen.git
   cd EmailTemplateGen
   ```

2. **(Optional) Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   flask run
   ```
   By default, the app runs at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage

1. Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).
2. Select an email template or create a new one.
3. Fill in the required fields to personalize your email.
4. Preview, copy, or download the generated email template.

### Example Usage

- **Business Introduction Email:**
  - Select the "Business Introduction" template.
  - Enter recipient's name, your business details, and message.
  - Click "Generate" to see the ready-to-use email.
  - Use "Copy" or "Download" to use the template in your email client.

- **Custom Template:**
  - Select "Custom" or "New Template".
  - Add your custom fields and content.
  - Save for future use or generate immediately.

---

## Configuration

You can customize the application using environment variables or by editing configuration files.

- **Environment Variables:**
  - `FLASK_ENV=development` for development mode
  - `SECRET_KEY` to set the Flask app secret

- **Templates:**
  - Edit or add new templates in the `/templates` directory (HTML/Jinja2 format).
  - Static assets (CSS, JS) can be modified in `/static`.

---

## Directory Structure

```
EmailTemplateGen/
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── templates/           # HTML/Jinja2 email templates
├── static/              # CSS, JS, images
├── README.md
└── ...
```

---

## Extending and Customization

- **Adding Templates:**  
  Add new `.html` files in the `templates/` directory. Update the app logic (typically in `app.py`) to recognize and render the new template.
- **Modifying Styles:**  
  Edit files in `static/` to change the look and feel.
- **Adding Fields:**  
  Modify the form logic in `app.py` and the corresponding HTML templates to include new fields.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements, new features, or bug fixes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

**EmailTemplateGen** — Seamlessly generate professional emails.