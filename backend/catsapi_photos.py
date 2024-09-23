import os
import requests
from dotenv import load_dotenv

load_dotenv()

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
CAT_API_KEY = os.getenv("CAT_API_KEY")  

def handle_cat_request(user_message):
    num_cats = 1
    breed = None

    breed_map = {
        "persian": "pers",
        "siamese": "siam",
        "maine coon": "mcoo",
        "ragdoll": "ragd",
        "bengal": "beng",
        "british shorthair": "bsho",
        "sphynx": "sphy",
        "abyssinian": "abys"
    }

    print(f"Received cat request: {user_message}")

    words = user_message.lower().split()

    for word in words:
        if word.isdigit():
            num_cats = int(word) 
            print(f"Number of cats requested: {num_cats}")
        if word in breed_map:
            breed = breed_map[word]  
            print(f"Breed requested: {word} (ID: {breed_map[word]})")

    if breed is None:
        print("No specific breed requested. Fetching random cat images.")

    cat_images = []

    params = {
        'limit': num_cats
    }
    if breed:
        params['breed_ids'] = breed

    print(f"Making request to CatAPI with parameters: {params}")

    response = requests.get(CAT_API_URL, headers={"x-api-key": CAT_API_KEY}, params=params)
    
    if response.status_code == 200:
        cat_data = response.json()
        if cat_data:
            for cat in cat_data:
                cat_images.append(cat['url'])
                print(f"Cat image URL added: {cat['url']}")
        else:
            print("No cat data found in response.")
    else:
        print(f"Error fetching cat image: {response.status_code} - {response.text}")

    if cat_images:
        # Create HTML image tags for cat images
        img_tags = ''.join(f'<img src="{url}" alt="Cat" style="width:200px; margin:5px;">' for url in cat_images)
        return f"Here are your cats:<br>{img_tags}"
    
    return "Sorry, I couldn't find any cats."
