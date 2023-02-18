import os
import random
words = {
    "computer": "A machine that performs processes, calculations and operations based on instructions provided",
    "programming": "A set of instructions fed into the computer that performs particular computation",
}


MAX_LIVES = 5


class Game:
    def __init__(self, words):
        self.words = words
        self.current_word = ""
        self.lives = MAX_LIVES
        self.score = 0
        self.used_words = []
        self.user_guesses = set()
        self.current_attempt = 0

    def word_to_list(self, word):
        blanks = [random.randint(0, len(self.current_word)-1)
                  for i in range(len(self.current_word)-1)]
        current_word_list = list(self.current_word.upper())
        for i in blanks:
            current_word_list[i] = "_"
        return current_word_list

    def word_is_used(self, word):
        return word in self.used_words

    def get_word(self):
        word = random.choice(list(self.words.keys()))
        if len(self.used_words) == len(self.words):
            print("No more words left.")
            print(f"Your score is {self.score}")
            print("Game Over.")
            exit(1)
        while self.word_is_used(word):
            word = random.choice(list(self.words.keys()))
        self.used_words.append(word)
        self.current_word = word
        return word

    def get_indices(self, char):
        indices = []
        for (i, c) in enumerate(list(self.current_word)):
            if c == char:
                indices.append(i)
        return indices

    def round_is_over(self, word_list):
        if "_" in word_list:
            return False
        return True

    def introduction(self):
        print("Welcome to hangman")
        name = input("Please enter your name: ")

        os.system("clear")
        print(f"Hello {name}. Pleased to have you in the game.")

    def play_round(self):
        word_list = self.word_to_list(self.get_word())
        word = " ".join(word_list)
        print("Hint:")
        print(self.words[self.current_word])
        print("\n")
        print(word)
        while not self.round_is_over(word_list):
            print(f"Total attempts: {self.current_attempt}")
            print(f"Remaining lives: {self.lives}")
            user_guess = input("Guess a letter: ")
            self.current_attempt += 1
            if user_guess in self.user_guesses:
                print("Youve already guessed this letter")
                self.lives -= 1
            self.user_guesses.add(user_guess.lower())
            if len(user_guess) > 1:
                print("Enter a single letter at a time")
                self.lives -= 1

            indices = self.get_indices(user_guess)
            if len(indices) == 0:
                self.lives -= 1
            for i in indices:
                word_list[i] = user_guess.upper()
            print(" ".join(word_list))

            if self.lives == 0:
                print(f"The word is {self.current_word}")
                print("You lose")
                exit(1)

    def play(self):
        self.introduction()
        choice = "y"
        while choice == "y":
            self.play_round()
            self.user_guesses.clear()
            choice = input(
                "Do you want to play another round? Press y for yes: ")
        print("Goodbye.")


game = Game(words)
game.play()
