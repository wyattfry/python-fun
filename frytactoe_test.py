import unittest
import frytactoe as sut

class TestFryTacToe(unittest.TestCase):

    def test_get_free_cell_count(self):
        # Arrange
        board = [[1, 2], [3, 4]]
        expect = board[0][0]

        # Act
        result = sut.get_cell(board, 0, 0)

        # Assert
        self.assertEqual(result, expect)

    def test_set_cell(self):
        # Arrange
        board = [
            ['X', 'X', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']]
        expect = 'O'

        # Act
        sut.set_cell(board, 1, 0, expect, '-')

        # Assert
        self.assertEqual(board[1][0], expect)

    def test_set_cell_settings_played_cell_raises_RuntimeException(self):
        # Arrange
        board = [
            ['X', 'X', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']]

        # Act & Assert
        with self.assertRaises(RuntimeError):
            sut.set_cell(board, 0, 0, 'O', '-')


    def test_get_free_cell_count(self):
        # Arrange
        board = [[1, 2], [3, 4]]
        expect = 5

        # Act
        sut.set_cell(board, 0, 0, expect)

        # Assert
        self.assertEqual(board[0][0], expect)

    def test_get_winning_cell_right_corner(self):
        # Arrange
        board = [
            ['X', 'X', '-'],
            ['-', '-', '-'],
            ['-', '-', '-']]
        expect = (0, 2)

        # Act
        result = sut.get_winning_cell(board, 'X', '-')

        # Assert
        self.assertEqual(result, expect)

    def test_get_winning_cell_middle(self):
        # Arrange
        board = [
            ['X', '-', 'X'],
            ['-', '-', '-'],
            ['-', '-', '-']]
        expect = (0, 1)

        # Act
        result = sut.get_winning_cell(board, 'X', '-')

        # Assert
        self.assertEqual(result, expect)

    def test_get_winning_cell_left_corner(self):
        # Arrange
        board = [
            ['-', 'X', 'X'],
            ['-', '-', '-'],
            ['-', '-', '-']]
        expect = (0, 0)

        # Act
        result = sut.get_winning_cell(board, 'X', '-')

        # Assert
        self.assertEqual(result, expect)

    def test_get_winning_cell_side_middle(self):
        # Arrange
        board = [
            ['X', '-', '-'],
            ['-', '-', '-'],
            ['X', '-', '-']]
        expect = (1, 0)

        # Act
        result = sut.get_winning_cell(board, 'X', '-')

        # Assert
        self.assertEqual(result, expect)

    def test_get_winning_cell_diagonal_NW(self):
        # Arrange
        board = [
            ['X', '-', '-'],
            ['-', '-', '-'],
            ['-', '-', 'X']]
        expect = (1, 1)

        # Act
        result = sut.get_winning_cell(board, 'X', '-')

        # Assert
        self.assertEqual(result, expect)

    def test_get_winning_cell_diagonal_NW_opponent(self):
        # Arrange
        board = [
            ['O', '-', '-'],
            ['X', '-', '-'],
            ['X', '-', 'O']]
        expect = (1, 1)

        # Act
        result = sut.get_winning_cell(board, 'X', '-', for_opponent=True)

        # Assert
        self.assertEqual(result, expect)

    def test_get_winning_cell_diagonal_NE(self):
        # Arrange
        board = [
            ['-', '-', 'X'],
            ['-', '-', '-'],
            ['X', '-', '-']]
        expect = (1, 1)

        # Act
        result = sut.get_winning_cell(board, 'X', '-')

        # Assert
        self.assertEqual(result, expect)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()