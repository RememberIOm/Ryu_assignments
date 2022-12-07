import sys

input = sys.stdin.readline


class Game:
    def __init__(self) -> None:
        self.__mode: int
        self.__my_image: Image = Image()
        self.__my_input_method: Input_method = Input_method()

    def __set_mode(self) -> None:
        self.__mode = self.__my_input_method.mode()

    def __set_image_and_size(self) -> None:
        image_file: list[str] = self.__my_input_method.image()

        self.__my_image.set_file_name(image_file[0])
        self.__my_image.set_size(list(map(int, image_file[1].split())))
        self.__my_image.set_image([list(i) for i in image_file[2:]])

    def __default_mode(self) -> None:
        self.__set_image_and_size()

        my_ui: Ui = Ui()

        my_ui.set_image_size(self.__my_image.get_size())
        my_ui.set_hint(self.__my_image.cal_hint())

        score_max = 0
        score = 0
        for image_col in self.__my_image.get_image():
            for image_i in image_col:
                try:
                    score_max += int(image_i)
                except:
                    pass

        while True:
            my_ui.show_ui()
            print(
                "Enter the index of the pixel you want to select. Restart: 0, Quit: 1"
            )
            index: list[int] = self.__my_input_method.index(self.__my_image.get_size())

            if index == [0]:
                my_ui.set_hint(self.__my_image.cal_hint())
                score = 0
                print("Restarted.")
            elif index == [1]:
                break
            else:
                my_ui.toggle_ui(index)

                if (
                    self.__my_image.get_image()[index[1]][index[0]]
                    == my_ui.get_image()[index[1]][index[0]]
                ):
                    score += 1
                else:
                    score -= 1

            if score == score_max:
                break

            print("Score: {}".format(score))

        print("You Win!")
        print("Quit default mode.")

    def __edit_mode(self) -> None:
        self.__set_image_and_size()

        while True:
            self.__my_image.show_image()
            print(
                "Enter the index of the pixel you want to toggle with. Save: 0, Quit: 1"
            )
            index: list[int] = self.__my_input_method.index(self.__my_image.get_size())

            if index == [0]:
                temp_fstream = open(
                    "./{}.txt".format(self.__my_image.get_file_name()), "w"
                )

                temp_fstream.write(
                    " ".join(map(str, self.__my_image.get_size())) + "\n"
                )
                temp_fstream.writelines(
                    ["".join(i) for i in self.__my_image.get_image()]
                )

                temp_fstream.close()

                print("Saved.")
            elif index == [1]:
                break
            else:
                self.__my_image.toggle_image(index)
                print("Toggle complete.")

        print("Quit edit mode.")

    def start(self) -> None:
        while True:
            self.__set_mode()

            if self.__mode == 1:
                self.__default_mode()
            elif self.__mode == 2:
                self.__edit_mode()
            else:
                break

        print("Quit.")


class Ui:
    def __init__(self) -> None:
        self.__ui: list[list[str]]
        self.__hint_size: list[int] = [0, 0]
        self.__image_size: list[int] = [0, 0]

    def set_image_size(self, image_size: list[int]) -> None:
        self.__image_size = image_size

    def set_hint(self, hint: list[list[list[int]]]) -> None:
        self.__hint_size[0] = max([len(i) for i in hint[0]])  # hint_side
        self.__hint_size[1] = max([len(i) for i in hint[1]])  # hint_top

        self.__ui_init()

        # hint_side
        for hint_i in range(len(hint[0])):
            for i in range(len(hint[0][hint_i])):
                self.__ui[self.__hint_size[1] + 1 + hint_i][
                    self.__hint_size[0] - len(hint[0][hint_i]) + i
                ] = str(hint[0][hint_i][i])

        # hint_top
        for hint_i in range(len(hint[1])):
            for i in range(len(hint[1][hint_i])):
                self.__ui[self.__hint_size[1] - len(hint[1][hint_i]) + i][
                    self.__hint_size[0] + 1 + hint_i
                ] = str(hint[1][hint_i][i])

    def __ui_init(self) -> None:
        row = self.__hint_size[0] + self.__image_size[0] + 1
        col = self.__hint_size[1] + self.__image_size[1] + 1

        self.__ui = [[" "] * row for _ in range(col)]

        for i in range(row):
            self.__ui[self.__hint_size[1]][i] = "+"

        for i in range(col):
            self.__ui[i][self.__hint_size[0]] = "+"

        for i in range(self.__image_size[1]):
            for j in range(self.__image_size[0]):
                self.__ui[self.__hint_size[1] + 1 + i][
                    self.__hint_size[0] + 1 + j
                ] = "0"

    def toggle_ui(self, index: list[int]) -> None:
        if (
            self.__ui[index[1] + self.__hint_size[0] + 1][
                index[0] + self.__hint_size[1] + 1
            ]
            == "0"
        ):
            self.__ui[index[1] + self.__hint_size[0] + 1][
                index[0] + self.__hint_size[1] + 1
            ] = "1"
        else:
            self.__ui[index[1] + self.__hint_size[0] + 1][
                index[0] + self.__hint_size[1] + 1
            ] = "0"

    def show_ui(self) -> None:
        for ui_col in self.__ui:
            print(*ui_col)

    def get_image(self) -> list[list[str]]:
        image_cur: list[list[str]] = []

        for i in range(self.__image_size[1]):
            image_cur.append(
                self.__ui[self.__hint_size[1] + 1 + i][self.__hint_size[0] + 1 :]
            )

        return image_cur


class Image:
    def __init__(self) -> None:
        self.__size: list[int]
        self.__image: list[list[str]]
        self.__file_name: str

    def set_size(self, input_size: list[int]) -> None:
        self.__size = input_size

    def get_size(self) -> list[int]:
        return self.__size

    def set_image(self, input_image: list[list[str]]) -> None:
        self.__image = input_image

    def get_image(self) -> list[list[str]]:
        return self.__image

    def show_image(self) -> None:
        for image_col in self.__image:
            print(*image_col, end="")

        print()

    def toggle_image(self, index: list[int]) -> None:
        if self.__image[index[0]][index[1]] == "0":
            self.__image[index[0]][index[1]] = "1"
        else:
            self.__image[index[0]][index[1]] = "0"

    def cal_hint(self) -> list[list[list[int]]]:
        hint: list[list[list[int]]] = [[], []]

        # hint_side
        for image_col in self.__image:
            hint_col: list[int] = []

            cnt = 0
            for image_i in image_col:
                if image_i == "1":
                    cnt += 1
                else:
                    if cnt > 0:
                        hint_col.append(cnt)
                        cnt = 0

            if cnt > 0:
                hint_col.append(cnt)

            hint[0].append(hint_col)

        # hint_top
        image_rotate = list(zip(*self.__image))

        for image_row in image_rotate:
            hint_row: list[int] = []

            cnt = 0
            for image_i in image_row:
                if image_i == "1":
                    cnt += 1
                else:
                    if cnt > 0:
                        hint_row.append(cnt)
                        cnt = 0

            if cnt > 0:
                hint_row.append(cnt)

            hint[1].append(hint_row)

        return hint

    def set_file_name(self, input_file_name: str) -> None:
        self.__file_name = input_file_name

    def get_file_name(self) -> str:
        return self.__file_name


class Input_method:
    def mode(self) -> int:
        print("Select Menu.\n1. Default Mode\n2. Edit Mode\n3. Quit")

        input_mode: str = input().rstrip()

        while input_mode not in [str(i) for i in range(1, 4)]:
            print("Wrong command. Enter again.")
            print("Select Menu.\n1. Default Mode\n2. Edit Mode\n3. Quit")

            input_mode = input().rstrip()

        return int(input_mode)

    def image(self) -> list[str]:
        print("Enter the file name.")

        file_name: str = input().rstrip()

        image_return = []

        while True:
            try:
                temp_fstream = open("./{}.txt".format(file_name), "r")

                image_return.append(file_name)
                image_return.extend(temp_fstream.readlines())

                temp_fstream.close()

                return image_return
            except:
                print("Wrong file name. Enter again.")

                file_name = input().rstrip()

    def index(self, index_limit: list[int]) -> list[int]:
        input_index = input().split()

        while True:
            try:
                input_index = list(map(int, input_index))

                if input_index in [[i] for i in range(0, 2)]:
                    break

                if (
                    len(input_index) == 2
                    and 0 <= input_index[0] < index_limit[0]
                    and 0 <= input_index[1] < index_limit[1]
                ):
                    break
            except:
                pass

            print("Wrong index. Enter again")

            input_index = input().split()

        return input_index


my_game: Game = Game()

my_game.start()
