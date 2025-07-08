# prequaligy.py

from ocr_utils import extract_images_from_pdf, run_ocr_on_images

class PrequaligyAgent:
    """
    PrequaligyAgent assesses subcontractor qualifications for financial and operational readiness.
    """
    def __init__(self, gemini_model):
        self.model = gemini_model

    def run(self, file_bytes: bytes) -> str:
        """
        Processes a subcontractor’s prequalification packet (PDF), extracts text via OCR,
        and generates a structured risk and readiness analysis.

        Args:
            file_bytes (bytes): The uploaded PDF document.

        Returns:
            str: AI-generated prequalification report with risks, recommendations, and pass/fail assessment.
        """
        try:
            # Step 1: Extract images from the document
            images = extract_images_from_pdf(file_bytes)
            if not images:
                return "No valid content found in the uploaded document."

            # Step 2: Perform OCR to extract text
            extracted_text = run_ocr_on_images(images)
            if not extracted_text.strip():
                return "Text extraction failed or no readable data found."

            # Step 3: Generate the prequal assessment prompt
            prompt = self._build_prompt(extracted_text)

            # Step 4: Invoke Gemini model
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"An error occurred during Prequaligy analysis: {e}"

    def _build_prompt(self, extracted_text: str) -> str:
        """
        Constructs the assessment prompt for the AI model.

        Args:
            extracted_text (str): OCR-derived text from subcontractor packet.

        Returns:
            str: Structured prompt for AI analysis.
        """
        return (
            "You are a subcontractor risk analyst reviewing a prequalification packet. Analyze the content and determine "
            "if the subcontractor is financially and operationally qualified to take on large construction or government projects.\n\n"
            "Focus on the following key areas:\n"
            "- Financial stability (e.g., revenue, net worth, credit history)\n"
            "- Bonding capacity (single and aggregate limits, bonding company rating)\n"
            "- Insurance coverage (GL, WC, Auto, Umbrella)\n"
            "- Safety metrics (EMR, OSHA incident rates, safety program documentation)\n"
            "- Relevant project experience (size, scope, industries)\n"
            "- References or client testimonials\n"
            "- Legal issues (lawsuits, terminations, regulatory violations)\n"
            "- Organization structure & staffing\n"
            "- Licensing & certifications\n\n"
            "=== DOCUMENT TEXT START ===\n"
            f"{extracted_text}\n"
            "=== DOCUMENT TEXT END ===\n\n"
            "Provide your response in this format:\n"
            "1. Overall Prequalification Status (Qualified / Conditional / Not Qualified)\n"
            "2. Strengths\n"
            "3. Risks or Missing Items\n"
            "4. Final Recommendation"
        )
