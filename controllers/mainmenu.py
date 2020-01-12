from socketserver import StreamRequestHandler
import json
import controllers.player

class MainMenu():

  def handle(self, requestHandler):
    data = requestHandler.rfile.readline()[:-1].decode("utf-8")
    args = data.split(" ")
    if args[0] == "login":
      password = ""
      if len(args) > 1:
        password = args[1]
      else:
        requestHandler.writeString(
          "Login page (not secure)\n"
          + "> Enter your password.\n"
        )
        password = requestHandler.rfile.readline()[:-1].decode("utf-8")
        print(password)
      with open('players.json') as json_file:
          players = json.load(json_file)
          if password in players:
            requestHandler.writeString("Welcome back!\n")
            requestHandler.writeString("Available commands: [problems [week] [100, 200, 300], flag [flag], scoreboard, env, logout, clear, quit]\n")
            while True:
              command = controllers.player.PlayerMenu().handle(requestHandler, password)
              if command == "quit":
                return
          else:
            requestHandler.writeString("Invalid.\n")
    elif args[0] == "register":
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
    elif args[0] == "info":
      requestHandler.writeString(
        "Lab CTF for Georgia Tech Greyhat How to Hack Seminar 2020\n"
        + "https://gthowtohack.github.io/\n"
      )
    elif args[0] == "clear":
      requestHandler.writeString(
        "\n"*100
      )
    elif args[0] == "quit":
      return data
    elif args[0] == "help":
      requestHandler.writeString(
        "Login or register to access lab features.\n"
        + "Available commands: [login, register, info, help, clear, quit]\n"
      )
