"""
app.py
======
FastAPI backend for GovForm Automator.

No database. No authentication. No login. Runs fully locally.
Exposes REST endpoints that the React frontend uses to list available
forms and to generate a filled Form 93 PDF from the original government
template.
"""

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
#from fastapi.responses import FileResponse
from pydantic import ValidationError

from schemas import Form93Data, FormDescriptor
#from schemas import Form93Data, GenerateResponse, FormDescriptor
from pdf_generator import generate_pdf, PDFGenerationError
#from pdf_generator import generate_pdf, PDFGenerationError, OUTPUT_DIR

app = FastAPI(
    title="GovForm Automator",
    description="Local application that fills Government Form 93 (PAN application) "
    "using the original PDF template.",
    version="1.0.0",
)

# Allow the local Vite dev server (and any local origin) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

SUPPORTED_FORMS = [
    FormDescriptor(
        id="form93",
        name="Form No. 93",
        description="Application for Allotment of Permanent Account Number "
        "(PAN) for an Individual being a Citizen of India.",
        pages=2,
    )
]


@app.get("/")
def root():
    return {
        "app": "GovForm Automator",
        "status": "running",
        "supported_forms": [f.id for f in SUPPORTED_FORMS],
    }


@app.get("/forms", response_model=list[FormDescriptor])
def list_forms():
    return SUPPORTED_FORMS


'''@app.post("/generate", response_model=GenerateResponse)
def generate(payload: Form93Data):
    try:
        filename = generate_pdf(payload)
    except PDFGenerationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    return GenerateResponse(
        success=True,
        filename=filename,
        download_url=f"/download/{filename}",
        message="Form 93 PDF generated successfully.",
    )'''

@app.post("/generate")
def generate(payload: Form93Data):
    try:
        pdf_buffer = generate_pdf(payload)
    except PDFGenerationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors()) from exc

    filename = f"{payload.first_name}_{payload.last_name}_new_pan_application.pdf"

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )
'''
@app.get("/download/{filename}")
def download(filename: str):
    # Prevent path traversal -- only allow plain filenames we generated.
    safe_name = os.path.basename(filename)
    file_path = os.path.join(OUTPUT_DIR, safe_name)

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=safe_name,
    )
'''

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
