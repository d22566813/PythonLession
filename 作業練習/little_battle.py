import sys

# Please implement this function according to Section "Read Configuration File"


class battle_map:
  # 建構式
    def __init__(self, width, height, waters, woods, foods, golds, h1, h2):
        self.width = width
        self.height = height
        self.waters = waters
        self.woods = woods
        self.foods = foods
        self.golds = golds
        self.h1 = h1
        self.h2 = h2

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
            for a in assets:
                if a.x == x and a.y == y:
                    h_s = h_s+icon
                    empty = False
                    break
        return h_s, empty

    def draw_map(self):
        print("Please check the battlefield, commander.")
        w = 0
        w_s = ""
        w_ys = ""
        while w < self.width:
            if w == 0:
                w_s = w_s+"0"+str(w)
                w_ys = w_ys+"--"
            else:
                w_s = w_s+" 0"+str(w)
                w_ys = w_ys+"---"
            w = w+1
        w_s = "  X"+w_s+"X"
        w_ys = " Y+"+w_ys+"+"
        y = 0
        h_s = ""
        while y < self.height:
            h_s = h_s+"0"+str(y)
            x = 0
            while x < self.width:
                h_s = h_s+"|"
                empty = True
                if self.h1.x == x and self.h1.y == y:
                    h_s = h_s+"H1"
                    empty = False
                elif self.h2.x == x and self.h2.y == y:
                    h_s = h_s+"H2"
                    empty = False
                for icon in ['~~', 'WW', 'FF', 'GG']:
                    h_s, empty = self.draw_map_assets(icon, h_s, x, y, empty)
                if empty:
                    h_s = h_s+"  "
                if x == (self.width-1):
                    h_s = h_s+"|"
                x += 1
            if y != (self.height-1):
                h_s = h_s+"\n"
            y += 1
        print(w_s)
        print(w_ys)
        print(h_s)
        print(w_ys)


class Position:
  # 建構式
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Player:
  # 建構式
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


def load_config_file(filepath):
    # It should return width, height, waters, woods, foods, golds based on the file
    # Complete the test driver of this function in file_loading_test.py
    width, height = 0, 0
    waters, woods, foods, golds = [], [], [], []  # list of position tuples
    f = open(filepath, 'r')
    content = f.read()
    for word in content.splitlines(keepends=False):
        # word = word.replace("Frame: ", "")
        # print(word)
        if "Frame: " in word:
            word = word.replace("Frame: ", "")
            map_wh = word.split("x")
            width = int(map_wh[0])
            height = int(map_wh[1])
            # print(word)
        elif "Water: " in word:
            word = word.replace("Water: ", "")
            assets = word.split(" ")
            # print("Water: ")
            # print(assets)
            # print("-------")
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

    return width, height, waters, woods, foods, golds


def show_recruit_price():
    print("Recruit Prices:")
    print("Spearman (S) -1W, 1F")
    print("Archer (A) -1W, 1G")
    print("Knight (K) -1F, 1G")
    print("Scout (T) -1W, 1F, 1G")


def show_year(year):
    print("-Year "+str(year)+"-\n")


def show_asstes(palyer):
    print("[Your Asset: Wood - {} Food - {} Gold - {}]".format(palyer.wood,
                                                               palyer.food, palyer.gold))


def show_recruit_msg(recruit_type):
    input_content = input(
        "You want to recruit a {}.Enter two integers as format 'x y' to place your army.", recruit_type)
    input_xy = input_content.splt(' ')


def check_home_base_empy(armies, check_p, check_p_list):
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


def recruit_stage(player, bt_map):
    print("+++"+player.name+"'s Stage: Recruit Armies+++")
    show_asstes(player)
    input_content = ""
    if (player.wood == 0 and player.food == 0) or (player.wood == 0 and player.gold == 0) or (player.gold == 0 and player.food == 0):
        print('No resources to recruit any armies.')
        return

    check_p = [Position(player.home.x-1, player.home.y),
               Position(player.home.x+1, player.home.y),
               Position(player.home.x, player.home.y+1),
               Position(player.home.x, player.home.y-1)
               ]
    check_p_list = [True, True, True, True]

    check_p_list = check_home_base_empy(player.spearman, check_p, check_p_list)
    check_p_list = check_home_base_empy(player.archer, check_p, check_p_list)
    check_p_list = check_home_base_empy(player.knight, check_p, check_p_list)
    check_p_list = check_home_base_empy(player.scout, check_p, check_p_list)

    check = True

    for c in check_p_list:
        if c:
            check = False

    if check:
        print('No place to recruit any armies.')
        return

    while input_content != 'NO':
        input_content = input(
            "Which type of army to recruit, (enter) 'S', 'A', 'K', or 'T'? Ener 'NO' to end this stage.\n")
        if input_content == 'DIS':
            bt_map.draw_map()
        elif input_content == 'PRIS':
            show_recruit_price()
        elif input_content == 'QUIT':
            exit()
        elif input_content == 'S':
            show_recruit_msg("Spearman")
            show_asstes(player)
        elif input_content == 'A':
            show_recruit_msg("Archer")
            show_asstes(player)
        elif input_content == 'K':
            show_recruit_msg("Knight")
            show_asstes(player)
        elif input_content == 'T':
            show_recruit_msg("Scout")
            show_asstes(player)
        else:
            print("Sorry, invalid input Try again.")


def move_stage():
    print("")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 little_battle.py <filepath>")
        sys.exit()
    # -------- load config.txt -----------#
    width, height, waters, woods, foods, golds = load_config_file(sys.argv[1])
    # -----------------------------------#

    # ----------Player initial-----------#
    player1 = Player("Player 1", 2, 2, 2, [], [], [], [], Position(1, 1))
    player2 = Player("Player 2", 2, 2, 2, [], [], [],
                     [], Position(width-2, height-2))
    # -----------------------------------#

    # ----------Map initial-----------#
    game_map = battle_map(width, height, waters, woods,
                          foods, golds, player1.home, player2.home)
    # -----------------------------------#

    # ----------Year initial-----------#
    year = 617
    # -----------------------------------#

    # ----------Game Start-----------#
    print("Configuration file config.txt was loaded.")
    print("Game Started: Little Battle! (enter QUIT to quit the game)\n")

    # ----------Draw Map-----------#
    game_map.draw_map()

    print("(enter DIS to display the map)\n\n")
    show_recruit_price()
    print("(enter PRIS to display the price list)\n\n")
    # ----------Show Year-----------#
    show_year(year)

    # ----------Stage_Recruit-----------#
    recruit_stage(player1, game_map)
    # -----------------------------------#
    # ----------Stage_MOve-----------#
    # move_stage(player1, game_map)
    # -----------------------------------#
