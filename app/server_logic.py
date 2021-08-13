import copy

def avoid_my_neck_and_walls(my_head, my_body, snakes, possible_moves):
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")
      
    if my_head["x"] == 10:
      possible_moves.remove("right")
    elif my_head["x"] == 0:
      possible_moves.remove("left")

# if {"x": my_head["x"], "y": my_head["y"]} in my_body:
    
    if my_head["y"] == 10:
      possible_moves.remove("up")
    elif my_head["y"] == 0:
      possible_moves.remove("down")

    # for i in range()

    return possible_moves


def avoid_snakes(my_head, snakes, possible_moves, length):
  grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]

  # Create grid
  for snakeIndex in range(len(snakes)):
    for bodyIndex in range(len(snakes[snakeIndex]["body"])-1):
      # Adds every part except the tail
      grid[snakes[snakeIndex]["body"][bodyIndex]["y"]][snakes[snakeIndex]["body"][bodyIndex]["x"]] = 1

    # Adds the possible ways a snake head could move if it has more health
    if snakes[snakeIndex]["body"][0] != my_head and snakes[snakeIndex]["length"] >= length:
      if snakes[snakeIndex]["body"][0]["x"] - 1 >= 0:
        grid[snakes[snakeIndex]["body"][0]["y"]][snakes[snakeIndex]["body"][0]["x"]-1] = 1
      if snakes[snakeIndex]["body"][0]["x"] + 1 <= 10:
        grid[snakes[snakeIndex]["body"][0]["y"]][snakes[snakeIndex]["body"][0]["x"]+1] = 1
      if snakes[snakeIndex]["body"][0]["y"] - 1 >= 0:
        grid[snakes[snakeIndex]["body"][0]["y"]-1][snakes[snakeIndex]["body"][0]["x"]] = 1
      if snakes[snakeIndex]["body"][0]["y"] + 1 <= 10:
        grid[snakes[snakeIndex]["body"][0]["y"]+1][snakes[snakeIndex]["body"][0]["x"]] = 1

  # Remove killing moves using grid
  if "up" in possible_moves and grid[my_head["y"]+1][my_head["x"]] == 1:
    possible_moves.remove("up")
  if "down" in possible_moves and grid[my_head["y"]-1][my_head["x"]] == 1:
    possible_moves.remove("down")
  if "left" in possible_moves and grid[my_head["y"]][my_head["x"]-1] == 1:
    possible_moves.remove("left")
  if "right" in possible_moves and grid[my_head["y"]][my_head["x"]+1] == 1:
    possible_moves.remove("right")
    
  return possible_moves
  
  # if {"x": my_head["x"], "y": my_head["y"]} in my_body:
  #   my_body.remove({"x": my_head["x"], "y": my_head["y"]})



def find_food(my_head, food, possible_moves):
  closestFood = {"x": 5, "y": 5}
  closestDist = 50
  
  for i in range(len(food)):
    dist = abs(my_head["x"] - food[i]["x"]) + abs(my_head["y"] - food[i]["y"])
    #print(dist, closestDist)
    if dist < closestDist:
      closestDist = dist
      closestFood = food[i]
    
  xDiff = abs(my_head["x"] - closestFood["x"])
  yDiff = abs(my_head["y"] - closestFood["y"])

  execute = True
  if xDiff > yDiff:
    execute = False
    if my_head["x"] > closestFood["x"]:
      choice = "left"
    else:
      choice = "right"
    
    if choice not in possible_moves:
      execute = True

  if execute:
    if my_head["y"] > closestFood["y"]:
      choice = "down"
    else:
      choice = "up"
    
    if choice not in possible_moves:
      return possible_moves[0]
  
  return choice

def simulate_move(my_head, my_body, snakes, food, length):
  try:
    possible_moves = list(["up", "down", "left", "right"])
    possible_moves = avoid_my_neck_and_walls(my_head, my_body, snakes, possible_moves)
    possible_moves = avoid_snakes(my_head, snakes, possible_moves, length)
    move = find_food(my_head, food, possible_moves)
  except:
    return "dead"

  if len(possible_moves) == 0:
    move = "dead"
  
  return move

def simulate_future(possible_moves, data):
  not_possible_moves = list([])
  dataOrigin = copy.deepcopy(data)
  for myMove in ((possible_moves)):
    data = copy.deepcopy(dataOrigin)
    for turnIndex in range(10): # num turns ahead
      snakeIndex = 0
      dataHolder = copy.deepcopy(data)
      shouldBreak = False
      for asdf in range(len(data["board"]["snakes"])):
        
        if (data["board"]["snakes"][snakeIndex]["name"] == "snek" and turnIndex == 0):
          move = myMove
        else:
          move = simulate_move(dataHolder["board"]["snakes"][snakeIndex]["head"], dataHolder["board"]["snakes"][snakeIndex]["body"], dataHolder["board"]["snakes"], dataHolder["board"]["food"], dataHolder["board"]["snakes"][snakeIndex]["length"])

        #print(move, data["turn"])
        if move == "dead":
          if data["board"]["snakes"][snakeIndex]["name"] == "snek":
            not_possible_moves.append([myMove, turnIndex])
            shouldBreak = True
            break
            
          del data["board"]["snakes"][snakeIndex]
          snakeIndex -= 1

        # moves the head
        elif move == "up":
          data["board"]["snakes"][snakeIndex]["head"]["y"] += 1

        elif move == "right":
          data["board"]["snakes"][snakeIndex]["head"]["x"] += 1

        elif move == "down":
          data["board"]["snakes"][snakeIndex]["head"]["y"] -= 1

        elif move == "left":
          data["board"]["snakes"][snakeIndex]["head"]["x"] -= 1
        
        for bodyIndex in range(len(data["board"]["snakes"][snakeIndex]["body"])-1, 0, -1):
          data["board"]["snakes"][snakeIndex]["body"][bodyIndex] = data["board"]["snakes"][snakeIndex]["body"][bodyIndex-1].copy()
        
        data["board"]["snakes"][snakeIndex]["body"][0] = data["board"]["snakes"][snakeIndex]["head"].copy()
        
        foodIndex = 0
        for i in range(len(data["board"]["food"])):
          if data["board"]["food"][foodIndex] == data["board"]["snakes"][snakeIndex]["head"]:
            del data["board"]["food"][foodIndex]
            foodIndex -= 1
          foodIndex += 1
        
        snakeIndex += 1
        # print("--------------------")
        # print(data["turn"], myMove, data["board"]["snakes"][0]["body"])
      if shouldBreak:
        break
      
    
        # print(data["board"]["snakes"][0]["body"], data["turn"])

  
  print(possible_moves, not_possible_moves, data["turn"])
  for i in range(len(not_possible_moves)):
    possible_moves.remove(not_possible_moves[i][0])
  
  if len(possible_moves) == 0:
    mostTurns = 0
    for i in range(len(not_possible_moves)):
      if not_possible_moves[i][1] > mostTurns:
        possible_moves = list([])
        possible_moves.append(not_possible_moves[i][0])
  return possible_moves
      
def choose_move(data: dict) -> str:
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]

    snakes = data["board"]["snakes"]


    possible_moves = ["up", "down", "left", "right"]
    # direction = helper.handler(data.get('you'), data.get('snakes'), data.get('food'))

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck_and_walls(my_head, my_body, snakes, possible_moves)
    possible_moves = avoid_snakes(my_head, snakes, possible_moves, data["you"]["length"])

    if data["turn"] > 4:
      data_copy = copy.deepcopy(data)
      possible_moves = simulate_future(possible_moves, data_copy)

    move = find_food(my_head, data["board"]["food"], possible_moves)

    # print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")
    # pp.pprint(data)

    return move