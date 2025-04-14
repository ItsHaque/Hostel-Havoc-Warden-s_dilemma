import random
from student import Actions,Traits

class Event:
    def __init__(self,description,choices):
        self.description=description
        self.choices=choices

    def apply_choices(self,index,students):
        label,effect_function=self.choices[index]
        effect_function(students)

def punish_students(students):
    for student in students:
        factor=1+student.traits[Traits.STUBBORNNESS]/100
        student.Happiness=max(0,student.Happiness-int(10*factor))

def warn_students(students):
    for student in students:
        factor=1+student.traits[Traits.EMPATHY]/100
        student.Happiness=max(0,min(100,student.Happiness+int(10*factor)))

def ignore_students(students):
    for student in students:
        factor=1+student.traits[Traits.INTEGRITY]/100
        student.Happiness=max(0,student.Happiness-int(10*factor))

def random_events():
    events=[
        Event("A student was caught sneaking out",[
            ("Punish",punish_students),
            ("Warn",warn_students),
            ("Ignore",ignore_students)
        ]),
        Event("Two students was caught fighting in the dorm",[
            ("Punish",punish_students),
            ("Warn",warn_students),
            ("Ignore",ignore_students)
        ]),
        Event("A student returned to hostel after 10 PM last night",[
            ("Punish",punish_students),
            ("Warn",warn_students),
            ("Ignore",ignore_students)
        ]),
    ]
    return random.choice(events)