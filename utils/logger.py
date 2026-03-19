import json
import os
from datetime import datetime
from fpdf import FPDF

def save_chat_to_file(role, content, user_email):
    """
    Saves chat messages to a unique file for each user.
    """
    filename = f"logs_{user_email.replace('@', '_').replace('.', '_')}.json"
    
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "content": content
    }
    
    data = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(log_entry)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def export_log_to_pdf(user_email):
    """Converts the user's JSON log into a professional PDF byte stream."""
    user_slug = user_email.replace('@', '_').replace('.', '_')
    json_filename = f"logs_{user_slug}.json"
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"VC Analyst AI: Research Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"User: {user_email}", ln=True, align='C')
    pdf.ln(10)

    if os.path.exists(json_filename):
        with open(json_filename, "r") as f:
            logs = json.load(f)
            for entry in logs:
                pdf.set_font("Arial", 'B', 10)
                pdf.multi_cell(0, 5, txt=f"[{entry['timestamp']}] {entry['role'].upper()}:")
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, txt=entry['content'])
                pdf.ln(5)
    
    
    return pdf.output(dest='S').encode('latin-1')



def load_chat_history(user_email):
    """Reads the user's specific JSON log and returns it for the UI."""
    user_slug = user_email.replace('@', '_').replace('.', '_')
    filename = f"logs_{user_slug}.json"
    
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []