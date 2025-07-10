# TemplateFusion

> **Actively maintained by [zerosocialcode](mailto:zerosocialcode@gmail.com)**

**TemplateFusion** is a powerful, modular toolkit for generating, managing, and sending email templates. It is designed to streamline the process of creating, customizing, and delivering HTML emails for a variety of use-cases, from automated alerts to marketing campaigns.

## Features

- **Web-based Email Template Generators:**  
  Create beautiful, responsive email templates through user-friendly web interfaces. No coding required—simply fill out a form and generate your desired email.

- **Multiple Generator Versions:**
  - **EmailGeneratorV1:**  
    The original, straightforward template generator for quick and simple email creation.
  - **EmailGeneratorV2:**  
    Enhanced with advanced template management, multiple pre-built templates (e.g., Account Suspension, Security Alert, Weekly Digest), and improved customization options.

- **Template Library:**  
  Access a comprehensive collection of ready-to-use HTML email templates for common scenarios like password resets, product spotlights, alerts, and more.

- **Seamless Email Sending with MailBird:**  
  Easily send generated emails to target users. Move the generated HTML into the `MailBird/mails/` folder and use the MailBird module to deliver emails directly from the command line.

- **Unified Main Script:**  
  Launch and manage all modules from a single entry point (`main.py` in the root directory).

---

## Directory Structure

```
TemplateFusion/
├── EmailGeneratorV1/
│   └── main.py
├── EmailGeneratorV2/
│   ├── main.py
│   └── templates/
│       ├── email_templates/
│       │   ├── Account Suspension.html
│       │   ├── Alert.html
│       │   ├── Email from admin.html
│       │   ├── Facebook DM.html
│       │   ├── Facebook Notice.html
│       │   ├── Instagram Warning.html
│       │   ├── Limited Time Offer.html
│       │   ├── Login Expired.html
│       │   ├── New Feature Update.html
│       │   ├── Password Reset Request.html
│       │   ├── Product Spotlight.html
│       │   ├── Security Alert.html
│       │   ├── Support Ticket.html
│       │   ├── Term Change Notification.html
│       │   ├── Update Required.html
│       │   ├── Verify Now.html
│       │   ├── Weekly Digest.html
│       │   ├── Welcom-Hero.html
│       │   └── invoice.html
│       ├── form.html
│       └── result.html
├── MailBird/
│   ├── mails/
│   │   └── example.html
│   └── main.py
└── main.py
```

---

## Usage Guide

1. **Run the Main Controller**

   In the root directory, launch the main controller script:

   ```bash
   python main.py
   ```

2. **Select a Tool**

   - The main controller will load and list all available modules (such as EmailGeneratorV1, EmailGeneratorV2, and MailBird) as tools.
   - You will be prompted to choose a tool to use (e.g., generate an email template or send an email).

3. **Follow the Interactive Prompts**

   - Once you select a tool, follow the on-screen prompts specific to that module:
     - For template generators, you will be guided to fill forms via a web interface (the script will provide the URL).
     - For MailBird, you will be guided to select an email HTML file and provide recipient details for sending.

4. **Workflow Example**

   - **To generate and send an email:**
     1. Start the main script and select EmailGeneratorV2.
     2. Use the web UI to create and download your email template.
     3. Place the generated HTML file in the `MailBird/mails/` directory.
     4. Restart the main script and select MailBird to send your email.

---

## Requirements

- Python 3.7+
- Flask (for web-based generators)
- Any additional dependencies listed in `requirements.txt` (if provided)

Install dependencies via:
```bash
pip install -r requirements.txt
```

---

## Customization

- **Add New Templates:**  
  Place your custom HTML templates in `EmailGeneratorV2/templates/email_templates/` to make them available in the generator.
- **Modify Forms:**  
  Update `form.html` in either generator directory to customize input fields.
- **Extend MailBird:**  
  Enhance sending logic, support attachments, or integrate with other email providers in `MailBird/main.py`.

---

## Contribution

Contributions and suggestions are welcome! Feel free to open issues or submit pull requests.

---

## Contact

- **Maintainer:** zerosocialcode
- **Email:** [zerosocialcode@gmail.com](mailto:zerosocialcode@gmail.com)

---

## License

[MIT License](LICENSE)  
(C) 2025 zerosocialcode
