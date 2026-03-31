import io
import docx
import pdfplumber

def extract_text_from_pdf(file_obj):
    text = ""
    try:
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_docx(file_obj):
    text = ""
    try:
        doc = docx.Document(file_obj)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX: {e}")
    return text

def extract_text(file_obj, filename):
    if filename.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_obj)
    elif filename.lower().endswith('.docx'):
        return extract_text_from_docx(file_obj)
    else:
        # Fallback for plain text files or unsupported formats
        try:
            return file_obj.read().decode('utf-8')
        except:
            return ""