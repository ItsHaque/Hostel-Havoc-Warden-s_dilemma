import pygame
from student import Student,Actions

class Game:
    def __init__(self):
        self.students=[
            Student("Abul",21),
            Student("Babul",23),
            Student("Dabul",22)
        ]
        pygame.init()
        info=pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w,info.current_h-70
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption("Hostel Havoc: Warden's Dilemma")
        self.clock = pygame.time.Clock()
        self.running = True
 
        self.students_approval = 50  # 0 to 100

    def handle_events(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                self.running=False
            elif event.type==pygame.VIDEORESIZE:
                self.WIDTH,self.HEIGHT=event.w,event.h
                self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT),pygame.RESIZABLE)

    def handle_input(self,events):
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    action=Actions.STRICT
                elif event.key==pygame.K_2:
                    action=Actions.STRICT
                elif event.key==pygame.K_3:
                    action=Actions.STRICT
                self.handle_action(action)

    def handle_action(self, action):
        for student in self.students:
            student.update_happiness(action)
        total_happiness=sum(student.Happiness for student in self.students)
        self.students_approval=total_happiness//len(self.students)

    def draw_ui(self):
        font = pygame.font.SysFont("arial", 24)
        text = font.render(f"Student's Approval: {self.students_approval}", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))

        prompt = font.render("Press 1 to be Strict | Press 2 to be Lenient | Press 3 to do nothing", True, (200, 200, 200))
        self.screen.blit(prompt, (20, 60))

        #draw student info
        y_offset=100
        for student in self.students:
            info=font.render(f"{student.name} | Happiness: {student.Happiness}",True,(188,188,255))
            self.screen.blit(info,(20,y_offset))
            y_offset+=30


    def run(self):
        while self.running:
            events=pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((30, 30, 30))
            self.draw_ui()

            self.handle_events(events)
            self.handle_input(events)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
