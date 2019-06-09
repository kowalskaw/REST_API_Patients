import http.client
import json


def print_response(response):
    print("Response: " + response.read().decode('utf-8') + '\n')
    # print("Status: " + str(response.status))
    # print("Reason: " + str(response.reason) + "\n")


def test_methods(method, path):
    connection = http.client.HTTPConnection('localhost', 80, timeout=10)
    connection.request(method, path)
    response = connection.getresponse()
    print_response(response)
    connection.close()


def test_json(method, path, json_data):
    conn = http.client.HTTPConnection('localhost', 80, timeout=10)
    conn.request(method, path, json_data)
    response = conn.getresponse()
    print_response(response)
    conn.close()


if __name__ == '__main__':
    patient1 = '''
    {
        "patient_id": "123",
        "name": "Werka"
    }
    '''
    patient2 = '''
        {
            "patient_id": "456",
            "name": "Marcel"
        }
    '''

    test_methods("GET", "/")
    test_methods("GET", "/werka")
    test_json('POST', "/werka/poznan/add", patient1)
    test_json('POST', "/werka/poznan/add", patient2)

    test_methods('GET', '/werka/poznan/patients')
    test_methods('GET', '/werka/poznan/123')
