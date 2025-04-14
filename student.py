from enum import Enum,auto
import random

class Traits(Enum):
    INTEGRITY = auto()
    AMBITION = auto()
    EMPATHY = auto()
    STUBBORNNESS = auto()
    CONFIDENCE = auto()

class Actions(Enum):
    STRICT = auto()
    LENIENT = auto()
    INDIFFERENT=auto()

class Student:
    def __init__(self,name,age):
        self.name=name
        self.age=age
        self.Happiness=50
        self.traits={trait: random.randint(20,80) for trait in Traits}

    def update_happiness(self,action: Actions):
        if action==Actions.STRICT:
            factor=1+self.traits[Traits.STUBBORNNESS]/100
            change=int(-5*factor)
        elif action==Actions.LENIENT:
            factor=1+self.traits[Traits.EMPATHY]/100
            change=int(5*factor)
        else:
            factor=1+self.traits[Traits.INTEGRITY]/100
            change=int(-3*factor) 
        
        self.Happiness=max(0,min(100,self.Happiness+change))
    
    def __str__(self):
        traits_string="\n".join([f"{trait.name.capitalize()}: {value}" for trait,value in self.traits.items()])
        return f"Name: {self.name} \n Age: {self.age} \n Happiness: {self.Happiness} \n Traits: \n {traits_string}"
    

