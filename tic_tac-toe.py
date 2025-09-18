import os

def clear_screen():
    # nt for windows and clear for linux pased systems
    os.system("cls" if os.name == "nt" else "clear")
class Player:
    def __init__(self) :
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True:
            name = input("Enter your  name (letters only): ")
            if name.isalpha():
                self.name = name
                break
            print("Invalid Entry name. Please use letters only.")
            
    def choose_symbol(self):
        while True:
            symbol = input(f"{self.name.capitalize()}, choose your symbol (a single letter):")
            if symbol.isalpha() and len(symbol) == 1:
                self.symbol = symbol
                break
            print("Invalid symbol. Please choose single letter.")

class Menu:

    def validate_choice(self,choice):
        while True:
            if choice == "1" or choice == "2":
                return choice
            else:
                print("Invalid Entry (it should be 1 or 2)")    
                choice = input("Enter a valid choice (1 or 2): ").strip()

    def display_main_menu(self):
        menu_text = """
        Welcom to my X-O game!
        1 Start Game
        2 Quit Game
        Enter your choice (1 or 2)
        """
        choice = input(menu_text).strip()
        return self.validate_choice(choice)

    def display_endgame_menu(self):
        menu_text = """
        Game Over!
        1 Restart Game
        2 Quit Game
        Enter your choice (1 or 2): 
        """
        choice = input(menu_text).strip()
        return self.validate_choice(choice)
        

class Board:

    def __init__(self) -> None:
        self.board = [str(i) for i in range(1,10)]    
    
    def display_board(self):
        for i in range(0,9,3):
            
            print("|".join(self.board[i:i+3])) # slicing 3 elements per row at a time
            if i < 6:  # Print a separator after each row except the last one
                print("-"*5)
    
    def update_board(self, choice, symbol):
        if self.is_valid_move(choice):
            self.board[choice - 1] = symbol  # Place the player's symbol
            return True
        return False
    
    # solid principles: single responsibility principle
    def is_valid_move(self,choice):
        return self.board[choice-1].isdigit()    
    
    def reset_board(self):
        self.board = [str(i) for i in range(1,10)]   

class Game:

    def __init__(self):
        self.board = Board()
        self.players = [Player(), Player()]
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.display_main_menu()
        if choice == "1":
            self.setup_players()
            self.play_game()   
        else:
            self.quit_game()    

    def setup_players(self):
        for player_number, player in enumerate(self.players,1):
            print(f"Player{player_number} enter your details: ")
            player.choose_name()
            player.choose_symbol()
            print("-" * 40)
            clear_screen()
   
    def play_game(self):
        while True:
            self.play_turn()
            
            if self.check_win():
                print(f"{self.players[1 - self.current_player_index].name} wins!")
                break
            elif self.check_draw():
                print("It's a draw!")
                break   
        choice = self.menu.display_endgame_menu() 
        if choice == "1":       
            self.restart_geme()    
        else:
            self.quit_game()
                     
    def restart_geme(self):
        self.board.reset_board() 
        self.current_player_index = 0
        self.play_game()                      

    def check_win(self):
        winning_combinations =[
        [0,1,2],[3,4,5],[6,7,8], # rows
        [0,3,6],[1,4,7],[2,5,8], # columns
        [0,4,8],[2,4,6]          #diagonals 
        ]
        for combo in winning_combinations:
            if self.board.board[combo[0]] == self.board.board[combo[1]] == self.board.board[combo[2]]:
                return True
        return False

    def check_draw(self):
        # tuple generator works on the fly
        return all(not cell.isdigit() for cell in self.board.board)

    def play_turn(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print(f"{player.name}'s turn ({player.symbol})")
        while True:
            try:
                cell_choice = int(input("Choose cell (1-9): "))
                if 1<= cell_choice <= 9 and self.board.update_board(cell_choice, player.symbol):
                    break
                else:
                    print("Invalid move, try again.")
            except ValueError:
                print("Please enter a number between 1 and 9")
        self.switch_player()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def quit_game(self):
        print("Thank you for playing!")      

game = Game()
game.start_game()            