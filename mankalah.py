import copy


# Инициализация доски
def initialize_board():
    return [4, 4, 4, 4, 4, 4,  # корзины игрока 1
            0,  # кала игрока 1
            4, 4, 4, 4, 4, 4,  # корзины игрока 2
            0]  # кала игрока 2


# Проверка конца игры
def game_over(board):
    return sum(board[0:6]) == 0 or sum(board[7:13]) == 0


# Оценочная функция
def evaluate(board):
    my_kalah = board[6]
    opponent_kalah = board[13]
    my_side = sum(board[0:6])
    opponent_side = sum(board[7:13])
    capture_threats = sum(board[12 - i] for i in range(6) if board[i] == 0 and board[12 - i] > 0)
    extra_turns_potential = sum(1 for i in range(6) if board[i] == 6 - i)

    return (
            (my_kalah - opponent_kalah) * 5 +  # Разница в очках
            (my_side - opponent_side) * 2 +  # Контроль камней
            extra_turns_potential * 4 -  # Возможные дополнительные ходы
            capture_threats * 4  # Угрозы захвата
    )


# Нормализация оценки в вероятность победы
def win_probability(evaluation):
    return 1 / (1 + 2.71828 ** (-evaluation / 20))  # Сигмоида для нормализации


# Получение всех возможных ходов
def get_valid_moves(board, player):
    if player == 1:
        return [i for i in range(6) if board[i] > 0]
    else:
        return [i for i in range(7, 13) if board[i] > 0]


# Выполнение хода
def make_move(board, move, player):
    new_board = copy.deepcopy(board)
    if player == 1:
        start, kalah, opponent_kalah = 0, 6, 13
    else:
        start, kalah, opponent_kalah = 7, 13, 6

    stones = new_board[move]
    new_board[move] = 0
    index = move

    while stones > 0:
        index = (index + 1) % 14
        if index == opponent_kalah:
            continue
        new_board[index] += 1
        stones -= 1

    if index == kalah:  # Дополнительный ход
        return new_board, True

    # Захват камней
    if start <= index < start + 6 and new_board[index] == 1 and new_board[12 - index] > 0:
        new_board[kalah] += new_board[12 - index] + 1
        new_board[index] = 0
        new_board[12 - index] = 0

    return new_board, False


# Алгоритм Альфа-бета отсечения с сохранением последовательности ходов
def alphabeta(board, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate(board), []

    if is_maximizing_player:
        max_eval = float('-inf')
        best_move = None
        best_sequence = []
        for move in get_valid_moves(board, player=1):
            new_board, extra_turn = make_move(board, move, player=1)
            eval, sequence = alphabeta(new_board, depth - 1 + int(extra_turn), alpha, beta, not extra_turn)
            if eval > max_eval:
                max_eval = eval
                best_move = move
                best_sequence = [move] + sequence
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_sequence
    else:
        min_eval = float('inf')
        best_move = None
        best_sequence = []
        for move in get_valid_moves(board, player=2):
            new_board, extra_turn = make_move(board, move, player=2)
            eval, sequence = alphabeta(new_board, depth - 1 + int(extra_turn), alpha, beta, not extra_turn)
            if eval < min_eval:
                min_eval = eval
                best_move = move
                best_sequence = [move] + sequence
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_sequence


# Игровой цикл
def play_game():
    board = initialize_board()
    player_turn = 1

    while not game_over(board):
        print(f"Текущая доска: {board}")
        if player_turn == 1:
            evaluation, best_sequence = alphabeta(board, depth=5, alpha=float('-inf'), beta=float('inf'),
                                                  is_maximizing_player=True)
            probability = win_probability(evaluation)
            print(
                f"Игрок 1 выбирает корзину {best_sequence[0]} (оценка: {evaluation}, вероятность победы: {probability:.2f})")
        else:
            evaluation, best_sequence = alphabeta(board, depth=5, alpha=float('-inf'), beta=float('inf'),
                                                  is_maximizing_player=False)
            probability = win_probability(-evaluation)
            print(
                f"Игрок 2 выбирает корзину {best_sequence[0]} (оценка: {evaluation}, вероятность победы: {probability:.2f})")

        board, extra_turn = make_move(board, best_sequence[0], player_turn)
        if not extra_turn:
            player_turn = 3 - player_turn  # Переключение хода

    print(f"Конец игры! Итоговая доска: {board}")
    print(f"Игрок 1: {board[6]}, Игрок 2: {board[13]}")


# Запуск игры
if __name__ == "__main__":
    play_game()
