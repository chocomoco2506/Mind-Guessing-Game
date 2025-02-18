import csv
import random

# Load dataset from CSV
def load_dataset(filename):
    characters = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            characters.append(row)
    return characters

# Ask a yes/no question
def ask_question(column, value):
    return input(f"Is the character {column} {value}? (yes/no): ").strip().lower() == "yes"

# Markov Chain-based model
def markov_chain_guess(characters, columns):
    # Initial state: all characters are possible
    remaining_characters = characters.copy()
    asked_values = {column: set() for column in columns}  # Track asked values for each column

    # First, ask about gender, type, or nationality
    first_columns = ["Gender", "Type", "Nationality"]
    while first_columns and len(remaining_characters) > 1:
        column = random.choice(first_columns)
        first_columns.remove(column)

        # Get unique values for the selected column from remaining characters
        unique_values = list(set(character[column] for character in remaining_characters if character[column] and character[column].strip()))
        
        if not unique_values:
            continue  # Skip if no unique values
        
        # Randomly select a value to ask about
        value = random.choice(unique_values)
        
        # Ask the user the question
        if ask_question(column, value):
            # Transition to a new state: characters that match the value
            remaining_characters = [character for character in remaining_characters if character[column] == value]
        else:
            # Transition to a new state: characters that do not match the value
            remaining_characters = [character for character in remaining_characters if character[column] != value]
        
        # Add the asked value to the set of asked values for this column
        asked_values[column].add(value)

        # Remove the column from the list of questions if all characters have the same value
        if len(set(character[column] for character in remaining_characters)) == 1:
            columns.remove(column)

    # Now, ask other columns
    while len(remaining_characters) > 1:
        if not columns:
            print("I cannot guess the character with the given information.")
            return remaining_characters

        # Randomly select a column to ask about
        column = random.choice(columns)
        
        # Skip GroupName and GroupPosition for Solo artists 
        if column in ["GroupName", "GroupPosition"]:
            if all(character["Type"] == "Solo" for character in remaining_characters):
                columns.remove(column)
                continue
        
        # Skip Relationship for non-Myanmar characters
        if column == "Relationship":
            if not any(character["Nationality"] == "Myanmar" for character in remaining_characters):
                columns.remove(column)
                continue
        
        # Get unique values for the selected column from remaining characters
        unique_values = list(set(character[column] for character in remaining_characters if character[column] and character[column].strip()))
        
        if not unique_values:
            # No more unique values to ask for this column
            columns.remove(column)
            continue
        
        # Randomly select a value to ask about
        value = random.choice(unique_values)
        
        # Ask the user the question
        if ask_question(column, value):
            # Transition to a new state: characters that match the value
            remaining_characters = [character for character in remaining_characters if character[column] == value]
        else:
            # Transition to a new state: characters that do not match the value
            remaining_characters = [character for character in remaining_characters if character[column] != value]
        
        # Add the asked value to the set of asked values for this column
        asked_values[column].add(value)

        # Remove the column from the list of questions if all characters have the same value
        if len(set(character[column] for character in remaining_characters)) == 1:
            columns.remove(column)

    return remaining_characters

# Main function
def main():
    print("Think of a character, and I will try to guess who it is!")
    
    # Load dataset
    characters = load_dataset("singers.csv")
    
    # List of columns to ask about
    columns = ["Type", "Nationality", "Gender", "Award", "Age", "MusicGenre", "GroupName", "GroupPosition", "PopularSong", "Relationship"]

    # Use Markov Chain-based model to narrow down characters
    remaining_characters = markov_chain_guess(characters, columns)

    # Guess the character
    if len(remaining_characters) == 1:
        character = remaining_characters[0]
        print(f"I guess the character is: {character['Name']}!")
        print(f"Award: {character['Award']}")
        print(f"Popular Song: {character['PopularSong']}")
    elif len(remaining_characters) > 1:
        print("Possible characters:")
        for character in remaining_characters:
            print(f"- {character['Name']}")
    else:
        print("I couldn't guess the character. Maybe they're not in my dataset.")

# Run the program
if __name__ == "__main__":
    main()