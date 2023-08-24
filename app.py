import customtkinter as ctk 
import darkdetect
from settings import *
from output_label import OutputLabel
from buttons import Button, NumButton, MathButton

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color = (BLACK, WHITE))
        
        ctk.set_appearance_mode(f"dark" if is_dark else "light")
        
        self.title("Calculator app")
        self.geometry(f"{APP_SIZE[0]}x{APP_SIZE[1]}")
        self.resizable(False, False)

        # grid layout
        self.rowconfigure(list(range(MAIN_ROWS)), weight = 1, uniform = "a")
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight = 1, uniform = "a")
       
        # data 
        self.result_string = ctk.StringVar(value = "0")
        self.formula_string = ctk.StringVar(value = "")
        self.display_nums = []
        self.full_operations = []

        # widgets 
        self.create_widgets()

        # run
        self.mainloop()

    def create_widgets(self):
        # font 
        main_font = ctk.CTkFont(family = FONT, size = NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family = FONT, size = OUTPUT_FONT_SIZE)
        
        OutputLabel(self, 0, "SE", main_font, self.formula_string)
        OutputLabel(self, 1, "E", result_font, self.result_string)
        
        # clear (AC) button
        Button(parent = self, 
               text = OPERATORS["clear"]["text"],
               func = self.clear,
               col = OPERATORS["clear"]["col"],
               row = OPERATORS["clear"]["row"], 
               font = main_font, 
               color = "dark-gray")

        # precentage button
        Button(parent = self, 
               text = OPERATORS["percent"]["text"],
               func = self.percent,
               col = OPERATORS["percent"]["col"],
               row = OPERATORS["percent"]["row"], 
               font = main_font, 
               color = "dark-gray")
        
        # invert button
        Button(parent = self, 
               text = OPERATORS["invert"]["text"],
               func = self.invert,
               col = OPERATORS["invert"]["col"],
               row = OPERATORS["invert"]["row"], 
               font = main_font, 
               color = "dark-gray")
        
        # number buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(parent= self,
                      text =num, 
                      func = self.num_press,
                      col = data["col"], 
                      row = data["row"],
                      span = data["span"],
                      font = main_font)
        
        # operators buttons
        for operator, data in MATH_POSITIONS.items():
            MathButton(parent= self,
                      text = data["character"],
                      operator = operator,
                      func = self.math_press,
                      col = data["col"], 
                      row = data["row"],
                      font = main_font)



    def num_press(self, value):
        self.display_nums.append(str(value))
        full_number = "".join(self.display_nums)
        self.result_string.set(full_number)

    def math_press(self, value):
        current_number = "".join(self.display_nums)

        if current_number:
            self.full_operations.append(current_number)
            
            if value != "=":
                # udapte data
                self.full_operations.append(value)
                self.display_nums.clear()
               
                # update output
                self.result_string.set("")
                self.formula_string.set(" ".join(self.full_operations))
            else:
                formula = " ".join(self.full_operations)
                result = eval(formula)
                
                # format the result 
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 3)

                # udapte data
                self.full_operations.clear()
                self.display_nums = [str(result)]

                # update output
                self.result_string.set(result)
                self.formula_string.set(" ".join(self.full_operations))


    def clear(self):
        # Clear the output
        self.result_string.set(0)
        self.formula_string.set("")

        # clear the data 
        self.display_nums.clear()
        self.full_operations.clear()

    def percent(self):
        if self.display_nums:
            # get the percent number 
            current_number = float("".join(self.display_nums))
            percent_number = current_number/ 100

            # update the data and output 
            self.display_nums = list(str(percent_number))
            self.result_string.set("".join(self.display_nums))
    
    def invert(self):
        current_number = "".join(self.display_nums)

        if current_number:
            if float(current_number) > 0:
                self.display_nums.insert(0, "-")
            else:
                del self.display_nums[0]
        
        self.result_string.set("".join(self.display_nums))

if __name__ == "__main__":
    Calculator(darkdetect.isDark())
