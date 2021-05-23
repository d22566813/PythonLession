from little_battle import load_config_file
# Don't remove any comments in this file
folder_path = "./invalid_files/"

# Please create appropriate invalid files in the folder "invalid_files"
# for each unit test according to the comments below and
# then complete them according to the function name


def test_file_not_found():
    # no need to create a file for FileNotFound
    load_config_file(folder_path+"test.txt")
    pass


def test_format_error():
    # add "format_error_file.txt" in "invalid_files"
    load_config_file(folder_path+"format_error_file.txt")
    pass


def test_frame_format_error():
    # add "frame_format_error_file.txt" in "invalid_files"
    load_config_file(folder_path+"frame_format_error_file.txt")
    pass


def test_frame_out_of_range():
    # add "format_out_of_range_file.txt" in "invalid_files"
    load_config_file(folder_path+"format_out_of_range_file.txt")
    pass


def test_non_integer():
    # add "non_integer_file.txt" in "invalid_files"
    load_config_file(folder_path+"non_integer_file.txt")
    pass


def test_out_of_map():
    # add "out_of_map_file.txt" in "invalid_files"

    # from the second line to the last line
    # 標籤後的座標須在地圖內
    # 印出 Invalid Configuration File: <line_name> contains a position that is out of map.
    load_config_file(folder_path+"out_of_map_file.txt")
    pass


def test_occupy_home_or_next_to_home():
    # add two invalid files: "occupy_home_file.txt" and
    # "occupy_next_to_home_file.txt" in "invalid_files"

    # from the second line to the last line
    # 基地與基地四周不得有資源
    # 印出 Invalid Configuration File: The positions of home bases or the positions next to the home bases are occupied!
    load_config_file(folder_path+"occupy_home_file.txt")
    load_config_file(folder_path+"occupy_next_to_home_file.txt")
    pass


def test_duplicate_position():
    # add two files: "dupli_pos_in_single_line.txt" and
    # "dupli_pos_in_multiple_lines.txt" in "invalid_files"

    # from the second line to the last line
    # 資源的座標不得重複
    # 印出 Invalid Configuration File: Duplicate position (x, y)!
    load_config_file(folder_path+"dupli_pos_in_single_line.txt")
    load_config_file(folder_path+"dupli_pos_in_multiple_lines.txt")
    pass


def test_odd_length():
    # add "odd_length_file.txt" in "invalid_files"

    # from the second line to the last line
    # 標籤後面的數字數量必須是偶數
    # Invalid Configuration File: <line_name (e.g., Water)> has an odd number of elements!
    load_config_file(folder_path+"odd_length_file.txt")
    pass


def test_valid_file():
    # no need to create file for this one, just test loading config.txt
    load_config_file("config.txt")
    pass


# you can run this test file to check tests and load_config_file
if __name__ == "__main__":
    test_file_not_found()
    test_format_error()
    test_frame_format_error()
    test_frame_out_of_range()
    test_non_integer()
    test_out_of_map()
    test_occupy_home_or_next_to_home()
    test_duplicate_position()
    test_odd_length()
    test_valid_file()
