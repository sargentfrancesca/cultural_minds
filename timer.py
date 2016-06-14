#!/usr/bin/env python
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *

import os,random,math,copy,string,time

'''Timer option configuration'''
imitation_observation = 6
imitation_building = 5
imitation_testing = 3
imitation_particiants_no = 14
imitation_remove_obs_from = 3
imitation_start_times = [0, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46]

emulation_learning = 2
emulation_building = 5
emulation_testing = 3
emulation_display = 10
emulation_particiants_no = 14
emulation_remove_learning_from = 0
emulation_start_times = [0, 2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46]

teaching_learning = 2
teaching_building = 5
teaching_testing = 3
teaching_teach = 10
teaching_particiants_no = 13
teaching_remove_learning_from = 3
teaching_start_times = [4]
''' End Timer option config'''

state = False
timer = [0, 0, 0]
secs = 0
pattern = '{0:02d}:{1:02d}'

def timings(participants, array):
    times = []
    staggers = len(array) - 1
    constant = array[-1]
    for i in range(0, staggers):
        try:
            previous = times[i-1]
        except IndexError:
            previous = 0
        last = array[i] + previous
        times.append(array[i] + previous)

    times_length = len(times)
    for x in range(times_length, participants):
        previous = times[i-1]
        times.append(previous + constant)

    return times

def convert_grid(old_value):
    old_max = 60
    old_min = 0
    new_max = 300
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
        participant_type = (self.mode).capitalize()
        participant_number = i + 1

        print participant_type, participant_number

        if self.mode == 'imitation':
            start_time = self.start_time + 10
            observation = self.obs_time * 5
            
            building = self.build_time * 5
            testing = self.test_time * 5


            canvas.create_line(x, start_time, x, start_time + observation, width=20, fill="red", tags=[participant_type, participant_number, "Observation"])
            canvas.create_line(x, (start_time + observation), x, (start_time + observation + building), width=20, fill="blue", tags=[participant_type, participant_number, "Building"])
            canvas.create_line(x, (start_time + observation + building), x, (start_time + observation + building + testing), width=20, fill="yellow", tags=[participant_type, participant_number, "Testing"])
        elif self.mode == 'emulation' or self.mode == 'teaching':
            start_time = self.start_time + 10
            learning = self.learning * 5
            building = self.build_time * 5
            testing = self.test_time * 5
            teach_display = self.teach_display * 5
            if self.mode=='emulation':
                tag = 'Display'
            else:
                tag = 'Teaching'

            canvas.create_line(x, start_time, x, start_time + learning, width=20, fill="red", tags=[participant_type, participant_number, "Learning"])
            canvas.create_line(x, (start_time + learning), x, (start_time + learning + building), width=20, fill="blue", tags=[participant_type, participant_number, "Building"])
            canvas.create_line(x, (start_time + learning + building), x, (start_time + learning + building + testing), width=20, fill="yellow", tags=[participant_type, participant_number, "Testing"])
            canvas.create_line(x, (start_time + learning + building + testing), x, (start_time + learning + building + testing + teach_display), width=20, fill="pink", tags=[participant_type, participant_number, tag])

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
            start_time = n * (stagger[0] * 5)
        else:
            if participant_no < len(stagger):
                start_time = stagger[participant_no] * 5
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

''' CONFIG '''
imitation = Mode('imitation',{'observation' : imitation_observation, 'building' : imitation_building, 'testing' : imitation_testing }, imitation_particiants_no, imitation_remove_obs_from, imitation_start_times)
emulation = Mode('emulation',{'learning' : emulation_learning, 'building' : emulation_building, 'testing' : emulation_testing, 'teach_display' : emulation_display}, emulation_particiants_no, emulation_remove_learning_from, emulation_start_times)
teaching = Mode('emulation',{'learning' : teaching_learning, 'building' : teaching_building, 'testing' : teaching_testing, 'teach_display' : teaching_teach}, teaching_particiants_no,teaching_remove_learning_from, teaching_start_times)
''' END CONFIG '''

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
            timer_by_tag = self.canvas.find_withtag("timer")
            timer_coords = self.canvas.coords(timer_by_tag)
            closest = self.canvas.find_overlapping(timer_coords[0], timer_coords[1], timer_coords[2], timer_coords[3])
            intersections = []
            for close in closest:
                tags = self.canvas.gettags(close)
                if "timer" not in tags:
                    if "grid" not in tags:
                        intersections.append(tags)
                        self.canvas.itemconfig(close, fill="grey")

            print intersections
            
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
        self.timerline = self.canvas.create_line(0, 10, 1024, 10, width=1, fill="green", tags="timer")


    def draw_grid(self):
        for x in range(0, 160):
            if x%5 == 0:
                line = self.canvas.create_line(0, convert_grid(x), 1024, convert_grid(x), width=1, fill="grey", tags="grid")
            else:
                line = self.canvas.create_line(0, convert_grid(x), 1024, convert_grid(x), width=1, fill="#ecf0f1", tags="grid")

    


w = win()