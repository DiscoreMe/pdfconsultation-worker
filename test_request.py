import requests

data = {
    "config": open("data.json", 'rb').read(),
    "test_form.pdf": open("test_form.pdf", 'rb').read()
}

response = requests.post("http://127.0.0.1:5000", files=data)

if response.status_code == 200:
    with open("testdownload.tar", 'wb') as f:
        f.write(response.content)
else:
    print("Invalid status code")