# MediScan

## Inspiration
Health literacy is a massive, universally understood real-world problem. Millions of people—especially the elderly and non-native speakers—struggle to decode confusing medical jargon on prescription labels. Phrases like "Take 1 tab PO QD PRN" can easily lead to accidental overdoses or improper usage. We were inspired to build a tool that directly addresses this gap, saving people from taking the wrong dosage by turning complex medical instructions into plain, everyday language. 

## What it does
MediScan is an accessibility-first mobile web app that instantly translates confusing prescription labels into simple English. Users simply take a photo of a medication label or guide. The app extracts the text, processes it through an AI model, and translates it into a 5th-grade reading level (e.g., turning "Take 1 tab PO QD PRN" into "Take 1 pill by mouth once a day as needed"). The interface features large fonts, high contrast, and a massive "Take Photo" button to ensure it is usable by our target audience.

## How we built it
We focused on leveraging existing APIs to build a highly feasible, functional prototype without getting bogged down in heavy custom coding. 
*   **Frontend:** We used **Streamlit** (or React) to create a simple, accessible UI with high contrast and large buttons. 
*   **Backend/OCR:** We integrated **easyocr** to extract raw text from the uploaded prescription images. 
*   **AI Integration:** We passed the extracted text to an LLM API (using Gemini). We carefully engineered a prompt: *"You are a helpful pharmacist. Translate this medical text into plain, simple English for a 5th-grade reading level."*

## Challenges we ran into
*   **OCR Accuracy:** Prescription bottles often have glare, curve around the cylinder, or use tiny fonts. We had to implement image cropping and preprocessing to help `easyocr` read the text accurately.
*   **Prompt Engineering:** We had to ensure the LLM strictly translated the text without hallucinating additional medical advice, keeping the output safe and strictly factual.
*   **Narrowing the Scope:** We resisted the urge to build a diagnostic tool. Keeping the app focused solely on *reading and simplifying text* was challenging but crucial for a polished hackathon demo.

## Accomplishments that we're proud of
*   **Live Demos** We successfully built a visually powerful "before and after" moment. Watching the app instantly translate confusing jargon into clear instructions leaves a lasting impression on judges.
*   **User-Centric Design:** We built an interface that truly understands the end-user, prioritizing accessibility (large text, high contrast) over flashy, complicated UI elements.

## What we learned
We learned the immense power of combining OCR with LLMs to create highly feasible, high-impact tools in a short timeframe. We also learned how to effectively use AI coding assistants to accelerate our development, allowing us to spend more time on problem validation and user accessibility. Most importantly, we learned that the best tech solutions are often the simplest ones that directly solve a human problem.

## What's next for MediScan
*   **Multi-language Support:** Expanding the LLM translation to include Spanish, Mandarin, and other languages to help non-native English speakers.
*   **Text-to-Speech:** Adding an audio playback feature for visually impaired users.
*   **Pharmacy Integration:** Partnering with local pharmacies to allow users to pull digital labels directly into the app, bypassing the need for a photo altogether.