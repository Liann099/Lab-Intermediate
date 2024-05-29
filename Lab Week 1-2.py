import random

def choose_word():
    return random.choice(["MEMORY"]).strip().lower()

def main():
    while True:
        secret_word = choose_word()
        guessed_letters = set()
        attempts = 6

        name = input("What is your name? ")

        print ("Hello, " + name, "Time to play hangman!")

        print(f"The secret word has {len(secret_word)} letters.")
        print(f"Clue: The secret word are computer related things.")

        while attempts > 0:
            print("\nAttempts left:", attempts)
            print("Word:", ''.join([letter if letter in guessed_letters else '_' for letter in secret_word]))

            guess = input("Enter a letter: ").strip().lower()

            if not guess.isalpha() or len(guess) != 1:
                print("Invalid input. Please enter a single letter.")
                continue

            if guess in guessed_letters:
                print("You already guessed that letter.")
                continue

            guessed_letters.add(guess)

            if guess not in secret_word:
                print("Oops! That letter is not in the word.")
                attempts -= 1

            if set(secret_word) == guessed_letters:
                print("Congratulations! You guessed the word:", secret_word)
                break

        if attempts == 0:
            print("Sorry, you ran out of attempts. The word was:", secret_word)

        if input("Do you want to play again? (yes/no): ").strip().lower() != "yes":
            break
        print("test")

if __name__ == "__main__":
    main()
