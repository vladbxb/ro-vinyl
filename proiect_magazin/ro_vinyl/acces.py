import datetime
from django.http import HttpRequest, QueryDict

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

class Accesare:
    """Clasa pentru a tine evidenta de accesarea unei pagini."""
    id_curent = 0
    def __init__(self, request: HttpRequest):
        self.id = Accesare.id_curent
        Accesare.id_curent += 1
        self.request = request
        self.ip_client = _client_ip_address(request)
        self.data_accesare = datetime.datetime.now()
    @staticmethod
    def lista_parametri(request: HttpRequest) -> list[tuple[str, str | int]]:
        """
        Returneaza o lista de tupluri formate din perechi cheie-valoare a parametrilor ceruti.
        Exemplu: ?a=10&b=1&c=2 in url -> [(a, 10), (b, 1), (c, 2)]
        """
        url = Accesare.url(request)
        if '?' not in url:
            return []
        query_string = url.split('?')[1]
        return list(QueryDict(query_string).items())
    @staticmethod
    def url(request: HttpRequest) -> str:
        """
        Returneaza path-ul si query-string-ul
        Exemplu: /log/?ultimele=10
        """
        return request.get_full_path()
    @property
    def pagina(self) -> str:
        """Returneaza numele paginii fara domeniu sau query-string."""
        return self.request.path
    @staticmethod
    def formatare_data(data_accesare: datetime.datetime, format_str: str) -> str:
        """Returneaza data accesarii in formatul specificat"""
        return datetime.datetime.strftime(data_accesare, format_str)
    def cere_proprietati(self, proprietati: list[str]) -> tuple:
        """
        Construieste lista de valori ale proprietatilor,
        in ordinea in care au fost cerute, din obiectul Accesare.
        """
        id, ip, url, data, ora, pagina = None, None, None, None, None, None
        for proprietate in proprietati:
            assert proprietate in VALORI_TABEL
            match proprietate:
                case 'id':
                    id = self.id
                case 'ip':
                    ip = self.ip_client
                case 'url':
                    url = Accesare.url(self.request)
                case 'data':
                    # rezultat.append(self.data(DATE_FORMAT_STR))
                    data = Accesare.formatare_data(self.data_accesare, DATE_FORMAT_STR)
                    print(data)
                case 'ora':
                    # rezultat.append(self.data(TIME_FORMAT_STR))
                    ora = Accesare.formatare_data(self.data_accesare, TIME_FORMAT_STR)
                    print(ora)
                case 'pagina':
                    pagina = self.pagina
                    print(pagina)
        return (id, ip, url, data, ora, pagina)
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
    cnt, rez = 0, str()
    for elem in accesari:
        elem_url = Accesare.url(elem.request)
        frecv[elem_url] = frecv.get(elem_url, 0) + 1
        if frecv[elem_url] >= cnt:
            cnt, rez = frecv[elem_url], elem_url
    if cea_mai_accesata:
        return rez if isinstance(rez, str) else str()
    cnt = max(frecv.values())
    rez = str()
    for url, fv in frecv.items():
        if fv <= cnt:
            rez, cnt = url, fv
    return rez if isinstance(rez, str) else str()

accesari: list[Accesare] = []
