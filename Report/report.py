import json
from datetime import date

def create_report(source_endpoint, destination_endpoint):    
    # Define variables with the values you want to include
    timestamp = str(date.today())
    destination_endpoint = destination_endpoint
    sender_reference = "LAFIA"
    source_name = "Healthcare Organization"
    source_contact_system = "phone"
    source_contact_value = "+1 (917) 123 4567"
    source_endpoint = source_endpoint
    reason_code = "encounter-end"
    focus_reference = "Bundle/content-bundle-example"

    
    # Create the JSON structure
    message_bundle = {
        "resourceType": "Bundle",
        "meta": {  
            "profile": ["http://hl7.org/fhir/us/medmorph/StructureDefinition/us-ph-reporting-bundle"]
        },
        "type": "message",
        "timestamp": timestamp,
        "entry": [
            {
                "resource": {
                    "resourceType": "MessageHeader",
                    "meta": {
                        "versionId": "1",
                        "lastUpdated": timestamp,
                        "profile": ["http://hl7.org/fhir/us/medmorph/StructureDefinition/us-ph-messageheader"]
                    },
                    "text": {
                        "status": "generated",
                        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">\n<p>Reporting Data</p> \n</div>"
                    },
                    "extension": [
                        {
                            "url": "http://hl7.org/fhir/us/medmorph/StructureDefinition/us-ph-data-encrypted-extension",
                            "valueBoolean": False
                        },
                        {
                            "url": "http://hl7.org/fhir/us/medmorph/StructureDefinition/us-ph-report-initiation-type",
                            "valueCodeableConcept": {
                                "coding": [
                                    {
                                        "system": "http://hl7.org/fhir/us/medmorph/CodeSystem/us-ph-report-initiation-types",
                                        "code": "subscription-notification"
                                    }
                                ]
                            }
                        }
                    ],
                    "eventCoding": {
                        "system": "http://hl7.org/fhir/us/medmorph/CodeSystem/us-ph-messageheader-message-types",
                        "code": "covid-report-message"
                    },
                    "destination": [
                        {
                            "name": "PHA endpoint",
                            "endpoint": destination_endpoint
                        }
                    ],
                    "sender": {
                        "reference": sender_reference
                    },
                    "source": {
                        "name": source_name,
                        "contact": {
                            "system": source_contact_system,
                            "value": source_contact_value
                        },
                        "endpoint": source_endpoint
                    },
                    "reason": {
                        "coding": [
                            {
                                "system": "http://hl7.org/fhir/us/medmorph/CodeSystem/us-ph-triggerdefinition-namedevents",
                                "code": reason_code
                            }
                        ]
                    },
                    "focus": [
                        {
                            "reference": focus_reference
                        }
                    ]
                }
            },
            {
                "resource": {
                    "resourceType": "Bundle",
                    "id": "content-bundle-example",
                    "meta": {
                        "versionId": "1",
                        "lastUpdated": "2020-11-29T02:03:28.045+00:00",
                        "profile": ["http://hl7.org/fhir/us/medmorph/StructureDefinition/us-ph-content-bundle"]
                    },
                    "type": "collection",
                    "timestamp": timestamp,
                    "entry": []
                }
            }
        ]
    }
    
    # Convert the Python dictionary to JSON format
    return json.dumps(message_bundle, indent=2)

