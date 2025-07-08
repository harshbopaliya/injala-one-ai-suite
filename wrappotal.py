# wrappotal.py

from ocr_utils import extract_images_from_pdf, run_ocr_on_images


class WrappotalAgent:
    """
    Analyzes Wrap-Up Insurance (OCIP/CCIP) documentation for compliance and structure.
    """
    def __init__(self, gemini_model):
        self.model = gemini_model

    def run(self, file_bytes: bytes) -> str:
        """
        Evaluates the uploaded PDF for wrap-up program compliance and completeness.

        Args:
            file_bytes (bytes): The uploaded PDF file content.

        Returns:
            str: Analysis result with summary and wrap-up validation.
        """
        try:
            # Step 1: Extract page images from PDF
            images = extract_images_from_pdf(file_bytes)
            if not images:
                return "The uploaded PDF contains no extractable content."

            # Step 2: Extract text from the PDF using OCR
            extracted_text = run_ocr_on_images(images)
            if not extracted_text.strip():
                return "No readable text was found in the document after OCR."

            # Step 3: Create detailed analysis prompt
            prompt = self._build_prompt(extracted_text)

            # Step 4: Send prompt to Gemini model
            response = self.model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            return f"An error occurred while analyzing the Wrap-Up document: {str(e)}"

    def _build_prompt(self, extracted_text: str) -> str:
        """
        Constructs the AI prompt to analyze OCIP/CCIP documentation.

        Args:
            extracted_text (str): Text extracted from the wrap-up PDF.

        Returns:
            str: Structured prompt for LLM analysis.
        """
        return (
            "You are an insurance compliance expert specializing in Wrap-Up Insurance (OCIP/CCIP) programs.\n\n"
            "Carefully analyze the document text below and determine the following:\n"
            "- Is this document part of a valid wrap-up program?\n"
            "- Are key elements included: project name, enrolled contractors, carrier details, "
            "coverage terms, exclusions, effective/expiration dates, and administrative contacts?\n"
            "- Identify any compliance risks, documentation gaps, or omitted sections.\n\n"
            "=== WRAP-UP DOCUMENT TEXT START ===\n"
            f"{extracted_text}\n"
            "=== WRAP-UP DOCUMENT TEXT END ===\n\n"
            "Provide a detailed summary including:\n"
            "1. **Wrap-Up Program Detected**: YES / NO\n"
            "2. **Key Information Present**: (list what was found)\n"
            "3. **Missing or Risk Areas**: (list gaps or concerns)\n"
            "4. **Wrap-Up Program Document Valid**: YES or NO\n"
        )
