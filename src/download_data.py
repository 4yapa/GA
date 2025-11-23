"""
Helper script to download Reddit tariffs dataset from Google Drive
"""

import os
import sys


def download_from_google_drive(file_id: str, output_path: str):
    """
    Download file from Google Drive

    Args:
        file_id: Google Drive file ID
        output_path: Local path to save the file
    """
    import requests

    print(f"Downloading file from Google Drive...")
    print(f"File ID: {file_id}")
    print(f"Output path: {output_path}")

    # Google Drive download URL
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, output_path)
    print(f"✓ File downloaded successfully to {output_path}")


def get_confirm_token(response):
    """Extract confirmation token from response cookies"""
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, output_path):
    """Save response content to file"""
    CHUNK_SIZE = 32768

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)


def main():
    """Main function"""

    # Google Drive file ID from the link
    # https://drive.google.com/file/d/1_x7n1RczEkEtohkQqduhD_UWnry0E54C/view?usp=sharing
    file_id = "1_x7n1RczEkEtohkQqduhD_UWnry0E54C"

    # Output path
    output_dir = "../data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "reddit_posts.csv")

    # Check if already exists
    if os.path.exists(output_path):
        response = input(f"{output_path} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Download cancelled.")
            return

    try:
        download_from_google_drive(file_id, output_path)
    except Exception as e:
        print(f"Error downloading file: {e}")
        print("\nAlternative: Please manually download the file from:")
        print("https://drive.google.com/file/d/1_x7n1RczEkEtohkQqduhD_UWnry0E54C/view?usp=sharing")
        print(f"and place it at: {output_path}")


if __name__ == "__main__":
    main()
