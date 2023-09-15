import customtkinter as ctk
from settings import *

class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent, row, anchor, font, string_var):
        super().__init__(master = parent, text = "123", text_color = WHITE, font = font, textvariable = string_var)

        self.grid(column = 0, columnspan = 4, row = row, sticky = anchor, padx = 10)
