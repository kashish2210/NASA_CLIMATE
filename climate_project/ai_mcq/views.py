from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import google.generativeai as genai
import os
import json
apiKey = "AIzaSyA2i4KZU4YzGty_GN0-obC07e_ufWPlxdg"
def mcqs(request):
    return render(request, 'mcqs.html')


def getMcqs(request):
    raw_data = request.body
    article_dict = json.loads(raw_data.decode('utf-8'))
    article = article_dict.get("article")
    
    prompt =  "can you ask me five mcq questions based on this article:" + article + '''Each question should be in dictionary format and all the question should be in the list:
{"question": "generated question",
"option_1": "generated option-1",
"option_2": "generated option-2",
"option_3": "generated option-3",
"option_4": "generated option-4",
"answer": "the correct answer(like this 1, 2, 3, 4)"}
i am going to use the result of this prompt in webapp so only provide five question nothing else.'''

    genai.configure(api_key=apiKey)
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(prompt)

    questions = json.loads(response.text[8:-3])
    

    jsonResult = {"questionList" : questions}
    print(jsonResult)
    
    return JsonResponse(jsonResult)
