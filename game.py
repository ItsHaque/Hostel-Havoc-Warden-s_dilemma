import pygame
from student import Student,Actions

class Game:
    def __init__(self):
        pygame.init()
        self.students=[
            Student("Abul",21),
            Student("Babul",23),
            Student("Dabul",22)
        ]
        info=pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w,info.current_h-70
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption("Hostel Havoc: Warden's Dilemma")
        self.show_student_list=False
        self.selected_student=None
        self.sidebar_width=300
        self.info_button_rect=pygame.Rect(self.WIDTH-self.sidebar_width+20,20,260,40)
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
                self.info_button_rect=pygame.rect(self.WIDTH-self.sidebar_width+20,20,260,40)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                if self.info_button_rect.collidepoint(mx,my):
                    self.show_student_list=not self.show_student_list
                    self.selected_student=None
                if self.show_student_list:
                    start_y=80
                    for idx,student in enumerate(self.students):
                        student_rect=pygame.Rect(self.WIDTH-self.sidebar_width+20, start_y+idx*40,260,35)
                        if student_rect.collidepoint(mx,my):
                            self.selected_student=student
                            break
                    

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
        # self.screen.fill((30,30,30))

        text = font.render(f"Student's Approval: {self.students_approval}", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))
        prompt = font.render("Press 1 to be Strict | Press 2 to be Lenient | Press 3 to do nothing", True, (200, 200, 200))
        self.screen.blit(prompt, (20, 60))

        #sidebar
        pygame.draw.rect(self.screen,(50,50,70),(self.WIDTH-self.sidebar_width,0,self.sidebar_width,self.HEIGHT))

        #info button
        pygame.draw.rect(self.screen,(100,100,200),self.info_button_rect)
        button_text=font.render("Show Students Info",True,(255,255,255))
        self.screen.blit(button_text,(self.info_button_rect.x+10,self.info_button_rect.y+5))


        #students list
        if self.show_student_list:
            small_font=pygame.font.SysFont("arial",20)
            start_y=80
            for idx,student in enumerate(self.students):
                student_rect=pygame.Rect(self.WIDTH-self.sidebar_width+20,start_y+idx*40,260,35)
                pygame.draw.rect(self.screen,(70,70,120),student_rect)
                name_text=small_font.render(student.name,True,(255,255,255))
                self.screen.blit(name_text,(student_rect.x+10,student_rect.y+8))

        #selected student info
        y_offset=300
        detail_font=pygame.font.SysFont("arial",18)
        lines=str(self.selected_student).split("\n")
        for line in lines:
            render=detail_font.render(line,True,(255,255,255))
            self.screen.blit(render,(self.WIDTH-self.sidebar_width+20,y_offset))
            y_offset+=25

    def run(self):
        while self.running:
            events=pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((30, 30, 30))
            

            self.handle_events(events)
            self.handle_input(events)
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
