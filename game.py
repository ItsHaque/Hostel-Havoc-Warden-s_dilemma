import pygame
from student import Student,Actions,Traits
from event import Event,random_events
import time
import random

class Game:
    def __init__(self):
        pygame.init()
        self.students=[
            Student("Abul",random.randint(15,25)),
            Student("Babul",random.randint(15,25)),
            Student("Dabul",random.randint(15,25)),
            Student("Eabul",random.randint(15,25)),
            Student("Fabul",random.randint(15,25))
        ]
        self.set_up_friendship()
        
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

        self.action_buttons={
            Actions.STRICT: pygame.Rect(20,140,150,40),
            Actions.LENIENT: pygame.Rect(190,140,150,40),
            Actions.INDIFFERENT: pygame.Rect(360,140,150,40)
        }

        self.clicked_button=None

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
                            self.clicked_button=f"event_{idx}"
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
                
                for action,rect in self.action_buttons.items():
                    if rect.collidepoint(mx,my):
                        self.clicked_button=action
                        self.handle_action(action)
                        return
            elif event.type==pygame.MOUSEBUTTONUP:
                mx,my=pygame.mouse.get_pos()

                for action,rect in self.action_buttons.items():
                    if rect.collidepoint(mx,my):
                        self.clicked_button=None
                        # self.handle_action(action)
                        return
                if self.info_button_rect.collidepoint(mx,my) and self.clicked_button=="info":
                    self.show_student_list=not self.show_student_list
                    self.selected_student=None
                    self.clicked_button=None

                if self.active_event and self.event_choice_rects:
                    for idx,rect in enumerate(self.event_choice_rects):
                        if rect.collidepoint(mx,my) and self.clicked_button==f"event_{idx}":
                            self.active_event.apply_choices(idx,self.students)
                            # self.update_students_approval()
                            self.active_event=None
                            self.clicked_button=None
                            return
                self.clicked_button=None

    def handle_action(self, action):
        changes={}
        for student in self.students:
            change= student.update_happiness(action)
            changes[student.name]=change
        
        for student in self.students:
            for friend_name,fship_score in student.friendship.items():
                friend_change=changes.get(friend_name,0)
                shared_effect=int(friend_change*(fship_score/200))
                student.Happiness=max(0,min(100,student.Happiness+shared_effect))

        self.update_students_approval()
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

        #sidebar
        pygame.draw.rect(self.screen,(50,50,70),(self.WIDTH-self.sidebar_width,0,self.sidebar_width,self.HEIGHT))

        #info button
        info_color=(150,150,150) if self.clicked_button=="info" else (100,100,200)
        pygame.draw.rect(self.screen,info_color,self.info_button_rect)
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
                color=(180,100,100) if self.clicked_button==f"event_{i}" else (120,60,60)
                pygame.draw.rect(self.screen,color,button_rect)
                text=self.event_font.render(label,True,(255,255,255))
                self.screen.blit(text,(button_rect.x+10,button_rect.y+5))
                self.event_choice_rects.append(button_rect)

        for action,rect in self.action_buttons.items():
            if self.clicked_button==action:
                color=(150,150,150)
            else:
                color=(100,100,100)
                
            pygame.draw.rect(self.screen,color,rect)
            label=font.render(action.name.capitalize(),True,(255,255,255))
            self.screen.blit(label,(rect.x+10,rect.y+5))

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
        
        y_offset=self.HEIGHT//2-(len(lines)*100)//2
        for line in lines:
            text_suface=font.render(line,True,color)
            self.screen.blit(text_suface,(self.WIDTH//2-text_suface.get_width()//2,y_offset))
            y_offset+=40
        
        sub_font=pygame.font.SysFont("arial",24)
        score_text=sub_font.render(f"Final Approval: {self.students_approval}",True,(200,200,200))
        self.screen.blit(score_text,(self.WIDTH//2-score_text.get_width()//2,self.HEIGHT//2))
        thanks_text=sub_font.render("Thanks for playing",True,(150,150,255))
        self.screen.blit(thanks_text,(self.WIDTH//2-thanks_text.get_width()//2,self.HEIGHT//2+50))
        
        button_font=pygame.font.SysFont("arial",24)
        restart_rect=pygame.Rect(self.WIDTH//2-300,self.HEIGHT-200,200,50)
        quit_rect=pygame.Rect(self.WIDTH//2,self.HEIGHT-200,200,50)
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
        
    def set_up_friendship(self):
        for i,st1 in enumerate(self.students):
            for j in range(i+1,len(self.students)):
                st2=self.students[j]
                matching_traits=0

                for trait in st1.traits:
                    if abs(st1.traits[trait]-st2.traits[trait])<10:
                        matching_traits+=1
                
                if matching_traits>=3:
                    st1.add_friend(st2)
                    st2.add_friend(st1)

    def run(self):
        while self.running:
            events=pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.user_quit=True
                    self.running = False
            
            self.screen.fill((30, 30, 30))
            

            self.handle_events(events)
            
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
