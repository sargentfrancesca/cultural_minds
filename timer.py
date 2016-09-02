#!/usr/bin/env python
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *
from threading import Timer,Thread,Event
import time

'''Timer option configuration'''
imitation_observation = 6
imitation_building = 5
imitation_testing = 3
imitation_particiants_no = 10
imitation_remove_obs_from = 1
# imitation_start_times = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36]
imitation_start_times = [0, 2, 6, 10, 14, 18, 22, 26, 30, 34]

emulation_learning = 2
emulation_building = 5
emulation_testing = 3
emulation_display = 10
emulation_particiants_no = 10
emulation_remove_learning_from = 2
emulation_start_times = [5, 8, 13, 18, 23, 28, 33, 38, 43, 48]

teaching_learning = 2
teaching_building = 5
teaching_testing = 3
teaching_teach = 10
teaching_particiants_no = 10
teaching_remove_learning_from = 2
teaching_start_times = [5, 8, 13, 18, 23, 28, 33, 38, 43, 48]
''' End Timer option config'''

state = False
timer = [0, 0, 0]
secs = 0
pattern = '{0:02d}:{1:02d}'

def draw_stage(participant, i, stage, canvas):
    canvas.create_text(100, (i * 10) + 100, text="Participant {} : {} Stage".format(participant, stage), fill="black", tags=["timer", "label"])

def draw_key(mode, canvas):
    if mode == 'imitation':
        start_time = 20
        observation = 6 * 10          
        building = 5 * 10
        testing = 3 * 10
        x = 800

        canvas.create_rectangle(x - 50, start_time-10, x + 100, (start_time + observation + building) + 50, fill="#ecf0f1", outline="#ecf0f1", tags="timer")
        canvas.create_line(x, start_time, x, start_time + observation, width=20, fill="red", tags="timer")
        canvas.create_text(x + 50, (start_time) + (observation / 2), text="Observe", fill="black", tags="timer")
        canvas.create_line(x, (start_time + observation), x, (start_time + observation + building), width=20, fill="blue", tags="timer")   
        canvas.create_text(x + 50, (start_time + observation) + (building / 2), text="Make", fill="black", tags="timer")
        canvas.create_line(x, (start_time + observation + building), x, (start_time + observation + building + testing), width=20, fill="yellow", tags="timer")
        canvas.create_text(x + 50, (start_time + observation + building) + (testing / 2), text="Test", fill="black", tags="timer")

    elif mode == 'emulation' or mode == 'teaching':
        start_time = 20
        learning = 2 * 10
        building = 5 * 10
        testing = 3 * 10
        teach_display = 10 * 10
        x = 800
        if mode=='emulation':
            tag = 'Display'
        if mode=="teaching":
            tag = 'Advice'

        canvas.create_rectangle(x - 50, start_time-10, x + 100, (start_time + learning + building + testing + teach_display) + 20, fill="#ecf0f1", outline="#ecf0f1", tags="timer")
        canvas.create_line(x, start_time, x, start_time + learning, width=20, fill="red", tags="timer")
        canvas.create_text(x + 50, start_time + (learning / 2), fill="black", text="Learn", tags="timer")
        canvas.create_line(x, (start_time + learning), x, (start_time + learning + building), width=20, fill="blue", tags="timer")
        canvas.create_text(x + 50, (start_time + learning) + (building / 2), fill="black", text="Make", tags="timer")
        canvas.create_line(x, (start_time + learning + building), x, (start_time + learning + building + testing), width=20, fill="yellow", tags="timer")
        canvas.create_text(x + 50, (start_time + learning + building) + (testing / 2), fill="black", text="Test", tags="timer")
        canvas.create_line(x, (start_time + learning + building + testing), x, (start_time + learning + building + testing + teach_display), width=20, fill="pink", tags="timer")
        canvas.create_text(x + 50, (start_time + learning + building + testing) + (teach_display / 2), fill="black", text=tag, tags="timer")
        

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
    new_max = 600
    new_min = 0
    old_range = float(old_max - old_min)
    new_range = float(new_max - new_min)
    value = float(((float((old_value - old_min) * new_range)) / old_range)) + new_min
    return float(value) + 10

global paused
global offset
paused = False
offset = 0

class RealTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      global state
      global paused
      global start_time
      global elapsed
      start_time = time.time()

      state = True      

      self.thread.start()


   def pause(self):
      global state
      global paused
      state = False
      paused = True      
      global pause_time
      pause_time = elapsed
      self.thread.cancel()

   def cancel(self):
      global state
      global paused
      global offset
      state = False
      paused = False
      offset = 0
      self.thread.cancel()


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

        print self.mode
        draw_key(self.mode, canvas)

        if self.mode == 'imitation':
            
            start_time = self.start_time + 10
            if participant_number == 2:
                observation = 4 * 10
            else:
                observation = self.obs_time * 10          
            building = self.build_time * 10
            testing = self.test_time * 10

            canvas.create_rectangle(x+30, start_time, x+60, start_time + observation, fill="red", outline="red", tags=[participant_type, participant_number, "Observe"])
            canvas.create_rectangle(x+30, start_time + observation, x+60, start_time + observation + building, fill="blue", outline="blue", tags=[participant_type, participant_number, "Make"])
            if observation != 0:
                canvas.create_text(x+45, (start_time + observation) + (observation / 2), text=participant_number, fill="white", tags="timer", font=("Purisa", 24))
            else:
                canvas.create_text(x+45, building/2, text=participant_number, fill="white", tags="timer", font=("Purisa", 24))
            canvas.create_rectangle(x+30, start_time + observation + building, x+60, start_time + observation + building + testing, fill="yellow", outline="yellow", tags=[participant_type, participant_number, "Test"])
        
        elif self.mode == 'emulation' or self.mode == 'teaching':
            start_time = self.start_time + 10
            learning = self.learning * 10
            building = self.build_time * 10
            testing = self.test_time * 10
            teach_display = self.teach_display * 10
            if self.mode=='emulation':
                tag = 'Display'
                tag_fill = "pink"
            else:
                tag = 'Advice'
                tag_fill = "pink"

            canvas.create_rectangle(x+30, start_time, x+60, start_time + learning, fill="red", outline="red", tags=[participant_type, participant_number, "Learn"])
            canvas.create_rectangle(x+30, start_time + learning, x+60, start_time + learning + building, fill="blue", outline="blue", tags=[participant_type, participant_number, "Make"])
            
            if learning != 0:
                canvas.create_text(x+45, (start_time + learning) + (building / 2), text=participant_number, fill="white", tags="timer", font=("Purisa", 24))
            else:
                canvas.create_text(x+45, (start_time + learning) + (building/2), text=participant_number, fill="white", tags="timer", font=("Purisa", 24))
            canvas.create_rectangle(x+30, start_time + learning + building, x+60, start_time + learning + building + testing, fill="yellow", outline="yellow", tags=[participant_type, participant_number, "Test"])
            canvas.create_rectangle(x+30, start_time + learning + building + testing, x+60, start_time + learning + building + testing + teach_display, fill="pink", outline="pink", tags=[participant_type, participant_number, tag])

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
teaching = Mode('teaching',{'learning' : teaching_learning, 'building' : teaching_building, 'testing' : teaching_testing, 'teach_display' : teaching_teach}, teaching_particiants_no,teaching_remove_learning_from, teaching_start_times)
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
        
        # self.tick()

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

    def rec_time(self):
        global elapsed
        global offset
        global paused
        

        if paused:
            offset = pause_time
            paused = False

        elapsed = (time.time() - start_time) + offset

        global time_string
        m, s = divmod(elapsed, 60)
        h, m = divmod(m, 60)
        time_string = "%d:%02d:%02d" % (h, m, s)

        print "Real Time", elapsed, time_string

        self.timeText.configure(text=time_string)
        self.canvas.coords(self.timerline, 0, ((convert_grid(elapsed) / 60) + 10), 1024, ((convert_grid(elapsed) / 60) + 10))
        timer_by_tag = self.canvas.find_withtag("line")
        timer_coords = self.canvas.coords(timer_by_tag)
        closest = self.canvas.find_overlapping(timer_coords[0], timer_coords[1], timer_coords[2], timer_coords[3])
        finished = self.canvas.find_enclosed(0, 0, timer_coords[2], timer_coords[3])
        intersections = []
        for finish in finished:
            tags = self.canvas.gettags(finish)
            if "timer" not in tags:
                if "grid" not in tags:
                    if "line" not in tags:
                        coords = self.canvas.coords(finish)
                        object_bound = coords[3]
                        timer_bound = timer_coords[1]
                        if timer_bound > object_bound:
                            self.canvas.itemconfig(finish, outline="grey", fill="grey")

        for i, close in enumerate(closest):
            tags = self.canvas.gettags(close)
            if "timer" not in tags:
                if "grid" not in tags:
                    if "line" not in tags:
                        if "label" not in tags:
                            intersections.append(tags)
                            self.canvas.itemconfig(close, outline="green")

        return elapsed

    def start(self):
        global state
        state = True
        self.t = RealTimer(1,self.rec_time)
        self.t.start()

    def pause(self):
        global state
        state = False
        self.t.pause()

    def reset(self):
        global timer
        global secs
        timer = [0, 0, 0]
        secs = 0
        self.timeText.configure(text='00:00:00')
        self.canvas.delete(self.timerline)
        try:
            self.t.cancel()
        except AttributeError:
            pass

        self.create_line()

    def create_line(self):
        self.timerline = self.canvas.create_line(0, 10, 1024, 10, width=1, fill="green", tags=["timer", "line"])


    def draw_grid(self):
        for x in range(0, 120):
            if x%5 == 0:
                line = self.canvas.create_line(0, convert_grid(x), 1024, convert_grid(x), width=1, fill="grey", tags="grid")
            else:
                line = self.canvas.create_line(0, convert_grid(x), 1024, convert_grid(x), width=1, fill="#ecf0f1", tags="grid")

    


w = win()