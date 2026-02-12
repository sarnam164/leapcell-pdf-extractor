from flask import Flask, request, jsonify
import base64
import zipfile
import io

app = Flask(__name__)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    try:
        data = request.json
        base64_zip = data.get('base64_zip')
        if not base64_zip:
            return jsonify({'error': 'No base64_zip data provided'}), 400

        zip_bytes = base64.b64decode(base64_zip)
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            pdf_file = next((name for name in z.namelist() if name.lower().endswith('.pdf')), None)
            if not pdf_file:
                return jsonify({'error': 'No PDF file found in ZIP'}), 400
            pdf_bytes = z.read(pdf_file)
            pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')
            return jsonify({
                'filename': pdf_file,
                'pdf_base64': pdf_b64
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)