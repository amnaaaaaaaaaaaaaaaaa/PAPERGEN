from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def build_pdf(df, metadata, output_path="output/question_paper.pdf"):
    """Build a simple question paper PDF."""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, height-50, metadata.get("school_name", "SCHOOL NAME"))
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, height-70, metadata.get("exam_title", "Exam Title"))

    # Metadata
    c.setFont("Helvetica", 10)
    c.drawString(50, height-100, f"Class: {metadata.get('class_name', 'XII')}")
    c.drawString(200, height-100, f"Max Marks: {metadata.get('max_marks', 70)}")
    c.drawString(350, height-100, f"Date: {metadata.get('date_str', '')}")
    c.drawString(50, height-115, f"Time: {metadata.get('time_allowed', '3 Hours')}")

    # Questions
    y = height - 150
    qno = 1
    for _, row in df.iterrows():
        text = f"Q{qno} ({row['marks']} marks): {row['question_text']}"
        c.setFont("Helvetica", 11)

        # Wrap text to fit the page
        max_width = width - 100
        wrapped = []
        line = ""
        for word in text.split():
            if c.stringWidth(line + word + " ", "Helvetica", 11) <= max_width:
                line += word + " "
            else:
                wrapped.append(line.strip())
                line = word + " "
        wrapped.append(line.strip())

        for l in wrapped:
            if y < 100:
                c.showPage()
                y = height - 100
                c.setFont("Helvetica", 11)
            c.drawString(50, y, l)
            y -= 18

        qno += 1
        y -= 10

    c.save()
    return output_path
