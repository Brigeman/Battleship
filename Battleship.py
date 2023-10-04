import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hits = [False] * len(coordinates)

    def is_sunk(self):
        return all(hit for hit in self.hits)

class Board:
    def __init__(self, ships):
        self.board_size = 6
        self.board = [['О' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ships = ships
        self.place_ships()

    def place_ships(self):
        for ship in self.ships:
            for point in ship.coordinates:
                self.board[point.y][point.x] = '■'

    def display(self):
        print("  | 1 | 2 | 3 | 4 | 5 | 6 |")
        for i in range(self.board_size):
            row = f"{i + 1} | {' | '.join(self.board[i])} |"
            print(row)

    def shoot(self, point, enemy_ships):
        x, y = point.x, point.y

        for ship in enemy_ships:
            for ship_point in ship.coordinates:
                if ship_point.x == x and ship_point.y == y:
                    if ship.hits[ship.coordinates.index(ship_point)]:
                        print("Вы уже стреляли в эту клетку.")
                        return False
                    else:
                        ship.hits[ship.coordinates.index(ship_point)] = True
                        self.board[y][x] = 'X'
                        if ship.is_sunk():
                            print("Корабль потоплен!")
                        else:
                            print("Вы попали!")
                        return True

        self.board[y][x] = 'T'
        print("Вы промахнулись.")
        return False

def generate_ships():
    ships = []

    def is_distance_valid(ship, existing_ships):
        for existing_ship in existing_ships:
            for point in existing_ship.coordinates:
                for new_point in ship.coordinates:
                    if (
                        abs(point.x - new_point.x) <= 1
                        and abs(point.y - new_point.y) <= 1
                    ):
                        return False
        return True

    for size, count in [(3, 1), (2, 2), (1, 4)]:
        for _ in range(count):
            while True:
                direction = random.choice(["horizontal", "vertical"])
                if direction == "horizontal":
                    x = random.randint(0, 6 - size)
                    y = random.randint(0, 5)
                    coordinates = [Point(x + i, y) for i in range(size)]
                else:
                    x = random.randint(0, 5)
                    y = random.randint(0, 6 - size)
                    coordinates = [Point(x, y + i) for i in range(size)]

                if (
                    all(0 <= p.x < 6 and 0 <= p.y < 6 for p in coordinates)
                    and not any(
                        p in ship.coordinates for ship in ships for p in coordinates
                    )
                    and is_distance_valid(Ship(coordinates), ships)
                ):
                    ships.append(Ship(coordinates))
                    break
    return ships


def computer_turn(player_board, player_ships, computer_board, computer_ships):
    while True:
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        point = Point(x, y)
        if not player_board.shoot(point, player_ships):
            break

def main():
    player_ships = generate_ships()
    computer_ships = generate_ships()

    player_board = Board(player_ships)
    computer_board = Board(computer_ships)

    print("Добро пожаловать в игру 'Морской бой'!")
    print("У вас на поле 1 корабль (размер 3 клетки), 2 корабля (размер 2 клетки) и 4 корабля (размер 1 клетка).")
    print("Давайте начнем игру!\n")

    player_turn = True

    while True:
        print("Ваша доска:")
        player_board.display()
        print("\nДоска компьютера:")
        computer_board.display()

        try:
            if player_turn:
                x = int(input("Введите номер столбца (1-6): ")) - 1
                y = int(input("Введите номер строки (1-6): ")) - 1
                if 0 <= x < 6 and 0 <= y < 6:
                    point = Point(x, y)
                    if not computer_board.shoot(point, computer_ships):
                        player_turn = False
                else:
                    print("Неверные координаты. Пожалуйста, введите числа от 1 до 6.")
            else:
                print("Ход компьютера...")
                computer_turn(player_board, player_ships, computer_board, computer_ships)
                player_turn = True

            if all(ship.is_sunk() for ship in computer_ships):
                print("Вы победили! Все корабли компьютера потоплены.")
                break

            if all(ship.is_sunk() for ship in player_ships):
                print("Компьютер победил! Все ваши корабли потоплены.")
                break

        except ValueError:
            print("Неверный ввод. Пожалуйста, введите числа от 1 до 6.")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
