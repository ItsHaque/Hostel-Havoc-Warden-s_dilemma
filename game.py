import pygame

class Game:
    def __init__(self):
        pygame.init()
        info=pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w,info.current_h-70
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT),pygame.RESIZABLE)
        pygame.display.set_caption("Hostel Havoc: Warden's Dilemma")
        self.clock = pygame.time.Clock()
        self.running = True
 
        self.satisfaction = 50  # 0 to 100

    def handle_events(self,events):
        for event in events:
            if event.type==pygame.QUIT:
                self.running=False
            elif event.type==pygame.VIDEORESIZE:
                self.WIDTH,self.HEIGHT=event.w,event.h
                self.screen=pygame.display.set_mode((self.WIDTH,self.HEIGHT),pygame.RESIZABLE)
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_1:
                    self.handle_choice("strict")
                elif event.key==pygame.K_2:
                    self.handle_choice("lenient")

    def handle_choice(self, choice):
        if choice == "strict":
            self.satisfaction = max(0, self.satisfaction - 10)
        elif choice == "lenient":
            self.satisfaction = min(100, self.satisfaction + 10)
        print(f"Satisfaction: {self.satisfaction}")

    def draw_ui(self):
        font = pygame.font.SysFont("arial", 24)
        text = font.render(f"Student Satisfaction: {self.satisfaction}", True, (255, 255, 255))
        self.screen.blit(text, (20, 20))

        prompt = font.render("Press 1 to be Strict | Press 2 to be Lenient", True, (200, 200, 200))
        self.screen.blit(prompt, (20, 60))

    def run(self):
        while self.running:
            events=pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((30, 30, 30))
            self.draw_ui()

            self.handle_events(events)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
