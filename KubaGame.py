from copy import deepcopy


class KubaGame:
    """represent a board game"""

    def __init__(self, player_A, player_B):
        """initializes private data members"""
        self._player_A_name = player_A[0]
        self._player_A_color = player_A[1]
        self._player_B_name = player_B[0]
        self._player_B_color = player_B[1]
        self._previous_turn = None
        self._winner = None
        self._white_count = 8
        self._black_count = 8
        self._red_count = 13
        self._previous_board = None
        self._player_A_capture = 0
        self._player_B_capture = 0
        self._board = [["W", "W", "X", "X", "X", "B", "B"],
                       ["W", "W", "X", "R", "X", "B", "B"],
                       ["X", "X", "R", "R", "R", "X", "X"],
                       ["X", "R", "R", "R", "R", "R", "X"],
                       ["X", "X", "R", "R", "R", "X", "X"],
                       ["B", "B", "X", "R", "X", "W", "W"],
                       ["B", "B", "X", "X", "X", "W", "W"]]

    def make_move(self, player_name, coordinates, direction):
        """takes three parameters player_name, coordinates containing the location of marble that
        is being moved and the direction in which the player wants to push the marble. Return True
        if the move is successful, else return False"""
        if not self.validate_move(player_name, coordinates, direction):
            return False
        else:
            self.move_marble(player_name, coordinates, direction)
            self._previous_turn = player_name

        return True

    def validate_move(self, player_name, coordinates, direction):
        """takes three parameters player_name, coordinates, and direction. Returns False if the move
        is being made after the game has been won, or when it's not the player's turn, or if the
        coordinates provided are not valid, or a marble in the coordinates cannot be moved in the
        direction specified, or it is not the player's marble, or if the current move will duplicate
        the previous game board. Return True if the move is valid"""
        if self._winner is not None or self._previous_turn == player_name:
            return False

        if player_name == self._player_A_name:
            if self._board[coordinates[0]][coordinates[1]] != self._player_A_color:
                return False

        if player_name == self._player_B_name:
            if self._board[coordinates[0]][coordinates[1]] != self._player_B_color:
                return False

        # check if coordinates are out of range

        board_range = [0, 1, 2, 3, 4, 5, 6]
        if coordinates[0] not in board_range or coordinates[1] not in board_range:
            return False

        # check if direction is a valid input

        direction_option = ["L", "R", "F", "B"]

        if direction not in direction_option:
            return False

        # check if the move resulted in the same positioning as the previous board

        previous_board = deepcopy(self._previous_board)
        current_board = deepcopy(self._board)
        marble_counts = list([self._white_count, self._black_count, self._red_count,
                              self._player_A_capture, self._player_B_capture])
        self.move_marble(player_name, coordinates, direction)
        if self._board == previous_board:
            self._board = current_board
            self._white_count = marble_counts[0]
            self._black_count = marble_counts[1]
            self._red_count = marble_counts[2]
            self._player_A_capture = marble_counts[3]
            self._player_B_capture = marble_counts[4]
            return False
        self._board = current_board
        self._white_count = marble_counts[0]
        self._black_count = marble_counts[1]
        self._red_count = marble_counts[2]
        self._player_A_capture = marble_counts[3]
        self._player_B_capture = marble_counts[4]

        # check the adjacent cell opposite to the pushing direction is vacant and if a player is pushing
        # its own marble off the board for pushing in the left direction

        if direction == "L":

            if coordinates[1] == 0:
                return False

            if coordinates[1] != 6:
                if self._board[coordinates[0]][coordinates[1] + 1] != "X":
                    return False

            if "X" not in self._board[coordinates[0]][:coordinates[1]]:

                if player_name == self._player_A_name:
                    if self._board[coordinates[0]][0] == self._player_A_color:
                        return False

                if player_name == self._player_B_name:
                    if self._board[coordinates[0]][0] == self._player_B_color:
                        return False

        # check the adjacent cell opposite to the pushing direction is vacant and if a player is pushing
        # its own marble off of the board for pushing in the right direction

        if direction == "R":

            if coordinates[1] == 6:
                return False

            if coordinates[1] != 0:
                if self._board[coordinates[0]][coordinates[1] - 1] != "X":
                    return False

            if "X" not in self._board[coordinates[0]][coordinates[1] + 1:]:

                if player_name == self._player_A_name:
                    if self._board[coordinates[0]][6] == self._player_A_color:
                        return False

                if player_name == self._player_B_name:
                    if self._board[coordinates[0]][6] == self._player_B_color:
                        return False

        # check the adjacent cell opposite to the pushing direction is vacant and if a player is pushing
        # its own marble off of the board for pushing in the forward direction

        if direction == "F":

            if coordinates[0] == 0:
                return False

            if coordinates[0] != 6:
                if self._board[coordinates[0] + 1][coordinates[1]] != "X":
                    return False

            check_space = []
            for idx in range(0, coordinates[0]):
                check_space.append(self._board[idx][coordinates[1]])

            if "X" not in check_space:

                if player_name == self._player_A_name:
                    if self._board[0][coordinates[1]] == self._player_A_color:
                        return False

                if player_name == self._player_B_name:
                    if self._board[0][coordinates[1]] == self._player_B_color:
                        return False

        # check the adjacent cell opposite to the pushing direction is vacant and if a player is pushing
        # its own marble off of the board for pushing in the backward direction

        if direction == "B":

            if coordinates[0] == 6:
                return False

            if coordinates[0] != 0:
                if self._board[coordinates[0] - 1][coordinates[1]] != "X":
                    return False

            check_space = []
            for idx in range(coordinates[0] + 1, 7):
                check_space.append(self._board[idx][coordinates[1]])

            if "X" not in check_space:

                if player_name == self._player_A_name:
                    if self._board[6][coordinates[1]] == self._player_A_color:
                        return False

                if player_name == self._player_B_name:
                    if self._board[6][coordinates[1]] == self._player_B_color:
                        return False

        return True

    def move_marble(self, player_name, coordinates, direction):
        """takes three parameters player_name, coordinates, and direction and push the marble in the
        direction in the given direction"""

        self._previous_board = deepcopy(self._board)

        if direction == "L":
            for idx in range(coordinates[1], 0, -1):
                if self._board[coordinates[0]][idx - 1] == "X":
                    self._board[coordinates[0]][idx - 1] = self._previous_board[coordinates[0]][idx]
                    break
                self._board[coordinates[0]][idx - 1] = self._previous_board[coordinates[0]][idx]
            self._board[coordinates[0]][coordinates[1]] = "X"

            if "X" not in self._previous_board[coordinates[0]][:coordinates[1]]:
                self.update_marble_count(direction, player_name, coordinates)
                self.update_winner()

        if direction == "R":
            for idx in range(coordinates[1], 6):
                if self._board[coordinates[0]][idx + 1] == "X":
                    self._board[coordinates[0]][idx + 1] = self._previous_board[coordinates[0]][idx]
                    break
                self._board[coordinates[0]][idx + 1] = self._previous_board[coordinates[0]][idx]
            self._board[coordinates[0]][coordinates[1]] = "X"

            if "X" not in self._previous_board[coordinates[0]][coordinates[1] + 1:]:
                self.update_marble_count(direction, player_name, coordinates)
                self.update_winner()

        if direction == "F":
            for idx in range(coordinates[0], 0, -1):
                if self._board[idx - 1][coordinates[1]] == "X":
                    self._board[idx - 1][coordinates[1]] = self._previous_board[idx][coordinates[1]]
                    break
                self._board[idx - 1][coordinates[1]] = self._previous_board[idx][coordinates[1]]
            self._board[coordinates[0]][coordinates[1]] = "X"

            check_space = []
            for idx in range(0, coordinates[0]):
                check_space.append(self._previous_board[idx][coordinates[1]])

            if "X" not in check_space:
                self.update_marble_count(direction, player_name, coordinates)
                self.update_winner()

        if direction == "B":
            for idx in range(coordinates[0], 6):
                self._board[coordinates[0]][coordinates[1]] = "X"
                if self._board[idx + 1][coordinates[1]] == "X":
                    self._board[idx + 1][coordinates[1]] = self._previous_board[idx][coordinates[1]]
                    break
                self._board[idx + 1][coordinates[1]] = self._previous_board[idx][coordinates[1]]
            self._board[coordinates[0]][coordinates[1]] = "X"

            check_space = []
            for idx in range(coordinates[0], 7):
                check_space.append(self._previous_board[idx][coordinates[1]])

            if "X" not in check_space:
                self.update_marble_count(direction, player_name, coordinates)
                self.update_winner()

    def update_marble_count(self, direction, player_name, coordinates):
        """takes four parameters: direction, player_name, coordinates, and previous_board. Updates
        marble count based on the color of the marble got pushed off"""
        if direction == "L":
            if self._previous_board[coordinates[0]][0] == "R":
                self.update_red_marble_count(player_name)

            if self._previous_board[coordinates[0]][0] == "W":
                self._white_count -= 1

            if self._previous_board[coordinates[0]][0] == "B":
                self._black_count -= 1

        if direction == "R":
            if self._previous_board[coordinates[0]][6] == "R":
                self.update_red_marble_count(player_name)

            if self._previous_board[coordinates[0]][6] == "W":
                self._white_count -= 1

            if self._previous_board[coordinates[0]][6] == "B":
                self._black_count -= 1

        if direction == "F":
            if self._previous_board[0][coordinates[1]] == "R":
                self.update_red_marble_count(player_name)

            if self._previous_board[0][coordinates[1]] == "W":
                self._white_count -= 1

            if self._previous_board[0][coordinates[1]] == "B":
                self._black_count -= 1

        if direction == "B":
            if self._previous_board[6][coordinates[1]] == "R":
                self.update_red_marble_count(player_name)

            if self._previous_board[6][coordinates[1]] == "W":
                self._white_count -= 1

            if self._previous_board[6][coordinates[1]] == "B":
                self._black_count -= 1

    def update_red_marble_count(self, player_name):
        """updates red_marble_count based on player's name"""
        if player_name == self._player_A_name:
            self._player_A_capture += 1
        if player_name == self._player_B_name:
            self._player_B_capture += 1
        self._red_count -= 1

    def update_winner(self):
        """updates winner if a player has captured seven neutral red stones or by pushing off all of
        the opposing stones or if one of the players has no available legal moves"""

        if self._player_A_capture > 6:
            self._winner = self._player_A_name

        elif self._player_B_capture > 6:
            self._winner = self._player_B_name

        if self._black_count == 0 and self._player_A_color == "B":
            self._winner = self._player_B_name

        elif self._white_count == 0 and self._player_A_color == "W":
            self._winner = self._player_B_name

        elif self._black_count == 0 and self._player_B_color == "B":
            self._winner = self._player_A_name

        elif self._white_count == 0 and self._player_B_color == "W":
            self._winner = self._player_A_name

    def get_current_turn(self):
        """returns the player name whose turn it is to play the game. It will return None if
        the first move hasn't been made yet"""

        if self._previous_turn is None:
            return None
        elif self._previous_turn == self._player_A_name:
            return self._player_B_name
        else:
            return self._player_A_name

    def get_winner(self):
        """returns the name of the winning player. If no player has won yet, it returns None."""

        if self._winner is None:
            return None
        else:
            return self._winner

    def get_captured(self, player_name):
        """takes player's name as parameter and returns the number of Red marbles captured by the
        player."""

        if player_name == self._player_A_name:
            return self._player_A_capture
        elif player_name == self._player_B_name:
            return self._player_B_capture

    def get_marble(self, coordinates):
        """takes the coordinates of a cell as a tuple and returns the marble that is present at the
        location."""

        return self._board[coordinates[0]][coordinates[1]]

    def get_marble_count(self):
        """returns the number of White marbles, Black marbles and Red marbles as tuple in the order
         (W,B,R)."""

        W_B_R_count = self._white_count, self._black_count, self._red_count
        return W_B_R_count

    def print_board(self):
        """print current state of the board"""
        for row in self._board:
            print(row)