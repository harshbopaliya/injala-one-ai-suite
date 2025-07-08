# asuretify.py

from ocr_utils import extract_images_from_pdf, run_ocr_on_images


class AsuretifyAgent:
    """
    Compares contract insurance requirements with a Certificate of Insurance (COI)
    to assess compliance, risk exposure, and coverage gaps.
    """

    def __init__(self, model):
        self.model = model

    def run(self, contract_bytes: bytes, coi_bytes: bytes) -> str:
        """
        Processes a construction contract and COI to determine compliance.

        Args:
            contract_bytes (bytes): Contract PDF file as byte stream.
            coi_bytes (bytes): COI PDF file as byte stream.

        Returns:
            str: A structured compliance audit report.
        """
        try:
            # Step 1: Extract and OCR contract
            contract_images = extract_images_from_pdf(contract_bytes)
            contract_text = run_ocr_on_images(contract_images)
            if not contract_text.strip():
                return "No readable text extracted from the contract document."

            # Step 2: Extract and OCR COI
            coi_images = extract_images_from_pdf(coi_bytes)
            coi_text = run_ocr_on_images(coi_images)
            if not coi_text.strip():
                return "No readable text extracted from the COI document."

            # Step 3: Generate LLM prompt
            prompt = self._build_prompt(contract_text, coi_text)

            # Step 4: Analyze with the model
            response = self.model.generate_content(prompt)

            # Step 5: Return formatted result
            return response.text.strip()

        except Exception as e:
            return f"❌ An error occurred during COI validation: {str(e)}"

    def _build_prompt(self, contract_text: str, coi_text: str) -> str:
        """
        Formats a detailed insurance compliance evaluation prompt.

        Args:
            contract_text (str): Text from the contract.
            coi_text (str): Text from the COI.

        Returns:
            str: Final structured prompt string.
        """
        return f"""
You are a certified insurance compliance auditor.

Your task is to compare the Certificate of Insurance (COI) against the insurance requirements outlined in a construction contract.

Evaluate using the following criteria:

---

1. ✅ **Coverage Match** – Do the listed policies (e.g., GL, Auto, WC, Umbrella) match the contract requirements?
2. ✅ **Policy Limits Validation** – Do the limits on the COI meet or exceed what the contract requires?
3. ⚠️ **Policy Period Validity** – Are the effective/expiration dates valid during the contract term?
4. ✅ **Named Insured Validation** – Does the COI's named insured match the contractor in the contract?
5. ✅ **Additional Insured Language** – Is the client listed as an additional insured if required?
6. 🚩 **Red Flags or Missing Elements**:
    - Waiver of Subrogation missing
    - Primary & Noncontributory wording missing
    - Expired policies
    - Certificate Holder incorrect
    - Incomplete COI form (missing policy numbers, dates, etc.)

7. ✅ **Risk Score** – Score from 1 (low risk) to 5 (high risk or non-compliant)
8. ✅ **Final Verdict** – COMPLIANT or NON-COMPLIANT

---

### 📄 CONTRACT INSURANCE REQUIREMENTS:
{contract_text}

---

### 📋 CERTIFICATE OF INSURANCE:
{coi_text}

---

Please output the results in the following format:

---
**🧾 Compliance Review Report**
- Coverage Match: ...
- Limit Match: ...
- Policy Validity: ...
- Named Insured Check: ...
- Additional Insured: ...
- Red Flags: ...
- Risk Score (1-5): ...
- ✅ Final Verdict: COMPLIANT or NON-COMPLIANT
"""
