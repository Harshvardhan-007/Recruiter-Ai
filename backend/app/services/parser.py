import instructor
import google.generativeai as genai
from app.models import JobSchema

# 1. Pass your Gemini API Key here
genai.configure(api_key=" *Your API KEY* ")

# 2. Patch the Gemini client with Instructor to force JSON output
client = instructor.from_gemini(
    client=genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest"),
    mode=instructor.Mode.GEMINI_JSON,
)

async def parse_unstructured_jd(raw_text: str) -> JobSchema:
    # 3. Instructor translates this OpenAI-style request into Gemini format automatically
    return client.chat.completions.create(
        response_model=JobSchema,
        messages=[
            {"role": "system", "content": "You are a professional technical recruiter. Extract the requested data accurately."},
            {"role": "user", "content": f"Extract structured requirements from this JD:\n\n{raw_text}"}
        ],
    )