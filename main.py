from fastapi import FastAPI, Response
from pydantic import BaseModel
from reportlab.lib.pagesizes import A4 # type: ignore
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer # type: ignore
from reportlab.lib import colors # pyright: ignore[reportMissingModuleSource]
from reportlab.lib.styles import getSampleStyleSheet # type: ignore
from io import BytesIO
import datetime
import asyncio

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


def generate_pdf(invoice: InvoiceData) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    # Header
    elements.append(Paragraph(f"<b>Invoice #{invoice.invoice_no}</b>", styles["Title"]))
    elements.append(Paragraph(f"Customer: {invoice.customer_name}", styles["Normal"]))
    elements.append(Paragraph(f"Date: {datetime.date.today()}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Table data (header + rows)
    data = [["Description", "Quantity", "Price", "Total"]]
    total_amount = 0

    for item in invoice.items:
        line_total = item.quantity * item.price
        total_amount += line_total
        data.append([
            item.description,
            str(item.quantity),
            f"${item.price:.2f}",
            f"${line_total:.2f}",
        ])

    # Add grand total row
    data.append(["", "", "Grand Total:", f"${total_amount:.2f}"])

    # Create table
    table = Table(data, colWidths=[200, 80, 100, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -2), colors.beige),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTNAME", (-2, -1), (-1, -1), "Helvetica-Bold"),
    ]))

    elements.append(table)

    # Build PDF
    doc.build(elements)
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content


@app.post("/create-invoice/")
async def create_invoice(invoice: InvoiceData):
    pdf_content = await asyncio.to_thread(generate_pdf, invoice)
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename=invoice_{invoice.invoice_no}.pdf"}
    )
