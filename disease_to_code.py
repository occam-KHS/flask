from flask import Flask, request, jsonify, render_template_string
import json
app = Flask(__name__)

# ICD-10 mapping table
# icd10_mapping = {
#     "E11": ["diabetes", "type 2 diabetes", "adult-onset diabetes"],
#     "I10": ["hypertension", "high blood pressure", "htn"],
#     "J45": ["asthma", "bronchial asthma"],
#     "U07.1": ["covid-19", "coronavirus", "sars-cov-2"],
# }

with open("tmr_icd10_aliases.json", "r", encoding="utf-8") as f:
    icd10_mapping = json.load(f)

# Flattened lookup for fast search
disease_to_code = {
    alias.lower(): code
    for code, aliases in icd10_mapping.items()
    for alias in aliases
}

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ICD-10 Lookup</title>
    </head>
    <body>
        <h2>ICD-10 Disease Code Lookup</h2>
        <input type="text" id="diseaseInput" placeholder="Enter disease name" />
        <button onclick="lookupCode()">Lookup</button>
        <p id="result"></p>

        <script>
            function lookupCode() {
                const disease = document.getElementById("diseaseInput").value;
                fetch("/get_icd10_code", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ disease: disease })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.icd10_code) {
                        document.getElementById("result").innerText = 
                            `"${data.disease}" → ICD-10 code is ${data.icd10_code}`;
                    } else {
                        document.getElementById("result").innerText = 
                            `No ICD-10 code found for "${data.disease}"`;
                    }
                });
            }
        </script>
    </body>
    </html>
    ''')

@app.route('/get_icd10_code', methods=['GET', 'POST'])
def get_icd10_code():
    disease = request.args.get('disease') if request.method == 'GET' else request.json.get('disease')

    if not disease:
        return jsonify({"error": "Missing 'disease' parameter"}), 400

    disease_lower = disease.lower()
    code = disease_to_code.get(disease_lower)

    if code:
        return jsonify({"disease": disease, "icd10_code": code})
    else:
        return jsonify({"disease": disease, "message": "No ICD-10 code found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
