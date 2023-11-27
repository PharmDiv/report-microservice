import os
import re
import json
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Local module imports
from Report.report import create_report

from Subscriptions.Process_subscriptions.process import extract_reference_values


load_dotenv()
app = Flask(__name__)

DATA_SOURCE = os.getenv("data_source")
DATA_RECEIVER = os.getenv("data_reciever")
HEADERS = {"Content-Type": "application/json"}


@app.route('/Condition/<id>', methods=['PUT'])
def handle_condition_update(id):
    """
    Dynamic Route to receive resources from the FHIR server.
    """
    try:
        request_data = request.get_json()
        display_value = request_data.get("code", {}).get("coding", [{}])[0].get("display", "")
        plandefinition_response = requests.get(url=f'{DATA_SOURCE}/PlanDefinition')
        plandefinition_data = plandefinition_response.json()

        disease_expressions = [
            entry['resource']['action'][1]['action'][0]['condition'][0]['expression']['expression']
            for entry in plandefinition_data['entry']
        ]

        for disease_expr in disease_expressions:
            if re.search(rf'{re.escape(disease_expr)}', display_value, re.IGNORECASE):
                validated_data = request_data
                report_data = create_report(DATA_SOURCE, DATA_RECEIVER)
                report_data = json.loads(report_data)

                for ref_value in extract_reference_values(validated_data):
                    response = requests.get(url=f"{DATA_SOURCE}/{ref_value}")
                    resource_data = response.json()
                    report_data["entry"].append({"resource": resource_data})

                report_data["entry"].append({"resource": validated_data})
                report_response = requests.post(url=f"{DATA_RECEIVER}/Bundle", data=json.dumps(report_data), headers=HEADERS)
                return jsonify(report_response.json())
        else:
            return jsonify({"condition": "Not met"})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
