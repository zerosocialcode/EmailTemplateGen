from flask import (
    Flask,
    render_template_string,
    request,
    send_file,
    flash,
    redirect,
    url_for,
    get_flashed_messages,
)
import io
import re
import html
import urllib.parse
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "enterprise-email-gen-secret"


def reverse_url(url: str) -> str:
    """Reverse URL and escape special characters for display."""
    return html.escape(url)[::-1]


def validate_color(color: str) -> bool:
    """Validate hex color format."""
    return bool(re.match(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", color))


def sanitize_url(url: str, fallback="https://example.com") -> str:
    """Basic URL validation and fallback."""
    try:
        parts = urllib.parse.urlparse(url.strip())
        if parts.scheme in {"http", "https"} and parts.netloc:
            return url
    except Exception:
        pass
    return fallback


def safe_filename(brand_name: str) -> str:
    """Create a safe filename for download."""
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", brand_name.strip()).strip("-").lower()
    return secure_filename(cleaned or "email") + "_security_email.html"


def get_field(form, name: str, default="") -> str:
    """Get field from form, trimming and stripping."""
    return (form.get(name) or default).strip()


def get_required_fields(form, fields):
    """Return missing required fields."""
    return [f for f in fields if not get_field(form, f)]


def escape_and_nl(text: str) -> str:
    """Escape and convert newlines to <br>."""
    return html.escape(text).replace("\n", "<br>")


def flash_form_errors(errors):
    for field in errors:
        flash(f"Missing required field: {field}", "error")


TEMPLATE_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enterprise Email Generator</title>
  <style>
    :root {
      --primary: #2563eb;
      --primary-dark: #1d4ed8;
      --secondary: #64748b;
      --light: #f8fafc;
      --dark: #0f172a;
      --border: #e2e8f0;
      --success: #10b981;
      --error: #ef4444;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
      color: var(--dark);
      min-height: 100vh;
      padding: 40px 0;
      line-height: 1.6;
    }
    .container {
      max-width: 900px;
      margin: 0 auto;
      padding: 0 10px;
    }
    header {
      text-align: center;
      margin-bottom: 40px;
    }
    header h1 {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 10px;
      background: linear-gradient(90deg, var(--primary), var(--primary-dark));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }
    header p {
      color: var(--secondary);
      font-size: 1.1rem;
      max-width: 600px;
      margin: 0 auto;
    }
    .card {
      background: white;
      border-radius: 16px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
      overflow: hidden;
    }
    .card-header {
      background: linear-gradient(90deg, var(--primary), var(--primary-dark));
      color: white;
      padding: 25px 30px;
    }
    .card-header h2 {
      font-size: 1.8rem;
      font-weight: 600;
    }
    .card-body {
      padding: 30px;
    }
    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 25px;
    }
    .form-group {
      margin-bottom: 20px;
    }
    .form-group label {
      display: block;
      font-weight: 600;
      margin-bottom: 8px;
      color: var(--dark);
      font-size: 0.95rem;
    }
    .form-control {
      width: 100%;
      padding: 14px 16px;
      border: 1px solid var(--border);
      border-radius: 10px;
      font-size: 1rem;
      transition: all 0.2s ease;
      background-color: #f8fafc;
    }
    .form-control:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
      background-color: white;
    }
    textarea.form-control {
      min-height: 120px;
      resize: vertical;
    }
    .form-footer {
      border-top: 1px solid var(--border);
      padding: 25px 30px;
      background-color: #f8fafc;
      text-align: center;
    }
    .btn {
      display: inline-block;
      padding: 16px 32px;
      background: linear-gradient(90deg, var(--primary), var(--primary-dark));
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 1.1rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .error-message {
      color: var(--error);
      font-size: 0.85rem;
      margin-top: 6px;
      display: none;
    }
    .form-group.invalid .error-message {
      display: block;
    }
    .form-group.invalid .form-control {
      border-color: var(--error);
    }
    .form-group.valid .form-control {
      border-color: var(--success);
    }
    .color-preview {
      width: 30px;
      height: 30px;
      border-radius: 6px;
      display: inline-block;
      vertical-align: middle;
      margin-left: 12px;
      border: 1px solid var(--border);
    }
    .section-title {
      font-size: 1.2rem;
      font-weight: 600;
      color: var(--primary);
      padding-bottom: 8px;
      border-bottom: 2px solid var(--border);
      margin: 35px 0 20px;
      grid-column: 1 / -1;
    }
    .notification {
      padding: 15px;
      border-radius: 10px;
      margin-bottom: 25px;
      background-color: #fffbeb;
      border-left: 4px solid #f59e0b;
      color: #92400e;
      grid-column: 1 / -1;
    }
    .flask-messages {
      margin: 0 0 20px 0;
      padding: 0;
      list-style: none;
      grid-column: 1 / -1;
    }
    .flask-messages li {
      margin-bottom: 10px;
      padding: 10px;
      border-radius: 6px;
      background: #fee2e2;
      color: #b91c1c;
      font-weight: 500;
      border-left: 4px solid #ef4444;
    }
    @media (max-width: 900px) {
      .container { padding: 0 6px; }
      .card-body { padding: 20px; }
      .form-grid { gap: 15px; }
    }
    @media (max-width: 600px) {
      .container { max-width: 100vw; padding: 0 2px; }
      header h1 { font-size: 1.55rem; }
      .card-header, .form-footer { padding: 16px 8px; }
      .card { border-radius: 0; }
      .card-body { padding: 8px; }
      .form-grid { grid-template-columns: 1fr; gap: 8px; }
      .section-title { margin: 18px 0 8px 0; font-size: 1rem; }
      .btn { width: 100%; padding: 14px; font-size: 1rem; }
      .form-group { margin-bottom: 10px; }
      .color-preview { width: 22px; height: 22px; margin-left: 6px; }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Enterprise Email Generator</h1>
      <p>Create professional, multipart email templates with advanced customization options</p>
    </header>
    <div class="card">
      <div class="card-header">
        <h2>Template Configuration</h2>
      </div>
      <form method="POST" id="emailForm" autocomplete="off">
        <div class="card-body">
          {% if messages %}
            <ul class="flask-messages">
              {% for category, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
              {% endfor %}
            </ul>
          {% endif %}
          <div class="notification">
            <strong>Note:</strong> This tool is for authorized educational and testing purposes only
          </div>
          <div class="form-grid">
            <div class="section-title">Brand Identity</div>
            <div class="form-group">
              <label for="brand_name">Brand/Company Name *</label>
              <input type="text" class="form-control" name="brand_name" id="brand_name" required>
              <div class="error-message">Please enter a brand name</div>
            </div>
            <div class="form-group">
              <label for="brand_logo">Brand Logo URL *</label>
              <input type="url" class="form-control" name="brand_logo" id="brand_logo" required>
              <div class="error-message">Please enter a valid URL</div>
            </div>
            <div class="form-group">
              <label for="brand_website">Company Website URL</label>
              <input type="url" class="form-control" name="brand_website" id="brand_website">
            </div>
            <div class="form-group">
              <label for="brand_color">Primary Brand Color (HEX) *</label>
              <div>
                <input type="text" class="form-control" name="brand_color" id="brand_color" 
                       value="#2563eb" required pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$">
                <span class="color-preview" id="colorPreview"></span>
              </div>
              <div class="error-message">Invalid color format (e.g. #2563eb)</div>
            </div>
            <div class="section-title">Email Content</div>
            <div class="form-group">
              <label for="email_title">Email Title/Subject *</label>
              <input type="text" class="form-control" name="email_title" id="email_title" required>
              <div class="error-message">Please enter an email title</div>
            </div>
            <div class="form-group" style="grid-column: span 2;">
              <label for="preheader">Preheader Text</label>
              <input type="text" class="form-control" name="preheader" id="preheader" 
                     placeholder="This text appears in email previews">
            </div>
            <div class="form-group" style="grid-column: span 2;">
              <label for="email_message">Main Message *</label>
              <textarea class="form-control" name="email_message" id="email_message" required></textarea>
              <div class="error-message">Please enter your message content</div>
            </div>
            <div class="form-group">
              <label for="button_text">Call-to-Action Text *</label>
              <input type="text" class="form-control" name="button_text" id="button_text" 
                     value="Verify Account" required>
            </div>
            <div class="form-group">
              <label for="malicious_link">Action URL *</label>
              <input type="url" class="form-control" name="malicious_link" id="malicious_link" required>
              <div class="error-message">Please enter a valid URL</div>
            </div>
            <div class="section-title">Security Elements</div>
            <div class="form-group">
              <label for="status_icon">Verification Icon URL</label>
              <input type="url" class="form-control" name="status_icon" id="status_icon"
                     placeholder="https://example.com/verified-icon.png">
            </div>
            <div class="form-group">
              <label for="legit_url">Legitimate URL (for reversal) *</label>
              <input type="url" class="form-control" name="legit_url" id="legit_url" required>
              <div class="error-message">Please enter a valid URL</div>
            </div>
            <div class="form-group">
              <label for="include_tracking">Include Tracking Pixel?</label>
              <select class="form-control" name="include_tracking" id="include_tracking">
                <option value="yes">Yes</option>
                <option value="no" selected>No</option>
              </select>
            </div>
            <div class="form-group">
              <label for="sender_name">Sender Name</label>
              <input type="text" class="form-control" name="sender_name" id="sender_name" 
                     value="Security Team">
            </div>
            <div class="section-title">Recipient & Support</div>
            <div class="form-group">
              <label for="recipient_email">Recipient Email (footer) *</label>
              <input type="email" class="form-control" name="recipient_email" id="recipient_email" value="example@example.com" required>
              <div class="error-message">Please provide a valid email address (for footer)</div>
            </div>
            <div class="form-group">
              <label for="support_email">Support Email (footer) *</label>
              <input type="email" class="form-control" name="support_email" id="support_email" value="support@example.com" required>
              <div class="error-message">Please provide a valid support email address</div>
            </div>
          </div>
        </div>
        <div class="form-footer">
          <button type="submit" class="btn">Generate Professional Email Template</button>
        </div>
      </form>
    </div>
  </div>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      const form = document.getElementById('emailForm');
      const colorInput = document.getElementById('brand_color');
      const colorPreview = document.getElementById('colorPreview');
      colorPreview.style.backgroundColor = colorInput.value;
      colorInput.addEventListener('input', function() {
        colorPreview.style.backgroundColor = this.value;
      });
      form.addEventListener('submit', function(e) {
        let valid = true;
        const required = form.querySelectorAll('[required]');
        required.forEach(field => {
          const group = field.closest('.form-group');
          if (!field.value.trim()) {
            group.classList.add('invalid');
            valid = false;
          } else {
            group.classList.remove('invalid');
            if (field.type === 'url') {
              try {
                new URL(field.value);
                group.classList.remove('invalid');
              } catch {
                group.classList.add('invalid');
                valid = false;
              }
            }
            if (field.type === 'email') {
              const emailPattern = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
              if (!emailPattern.test(field.value)) {
                group.classList.add('invalid');
                valid = false;
              }
            }
          }
        });
        const colorGroup = colorInput.closest('.form-group');
        if (!/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(colorInput.value)) {
          colorGroup.classList.add('invalid');
          valid = false;
        } else {
          colorGroup.classList.remove('invalid');
        }
        if (!valid) {
          e.preventDefault();
          alert('Please fix the errors in the form');
        }
      });
    });
  </script>
</body>
</html>
'''


def generate_premium_email(data: dict) -> str:
    """Generate sophisticated multipart email HTML."""
    current_year = datetime.now().year

    # Escape all user inputs
    brand_name = html.escape(data["brand_name"])
    brand_logo = sanitize_url(data["brand_logo"])
    brand_website = sanitize_url(data.get("brand_website", "#"), "#")
    brand_color = data["brand_color"] if validate_color(data["brand_color"]) else "#2563eb"
    email_title = html.escape(data["email_title"])
    preheader = html.escape(data.get("preheader", ""))
    email_message = escape_and_nl(data["email_message"])
    button_text = html.escape(data["button_text"])
    status_icon = sanitize_url(data.get("status_icon", ""))
    malicious_link = sanitize_url(data["malicious_link"])
    legit_url = sanitize_url(data["legit_url"])
    sender_name = html.escape(data.get("sender_name", "Security Team"))
    recipient_email = html.escape(data.get("recipient_email", "example@example.com"))
    support_email = html.escape(data.get("support_email", "support@example.com"))

    tracking_pixel = ""
    if data.get("include_tracking", "no") == "yes":
        tracking_pixel = f"""<img src="https://tracking.example.com/pixel?ref={urllib.parse.quote_plus(data['brand_name'])}" 
              width="1" height="1" style="display:none" alt="tracking pixel">"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{email_title}</title>
  <style>
    @media only screen and (max-width: 600px) {{
      .container {{
        width: 100% !important;
      }}
      .header {{
        padding: 20px 15px !important;
      }}
      .content {{
        padding: 25px 15px !important;
      }}
      .footer {{
        padding: 20px 15px !important;
      }}
      .footer-columns {{
        display: block !important;
      }}
      .footer-column {{
        display: block !important;
        width: 100% !important;
        padding: 0 !important;
        margin-bottom: 20px !important;
      }}
    }}
  </style>
</head>
<body style="margin:0; padding:0; background-color:#f3f4f6; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;">
  <div style="display:none; max-height:0; overflow:hidden;">
    {preheader if preheader else 'Important security notification from ' + brand_name}
  </div>
  <table width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#f3f4f6">
    <tr>
      <td align="center">
        <table class="container" width="600" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff" style="border-radius:12px; overflow:hidden; margin:30px auto; box-shadow:0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.02);">
          <tr>
            <td class="header" bgcolor="{brand_color}" style="padding:30px; text-align:center; background: linear-gradient(135deg, {brand_color} 0%, {brand_color} 100%);">
              <a href="{brand_website}" target="_blank">
                <img src="{brand_logo}" alt="{brand_name}" width="120" style="max-width:100%; height:auto; display:block; margin:0 auto 20px;">
              </a>
              {f'<img src="{status_icon}" alt="Verified" width="40" style="margin-bottom:15px;">' if status_icon else ''}
              <h1 style="color:#ffffff; font-size:28px; font-weight:600; margin:0;">{email_title}</h1>
            </td>
          </tr>
          <tr>
            <td class="content" style="padding:40px 30px; color:#334155; font-size:16px; line-height:1.6;">
              <p style="margin-top:0; margin-bottom:25px;">{email_message}</p>
              <table width="100%" cellspacing="0" cellpadding="0" style="margin:35px 0;">
                <tr>
                  <td align="center">
                    <a href="{malicious_link}" style="display:inline-block; padding:16px 40px; background-color:{brand_color}; color:#ffffff; text-decoration:none; border-radius:8px; font-weight:600; font-size:16px; box-shadow:0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.05);">
                      {button_text}
                    </a>
                  </td>
                </tr>
              </table>
              <table width="100%" cellspacing="0" cellpadding="0" style="background-color:#f8fafc; border-radius:10px; padding:25px; margin:30px 0;">
                <tr>
                  <td>
                    <h3 style="font-size:18px; margin-top:0; margin-bottom:15px; color:{brand_color};">Important Security Notice</h3>
                    <p style="margin:0;">For your protection, never share your password or security codes with anyone. {brand_name} will never ask for this information via email.</p>
                  </td>
                </tr>
              </table>
              <p style="margin-bottom:0;">If you have any questions, please contact our support team at <a href="mailto:{support_email}" style="color:{brand_color};">{support_email}</a></p>
              <p style="margin:5px 0 0;">Sincerely,<br>{sender_name}<br>{brand_name} Security</p>
            </td>
          </tr>
          <tr>
            <td class="footer" bgcolor="#0f172a" style="padding:40px 30px; color:#cbd5e1; font-size:14px;">
              <table class="footer-columns" width="100%" cellspacing="0" cellpadding="0" style="display:table;">
                <tr>
                  <td class="footer-column" width="60%" style="display:table-cell; vertical-align:top; padding-right:20px;">
                    <h3 style="color:#ffffff; font-size:16px; margin-top:0; margin-bottom:15px;">About {brand_name}</h3>
                    <p style="margin:0 0 20px;">{brand_name} provides industry-leading security solutions to protect your digital assets and identity. Trusted by millions worldwide.</p>
                    <p style="margin:0;">&copy; {current_year} {brand_name}. All rights reserved.</p>
                  </td>
                  <td class="footer-column" width="40%" style="display:table-cell; vertical-align:top;">
                    <h3 style="color:#ffffff; font-size:16px; margin-top:0; margin-bottom:15px;">Quick Links</h3>
                    <ul style="margin:0; padding:0; list-style:none;">
                      <li style="margin-bottom:10px;"><a href="{brand_website}/security" style="color:#cbd5e1; text-decoration:none;">Security Center</a></li>
                      <li style="margin-bottom:10px;"><a href="{brand_website}/support" style="color:#cbd5e1; text-decoration:none;">Support</a></li>
                      <li style="margin-bottom:10px;"><a href="{brand_website}/privacy" style="color:#cbd5e1; text-decoration:none;">Privacy Policy</a></li>
                      <li><a href="{brand_website}/unsubscribe" style="color:#cbd5e1; text-decoration:none;">Unsubscribe</a></li>
                    </ul>
                  </td>
                </tr>
              </table>
              <table width="100%" cellspacing="0" cellpadding="0" style="margin-top:30px; border-top:1px solid #334155; padding-top:20px;">
                <tr>
                  <td align="center">
                    <p style="margin:0 0 15px; font-size:13px;">
                      This email was sent to {recipient_email} because you have an account with {brand_name}
                    </p>
                    <p style="margin:0 0 15px; font-size:13px;">
                      Please do not reply to this message. Emails sent to this address will not be answered.
                    </p>
                    <p style="margin:0; font-size:13px; color:#94a3b8;">
                      <span style="unicode-bidi:bidi-override; direction:rtl;">{reverse_url(legit_url)}</span>
                    </p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
  {tracking_pixel}
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        required_fields = [
            "brand_name",
            "brand_logo",
            "email_title",
            "email_message",
            "button_text",
            "malicious_link",
            "legit_url",
            "brand_color",
            "recipient_email",
            "support_email",
        ]
        errors = get_required_fields(request.form, required_fields)
        if errors:
            flash_form_errors(errors)
            return redirect(url_for("form"))
        if not validate_color(request.form["brand_color"]):
            flash("Invalid color format. Use hex format like #FFFFFF", "error")
            return redirect(url_for("form"))
        recipient_email = get_field(request.form, "recipient_email")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", recipient_email):
            flash("Please provide a valid recipient email address.", "error")
            return redirect(url_for("form"))
        support_email = get_field(request.form, "support_email")
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", support_email):
            flash("Please provide a valid support email address.", "error")
            return redirect(url_for("form"))

        # Gather and sanitize data
        data = {k: get_field(request.form, k) for k in request.form.keys()}
        data.setdefault("brand_website", "https://example.com")
        data.setdefault("sender_name", "Security Team")
        data.setdefault("recipient_email", "example@example.com")
        data.setdefault("support_email", "support@example.com")

        try:
            html_content = generate_premium_email(data)
            filename = safe_filename(data["brand_name"])
            response = send_file(
                io.BytesIO(html_content.encode("utf-8")),
                mimetype="text/html",
                as_attachment=True,
                download_name=filename,
            )
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers[
                "Content-Security-Policy"
            ] = "default-src 'none'; style-src 'unsafe-inline'; img-src *; font-src *;"
            return response
        except Exception as e:
            flash(f"Error generating template: {str(e)}", "error")
            return redirect(url_for("form"))

    messages = get_flashed_messages(with_categories=True)
    return render_template_string(TEMPLATE_FORM, messages=messages)


if __name__ == "__main__":
    app.run(debug=False)
