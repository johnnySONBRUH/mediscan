[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# MediScan

MediScan is an application designed to bridge the health literacy gap by simplifying complex medication labels and guides.


## Features
- **Intelligent OCR**: Extracts text from images of prescription bottles and medication labels with high accuracy.
- **AI-Powered Simplification**: Translates complex medical jargon into 5th-grade level English using Google Gemini 1.5 Flash.
- **Accessible UI**: Built with Streamlit for a simple, intuitive user experience.
- **Real-time Processing**: Streamed AI responses allow users to read the simplified instructions as they are generated.
- **Robust Error Handling**: Handles image upload issues, OCR failures, and API constraints gracefully.

## How it works
1. **Upload**: Users take a photo or upload an image of a prescription bottle or medication guide.
2. **Preprocessing**: The image is processed using `OpenCV` to enhance text readability for OCR.
3. **OCR**: The app uses `EasyOCR` to extract text from the image.
4. **Translation**: The extracted text is sent to an LLM (Google Gemini) with a prompt designed to translate medical jargon into plain, 5th-grade level English.


## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mediscan
   ```
2. Install the required dependencies:
   ```bash
   pip install streamlit easyocr opencv-python-headless google-generativeai
   ```

## Setup

1. Get your Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
2. Create a `.streamlit` folder if it doesn't exist.
3. Create a `secrets.toml` file inside the `.streamlit` folder.
4. Add your API key to the `secrets.toml` file:
   ```toml
   GEMINI_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run streamlit_app.py
   ```
2. Open the URL provided in the terminal (usually `http://localhost:8501`).
3. Upload an image of a prescription bottle or label.
4. Click "Scan and Translate" to see the extracted text and the plain-language simplification.


## Built With
- **Streamlit**: Web framework for a simple, accessible UI.
- **EasyOCR**: For optical character recognition.
- **Google GenAI API**: For intelligent text simplification (Gemini 1.5 Flash).
- **OpenCV**: For image preprocessing.

## Hackathon Goal
This project addresses the "Healthcare" track by improving patient access and health literacy, providing immediate value by helping users understand medication dosages and instructions.

## Problem Validation
We validated this idea by speaking with potential users, including local seniors and pharmacy technicians. 
- **Key Insight**: Users expressed frustration with small fonts on prescription bottles and confusion regarding abbreviations (e.g., "PO" vs "PRN").
- **User Quote**: "I often have to call my pharmacist just to understand how many times a day I should take my medication."

## Mentors & Acknowledgments
- We would like to thank our team and community mentors for their guidance on UX design for accessibility.

## AI Tool Disclosure
- **AI Coding Assistants**: This application was built with the assistance of an AI coding agent (Cline).
- **LLM used for simplification**: Gemini 1.5 Flash via Google Generative AI SDK.
- **Purpose**: AI was used for architecting the OCR-to-LLM pipeline, developing the Streamlit UI, implementing error handling, and writing documentation/scripts.
