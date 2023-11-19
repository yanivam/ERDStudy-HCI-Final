import tkinter as tk
import os

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
    def __init__(self, trial, weeks_until_inventory_runs_out, cost_per_week, manufacturer, visual_UI, dir_name):

        self.week = 0
        self.dir_name = dir_name
        self.visual_exp = visual_UI
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

        self.erd_button = tk.Button(self.left_frame, text="ERD View") # command=print("hello 1")
        self.erd_button.grid(row=0, column=0, padx=20, pady=50)

        self.historical_button = tk.Button(self.left_frame, text="Historical Graph") #command=print("hello 1")
        self.historical_button.grid(row=1, column=0, padx=20, pady=50)

        self.money_button = tk.Button(self.left_frame, text="Money Spent") #command=print("hello 3)
        self.money_button.grid(row=2, column=0, padx=20, pady=50)

        self.erd_label = tk.Label(self.top_frame, text=f"Estimated Resupply Date: {self.current_ERD}")
        self.erd_label.pack()

        self.week_label = tk.Label(self.top_frame, text=f"Week: {self.week + 1}")
        self.week_label.pack()
        
        self.switched = False

        self.data_file = open(self.dir_name + "Trial #" + str(self.trial + 1) + " data.txt", 'w')
        self.data_file.write("Trial #" + str(self.trial + 1) + ":")

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
        
        # The non visual UI setup
        if not self.visual_exp:

            # Print the trial number
            print ("--------------------------START TRIAL #" + str(self.trial + 1) + "----------------------------------")

            while self.week <= 5:    
                # if the week Im in is valid AND the ERD came to be, return it.
                if self.week+1 == self.manufacturer.get_sequence()[self.trial][self.week] and self.week+1 <= 6:
                    self.data_file.write("\n - Week #" + str(self.week+1) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week]) + ", user action: " + str('STAYED'))
                    self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(self.cost_per_week[self.week-1]))
                    self.data_file.close()
                    return 0, self.week 
                if self.manufacturer.get_sequence()[self.trial][self.week] > 6 and self.week+1 == 6:
                    self.data_file.write("\n - Week #" + str(self.week+1) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week]) + ", user action: " + str('STAYED'))
                    self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(self.cost_per_week[self.week-1]))
                    self.data_file.close()
                    print("\nYour inventory ran out, your penalty is 100000")
                    print ("\n-------------------------END TRIAL #" + str(self.trial + 1) + "-----------------------------------")
                    return 100000, self.week 
                else:
                    # Ask the user whether they want to switch or stay
                    print ("------------------------------------------------------------------------")
                    print("- Week " + str(self.week + 1) + ": Your MN's ERD is for week " + str(self.manufacturer.get_sequence()[self.trial][self.week]))
                    action_time = input("Do you want to wait (W) or switch (S)? The cost for switching is " + str(self.cost_per_week[self.week])  + " \nMark either (W/S): ")
                    print(" ")

                    # If you switch, end the trial
                    if action_time == "S":
                        self.switched = True
                        self.data_file.write("\n - Week #" + str(self.week+1) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week]) + ", user action: " + str('SWITCHED'))
                        self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(self.cost_per_week[self.week-1]))
                        self.data_file.close()
                        print ("---------------------------END TRIAL " + str(self.trial + 1) + "----------------------------------")
                        return self.cost_per_week[self.week], self.week
                    # update the week info
                    else:
                        self.data_file.write("\n - Week #" + str(self.week+1) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week]) + ", user action: " + str('STAYED'))
                        self.week += 1
                
                # elif self.week+1 == self.manufacturer.get_sequence()[self.trial][self.week] and self.week+1 <= 6:
                #     return 0, self.week 
            self.data_file.write("\n - Week #" + str(self.week+1) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week-1]) + ", user action: " + str('STAYED'))
            self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(self.cost_per_week[self.week-1]))
            self.data_file.close()
            print ("------------------------------------------------------------------------")
            print("\nYour inventory ran out, your penalty is 100000")
            print ("\n-------------------------END TRIAL #" + str(self.trial + 1) + "-----------------------------------")
            return self.cost_per_week[self.week-1], self.week-1
        else:
            show_erd_view()
        

class Study():
    def __init__(self, num_trials):
        self.num_trials = num_trials

    def run_experiment(self):

        user = input("\nHello! Add a username for to recognize you for the study!: ")

        while (True):
            if not os.path.exists("experiment_" + user + str('/')):
                os.mkdir("experiment_" + user + str('/'))
                print("\nThank you!")
                break
            else:
                user = input("\nName taken, add another username for to recognize you for the study!: ")

        hc_budget = 700000

        for file_nums in range(7):
            if os.path.exists("experiment_" + user + str('/') + "Trial #" + str(file_nums+1) + " data.txt"):
                os.remove("experiment_" + user + str('/') + "Trial #" + str(file_nums+1) + " data.txt")
            else:
                continue

        cost_overall = 0
        user_data_file = open("experiment_" + user + str('/') + "Trial Summary" + " data.txt", 'w')
        visual_UI = False
        for i in range(self.num_trials):
            trial = Trial(i, 6, [37500, 40000,45000,55000,70000,100000], "ACC", visual_UI, "experiment_" + user + str('/'))
            cost_incurred, week = trial.run_trial()
            cost_overall += cost_incurred
            print("\nTrial " + str(i+1) + " ended on week " +  str(week+1) + " and the cost incurred was $" + str(cost_incurred))
            hc_budget -= cost_incurred
            user_data_file.write("\nTrial #" + str(i + 1) + " cost: " + str(cost_incurred))
            print("The remaining budget after Trial #" + str(i+1) + " is " + str(hc_budget) + "\n \n")
            
        user_data_file.write("\nFinal tally cost: " + str(cost_overall))
        user_data_file.write("\nRemaining budget: " + str(hc_budget))
        user_data_file.close()
        print("Thank you", user, "for participating! \n ")

# set to 7
trial_total = 7
study = Study(trial_total)
study.run_experiment()