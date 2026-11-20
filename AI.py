from google import genai

class AI():
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def simplify_text_stream(self, medical_text):
        # Primary model with fallbacks if an API call fails
        models = ["gemini-4-hydrogen", "gemini-3.8-flash", "gemini-3.5-flash-lite"]

        prompt = f"You are a helpful pharmacist. Translate this medical text into plain, simple English for a 5th-grade reading level:\n\n{medical_text}"
        
        last_error = None
        for model_name in models:
            try:
                response = self.client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt,
                )
                streamed = False
                for chunk in response:
                    if chunk.text:
                        streamed = True
                        yield chunk.text
                if streamed:
                    return
            except Exception as e:
                last_error = e
                # Try next model in fallback list
                continue

        # If all candidate models failed, yield the last encountered error
        yield f"ERROR_API_FAILURE: {str(last_error)}"


