from django.shortcuts import render
from django.http import JsonResponse
import openai
import elevenlabs

openai_api_key = '****'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        message="first translate then answer this in english and answer like your text:.... ,response:......"+message
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')


def pronunciation(request):
    if request.method == 'POST':
        elevenlabs.set_api_key("****")
        voice = elevenlabs.Voice(
            voice_id="ZQe5CZNOzWyzPSCn5a3c",
            settings=elevenlabs.VoiceSettings(
                stability=0,
                similarity_boost=0.75
            )
        )

        response_text = request.POST.get('response')
        
        audio = elevenlabs.generate(
            text=response_text,
            voice=voice
        )
        elevenlabs.play(audio)

    return JsonResponse({'status': 'success'})


