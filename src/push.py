import http.client, urllib


def pushover(message):
    # Need to pay
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", 
                 "/1/messages.json",
                urllib.parse.urlencode({
                    "token": "an2z5m5b62f5ykpnjzoh3rjyaocojc",
                    "user": "u7ff9zbv33xaomy4uvqhc93c36dbo6",
                    "message": message,
                }), 
                { "Content-type": "application/x-www-form-urlencoded" })
    return conn.getresponse().status

if __name__ == '__main__':
    print(pushover('hello') == 200)