from fastapi import FastAPI, Response
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime

app = FastAPI()

# Request body schema
class InvoiceItem(BaseModel):
    description: str
    quantity: int
    price: float

class InvoiceData(BaseModel):
    invoice_no: str
    customer_name: str
    items: list[InvoiceItem]

# API endpoint to create invoice PDF
@app.post("/create-invoice/")
def create_invoice(invoice: InvoiceData):
    # Create PDF in memory
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Invoice #{invoice.invoice_no}")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Customer: {invoice.customer_name}")
    c.drawString(50, height - 100, f"Date: {datetime.date.today()}")

    # Table header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 140, "Description")
    c.drawString(300, height - 140, "Quantity")
    c.drawString(400, height - 140, "Price")
    c.drawString(500, height - 140, "Total")

    # Table rows
    y = height - 160
    total_amount = 0
    c.setFont("Helvetica", 12)

    for item in invoice.items:
        line_total = item.quantity * item.price
        total_amount += line_total

        c.drawString(50, y, item.description)
        c.drawString(300, y, str(item.quantity))
        c.drawString(400, y, f"${item.price:.2f}")
        c.drawString(500, y, f"${line_total:.2f}")
        y -= 20

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y - 20, "Grand Total:")
    c.drawString(500, y - 20, f"${total_amount:.2f}")

    c.showPage()
    c.save()

    buffer.seek(0)
    pdf_content = buffer.getvalue()
    buffer.close()

    return Response(content=pdf_content, media_type="application/pdf")
