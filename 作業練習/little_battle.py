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

def has_armies():
    has_armies_in_list = False
    armies_info = ""
    armies += player.spearman + player.archer + player.scout + player.knight
    for a in armies:
        if a.x == input_content_p_xy[0] and a.y == input_content_p_xy[1]:
            has_armies_in_list = True
            break
    return has_armies_in_list

def invalid_condition():
    condition = False
    if not has_armies_in_list and input_content_p_xy[2] != player.home.x and input_content_p_xy[3] != player.home.y:
        if input_content_p_xy[2] <= width or input_content_p_xy[3] <= height:
           if input_content_p_xy[2] != input_content_p_xy[0] and input_content_p_xy[3] != input_content_p_xy[1]:
               condition = True
    return condition

def available_destination():    
    armies_sak = player.spearman + player.archer + player.knight
    armies_t = player.scout
    good_destination = False
    final_destination = False
    for point in armies_sak:
        if point.x == input_content_p_xy[2] and point.y == input_content_p_xy[3]:
            if input_content_p_xy[2] - input_content_p_xy[0] == 1 and input_content_p_xy[3] - input_content_p_xy[1] == 1:
                good_destination = True
                if good_destination and condition:
                    final_destination = True
                    if input_content_p_xy[2].x == player.home.x and input_content_p_xy[3].y == player.home.y:
                        
    for point in armies_t:
        if point.x == input_content_p_xy[2] and point.y == input_content_p_xy[3]:
            if (input_content_p_xy[2] - input_content_p_xy[0] == 1 and input_content_p_xy[3] - input_content_p_xy[1] == 1) \
                or (input_content_p_xy[2] - input_content_p_xy[0] == 2 and input_content_p_xy[3] - input_content_p_xy[1] == 2):
                if good_destination and condition:
                    final_destination = True
    return final_destination 
        
def army_type(player):
    if input_content_p_xy[0] == player.spearman.x and input_content_p_xy[1] == player.spearman.y:
         army_type = "Spearman"
    if input_content_p_xy[0] == player.archer.x and input_content_p_xy[1] == player.archer.y:
         army_type = "Archer"
    if input_content_p_xy[0] == player.scout.x and input_content_p_xy[1] == player.scout.y:
         army_type = "Scout"
    if input_content_p_xy[0] == player.knight.x and input_content_p_xy[1] == player.knight.y:
         army_type = "Knight"
    return army_type

def lose_armies(enemy):
    lose_army = True
    for point in BattleMap.waters:
        if input_content_p_xy[2].x == BattleMap.waters.x and input_content_p_xy[3].y == BattleMap.waters.y:
            lose_army = False
    enemy_armies = enemy.spearman + enemy.archer + enemy.scout + enemy.knight
    for point in enemy_armies:
        if input_content_p_xy[2].x

def win():
    if input_content_p_xy[2].x == player.home.x and input_content_p_xy[3].y == player.home.y:


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
                    if has_armies_in_list and final_destination:
                        print("You have moved {} from ({}, {}) to ({}, {}).".format(army_type, input_content_p_xy[0], input_content_p_xy[1], input_content_p_xy[2], input_content_p_xy[3]))
                        if 
                    else:



                    

        # region
        # 起始點 x0 y0 是否玩家為移動的兵中有此座標
        # t: 有
        #    已知道是什麼兵種
        #     終點的有效條件
        #     1.不可以相同
        #     2.不可以再地圖外
        #     3.不可以在自己的兵上
        #     4.不可以在自己的基地
        #     5.終點與起點只能差一步 （偵察兵 兩步）
        #        t:
        #             1.You have moved < Spearman/Archer/Knight/Scout > from (x0, y0) to(x1, y1).
        #             2.move result
        #                volid move 的條件
        #                     1.踩到敵人基地
        #                        1.問指揮官名字
        #                         2.印出恭喜
        #                         3.exist()
        #                     2.兵死掉了
        #                        1.只有他死掉
        #                            player.spearman.remove((x0, y0))
        #                         2.自己死掉敵人也死掉
        #                            player.spearman.remove((x0, y0))
        #                             enemy.spearman.remove((x0, y0))
        #                     3.兵沒死
        #                        1.到新的座標
        #                            player.spearman[0]. x跟y改成新座標
        #                             player_already_move.append(x1, y1)

        #             3.move_stage(player, player_already_move, enemy, game_map,False)

        #         f: Invalid move. Try again
        #             move_stage(player, enemy, game_map, False)
        # f: Invalid move. Try again
        #     move_stage(player, enemy, game_map, False)
        # endregion
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
