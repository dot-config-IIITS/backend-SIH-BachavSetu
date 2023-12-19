import requests



response = requests.get('https://tathya.uidai.gov.in/generateCaptcha')
response.text()


json_data = {
    'uid': '597926744059',
    'captcha': 'HnIsG',
    'captchaTxnId': 'dSRDIe5a0JKA',
}

response = requests.post('https://tathya.uidai.gov.in/generateOTPForOAuth', json=json_data)
print(response.text())

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"uid":"597926744059","captcha":"HnIsG", "captchaTxnId":"dSRDIe5a0JKA"}'
#response = requests.post('https://tathya.uidai.gov.in/generateOTPForOAuth', cookies=cookies, headers=headers, data=data)