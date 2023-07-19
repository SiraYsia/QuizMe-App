import openai
import os
import re

openai.api_key = os.environ['OPENAI_API_KEY']

def generate_flashcards(study_material, flashcard_count):
    conversation = [
        {'role': 'user', 'content': f'Create {flashcard_count} concise flashcards to demonstrate my understanding of the following text: {study_material}. Each flashcard should consist of a question and an answer, separated by a question mark (?). Use a new line to separate each flashcard. The format should be as follows: this is the question? this is the answer. Please avoid including any additional formatting steps, such as numbering the flashcards. DO NOT NUMBER THE FLASCHARDS OR NAME THEM QUESTION AND ANSWER SIMPLY PUT THE QUESTION THEN ANSWER PLEASE'}
    ]
    try:
        # Make the API request to ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.7,
            max_tokens=500
        )

        print(study_material)
        assistant_response = response.choices[0].message['content']
        print(assistant_response)

        flashcards = []

        flashcard_entries = re.findall(r"(.*?)\.(.*?)\n", assistant_response)
        print(flashcard_entries)

        for entry in flashcard_entries:
                print(entry)
                print('EACH ENTRY')
                question_and_answer = entry[0].strip()
                question, answer = question_and_answer.split("?", 1)
                question = question.strip()
                answer = answer.strip()
                flashcards.append([question, answer])
        return flashcards

    except Exception as e:
        # Handle any errors that occur during flashcard generation
        print("An error occurred during flashcard generation:", str(e))
        return []
