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

# help anaylize map txt fuction


def set_assets(assets):
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

# loading map message by txt


def load_config_file(filepath):
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


# show recruit price list
def show_recruit_price():
    print("Recruit Prices:")
    print("  Spearman (S) -1W, 1F")
    print("  Archer (A) -1W, 1G")
    print("  Knight (K) -1F, 1G")
    print("  Scout (T) -1W, 1F, 1G")

# show year each round need to show


def show_year(year):
    print("-Year "+str(year)+"-\n")

# show player assets - Wood , Gold , Food


def show_asstes(palyer):
    print("[Your Asset: Wood - {} Food - {} Gold - {}]\n".format(palyer.wood,
                                                                 palyer.food, palyer.gold))

# string to int return value (int or string), canParse or not (boolean)


def int_try_parse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False

# enter recruit x y position use in recruit_stage


def show_recruit_msg(recruit_type, check_home_p, check_p_empty_list, player, game_map):
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
                            player, game_map, False)
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

# check home 4 position is empty (checkArray,home_4_position_list,check_result_list)


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


def recruit_stage(player, game_map, show_player_msg):
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

    check_p_empty_list = check_home_place_empty(
        player.spearman, check_home_p, check_p_empty_list)
    check_p_empty_list = check_home_place_empty(
        player.archer, check_home_p, check_p_empty_list)
    check_p_empty_list = check_home_place_empty(
        player.knight, check_home_p, check_p_empty_list)
    check_p_empty_list = check_home_place_empty(
        player.scout, check_home_p, check_p_empty_list)

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
                                                    check_p_empty_list, player, game_map)
                return player, game_map
        elif input_content == 'A':
            #------------edge case-----------#
            if player.wood == 0 or player.gold == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                player, game_map = show_recruit_msg("Archer", check_home_p,
                                                    check_p_empty_list, player, game_map)
            return player, game_map
        elif input_content == 'K':
            #------------edge case-----------#
            if player.gold == 0 or player.food == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                player, game_map = show_recruit_msg("Knight", check_home_p,
                                                    check_p_empty_list, player, game_map)
                return player, game_map
        elif input_content == 'T':
            #------------edge case-----------#
            if player.wood == 0 or player.food == 0 or player.gold == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                player, game_map = show_recruit_msg("Scout", check_home_p,
                                                    check_p_empty_list, player, game_map)
                return player, game_map
        #-------------negative case---------------#
        else:
            print("Sorry, invalid input Try again.\n")
    # endregion


def move_stage():
    print("")


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

    # ----------Show Year-----------#
    show_year(year)
    # -----------------------------------#

    # ----------Stage_Recruit-----------#
    player1, game_map = recruit_stage(player1, game_map, True)
    # -----------------------------------#

    # ----------Stage_Move-----------#
    # move_stage(player1, game_map)
    # -----------------------------------#
