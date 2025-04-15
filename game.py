import pygame
from student import Student,Actions,Traits
from event import Event,random_events
import time
import random

class Game:
    def __init__(self):
        pygame.init()
        self.students=[
            Student("Abul",21),
            Student("Babul",23),
            Student("Dabul",22)
        ]
        self.WIDTH, self.HEIGHT = 1200,600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption("Hostel Havoc: Warden's Dilemma")
        self.show_student_list=False
        self.selected_student=None
        self.sidebar_width=300
        self.info_button_rect=pygame.Rect(self.WIDTH-self.sidebar_width+20,20,260,40)

        self.clock = pygame.time.Clock()
        self.running = True
 
        self.students_approval = 50  # 0 to 100

        self.active_event=None
        self.event_start_time=None
        self.event_duration=15
        self.last_event_time=time.time()
        self.event_font=pygame.font.SysFont("arial",20)
        self.event_choice_rects=[]

        self.current_day=1
        self.max_days=7

        self.user_quit=False

    def handle_events(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                self.running=False
            elif event.type==pygame.VIDEORESIZE:
                self.WIDTH,self.HEIGHT=event.w,event.h
                self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT),pygame.RESIZABLE)
                self.info_button_rect=pygame.Rect(self.WIDTH-self.sidebar_width+20,20,260,40)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()

                if self.active_event and self.event_choice_rects:
                    for idx,rect in enumerate(self.event_choice_rects):
                        if rect.collidepoint(mx,my):
                            self.active_event.apply_choices(idx,self.students)
                            self.update_students_approval()
                            self.active_event=None
                            return

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
                    action=Actions.LENIENT
                elif event.key==pygame.K_3:
                    action=Actions.INDIFFERENT
                self.handle_action(action)

    def handle_action(self, action):
        for student in self.students:
            student.update_happiness(action)
        total_happiness=sum(student.Happiness for student in self.students)
        self.students_approval=total_happiness//len(self.students)
        if self.current_day<self.max_days:
            self.current_day+=1
        else:
            self.running=False

    def update_students_approval(self):
        total_happiness=sum(student.Happiness for student in self.students)
        self.students_approval=total_happiness//len(self.students)

    def draw_ui(self):
        day_font=pygame.font.SysFont("arial",20)
        day_text=day_font.render(f"Day: {self.current_day}/{self.max_days}",True,(255,255,0))
        self.screen.blit(day_text,(20,20))


        font = pygame.font.SysFont("arial", 24)
        # self.screen.fill((30,30,30))

        text = font.render(f"Student's Approval: {self.students_approval}", True, (255, 255, 255))
        self.screen.blit(text, (20, 60))
        prompt = font.render("Press 1 to be Strict | Press 2 to be Lenient | Press 3 to do nothing", True, (200, 200, 200))
        self.screen.blit(prompt, (20, 100))

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
        if self.selected_student:
            lines=str(self.selected_student).split("\n")
            for line in lines:
                render=detail_font.render(line,True,(255,255,255))
                self.screen.blit(render,(self.WIDTH-self.sidebar_width+20,y_offset))
                y_offset+=25
        
        if self.active_event:
            x,y=50,self.HEIGHT//2
            pygame.draw.rect(self.screen,(80,30,30),(x,y-20,self.WIDTH-100,150))
            title=self.event_font.render(f"Event: {self.active_event.description}",True,(255,255,255))
            self.screen.blit(title,(x+10,y))

            self.event_choice_rects.clear()
            for i,(label,_) in enumerate(self.active_event.choices):
                button_rect=pygame.Rect(x+20,y+40+i*40,300,30)
                pygame.draw.rect(self.screen,(120,60,60),button_rect)
                text=self.event_font.render(label,True,(255,255,255))
                self.screen.blit(text,(button_rect.x+10,button_rect.y+5))
                self.event_choice_rects.append(button_rect)

        

    def trigger_random_event(self):
        self.active_event=random_events()
        self.event_start_time=time.time()
        self.last_event_time=time.time()
        self.event_choice_rects=[]

    def show_end_screen(self):
        self.screen.fill((30,30,30))
        font=pygame.font.SysFont("arial",36)
        if self.students_approval<30:
            lines=[
                "The students rebelled.",
                "The Warden(You) was forced to resign",
                "A new warden will take the position soon."
            ]
            color=(255,0,0)
        elif self.students_approval>80:
            lines=["You maintained order! The warden survives"]
            color=(0,255,0)
        else:
            lines=[
                "The week ends.",
                "You did ok, but not great."
            ]
            color=(200,200,0)
        
        y_offset=self.HEIGHT//2-(len(lines)*30)//2
        for line in lines:
            text_suface=font.render(line,True,color)
            self.screen.blit(text_suface,(self.WIDTH//2-text_suface.get_width()//2,y_offset))
            y_offset+=40
        
        sub_font=pygame.font.SysFont("arial",24)
        score_text=sub_font.render(f"Final Approval: {self.students_approval}",True,(200,200,200))
        self.screen.blit(score_text,(self.WIDTH//2-score_text.get_width()//2,self.HEIGHT//2+80))
        thanks_text=sub_font.render("Thanks for playing",True,(150,150,255))
        self.screen.blit(thanks_text,(self.WIDTH//2-thanks_text.get_width()//2,self.HEIGHT//2+120))
        
        button_font=pygame.font.SysFont("arial",24)
        restart_rect=pygame.Rect(self.WIDTH//2-100,self.HEIGHT-100,200,50)
        quit_rect=pygame.Rect(self.WIDTH//2-100,self.HEIGHT-50,200,50)
        restart_color=(0,200,0)
        quit_color=(200,0,0)

        pygame.draw.rect(self.screen,restart_color,restart_rect)#restart button
        pygame.draw.rect(self.screen,quit_color,quit_rect)#quit button

        restart_text=button_font.render("Restart",True,(255,255,255))
        quit_text=button_font.render("Quit",True,(255,255,255))

        self.screen.blit(restart_text,(restart_rect.x+50,restart_rect.y+10))
        self.screen.blit(quit_text,(quit_rect.x+70,quit_rect.y+10))
        
        pygame.display.flip()
        return self.handle_end_screen_buttons(restart_rect,quit_rect)

    def handle_end_screen_buttons(self,restart_rect,quit_rect):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    self.user_quit=True
                    pygame.quit()
                    quit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    mx,my=pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mx,my):
                        return True
                    elif quit_rect.collidepoint(mx,my):
                        return False
        

    def run(self):
        while self.running:
            events=pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.user_quit=True
                    self.running = False
            
            self.screen.fill((30, 30, 30))
            

            self.handle_events(events)
            self.handle_input(events)
            
            current_time=time.time()
            if not self.active_event and current_time-self.last_event_time>self.event_duration:
                self.trigger_random_event()

            if self.students_approval<30 or self.students_approval>80:
                self.running=False
                continue

            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)

        if not self.user_quit:
            return self.show_end_screen()
        else:
            pygame.quit()
            quit()
