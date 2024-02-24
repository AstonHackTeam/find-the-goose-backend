import requests

def upload_file(url: str, file_path: str):
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'audio/wav')}
        response = requests.post(url, files=files)
        return response

def main():
    file_path = 'test1.wav'  # 确保这个文件在你的脚本运行目录下
    url = "http://localhost:8000/upload"  # 修改为你的 FastAPI 应用的 URL

    print(f"Uploading {file_path} to {url}")
    response = upload_file(url, file_path)
    if response.status_code == 200:
        print("Upload successful!")
        print("Response:", response.json())
    else:
        print(f"Upload failed with status code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    main()
