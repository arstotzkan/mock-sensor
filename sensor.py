import socketserver
import datetime
import random

def generate_report_string():
    now = datetime.datetime.now()
    current_month = now.date().month

    temperature = 10 + random.uniform(2, 2.5) * (current_month % 11) 
    pressure = random.uniform(950, 1000) 
    relative_humidity = max(45 + random.uniform(1.5, 2.25) * (current_month % 11), 100)
    precipitation = random.uniform(1, 2)

    return f"T:{round(temperature, 2)},P:{round(pressure, 2)},H:{round(relative_humidity, 2)},R:{round(precipitation, 2)}"

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        if self.data.decode("utf-8") == "REPORT":
            report_string = generate_report_string()
            self.request.sendall(report_string.encode())
            self.request.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print("Server runs")
        server.serve_forever()
