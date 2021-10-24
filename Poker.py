import pygame
import random

class Poker(pygame.sprite.Sprite):
    '''扑克'''
    def __init__(self, poker_name):
        super().__init__()

        self.image = pygame.image.load(poker_name)
        self.rect = self.image.get_rect()
        # self.suit = suit

    def set_suit(self, suit):
        self.suit = suit

    def set_point(self, point):
        self.point = point
    def update(self):
        '''pass'''


class Backgroud(Poker):
    def __init__(self):
        super().__init__("./img/bg1.png")
        self.image = pygame.transform.scale(self.image, (1000, 600))


class Back(Poker):
    def __init__(self, cur):
        super().__init__("./img/BeiMian.jpg")
        self.rect.x = 400+cur
        self.rect.y = 200


class place(pygame.sprite.Sprite):
    def __init__(self, image, suit):
        super().__init__()
        self.suit = suit
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 200
        # 记录该牌有无被选中默认无
        self.flag = False

    def set_points(self, points):
        self.points = points

    def update(self):
        if self.rect.x > 700:
            self.rect.x -= 20
        elif self.rect.x < 700:
            self.rect.x += 20
        if self.rect.y > 200:
            self.rect.y -= 10
        elif self.rect.y < 200:
            self.rect.y += 10



'''生成并打乱扑克'''
def createPoker():
    Puke = []
    color = ['Spade', 'Heart', 'Club', 'Diamond']
    for i in range(0, 4):
        for j in range(3, 16):
            puke = Poker('./img/{}.jpg'.format(j+13*i))
            puke.set_suit(color[i])
            if 3 <= j <= 10:
                puke.set_point(str(j))
            elif j == 11:
                puke.set_point('J')
            elif j == 12:
                puke.set_point('Q')
            elif j == 13:
                puke.set_point('K')
            elif j == 14:
                puke.set_point('1')
            elif j == 15:
                puke.set_point('2')
            Puke.append(puke)
    random.shuffle(Puke)
    return Puke


