from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path
import os
import re
import json5

from assignment.core.gemini.prompts import parsing_prompt

load_dotenv(dotenv_path=Path(__file__).parent.parent.parent.parent / '.env')

API_KEY = os.getenv("API_KEY")		# On render this should just work on its own
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-pro')
chat = model.start_chat(history=[])

def parse(extracted_pdf):

    prompt = parsing_prompt + f"""
    These are the contents of the pdf: {extracted_pdf}
    """

    try:
        output = ""
        response = chat.send_message(prompt, stream=False, safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, 
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        })

        if not response:
            raise ValueError("No response received")

        for chunk in response:
            if chunk.text:
                output += str(chunk.text)

        json_list = re.findall("@@@json.*@@@", output, re.DOTALL)
        json_val = re.findall("{.*}", json_list[0].strip(), re.DOTALL)[0].strip()
    
        return json5.loads(json_val)

    except Exception as e:
        return 'Try again'