import sys

# Please implement this function according to Section "Read Configuration File"


class BattleMap:
    def __init__(self, width, height, waters, woods, foods, golds, player1, player2):
        self.width = width
        self.height = height
        self.waters = waters
        self.woods = woods
        self.foods = foods
        self.golds = golds
        self.player1 = player1
        self.player2 = player2

    def draw_map_assets(self, icon, h_s, x, y, empty):
        if empty:
            if icon == '~~':
                assets = self.waters
            elif icon == 'WW':
                assets = self.woods
            elif icon == 'FF':
                assets = self.foods
            elif icon == 'GG':
                assets = self.golds
            elif icon == 'S1':
                assets = self.player1.spearman
            elif icon == 'A1':
                assets = self.player1.archer
            elif icon == 'K1':
                assets = self.player1.knight
            elif icon == 'T1':
                assets = self.player1.scout
            elif icon == 'S2':
                assets = self.player2.spearman
            elif icon == 'A2':
                assets = self.player2.archer
            elif icon == 'K2':
                assets = self.player2.knight
            elif icon == 'T2':
                assets = self.player2.scout
            for a in assets:
                if a.x == x and a.y == y:
                    h_s = h_s+icon
                    empty = False
                    break
        return h_s, empty

    def draw_map(self):
        print("Please check the battlefield, commander.")
        #-------------x-content && y-content-------------#
        # region
        w = 0
        w_xs = ""
        w_ys = ""
        while w < self.width:
            if w == 0:
                w_xs = w_xs+"0"+str(w)
                w_ys = w_ys+"--"
            else:
                w_xs = w_xs+" 0"+str(w)
                w_ys = w_ys+"---"
            w = w+1
        w_xs = "  X"+w_xs+"X"
        w_ys = " Y+"+w_ys+"+"
        # endregion
        #-------------map-content-------------#
        # region
        y = 0
        h_s = ""
        while y < self.height:
            h_s = h_s+"0"+str(y)
            x = 0
            while x < self.width:
                h_s = h_s+"|"
                empty = True
                # player 1 Base
                if self.player1.home.x == x and self.player1.home.y == y:
                    h_s = h_s+"H1"
                    empty = False
                # player 2 Base
                elif self.player2.home.x == x and self.player2.home.y == y:
                    h_s = h_s+"H2"
                    empty = False
                # assets Icon
                for icon in ['~~', 'WW', 'FF', 'GG',
                             'S1', 'A1', 'K1', 'T1',
                             'S2', 'A2', 'K2', 'T2',
                             ]:
                    h_s, empty = self.draw_map_assets(icon, h_s, x, y, empty)
                # None Icon
                if empty:
                    h_s = h_s+"  "
                if x == (self.width-1):
                    h_s = h_s+"|"
                x += 1
            if y != (self.height-1):
                h_s = h_s+"\n"
            y += 1
        # endregion
        #-------------draw-map-------------#
        # region
        print(w_xs)
        print(w_ys)
        print(h_s)
        print(w_ys)
        # endregion


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player:
    def __init__(self, name, wood, food, gold, spearman, archer, knight, scout, home):
        self.name = name
        self.wood = wood
        self.food = food
        self.gold = gold
        self.spearman = spearman
        self.archer = archer
        self.knight = knight
        self.scout = scout
        self.home = home


def set_assets(assets):  # help anaylize map txt fuction
    p_list = []
    p = Position("", "")
    for a in assets:
        if p.x == "":
            p.x = int(a)
        elif p.y == "":
            p.y = int(a)
            p_list.append(p)
            p = Position("", "")
    return p_list


def load_config_file(filepath):  # loading map message by txt
    # It should return width, height, waters, woods, foods, golds based on the file
    # Complete the test driver of this function in file_loading_test.py
    width, height = 0, 0
    waters, woods, foods, golds = [], [], [], []  # list of position tuples
    try:
        f = open(filepath, 'r')
        content = f.read()
        for word in content.splitlines(keepends=False):
            if "Frame: " in word:
                word = word.replace("Frame: ", "")
                map_wh = word.split("x")
                width = int(map_wh[0])
                height = int(map_wh[1])
            elif "Water: " in word:
                word = word.replace("Water: ", "")
                assets = word.split(" ")
                waters = set_assets(assets)
            elif "Wood: " in word:
                word = word.replace("Wood: ", "")
                assets = word.split(" ")
                woods = set_assets(assets)
            elif "Food: " in word:
                word = word.replace("Food: ", "")
                assets = word.split(" ")
                foods = set_assets(assets)
            elif "Gold: " in word:
                word = word.replace("Gold: ", "")
                assets = word.split(" ")
                golds = set_assets(assets)
    except IOError:
        print("FileNotFoundError")
    finally:
        f.close()
    return width, height, waters, woods, foods, golds


def show_recruit_price():  # show recruit price list
    print("Recruit Prices:")
    print("  Spearman (S) -1W, 1F")
    print("  Archer (A) -1W, 1G")
    print("  Knight (K) -1F, 1G")
    print("  Scout (T) -1W, 1F, 1G")


def show_year(year):  # show year each round need to show
    print("-Year "+str(year)+"-\n")


def show_asstes(palyer):  # show player assets - Wood , Gold , Food
    print("[Your Asset: Wood - {} Food - {} Gold - {}]\n".format(palyer.wood,
                                                                 palyer.food, palyer.gold))


def int_try_parse(value):  # return value (int or string), canParse or not (boolean)
    try:
        return int(value), True
    except ValueError:
        return value, False


# enter recruit x y position use in recruit_stage
def show_recruit_msg(recruit_type, check_home_p, check_p_empty_list, player, enemy, game_map):
    while True:
        input_content = input(
            "You want to recruit a {}.Enter two integers as format 'x y' to place your army.\n".format(
                recruit_type)
        )
        #-------------edge case------------------#
        if input_content == 'DIS':
            game_map.draw_map()
        elif input_content == 'PRIS':
            show_recruit_price()
        elif input_content == 'QUIT':
            exit()
        #------------------positive case------------------#
        elif ' ' in input_content:
            input_xy = input_content.split(' ')
            #------------------positive case-----------#
            input_x, input_x_is_int = int_try_parse(input_xy[0])
            input_y, input_y_is_int = int_try_parse(input_xy[1])
            if len(input_xy) == 2 and input_x_is_int and input_y_is_int:
                input_p = Position(input_x, input_y)
                i = 0
                check_place_success = False
                for check in check_p_empty_list:
                    #-------------positive case---------------#
                    if check and input_p.x == check_home_p[i].x and input_p.y == check_home_p[i].y:
                        if recruit_type == "Spearman":
                            player.wood = player.wood-1
                            player.food = player.food-1
                            player.spearman.append(input_p)
                        elif recruit_type == "Archer":
                            player.wood = player.wood-1
                            player.gold = player.gold-1
                            player.archer.append(input_p)
                        elif recruit_type == "Knight":
                            player.food = player.food-1
                            player.gold = player.gold-1
                            player.knight.append(input_p)
                        elif recruit_type == "Scout":
                            player.wood = player.wood-1
                            player.food = player.food-1
                            player.gold = player.gold-1
                            player.scout.append(input_p)
                        check_p_empty_list[i] = False
                        check_place_success = True
                        print("\nYou has recruited a {}.\n".format(recruit_type))
                        if player.name == "Player 1":
                            game_map.player1 = player
                        else:
                            game_map.player2 = player
                        player, game_map = recruit_stage(
                            player, enemy, game_map, False)
                        return player, game_map
                    i += 1
                #-------------edge case---------------#
                if not check_place_success:
                    print(
                        "You must place your newly recruited unit in an unoccupied position next to your home base. Try again.\n")
            #-------------negative case---------------#
            else:
                print("Sorry, invalid input Try again.\n")
        #-------------negative case---------------#
        else:
            print("Sorry, invalid input Try again.\n")


# check home 4 position is empty
def check_home_place_empty(armies, check_p, check_p_list):
    for p in armies:
        if (p.x == check_p[0].x and p.y == check_p[0].y) and check_p_list[0]:
            check_p_list[0] = False
        if (p.x == check_p[1].x and p.y == check_p[1].y) and check_p_list[1]:
            check_p_list[1] = False
        if(p.x == check_p[2].x and p.y == check_p[2].y) and check_p_list[2]:
            check_p_list[2] = False
        if(p.x == check_p[3].x and p.y == check_p[3].y) and check_p_list[3]:
            check_p_list[3] = False
    return check_p_list


# recruit_stage return player_info,map_info
def recruit_stage(player, enemy, game_map, show_player_msg):
    if show_player_msg:
        print("+++"+player.name+"'s Stage: Recruit Armies+++")

    #-------------show player resource-------------#
    show_asstes(player)
    #-------------check resource is enough-------------#
    # region
    if (player.wood == 0 and player.food == 0) or (player.wood == 0 and player.gold == 0) or (player.gold == 0 and player.food == 0):
        print('No resources to recruit any armies.')
        return player, game_map
    # endregion

    #-------------check has place to recruit-------------#
    # region
    check_home_p = [
        Position(player.home.x-1, player.home.y),
        Position(player.home.x+1, player.home.y),
        Position(player.home.x, player.home.y+1),
        Position(player.home.x, player.home.y-1)
    ]
    # HomeBase 4 Position is Empty
    check_p_empty_list = [True, True, True, True]
    #---------check player armies----------#
    armies = player.spearman+player.archer+player.knight+player.scout + \
        enemy.spearman+enemy.archer+enemy.knight+enemy.scout

    check_p_empty_list = check_home_place_empty(
        armies, check_home_p, check_p_empty_list)

    check_place = True

    for c in check_p_empty_list:
        if c:
            check_place = False

    if check_place:
        print('No place to recruit any armies.')
        return player, game_map
    # endregion

    #----------------recruit army-----------------------#
    # region
    input_content = ""
    while input_content != 'NO':
        input_content = input(
            "Which type of army to recruit, (enter) 'S', 'A', 'K', or 'T'? Ener 'NO' to end this stage.\n")

        #-------------edge case------------------#
        if input_content == 'DIS':
            game_map.draw_map()
        elif input_content == 'PRIS':
            show_recruit_price()
        elif input_content == 'QUIT':
            exit()
        elif input_content == 'NO':
            return player, game_map
        #--------------positive case--------------#
        elif input_content == 'S':
            #------------edge case-----------#
            if player.wood == 0 or player.food == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                player, game_map = show_recruit_msg("Spearman", check_home_p,
                                                    check_p_empty_list, player, enemy, game_map)
                return player, game_map
        elif input_content == 'A':
            #------------edge case-----------#
            if player.wood == 0 or player.gold == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                player, game_map = show_recruit_msg("Archer", check_home_p,
                                                    check_p_empty_list, player, enemy, game_map)
            return player, game_map
        elif input_content == 'K':
            #------------edge case-----------#
            if player.gold == 0 or player.food == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                player, game_map = show_recruit_msg("Knight", check_home_p,
                                                    check_p_empty_list, player, enemy, game_map)
                return player, game_map
        elif input_content == 'T':
            #------------edge case-----------#
            if player.wood == 0 or player.food == 0 or player.gold == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                player, game_map = show_recruit_msg("Scout", check_home_p,
                                                    check_p_empty_list, player, enemy, game_map)
                return player, game_map
        #-------------negative case---------------#
        else:
            print("Sorry, invalid input Try again.\n")
    # endregion


def armies_info(player, army_type, player_already_move):  # show can move armies_info
    armies_info = ""
    armies_first_for_no_comma = True

    armies = []
    if army_type == "Spearman":
        armies = player.spearman
    elif army_type == "Archer":
        armies = player.archer
    elif army_type == "Scout":
        armies = player.scout
    elif army_type == "Knight":
        armies = player.knight

    for p in armies:
        check_already_move = True
        for a_p in player_already_move:
            if p.x == a_p.x and p.y == a_p.y:
                check_already_move = False
                break
        if check_already_move:
            if armies_first_for_no_comma:
                armies_info = armies_info+"({},{})".format(p.x, p.y)
            else:
                armies_info = armies_info+", ({},{})".format(p.x, p.y)
        armies_first_for_no_comma = False
    armies_info = "{}: {}\n".format(army_type, armies_info)
    return armies_info


# scout can move to 2 steps,others only 1 step
def move_step_available(army_type, start, end):
    move_step = abs(int(end)-int(start))
    if army_type == 'Scout':
        if move_step <= 2:
            return True
        else:
            return False
    else:
        if move_step == 1:
            return True
        else:
            return False


def check_position_in_array(position, position_array):
    for p in position_array:
        if int(position.x) == int(p.x) and int(position.y) == int(p.y):
            return True
    return False


def has_armies_type(player, position):  # has_armies and return army type
    if check_position_in_array(position, player.spearman):
        return True, 'Spearman'
    elif check_position_in_array(position, player.archer):
        return True, 'Archer'
    elif check_position_in_array(position, player.knight):
        return True, 'Knight'
    elif check_position_in_array(position, player.scout):
        return True, 'Scout'
    else:
        return False, 'none'


def available_destination(start_position, end_position, battle_map, player, enemy, year):
    has_armies, army_type = has_armies_type(player, start_position)
    if not has_armies:
        return False, army_type

    #   out of map_range
    if not(int(end_position.x) <= (int(battle_map.width)-1) and int(end_position.y) <= (int(battle_map.height)-1)):
        return False, army_type

    #   not move , not on other armies position
    armis = player.spearman + player.archer + player.knight+player.scout
    #   not on home_base
    armis.append(player.home)
    if end_position in armis:
        return False, army_type

    #   go up or down
    if start_position.x == end_position.x:
        return move_step_available(army_type, end_position.y, start_position.y), army_type
    #   go left or right
    elif start_position.y == end_position.y:
        return move_step_available(army_type, end_position.x, start_position.x), army_type
    #   not diagonal
    else:
        return False, army_type


def meet_solider_or_nothing(army_position, step, army_type, player, enemy, player_already_move):
    army_alive = False
    # meet spearman
    if check_position_in_array(step, enemy.spearman):
        if army_type == "Spearman":
            player.spearman.remove(army_position)
            enemy.spearman.remove(step)
            print("We destroyed the enemy {} with massive loss!\n".format(army_type))
        elif army_type == "Archer":
            player.archer.replace(army_position, step)
            enemy.spearman.remove(step)
            print("Great! We defeated the enemy {}!\n".format(army_type))
            army_alive = True
            player_already_move.append(step)
        elif army_type == 'Knight':
            player.knight.remove(army_position)
            print("We lost the army {} due to your command!\n".format(army_type))
        elif army_type == 'Scout':
            player.scout.remove(army_position)
            print("We lost the army {} due to your command!\n".format(army_type))
    # meet archer
    elif check_position_in_array(step, enemy.archer):
        if army_type == "Spearman":
            player.spearman.remove(army_position)
            print("We lost the army {} due to your command!\n".format(army_type))
        elif army_type == "Archer":
            player.archer.remove(army_position)
            enemy.archer.remove(step)
            print("We destroyed the enemy {} with massive loss!\n".format(army_type))
        elif army_type == 'Knight':
            player.knight.replace(army_position, step)
            enemy.archer.remove(step)
            print("Great! We defeated the enemy {}!\n".format(army_type))
            army_alive = True
            player_already_move.append(step)
        elif army_type == 'Scout':
            player.scout.remove(army_position)
            print("We lost the army {} due to your command!\n".format(army_type))
    # meet knight
    elif check_position_in_array(step, enemy.knight):
        if army_type == "Spearman":
            player.spearman.replace(army_position, step)
            enemy.knight.remove(step)
            print("Great! We defeated the enemy {}!\n".format(army_type))
            army_alive = True
            player_already_move.append(step)
        elif army_type == "Archer":
            player.archer.remove(army_position)
            print("We lost the army {} due to your command!\n".format(army_type))
        elif army_type == 'Knight':
            player.knight.remove(army_position)
            enemy.knight.remove(step)
            print("We destroyed the enemy {} with massive loss!\n".format(army_type))
        elif army_type == 'Scout':
            player.scout.remove(army_position)
            print("We lost the army {} due to your command!\n".format(army_type))
    # meet scout
    elif check_position_in_array(step, enemy.scout):
        if army_type == "Spearman":
            player.spearman.replace(army_position, step)
            enemy.scout.remove(step)
            print("Great! We defeated the enemy {}!\n".format(army_type))
            army_alive = True
            player_already_move.append(step)
        elif army_type == "Archer":
            player.archer.replace(army_position, step)
            enemy.scout.remove(step)
            print("Great! We defeated the enemy {}!\n".format(army_type))
        elif army_type == 'Knight':
            player.knight.replace(army_position, step)
            enemy.scout.remove(step)
            print("Great! We defeated the enemy {}!\n".format(army_type))
        elif army_type == 'Scout':
            print("We destroyed the enemy {} with massive loss!".format(army_type))
            player.scout.remove(army_position)
            enemy.scout.remove(step)
    # notthiig
    else:
        player = army_move(army_type, army_position, step, player)
        player_already_move.append(step)

    return player, enemy, army_alive, player_already_move


def replace_position_in_array(old_position, new_position, position_array):
    i = 0
    tmp_position_array = position_array
    for p in position_array:
        if(int(p.x) == int(old_position.x) and int(p.y) == int(old_position.y)):
            tmp_position_array[i] = new_position
            return tmp_position_array
        i += 1
    return tmp_position_array


def army_move(army_type, army_position, step, player):
    if army_type == "Spearman":
        player.spearman = replace_position_in_array(
            army_position, step, player.spearman)
        # player.spearman.replace(army_position, step)
    elif army_type == "Archer":
        player.archer.replace(army_position, step)
    elif army_type == 'Knight':
        player.knight.replace(army_position, step)
    elif army_type == 'Scout':
        player.scout.replace(army_position, step)
    return player


def move_result(army_position, step, battle_map, player, enemy, army_type, player_already_move):
    army_alive = True
    #-------- win game status -------#
    if enemy.home == step:
        print("The army {} captured the enemy’s capital.\n".format(army_type))
        cmd_name = input("What’s your name, commander?\n")
        print("***Congratulation! Emperor {} unified the country in {}.***\n".format(cmd_name, year))
        exit()
    #-------- get resource status -------#
    elif step in battle_map.woods:
        player.wood = player.wood+2
        battle_map.woods.remove(step)
        player = army_move(army_type, army_position, step, player)
        player_already_move.append(step)
        print("Good. We collected 2 Wood.\n")
    elif step in battle_map.foods:
        player.food = player.food+2
        battle_map.foods.remove(step)
        player = army_move(army_type, army_position, step, player)
        player_already_move.append(step)
        print("Good. We collected 2 Food.\n")
    elif step in battle_map.golds:
        player.gold = player.gold+2
        battle_map.golds.remove(step)
        player = army_move(army_type, army_position, step, player)
        player_already_move.append(step)
        print("Good. We collected 2 Gold.\n")
    #-------- meet water status -------#
    elif step in battle_map.waters:
        if army_type == 'Spearman':
            player.spearman.remove(army_position)
        elif army_type == 'Archer':
            player.archer.remove(army_position)
        elif army_type == 'Knight':
            player.knight.remove(army_position)
        elif army_type == 'Scout':
            player.scout.remove(army_position)
        army_alive = False
        print("We lost the army {} due to your command!\n".format(army_type))
    #-------- meet solider or nothing -------#
    else:
        player, enemy, army_alive, player_already_move = meet_solider_or_nothing(
            army_position, step, army_type, player, enemy, player_already_move)

    return player, enemy, battle_map, army_alive, player_already_move


def valid_move(player, enemy, battle_map, army_type, start_position, end_position, year, player_already_move):
    #-------- get all step ----------#
    all_step = []
    if army_type == "Scout":
        if start_position.x == end_position.x:
            move_step = abs(int(end_position.y)-int(start_position.y))
            if move_step == 2:
                if end_position.y > start_position.y:
                    all_step.append(
                        Position(start_position.x, start_position.y+1))
                else:
                    all_step.append(
                        Position(start_position.x, start_position.y-1))
        else:
            move_step = abs(int(end_position.x)-int(start_position.x))
            if move_step == 2:
                if end_position.x > start_position.x:
                    all_step.append(
                        Position(int(start_position.x)+1, int(start_position.y)))
                else:
                    all_step.append(
                        Position(int(start_position.x)-1, int(start_position.y)))
    all_step.append(end_position)
    army_alive = True
    #--------move_result-----------#
    for step in all_step:
        if army_alive:
            player, enemy, battle_map, army_alive, player_already_move = move_result(
                start_position, step, battle_map, player, enemy, army_type, player_already_move)

    return player, enemy, battle_map, player_already_move


def move_stage(player, enemy, game_map, player_already_move, show_player_msg, year):
    if show_player_msg:
        print("==={}'s Stage: Move Armies===\n".format(player.name))
    while True:
        tmp_player = player
        for p in player_already_move:
            tmp_player.spearman.remove(p)
            tmp_player.archer.remove(p)
            tmp_player.knight.remove(p)
            tmp_player.scout.remove(p)
        #------------check player army exist----------#
        if len(tmp_player.spearman) == 0 and len(tmp_player.archer) == 0 and len(tmp_player.knight) == 0 and len(tmp_player.scout) == 0:
            print("No Army to Move: next turn\n")
            return player, enemy, game_map
        else:
            print("Armies to Move\n")
            armies_info_show = ""
            for army_type in ["Spearman", "Archer", "Knight", "Scout"]:
                armies_info_show = armies_info_show + \
                    armies_info(player, army_type, player_already_move)
            print(armies_info_show)
            input_content = input(
                "\nEnter four integers as a format 'x0 y0 x1 y1' to represent move unit from (x0, y0) to (x1, y1) ir 'NO' to end this turn.\n")
            #-------------edge case------------------#
            if input_content == 'DIS':
                game_map.draw_map()
            elif input_content == 'PRIS':
                show_recruit_price()
            elif input_content == 'QUIT':
                exit()
            elif input_content == 'NO':
                return player, enemy, game_map
            #-------------positive case------------------#
            elif ' ' in input_content:
                input_content_p_xy = input_content.split(' ')
                if len(input_content_p_xy) == 4:
                    if input_content_p_xy[0].isdigit() and input_content_p_xy[1].isdigit() and input_content_p_xy[2].isdigit() and input_content_p_xy[3].isdigit():
                        start_position = Position(
                            input_content_p_xy[0], input_content_p_xy[1])
                        end_position = Position(
                            input_content_p_xy[2], input_content_p_xy[3])
                        # behave as move result
                        available, army_type = available_destination(
                            start_position, end_position, game_map, player, enemy, year)
                        #-------------behave as move result:valid move------------------#
                        if available:
                            print("You have moved {} from ({}, {}) to ({}, {}).".format(
                                army_type, start_position.x, start_position.y, end_position.x, end_position.y))

                            player, enemy, game_map, player_already_move = valid_move(player, enemy, game_map, army_type,
                                                                                      start_position, end_position, year, player_already_move)
                        #-------------behave as move result:invalid move---------------#
                        else:
                            print("Invalid move. Try again.\n")
            #-------------negative case---------------#
            else:
                print("Invalid move. Try again.\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 little_battle.py <filepath>")
        sys.exit()
    # -------- load config.txt -----------#
    width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])
    print("Configuration file config.txt was loaded.")
    # -----------------------------------#

    # ----------Player initial-----------#
    player1 = Player("Player 1", 2, 2, 2,
                     [], [], [], [], Position(1, 1))
    player2 = Player("Player 2", 2, 2, 2,
                     [], [], [], [], Position(width-2, height-2))
    # -----------------------------------#

    # ----------Map initial-----------#
    game_map = BattleMap(width, height, waters, woods,
                         foods, golds, player1, player2)
    # -----------------------------------#

    # ----------Year initial-----------#
    year = 617
    # -----------------------------------#

    # ----------<*Game Start*>-----------#
    print("Game Started: Little Battle! (enter QUIT to quit the game)\n")

    # ----------Draw Map-----------#
    game_map.draw_map()
    print("(enter DIS to display the map)\n\n")
    # -----------------------------------#

    # ----------Show recruit price-----------#
    show_recruit_price()
    print("(enter PRIS to display the price list)\n\n")
    # -----------------------------------#

    while True:
        # ----------Show Year-----------#
        show_year(year)
        # -----------------------------------#

        # ----------Player1 Stage_Recruit-----------#
        player1, game_map = recruit_stage(
            player1, player2, game_map, True)
        # -----------------------------------#

        # ----------Player1 Stage_Move-----------#
        player1, player2, game_map = move_stage(
            player1, player2, game_map, [], True, year)
        # -----------------------------------#

        # ----------Player2 Stage_Recruit-----------#
        player2, game_map = recruit_stage(
            player2, player1, game_map, True)
        # -----------------------------------#

        # ----------Player2 Stage_Move-----------#
        player2, player1, game_map = move_stage(
            player2, player1, game_map, [], True, year)
        # -----------------------------------#

        # ----------Year Pass-----------#
        year += 1
        # ------------------------------#


# region

# def army_type(player):
#     if input_content_p_xy[0] == player.spearman.x and input_content_p_xy[1] == player.spearman.y:
#         army_type = "Spearman"
#     if input_content_p_xy[0] == player.archer.x and input_content_p_xy[1] == player.archer.y:
#         army_type = "Archer"
#     if input_content_p_xy[0] == player.scout.x and input_content_p_xy[1] == player.scout.y:
#         army_type = "Scout"
#     if input_content_p_xy[0] == player.knight.x and input_content_p_xy[1] == player.knight.y:
#         army_type = "Knight"
#     return army_type


# def lose_armies(player_position, battle_map, player, enemy):

#     lose_army = False
#     for point in battle_map.waters:
#         if player_position.x == point.x and player_position.y == point.y:
#             lose_army = True
#     for point in player

#     enemy_armies = enemy.spearman + enemy.archer + enemy.scout + enemy.knight
#     for point in enemy_armies:
#         if input_content_p_xy[2].x


# def lose_armies(enemy):
#     lose_army = True
#     for point in BattleMap.waters:
#         if input_content_p_xy[2].x == BattleMap.waters.x and input_content_p_xy[3].y == BattleMap.waters.y:
#             lose_army = False
#     enemy_armies = enemy.spearman + enemy.archer + enemy.scout + enemy.knight
#     for point in enemy_armies:
#         if input_content_p_xy[2].x


# def invalid_condition():
#     condition = False
#     if not has_armies_in_list and input_content_p_xy[2] != player.home.x and input_content_p_xy[3] != player.home.y:
#         if input_content_p_xy[2] <= width or input_content_p_xy[3] <= height:
#             if input_content_p_xy[2] != input_content_p_xy[0] and input_content_p_xy[3] != input_content_p_xy[1]:
#                 condition = True
#     return condition


# def win():
#     if input_content_p_xy[2].x == player.home.x and input_content_p_xy[3].y == player.home.y:

# endregion
