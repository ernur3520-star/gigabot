# logic to verify PDF receipt using Gemini or other ML

from config import Settings

settings = Settings()


def check_payment(image_bytes: bytes) -> bool:
    """Placeholder for payment check. In real implementation, use Gemini to analyze image."""
    # TODO: implement OCR and validation
    return True  # Simulate success


def verify_receipt(pdf_bytes: bytes, expected_amount: int, card: str):
    """Analyze the binary contents of a PDF receipt and ensure that:

    * the total amount matches `expected_amount`
    * the date is today's date and not older than 15 minutes
    * the recipient card number matches `card`
    * the receipt hasn't already been used (lookup in database)

    The implementation can use Gemini's document understanding or a custom
    OCR pipeline; for now the function returns a placeholder.

    Returns a dict: {'valid': bool, 'reason': str}
    """
    # TODO: implement
    return {'valid': True, 'reason': 'Placeholder'}
    # TODO: integrate with Gemini 1.5 Flash via its REST API
    return {"valid": False, "reason": "not implemented"}
