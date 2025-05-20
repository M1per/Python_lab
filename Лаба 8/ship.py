import tkinter as tk
from tkinter import messagebox
import random
from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class ShipPlacementError(Exception):
    pass


class InvalidCoordinateError(Exception):
    pass


class CellState(Enum):
    EMPTY = 0
    SHIP = 1
    MISS = 2
    HIT = 3
    SUNK = 4


class PlayerType(Enum):
    PLAYER1 = 0
    PLAYER2 = 1


class Ship:
    def __init__(self, size, name):
        self.size = size
        self.name = name
        self.hits = 0
        self.sunk = False
        self.cells = []

    def hit(self):
        self.hits += 1
        if self.hits >= self.size:
            self.sunk = True
            for cell in self.cells:
                cell.state = CellState.SUNK
            return True
        return False


class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = CellState.EMPTY
        self.ship = None

    def __str__(self):
        return f"({self.row}, {self.col})"

    def set_ship(self, ship):
        self.state = CellState.SHIP
        self.ship = ship
        ship.cells.append(self)


class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[Cell(row, col) for col in range(size)] for row in range(size)]
        self.ships = []
        self.ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.ship_names = ["Линкор", "Крейсер 1", "Крейсер 2",
                           "Эсминец 1", "Эсминец 2", "Эсминец 3",
                           "Катер 1", "Катер 2", "Катер 3", "Катер 4"]

    def is_valid_coordinate(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def place_ship(self, row, col, size, orientation):
        if not self.is_valid_coordinate(row, col):
            raise InvalidCoordinateError("Недопустимые координаты")

        cells = []
        for i in range(size):
            if orientation == Orientation.HORIZONTAL:
                new_row, new_col = row, col + i
            else:
                new_row, new_col = row + i, col

            if not self.is_valid_coordinate(new_row, new_col):
                raise ShipPlacementError("Корабль выходит за границы поля")

            for r in range(new_row - 1, new_row + 2):
                for c in range(new_col - 1, new_col + 2):
                    if self.is_valid_coordinate(r, c) and self.grid[r][c].state == CellState.SHIP:
                        raise ShipPlacementError("Корабли не могут соприкасаться")

            cells.append(self.grid[new_row][new_col])

        ship = Ship(size, self.ship_names[len(self.ships)])
        for cell in cells:
            cell.set_ship(ship)
        self.ships.append(ship)

    def auto_place_ships(self):
        for size in self.ship_sizes:
            placed = False
            attempts = 0
            while not placed and attempts < 100:
                attempts += 1
                try:
                    orientation = random.choice([Orientation.HORIZONTAL, Orientation.VERTICAL])
                    row = random.randint(0, self.size - 1)
                    col = random.randint(0, self.size - 1)
                    self.place_ship(row, col, size, orientation)
                    placed = True
                except (ShipPlacementError, InvalidCoordinateError):
                    pass
            if not placed:
                raise ShipPlacementError("Не удалось автоматически разместить корабли")

    def receive_attack(self, row, col):
        if not self.is_valid_coordinate(row, col):
            raise InvalidCoordinateError("Недопустимые координаты")

        cell = self.grid[row][col]
        if cell.state in [CellState.HIT, CellState.MISS, CellState.SUNK]:
            raise InvalidCoordinateError("Уже стреляли в эту клетку")

        if cell.state == CellState.SHIP:
            cell.state = CellState.HIT
            sunk = cell.ship.hit()
            return True, sunk
        else:
            cell.state = CellState.MISS
            return False, False

    def all_ships_sunk(self):
        return all(ship.sunk for ship in self.ships)


class SeaBattleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Морской бой - Игрок 1 vs Игрок 2")
        self.game = Game()

        self.font = ("Arial", 12)
        self.bold_font = ("Arial", 12, "bold")

        self.setup_frames()
        self.setup_boards()
        self.setup_info_panels()

        self.game_status = tk.Label(self.main_frame, text="Ход Игрока 1", font=self.bold_font)
        self.game_status.grid(row=2, column=0, columnspan=4, pady=10)

        restart_btn = tk.Button(self.main_frame, text="Новая игра", command=self.restart_game, font=self.font)
        restart_btn.grid(row=3, column=0, columnspan=4, pady=10)

        # Начинаем с хода первого игрока
        self.enable_current_player()

    def setup_frames(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10)

        # Фреймы для досок и информации
        self.player1_frame = tk.Frame(self.main_frame)
        self.player1_frame.grid(row=0, column=0, padx=10)

        self.player1_info_frame = tk.Frame(self.main_frame)
        self.player1_info_frame.grid(row=0, column=1, padx=10, sticky="n")

        self.player2_frame = tk.Frame(self.main_frame)
        self.player2_frame.grid(row=0, column=3, padx=10)

        self.player2_info_frame = tk.Frame(self.main_frame)
        self.player2_info_frame.grid(row=0, column=2, padx=10, sticky="n")

    def setup_boards(self):
        letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'К']

        # Доска Игрока 1 (для выстрелов Игрока 2) - слева
        tk.Label(self.player1_frame, text="Поле Игрока 1", font=self.bold_font).grid(row=0, column=0, columnspan=12)
        self.player1_shots = []

        for col in range(10):
            tk.Label(self.player1_frame, text=letters[col]).grid(row=1, column=col + 2)

        for row in range(10):
            tk.Label(self.player1_frame, text=str(row + 1)).grid(row=row + 2, column=1)
            button_row = []
            for col in range(10):
                btn = tk.Button(self.player1_frame, width=2, height=1, bg="lightblue",
                                command=lambda r=row, c=col: self.make_shot(PlayerType.PLAYER2, r, c))
                btn.grid(row=row + 2, column=col + 2)
                button_row.append(btn)
            self.player1_shots.append(button_row)

        # Доска Игрока 2 (для выстрелов Игрока 1) - справа
        tk.Label(self.player2_frame, text="Поле Игрока 2", font=self.bold_font).grid(row=0, column=0, columnspan=12)
        self.player2_shots = []

        for col in range(10):
            tk.Label(self.player2_frame, text=letters[col]).grid(row=1, column=col + 2)

        for row in range(10):
            tk.Label(self.player2_frame, text=str(row + 1)).grid(row=row + 2, column=1)
            button_row = []
            for col in range(10):
                btn = tk.Button(self.player2_frame, width=2, height=1, bg="lightblue",
                                command=lambda r=row, c=col: self.make_shot(PlayerType.PLAYER1, r, c))
                btn.grid(row=row + 2, column=col + 2)
                button_row.append(btn)
            self.player2_shots.append(button_row)

    def setup_info_panels(self):
        # Информация о кораблях Игрока 1 (слева от его поля)
        tk.Label(self.player1_info_frame, text="Корабли Игрока 1:", font=self.bold_font).pack(anchor=tk.W)
        self.player1_ships_info = tk.Label(self.player1_info_frame,
                                           text=self.get_ships_info(self.game.player1_board),
                                           font=self.font, justify=tk.LEFT)
        self.player1_ships_info.pack(anchor=tk.W)

        # Информация о кораблях Игрока 2 (справа от его поля)
        tk.Label(self.player2_info_frame, text="Корабли Игрока 2:", font=self.bold_font).pack(anchor=tk.W)
        self.player2_ships_info = tk.Label(self.player2_info_frame,
                                           text=self.get_ships_info(self.game.player2_board),
                                           font=self.font, justify=tk.LEFT)
        self.player2_ships_info.pack(anchor=tk.W)

    def get_ships_info(self, board):
        ships_info = []
        for ship in board.ships:
            status = "потоплен" if ship.sunk else "цел" if ship.hits == 0 else f"ранен ({ship.hits}/{ship.size})"
            ships_info.append(f"{ship.name}: {status}")
        return "\n".join(ships_info)

    def make_shot(self, player, row, col):
        if player != self.game.current_player:
            messagebox.showwarning("Не ваш ход", f"Сейчас ход Игрока {self.game.current_player.value + 1}!")
            return

        try:
            if player == PlayerType.PLAYER1:
                target_board = self.game.player2_board
                shots_board = self.player2_shots
                opponent_name = "Игрока 2"
            else:
                target_board = self.game.player1_board
                shots_board = self.player1_shots
                opponent_name = "Игрока 1"

            hit, sunk = target_board.receive_attack(row, col)
            shots_board[row][col].config(state=tk.DISABLED)

            if hit:
                shots_board[row][col].config(bg="red", text="X")
                if sunk:
                    messagebox.showinfo("Потоплен!",
                                        f"Игрок {player.value + 1} потопил {target_board.grid[row][col].ship.name} {opponent_name}!")

                if target_board.all_ships_sunk():
                    messagebox.showinfo("Победа!",
                                        f"Игрок {player.value + 1} победил! Все корабли {opponent_name} потоплены.")
                    self.disable_all_buttons()
                    return

                self.game_status.config(text=f"Попадание! Игрок {player.value + 1} стреляет снова")
            else:
                shots_board[row][col].config(bg="white", text="•")
                self.game.current_player = PlayerType.PLAYER2 if player == PlayerType.PLAYER1 else PlayerType.PLAYER1
                self.game_status.config(text=f"Ход Игрока {self.game.current_player.value + 1}")
                self.enable_current_player()

            self.player1_ships_info.config(text=self.get_ships_info(self.game.player1_board))
            self.player2_ships_info.config(text=self.get_ships_info(self.game.player2_board))

        except InvalidCoordinateError as e:
            messagebox.showerror("Ошибка", str(e))

    def enable_current_player(self):
        for row in range(10):
            for col in range(10):
                self.player1_shots[row][col].config(state=tk.DISABLED)
                self.player2_shots[row][col].config(state=tk.DISABLED)

        if self.game.current_player == PlayerType.PLAYER1:
            for row in range(10):
                for col in range(10):
                    if self.player2_shots[row][col]['text'] == '':
                        self.player2_shots[row][col].config(state=tk.NORMAL)
        else:
            for row in range(10):
                for col in range(10):
                    if self.player1_shots[row][col]['text'] == '':
                        self.player1_shots[row][col].config(state=tk.NORMAL)

    def disable_all_buttons(self):
        for row in range(10):
            for col in range(10):
                self.player1_shots[row][col].config(state=tk.DISABLED)
                self.player2_shots[row][col].config(state=tk.DISABLED)

    def restart_game(self):
        self.root.destroy()
        root = tk.Tk()
        game = SeaBattleGUI(root)
        root.mainloop()


class Game:
    def __init__(self):
        self.player1_board = Board()
        self.player2_board = Board()
        self.current_player = PlayerType.PLAYER1
        self.setup_game()

    def setup_game(self):
        self.player1_board.auto_place_ships()
        self.player2_board.auto_place_ships()


if __name__ == "__main__":
    root = tk.Tk()
    game = SeaBattleGUI(root)
    root.mainloop()