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


def armies_info(player, army_type, player_already_move):
    armies_info = ""
    armies_count = 0
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
        check = True
        for a_p in player_already_move:
            if p.x == a_p.x and p.y == a_p.y:
                check = False
                break
        if check:
            if armies_count == 0:
                armies_info = armies_info+"({},{})".format(p.x, p.y)
            else:
                armies_info = armies_info+", ({},{})".format(p.x, p.y)
        armies_count += 1
    armies_info = "{}: {}\n".format(army_type, armies_info)
    return armies_info


def move_step_available(army_type, start, end):
    move_step = abs(end-start)
    if army_type == 'scout':
        if not(move_step <= 2):
            return False
        else:
            return True
    else:
        if not(move_step == 1):
            return False
        else:
            return True


def available_destination(start_position, end_position, battle_map, player_already_move, player, enemy):
    has_armies, army_type, = has_armies(player, start_position)
    #  no army on that position
    if has_armies:
        return False, army_type

    #   out of map_range
    if not(end_position.x <= (battle_map.width-1) and end_position.y <= (battle_map.height-1)):
        return False, army_type

    #   not move , not on other armies position
    armis = player.spearman + player.archer + player.knight+player.scout
    #   not on home_base
    armis.append(player.home)
    if end_position in armis:
        return False, army_type

    # 每回合只能移動一次

    # 兵移動到水或是被克制的兵種
    # Scout 移動中間一步 也消失
    # 自己兵消失
    # 印出 We lost the army <Spearman/Archer/Knight/Scout> due to your command!

    # 兵移動到同兵種
    # 兩方兵消失
    # Scout 移動中間一步 也消失
    # 印出 We destroyed the enemy <Spearman/Archer/Knight/Scout> with massive loss!

    # 兵移動到克制兵種
    # 敵方兵消失
    # 印出 Great! We defeated the enemy <Spearman/Archer/Knight/Scout>!

    # 兵移動到資源
    # 資源消失
    # Scout如兩步都蒐集到資源 印兩次
    # 印出Good. We collected 2 <Wood/Food/Gold>.

    # 兵移動到敵人主堡
    # 印出 The army <Spearman/Archer/Knight/Scout> captured the enemy’s capital.
    # What’s your name, commander? 任何輸入當作名字
    # 印出 ***Congratulation! Emperor <name> unified the country in <year>.***
    # 結束遊戲

    #   go up or down
    if start_position.x == end_position.x:
        if move_step_available(army_type, end_position.y, start_position.y):
            # 兵移動到敵人主堡
            # 兵移動到資源
            # 兵移動到克制兵種
            # 兵移動到同兵種
            # 兵移動到水或是被克制的兵種

            # if army_type == "scout":

            # else:
            return True, army_type
        else:
            return False, army_type
    #   go left or right
    elif start_position.y == end_position.y:
        if move_step_available(army_type, end_position.x, start_position.x):
            return True, army_type
        else:
            return False, army_type
    #   not diagonal
    else:
        return False, army_type


def has_armies(player, position):
    if position in player.spearman:
        return True, 'spearman'
    elif position in player.archer:
        return True, 'archer'
    elif position in player.scout:
        return True, 'scout'
    elif position in player.knight:
        return True, 'knight'
    else:
        return False, 'none'


def move_stage(player, enemy, game_map, player_already_move, show_player_msg):
    if show_player_msg:
        print("==={}'s Stage: Move Armies===\n".format(player.name))

    #------------check player army exist----------#
    if len(player.spearman) == 0 and len(player.archer) == 0 and len(player.knight) == 0 and len(player.scout) == 0:
        print("No Army to Move: next turn\n")
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
                    available_destination, army_type = available_destination(
                        start_position, end_position, game_map, player)
                    #-------------behave as move result:valid move------------------#
                    if available_destination:
                        print("You have moved {} from ({}, {}) to ({}, {}).".format(
                            army_type, start_position.x, start_position.y, end_position.x, end_position.y))

                    #-------------behave as move result:invalid move---------------#
                    else:
                        print("Invalid move. Try again.\n")
        #-------------edge case------------------#
        elif input_content == 'NO':
            return player, enemy, game_map
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
            player1, player2, game_map, [], True)
        # -----------------------------------#

        # ----------Player2 Stage_Recruit-----------#
        player2, game_map = recruit_stage(
            player2, player1, game_map, True)
        # -----------------------------------#

        # ----------Player2 Stage_Move-----------#
        player2, player1, game_map = move_stage(
            player2, player1, game_map, [], True)
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
