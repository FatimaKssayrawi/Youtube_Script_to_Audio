import streamlit as st
import requests
import os
import dotenv
dotenv.load_dotenv('.env')

url = "https://play.ht/api/v1/convert"

# Streamlit app title and description
st.title("Youtube Video Script Generator")
video_title = st.text_input("Enter the video's title",placeholder = "Essential Tips for Successful Job Interviews, Quick and Easy Dinner Recipes for Busy Parents")
video_description = st.text_input("Enter the video's description",
                                  placeholder = "From preparation to body language, we'll guide you towards success and help you land your dream job")
search_term = st.text_input('Enter search term',placeholder = "job interview tips,how to succeed in interviews,interview preparation advice")
tone_voice = st.text_input('Enter tone of voice', placeholder = "Supportive, empowering, informative")
#length = st.number_input('Enter number of words')
#length = int(length)
# original prompt that includes all user's inputs
prompt = f"I want you to act as a scriptwriter for a short YouTube video titled '{video_title} '.\
            Your task is to write a script between 200 and 700 words in an '{tone_voice}' tone. Please be precise with the number of words. Consider the video’s description: '{video_description}'. \
            and the following search terms: '{search_term}'. "


def generate(prompt):
    res = ''
    headers = {
        'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}',
        'Content-Type': 'application/json'
    }

    payload = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'max_tokens': 1500,
    }

    response = requests.post(
        os.environ["OPENAI_API_URL"],
        headers=headers,
        json=payload
    )

    api_response = response.json()
    res = api_response["choices"][0]["text"]

    return res
response = ''
# Button to fetch the response
# if the button is pressed, the code will be executed
if st.button("**Click here to generate script and audio**"):
# Check if product_name and product_description are provided

        response = generate(prompt)

        # Display the response in Streamlit
        st.write(" Youtube Video Script: ")
        #st.write(prompt)
        #st.write(response)

def remove_text_in_brackets(text):
    result = ""
    inside_brackets = False
    inside_parentheses = False

    for char in text:
        if char == "[":
            inside_brackets = True
            continue
        elif char == "]":
            inside_brackets = False
            continue
        elif char == "(":
             inside_parentheses = True
             continue
        elif char == ")":
            inside_parentheses = False
            continue

        if not inside_brackets and not inside_parentheses:
            result += char

    return result

cleaned_text = remove_text_in_brackets(response)
#st.write("**Your Youtube Video Script:**")
#st.write(cleaned_text)

def remove_words(text, words):
    for word in words:
        text = text.replace(word + ":", "")
    return text


words_to_remove = ["Narrator", "Host", "Presenter","Emcee", "Commentator",
		            "NARRATOR", "HOST", "PRESENTER","EMCEE", "COMMENTATOR"
                    "Announcer","Voiceover", "artist", "Speaker", "Performer",
		            "ANNOUNCER","VOICEOVER", "ARTIST", "SPEAKER", "PERFORMER",
                    "Character", "Actor/Actress", "Protagonist", "Antagonist",
		            "ChARACTER", "ACTOR/ACTRESS", "PROTAGONIST", "ANTAGONIST",
                    "Interviewee", "Interviewer", "Expert", "Guest", "Intro",
		            "INTERVIEWEE", "IntERVIEWER", "EXPERT", "GUEST", "INTRO",
                    "Introduction", "Outro", "Conclusion", "Summary", "Co-host",
		             "INTRODUCTION", "OUTRO", "CONCLUSION", "SUMMARY", "CO-HOST",
                    "Lead","Sidekick","Panelist","Moderator","Participant", "Script",
		            "LEAD","SIDEKICK","PANELIST","MODERATOR","PARTICIPANT", "SCRIPT",
                    "Demonstrator","Coach","Mentor","Consultant","Guide","Support",
		            "DEMONSTRATOR","COACH","MENTOR","CONSULTANT","GUIDE","SUPPORT",
                    "Facilitator","Educator","Influencer","Expertise"," Specialist",
		            "FACILITATOR","EDUCATOR","INFLUENCER","EXPERTISE"," SPECIALIST",
                    "Trainer", "Youtuber","Content creator","Vlogger","Showcaser","Reviewer"
		            "TRAINER", "YOUTUBER","CONTENT CREATOR","VLOGGER","SHOWCASER","REVIEWER"]

cleaned_text1 = remove_words(cleaned_text, words_to_remove)
st.write("**Your Youtube Generated Script:**")
st.write(cleaned_text1)

payload = {
    "content": [cleaned_text1],
    "voice": "en-US-JennyNeural",
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "AUTHORIZATION": os.getenv('SECRET_KEY'),
    "X-USER-ID": os.getenv('USER_ID')
}

response = requests.post(url, json=payload, headers=headers)
#st.write(" Response from post method: ")
#st.write(response.text)

response_data = response.json()
transcription_id = response_data.get('transcriptionId')
#st.write(" transcriptionId: ")
#st.write(transcription_id)
url = "https://play.ht/api/v1/articleStatus?transcriptionId={}".format(transcription_id)

headers = {
    "accept": "application/json",
    "AUTHORIZATION": os.getenv('SECRET_KEY'),
    "X-USER-ID": os.getenv('USER_ID')
}

response = requests.get(url, headers=headers)
#st.write('response')
#st.write(response.text)
while response.json()["converted"] == False:
    response = requests.get(url, headers=headers)
response_data = response.json()
audio_url = response_data.get('audioUrl')


st.write("**Click on the below URL to download the audio in mp3 format:**")
st.write(audio_url)
