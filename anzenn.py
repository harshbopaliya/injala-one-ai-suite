# anzenn.py

from ocr_utils import extract_images_from_pdf, run_ocr_on_images


class AnzennAgent:
    """
    AnzennAgent analyzes workplace safety and compliance documents using OCR and a Gemini model.
    """
    def __init__(self, gemini_model):
        self.model = gemini_model

    def run(self, file_bytes: bytes) -> str:
        """
        Processes a PDF document (e.g., safety manual, compliance report), extracts text via OCR,
        and evaluates OSHA & industry-standard compliance.

        Args:
            file_bytes (bytes): The uploaded PDF file as byte stream.

        Returns:
            str: AI-generated compliance analysis and risk report.
        """
        try:
            # Step 1: Extract visual content
            images = extract_images_from_pdf(file_bytes)
            if not images:
                return "No readable pages found in the PDF."

            # Step 2: OCR extraction
            extracted_text = run_ocr_on_images(images)
            if not extracted_text.strip():
                return "Text extraction failed or resulted in empty content."

            # Step 3: Build prompt
            prompt = self._build_prompt(extracted_text)

            # Step 4: Query Gemini model
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"An error occurred while processing the document: {e}"

    def _build_prompt(self, extracted_text: str) -> str:
        """
        Constructs a structured prompt for Gemini to analyze safety & compliance documentation.

        Args:
            extracted_text (str): OCR-extracted document content.

        Returns:
            str: Full analysis prompt.
        """
        return (
            "You are a certified workplace safety and OSHA compliance auditor. "
            "Review the following safety manual or documentation and determine whether it meets OSHA "
            "and industry-standard safety compliance guidelines.\n\n"
            "Evaluate the document for the presence, completeness, and adequacy of the following:\n"
            "1. Safety training records (including dates, scope, and participants)\n"
            "2. Written safety policies and procedures\n"
            "3. Incident logs and reporting systems\n"
            "4. Hazard communication program (SDS, labeling, training)\n"
            "5. Emergency action plans (fire, medical, evacuation, etc.)\n"
            "6. Designated safety officer or roles\n"
            "7. Evidence of regular audits or inspections\n"
            "8. Specific procedures for common hazards (e.g., LOTO, fall protection)\n\n"
            f"=== DOCUMENT TEXT START ===\n{extracted_text}\n=== DOCUMENT TEXT END ===\n\n"
            "Summarize your findings in the following structure:\n"
            "- Overall Compliance Assessment (Compliant: YES/NO)\n"
            "- Observed Strengths\n"
            "- Missing or Incomplete Elements\n"
            "- Risks and Recommendations"
        )
