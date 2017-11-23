import pygame
import threading


class Gui :

    def __init__(self, envList, lock):
        pygame.init()

        self.info = pygame.display.Info()

        self.fenetre = pygame.display.set_mode((self.info.current_w, self.info.current_h), pygame.FULLSCREEN)
        self.fenetre.fill((255, 255, 255))
        self.envList = envList
        self.pxarray = pygame.PixelArray(self.fenetre)
        self.lock = lock
        self.listPos = list()

        pygame.key.set_repeat(400, 30)

    def run(self):

        pygame.display.flip()

        continuer = 1

        while continuer:

            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                if event.type == pygame.QUIT:  # Si un de ces événements est de type QUIT
                    continuer = 0  # On arrête la boucle

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        continuer = 0

            self.fenetre.fill((255, 255, 255))

            self.listPos.clear()
            with self.lock:
                for el in self.envList:
                    self.listPos.append(el.position)

            for el in self.listPos:
                self.drawPoint(el, self.info)

            # Rafraichissement
            pygame.display.update()

    def drawPoint(self, pos, info):

        radius = 1
        (x, y) = pos
        x = int(x + self.info.current_w/2)
        y = int(y + self.info.current_h/2)

        if y in range()

        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                self.pxarray[i, j] = (0, 0, 0)

    def __del__(self):
        pygame.quit()
