import tkinter as tk
from tkinter import ttk


SUPPLIES = (400, 540, 120, 9, 550)


class MyButton(ttk.Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def pack(self, **kwargs):
        super().pack(padx=2, pady=5, fill=tk.BOTH)


class Entry_digits(ttk.Entry):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        master = kwargs.get("master")

        text_check = master.register(self.__is_valid_input)
        self.configure(validate="key", validatecommand=(text_check, "%P"))

    def __is_valid_input(self, text):
        if text.isnumeric():
            return True
        return False

class Main_run(tk.Tk):
    def __init__(self, supplies, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Coffee Machine")

        self.main_frame = ttk.Frame(master=self)
        self.left_pan = ttk.Frame(master=self.main_frame)
        self.right_pan = ttk.Frame(master=self.main_frame)
        self.bottom_pan = ttk.Frame(master=self.main_frame)
        self.main_frame.pack()
        self.left_pan.grid(row=0, column=0)
        self.right_pan.grid(row=0, column=1)
        self.bottom_pan.grid(row=1, column=0, columnspan=2)

        self.btn_buy = MyButton(master=self.left_pan, text="Buy a Coffee", command=self.__buy)
        self.btn_fill = MyButton(master=self.left_pan, text="Add Supplies", command=self.__fill)
        self.btn_take = MyButton(master=self.left_pan, text="Take Cash", command=self.__take)
        self.btn_remaining = MyButton(master=self.left_pan, text="Remaining Supplies", command=self.__remaining)

        self.btn_buy.pack()
        self.btn_fill.pack()
        self.btn_take.pack()
        self.btn_remaining.pack()

        self.btn_quit = MyButton(master=self.left_pan, text="Quit", command=self.destroy)
        self.btn_quit.pack()

        self.water, self.milk, self.coffee, self.cups, self.money = supplies

    def __buy(self):
        self.__clear()

        self.buy_pan = ttk.Frame(master=self.right_pan)
        self.buy_pan.pack()
        self.lbl_buy = ttk.Label(master=self.buy_pan, text="What do you want to buy?")
        self.lbl_buy.pack()

        self.coffee_types = {
            "Espresso": {"water": 250, "coffee": 16, "cost": 4},
            "Latte": {"water": 350, "milk": 75, "coffee": 20, "cost": 7},
            "Cappuccino": {"water": 200, "milk": 100, "coffee": 12, "cost": 6},
        }

        for coffee in self.coffee_types:
            MyButton(master=self.buy_pan, text=coffee, command=lambda x=coffee: self.__make_coffee(x)).pack()

        MyButton(master=self.buy_pan, text="Go Back", command=self.buy_pan.destroy).pack()

    def __make_coffee(self, coffee):
        needed_supplies = self.coffee_types.get(coffee)
        lack_resources = self.__check_supplies(needed_supplies)

        if lack_resources:
            for child in self.bottom_pan.winfo_children():
                child.destroy()
            ttk.Label(master=self.bottom_pan, text=f"Sorry, not enough {', '.join(lack_resources)}!").pack()
        else:
            for child in self.bottom_pan.winfo_children():
                child.destroy()
            ttk.Label(master=self.bottom_pan, text=f"You choose {coffee}. I have enough resources, making you a coffee!").pack()

            self.water -= needed_supplies.get("water", 0)
            self.milk -= needed_supplies.get("milk", 0)
            self.coffee -= needed_supplies.get("coffee", 0)
            self.cups -= 1
            self.money += needed_supplies.get("cost", 0)

    def __check_supplies(self, needed_supplies):

        available_supplies = [("water", self.water - needed_supplies.get("water")),
                                ("milk", self.milk - needed_supplies.get("milk", 0)),
                                ("coffee beans", self.coffee - needed_supplies.get("coffee")),
                                ("cups", self.cups - 1)]

        lack_resources = [i[0] for i in available_supplies if i[1] < 0]

        return lack_resources

    def __fill(self):
        self.__clear()

        self.fill_pan = ttk.Frame(master=self.right_pan)
        self.fill_pan.pack()

        self.fill_pan.columnconfigure(0)
        self.fill_pan.columnconfigure(1)

        for x in range(6):
            self.fill_pan.rowconfigure(x)

        self.lbl_title = ttk.Label(master=self.fill_pan, text="Supplies to add:")
        self.lbl_title.grid(row=0, column=0, columnspan=2)

        self.lbl_water = ttk.Label(master=self.fill_pan, text="Water:")
        self.lbl_water.grid(row=1, column=0)
        self.lbl_milk = ttk.Label(master=self.fill_pan, text="Milk:")
        self.lbl_milk.grid(row=2, column=0)
        self.lbl_coffee = ttk.Label(master=self.fill_pan, text="Coffee:")
        self.lbl_coffee.grid(row=3, column=0)
        self.lbl_cups = ttk.Label(master=self.fill_pan, text="Cups:")
        self.lbl_cups.grid(row=4, column=0)

        self.ent_water = Entry_digits(master=self.fill_pan)
        self.ent_water.grid(row=1, column=1)
        self.ent_milk = Entry_digits(master=self.fill_pan)
        self.ent_milk.grid(row=2, column=1)
        self.ent_coffee = Entry_digits(master=self.fill_pan)
        self.ent_coffee.grid(row=3, column=1)
        self.ent_cups = Entry_digits(master=self.fill_pan)
        self.ent_cups.grid(row=4, column=1)

        self.btn_submit = MyButton(master=self.fill_pan, text="Submit", command=self.__fill_it)
        self.btn_submit.grid(row=5, column=0, columnspan=2)

    def __fill_it(self):

        self.water += int(self.ent_water.get()) if self.ent_water.get() else 0
        self.milk += int(self.ent_milk.get()) if self.ent_milk.get() else 0
        self.coffee += int(self.ent_coffee.get()) if self.ent_coffee.get() else 0
        self.cups += int(self.ent_cups.get()) if self.ent_cups.get() else 0

        self.__clear()

    def __remaining(self):
        self.__clear()

        ttk.Label(master=self.right_pan, text="The coffee machine has:").pack()
        ttk.Label(master=self.right_pan, text=f"{self.water} ml of water").pack()
        ttk.Label(master=self.right_pan, text=f"{self.milk} ml of milk").pack()
        ttk.Label(master=self.right_pan, text=f"{self.coffee} g of coffee beans").pack()
        ttk.Label(master=self.right_pan, text=f"{self.cups} disposable cups").pack()
        ttk.Label(master=self.right_pan, text=f"${self.money} of money").pack()

    def __take(self):
        self.__clear()

        ttk.Label(master=self.bottom_pan, text=f"I gave you {self.money} $").pack()
        self.money = 0

    def __clear(self):
        for child in self.right_pan.winfo_children():
            child.destroy()

        for child in self.bottom_pan.winfo_children():
            child.destroy()


if __name__ == "__main__":
    app = Main_run(SUPPLIES)
    app.mainloop()
