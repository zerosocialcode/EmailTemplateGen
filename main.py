import os
from flask import Flask, render_template, request

app = Flask(__name__)

TEMPLATES_DIR = "email_templates"

def get_available_templates():
    folder = os.path.join(app.template_folder, TEMPLATES_DIR)
    # Only .html files, sorted alphabetically for user-friendliness
    return sorted([
        f[:-5] for f in os.listdir(folder)
        if f.endswith(".html") and not f.startswith("_")
    ])

@app.route('/', methods=['GET', 'POST'])
def index():
    available_templates = get_available_templates()
    if request.method == 'POST':
        data = {field: request.form.get(field, '') for field in [
            'subject', 'greeting', 'body', 'closing', 'signature', 'footer',
            'button_text', 'button_url', 'logo_url', 'font',
            'header_color', 'body_color', 'footer_color', 'button_color',
            'header_text_color', 'footer_text_color', 'button_text_color', 'text_color',
            'hero_url', 'accent_color'
        ]}
        template_name = request.form.get('template_style', available_templates[0])
        template_file = f"{TEMPLATES_DIR}/{template_name}.html"
        return render_template(template_file, **data, templates=available_templates, template_name=template_name)
    return render_template("form.html", templates=available_templates)

if __name__ == '__main__':
    app.run(debug=True)
