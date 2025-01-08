import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from langchain_groq import ChatGroq
from markdown import markdown
from backend.faisca.models import Chat



os.environ['GROQ_API_KEY'] = settings.GROQ_API_KEY


def get_chat_history(chats):
   chat_history = []
   for chat in chats:
      chat_history.append(
         ('human', chat.message,)
         )
      chat_history.append(
         ('ai', chat.response,)
         )
   return chat_history

def ask_ai(context, message):
   model = ChatGroq(model='llama-3.2-90b-vision-preview')
   messages = [   
   (
      'system',
      'Você é um assistente , chamado Faísca, responsável por tirar dúvidas sobre Normas, Regulamentos e Legislações sobre a PM e CB.'
      'Responda em formato markdown.',
   ),
   ]
   messages.extend(context)
   messages.append(
      (
         'human',
         message,
       ),
   )
   print(messages)
   response = model.invoke(messages)
   return markdown(response.content, output_format='html')


@login_required
def chatbot(request):
   chats = Chat.objects.filter(user=request.user)

   if request.method == 'POST':
       context = get_chat_history(
         chats=chats,
         )
       message = request.POST.get('message')
       response = ask_ai(
         context=context,
         message=message,
       )
       chat = Chat(
        user=request.user,
         message=message,
         response=response,
       )
       chat.save()
       return JsonResponse({
         'message': message,
         'response': response,
    })
   return render(request, 'chatbot.html', {'chats': chats})

def reset_chat(request):
    if request.method == 'POST':
        Chat.objects.filter(user=request.user).delete()  # Delete chat history
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def reset_and_redirect(request):
    if request.method == 'POST':
        Chat.objects.filter(user=request.user).delete()  # Delete chat history
        return redirect('faisca:chatbot')  # Redirect to chatbot page
    return JsonResponse({'success': False})