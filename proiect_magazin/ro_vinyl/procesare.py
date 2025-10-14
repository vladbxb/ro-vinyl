# In acest middleware pur si simplu pot stoca accesarile si sa mut diversi helperi din views.py aici. Adica practic sa cuplez mai mult implementarile din views.py de acest middleware pentru tema 2 de laborator (sau task 2 cred ca se numea)
# https://docs.google.com/document/d/1lDJNvhsuVYqGF2KrQ4l7iRXq73-Mh_7WqoPhMseWkYU/edit?tab=t.0#heading=h.xifb2bxbc7q4

from django.http import HttpRequest, HttpResponse
from ro_vinyl import acces

class MiddlewareNou:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        # cod de procesare a cererii ....
        # putem trimite date către funcția de vizualizare; le setăm ca proprietăți în request
        # request.proprietate_noua=17
        # se apelează (indirect) funcția de vizualizare (din views.py)
        response = self.get_response(request)

        # putem adauga un header HTTP pentru toate răspunsurile
        response['header_nou'] = 'valoare'
        # aici putem modifica chiar conținutul răspunsului
        # verificăm tipul de conținut folosind headerul HTTP Content-Type
        # motivul fiind că putem transmite și alte resurse (imagini, css etc.), nu doar fișiere html
        if response.has_header('Content-Type') and 'text/html' in response['Content-Type']:
           
            # obținem conținutul
            # (response.content este memorat ca bytes, deci îl transformăm în string)
            content = response.content.decode('utf-8')
           
            # Modificăm conținutul
            # new_content = content.replace(
            #     '</body>',
            #     '<div>Continut suplimentar</div></body>'
            # )
           
            # Suprascriem conținutul răspunsului
            # response.content = new_content.encode('utf-8')

            # response.content = 'buna eu sunt response content'
            
            # Actualizăm lungimea conținutului (obligatoriu, fiind header HTTP)
            response['Content-Length'] = len(response.content)
       
        return response
   
    @staticmethod
    def adauga_accesare(request: HttpRequest):
        """Helper pentru adaugat o accesare noua."""
        accesare_noua = acces.Accesare(request)
        acces.accesari.append(accesare_noua)
        return accesare_noua
