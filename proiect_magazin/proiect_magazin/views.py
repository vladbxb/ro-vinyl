"""
Views pentru proiect
"""
# Project views
import datetime
from django.http import HttpResponse, HttpRequest, QueryDict

# Format string for the datetime object
# %A - day as full name
# %d - day in date
# %B - month as full name
# %Y - year with decade prefix
# Formats into something like
# Thursday, 2 October 2025
DATE_FORMAT_STR = '%A, %d %B %Y'
# %H - hours in 24-hour format
# %M - minutes
# %S - seconds
# 12:40:22
TIME_FORMAT_STR = '%H:%M:%S'

# Valori valide pentru proprietatea 'tabel' din url
VALORI_TABEL = ('id', 'ip', 'url', 'data', 'ora', 'pagina')

class Accesare:
    """Clasa pentru a tine evidenta de accesarea unei pagini."""
    id_curent = 0
    def __init__(self, request: HttpRequest):
        self.id = Accesare.id_curent
        Accesare.id_curent += 1
        self.request = request
        self.ip_client = _client_ip_address(request)
        self.data_accesare = datetime.datetime.now()
    @property
    def lista_parametri(self) -> list[tuple[str, str | int]]:
        """
        Returneaza o lista de tupluri formate din perechi cheie-valoare a parametrilor ceruti.
        Exemplu: ?a=10&b=1&c=2 in url -> [(a, 10), (b, 1), (c, 2)]
        """
        if '?' not in self.url:
            return []
        query_string = self.url.split('?')[1]
        return list(QueryDict(query_string).items())
    @property
    def url(self) -> str:
        """
        Returneaza path-ul si query-string-ul
        Exemplu: /log/?ultimele=10
        """
        return self.request.get_full_path()
    @property
    def pagina(self) -> str:
        """Returneaza numele paginii fara domeniu sau query-string."""
        return self.request.path
    def data(self, format_str) -> str:
        """Returneaza data accesarii in formatul specificat"""
        return datetime.datetime.strftime(self.data_accesare, format_str)
    def cere_proprietati(self, proprietati: list[str]) -> list:
        """
        Construieste lista de valori ale proprietatilor,
        in ordinea in care au fost cerute, din obiectul Accesare.
        """
        rezultat = []
        for proprietate in proprietati:
            assert proprietate in VALORI_TABEL
            match proprietate:
                case 'id':
                    rezultat.append(self.id)
                case 'ip':
                    rezultat.append(self.ip_client)
                case 'url':
                    rezultat.append(self.url)
                case 'data':
                    rezultat.append(self.data(DATE_FORMAT_STR))
                case 'ora':
                    rezultat.append(self.data(TIME_FORMAT_STR))
                case 'pagina':
                    rezultat.append(self.pagina)
        return rezultat
accesari: list[Accesare] = []

def _adauga_accesare(request: HttpRequest) -> Accesare:
    """Helper pentru adaugat o accesare noua."""
    accesare_noua = Accesare(request)
    accesari.append(accesare_noua)
    return accesare_noua

def _client_ip_address(request: HttpRequest) -> str:
    """Helper pentru obtinut adresa IP a clientului dintr-un HttpRequest."""
    # https://how.dev/answers/how-to-get-the-user-ip-address-in-django
    req_headers = request.META
    x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for_value:
        ip_addr = x_forwarded_for_value.split(',')[-1].strip()
    else:
        ip_addr = req_headers.get('REMOTE_ADDR')
    if ip_addr is None:
        raise RuntimeError('Fetching client IP address from HttpRequest yielded None')
    return ip_addr

def index(request: HttpRequest) -> HttpResponse:
    """Ruta pentru pagina 'index'."""
    _adauga_accesare(request)
    return HttpResponse('''
                        Descriere: 
                        Proiectul consta intr-un site pentru un magazin de discuri de vinil. 
                        Utilizatorii acestui site pot consulta catalogul magazinului, pot achizitiona discuri si pot vedea recenziile altor utilizatori.
                        ''')

def info(request: HttpRequest) -> HttpResponse:
    """Ruta pentru pagina 'info'."""
    accesare_noua = _adauga_accesare(request)
    lista_parametri = accesare_noua.lista_parametri
    doc = f'''
<html>
    <head>
        <title>Informatii despre server</title>
    </head>
    <body>
        <h1>Informatii despre server</h1>
        <section>
            <h2>Parametri</h2>
            <p>Parametrii primiti: <strong>{len(lista_parametri)}</strong></p>
'''
    if len(lista_parametri) > 0:
        doc += '''
            <p>Numele parametrilor:
'''
        for param_name, _ in lista_parametri:
            doc += f' {param_name},'
        # Sterge ultima virgula
        doc = doc[:-1]
        doc += '</p>'
    doc += '''
    </body>
</html>
'''
    return HttpResponse(doc)

def static_data(request: HttpRequest) -> HttpResponse:
    """Ruta pentru pagina 'data'."""
    accesare_noua = _adauga_accesare(request)
    return HttpResponse(
f'''
<html>
    <head>
        <title>Data si ora</title>
    </head>
    <body>
        <h1>Data si ora</h1>
        <p>{accesare_noua.data(DATE_FORMAT_STR)}</p>
        <p>{accesare_noua.data(TIME_FORMAT_STR)}</p>
    </body>
</html>
'''
    )

def afis_data(request: HttpRequest, data) -> HttpResponse:
    """Ruta pentru pagina 'data', cu url dinamic."""
    accesare_noua = _adauga_accesare(request)
    doc = '''
<html>
    <head>
        <title>Data si ora</title>
    </head>
    <body>
        <h1>Data si ora</h1>
'''
    match data:
        case 'zi':
            date = accesare_noua.data(DATE_FORMAT_STR)
            tag_to_concat = f'<p>{date}</p>'
            doc += tag_to_concat
        case 'timp':
            time = accesare_noua.data(TIME_FORMAT_STR)
            tag_to_concat = f'<p>{time}</p>'
            doc += tag_to_concat
        case _:
            raise ValueError(f"Expected query params 'zi' or 'data', instead got {data}")
    doc += '''
    </body>
</html>
'''
    return HttpResponse(doc)

def iduri_la_accesari(iduri: list[str], *, dubluri: bool) -> list[Accesare]:
    """
    Returneaza o lista de obiecte de tip Accesare
    formate dupa o lista de iduri.
    """
    assert len(iduri) > 0
    iduri_split_de_virgula = [s.split(',') for s in iduri]
    iduri_deimbricate = [s for iduri in iduri_split_de_virgula for s in iduri]
    iduri_parsate_gen = (int(s) - 1 for s in iduri_deimbricate)
    if dubluri:
        iduri_de_parcurs = list(iduri_parsate_gen)
    else:
        iduri_de_parcurs = list(set(iduri_parsate_gen))
    for idx in iduri_de_parcurs:
        if idx >= len(accesari) or idx < 0:
            raise ValueError(f'Accesarea cu id-ul {idx + 1} din iduri cerute nu exista!')
    accesari_de_parcurs = [accesari[idx] for idx in iduri_de_parcurs]
    return accesari_de_parcurs

def frecv_pagina(*, cea_mai_accesata: bool) -> str:
    """
    Returneaza cea mai frecventata sau cea mai putin frecventata pagina
    in functie de parametru.
    """
    frecv = {}
    cnt, rez = 0, ''
    for elem in accesari:
        frecv[elem.url] = frecv.get(elem.url, 0) + 1
        if frecv[elem.url] >= cnt:
            cnt, rez = frecv[elem.url], elem.url
    if cea_mai_accesata:
        return rez
    else:
        cnt = max(frecv.values())
        rez = ''
        for url, fv in frecv.items():
            if fv <= cnt:
                rez, cnt = url, fv
    return rez


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
        <p><strong>Au fost cerute {len(accesari)} accesari in total, de la pornirea serverului.</strong></p>
'''
    if len(iduri) > 0:
        accesari_de_parcurs = iduri_la_accesari(iduri, dubluri=dubluri_cerute)
    else:
        accesari_de_parcurs = accesari[:min(accesari_cerute, len(accesari))]
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
        proprietati_str = [proprietate for proprietate in proprietati_cerute.split(',') if proprietate in VALORI_TABEL]
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
                    <li>pe data: <strong>{accesare.data(DATE_FORMAT_STR)}</strong></li>
                    <li>la ora: <strong>{accesare.data(TIME_FORMAT_STR)}</strong></li>
                </ul>
            </ul>
 '''
    cmp_accesata_pagina = frecv_pagina(cea_mai_accesata=False)
    cmm_accesata_pagina = frecv_pagina(cea_mai_accesata=True)
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
    _adauga_accesare(request)
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
    return craft_log_response(
        ultimele,
        iduri,
        tabel,
        total_accesari_cerute=cerere_accesari=='nr',
        detalii_cerute=cerere_accesari=='detalii',
        dubluri_cerute=cerere_dubluri=='true'
    )
