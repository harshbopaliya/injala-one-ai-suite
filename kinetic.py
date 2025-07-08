# kinetic.py

from ocr_utils import extract_images_from_pdf, run_ocr_on_images


class KineticAgent:
    """
    Evaluates safety policy documents for OSHA compliance and workplace risk using LLM analysis.
    """
    def __init__(self, gemini_model):
        self.model = gemini_model

    def run(self, file_bytes: bytes) -> str:
        """
        Analyzes a PDF safety policy for OSHA and safety program compliance.

        Args:
            file_bytes (bytes): PDF file in bytes.

        Returns:
            str: Structured OSHA compliance evaluation.
        """
        try:
            # Step 1: Convert PDF to images
            images = extract_images_from_pdf(file_bytes)
            if not images:
                return "The uploaded PDF does not contain any pages or visual content."

            # Step 2: Extract text via OCR
            extracted_text = run_ocr_on_images(images)
            if not extracted_text.strip():
                return "OCR failed to extract meaningful text from the document."

            # Step 3: Build structured OSHA prompt
            prompt = self._build_prompt(extracted_text)

            # Step 4: Analyze with Gemini model
            response = self.model.generate_content(prompt)

            # Step 5: Return output text
            return response.text.strip()

        except Exception as e:
            return f"An error occurred during OSHA compliance evaluation: {str(e)}"

    def _build_prompt(self, extracted_text: str) -> str:
        """
        Builds a detailed OSHA compliance evaluation prompt for the LLM.

        Args:
            extracted_text (str): OCR-extracted text from the safety policy.

        Returns:
            str: Formatted prompt string.
        """
        return f"""
You are a certified OSHA compliance auditor and workplace safety evaluator.

Your job is to assess a contractor's workplace safety policy against OSHA 29 CFR 1910 and 1926 standards and modern industry best practices.

Evaluate the document using the following framework:

---

1. **PPE Requirements** – Are they task-specific? Is PPE listed per job hazard?
2. **Training Protocols** – Are mandatory trainings listed (Fall Protection, LOTO, HazCom)? Who trains, and how is it tracked?
3. **Incident Reporting** – Are reporting steps, definitions, and corrective actions clearly outlined?
4. **Hazard Identification** – Is there a formal inspection or hazard reporting process?
5. **Inspections & Audits** – Are audits scheduled, documented, and led by responsible personnel?
6. **Coverage of Key Programs** – Does the document mention:
    - Hazard Communication (HazCom)
    - Lockout/Tagout (LOTO)
    - Confined Space Entry
    - Fall Protection
    - Emergency Action Plan (EAP)
    - Fire Safety, Respiratory Protection, First Aid
    - Recordkeeping (OSHA 300 logs, training certs)

7. **Red Flags** – Identify vague or boilerplate language (“PPE must be worn” with no task linkage).
8. **Continuous Improvement** – Does the program include updates, revisions, and performance tracking?
9. **Compliance Risk Score** – Rate the policy from 1 (poor) to 5 (excellent).
10. **Final Verdict** – Label the policy as COMPLIANT, PARTIALLY COMPLIANT, or NON-COMPLIANT.

---

### Contractor’s Safety Policy:
{extracted_text}

---

Please format your response clearly using the following format:

---
🛡 **OSHA Compliance Evaluation**
- PPE Assessment: ...
- Training Assessment: ...
- Incident Reporting Assessment: ...
- Hazard Controls: ...
- Audit & Inspection Protocols: ...
- Program Inclusions: ...
- Vague Language / Gaps: ...
- Continuous Improvement: ...
- Risk Score (1-5): ...
- ✅ Final Verdict: ...
"""
