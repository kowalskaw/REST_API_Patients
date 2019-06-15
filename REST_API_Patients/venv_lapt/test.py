import http.client
import requests
import json


# raport, caly kod w pliku z raportem, komentarze w kodzie, prezentowanie endpointow, metody,
# na endpointach, kody statusu, koncepty ze swiata rzeczyiwstego (resources)
# pola naglowkowe! -> apllication JSON
def print_response(response):
    print("Response: " + response.read().decode('utf-8') + '\n')
    print("Status: " + str(response.status))
    print("Reason: " + str(response.reason) + "\n")


# returns a token for an employee
def login(method, url, body,  headers, connection):
    connection.request(method, url, body, headers)
    return connection.getresponse()


if __name__ == '__main__':
    connection = http.client.HTTPConnection('localhost', 80, timeout=10)

    # body
    patient1 = {"name": "Slon", "surname": "Trabalski", "age": "10", "ward": "oddzial", "diagnosis": "diagnoza"}
    patient2 = {"name": "Bolek", "surname": "Bajkowy", "age": "30", "ward": "oddzial", "diagnosis": "diagnoza"}
    patient3 = {"name": "Lolek", "surname": "Bajkowy", "age": "31", "ward": "oddzial", "diagnosis": "diagnoza"}
    patient4 = {"name": "Krzys", "surname": "Mis", "age": "50", "ward": "oddzial", "diagnosis": "diagnoza"}

    employee1 = {"name": "Werka", "surname": "Koderka", "password": "werka"}
    employee2 = {"name": "Anna", "surname": "Nowak", "password": "anna"}

    # (method, url, body=None, headers={}, *, encode_chunked=False)
    # requests.get(url, headers={'Authorization': 'GoogleLogin auth=%s' % authorization_token})
    # headers = {'Authorization': 'Basic QWRtaW46YWRtaW4=' % authorization_token}
    # login('GET', '/login', body=None, )

    conn.close()
