# Leapcell PDF Extractor

Minimal Flask API to extract a PDF from a base64-encoded zip file.

- POST /extract-pdf
  - Request: { "base64_zip": "<yourString>" }
  - Response: { "filename": "...", "pdf_base64": "..." }