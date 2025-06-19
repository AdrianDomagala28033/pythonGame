import pygame



class DialogBox:
    def __init__(self, text, options, font, width=400, height=150):
        self.text = text
        self.options = options
        self.font = font
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(center=(1280 // 2, 720 // 2))
        self.selected = 0
        self.active = True
        self.optionRects = []

    def draw(self, window):
        if not self.active:
            return
        self.surface.fill((20,20,20))
        pygame.draw.rect(self.surface, (200,200,200), self.surface.get_rect(), 3)

        textSurf = self.font.render(self.text, True, (255,255,255))
        self.surface.blit(textSurf, (20, 20))

        self.optionRects = []
        totalWidth = sum(self.font.size(label)[0] + 40 for label, _ in self.options)
        x = (self.width - totalWidth) // 2

        absMouse = pygame.mouse.get_pos()
        relMouse = (absMouse[0] - self.rect.x, absMouse[1] - self.rect.y)

        for i, (label, _) in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (180,180,180)
            optSurf = self.font.render(label, True, color)
            optRect = optSurf.get_rect(topleft=(x, 80))
            self.optionRects.append(optRect)
            if optRect.collidepoint(relMouse):
                self.selected = i
            isSelected = (i == self.selected)
            color = (255,255,0) if isSelected else (180,180,180)
            self.surface.blit(optSurf, optRect.topleft)
            optSurf = self.font.render(label, True, color)
            x += optRect.width + 40
        window.blit(self.surface, self.rect)


    def handleEvent(self, event):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_RIGHT:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                _, callback = self.options[self.selected]
                self.active = False
                self.closeAndExecute(callback)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mousePos = pygame.mouse.get_pos()
            relMouse = (mousePos[0] - self.rect.x, mousePos[1] - self.rect.y)

            for i, rect in enumerate(self.optionRects):
                if rect.collidepoint(relMouse):
                    _, callback = self.options[i]
                    self.closeAndExecute(callback)
                    break

    def closeAndExecute(self, callback):
        self.active = False
        if callback:
            callback()