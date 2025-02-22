import requests
import json

def extract_att(text):
    query = text

    API_KEY = "AIzaSyDYAZzL4cQAaMAZRW916BV1BBKZpzNi1qM"  # Replace with your actual API key
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

    headers = {
        'Content-Type': 'application/json'
        # 'x-goog-api-key': API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            'Extract attributes from the following text and respond in JSON format: '
                            '{"location": null, "degree": null, "ielts": null, "toefl": null, "gre_required": false, '
                            '"gpa": null, "gre": null, "course": null, "method": null, "deadline": null, '
                            '"joint_degree": false, "combined_degree": false}. '
                            'Text: "%s".' % query
                        )
                    }
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, params={'key': API_KEY}, json=data)
    json_val = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    json_str = json_val.replace("```json", "").replace("```", "").strip()
        
        # Convert to a dictionary
    json_data = json.loads(json_str)
    return json_data