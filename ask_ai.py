import os 
import google.generativeai as genai
from dotenv import load_dotenv


#API-Configuration
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables.")

else:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("Gemini API key Confifigured Successfully")
    except Exception as e:
        print(f"Error : Failed to COnfigure gemini API Key")

async def handle_ai_messages(user_message: str) -> str:
    """
    Handles AI-related messages and returns the response.
    """
    if user_message.startswith("$ask"):
        command = "$ask"
        prompt_suffix = "Answer in 200 characters or less"
    elif user_message.startswith("$explain"):
        command= "$explain"
        prompt_suffix = "Answer in 1500 Characters or less."
    elif user_message.startswith("$news"):
        command = "$news"
        prompt_suffix = "-Tell me the latest news like the absolute Geopolitical or whatever news from here in 1000 characters or less in Bullet points"
    elif user_message.startswith("$summarize"):
        command = "$summarize"
        prompt_suffix = "Summarize the following into 500-700 characters or less"
        
    else:
        return ""
        
    prompt = user_message[len(command):].strip()
    if not prompt:
        return "❌ Please provide a question or topic to ask about."
    else:
        full_prompt = f"{prompt}\n\n{prompt_suffix}"
        return await ask_gemini(full_prompt)

async def ask_gemini(prompt: str) -> str:
    #this function will call the Gemini API and return the response
    if not GEMINI_API_KEY:
        return "**API Error**: The Gemini API Key is Missing or Invalid."
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = await model.generate_content_async(prompt)

        if not response.parts:
            return "**Content Error: The Model Generated an Empty Response.**"
        
        return response.text
    except Exception as e:
        print(f"An Error Occurred with the Gemini API: {e}")
        return f"**API Error**: I couldn't get a Response, please try again later.\nError Details: {e}"