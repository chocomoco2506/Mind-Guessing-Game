import csv
import random
import json

# Load translations from JSON file
def load_translations(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        return json.load(file)

# Translate text using the loaded translations
def translate(text, translations):
    return translations.get(text, text)  # Return translated text or original if not found

# Load dataset from CSV
def load_dataset(filename):
    animals = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            animals.append(row)
    return animals

# Ask a yes/no question (translated)
def ask_question(column, value, translations):
    question = f"Is the animal {column} {value}?"
    translated_question = translate(question, translations)
    user_input = input(f"{translated_question} ({translate('yes', translations)}/{translate('no', translations)}): ").strip().lower()
    return user_input == translate("yes", translations)

# Markov Chain-based model
def markov_chain_guess(animals, columns, translations):
    remaining_animals = animals.copy()
    asked_values = {column: set() for column in columns}

    # First, ask about class, size, or habitat
    first_columns = ["class", "size", "habitat"]
    while first_columns and len(remaining_animals) > 1:
        column = random.choice(first_columns)
        first_columns.remove(column)

        unique_values = list(set(animal[column] for animal in remaining_animals if animal[column] and animal[column].strip()))
        
        if not unique_values:
            continue
        
        value = random.choice(unique_values)
        
        if ask_question(column, value, translations):
            remaining_animals = [animal for animal in remaining_animals if animal[column] == value]
        else:
            remaining_animals = [animal for animal in remaining_animals if animal[column] != value]
        
        asked_values[column].add(value)

        if len(set(animal[column] for animal in remaining_animals)) == 1:
            columns.remove(column)

    # Now, ask other columns
    while len(remaining_animals) > 1:
        if not columns:
            print(translate("I cannot guess the animal with the given information.", translations))
            return remaining_animals

        column = random.choice(columns)
        
        unique_values = list(set(animal[column] for animal in remaining_animals if animal[column] and animal[column].strip()))
        
        if not unique_values:
            columns.remove(column)
            continue
        
        value = random.choice(unique_values)
        
        if ask_question(column, value, translations):
            remaining_animals = [animal for animal in remaining_animals if animal[column] == value]
        else:
            remaining_animals = [animal for animal in remaining_animals if animal[column] != value]
        
        asked_values[column].add(value)

        if len(set(animal[column] for animal in remaining_animals)) == 1:
            columns.remove(column)

    return remaining_animals

# Main function
def main():
    # Load translations
    translations = load_translations("translations.json")
    
    # Print welcome message (translated)
    print(translate("Think of an animal, and I will try to guess what it is!", translations))
    
    # Load dataset
    animals = load_dataset("animals.csv")
    
    # List of columns to ask about
    columns = ["class", "size", "color", "body covering", "legs", "tail", "habitat", "fly", "venomous", "diet", "pet", "social behaviour", "speed"]

    # Use Markov Chain-based model to narrow down animals
    remaining_animals = markov_chain_guess(animals, columns, translations)

    # Guess the animal
    if len(remaining_animals) == 1:
        animal = remaining_animals[0]
        animal_name = animal['animal name']
        translated_animal_name = translate(animal_name, translations)  # Translate animal name
        print(translate("I guess the animal is", translations) + f": {translated_animal_name}!")
        print(f"{translate('Class', translations)}: {translate(animal['class'], translations)}")
        print(f"{translate('Habitat', translations)}: {translate(animal['habitat'], translations)}")
        print(f"{translate('Diet', translations)}: {translate(animal['diet'], translations)}")
    elif len(remaining_animals) > 1:
        print(translate("Possible animals", translations) + ":")
        for animal in remaining_animals:
            animal_name = animal['animal name']
            translated_animal_name = translate(animal_name, translations)  # Translate animal name
            print(f"- {translated_animal_name}")
    else:
        print(translate("I couldn't guess the animal. Maybe it's not in my dataset.", translations))

# Run the program
if __name__ == "__main__":
    main()