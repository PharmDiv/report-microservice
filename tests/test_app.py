import os
import json
import sys
import pytest
from unittest.mock import patch
from flask import Flask, request, jsonify
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Subscriptions.Process_subscriptions.process import extract_reference_values
from app import app
from Report.report import create_report


@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_handle_condition_update_valid_condition(client):
    with patch('app.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'entry': [
                {
                    'resource': {
                        'action': [
                            {'action': [
                                {'condition': [
                                    {'expression': {'expression': 'covid'}}
                                ]}
                            ]}
                        ]
                    }
                }
            ]
        }
        mock_get.return_value.status_code = 200

        response = client.put('/Condition/123', json={
    "resourceType": "Condition",
    "id": "3606",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2023-09-21T01:00:25.827+00:00",
        "source": "#8641e359e4c35bb6"
    },
    "clinicalStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active",
                "display": "Active"
            }
        ]
    },
    "verificationStatus": {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": "confirmed",
                "display": "Confirmed"
            }
        ]
    },
    "category": [
        {
            "coding": [
                {
                    "code": "4373005",
                    "display": "Clubbing of nail"
                }
            ]
        }
    ],
    "severity": {
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "255604002",
                "display": "Mild"
            }
        ]
    },
    "code": {
        "coding": [
            {
                "display": "covid"
            }
        ]
    },
    "subject": {
        "reference": "Patient/2680"
    },
    "encounter": {
        "reference": "Encounter/2702"
    }
})

        print(response.status_code)
        print(response.get_json())

        assert response.status_code == 200
        #assert 'condition' in response.json

def test_handle_condition_update_invalid_condition(client):
    with patch('app.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'entry': [
                {
                    'resource': {
                        'action': [
                            {'action': [
                                {'condition': [
                                    {'expression': {'expression': 'SomeCondition'}}
                                ]}
                            ]}
                        ]
                    }
                }
            ]
        }
        mock_get.return_value.status_code = 200

        response = client.put('/Condition/123', json={'code': {'coding': [{'display': 'InvalidCondition'}]}})

        print(response.status_code)
        print(response.get_json())

        assert response.status_code == 200
        #assert 'condition' in response.json

def test_extract_reference_values_dict():
    data = {"reference": "value"}
    result = extract_reference_values(data)
    assert result == ["value"]

def test_extract_reference_values_nested_dict():
    data = {"key": {"reference": "value"}}
    result = extract_reference_values(data)
    assert result == ["value"]

def test_extract_reference_values_list():
    data = [{"reference": "value1"}, {"reference": "value2"}]
    result = extract_reference_values(data)
    assert result == ["value1", "value2"]

def test_extract_reference_values_nested_list():
    data = [{"key": {"reference": "value1"}}, {"key": {"reference": "value2"}}]
    result = extract_reference_values(data)
    assert result == ["value1", "value2"]

def test_extract_reference_values_mixed():
    data = {"reference": "value1", "key": [{"reference": "value2"}]}
    result = extract_reference_values(data)
    assert result == ["value1", "value2"]

def test_extract_reference_values_no_reference():
    data = {"key": "value"}
    result = extract_reference_values(data)
    assert result == []

def test_extract_reference_values_empty_input():
    data = None
    result = extract_reference_values(data)
    assert result == []



#def test_create_report():
#    # Define placeholder values for endpoints
#    source_endpoint = "http://example.com/source"
#    destination_endpoint = "http://example.com/destination"
#
#    # Call the function to generate the FHIR Bundle
#    with patch('your_module_name.date') as mock_date:
#        mock_date.today.return_value = date(2023, 1, 1)  # Mock the date to a fixed value for consistency
#
#        generated_bundle = create_report(source_endpoint, destination_endpoint)
#
#    # Convert the expected structure to a Python dictionary
#    expected_bundle = {
#        "resourceType": "Bundle",
#        # ... add other expected keys and values based on the function logic
#    }
#
#    # Convert the generated JSON to a Python dictionary
#    generated_bundle_dict = json.loads(generated_bundle)
#
#    # Assert that the generated bundle matches the expected structure
#    assert generated_bundle_dict == expected_bundle

