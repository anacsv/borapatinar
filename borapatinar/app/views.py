from urllib import response
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.conf import settings



class RollerbladeWeather(APIView):
   def get(self, request):

        req = self.get_data_from_external_api()

        list = self.handle_data(req)

        temp = self.get_temp(list)
        
        humidity = list['currentConditions']['humidity']
        windspeed = list['currentConditions']['windspeed']
        datetime = list['currentConditions']['datetime']
        conditions = list['currentConditions']['conditions']
        
        verdict = self.get_verdict(temp, humidity, windspeed)

        return Response(self.get_response(temp, humidity, windspeed, datetime, conditions, verdict))

   def get_response(self, temp, humidity, windspeed, datetime, conditions, verdict):
       infos_dict = {
            "verdict" : verdict,
            "temperature" : "%.1f" % temp,
            "humidity": humidity,
            "windspeed" : windspeed,
            "time" : datetime,
            "local" : "Matosinhos",
            "conditions" : conditions,
        }
       
       return infos_dict

   def get_verdict(self, temp, humidity, windspeed):
       verdict = ""
        
       if temp < 35 and humidity < 70 and windspeed < 20:
           verdict = "Yes, lets go!"
       else:
           verdict = "No, climate conditions not good!"
       return verdict

   def get_temp(self, list):
       temp = list['currentConditions']['temp']
       temp = (temp - 32) / 1.8
       return temp

   def handle_data(self, req):
       try:
           list = req.json()
       except ValueError:
           print("A resposta não chegou com o formato esperado.")
       return list

   def get_data_from_external_api(self):       
       api = f"{settings.VISUALCROSSING_API_ENDPOINT}{settings.VISUALCROSSING_API_LAT_LON}?key={settings.VISUALCROSSING_API_KEY}"
       req = requests.get(api)
       return req

