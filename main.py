import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # Needed for session to work

TEMPLATES_DIR = "email_templates"

def get_available_templates():
    folder = os.path.join(app.template_folder, TEMPLATES_DIR)
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
        generated_html = render_template(template_file, **data)
        # Store in session and redirect
        session['generated_html'] = generated_html
        session['template_name'] = template_name
        return redirect(url_for('result'))
    return render_template("form.html", templates=available_templates)

@app.route('/result')
def result():
    generated_html = session.get('generated_html')
    template_name = session.get('template_name')
    if not generated_html:
        return redirect(url_for('index'))
    return render_template("result.html", generated_html=generated_html, template_name=template_name)

if __name__ == '__main__':
    app.run(debug=True)
