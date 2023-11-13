from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import black
from reportlab.pdfgen import canvas
import io

def read():
    reader = PdfReader("source.pdf")
    text = ""

    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()

    return replace_ligatures(text)

def write(text):
    words = text.split()
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    x_pos = 100
    y_pos = 750

    font = 'Courier'
    bold = "Courier-Bold"
    font_size = 12

    for word in words:
        half_len = len(word) // 2
        first_half = word[:half_len]
        second_half = word[half_len:]

        c.setFont(bold, font_size)
        c.drawString(x_pos, y_pos, first_half)
        x_pos += c.stringWidth(first_half, bold, font_size)

        c.setFont(font, font_size)
        c.drawString(x_pos, y_pos, second_half)
        x_pos += c.stringWidth(second_half, font, font_size) + 5

        if x_pos > 500:
            x_pos = 100
            y_pos -= font_size + 5

    c.save()

    packet.seek(0)

    with open('output.pdf', 'wb') as f:
        f.write(packet.getvalue())

    print("New PDF saved as output.pdf")


def replace_ligatures(text):
    ligature_map = {
        'ﬀ': 'ff',
        'ﬁ': 'fi',
        'ﬂ': 'fl',
        'ﬃ': 'ffi',
        'ﬄ': 'ffl',
        'œ': 'oe',
        'æ': 'ae'
    }

    for ligature, replacement in ligature_map.items():
        text = text.replace(ligature, replacement)

    return text