import tkinter as tk


class Location:
    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column


class LocationRange:
    def __init__(self, start: Location, end: Location):
        self.start = start
        self.end = end


class TextEditorModel:
    def __init__(self, lines_string: str):
        self.lines = lines_string.split("\n")
        self.selection_range = Location(0, 0)
        self.cursor_location = Location(0, 0)


class TextEditor(tk.Tk):
    def __init__(self, text_editor_model: TextEditorModel):
        super().__init__()
        self.canvas = tk.Canvas()
        self.text_editor_model = text_editor_model
        self.canvas.create_text(text="Test")


def main():
    model = TextEditorModel("test\ntest\ntest")
    editor = TextEditor(model)
    editor.mainloop()


if __name__ == "__main__":
    main()
