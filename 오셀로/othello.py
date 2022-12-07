import sys
import random

input = sys.stdin.readline


class Board:
    def __init__(self) -> None:
        self.__BOARD_SIZE: int = 8
        self.__board: list[list[str]]

    def initialize(self) -> None:
        self.__board = [["+"] * self.__BOARD_SIZE for _ in range(self.__BOARD_SIZE)]

        self.__board[3][3] = self.__board[4][4] = "O"
        self.__board[4][3] = self.__board[3][4] = "X"

    def get_board(self) -> list[list[str]]:
        return self.__board


class Game:
    def __init__(self) -> None:
        self.__score: list[int] = [0, 0]
        self.__turn: int = 0
        self.__player: int
        self.__player_symbol: str

        self.__board: Board = Board()
        self.__algorithm: Algorithm = Algorithm()

    def __set_player(self) -> None:
        print("Enter 0 for First Turn, 1 for Second Turn.")

        temp: str = input().rstrip()
        while not (temp == "0" or temp == "1"):
            print("Wrong Input. Enter again.")
            temp = input().rstrip()

        self.__player = int(temp)
        self.__player_symbol: str = "O" if self.__player == 0 else "X"

    def __show_score(self) -> None:
        self.__score = [0, 0]

        for board_col in self.__board.get_board():
            self.__score[0] += board_col.count("O")
            self.__score[1] += board_col.count("X")

        if self.__player == 0:
            print("Player {0} : {1} Computer".format(*self.__score))
        else:
            print("Computer {0} : {1} Player".format(*self.__score))

    def __show_board(self) -> None:
        print(end="  ")
        print(*range(0, len(self.__board.get_board())))

        for i in range(len(self.__board.get_board())):
            print(i, end=" ")
            print(*self.__board.get_board()[i], end=" ")
            print(i)

        print(end="  ")
        print(*range(0, len(self.__board.get_board())))

    def __show_result(self) -> None:
        self.__show_score()
        self.__show_board()

        if self.__score[self.__player] > self.__score[self.__player ^ 1]:
            print("Player Win")
        else:
            print("Computer Win")

    def __set_index(self) -> list[int]:
        index = ""

        while True:
            index = input().rstrip()

            try:
                index = list(map(int, index.split()))

                if (
                    len(index) == 2
                    and 0 <= index[0] < len(self.__board.get_board())
                    and 0 <= index[1] < len(self.__board.get_board())
                ):
                    break
                else:
                    print("Unavailable index. Enter again.")
            except:
                print("Unavailable index. Enter again.")

        return index[::-1]

    def start(self) -> None:
        self.__set_player()

        self.__board.initialize()

        pass_count = 0

        while True:
            if self.__algorithm.check_blank(self.__board.get_board()) == False:
                break

            self.__show_score()
            self.__show_board()

            if self.__algorithm.check_pass(self.__board.get_board(), self.__turn):
                print("PASSED")
                pass_count += 1

                if pass_count == 2:
                    break
            else:
                if self.__turn == self.__player:
                    print(
                        "Your Symbol is {0}. Enter the index x y. (ex. 1 3)".format(
                            self.__player_symbol
                        )
                    )

                    index: list[int] = self.__set_index()

                    while not self.__algorithm.add_player(
                        self.__board.get_board(), index, self.__turn
                    ):
                        print("Unavailable index. Enter again.")
                        index = self.__set_index()
                else:
                    print("Computer's turn.")
                    self.__algorithm.add_computer(self.__board.get_board(), self.__turn)

                pass_count = 0

            self.__turn ^= 1

        self.__show_result()


class Algorithm:
    def __init__(self) -> None:
        self.__adder: list[list[int]] = [
            [-1, 0],
            [-1, 1],
            [0, 1],
            [1, 1],
            [1, 0],
            [1, -1],
            [0, -1],
            [-1, -1],
        ]

    def add_player(self, BOARD: list[list[str]], INDEX: list[int], turn: int) -> bool:
        if self.__cal_weight(BOARD, turn)[INDEX[0]][INDEX[1]]:
            self.__flip(BOARD, INDEX, turn)

            return True
        else:
            return False

    def add_computer(self, BOARD: list[list[str]], turn: int) -> None:
        weight = self.__cal_weight(BOARD, turn)
        weight_max = 1
        weight_max_list = []

        for i in range(len(BOARD)):
            for j in range(len(BOARD)):
                if weight[i][j] > weight_max:
                    weight_max_list.clear()
                    weight_max = weight[i][j]
                    weight_max_list.append([i, j])
                elif weight[i][j] == weight_max:
                    weight_max_list.append([i, j])

        self.__flip(BOARD, random.choice(weight_max_list), turn)

    def check_pass(self, board: list[list[str]], turn: int) -> bool:
        if sum(sum(self.__cal_weight(board, turn), [])):
            return False
        else:
            return True

    def check_blank(self, BOARD: list[list[str]]) -> bool:
        if sum(BOARD, []).count("+"):
            return True
        else:
            return False

    def __flip(self, board: list[list[str]], INDEX: list[int], turn: int) -> None:
        turn_symbol: str = "O" if turn == 0 else "X"

        board[INDEX[0]][INDEX[1]] = turn_symbol

        for adder_i in self.__adder:
            di: int = INDEX[0]
            dj: int = INDEX[1]

            add_list: list = []

            while True:
                di, dj = di + adder_i[0], dj + adder_i[1]

                if not (0 <= di < len(board) and 0 <= dj < len(board)):
                    add_list.clear()
                    break

                if board[di][dj] == "+":
                    add_list.clear()
                    break

                if board[di][dj] == turn_symbol:
                    break
                else:
                    add_list.append([di, dj])

            for add_list_i in add_list:
                di, dj = add_list_i

                board[di][dj] = turn_symbol

    def __cal_weight(self, BOARD: list[list[str]], turn: int) -> list[list[int]]:
        weight: list[list[int]] = [[0] * len(BOARD) for _ in range(len(BOARD))]

        turn_symbol: str = "O" if turn == 0 else "X"

        for i in range(len(BOARD)):
            for j in range(len(BOARD)):
                if BOARD[i][j] == "+":
                    for adder_i in self.__adder:
                        di: int = i
                        dj: int = j
                        weight_count: int = 0

                        while True:
                            di, dj = di + adder_i[0], dj + adder_i[1]

                            if not (0 <= di < len(BOARD) and 0 <= dj < len(BOARD)):
                                weight_count = 0
                                break

                            if BOARD[di][dj] == "+":
                                weight_count = 0
                                break

                            if BOARD[di][dj] == turn_symbol:
                                break
                            else:
                                weight_count += 1

                        weight[i][j] += weight_count
                else:
                    weight[i][j] = 0

        return weight


my_game = Game()

my_game.start()
