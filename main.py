from socketserver import TCPServer, StreamRequestHandler, ForkingMixIn
from controllers import *

class MessageHandler(StreamRequestHandler):

  def handle(self):
    self.writeString(
      "How to Hack Lab Server\n"
      + "v1.0\n"
      + "------------------\n"
      + "Available commands: [login, register, info, help, clear, quit]\n"
      )
    while True:
      last_command = mainmenu.MainMenu().handle(self)
      if last_command == "quit":
        return

  def writeString(self, string):
    self.wfile.write(bytes(string, "utf-8"))

class ReusableTCPServer(ForkingMixIn, TCPServer):
    allow_reuse_address = True

if __name__ == '__main__':
  TCPServer.allow_reuse_address = True
  server = ReusableTCPServer(("0.0.0.0", 8080), MessageHandler)
  server.serve_forever()