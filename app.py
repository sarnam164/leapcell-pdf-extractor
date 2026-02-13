from flask import Flask, request, jsonify
import base64
import zipfile
import io

app = Flask(__name__)

@app.route('/extract-csv', methods=['POST'])
def extract_csv():
    try:
        data = request.json
        base64_zip = data.get('base64_zip')
        if not base64_zip:
            return jsonify({'error': 'No base64_zip data provided'}), 400

        zip_bytes = base64.b64decode(base64_zip)
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            # Find the first CSV file
            csv_file = next((name for name in z.namelist() if name.lower().endswith('.csv')), None)
            if not csv_file:
                return jsonify({'error': 'No CSV file found in ZIP'}), 400
            csv_bytes = z.read(csv_file)
            csv_b64 = base64.b64encode(csv_bytes).decode('utf-8')
            return jsonify({
                'filename': csv_file,
                'csv_base64': csv_b64
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)