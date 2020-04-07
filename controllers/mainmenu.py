from socketserver import StreamRequestHandler
import json
import controllers.player

class MainMenu():

  def handle(self, requestHandler):
    print(555555555)
    data = requestHandler.rfile.readline()[:-1].decode("utf-8")
    args = data.split(" ")
    if args[0] == "login" or args[0] == 'l':
      print(133)
      password = ""
      if len(args) > 1:
        password = args[1]
      else:
        requestHandler.writeString(
          "Login page (not secure)\n"
          + "> Enter your password.\n"
        )
        print(111)
        password = requestHandler.rfile.readline()[:-1].decode("utf-8")
        print(password)
      with open('players.json') as json_file:
          players = json.load(json_file)
          if password in players:
            requestHandler.writeString("Welcome back!\n")
            requestHandler.writeString("Available commands: [p[roblems] [week] [100, 200, 300], f[lag] [flag], score[board], j[ourney], env, logout, c[lear], q[uit]]\n")
            while True:
              command = controllers.player.PlayerMenu().handle(requestHandler, password)
              if command == "quit" or command == 'q' or command == "logout":
                return command
          else:
            requestHandler.writeString("Invalid.\n")
    elif args[0] == "register" or args[0] == 'r':
      requestHandler.writeString(
        "Register page (not secure)\n"
        + "> Enter a password to identify yourself with. This will also be your username, so make sure no one can guess it.\n"
      )
      password = requestHandler.rfile.readline()[:-1].decode("utf-8")
      with open('players.json') as json_file:
        players = json.load(json_file)
        if password in players:
          requestHandler.writeString("This key is already in use.\n")
        else:
          players[password] = { "points": 0 }
        with open('players.json', 'w') as outfile:
            json.dump(players, outfile)
      requestHandler.writeString(
        "Welcome! Your password is: `" + password + "`. Make sure you keep this secret!\n"
        + "Now, you need to login.\n"
      )
    elif args[0] == "info" or args[0] == 'i':
      requestHandler.writeString(
        "Lab CTF for Georgia Tech Greyhat How to Hack Seminar 2020\n"
        + "https://gthowtohack.github.io/\n"
      )
    elif args[0] == "clear" or args[0] == 'c':
      requestHandler.writeString(
        "\n"*100
      )
    elif args[0] == "quit" or args[0] == 'q':
      return data
    elif args[0] == "help" or args[0] == 'h':
      requestHandler.writeString(
        "Login or register to access lab features.\n"
        + "Available commands: [l[ogin], r[egister], i[nfo], h[elp], c[lear], q[uit]]\n"
      )
