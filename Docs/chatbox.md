# CHATBOT

It is a user interface widget, typically located in a corner of a webpage, that enables real-time text communication between a website visitor and a company representative or an AI bot

---

## Chatbot vs Chatbox

### Chatbot

The logic that reads messages and returns responses. It's the software/logic behind the conversation

Located in ```routes/chat.py```

### Chatbox

In the frontend, it is the UI widget the customer types into

--- 

## Types of chatbots

#### 1. Rule-based
use predefined scripts, keywords, and decision trees to interact with users, making them highly efficient for FAQ, scheduling, and structured, repetitive tasks. They follow specific, pre-programmed rules rather than AI to identify keywords, making them cost-effective and easy to deploy for straightforward, predictable conversational flows. 

Three parts of this chatbot
1. Triggers: Keywords
2. Responses: what to reply when a trigger matches
3. Fallback: what to sya when nothing matches

#### 2. AI/NLP powered
They are software applications that use Natural Language Processing (NLP) to understand, interpret, and respond to human language in a natural, conversational manner, moving beyond simple keyword matching. These systems, which include both conversational AI and Generative AI, enhance customer service by providing 24/7 availability, scalability, and improved accuracy through understanding intent and sentiment.

#### 3. Hybrid
It combines rule-based automation with AI-driven adaptability (NLP/LLM), offering structured, reliable responses for routine inquiries while intelligently handling complex, conversational queries. By seamlessly escalating to human agents when necessary, they provide 24/7 service, reduced costs, and improved customer experience. 

---

## 🧪 Testing Your Flask Chatbot with Postman

#### 1. Set Request Type
Method: POST
URL:
http://127.0.0.1:5000/chat


#### 2. Add Headers

Go to the Headers tab and add:

```Content-Type: application/json```


#### 3. Add Request Body

Go to Body → raw → JSON and use:

```
{
  "message": "do you deliver"
}
```

#### 4. Send Request

```
Click Send.
```

#### 5. Expected Response

You should receive a response like:

```
{
  "response": "Yes we do! 🚚 Nairobi deliveries take 1-2 days and countrywide takes 3-5 days via G4S."
}
```

#### 6. Test Multiple Inputs

Try different messages to verify chatbot behavior:

```
{ "message": "hi" }
{ "message": "what do you sell" }
{ "message": "how do i pay" }
{ "message": "random text" }
```

---

