import sys
 
# Please implement this function according to Section "Read Configuration File"
#-----------loading map functions----------#
# region
def format_check(content):
    check=True
    content_array=content.splitlines(keepends=False)
    if len(content_array)!=5:
        check=False
    else:
        if not "Frame:" in content_array[0] and not "Water:" in content_array[1] and not "Wood:" in content_array[2] and not "Food:" in content_array[3] and not "Gold:" in content_array[4]:
            check=False
    if not check:
        print("Invalid Configuration File: format error!")
    return check


def format_error_check(content):
    check=True
    content_array=content.splitlines(keepends=False)
    
    word = content_array[0].replace("Frame: ", "")
    if "x" not in word:
        check=False
    else:
        map_wh = word.split("x")
        if(len(map_wh)==2):
            width,width_isnumber=int_try_parse(map_wh[0])
            height,height_isnumber=int_try_parse(map_wh[1])
            if width_isnumber and height_isnumber:
                check=True
            else:
                check=False
        else:
            check=False
    if not check:
        print("Invalid ConfigurationFile: frame should be in format widthxheight!")
    return check
    

def frame_out_of_range_check(content):
    check=True
    content_array=content.splitlines(keepends=False)
    word = content_array[0].replace("Frame: ", "")
    map_wh = word.split("x")
    width,width_isnumber=int_try_parse(map_wh[0])
    height,height_isnumber=int_try_parse(map_wh[1])
    if width<5 or width >7 or height<5 or height>7:
        check=False
    if not check:
        print("Invalid Configuration File: width and height should range from 5 to 7!")
    return check
 
 
def remove_all_number_space(word):
    word=word.replace(" ", "")
    word=word.replace("0", "")
    word=word.replace("1", "")
    word=word.replace("2", "")
    word=word.replace("3", "")
    word=word.replace("4", "")
    word=word.replace("5", "")
    word=word.replace("6", "")
    word=word.replace("7", "")
    word=word.replace("8", "")
    word=word.replace("9", "")
    return word
 
 
def non_integer_check(content):
    check=True
    word_type=""
    for word in content.splitlines(keepends=False):
        if "Water: " in word:
            word_type="Water"
            word = word.replace("Water: ", "")
            word=remove_all_number_space(word)
            if word!="":
                check=False
        elif "Wood: " in word:
            word = word.replace("Wood: ", "")
            word_type="Wood"
            word = word.replace("Wood: ", "")
            word=remove_all_number_space(word)
            if word!="":
                check=False
        elif "Food: " in word:
            word = word.replace("Food: ", "")
            word_type="Food"
            word = word.replace("Food: ", "")
            word=remove_all_number_space(word)
            if word!="":
                check=False
        elif "Gold: " in word:
            word = word.replace("Gold: ", "")
            word_type="Gold"
            word = word.replace("Gold: ", "")
            word=remove_all_number_space(word)
            if word!="":
                check=False
    
    if not check:
        print("Invalid Configuration File: {} contains non integer characters!".format(word_type))
    return check


def out_of_map_check(content):
    check=True
    word_type=""
    if not check:
        print("Invalid Configuration File: <line_name> contains a position that is out of map.".format(word_type))
    return check


def occupy_home_or_next_to_home_check(content):
    check=True
    if not check:
        print("Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!")
    return check


def duplicate_position_check(content):
    check=True
    if not check:
        print("Invalid Configuration File: Duplicate position (x, y)!")
    return check


def odd_length_check(content):
    check=True
    word_type=""
    if not check:
        print("Invalid Configuration File: {} has an odd number of elements!".format(word_type))
    return check


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
    check=True
    try:
        f = open(filepath, 'r')
        content = f.read() 
        #-------------loading test------------#
        if format_check(content):
            check=False
        if check:
            check=format_error_check(content)
        if check:
            check=frame_out_of_range_check(content)
        if check:
            check=non_integer_check(content)
        #-------------練習----------------#
        if check:
            check=out_of_map_check(content)
        if check:
            check=occupy_home_or_next_to_home_check(content)
        if check:
            check=duplicate_position_check(content)
        if check:
            check=odd_length_check(content)
        #-------------------------------#
        #-------------------------------------#
        
        #---------- txt complete without err -----------#
        if check:
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
            print("Configuration file config.txt was loaded.")
    except IOError:
        check=False
        print("FileNotFoundError")
    finally:
        f.close()
    return width, height, waters, woods, foods, golds

# endregion
#-----------------------------------------#


#------------Game classes--------------#
# region


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
                if int(a.x) == int(x) and int(a.y) == int(y):
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
# endregion
#-----------------------------------------#

#------------common functions--------------#
# region


def replace_position_in_array(old_position, new_position, position_array):
    i = 0
    tmp_position_array = position_array
    for p in position_array:
        if(int(p.x) == int(old_position.x) and int(p.y) == int(old_position.y)):
            tmp_position_array[i] = new_position
        i += 1
    return tmp_position_array


def remove_first_position_in_array(remove_position, position_array):
    i = 0
    for p in position_array:
        if(int(p.x) == int(remove_position.x) and int(p.y) == int(remove_position.y)):
            del position_array[i]
            return position_array
        i += 1
    return position_array


def check_position_in_array(position, position_array):
    for p in position_array:
        if int(position.x) == int(p.x) and int(position.y) == int(p.y):
            return True
    return False


def int_try_parse(value):  # return value (int or string), canParse or not (boolean)
    try:
        return int(value), True
    except ValueError:
        return value, False


# endregion
#-----------------------------------------#


#------------show msg functions------------#
# region


def show_recruit_price():  # show recruit price list
    print("Recruit Prices:")
    print("  Spearman (S) - 1W, 1F")
    print("  Archer (A) - 1W, 1G")
    print("  Knight (K) - 1F, 1G")
    print("  Scout (T) - 1W, 1F, 1G")


def show_year(year):  # show year each round need to show
    print("-Year "+str(year)+"-\n")


def show_asstes(palyer):  # show player assets - Wood , Gold , Food
    print("[Your Asset: Wood - {} Food - {} Gold - {}]".format(palyer.wood,
                                                                 palyer.food, palyer.gold))
# endregion
#-----------------------------------------#


#------------recruit stage functions-----------#
# region
def show_recruit_msg(recruit_type, check_home_p, check_p_empty_list, player, enemy, game_map):
    while True:
        input_content = input(
            "You want to recruit a {}. Enter two integers as format ‘x y’ to place your army.\n".format(
                recruit_type)
        )
        #-------------edge case------------------#
        if input_content == 'DIS':
            game_map.draw_map()
            print()
        elif input_content == 'PRIS':
            show_recruit_price()
            print()
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
                print("Sorry, invalid input. Try again.\n")
        #-------------negative case---------------#
        else:
            print("Sorry, invalid input. Try again.\n")


# check home 4 position is empty
def check_home_place_empty(armies, check_p, check_p_list):
    for p in armies:
        if (int(p.x) == int(check_p[0].x) and int(p.y) == int(check_p[0].y)) and check_p_list[0]:
            check_p_list[0] = False
        if (int(p.x) == int(check_p[1].x) and int(p.y) == int(check_p[1].y)) and check_p_list[1]:
            check_p_list[1] = False
        if(int(p.x) == int(check_p[2].x) and int(p.y) == int(check_p[2].y)) and check_p_list[2]:
            check_p_list[2] = False
        if(int(p.x) == int(check_p[3].x) and int(p.y) == int(check_p[3].y)) and check_p_list[3]:
            check_p_list[3] = False
    return check_p_list


# recruit_stage return player_info,map_info
def recruit_stage(player, enemy, game_map, show_player_msg):
    if show_player_msg:
        print("+++"+player.name+"'s Stage: Recruit Armies+++\n")


    #-------------check resource is enough-------------#
    # region
    if (player.wood == 0 and player.food == 0) or (player.wood == 0 and player.gold == 0) or (player.gold == 0 and player.food == 0):
        show_asstes(player)
        print('No resources to recruit any armies.\n')
        return player, game_map
    # endregion
    #-------------show player resource-------------#
    show_asstes(player)
    print()
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
            "Which type of army to recruit, (enter) ‘S’, ‘A’, ‘K’, or ‘T’? Enter ‘NO’ to end this stage.\n")

        #-------------edge case------------------#
        if input_content == 'DIS':
            game_map.draw_map()
            print()
        elif input_content == 'PRIS':
            show_recruit_price()
            print()
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
                print()
                player, game_map = show_recruit_msg("Spearman", check_home_p,
                                                    check_p_empty_list, player, enemy, game_map)
                return player, game_map
        elif input_content == 'A':
            #------------edge case-----------#
            if player.wood == 0 or player.gold == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                print()
                player, game_map = show_recruit_msg("Archer", check_home_p,
                                                    check_p_empty_list, player, enemy, game_map)
                return player, game_map
        elif input_content == 'K':
            #------------edge case-----------#
            if player.gold == 0 or player.food == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                print()
                player, game_map = show_recruit_msg("Knight", check_home_p,
                                                    check_p_empty_list, player, enemy, game_map)
                return player, game_map
        elif input_content == 'T':
            #------------edge case-----------#
            if player.wood == 0 or player.food == 0 or player.gold == 0:
                print("Insufficient resources. Try again.\n")
            #---------positive case----------#
            else:
                print()
                player, game_map = show_recruit_msg("Scout", check_home_p,
                                                    check_p_empty_list, player, enemy, game_map)
                return player, game_map
        #-------------negative case---------------#
        else:
            print("Sorry, invalid input. Try again.\n")
    # endregion
# endregion
#-----------------------------------------#

#------------move stage functions-----------#
# region


def armies_info(player, army_type, player_already_move):  # show can move armies_info
    armies_info = ""
    armies_first_for_no_comma = True

    armies = []
    next_line = True
    if army_type == "Spearman":
        armies = player.spearman
        if len(player.archer) == 0 and len(player.scout) == 0 and len(player.knight) == 0:
            next_line = False
    elif army_type == "Archer":
        armies = player.archer
        if len(player.scout) == 0 and len(player.knight) == 0:
            next_line = False
    elif army_type == "Knight":
        armies = player.knight
        if len(player.scout) == 0:
            next_line = False
    elif army_type == "Scout":
        armies = player.scout
        next_line = False

    for p in armies:
        check_already_move = True
        for a_p in player_already_move:
            if p.x == a_p.x and p.y == a_p.y:
                check_already_move = False
                break
        if check_already_move:
            if armies_first_for_no_comma:
                armies_info = armies_info+"({}, {})".format(p.x, p.y)
            else:
                armies_info = armies_info+", ({}, {})".format(p.x, p.y)
            armies_first_for_no_comma = False
    if armies_info != "":
      if next_line:
          armies_info = "  {}: {}\n".format(army_type, armies_info)
      else:
          armies_info = "  {}: {}".format(army_type, armies_info)

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
    if check_position_in_array(end_position, armis):
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


def meet_solider_or_nothing(army_position, step, army_type, player, enemy, player_already_move, step_count):
    army_alive = False
    # meet spearman
    if check_position_in_array(step, enemy.spearman):
        enemy_type = "Spearman"
        if army_type == "Spearman":
            player.spearman = remove_first_position_in_array(
                army_position, player.spearman)
            enemy.spearman = remove_first_position_in_array(
                step, enemy.spearman)
            print("We destroyed the enemy {} with massive loss!\n".format(enemy_type))
        elif army_type == "Archer":
            player.archer = replace_position_in_array(
                army_position, step, player.archer)
            enemy.spearman = remove_first_position_in_array(
                step, enemy.spearman)
            print("Great! We defeated the enemy {}!\n".format(enemy_type))
            army_alive = True
            if step_count == 0:
                player_already_move.append(step)
        elif army_type == 'Knight':
            player.knight = remove_first_position_in_array(
                army_position, player.knight)
            print("We lost the army {} due to your command!\n".format(army_type))
        elif army_type == 'Scout':
            player.scout = remove_first_position_in_array(
                army_position, player.scout)
            print("We lost the army {} due to your command!\n".format(army_type))
    # meet archer
    elif check_position_in_array(step, enemy.archer):
        enemy_type = "Archer"
        if army_type == "Spearman":
            player.spearman = remove_first_position_in_array(
                army_position, player.spearman)
            print("We lost the army {} due to your command!\n".format(army_type))
        elif army_type == "Archer":
            player.archer = remove_first_position_in_array(
                army_position, player.archer)
            enemy.archer = remove_first_position_in_array(step, enemy.archer)
            print("We destroyed the enemy {} with massive loss!\n".format(enemy_type))
        elif army_type == 'Knight':
            player.knight = replace_position_in_array(
                army_position, step, player.knight)
            enemy.archer = remove_first_position_in_array(step, enemy.archer)
            print("Great! We defeated the enemy {}!\n".format(enemy_type))
            army_alive = True
            if step_count == 0:
                player_already_move.append(step)
        elif army_type == 'Scout':
            player.scout = remove_first_position_in_array(
                army_position, player.scout)
            print("We lost the army {} due to your command!\n".format(army_type))
    # meet knight
    elif check_position_in_array(step, enemy.knight):
        enemy_type = "Knight"
        if army_type == "Spearman":
            player.spearman = replace_position_in_array(
                army_position, step, player.spearman)
            enemy.knight = remove_first_position_in_array(step, enemy.knight)
            print("Great! We defeated the enemy {}!\n".format(enemy_type))
            army_alive = True
            if step_count == 0:
                player_already_move.append(step)
        elif army_type == "Archer":
            player.archer = remove_first_position_in_array(
                army_position, player.archer)
            print("We lost the army {} due to your command!\n".format(army_type))
        elif army_type == 'Knight':
            player.knight = remove_first_position_in_array(
                army_position, player.knight)
            enemy.knight = remove_first_position_in_array(step, enemy.knight)
            print("We destroyed the enemy {} with massive loss!\n".format(enemy_type))
        elif army_type == 'Scout':
            player.scout = remove_first_position_in_array(
                army_position, player.scout)
            print("We lost the army {} due to your command!\n".format(army_type))
    # meet scout
    elif check_position_in_array(step, enemy.scout):
        enemy_type = "Scout"
        if army_type == "Spearman":
            player.spearman = replace_position_in_array(
                army_position, step, player.spearman)
            enemy.scout = remove_first_position_in_array(step, enemy.scout)
            print("Great! We defeated the enemy {}!\n".format(enemy_type))
            army_alive = True
            if step_count == 0:
                player_already_move.append(step)
        elif army_type == "Archer":
            player.archer = replace_position_in_array(
                army_position, step, player.archer)
            enemy.scout = remove_first_position_in_array(step, enemy.scout)
            print("Great! We defeated the enemy {}!\n".format(enemy_type))
        elif army_type == 'Knight':
            player.knight = replace_position_in_array(
                army_position, step, player.knight)
            enemy.scout = remove_first_position_in_array(step, enemy.scout)
            print("Great! We defeated the enemy {}!\n".format(enemy_type))
        elif army_type == 'Scout':
            print("We destroyed the enemy {} with massive loss!".format(enemy_type))
            player.scout = remove_first_position_in_array(
                army_position, player.scout)
            enemy.scout = remove_first_position_in_array(step, enemy.scout)
    # notthiig
    else:
        army_alive = True
        player = army_move(army_type, army_position, step, player)
        if step_count == 0:
            player_already_move.append(step)

    return player, enemy, army_alive, player_already_move


def army_move(army_type, army_position, step, player):
    if army_type == "Spearman":
        player.spearman = replace_position_in_array(
            army_position, step, player.spearman)
    elif army_type == "Archer":
        player.archer = replace_position_in_array(
            army_position, step, player.archer)
    elif army_type == 'Knight':
        player.knight = replace_position_in_array(
            army_position, step, player.knight)
    elif army_type == 'Scout':
        player.scout = replace_position_in_array(
            army_position, step, player.scout)
    return player


def move_result(army_position, step, battle_map, player, enemy, army_type, player_already_move, step_count):
    army_alive = True
    #-------- win game status -------#
    if int(enemy.home.x) == int(step.x) and int(enemy.home.y) == int(step.y):
        print("The army {} captured the enemy’s capital.\n".format(army_type))
        cmd_name = input("What’s your name, commander?\n")
        print("\n***Congratulation! Emperor {} unified the country in {}.***".format(cmd_name, year))
        exit()
    #-------- get resource status -------#
    elif check_position_in_array(step, battle_map.woods):
        player.wood = player.wood+2
        battle_map.woods = remove_first_position_in_array(
            step, battle_map.woods)
        player = army_move(army_type, army_position, step, player)
        if step_count == 0:
            player_already_move.append(step)
            print("Good. We collected 2 Wood.\n")
        else:
            print("Good. We collected 2 Wood.")
    elif check_position_in_array(step, battle_map.foods):
        player.food = player.food+2
        battle_map.foods = remove_first_position_in_array(
            step, battle_map.foods)
        player = army_move(army_type, army_position, step, player)
        if step_count == 0:
            player_already_move.append(step)
            print("Good. We collected 2 Food.\n")
        else:
            print("Good. We collected 2 Food.")
    elif check_position_in_array(step, battle_map.golds):
        player.gold = player.gold+2
        battle_map.golds = remove_first_position_in_array(
            step, battle_map.golds)
        player = army_move(army_type, army_position, step, player)
        if step_count == 0:
            player_already_move.append(step)
            print("Good. We collected 2 Gold.\n")
        else:
            print("Good. We collected 2 Gold.")
    #-------- meet water status -------#
    elif check_position_in_array(step, battle_map.waters):
        if army_type == 'Spearman':
            player.spearman = remove_first_position_in_array(
                army_position, player.spearman)
        elif army_type == 'Archer':
            player.archer = remove_first_position_in_array(
                army_position, player.archer)
        elif army_type == 'Knight':
            player.knight = remove_first_position_in_array(
                army_position, player.knight)
        elif army_type == 'Scout':
            player.scout = remove_first_position_in_array(
                army_position, player.scout)
        army_alive = False
        print("We lost the army {} due to your command!\n".format(army_type))
    #-------- meet solider or nothing -------#
    else:
        player, enemy, army_alive, player_already_move = meet_solider_or_nothing(
            army_position, step, army_type, player, enemy, player_already_move, step_count)

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
                        Position(int(start_position.x), int(start_position.y)+1))
                else:
                    all_step.append(
                        Position(int(start_position.x), int(start_position.y)-1))
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
    i = 1
    #--------move_result-----------#
    for step in all_step:
        if army_alive:
            player, enemy, battle_map, army_alive, player_already_move = move_result(
                start_position, step, battle_map, player, enemy, army_type, player_already_move, len(all_step)-i)
        start_position = step
        i = i+1

    return player, enemy, battle_map, player_already_move


def move_stage(player, enemy, game_map, show_player_msg, year):
    player_already_move = []
    if show_player_msg:
        print("==={}'s Stage: Move Armies===\n".format(player.name))
    while True:
        armies = player.spearman+player.archer+player.knight+player.scout
        for p in player_already_move:
            armies = remove_first_position_in_array(p, armies)
        #------------check player army exist----------#
        if len(armies) == 0:
            print("No Army to Move: next turn.\n")
            return player, enemy, game_map
        else:
            print("Armies to Move:")
            armies_info_show = ""
            for army_type in ["Spearman", "Archer", "Knight", "Scout"]:
                armies_info_show = armies_info_show + \
                    armies_info(player, army_type, player_already_move)
            print(armies_info_show)
            input_content = input(
                "\nEnter four integers as a format ‘x0 y0 x1 y1’ to represent move unit from (x0, y0) to (x1, y1) or ‘NO’ to end this turn.\n")
            #-------------edge case------------------#
            if input_content == 'DIS':
                game_map.draw_map()
                print()
            elif input_content == 'PRIS':
                show_recruit_price()
                print()
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
                            print("\nYou have moved {} from ({}, {}) to ({}, {}).".format(
                                army_type, start_position.x, start_position.y, end_position.x, end_position.y))

                            player, enemy, game_map, player_already_move = valid_move(player, enemy, game_map, army_type,
                                                                                      start_position, end_position, year, player_already_move)
                        #-------------behave as move result:invalid move---------------#
                        else:
                            print("Invalid move. Try again.\n")
                else:
                    print("Invalid move. Try again.\n")
            #-------------negative case---------------#
            else:
                print("Invalid move. Try again.\n")

#  endregion
#-------------------------------------------#

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 little_battle.py <filepath>")
        sys.exit()
    # -------- load config.txt -----------#
    width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])
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
    print("(enter DIS to display the map)\n")
    # -----------------------------------#

    # ----------Show recruit price-----------#
    show_recruit_price()
    print("(enter PRIS to display the price list)\n")
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
            player1, player2, game_map, True, year)
        # -----------------------------------#

        # ----------Player2 Stage_Recruit-----------#
        show_year(year)
        player2, game_map = recruit_stage(
            player2, player1, game_map, True)
        # -----------------------------------#
        print()
        # ----------Player2 Stage_Move-----------#
        player2, player1, game_map = move_stage(
            player2, player1, game_map, True, year)
        # -----------------------------------#

        # ----------Year Pass-----------#
        year += 1
        # ------------------------------#
