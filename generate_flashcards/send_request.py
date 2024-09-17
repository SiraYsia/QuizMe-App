import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_flashcards(response_text):
    # First, try the original pattern
    pattern = r'Front: (.*?)\nBack: (.*?)(?=\nFront: |\Z)'
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    flashcard_map = {}
    
    for front, back in matches:
        front_cleaned = re.sub(r'[^\w\s\?]', '', front).strip()
        back_cleaned = re.sub(r'[^\w\s\?]', '', back).strip()
        flashcard_map[front_cleaned] = back_cleaned
    
    # If flashcard_map is empty, its likeley that it used **Front** and **Back** pattern
    if not flashcard_map:
        alternative_pattern = r'\*\*Front:\*\* (.*?)\n\*\*Back:\*\* (.*?)(?=\n\*\*Front:\*\* |\Z)'
        alternative_matches = re.findall(alternative_pattern, response_text, re.DOTALL)
        
        for front, back in alternative_matches:
            front_cleaned = re.sub(r'[^\w\s\?]', '', front).strip()
            back_cleaned = re.sub(r'[^\w\s\?]', '', back).strip()
            flashcard_map[front_cleaned] = back_cleaned
    
    return flashcard_map

def generate_flashcards(study_material, flashcard_count):
    flashcard_map = {}  
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Prepare the content prompt
        content = (f'Create {flashcard_count} concise flashcards to demonstrate my understanding '
                   f'of the following topic or text: {study_material}. '
                   'Provide the flashcards in the following format: '
                   'Front: <question>? Back: <answer>. Each flashcard should be separated by "Front:" keyword.'
                   'Please do not style the conent, do not bold or underline anything. Do not use **' )
        
        # Generate content
        response = model.generate_content(content)
        print(response.text)
        
        flashcard_map = extract_flashcards(response.text)
            
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return flashcard_map

# Testing 
# generate_flashcards("World War 2", 10)
