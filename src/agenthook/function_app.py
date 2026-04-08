import azure.functions as func
import logging
import json

app = func.FunctionApp()

@app.route(route="telnyx_webhook", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def telnyx_webhook(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Telnyx webhook received a request.')

    try:
        # Parse the JSON payload sent by Telnyx
        req_body = req.get_json()
        data = req_body.get('data', {})
        
        # Extract the message text and sender
        if data.get('event_type') == 'message.received':
            payload = data.get('payload', {})
            msg_text = payload.get('text')
            sender = payload.get('from', {}).get('phone_number')
            
            logging.info(f"Message from {sender}: {msg_text}")
            
        # Telnyx requires a 2xx response within 2-5 seconds
        return func.HttpResponse("OK", status_code=200)
        
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)
