import requests
import os
from urllib.parse import urlparse

# Max allowed image size (5 MB for safety)
MAX_SIZE = 5 * 1024 * 1024  

def download_image(url):
    try:
        # Fetch the image
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Check content type
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type.lower():
            print(f"✗ Skipping (Not an image): {url}")
            return

        # Check file size (Content-Length from header if available)
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_SIZE:
            print(f"✗ Skipping (File too large > 5MB): {url}")
            return

        # Extract filename from URL
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_image.jpg"

        filepath = os.path.join("Fetched_Images", filename)

        # Prevent duplicate downloads
        if os.path.exists(filepath):
            print(f"⚠ Skipping duplicate: {filename}")
            return

        # Save image in binary mode
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):  # Save in chunks
                f.write(chunk)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error for {url}: {e}")
    except requests.exceptions.ConnectionError:
        print(f"✗ Connection Error: Unable to reach {url}")
    except requests.exceptions.Timeout:
        print(f"✗ Timeout Error: {url} took too long to respond")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request Error for {url}: {e}")
    except Exception as e:
        print(f"✗ Unexpected error for {url}: {e}")


def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Create directory if it doesn't exist
    os.makedirs("Fetched_Images", exist_ok=True)

    # Accept multiple URLs separated by commas
    urls = input("Enter image URL(s) (separated by commas): ").split(",")

    for url in urls:
        url = url.strip()
        if url:
            download_image(url)

    print("\nConnection strengthened. Community enriched.")


if __name__ == "__main__":
    main()
