import tkinter as tk

class Manufacturer():
    def __init__(self, type):
        self.type = type
        self.sequence = []
        if(type == "ACC"):
            self.sequence.append([5,5,6,6,6,6]) 
            self.sequence.append([4,4,5,5,5])
            self.sequence.append([6,6,6,6,6,6])
            self.sequence.append([6,6,6,7,7,7])
            self.sequence.append([7,7,8,8,8,8])
            self.sequence.append([7,7,7,7,7,7])
            self.sequence.append([5,5,5,6,6,6])
        elif(type == "PB"):
            self.sequence.append([5,5,5,6,6,6]) 
            self.sequence.append([3,4,4,5,5])
            self.sequence.append([4,4,4,5,6,6])
            self.sequence.append([5,5,5,6,7,7])
            self.sequence.append([6,6,6,6,7,8])
            self.sequence.append([6,6,6,6,6,7])
            self.sequence.append([5,5,5,5,6,6])
        else:
             self.sequence.append([5,5,7,7,6,6])
             self.sequence.append([7,7,6,6,5])
             self.sequence.append([5,5,5,6,6,6])
             self.sequence.append([7,7,6,6,7,7])
             self.sequence.append([6,6,7,7,7,8])
             self.sequence.append([4,4,6,6,7,7])
             self.sequence.append([5,5,5,7,7,6])

    def get_sequence(self):
        return self.sequence

class Trial():
    def __init__(self, trial, weeks_until_inventory_runs_out, cost_per_week, manufacturer):
        self.week = 0
        self.trial = trial
        self.weeks_until_inventory_runs_out = weeks_until_inventory_runs_out
        self.cost_per_week = cost_per_week
        self.root = tk.Tk()
        self.root.title("Experiment UI")
        self.manufacturer = Manufacturer(manufacturer)
        self.current_ERD = self.manufacturer.get_sequence()[trial][0]

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.main_frame, width=150, bg="lightgray")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.top_frame = tk.Frame(self.content_frame, height=300, bg="lightblue")
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.content_frame, height=100, bg="lightgreen")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.switch_button = tk.Button(self.bottom_frame, text="Switch", command=self.switch_action)
        self.switch_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.wait_button = tk.Button(self.bottom_frame, text="Wait", command=self.wait_action)
        self.wait_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.erd_button = tk.Button(self.left_frame, text="ERD View", command=print("hello 1"))
        self.erd_button.grid(row=0, column=0, padx=20, pady=50)

        self.historical_button = tk.Button(self.left_frame, text="Historical Graph", command=print("hello 2"))
        self.historical_button.grid(row=1, column=0, padx=20, pady=50)

        self.money_button = tk.Button(self.left_frame, text="Money Spent", command=print("hello 3"))
        self.money_button.grid(row=2, column=0, padx=20, pady=50)

        self.erd_label = tk.Label(self.top_frame, text=f"Estimated Resupply Date: {self.current_ERD}")
        self.erd_label.pack()

        self.week_label = tk.Label(self.top_frame, text=f"Week: {self.week + 1}")
        self.week_label.pack()
        
        self.switched = False

    def update_ERD_display(self):
        self.erd_label.config(text=f"Estimated Resupply Date: {self.current_ERD}")

    def update_week_display(self):
        self.week_label.config(text=f"Week: {self.week + 1}")

    def switch_action(self):
        self.switched = True
        self.root.destroy()

    def wait_action(self):
        self.week += 1
        if self.week >= len(self.manufacturer.get_sequence()[self.trial]):
            self.root.destroy()
        else:
            self.current_ERD = self.manufacturer.get_sequence()[self.trial][self.week]
            self.update_ERD_display()
            self.update_week_display()

    def run_trial(self):
        def create_button(text, command, row, column):
            button = tk.Button(self.root, text=text, command=command)
            button.grid(row=row, column=column, padx=200, pady=100)
        
        def show_erd_view():
            # Replace this function with code to display ERD view
            print("ERD view displayed")

        def show_historical_graph():
            # Replace this function with code to display historical graph
            print("Historical graph displayed")

        def show_money_spent():
            # Replace this function with code to display money spent per trial
            print("Money spent view displayed")


        # Initially, show the ERD view (replace this with your default view)
        show_erd_view()
        self.root.mainloop()
        if self.switched:
            self.switched = False
            return self.cost_per_week[self.week], self.week
        if self.weeks_until_inventory_runs_out >= self.week:
            if self.manufacturer.get_sequence()[self.trial][-1] >= self.week:
                if self.manufacturer.get_sequence()[self.trial][-1] > self.weeks_until_inventory_runs_out:
                    return self.cost_per_week[-1], self.week
                return 0, self.week
            else:
                return self.cost_per_week[self.week], self.week
        else:
            return self.cost_per_week[-1], self.week

class Study():
    def __init__(self, num_trials):
        self.num_trials = num_trials

    def run_experiment(self):
        for i in range(self.num_trials):
            trial = Trial(i, 6, [37500, 40000,45000,55000,70000,100000], "ACC")
            cost_incurred, week = trial.run_trial()
            print("Trial " + str(i) + " ended on week " +  str(week) + " and the cost incurred was $" + str(cost_incurred))

study = Study(7)
study.run_experiment()