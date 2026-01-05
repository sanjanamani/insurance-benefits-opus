"""
Claude AI-powered document parser for insurance benefits extraction
Uses Anthropic's Claude API to intelligently parse insurance documents
"""

import anthropic
import os
import base64
from io import BytesIO
from typing import Dict, Any, Optional
import PyPDF2
from PIL import Image


def parse_insurance_document(uploaded_file) -> Dict[str, Any]:
    """
    Parse insurance document using Claude AI

    Args:
        uploaded_file: Streamlit uploaded file object (PDF or image)

    Returns:
        Dictionary containing extracted insurance information
    """
    try:
        # Get API key
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            return {
                "success": False,
                "error": "ANTHROPIC_API_KEY not configured"
            }

        # Initialize Claude client
        client = anthropic.Anthropic(api_key=api_key)

        # Get file type
        file_type = uploaded_file.type
        file_name = uploaded_file.name.lower()

        # Process based on file type
        if "pdf" in file_type or file_name.endswith(".pdf"):
            result = _parse_pdf_document(client, uploaded_file)
        elif any(ext in file_name for ext in [".png", ".jpg", ".jpeg"]):
            result = _parse_image_document(client, uploaded_file)
        else:
            return {
                "success": False,
                "error": f"Unsupported file type: {file_type}"
            }

        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Error parsing document: {str(e)}"
        }


def _parse_pdf_document(client: anthropic.Anthropic, pdf_file) -> Dict[str, Any]:
    """Parse PDF insurance document"""

    try:
        # Read PDF and extract text
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_content = ""

        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"

        if not text_content.strip():
            # If text extraction failed, try OCR approach
            return {
                "success": False,
                "error": "Could not extract text from PDF. Please ensure it's not a scanned image."
            }

        # Use Claude to analyze the text
        result = _analyze_with_claude(client, text_content)
        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing PDF: {str(e)}"
        }


def _parse_image_document(client: anthropic.Anthropic, image_file) -> Dict[str, Any]:
    """Parse image insurance document using Claude's vision capabilities"""

    try:
        # Read image file
        image_bytes = image_file.read()

        # Encode to base64
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # Determine media type
        file_type = image_file.type
        if "png" in file_type:
            media_type = "image/png"
        elif "jpeg" in file_type or "jpg" in file_type:
            media_type = "image/jpeg"
        else:
            media_type = "image/png"  # default

        # Use Claude's vision API to analyze the image
        result = _analyze_image_with_claude(client, image_base64, media_type)
        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing image: {str(e)}"
        }


def _analyze_with_claude(client: anthropic.Anthropic, text_content: str) -> Dict[str, Any]:
    """Analyze text content with Claude to extract insurance details"""

    prompt = f"""Analyze this insurance document and extract the following information in a structured format:

1. Plan Name
2. Deductible (Individual and Family if available)
3. Out-of-Pocket Maximum (Individual and Family if available)
4. Copay amounts for:
   - Primary Care Visit
   - Specialist Visit
   - Emergency Room
   - Urgent Care
   - Lab tests
5. Coinsurance percentage
6. In-network vs Out-of-network coverage differences
7. Pharmacy benefits (generic, preferred brand, non-preferred brand)
8. Any other important coverage details

Insurance Document Text:
{text_content}

Please provide:
1. A JSON-like structured response with all the extracted values
2. A plain English summary explaining the coverage
3. Network information
4. Pharmacy benefits details

Format your response clearly with sections for each part."""

    try:
        # Call Claude API
        message = client.messages.create(
            model=os.getenv("CLAUDE_MODEL", "claude-opus-4-5-20251101"),
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Parse Claude's response
        response_text = message.content[0].text

        # Extract structured data from response
        extracted_data = _parse_claude_response(response_text)

        return {
            "success": True,
            **extracted_data,
            "raw_response": response_text
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Claude API error: {str(e)}"
        }


def _analyze_image_with_claude(client: anthropic.Anthropic, image_base64: str, media_type: str) -> Dict[str, Any]:
    """Analyze insurance card image with Claude Vision"""

    prompt = """Analyze this insurance card image and extract all visible information:

1. Plan Name / Insurance Company
2. Member ID
3. Group Number
4. Deductible information (if visible)
5. Copay amounts (if visible on card)
6. Coinsurance (if visible)
7. Phone numbers for customer service
8. Website
9. RxBIN, RxPCN, RxGRP (pharmacy info if visible)
10. Any other coverage details visible on the card

Please provide:
1. All extracted text and numbers
2. A structured summary of the key insurance details
3. A plain English explanation of what this coverage likely includes
4. Note if this appears to be front or back of card, and if you need the other side for complete information

Format your response clearly with sections for each part."""

    try:
        # Call Claude Vision API
        message = client.messages.create(
            model=os.getenv("CLAUDE_MODEL", "claude-opus-4-5-20251101"),
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        # Parse Claude's response
        response_text = message.content[0].text

        # Extract structured data from response
        extracted_data = _parse_claude_response(response_text)

        return {
            "success": True,
            **extracted_data,
            "raw_response": response_text
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Claude Vision API error: {str(e)}"
        }


def _parse_claude_response(response_text: str) -> Dict[str, Any]:
    """Parse Claude's response into structured data"""

    # This is a simplified parser - in production you'd want more robust parsing
    data = {
        "plan_name": "Not found",
        "deductible": "Not found",
        "oop_max": "Not found",
        "copay_primary": "Not found",
        "copay_specialist": "Not found",
        "copay_er": "Not found",
        "copay_urgent_care": "Not found",
        "coinsurance": "Not found",
        "plain_english_summary": response_text,
        "network_info": "",
        "pharmacy_benefits": ""
    }

    # Simple keyword extraction (this could be made more sophisticated)
    lines = response_text.lower().split('\n')

    for line in lines:
        # Extract plan name
        if 'plan name' in line or 'plan:' in line:
            data["plan_name"] = line.split(':')[-1].strip() if ':' in line else "See summary"

        # Extract deductible
        if 'deductible' in line and '$' in line:
            # Try to extract dollar amount
            import re
            amounts = re.findall(r'\$[\d,]+', line)
            if amounts:
                data["deductible"] = amounts[0]

        # Extract OOP max
        if ('out-of-pocket' in line or 'oop max' in line) and '$' in line:
            import re
            amounts = re.findall(r'\$[\d,]+', line)
            if amounts:
                data["oop_max"] = amounts[0]

        # Extract copays
        if 'primary care' in line and ('copay' in line or '$' in line):
            import re
            amounts = re.findall(r'\$[\d,]+', line)
            if amounts:
                data["copay_primary"] = amounts[0]

        if 'specialist' in line and ('copay' in line or '$' in line):
            import re
            amounts = re.findall(r'\$[\d,]+', line)
            if amounts:
                data["copay_specialist"] = amounts[0]

        # Extract coinsurance
        if 'coinsurance' in line and '%' in line:
            import re
            percentages = re.findall(r'\d+%', line)
            if percentages:
                data["coinsurance"] = percentages[0]

    # Extract sections from response
    if "network" in response_text.lower():
        # Try to extract network section
        parts = response_text.split('\n\n')
        for part in parts:
            if 'network' in part.lower() and len(part) > 50:
                data["network_info"] = part
                break

    if "pharmacy" in response_text.lower():
        # Try to extract pharmacy section
        parts = response_text.split('\n\n')
        for part in parts:
            if 'pharmacy' in part.lower() and len(part) > 50:
                data["pharmacy_benefits"] = part
                break

    return data


def answer_coverage_question(coverage_data: Dict[str, Any], question: str) -> str:
    """
    Answer user questions about their coverage using Claude

    Args:
        coverage_data: Extracted coverage information
        question: User's question

    Returns:
        Answer string
    """
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            return "API key not configured. Please set ANTHROPIC_API_KEY in .env file."

        client = anthropic.Anthropic(api_key=api_key)

        # Build context from coverage data
        context = f"""
Insurance Coverage Information:
- Plan: {coverage_data.get('plan_name', 'Unknown')}
- Deductible: {coverage_data.get('deductible', 'Unknown')}
- Out-of-Pocket Max: {coverage_data.get('oop_max', 'Unknown')}
- Primary Care Copay: {coverage_data.get('copay_primary', 'Unknown')}
- Specialist Copay: {coverage_data.get('copay_specialist', 'Unknown')}
- Coinsurance: {coverage_data.get('coinsurance', 'Unknown')}

Full Coverage Summary:
{coverage_data.get('plain_english_summary', '')}

Network Information:
{coverage_data.get('network_info', '')}

Pharmacy Benefits:
{coverage_data.get('pharmacy_benefits', '')}
"""

        prompt = f"""Based on the following insurance coverage information, please answer the user's question clearly and concisely:

{context}

User Question: {question}

Please provide a helpful, accurate answer in 2-3 sentences. If the information needed to answer isn't available in the coverage data, please say so."""

        message = client.messages.create(
            model=os.getenv("CLAUDE_MODEL", "claude-opus-4-5-20251101"),
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return message.content[0].text

    except Exception as e:
        return f"Error answering question: {str(e)}"


def merge_parsed_results(results: list[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge multiple parsed insurance documents into a single comprehensive result

    Args:
        results: List of parsed insurance document results

    Returns:
        Merged dictionary with comprehensive coverage information
    """
    if not results:
        return {"success": False, "error": "No results to merge"}

    if len(results) == 1:
        return results[0]

    # Start with the first result as base
    merged = results[0].copy()

    # Merge data from all documents
    for result in results[1:]:
        # Update with non-empty values
        for key, value in result.items():
            if key == "success":
                continue

            # If current value is empty or "N/A", take new value
            if not merged.get(key) or merged.get(key) == "N/A" or merged.get(key) == "Not found":
                if value and value != "N/A" and value != "Not found":
                    merged[key] = value

            # For lists, merge them
            elif isinstance(value, list) and isinstance(merged.get(key), list):
                # Combine lists and remove duplicates
                merged[key] = list(set(merged[key] + value))

            # For dictionaries, merge them
            elif isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key].update(value)

    # Combine all plain English summaries if multiple
    summaries = [r.get('plain_english_summary', '') for r in results if r.get('plain_english_summary')]
    if len(summaries) > 1:
        merged['plain_english_summary'] = "\n\n---\n\n".join(summaries)

    return merged
