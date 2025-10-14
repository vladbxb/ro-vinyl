"""
Views pentru paginile de info
"""
# Project views
from ro_vinyl import acces
import datetime
from django.http import HttpResponse, HttpRequest, QueryDict
from django.shortcuts import render



def index(request: HttpRequest) -> HttpResponse:
    """Ruta pentru pagina 'index'."""
    return render(request,"ro_vinyl/descriere.html")

def info(request: HttpRequest) -> HttpResponse:
    """Ruta pentru pagina 'info'."""
    lista_parametri = acces.Accesare.lista_parametri(request)
    nume_parametri = [nume_parametru for (nume_parametru, _) in lista_parametri]
    return render(
        request,
        'ro_vinyl/info.html',
        {
            'nr_parametri': len(lista_parametri),
            'nume_parametri': nume_parametri,
        }
    )
#     accesare_noua = _adauga_accesare(request)
#     lista_parametri = accesare_noua.lista_parametri
#     doc = f'''
# <html>
#     <head>
#         <title>Informatii despre server</title>
#     </head>
#     <body>
#         <h1>Informatii despre server</h1>
#         <section>
#             <h2>Parametri</h2>
#             <p>Parametrii primiti: <strong>{len(lista_parametri)}</strong></p>
# '''
#     if len(lista_parametri) > 0:
#         doc += '''
#             <p>Numele parametrilor:
# '''
#         for param_name, _ in lista_parametri:
#             doc += f' {param_name},'
#         # Sterge ultima virgula
#         doc = doc[:-1]
#         doc += '</p>'
#     doc += '''
#     </body>
# </html>
# '''
#     return HttpResponse(doc)

def static_data(request: HttpRequest) -> HttpResponse:
    """Ruta pentru pagina 'data'."""
    data_accesare = datetime.datetime.now()
    return render(
        request,
        'ro_vinyl/data.html',
        {
            'zi': acces.Accesare.formatare_data(data_accesare, acces.DATE_FORMAT_STR),
            'timp': acces.Accesare.formatare_data(data_accesare, acces.TIME_FORMAT_STR),
        }
    )
#     accesare_noua = _adauga_accesare(request)
#     return HttpResponse(
# f'''
# <html>
#     <head>
#         <title>Data si ora</title>
#     </head>
#     <body>
#         <h1>Data si ora</h1>
#         <p>{accesare_noua.data(DATE_FORMAT_STR)}</p>
#         <p>{accesare_noua.data(TIME_FORMAT_STR)}</p>
#     </body>
# </html>
# '''
#     )

def afis_data(request: HttpRequest, data) -> HttpResponse:
    """Ruta pentru pagina 'data', cu url dinamic."""
    acum = datetime.datetime.now()
    zi, timp = None, None
    match data:
        case 'zi':
            zi = acces.Accesare.formatare_data(acum, acces.DATE_FORMAT_STR)
        case 'timp':
            timp = acces.Accesare.formatare_data(acum, acces.TIME_FORMAT_STR)
        case _:
            # This is a no op, because the url for this route
            # blocks any other values, but just in case
            raise ValueError(f"Expected query params 'zi' or 'timp', instead got {data}")
    render(
        request,
        'ro_vinyl/data.html',
        {
            'zi': zi,
            'timp': timp,
        }
    )
#     accesare_noua = _adauga_accesare(request)
#     doc = '''
# <html>
#     <head>
#         <title>Data si ora</title>
#     </head>
#     <body>
#         <h1>Data si ora</h1>
# '''
#     match data:
#         case 'zi':
#             date = accesare_noua.data(DATE_FORMAT_STR)
#             tag_to_concat = f'<p>{date}</p>'
#             doc += tag_to_concat
#         case 'timp':
#             time = accesare_noua.data(TIME_FORMAT_STR)
#             tag_to_concat = f'<p>{time}</p>'
#             doc += tag_to_concat
#         case _:
#             # This is a no op, because the url for this route blocks any other values, but just in case
#             raise ValueError(f"Expected query params 'zi' or 'timp', instead got {data}")
#     doc += '''
#     </body>
# </html>
# '''
#     return HttpResponse(doc)

def craft_log_response(
        accesari_cerute: int,
        iduri: list[str],
        tabel: str | None,
        *,
        total_accesari_cerute: bool,
        detalii_cerute: bool,
        dubluri_cerute: bool
    ) -> HttpResponse:
    """
    Returneaza un HttpResponse pentru log-urile curente ale serverului,
    bazat pe mai multe optiuni care pot fi pasate ca parametrii prin query-string.
    """
    doc = '''
<html>
    <body>
'''
    if total_accesari_cerute:
        doc += f'''
        <p><strong>Au fost cerute {len(acces.accesari)} accesari in total, de la pornirea serverului.</strong></p>
'''
    if len(iduri) > 0:
        accesari_de_parcurs = acces.Accesare.iduri_la_accesari(iduri, dubluri=dubluri_cerute)
    else:
        accesari_de_parcurs = acces.accesari[:min(accesari_cerute, len(acces.accesari))]
    if tabel is not None:
        doc += '''
        <table style="border: 1px solid black; border-collapse: collapse;">
            <tr>
'''
        if tabel == 'tot':
            proprietati_cerute = 'id,ip,url,data'
        else:
            proprietati_cerute = tabel
        # Filtreaza proprietatile de la atributul 'tabel' care nu sunt asteptate de program
        proprietati_str = [proprietate for proprietate in proprietati_cerute.split(',')
                           if proprietate in acces.VALORI_TABEL]
        for proprietate_str in proprietati_str:
            doc += f'''
                <th style="padding: 1em; border: 1px solid black;">{proprietate_str.upper()}</th>
'''
        doc += '''
            </tr>
'''
        for accesare in accesari_de_parcurs:
            # Din cauza ca proprietatile au fost filtrate mai devreme, metoda
            # cere_proprietati() face o asertie la inceput ca lista proprietati_str
            # sigur va contine doar proprietati valide
            proprietati = accesare.cere_proprietati(proprietati_str)
            doc += '''
            <tr>
'''
            for proprietate in proprietati:
                doc += f'''
                <td style="padding: 1em; border: 1px solid black;">{proprietate}</td>
'''
            doc += '''
            </tr>
'''
        doc += '''
        </table>
'''
    elif not detalii_cerute:
        for accesare in accesari_de_parcurs:
            doc += f'''
            <p>Accesarea nr. <strong>{accesare.id + 1}</strong> a fost facuta la pagina {accesare.pagina}</strong></p>
'''
    else:
        for accesare in accesari_de_parcurs:
            doc += f'''
            <p>Accesarea nr. <strong>{accesare.id + 1}</strong>:</p>
            <ul>
                <li>are IP-ul <strong>{accesare.ip_client}</strong></li>
                <li>a accesat url-ul <strong>{accesare.url}</strong></li> 
                <ul>
                    <li>pe data: <strong>{accesare.data(acces.DATE_FORMAT_STR)}</strong></li>
                    <li>la ora: <strong>{accesare.data(acces.TIME_FORMAT_STR)}</strong></li>
                </ul>
            </ul>
 '''
    cmp_accesata_pagina = acces.Accesare.frecv_pagina(cea_mai_accesata=False)
    cmm_accesata_pagina = acces.Accesare.frecv_pagina(cea_mai_accesata=True)
    doc += f'''
            <p>Cea mai putin accesata pagina este: <strong>{cmp_accesata_pagina}</strong></p>
'''
    doc += f'''
            <p>Cea mai mult accesata pagina este: <strong>{cmm_accesata_pagina}</strong></p>
'''
    if accesari_cerute > len(accesari):
        doc += f'''
            <p><strong>Exista doar <span style="color: green;">{len(accesari)}</span> accesari fata de <span style="color: red;">{accesari_cerute}</span> accesari cerute</strong></p>'''
    doc += '''
    </body>
</html>
'''
    return HttpResponse(doc)

def log(request: HttpRequest) -> HttpResponse:
    """Ruta pentru pagina 'log'."""
    ultimele = request.GET.get('ultimele')
    if ultimele:
        # Se alege 0 ca valoare minima ca un sanity-check
        # pentru numere negative
        ultimele = max(int(ultimele), 0)
    else:
        ultimele = len(accesari)
    iduri = request.GET.getlist('iduri')
    tabel = request.GET.get('tabel')
    cerere_accesari = request.GET.get('accesari')
    cerere_dubluri = request.GET.get('dubluri')
    
#     _adauga_accesare(request)
#     ultimele = request.GET.get('ultimele')
#     if ultimele:
#         # Se alege 0 ca valoare minima ca un sanity-check
#         # pentru numere negative
#         ultimele = max(int(ultimele), 0)
#     else:
#         ultimele = len(accesari)
#     iduri = request.GET.getlist('iduri')
#     tabel = request.GET.get('tabel')
#     cerere_accesari = request.GET.get('accesari')
#     cerere_dubluri = request.GET.get('dubluri')
#     return craft_log_response(
#         ultimele,
#         iduri,
#         tabel,
#         total_accesari_cerute=cerere_accesari=='nr',
#         detalii_cerute=cerere_accesari=='detalii',
#         dubluri_cerute=cerere_dubluri=='true'
#     )
