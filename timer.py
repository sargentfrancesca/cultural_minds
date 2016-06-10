#!/usr/bin/env python
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *

import os,random,math,copy,string,time

state = False
timer = [0, 0, 0]
secs = 0
pattern = '{0:02d}:{1:02d}'

def convert_grid(old_value):
    old_max = 60
    old_min = 0
    new_max = 600
    new_min = 0
    old_range = float(old_max - old_min)
    new_range = float(new_max - new_min)
    value = float(((float((old_value - old_min) * new_range)) / old_range)) + new_min
    return float(value) + 10

class Participant:
    def __init__(self, mode):
        self.mode = mode
        self.start_time = ''
        self.obs_time = ''
        self.learning = ''
        self.build_time = ''
        self.test_time = ''
        self.teach_display = ''

    def draw_participant(self, i, canvas):
        x = (i * 40) + 100
        if self.mode == 'imitation':
            start_time = self.start_time + 10
            print "start time", start_time
            observation = self.obs_time * 10
            # print "build", self.build_time
            building = self.build_time * 10
            testing = self.test_time * 10
            # print "testing", self.test_time

            canvas.create_line(x, start_time, x, start_time + observation, width=20, fill="red")
            canvas.create_line(x, (start_time + observation), x, (start_time + observation + building), width=20, fill="blue")
            canvas.create_line(x, (start_time + observation + building), x, (start_time + observation + building + testing), width=20, fill="yellow")
        elif self.mode == 'emulation' or self.mode == 'teaching':
            start_time = self.start_time + 10
            learning = self.learning * 10
            building = self.build_time * 10
            testing = self.test_time * 10
            teach_display = self.teach_display * 10

            canvas.create_line(x, start_time, x, start_time + learning, width=20, fill="red")
            canvas.create_line(x, (start_time + learning), x, (start_time + learning + building), width=20, fill="blue")
            canvas.create_line(x, (start_time + learning + building), x, (start_time + learning + building + testing), width=20, fill="yellow")
            canvas.create_line(x, (start_time + learning + building + testing), x, (start_time + learning + building + testing + teach_display), width=20, fill="pink")

    def __repr__(self):
        return '< {} >'.format(self.mode)

class Mode:
    def __init__(self, name, stages, n_participants, remove_first, stagger):
        self.name = name
        self.stages = stages
        self.n_participants = n_participants
        self.remove_first = remove_first
        self.stagger = stagger
        self.participants = []

        for n in range(0, n_participants):           
            participant = self.create_participant(name, n, stages, remove_first, stagger)
            self.participants.append(participant)  

    
    def calculate_start(self, n, stagger):
        participant_no = n - 1
        if len(stagger) == 1:
            start_time = n * (stagger[0] * 10)
        else:
            if participant_no < len(stagger):
                start_time = stagger[participant_no] * 10
        print start_time
        return start_time

    def create_participant(self, name, n, stages, remove_first, stagger):
        participant = Participant(name)
        if n > 0:
            participant.start_time = self.calculate_start(n, stagger)
        else:
            participant.start_time = 0
        if n < remove_first and n >= 0:
            if 'observation' in stages:                                     
                participant.obs_time = 0
            else:
                participant.learning = 0
        else:
            if 'observation' in stages:
                participant.obs_time = stages['observation']
            else:
                participant.learning = stages['learning']

        participant.build_time = stages['building']
        participant.test_time = stages['testing']

        if 'teach_display' in stages:
            participant.teach_display = stages['teach_display']

        return participant


    def display_participants(self, canvas):
        for i, participant in enumerate(self.participants):
            participant.draw_participant(i, canvas)

    def __repr__(self):
        return self.name

imitation = Mode('imitation',{'observation' : 6, 'building' : 5, 'testing' : 3 }, 12, 3, [0, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38])
emulation = Mode('emulation',{'learning' : 2, 'building' : 5, 'testing' : 3 , 'teach_display' : 10}, 12, 3, [4])
teaching = Mode('emulation',{'learning' : 2, 'building' : 5, 'testing' : 3 , 'teach_display' : 10}, 10, 3, [4])

class win:
    def __init__(self):
        # create window
        self.root = Tk()
        self.root.title("Cultural Minds Timer")
        self.root.geometry("1024x768")     
        f=Frame(self.root)
        f.pack()

        # make the menu
        self.root.option_add('*tearOff', FALSE)
        menubar = Menu(self.root)
        self.root['menu']=menubar
        menu_file = Menu(menubar)
        menu_about = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')

        self.canvas=Canvas(self.root, width=1024, height=768, bg='white')
        self.canvas.pack()  

        

        self.draw_grid()

        self.mode_var = StringVar(f)
        self.mode_var.set("Imitation") # default value
        self.w = OptionMenu(f, self.mode_var, "Imitation", "Teaching", "Emulation")
        self.w.grid(row=0, column=0, sticky="we")


        self.run_button = Button(f, text="OK", command=self.select_mode)
        self.run_button.grid(row=0, column=2, sticky="we")
        
        self.timeText = Label(f, text="00:00")
        self.timeText.grid(row=0, column=3, sticky="we")     
        self.startButton = Button(f, fg='blue', text='Start', command=self.start).grid(row=0, column=5, sticky="we")
        self.pauseButton = Button(f, fg='blue', text='Pause', command=self.pause).grid(row=0, column=6, sticky="we")
        self.resetButton = Button(f, fg='blue', text='Reset', command=self.reset).grid(row=0, column=7, sticky="we")

        imitation.display_participants(self.canvas)
        self.create_line()
        self.tick()

        self.root.mainloop()

    def select_mode(self):
        mode = self.mode_var.get()
        self.reset()
        self.canvas.delete("all")        
        self.draw_grid()
        if mode == 'Imitation':
            imitation.display_participants(self.canvas)
        elif mode == 'Teaching':
            teaching.display_participants(self.canvas)
        elif mode == 'Emulation':
            emulation.display_participants(self.canvas)
        else:
            imitation.display_participants(self.canvas)
        self.create_line()
    
    def tick(self):
        if (state):
            global timer
            global secs

            timer[2] += 1
            if (timer[2] >= 100):
                timer[2] = 0
                timer[1] += 1 
                secs += 1           
            if (timer[1] >= 60):
                timer[0] += 1
                timer[1] = 0
            timeString = pattern.format(timer[0], timer[1])          
            self.timeText.configure(text=timeString)
            self.canvas.coords(self.timerline, 0, ((convert_grid(secs) / 60) + 10), 1024, ((convert_grid(secs) / 60) + 10))
        self.root.after(10, self.tick)

    def start(self):
        global state
        state = True

    def pause(self):
        global state
        state = False

    def reset(self):
        global timer
        global secs
        timer = [0, 0, 0]
        secs = 0
        self.timeText.configure(text='00:00')
        self.canvas.delete(self.timerline)
        self.create_line()

    def create_line(self):
        self.timerline = self.canvas.create_line(0, 10, 1024, 10, width=1, fill="green")


    def draw_grid(self):
        for x in range(0, 120):
            if x%5 == 0:
                line = self.canvas.create_line(0, convert_grid(x), 1024, convert_grid(x), width=1, fill="grey")
            else:
                line = self.canvas.create_line(0, convert_grid(x), 1024, convert_grid(x), width=1, fill="#ecf0f1")

    


w = win()