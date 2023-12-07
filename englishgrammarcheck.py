import spacy
from textblob import TextBlob
import tkinter as tk
from tkinter import ttk

# Load spaCy and the English language model
nlp = spacy.load("en_core_web_sm")

def analyze_and_correct_sentence():
    sentence = sentence_entry.get()

    # Process the input sentence with spaCy
    doc = nlp(sentence)

    # Check for punctuation errors
    punctuation_errors = [token.text for token in doc if token.is_punct]

    # Detect the tense and voice (active or passive)
    tense = None
    voice = None
    for token in doc:
        if token.dep_ in ("aux", "auxpass"):
            if token.text.lower() == "will":
                tense = "future"
            elif token.text.lower() == "was" or token.text.lower() == "were":
                tense = "past"
            elif token.text.lower() == "am" or token.text.lower() == "is" or token.text.lower() == "are":
                tense = "present"
        if token.dep_ == "auxpass":
            voice = "passive"
        if token.dep_ == "nsubj":
            voice = "active"

    # Check for vocabulary and spelling suggestions using TextBlob
    blob = TextBlob(sentence)

    # Correct spelling and grammar, but not punctuation
    corrected_sentence_blob = blob.correct()
    corrected_sentence = str(corrected_sentence_blob)

    # Capitalize the first letter of the corrected sentence
    if len(corrected_sentence) > 0:
        corrected_sentence = corrected_sentence[0].upper() + corrected_sentence[1:]

    # Replace punctuation errors
    for error in punctuation_errors:
        corrected_sentence = corrected_sentence.replace(error, '')

    # Display the results in the GUI
    original_sentence_label.config(text=f"Original Sentence: {sentence}")
    punctuation_errors_label.config(text=f"Punctuation Errors: {', '.join(punctuation_errors)}")
    tense_label.config(text=f"Tense: {tense}")
    voice_label.config(text=f"Voice: {voice}")
    corrected_sentence_label.config(text=f"Corrected Sentence: {corrected_sentence}")

# Create the GUI window
window = tk.Tk()
window.title("Sentence Analysis Tool")

# Create and configure GUI elements
sentence_label = ttk.Label(window, text="Enter a sentence:")
sentence_entry = ttk.Entry(window, width=40)
analyze_button = ttk.Button(window, text="Analyze and Correct", command=analyze_and_correct_sentence)
original_sentence_label = ttk.Label(window, text="")
punctuation_errors_label = ttk.Label(window, text="")
tense_label = ttk.Label(window, text="")
voice_label = ttk.Label(window, text="")
corrected_sentence_label = ttk.Label(window, text="")

# Arrange GUI elements in a grid layout
sentence_label.grid(row=0, column=0, padx=10, pady=10)
sentence_entry.grid(row=0, column=1, padx=10, pady=10)
analyze_button.grid(row=0, column=2, padx=10, pady=10)
original_sentence_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
punctuation_errors_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
tense_label.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
voice_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5)
corrected_sentence_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

# Start the GUI main loop
window.mainloop()
