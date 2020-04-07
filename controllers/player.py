from socketserver import StreamRequestHandler
import json
import controllers.ModelSingleton
import os
import subprocess
from datetime import datetime

class PlayerMenu():

  def handle(self, requestHandler, user):
    data = requestHandler.rfile.readline()[:-1].decode("utf-8")
    args = data.split(" ")
    if args[0] == "problems" or args[0] == 'p' or args[0] == "ls":
      if len(args) == 1:
        requestHandler.writeString(
          "Usage: problems [week] [id 1-8]\n"
          )
      else:
        with open('problems.json') as json_file:
          problems = json.load(json_file)
          if len(args) == 2:
            week = int(args[1]) - 1
            returnString = ""
            if week < 0 or week > 8:
              returnString = "Out of bounds. Enter a week from 1-8\n"
            else:
              if len(problems) < week + 1:
                returnString = "No problems posted.\n"
              else:
                for i, problem in enumerate(problems[week]["problems"]):
                  if problem["points"] == 1000000: # 1 million points -> Boss problem
                    returnString += str(i + 1) + ". " + problem["name"] + " (\xe2\x98\xa0)\n"
                  else:
                    returnString += str(i + 1) + ". " + problem["name"] + " (" + str(problem["points"]) + ")\n"
            requestHandler.writeString(
              "# Week " +  args[1] + "\n"
              + returnString
            )
          elif len(args) == 3:
            week = int(args[1]) - 1
            returnString = ""
            if week < 0 or week > 12:
              returnString = "Week out of bounds. Enter a week from 1-8\n"
            else:
              key = args[2][0]
              key = int(key)
              if key < 1 or key > 4:
                returnString = "Question number out of bounds. Enter a problem from 1-4.\n"
              else:
                if len(problems) < week + 1 or len(problems[week]["problems"]) < key:
                  returnString = "This problem has not been posted for this week.\n"
                else:
                  problem = problems[week]["problems"][key - 1]
                  returnString = "## " + problem["name"] + " (" + str(problem["points"]) + ")\n" \
                    + "### Description\n" + problem["description"] + "\n"
            requestHandler.writeString(
              "# Week " +  args[1] + "\n"
              + returnString
            )
    elif args[0] == "flag" or args[0] == 'f':
      if len(args) == 1:
        requestHandler.writeString("Use this command to submit flags. Usage: f[lag] [flag]")
      else:
        with open('problems.json') as problems_file:
          with open('players.json') as players_file:
            players = json.load(players_file)
            problems = json.load(problems_file)
            for week in problems:
              if "flags" in week:
                # Headless Flags
                for flag in week["flags"].keys():
                  if flag == args[1]:
                    with open('solves.json') as solves_file:
                      solves = json.load(solves_file)
                      if not week["name"] in solves:
                        solves[week["name"]] = {}
                      if not flag in solves[week["name"]]:
                        solves[week["name"]][flag] = []
                      if not user in solves[week["name"]][flag]:
                        solves[week["name"]][flag].append(user)
                        players[user]["points"] += week["flags"][flag]
                        if "journey_points" not in players[user]:
                          players[user]["journey_points"] = 0
                        players[user]["journey_points"] += week["flags"][flag]
                        time = datetime.now()
                        players[user]["last_solve"] = int(time.strftime("%s"))
                        with open('players.json', 'w') as players_out:
                          with open('solves.json', 'w') as solves_out:
                            json.dump(players, players_out)
                            json.dump(solves, solves_out)
                            requestHandler.writeString("Congratulations, you have earned " + str(week["flags"][flag]) + " points.\n")
                            if week["flags"][flag] > 1000000:
                              if os.environ.get('WORMHOLE') != None:
                                process = subprocess.Popen(os.environ.get('WORMHOLE'), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
                                while True:
                                  process.stdin.write(input())
                                  process.stdin.flush()
                                  stdout, stderr = process.communicate()
                                  print(stdout, end='')

                      else:
                        requestHandler.writeString("You've already solved this one.\n")
              # Jeopardy Flags
              if "problens" in week:
                for problem in week["problems"]:
                  if problem["flag"] == args[1]:
                    with open('solves.json') as solves_file:
                      solves = json.load(solves_file)
                      if not week["name"] in solves:
                        solves[week["name"]] = {}
                      if not problem["name"] in solves[week["name"]]:
                        solves[week["name"]][problem["name"]] = []
                      if not user in solves[week["name"]][problem["name"]]:
                        solves[week["name"]][problem["name"]].append(user)
                        players[user]["points"] += problem["points"]
                        with open('players.json', 'w') as players_out:
                          with open('solves.json', 'w') as solves_out:
                            json.dump(players, players_out)
                            json.dump(solves, solves_out)
                            requestHandler.writeString("Congratulations, you have solved '" + problem["name"] + "' for " + str(problem["points"]) + " points.\n")
                      else:
                        requestHandler.writeString("You've already solved this one.\n")

    elif args[0] == "scoreboard" or args[0] == "score":
      requestHandler.writeString(
          "================\n"
        + "   Scoreboard\n"
        + "================\n"
      )
      with open('players.json') as json_file:
        players = json.load(json_file)
        sorted_list = sorted(players, key=lambda k: players[k]["points"], reverse=True)
        string = ""

        written = 0
        with open('env.json') as json_file:
          env = json.load(json_file)
          for i, player_name in enumerate(sorted_list):
            player = players[player_name]
            if written < 10:
              display_name = "<anonymous>"
              if player_name in env and "name" in env[player_name] and env[player_name] != "":
                display_name = env[player_name]["name"]
              string += ("* " if player_name == user else "") \
                + str(i + 1) + ". " + display_name + " - " + str(player["points"]) + "\n"
              written += 1
            elif player_name == user:
              display_name = "<anonymous>"
              if player_name in env and "name" in env[player_name] and env[player_name] != "":
                display_name = env[player_name]["name"]
              string += "* " + str(i + 1) + ". " + display_name + " - " + str(player["points"]) + "\n"
              break

        requestHandler.writeString(
          string + "\n"
        )
    elif args[0] == "journey" or args[0] == "j":
      requestHandler.writeString(
          "====================\n"
        + " Journey Scoreboard \n"
        + "====================\n"
      )
      with open('players.json') as json_file:
        players = json.load(json_file)
        sorted_list = sorted(players, key=lambda k: players[k]["points"], reverse=True)
        string = ""

        written = 0
        with open('env.json') as json_file:
          env = json.load(json_file)
          for i, player_name in enumerate(sorted_list):
            player = players[player_name]
            if player_name == user:
              display_name = "<anonymous>"
              points = (player["journey_points"] if "journey_points" in player else 0)
              if player_name in env and "name" in env[player_name] and env[player_name] != "":
                display_name = env[player_name]["name"]
              string += "* " + str(i + 1) + ". " + display_name + " - " + str(points) + "\n"
              if written > 20:
                break
            elif written < 20:
              display_name = "<anonymous>"
              if not "journey_points" in player:
                continue
              if player_name in env and "name" in env[player_name] and env[player_name] != "":
                display_name = env[player_name]["name"]
              string += ("* " if player_name == user else "") \
                + str(i + 1) + ". " + display_name + " - " + str(player["journey_points"]) + "\n"
              written += 1

        requestHandler.writeString(
          string + "\n"
        )
    elif args[0] == "env":
      with open('env.json') as json_file:
        players = json.load(json_file)
        if len(args) == 1:
          if user in players:
            requestHandler.writeString(
              "DISPLAY_NAME=" + players[user]["name"] + "\nSHOW_ON_SCOREBOARD=" + ("1" if players[user]["scoreboard"] else "0")  + "\n"
            )
          else:
            requestHandler.writeString(
              "DISPLAY_NAME=\nSHOW_ON_SCOREBOARD=1\n"
            )
        else:
          equals = args[1].split('=')
          if len(equals) != 2:
            requestHandler.writeString(
              "Usage: env VAR=VALUE\n"
            )
          else:
            real_key = ""
            value = ""
            if equals[0] == "DISPLAY_NAME":
              real_key = "name"
              value = equals[1]
            elif equals[0] == "SHOW_ON_SCOREBOARD":
              real_key = "scoreboard"
              value = equals[1] == "1"
            if not user in players:
              players[user] = {"name": "<anonymous>", "scoreboard": True}
            if value != None:
              players[user][real_key] = value
            requestHandler.writeString(
              args[1] + "\n"
            )
            with open('env.json', 'w') as outfile:
                json.dump(players, outfile)
    elif args[0] == "clear" or args[0] == 'c':
      requestHandler.writeString(
        "\n"*100
      )
    elif args[0] == "quit" or args[0] == 'q':
      return args[0]
    elif args[0] == "logout":
      return args[0]
    elif args[0] == "help" or args[0] == 'h':
      requestHandler.writeString(
        "You are logged into the lab portal.\n"
          + "Available commands: [p[roblems] [week] [100, 200, 300], f[lag] [flag], score[board], [j]ourney, env, logout, c[lear], q[uit]]\n"
      )
