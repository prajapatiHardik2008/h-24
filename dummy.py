import requests

# 1. Prompt define karein
prompt = "a cute cat with green eyes, high resolution, 4k"

# 2. URL banayein (prompt ko URL friendly banane ke liye quote ka use karein)
url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}"

# 3. Request bhejein
response = requests.get(url)

# 4. Image save karein
if response.status_code == 200:
    with open("my_cat_image.jpg", "wb") as f:
        f.write(response.content)
    print("Image successfully saved as my_cat_image.jpg")
else:
    print("Error generating image")