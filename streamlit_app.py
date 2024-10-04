import streamlit as st
import random

HANGMANPICS = [r'''
  +---+
  |   |
      |
      |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
      |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''',
r'''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

# Word bank of animals
words = ('ant baboon badger bat bear beaver camel cat clam cobra cougar '
         'coyote crow deer dog donkey duck eagle ferret fox frog goat '
         'goose hawk lion lizard llama mole monkey moose mouse mule newt '
         'otter owl panda parrot pigeon python rabbit ram rat raven '
         'rhino salmon seal shark sheep skunk sloth snake spider '
         'stork swan tiger toad trout turkey turtle weasel whale wolf '
         'wombat zebra ').split()

# Set up session state to store game state
if 'curr_word' not in st.session_state:
    st.session_state.curr_word = random.choice(words)
    st.session_state.guess_list = ["_"] * len(st.session_state.curr_word)
    st.session_state.man = 0
    st.session_state.guessed_letters = []
    st.session_state.game_over = False
    st.session_state.message = ""  # Store only the latest message

st.title('Hangman Game by Swayam')
st.write('Guess the word!')

# Display the current state of the word
st.write(f"Word to guess: {' '.join(st.session_state.guess_list)}")

# Display the current hangman picture using st.code for better formatting
st.code(HANGMANPICS[st.session_state.man])

# Use a form to handle both the submit button and Enter key for guessing
with st.form(key='guess_form'):
    guess = st.text_input("Guess a letter", max_chars=1)
    submit_button = st.form_submit_button("Submit Guess")

# Game logic
if submit_button and not st.session_state.game_over:
    if guess and guess.isalpha() and len(guess) == 1:
        guess = guess.lower()
        if guess in st.session_state.guessed_letters:
            st.session_state.message = f"You already guessed '{guess}'. Try a different letter."
        else:
            st.session_state.guessed_letters.append(guess)
            if guess in st.session_state.curr_word:
                for i, letter in enumerate(st.session_state.curr_word):
                    if letter == guess:
                        st.session_state.guess_list[i] = letter
                st.session_state.message = f"Good guess! {guess} is in the word."
            else:
                st.session_state.man += 1
                st.session_state.message = f"Wrong guess! {guess} is not in the word."
    
    # Force a re-render to immediately show updated state
    st.rerun()

# Check if the player has won or lost
if "_" not in st.session_state.guess_list:
    st.session_state.message = f"Congratulations! You've guessed the word: {''.join(st.session_state.guess_list)}"
    st.session_state.game_over = True
elif st.session_state.man >= len(HANGMANPICS) - 1:
    st.session_state.message = f"You've run out of lives! The word was: {st.session_state.curr_word}"
    st.session_state.game_over = True

# Display only the latest message
if st.session_state.message:
    if "Congratulations" in st.session_state.message or "You've run out of lives" in st.session_state.message:
        st.success(st.session_state.message)
    elif "Good guess" in st.session_state.message:  # Show "Good guess" message in green
        st.success(st.session_state.message)
    elif "Wrong guess" in st.session_state.message:  # Show wrong guess in red
        st.error(st.session_state.message)
    else:
        st.warning(st.session_state.message)

# Reset the game
if st.session_state.game_over:
    if st.button("Play Again"):
        # Reset the session state for a new game
        st.session_state.curr_word = random.choice(words)
        st.session_state.guess_list = ["_"] * len(st.session_state.curr_word)
        st.session_state.man = 0
        st.session_state.guessed_letters = []
        st.session_state.message = ""  # Reset message
        st.session_state.game_over = False
        st.rerun()
