import requests

url = "http://127.0.0.1/api/warnings"

try:
    response = requests.get(url)
    response.raise_for_status()  # Ném lỗi nếu yêu cầu không thành công

    data = response.json()
    print(data)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
