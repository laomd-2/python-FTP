from utility.handlers import ResponseHandler


class CSClient(ResponseHandler):
    """docstring for CSClient"""

    def handle(self):
        with open("a.txt", 'r') as file:
            for line in file:
                self.send(line)


if __name__ == '__main__':
    client = CSClient()
    client.connect(("localhost", 12000))
    client.handle()
    client.disconnect()
