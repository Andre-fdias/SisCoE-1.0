import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from langchain_groq import ChatGroq
from markdown import markdown
from backend.faisca.models import Chat
from datetime import datetime
import pytz



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
        ('system', 
         'Você é Faisca AI, um assistente virtual especializado em responder dúvidas sobre Normas e Regras da Polícia Militar do Estado de São Paulo (PMESP) e do Corpo de Bombeiros (CB).'
         ' Sua função é fornecer informações precisas e claras, sempre em formato markdown.'
         ' Além disso, você deve manter o contexto das conversas para oferecer respostas mais relevantes.'
         ' Se necessário, consulte documentos específicos internos para fornecer a melhor resposta possível.'
         ' Lembre-se de sempre chamar o usuario de Sr. sendo sempre educado e profissional em suas respostas.'
         ),
(
      'human',
      message,
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
        context = get_chat_history(chats=chats)
        message = request.POST.get('message')
        response = ask_ai(context=context, message=message)
        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=get_local_time()  # Usar o horário local para o campo created_at
        )
        chat.save()

        return JsonResponse({
            'message': message,
            'response': response,
        })
    return render(request, 'chatbot.html', {'chats': chats})




# Função para obter o horário local
def get_local_time():
    local_tz = pytz.timezone('America/Sao_Paulo')
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    local_now = utc_now.astimezone(local_tz)
    return local_now

# Função para formatar o histórico de chat com os horários corretos
def format_chat_history(chats):
    formatted_history = []
    for chat in chats:
        created_at_local = chat.created_at.astimezone(pytz.timezone('America/Sao_Paulo'))
        formatted_history.append({
            'message': chat.message,
            'response': chat.response,
            'created_at': created_at_local.strftime('%Y-%m-%d %H:%M:%S')
        })
    return formatted_history


@login_required
def chat_history(request):
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')
    history = format_chat_history(chats)
    return JsonResponse({'history': history})