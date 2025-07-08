# riskguru.py

from ocr_utils import extract_images_from_pdf, run_ocr_on_images


class RiskguruAgent:
    """
    RiskguruAgent evaluates subcontractor risk based on insurance, financials, safety, and compliance documents.
    """
    def __init__(self, gemini_model):
        self.model = gemini_model

    def run(self, file_bytes: bytes) -> str:
        """
        Performs OCR on a subcontractor document and evaluates their overall risk profile.

        Args:
            file_bytes (bytes): The uploaded PDF containing prequal, financials, or compliance info.

        Returns:
            str: A risk rating summary with detailed observations.
        """
        try:
            # Step 1: Extract images from PDF
            images = extract_images_from_pdf(file_bytes)
            if not images:
                return "The uploaded PDF appears to be empty or unreadable."

            # Step 2: Run OCR on images
            extracted_text = run_ocr_on_images(images)
            if not extracted_text.strip():
                return "OCR failed to extract meaningful text from the document."

            # Step 3: Generate structured prompt
            prompt = self._build_prompt(extracted_text)

            # Step 4: Query Gemini model
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"An error occurred during risk assessment: {e}"

    def _build_prompt(self, extracted_text: str) -> str:
        """
        Builds a structured prompt for the AI model to analyze subcontractor risk.

        Args:
            extracted_text (str): Text extracted via OCR from the uploaded document.

        Returns:
            str: A formatted prompt for the AI.
        """
        return (
            "You are a construction subcontractor risk assessment expert.\n\n"
            "Review the following documentation and assign a risk rating to the subcontractor. "
            "Evaluate their risk level based on the following criteria:\n"
            "- Financial stability (balance sheet strength, credit rating, cash flow)\n"
            "- Safety performance (EMR, OSHA records, incident reports)\n"
            "- Insurance adequacy (coverage limits, policy types, exclusions)\n"
            "- Work history and capacity (past projects, backlog, references)\n"
            "- Legal/compliance issues (lawsuits, terminations, citations)\n\n"
            "=== DOCUMENT TEXT START ===\n"
            f"{extracted_text}\n"
            "=== DOCUMENT TEXT END ===\n\n"
            "Respond with the following format:\n"
            "1. **Overall Risk Rating**: Low / Medium / High\n"
            "2. **Key Strengths**: List observed strengths\n"
            "3. **Key Risk Factors**: List observed risks or gaps\n"
            "4. **Recommendation**: Proceed / Proceed with conditions / Do not proceed"
        )
