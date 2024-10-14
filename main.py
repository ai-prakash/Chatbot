from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db import init_db, add_order, remove_order, complete_order, track_order

app = FastAPI()

# Initialize the database
init_db()

@app.post("/dialogflow")
async def dialogflow_webhook(request: Request):
    data = await request.json()
    # Get intent from Dialogflow
    intent = data['queryResult']['intent']['displayName']
    
    # Handle different intents
    if intent == "newOrder":
        response = add_order(data)
    elif intent == "removeOrder":
        response = remove_order(data)
    elif intent == "completeOrder":
        response = complete_order(data)
    elif intent == "trackOrder":
        response = track_order(data)
    else:
        # Default response if the intent is not handled
        response = {"fulfillmentText": "Sorry, I didn't understand that request."}
    
    # Return the response as JSON
    return JSONResponse(content=response)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
