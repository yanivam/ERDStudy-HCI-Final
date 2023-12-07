import tkinter as tk
from tkinter import ttk
import os
import matplotlib.pyplot as plt
import PIL
from PIL import Image,ImageTk

def TrialCosts(trial, cost, weeks, path):
  plt.figure()
  plt.bar(weeks, cost, color='red')
  plt.title("Cost per Trial Week (Last Trial Completed: " + str(trial) + ")")
  plt.xlabel("Trial #")
  plt.ylabel("Cost Incurred")
  plt.savefig(path + 'Trial_' + str(trial) + '.jpg')
  return

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
    def __init__(self, trial, weeks_until_inventory_runs_out, cost_per_week, manufacturer, visual_UI, dir_name, cost_ov):

        self.week = 0
        self.cost = cost_ov
        self.dir_name = dir_name
        self.visual_exp = visual_UI
        self.trial = trial
        self.weeks_until_inventory_runs_out = weeks_until_inventory_runs_out
        self.cost_per_week = cost_per_week
        self.manufacturer = Manufacturer(manufacturer)
        self.current_ERD = self.manufacturer.get_sequence()[trial][0]
        self.switched = False
        self.data_file = open(self.dir_name + "Trial #" + str(self.trial + 1) + " data.txt", 'w')
        self.data_file.write("Trial #" + str(self.trial + 1) + ":")
        
        if self.visual_exp:
            self.root = tk.Tk()
            self.root.title("Experiment UI")

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
            
            self.inv_button = tk.Button(self.left_frame, text="Inventory Info", command=self.getTable)
            self.inv_button.grid(row=0, column=0, padx=20, pady=50)

            self.erd_button = tk.Button(self.left_frame, text="ERD View", command= self.updateERD_Weekly)
            self.erd_button.grid(row=1, column=0, padx=20, pady=50)

            self.historical_button = tk.Button(self.left_frame, text="Historical Graph", command=self.updateERD_Hist)
            self.historical_button.grid(row=2, column=0, padx=20, pady=50)
            
            # self.initial = tk.Label(self.top_frame, font=('Arial', 25), text=f"Welcome to Trial #{self.trial}! Click one of the buttons on the left!")
            # self.initial.pack()
            
            self.titleFormat('Inv')
            
            self.getTable()
            
    def titleFormat(self, section):  
        for child in self.top_frame.winfo_children():
            child.destroy()
            
        self.erd_label = tk.Label(self.top_frame, font=('Arial', 25), text=f"Estimated Resupply Date: {self.current_ERD}")
        self.erd_label.pack()

        self.week_label = tk.Label(self.top_frame, font=('Arial', 25), text=f"Week: {self.week + 1}")
        self.week_label.pack()
        
        if section == 'Inv':
            self.weeks_until_inventory_runs_out_label = tk.Label(self.top_frame, font=('Arial', 20), text=f"Week that inventroy runs out: {self.weeks_until_inventory_runs_out}")
            self.weeks_until_inventory_runs_out_label.pack()

            self.max_cost_label = tk.Label(self.top_frame, font=('Arial', 20), text=f"Cost of running out of inventory without switching: {self.cost_per_week[-1]}")
            self.max_cost_label.pack()

            self.switching_cost_label = tk.Label(self.top_frame, font=('Arial', 20), text=f"Cost of of switching per week:")
            self.switching_cost_label.pack()
            
        elif section == 'ERD_Week':
            self.erd_week_labesl = tk.Label(self.top_frame, font=('Arial', 20), text=f"Here is a look at the expected ERDs:")
            self.erd_week_labesl.pack()
        else:
            self.erd_hist_cost = tk.Label(self.top_frame, font=('Arial', 20), text=f"Here is a look your historical expenses:")
            self.erd_hist_cost.pack()
            

    def getTable(self):
        for child in self.top_frame.winfo_children():
            child.destroy()
            
        self.titleFormat('Inv')
        
        self.table_frame = tk.Frame(self.top_frame)

        self.tree = ttk.Treeview(self.table_frame, columns=(1, 2, 3, 4, 5, 6), show="headings", height=1)
        self.tree.grid(row=2, column=len(self.cost_per_week), columnspan=2, padx=10, pady=10)

        # Define columns
        for week in range(len(self.cost_per_week) + 1):
            self.tree.heading(week, text=f"Week {week}")

        self.tree.insert(parent="", index="end", values=self.cost_per_week)

        for col in range(1, len(self.cost_per_week) + 1):
            self.tree.column(col, anchor="center")

        self.table_frame.pack()

    def manufacturerDelay(self):
        total = 0
        sequences = self.manufacturer.sequence[self.trial]
        total += abs(sequences[0] - sequences[-1])
        return total / len(self.manufacturer.sequence)

    def update_ERD_display(self):
        self.erd_label.config(text=f"Estimated Resupply Date: {self.current_ERD}")

    def update_week_display(self):
        self.week_label.config(text=f"Week: {self.week + 1}")

    def switch_action(self):
        self.switched = True
        self.root.quit()

    def updateERD_Hist(self):
        for child in self.top_frame.winfo_children():
            child.destroy()
            
        self.titleFormat('ERD_Hist')
        trial = self.trial
        if trial == 0:
            self.trial_vis = tk.Label(self.top_frame)
            self.trial_vis.configure(font=('Arial', 15), text='There is no historical data available yet...')
            self.trial_vis.pack()
            return
        else:
            plt.clf()
            self.trial_Title = tk.Label(self.top_frame, font=('Arial', 20), text="Historical Data for Incurred Costs")
            self.trial_Title.pack()
            # self.trial_vis.pack(side='left')
            self.trial_cost = tk.Label(self.top_frame)
            path = self.dir_name + "visualizations/Trial_" + str(trial) + ".jpg"
            img1 = Image.open(path)
            img1 = img1.resize((400, 350))
            img = ImageTk.PhotoImage(img1, master=self.root)
            self.trial_vis = tk.Label(self.top_frame, image=img)
            self.trial_vis.image=img
            self.trial_vis.pack(side='left')
            self.trial_cost.config(text= "Total cost so far: \n $"+str(self.cost))
            self.trial_cost.pack(side='right')
            return

    def updateERD_Weekly(self):
        for child in self.top_frame.winfo_children():
            child.destroy()
            
        self.titleFormat('ERD_Week')
        week = self.week
        if week == 0:
            self.trial_vis = tk.Label(self.top_frame)
            self.trial_vis.configure(font=('Arial', 15), text='Its week 1! Choose to either Wait or Switch!')
            self.trial_vis.pack()
            return
        else:
            plt.clf()
            # self.trial_vis.image = " "
            weeks = [x + 1 for x in range(week)]
            ERD = [self.manufacturer.get_sequence()[self.trial][week - 1] for week in weeks]
            self.trial_del = tk.Label(self.top_frame)
            path = self.dir_name + "visualizations/Trial_" + str(
                self.trial) + '_week_' + str(week) + '.jpg'
            plt.title("ERD Estimate (Trial: " + str(self.trial + 1) + ")")
            plt.xlabel("Week #")
            plt.ylabel("Expected ERD")
            plt.plot(weeks, ERD, color='red')
            plt.xticks(range(1, 7))
            plt.yticks(range(1, 10))
            plt.savefig(path)
            
            img1 = Image.open(path)
            img1 = img1.resize((400, 350))
            img = ImageTk.PhotoImage(img1, master=self.root)
            self.trial_vis = tk.Label(self.top_frame, image=img)
            self.trial_vis.image = img
            self.trial_vis.pack(side='left')
            self.trial_del.config(text="Average ERD Delay: \n"+str(round(self.manufacturerDelay(), 3)) + " week(s)")
            self.trial_del.pack(side='right')
            
            return

    def wait_action(self):
        # self.updateERD_Weekly()
        self.week += 1
        if self.week == len(self.manufacturer.get_sequence()[self.trial]):
            self.root.quit()
        else:
            self.current_ERD = self.manufacturer.get_sequence()[self.trial][self.week-1]
            self.update_ERD_display()
            self.update_week_display()
            self.updateERD_Weekly()
            self.getTable()

    def run_trial(self):
        # The non visual UI setup
        if not self.visual_exp:

            # Print the trial number
            print ("--------------------------START TRIAL #" + str(self.trial + 1) + "----------------------------------")

            while self.week <= 5:    
                # if the week Im in is valid AND the ERD came to be, return it.
                if self.week+1 == self.manufacturer.get_sequence()[self.trial][self.week] and self.week+1 <= 6:
                    self.data_file.write("\n - Week #" + str(self.week+1) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week]) + ", user action: " + str('STAYED'))
                    self.data_file.write("\n ERD was accomplished!")
                    self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(0))
                    self.data_file.close()
                    return 0, self.week 
                if self.manufacturer.get_sequence()[self.trial][self.week] > 6 and self.week+1 == 6:
                    self.data_file.write("\n - Week #" + str(self.week+1) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week]) + ", user action: " + str('STAYED'))
                    self.data_file.write("\n ERD was not accomplished!")
                    self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(self.cost_per_week[self.week]))
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
                        self.data_file.write("\n Switched manufacturers!")
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
            self.data_file.write("\n - Week #" + str(self.week+1) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week]) + ", user action: " + str('STAYED'))
            self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(self.cost_per_week[self.week-1]))
            self.data_file.close()
            print ("------------------------------------------------------------------------")
            print("\nYour inventory ran out, your penalty is 100000")
            print ("\n-------------------------END TRIAL #" + str(self.trial + 1) + "-----------------------------------")
            return self.cost_per_week[self.week-1], self.week-1
        else:
            self.root.mainloop()
            try:
                self.root.destroy()
            except:
                self.switched = True
            if self.switched == True:
                self.data_file.write("\n - Week #" + str(self.week) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week - 1]) + ", user action: " + str('SWITCHED'))
                self.data_file.write("\n Switched manufacturers!")
                self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(self.cost_per_week[self.week-1]))
                self.data_file.close()
                print ("---------------------------END TRIAL " + str(self.trial + 1) + "----------------------------------")
                return self.cost_per_week[self.week], self.week
            else:
                if self.week <= self.manufacturer.get_sequence()[self.trial][self.week - 1] and self.week <= 6 and self.manufacturer.get_sequence()[self.trial][self.week - 1] <= 6:
                    self.data_file.write("\n - Week #" + str(self.week) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week - 1]) + ", user action: " + str('STAYED'))
                    self.data_file.write("\n ERD was accomplished!")
                    self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(0))
                    self.data_file.close()
                    return 0, self.week - 1
                else:
                    self.data_file.write("\n - Week #" + str(self.week) + " expected ERD: Week #" + str(self.manufacturer.get_sequence()[self.trial][self.week - 1]) + ", user action: " + str('STAYED'))
                    self.data_file.write("\n ERD was not accomplished!")
                    self.data_file.write("\n Total cost for Trial #" + str(self.trial + 1) + " = " + str(self.cost_per_week[self.week - 1]))
                    self.data_file.close()
                    print("\nYour inventory ran out, your penalty is 100000")
                    print ("\n-------------------------END TRIAL #" + str(self.trial + 1) + "-----------------------------------")
                    return 100000, self.week - 1
                

def withinTrialSurvey(file_path, trial):
    
    survey = open(file_path + "Trial #" + str(trial) + " survey.txt", 'w')
    survey.write("Trial #" + str(trial) + " Survey Question Answers: ")
    print ("------------------------------------------------------------------------")
    trust = input("Trust: How much do you trust on a scale from 1-5 XYZ to deliver the product on time?: \nNone at all  (1) " +
                    "\nA little (2)  \nA moderate amount (3) \nA lot (4) \nA great deal  (5) \nInput a number from 1-5: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ1 Answer: " + trust)
    print ("------------------------------------------------------------------------")
    competence = input("Competent: How competent XYZ is in delivering drugs as promised? : \nNone at all  (1) " +
                    "\nA little (2)  \nA moderate amount (3) \nA lot (4) \nA great deal  (5) \nInput a number from 1-5: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ2 Answer: " + competence)
    print ("------------------------------------------------------------------------")
    bene = input("Benevolent: How much do you think XYZ act in the best interests of you?: \nNone at all  (1) " +
                    "\nA little (2)  \nA moderate amount (3) \nA lot (4) \nA great deal  (5) \nInput a number from 1-5: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ3 Answer: " + bene)
    print ("------------------------------------------------------------------------")
    predict = input("Predictable: How predictive are XYZ's ERD messages?: \nExtremely non-predictive  (1) " +
                    "\nSomewhat non-predictive (2) \nNeither non-predictive nor predictive (3) \nSomewhat predictive (4) \nExtremely predictive  (5) \nInput a number from 1-5: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ4 Answer: " + predict)
    print ("------------------------------------------------------------------------")
    resp = input("Responsibility How much do you think XYZ is in control of when to deliver the products during shortages?: \nExtremely not in control  (1) " +
                    "\nSomewhat not in control (2) \nNeither not in control nor in control (3) \nSomewhat in control (4) \nExtremely in control (5) \nInput a number from 1-5: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ5 Answer: " + resp)
    print ("End for Trial #" + str(trial) + " Survey")
    print ("------------------------------------------------------------------------")
    survey.close()

    return
 

def userSurvey(user, file_path):
    survey = open(file_path + "General Survey for " + str(user) + ".txt", 'w')
    survey.write("Survey Question Answers")
    print ("------------------------------------------------------------------------")
    satisfaction = input("Please rate your satisfaction in a scale from 1-5 working with XYZ: \nExtremely dissatisfied  (1) " +
                    "\nSomewhat dissatisfied (2) \nNeither satisfied nor dissatisfied (3) \nSomewhat satisfied (4) \nExtremely satisfied  (5) \nInput a number from 1-5: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ1 Satisfaction answer: " + satisfaction)
    print ("------------------------------------------------------------------------")
    work_again = input("Please rate in a scale from 1-5 how likely would you work again with XYZ: \nExtremely unlikely (1)" +
                    "\nSomewhat unlikely (2) \nNeither likely nor unlikely (3)  \nSomewhat likely (4) \nExtremely likely (5) \nInput a number from 1-5: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ2 Work again answer: " + work_again)
    print ("------------------------------------------------------------------------")
    age = input("How old are you (in years)?: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ3 Age: " + age)
    gender = input("What is your gender? (Input DNS for 'Prefer not to say'): ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ4 Gender: " + gender)
    print ("------------------------------------------------------------------------")
    edu = input("Please indicate your highest level of education (on a scale from 1-8): " +
                "\nLess than high school  (1) \nHigh school graduate  (2)  \nSome college  (3) \n2 year degree  (4) \n4 year degree  (5)" +
                "\nProfessional degree  (6)  \nMaster degree  (7) \nDoctorate  (8) \nInput a number from 1-8: ")
    print ("------------------------------------------------------------------------")
    survey.write("\nQ5 Education level: " + edu)
    survey.close()

    return

class Study():
    def __init__(self, num_trials):
        self.num_trials = num_trials

    def run_experiment(self):

        weeks = [1,2,3,4,5,6,7]
        costs = [0,0,0,0,0,0,0]

        user = input("\nHello! Add a username for to recognize you for the study!: ")

        while (True):
            if not os.path.exists("experiment_" + user + str('/')):
                os.mkdir("experiment_" + user + str('/'))
                os.mkdir("experiment_" + user + str('/visualizations/'))
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
        visual_UI = True
        for i in range(self.num_trials):
            trial = Trial(i, 6, [37500, 40000,45000,55000,70000,100000], "ACC", visual_UI, "experiment_" + user + str('/'), cost_overall)
            cost_incurred, week = trial.run_trial()
            cost_overall += cost_incurred
            print("\nTrial " + str(i+1) + " ended on week " +  str(week+1) + " and the cost incurred was $" + str(cost_incurred))
            hc_budget -= cost_incurred
            costs[i] = cost_incurred
            TrialCosts(i+1, costs, weeks, "experiment_" + user + str('/visualizations/'))
            user_data_file.write("\nTrial #" + str(i + 1) + " cost: " + str(cost_incurred))
            print("The remaining budget after Trial #" + str(i+1) + " is " + str(hc_budget) + "\n \n")
            print(" ")
            print ("------------------------------------------------------------------------")
            print("Trial #" + str(i+1) + " survey time! \n")
            withinTrialSurvey("experiment_" + user + str('/'), i+1)
            print ("------------------------------------------------------------------------")

            
        user_data_file.write("\nFinal tally cost: " + str(cost_overall))
        user_data_file.write("\nRemaining budget: " + str(hc_budget))
        user_data_file.close()
        print(" ")
        print ("------------------------------------------------------------------------")
        print("Post study survey time!: Please fill the following questions: \n")
        userSurvey(user, "experiment_" + user + str('/'))
        print("Thank you", user, "for participating!")

# set to 7
trial_total = 7
study = Study(trial_total)
study.run_experiment()