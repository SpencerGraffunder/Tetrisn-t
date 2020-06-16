from copy import copy
from client.globals import *
from common.enums import *


class Piece:

    def __init__(self, piece_type, player_number, spawn_column, player_count):

        self.piece_type = 0
        self.tile_type = 0
        self.rotation = 0
        self.locations = [None, None, None, None]  # col,row
        self.piece_type = piece_type
        self.player_number = player_number

        if self.piece_type == PieceType.I:
            self.locations[0] = (spawn_column - 2, 2)  # [-][-][-][-] | [-][-][0][-]
            self.locations[1] = (spawn_column - 1, 2)  # [-][-][-][-] | [-][-][1][-]
            self.locations[2] = (spawn_column, 2)      # [0][1][2][3] | [-][-][2][-]
            self.locations[3] = (spawn_column + 1, 2)  # [-][-][-][-] | [-][-][3][-]
            self.tile_type = TileType.IOT.value
        elif self.piece_type == PieceType.O:
            self.locations[0] = (spawn_column - 1, 2)  #
            self.locations[1] = (spawn_column, 2)      # [0][1]
            self.locations[2] = (spawn_column - 1, 3)  # [2][3]
            self.locations[3] = (spawn_column, 3)      #
            self.tile_type = TileType.IOT.value
        elif self.piece_type == PieceType.T:
            self.locations[0] = (spawn_column - 1, 2)  # [-][-][-] | [-][0][-] | [-][3][-] | [-][2][-]
            self.locations[1] = (spawn_column, 2)      # [0][1][2] | [3][1][-] | [2][1][0] | [-][1][3]
            self.locations[2] = (spawn_column + 1, 2)  # [-][3][-] | [-][2][-] | [-][-][-] | [-][0][-]
            self.locations[3] = (spawn_column, 3)      # |           |           |
            self.tile_type = TileType.IOT.value
        elif self.piece_type == PieceType.L:
            self.locations[0] = (spawn_column - 1, 2)  # [-][-][-] | [3][0][-] | [-][-][3] | [-][2][-]
            self.locations[1] = (spawn_column, 2)      # [0][1][2] | [-][1][-] | [2][1][0] | [-][1][-]
            self.locations[2] = (spawn_column + 1, 2)  # [3][-][-] | [-][2][-] | [-][-][-] | [-][0][3]
            self.locations[3] = (spawn_column - 1, 3)  # |           |           |
            self.tile_type = TileType.LZ.value
        elif self.piece_type == PieceType.J:
            self.locations[0] = (spawn_column - 1, 2)  # [-][-][-] | [-][0][-] | [3][-][-] | [-][2][3]
            self.locations[1] = (spawn_column, 2)      # [0][1][2] | [-][1][-] | [2][1][0] | [-][1][-]
            self.locations[2] = (spawn_column + 1, 2)  # [-][-][3] | [3][2][-] | [-][-][-] | [-][0][-]
            self.locations[3] = (spawn_column + 1, 3)  # |           |           |
            self.tile_type = TileType.JS.value
        elif self.piece_type == PieceType.Z:
            self.locations[0] = (spawn_column - 1, 2)  # [-][-][-] | [-][-][3]
            self.locations[1] = (spawn_column, 2)      # [0][1][-] | [-][1][2]
            self.locations[2] = (spawn_column, 3)      # [-][2][3] | [-][0][-]
            self.locations[3] = (spawn_column + 1, 3)  # |
            self.tile_type = TileType.LZ.value
        elif self.piece_type == PieceType.S:
            self.locations[0] = (spawn_column, 2)      # [-][-][-] | [-][1][-]
            self.locations[1] = (spawn_column + 1, 2)  # [-][0][1] | [-][0][3]
            self.locations[2] = (spawn_column - 1, 3)  # [2][3][-] | [-][-][2]
            self.locations[3] = (spawn_column, 3)      # |
            self.tile_type = TileType.JS.value

        if player_count != 1:
            self.tile_type = player_number

    def move(self, direction=Direction.DOWN, locations=None):

        if locations is None:
            locations = self.locations

        if direction == Direction.DOWN:
            for index, location in enumerate(locations):
                locations[index] = (location[0], location[1] + 1)
        elif direction == Direction.LEFT:
            for index, location in enumerate(locations):
                locations[index] = (location[0] - 1, location[1])
        elif direction == Direction.RIGHT:
            for index, location in enumerate(locations):
                locations[index] = (location[0] + 1, location[1])

    # Direction == None for no direction (spawning)
    def can_move(self, board, players, direction):

        test_locations = copy(self.locations)

        # If not spawning piece
        if direction is not None:
            self.move(direction, test_locations)

        for location in test_locations:
            if location[1] >= len(board) \
                    or location[0] < 0 \
                    or location[0] >= len(board[0]):
                return MoveAllowance.CANT_BOARD

            if direction is not None:
                if board[location[1]][location[0]].tile_type != TileType.BLANK:
                    return MoveAllowance.CANT_BOARD

            for player in players:
                if player.active_piece is not None:
                    if player.active_piece.player_number != self.player_number:
                        for other_location in player.active_piece.locations:
                            if other_location == location:
                                return MoveAllowance.CANT_PIECE

        return MoveAllowance.CAN

    def rotate(self, rotation_direction, locations=None, rotation=None):

        save_rotation = False
        if locations is None:
            locations = self.locations
        if rotation is None:
            save_rotation = True
            rotation = self.rotation

        new_rotation = rotation

        if self.piece_type == PieceType.O:  # for the meme
            pass
        elif self.piece_type == PieceType.I or self.piece_type == PieceType.S or self.piece_type == PieceType.Z:  # the two-rotation-position pieces
            turn = None
            pivot = None
            if self.piece_type == PieceType.I:
                pivot = locations[2]
                if rotation in [0, 180]:
                    turn = Turn.CW  # turn to vertical
                else:
                    turn = Turn.CCW  # turn to horizontal
            elif self.piece_type == PieceType.S:
                pivot = copy(locations[0])
                if rotation in [0, 180]:
                    turn = Turn.CCW  # turn to vertical
                else:
                    turn = Turn.CW  # turn to horizontal
            elif self.piece_type == PieceType.Z:
                pivot = copy(locations[1])
                if rotation in [0, 180]:
                    turn = Turn.CCW  # turn to vertical
                else:
                    turn = Turn.CW  # turn to horizontal
            if turn == Turn.CW:
                # General rotate CW:
                for i, location in enumerate(locations):
                    locations[i] = ((pivot[1] - location[1]) + pivot[0], (location[0] - pivot[0]) + pivot[1])
                new_rotation = (rotation + 90) % 360
            elif turn == Turn.CCW:
                # General rotate CCW:
                for i, location in enumerate(locations):
                    locations[i] = ((location[1] - pivot[1]) + pivot[0], (pivot[0] - location[0]) + pivot[1])
                new_rotation = (rotation - 90) % 360
        elif self.piece_type == PieceType.T or self.piece_type == PieceType.L or self.piece_type == PieceType.J:  # the four-rotation-position pieces
            pivot = copy(locations[1])
            if rotation_direction == Rotation.CW:
                # General rotate CW:
                for i, location in enumerate(locations):
                    locations[i] = ((pivot[1] - location[1]) + pivot[0], (location[0] - pivot[0]) + pivot[1])
                new_rotation = (rotation + 90) % 360
            elif rotation_direction == Rotation.CCW:
                # General rotate CCW:
                for i, location in enumerate(locations):
                    locations[i] = ((location[1] - pivot[1]) + pivot[0], (pivot[0] - location[0]) + pivot[1])
                new_rotation = (rotation - 90) % 360

        if save_rotation:
            self.rotation = new_rotation

    def can_rotate(self, board, players, rotation_direction):

        test_locations = copy(self.locations)
        test_rotation = copy(self.rotation)

        self.rotate(rotation_direction, test_locations, test_rotation)

        for location in test_locations:
            if location[1] >= len(board) or location[0] < 0 or location[0] >= len(board[0]):
                return False
            if board[location[1]][location[0]].tile_type != TileType.BLANK:
                return False

            for player in players:
                if player.active_piece is not None:
                    if player.active_piece.player_number != self.player_number:
                        for other_location in player.active_piece.locations:
                            if other_location == location:
                                return False

        return True
