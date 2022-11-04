"""
PAWPRINTS-WEBSCRAPER

This module spoofs the websocket request, and receives the pawprints raw data in string form.

Author: Carter4242
https://github.com/Carter4242
"""


from websocket import create_connection
import format
import json


def scrapeAll () -> list:
    """
    Spoofs(?) a websocket open request, and sends a request for all petitions.
    The first message received is the default 33 or so length string of petitions. The second will be the actual request.

    :return: Completed Petition list
    :rtype: list
    """

    # Spoofed request basically just pasted from browser. 
    # User-Agent + Sec-WebSocket-Key modified, cookie line deleted.
    headers = json.dumps({
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'Upgrade',
        'Host': 'pawprints.rit.edu',
        'Origin': 'https://pawprints.rit.edu',
        'Pragma': 'no-cache',
        'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
        'Sec-WebSocket-Key': 'https://github.com/Carter4242/Pawprints-Webscraper', # Modified
        'Sec-WebSocket-Version': '13',
        'Upgrade': 'websocket',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    })


    print("\nCreating Connection")

    # Launch the connection to the server.
    # Perform the handshake.
    ws = create_connection('wss://pawprints.rit.edu/ws/', headers=headers)

    # ws.send(json.dumps({"command": "get", "id": 7})) - Unused
    #ws.send(json.dumps({"command":"paginate","sort":"most recent","filter":"all","page":1}))  # - Just 1 page (~33)
    ws.send(json.dumps({"command":"all"}))  # - All (~2500+)

    print("\nReceiving paginate")
    ws.recv()  # paginate
    print("Receiving all")
    result = ws.recv()  # all
    ws.close()

    # Format data and then return the completed list.
    return format.formatPetitions(result)
