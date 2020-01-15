from socketserver import ForkingTCPServer, StreamRequestHandler, ForkingMixIn
from controllers import *

class MessageHandler(StreamRequestHandler):

  def handle(self):
    self.writeString(
      "GreyH@t Stepping into Security - Lab Server\n"
      + "v1.0.1\n"
      + "------------------\n"
      + "Available commands: [login, register, info, help, clear, quit]\n"
      )
    while True:
      last_command = mainmenu.MainMenu().handle(self)
      if last_command == "quit":
        return

  def writeString(self, string):
    self.wfile.write(bytes(string, "utf-8"))

if __name__ == '__main__':
  server = ForkingTCPServer(("0.0.0.0", 1000), RequestHandlerClass=MessageHandler, bind_and_activate=False)
  server.allow_reuse_address = True
  server.server_bind()
  server.server_activate()
  print("Now listening on port 1000!")
  server.serve_forever()
