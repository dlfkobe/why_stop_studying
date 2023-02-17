from django.shortcuts import render,HttpResponse
from chat.chatWithRobot import ChatBotGraph
handler = ChatBotGraph()
# Create your views here.
def test(request):
    if request.method == 'POST':
        return HttpResponse("请使用get")
    
    question = request.GET.get("word")
    print(question)
    answer = handler.chat_main(question)
    print(answer)
    print("shdjkash")
    return HttpResponse(answer)