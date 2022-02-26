from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.sessions.models import Session
from .gui import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class Message(APIView):

	def get(self, request):
		msg = request.GET.get('text')
		response = chatbot_response(msg)
		print(response)
		valid=validators.url(response)
		if valid==True:
			data1 = 'True'
			data = {
			'respond': response,'respond1':data1
			}
			return Response(data)
		else:
			data1 = 'False'
			data = {
			'respond': response,'respond1':data1
			}
			return Response(data)
		

		#return HttpResponse('data')


	def clean_up_sentence(sentence):
		sentence_words = nltk.word_tokenize(sentence)
		sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
		return sentence_words

	def bow(sentence, words, show_details=True):
		sentence_words = clean_up_sentence(sentence)
		bag = [0] * len(words)
		for s in sentence_words:
			for i, w in enumerate(words):
				if w == s:
					bag[i] = 1
					if show_details:
						print("found in bag: %s" % w)
		return (np.array(bag))


	def predict_class(sentence, model):
		p = bow(sentence, words, show_details=False)
		print(p)
		res = model.predict(np.array([p]))[0]
		print(res)
		ERROR_THRESHOLD = 0.25
		results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
		results.sort(key=lambda x: x[1], reverse=True)
		return_list = []
		for r in results:
			return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
		return return_list

	def getResponse(ints, intents_json):
		tag = ints[0]['intent']
		list_of_intents = intents_json['intents']
		for i in list_of_intents:
			if (i['tag'] == tag):
				result = random.choice(i['responses'])
				print(result)
				break
		return result

	def chatbot_response(msg):
		ints = predict_class(msg, model)
		res = getResponse(ints, intents)
		print(res)
		
		return res
