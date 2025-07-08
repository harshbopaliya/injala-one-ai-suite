# auto_router.py

import re
from typing import List, Tuple


class AgentDetectionError(Exception):
    """Custom exception raised when agent routing fails."""
    pass


def detect_agent_with_gemini(gemini_model, query: str, uploaded_files: List[bytes]) -> Tuple[str, List[int]]:
    """
    Detects which specialized agent should handle the user's query based on the query and uploaded files.

    Args:
        gemini_model: An instance of a Gemini-compatible model with a `.generate_content(prompt)` method.
        query (str): The user's natural language query.
        uploaded_files (List[bytes]): List of uploaded PDF files (in byte form).

    Returns:
        Tuple[str, List[int]]: Detected agent name and the indices of relevant files.

    Raises:
        AgentDetectionError: If parsing fails or response is ambiguous.
    """
    file_count = len(uploaded_files)
    file_hint = f"There are {file_count} PDF file(s) uploaded."

    prompt = f"""
You are an AI routing assistant for an LLM-powered document analysis platform.

Your job is to decide which specialized document processing agent should handle the user's request. Use the following list of agent types:

1. **asuretify** – Compare insurance requirements in a contract vs. a COI (requires 2 PDFs)
2. **kinetic** – Evaluate subcontractor safety or OSHA policies (1 PDF)
3. **wrappotal** – Analyze wrap-up (OCIP/CCIP) insurance documents (1 PDF)
4. **riskguru** – Rate subcontractor risk from company profile or documents (1 PDF)
5. **prequaligy** – Assess financial prequalification, financials, bonding, etc. (1 PDF)
6. **anzenn** – Evaluate workplace safety, field safety protocols, or audits (1 PDF)

Instructions:
- Choose the most relevant agent based on the query and file count.
- Return response in this JSON-like format:
  agent: <agent_name>
  files: [<file_indices>]

Example:
agent: asuretify
files: [0, 1]

Query:
\"\"\"{query}\"\"\"
{file_hint}
    """

    try:
        # Call LLM
        response = gemini_model.generate_content(prompt)
        response_text = response.text.lower().strip()

        # Parse agent name
        agent_match = re.search(r"agent:\s*([a-z_]+)", response_text)
        file_match = re.search(r"files:\s*\[([\d,\s]+)\]", response_text)

        if not agent_match or not file_match:
            raise AgentDetectionError("Agent or file indices not found in model response.")

        agent = agent_match.group(1).strip()
        file_indices = [int(i.strip()) for i in file_match.group(1).split(",") if i.strip().isdigit()]

        if not file_indices or max(file_indices) >= file_count:
            raise AgentDetectionError(f"Invalid file indices returned: {file_indices}")

        return agent, file_indices

    except Exception as e:
        raise AgentDetectionError(f"Routing failed: {str(e)}")
