# Invoice PDF Generator

This project is a FastAPI-based web service for generating invoice PDFs dynamically. It uses ReportLab for PDF creation and Pydantic for data validation.

## Project Structure

```
invoice pdf/
├── main.py            # FastAPI app with endpoint to generate invoice PDFs
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
└── __pycache__/       # Python cache files (auto-generated)
```

## Features

## Project Setup

Follow these steps to set up and run the project:

1. **Clone the repository** (if not already):

```bash
git clone <your-repo-url>
cd "invoice pdf"
```

2. **(Optional) Create a virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the FastAPI server**:

```bash
uvicorn main:app --reload
```

5. **Test the API**:

- Use an API client (e.g., Postman, curl) to send a POST request to `http://127.0.0.1:8000/create-invoice/` with the required JSON body.
- The response will be a PDF invoice.

## Usage

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```
3. **Send a POST request** to `/create-invoice/` with invoice data. The response will be a PDF invoice.

## Example Request

```json
{
  "invoice_no": "INV-001",
  "customer_name": "John Doe",
  "items": [
    { "description": "Product A", "quantity": 2, "price": 10.0 },
    { "description": "Product B", "quantity": 1, "price": 20.0 }
  ]
}
```

## Dependencies

- fastapi
- uvicorn
- pydantic
- reportlab

See `requirements.txt` for the full list.

## License

MIT
