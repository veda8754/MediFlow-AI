def get_demo_analysis(enquiry):

    text = enquiry.lower()

    # Default classification
    category = "General Enquiry"
    sentiment = "Neutral"
    priority = "Medium"
    requires_followup = False

    summary = "Patient has submitted a general enquiry."

    response = (
        "Thank you for contacting our clinic. "
        "Our team will review your enquiry and assist you shortly."
    )

    # Appointment booking
    if "appointment" in text or "book" in text:

        category = "Appointment Booking"
        summary = "Patient is enquiring about booking an appointment."

        response = (
            "Thank you for your interest in booking an appointment. "
            "Our clinic team will contact you to assist with scheduling."
        )

        requires_followup = True

    # Cancellation
    elif "cancel" in text:

        category = "Appointment Cancellation"
        summary = "Patient wants assistance with appointment cancellation."

        response = (
            "We have received your cancellation request. "
            "Our clinic team will review it and assist you."
        )

        requires_followup = True

    # Billing
    elif "payment" in text or "bill" in text or "refund" in text:

        category = "Billing & Payments"
        summary = "Patient has a billing or payment-related enquiry."

        response = (
            "Thank you for contacting us regarding your payment. "
            "Our billing team will review your enquiry and assist you."
        )

        requires_followup = True

    # Insurance
    elif "insurance" in text:

        category = "Insurance"
        summary = "Patient has an insurance-related enquiry."

        response = (
            "Thank you for your insurance enquiry. "
            "Our administrative team will assist you with the relevant information."
        )

        requires_followup = True

    # Negative sentiment
    if any(word in text for word in ["angry", "unhappy", "complaint", "waiting", "frustrated"]):

        sentiment = "Negative"
        priority = "High"
        requires_followup = True

    # Positive sentiment
    elif any(word in text for word in ["thank you", "happy", "excellent", "great"]):

        sentiment = "Positive"

    return {
        "category": category,
        "sentiment": sentiment,
        "priority": priority,
        "summary": summary,
        "requires_followup": requires_followup,
        "suggested_response": response
    }