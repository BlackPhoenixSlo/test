import os
import random

def get_random_media(material_path):
    # 1. Randomly determine if media will be sent
    if random.randint(1,5) == 1:
        
        # 2. Randomly select media type
        media_type = random.choice(['img', 'vids'])
        
        # 3. Randomly select from 'live' or 'others'
        media_category = random.choice(['live', 'others'])
        
        # Construct the path to the chosen directory
        dir_path = os.path.join(material_path, media_type, media_category)
        
        # Get a list of all files in the chosen directory
        all_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        
        # Randomly choose a file
        chosen_file = random.choice(all_files)
        
        file_path = os.path.join(dir_path, chosen_file)
        
        # 4. Generate media_input text
        if media_type == 'img':
            if media_category == 'live':
                media_input = "Girlfriend: [sends a live teasing photo aka selfy of herself]"
            else:
                media_input = "Girlfriend: [sends a picture of herself taken with help of others]"
        else:  # for videos
            if media_category == 'live':
                media_input = "Girlfriend: [sends a quick video of herself dancing]"
            else:
                media_input = "Girlfriend: [sends a quick video having fun with friends]"
                
        # 5. Return the file path and media_input
        return file_path, media_input
    else:
        return None, None  # No media will be sent

# Usage
MATERIAL_PATH = "/Users/jakabasej/Documents/GitHub/test/material"
file_path, media_input = get_random_media(MATERIAL_PATH)
if file_path:
    # Send the media file to telegram bot
    # e.g., update.message.reply_media(open(file_path, 'rb'))
    print(f"Sending {file_path} with media input: {media_input}")
else:
    print("No media to send.")


get_random_media("/Users/jakabasej/Documents/GitHub/test/material")