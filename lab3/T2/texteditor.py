import tkinter as tk


class TextEditorModel:
    def __init__(self, lines_string: str):
        self.lines = lines_string.split("\n")
        self.selection_range = list()
        self.cursor_location = list()


class TextEditor(tk.Frame):
    def __init__(self, text_editor_model: TextEditorModel):
        self.text_editor_model = text_editor_model


def main():
    pass


if __name__ == "__main__":
    main()