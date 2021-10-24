import pygame
from api import *
from Poker import *
from demo2 import *
from tkinter import *
from tkinter import messagebox
import time
SCREEN_RECT = pygame.Rect(0,0,1000,600)
FRAME_PER_SEC = 60
poker_cur = 0
POKUER_WIDTH = 105
POKUER_HEIGHT = 150
pygame.init()





class Button(object):
    def __init__(self, text, x, y, size=30):
        self.font = pygame.font.Font("./ziti/HuXiaoBoSaoBaoTi-2.otf", size)
        self.text = self.font.render(text, True, (255, 0, 0))
        self.rect = self.text.get_rect()
        self.rect.x = x
        self.rect.y = y

class PokerGame(object):

    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        self.puke = createPoker()
        self.bt1 = Button('抽牌', 200, 300, 30)
        self.bt2 = Button('出牌', 200, 200, 30)
        self.flag = False
        # 电脑的反应延迟
        self.computer_times = 0
        self.deposit_times = 0
        self.u_flag = 0
        self.win_flag = 0
        #
        self.lock = False
        self.last_data = None

    def __create_sprites(self):
        bg1 = Backgroud()
        self.back_group = pygame.sprite.Group(bg1)
        self.bei_group = pygame.sprite.Group()
        self.hand_group = pygame.sprite.Group()
        self.enemy_hand = pygame.sprite.Group()
        self.online_heap = pygame.sprite.Group()
        cur = 0
        for i in range(52):
            bei = Back(cur)
            self.bei_group.add(bei)
            cur += 1
        self.place_group = pygame.sprite.Group()

    def start(self):
        ui_bg = pygame.image.load('./img/ui_bg.jpg')
        self.ui_bg = pygame.transform.scale(ui_bg, (1000, 600))
        self.button1 = Button('开始游戏', 400, 200, 30)
        pygame.display.set_caption("猪尾巴", "猪尾巴")
        self.bg_music()
        self.times = 0
        while True:
            if self.u_flag == 0:
                self.ui()
            elif self.u_flag == 1:
                self.choose_game()
            elif self.u_flag == 2:
                self.pvp_start_game()
            elif self.u_flag == 3:
                self.pve_start_game()
            elif self.u_flag == 4:
                self.online_face1()
            elif self.u_flag == 5:
                self.online_face2()
            elif self.u_flag == 6:
                self.online_game()
            elif self.u_flag == 7:
                self.over()

    #游戏开始界面
    def ui(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = pygame.mouse.get_pos()
                if self.button1.rect.x <= x1 <= self.button1.rect.x + self.button1.rect.width and self.button1.rect.y <= y1 <= self.button1.rect.y + self.button1.rect.height:
                    self.u_flag = 1

        self.screen.blit(self.ui_bg, (0, 0))
        self.screen.blit(self.button1.text, (self.button1.rect.x, self.button1.rect.y))
        pygame.display.update()

    def choose_game(self):
        pvp = Button("人人对战", 400, 100)
        pve = Button("人机对战", 400, 200)
        pvp_online = Button("在线对战(未完成)", 400, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = pygame.mouse.get_pos()
                if pvp.rect.x <= x1 <= pvp.rect.x + pvp.rect.width and pvp.rect.y <= y1 <= pvp.rect.y + pvp.rect.height:
                    self.u_flag = 2
                elif pve.rect.x <= x1 <= pve.rect.x + pve.rect.width and pve.rect.y <= y1 <= pve.rect.y + pve.rect.height:
                    self.u_flag = 3
                elif pvp_online.rect.x <= x1 <= pvp_online.rect.x + pvp_online.rect.width and pvp_online.rect.y <= y1 <= pvp_online.rect.y + pvp_online.rect.height:
                    self.u_flag = 4
        self.screen.blit(self.ui_bg, (0, 0))
        self.screen.blit(pvp.text, (pvp.rect.x, pvp.rect.y))
        self.screen.blit(pve.text, (pve.rect.x, pve.rect.y))
        self.screen.blit(pvp_online.text, (pvp_online.rect.x, pvp_online.rect.y))
        pygame.display.update()

    def online_face1(self):
        clock = pygame.time.Clock()
        account = Button("账号:", 330, 90)
        password = Button("密码:", 330, 130)
        sign = Button("登录", 460, 170)
        input_box1 = InputBox(400, 100, 140, 32)
        input_box2 = InputBox(400, 140, 140, 32)
        input_boxes = [input_box1, input_box2]

        # 这里不加循环会出问题
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if sign.rect.collidepoint(event.pos):
                        self.token = get_token(input_box1.text, input_box2.text)
                        if not self.token:
                            Tk().wm_withdraw()  # to hide the main window
                            print(self.token)
                            messagebox.showinfo('!', '账号或密码错误!')
                        else:
                            self.u_flag = 5
                            return
                        for box in input_boxes:
                            box.text = ''
                            box.txt_surface = FONT.render(box.text, True, box.color)

                        # self.u_flag = 5
                        # return
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            self.screen.blit(self.ui_bg, (0, 0))
            self.screen.blit(account.text, (account.rect.x, account.rect.y))
            self.screen.blit(password.text, (password.rect.x, password.rect.y))
            self.screen.blit(sign.text, (sign.rect.x, sign.rect.y))
            for box in input_boxes:
                box.draw(self.screen)

            pygame.display.update()
            clock.tick(30)

    def online_face2(self):
        clock = pygame.time.Clock()
        text_uuid = Button("uuid:", 350, 90)
        input_box1 = InputBox(400, 100, 140, 32)
        create_text = Button("创建私人房间", 450, 200)
        create_text2 = Button("创建公共房间", 450, 250)
        join_text = Button("加入", 600, 90)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if create_text.rect.collidepoint(event.pos):
                        self.uuid = create_game(True, self.token)
                        self.u_flag = 6
                        print(self.uuid)
                        return
                    if create_text.rect.collidepoint(event.pos):
                        self.uuid = create_game(False, self.token)
                        self.u_flag = 6
                        print(self.uuid)
                        return
                    if join_text.rect.collidepoint(event.pos):
                        self.uuid = input_box1.text
                        join_flag = join_game(self.token, self.uuid)
                        if join_flag:
                            print(self.uuid)
                            self.u_flag = 6
                            return
                        else:
                            input_box1.text = ''
                input_box1.handle_event(event)
                input_box1.update()

            self.screen.blit(self.ui_bg, (0, 0))
            self.screen.blit(text_uuid.text, (text_uuid.rect.x, text_uuid.rect.y))
            self.screen.blit(create_text.text, (create_text.rect.x, create_text.rect.y))
            self.screen.blit(join_text.text, (join_text.rect.x, join_text.rect.y))
            self.screen.blit(create_text2.text, (create_text2.rect.x, create_text2.rect.y))
            input_box1.draw(self.screen)

            pygame.display.update()
            clock.tick(30)


    def online_game(self):
        # 结束延迟触发
        # while True:
        # 设置刷新帧率
        self.clock.tick(FRAME_PER_SEC)
        enemy_hand_sum = Button('X{}'.format(len(self.enemy_hand)), 50, 0, 100)
        player_hand_sum = Button('X{}'.format(len(self.hand_group)), 50, 400, 100)
        text_uuid = Button('uuid:{}'.format(self.uuid), 700, 0)
        # 抽空牌堆
        if len(self.bei_group) == 0:
            if self.times >= 60:
                if len(self.enemy_hand) > len(self.hand_group):
                    self.win_flag = 1
                elif len(self.enemy_hand) < len(self.hand_group):
                    self.win_flag = 2
                else:
                    self.win_flag = 3
                # PokerGame.__game_over()
                self.u_flag = 7
            self.times += 1
        # 事件监听
        # self.deposit()
        self.online__event_handler()
        # 碰撞检测
        self.__check_collide()
        # 更新/绘制精灵组
        self.__update_sprites()
        # 更新显示
        self.screen.blit(enemy_hand_sum.text, (enemy_hand_sum.rect.x, enemy_hand_sum.rect.y))
        self.screen.blit(player_hand_sum.text, (player_hand_sum.rect.x, player_hand_sum.rect.y))
        self.screen.blit(text_uuid.text, (text_uuid.rect.x, text_uuid.rect.y))
        pygame.display.update()
    # 游戏进行界面

    def online__event_handler(self):
        if len(self.bei_group) == 0:
            return

        t_flag = False
        self.last_data = get_operation(self.token, self.uuid)
        if not self.last_data:
            for event in pygame.event.get():
                # 判断是否退出游戏
                if event.type == pygame.QUIT:
                    PokerGame.__game_over()
            Tk().wm_withdraw()
            messagebox.showinfo('!', '对局还没开始~')
            return
        self.flag = not self.last_data['your_turn']
        last_code = self.last_data['last_code'].split(' ')

        # 对手回合
        if not self.flag and not self.lock:
            if len(last_code) == 3:
                if last_code[1] == '1':
                    place_l = self.place_group.sprites()
                    enemy_l = self.enemy_hand.sprites()
                    for el in reversed(enemy_l):
                            if el.suit == last_code[2][0] and el.points == last_code[2][1:]:
                                self.place_group.add(el)
                                self.enemy_hand.remove(el)
                                self.handSort()
                                self.lock = True
                        # 出牌
                elif last_code[1] == '0':
                    # 抽牌
                    chou_sound = pygame.mixer.Sound('./music/抽牌.wav')
                    chou_sound.play()
                    for pl in self.puke:
                        if pl.suit == last_code[2][0] and pl.point == last_code[2][1:]:
                            temp = place(pl.image, pl.suit)
                            temp.set_points(pl.point)
                            self.enemy_hand.add(temp)
                            self.puke.remove(pl)
                            break
                    # self.get_poker()
                    self.handSort()
                    self.lock = True


        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PokerGame.__game_over()
            # 鼠标按下则从牌堆抽牌到放置区
            if not self.flag:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.bt1.rect.x, self.bt1.rect.y
                    x1, y1 = pygame.mouse.get_pos()
                    # 按抽牌按钮
                    if x <= x1 <= x + self.bt1.rect.width and y <= y1 <= y + self.bt1.rect.height:
                        chou_sound = pygame.mixer.Sound('./music/抽牌.wav')
                        chou_sound.play()
                        self.Set_poker()
                        self.get_online_poker()
                        self.handSort()
                        self.lock = False
                    # 按出牌按钮
                    elif self.bt2.rect.x <= x1 <= self.bt2.rect.x + self.bt2.rect.width and self.bt2.rect.y <= y1 <= self.bt2.rect.y + self.bt2.rect.height:
                        self.online_play_poker()
                        # self.get_poker()
                        self.handSort()
                        self.lock = False
                    elif 200 <= x1 <= 200 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                        self.click_poker("Spade")
                    elif 400 <= x1 <= 400 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                        self.click_poker("Heart")
                    elif 600 <= x1 <= 600 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                        self.click_poker("Club")
                    elif 800 <= x1 <= 800 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                        self.click_poker("Diamond")

    def pve_start_game(self):
        # 结束延迟触发

        # while True:
        # 设置刷新帧率
        self.clock.tick(FRAME_PER_SEC)
        enemy_hand_sum = Button('X{}'.format(len(self.enemy_hand)), 50, 0, 100)
        player_hand_sum = Button('X{}'.format(len(self.hand_group)), 50, 400, 100)
        # 抽空牌堆
        if len(self.bei_group) == 0:
            if self.times >= 60:
                if len(self.enemy_hand) > len(self.hand_group):
                    self.win_flag = 1
                elif len(self.enemy_hand) < len(self.hand_group):
                    self.win_flag = 2
                else:
                    self.win_flag = 3
                # PokerGame.__game_over()
                self.u_flag = 7
            self.times += 1
        # 事件监听
        # self.deposit()
        self.pve__event_handler()
        # 碰撞检测
        self.__check_collide()
        # 更新/绘制精灵组
        self.__update_sprites()
        # 更新显示
        self.screen.blit(enemy_hand_sum.text, (enemy_hand_sum.rect.x, enemy_hand_sum.rect.y))
        self.screen.blit(player_hand_sum.text, (player_hand_sum.rect.x, player_hand_sum.rect.y))
        pygame.display.update()

    def pvp_start_game(self):
        self.clock.tick(FRAME_PER_SEC)
        enemy_hand_sum = Button('X{}'.format(len(self.enemy_hand)), 50, 0, 100)
        player_hand_sum = Button('X{}'.format(len(self.hand_group)), 50, 400, 100)
        if self.flag:
            temp = 2
        else:
            temp = 1
        who_times = Button('现在{}P的回合'.format(temp), 30, 250, 30)
        # 抽空牌堆
        if len(self.bei_group) == 0:
            if self.times >= 60:
                if len(self.enemy_hand) > len(self.hand_group):
                    self.win_flag = 5
                elif len(self.enemy_hand) < len(self.hand_group):
                    self.win_flag = 4
                else:
                    self.win_flag = 3
                # PokerGame.__game_over()
                self.u_flag = 7
            self.times += 1
        # 事件监听
        self.pvp__event_handler()
        # 碰撞检测
        self.__check_collide()
        # 更新/绘制精灵组
        self.__update_sprites()
        # 更新显示
        self.screen.blit(enemy_hand_sum.text, (enemy_hand_sum.rect.x, enemy_hand_sum.rect.y))
        self.screen.blit(player_hand_sum.text, (player_hand_sum.rect.x, player_hand_sum.rect.y))
        self.screen.blit(who_times.text, (who_times.rect.x, who_times.rect.y))
        pygame.display.update()

    def deposit(self):
        t_flag = False
        place_l = self.place_group.sprites()
        hand_l = self.hand_group.sprites()
        self.deposit_times += 1
        if self.deposit_times >= 60:
            for pl in reversed(hand_l):
                if len(place_l) >= 1 and pl.suit != place_l[-1].suit or len(place_l) == 0:
                    self.place_group.add(pl)
                    self.hand_group.remove(pl)
                    self.handSort()
                    t_flag = True
                    break
                    # 出牌
            if not t_flag:
                # 抽牌
                chou_sound = pygame.mixer.Sound('./music/抽牌.wav')
                chou_sound.play()
                self.get_poker()
                self.handSort()
            self.flag = True
            self.deposit_times = 0
    #结束界面
    def over(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.screen.blit(self.ui_bg, (0, 0))
        # font = pygame.font.Font("./ziti/HuXiaoBoSaoBaoTi-2.otf", 30)
        if self.win_flag == 1:
            # text = font.render("恭喜你赢了！", True, (255, 0, 0))
            over_tips = Button("恭喜你赢了！", 400, 200, 30)
        elif self.win_flag == 2:
            over_tips = Button("遗憾你输了", 400, 200, 30)
        elif self.win_flag == 3:
            over_tips = Button("平局再接再厉！", 400, 200, 30)
        elif self.win_flag == 4:
            over_tips = Button("2P玩家获胜！", 400, 200, 30)
        elif self.win_flag == 5:
            over_tips = Button("1P玩家获胜！", 400, 200, 30)
        self.screen.blit(over_tips.text, (400, 200))
        pygame.display.update()

    def pvp__event_handler(self):
        if len(self.bei_group) == 0:
            return
        for event in pygame.event.get():

            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PokerGame.__game_over()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = self.bt1.rect.x, self.bt1.rect.y
                x1, y1 = pygame.mouse.get_pos()
                # 按抽牌按钮
                if x <= x1 <= x + self.bt1.rect.width and y <= y1 <= y + self.bt1.rect.height:
                    chou_sound = pygame.mixer.Sound('./music/抽牌.wav')
                    chou_sound.play()
                    self.Set_poker()
                    self.get_poker()
                    self.handSort()
                    if not self.flag:
                        self.flag = True
                    else:
                        self.flag = False
                # 按出牌按钮
                elif self.bt2.rect.x <= x1 <= self.bt2.rect.x + self.bt2.rect.width and self.bt2.rect.y <= y1 <= self.bt2.rect.y + self.bt2.rect.height:
                    temp = self.play_poker()
                    # self.get_poker()
                    self.handSort()
                    self.flag = temp
                else:
                    if not self.flag:
                        if 200 <= x1 <= 200 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                            self.click_poker("Spade")
                        elif 400 <= x1 <= 400 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                            self.click_poker("Heart")
                        elif 600 <= x1 <= 600 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                            self.click_poker("Club")
                        elif 800 <= x1 <= 800 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                            self.click_poker("Diamond")
                    else:
                        if 200 <= x1 <= 200 + POKUER_WIDTH and 50 <= y1 <= 50 + POKUER_HEIGHT:
                            self.click_poker("Spade")
                        elif 400 <= x1 <= 400 + POKUER_WIDTH and 50 <= y1 <= 50 + POKUER_HEIGHT:
                            self.click_poker("Heart")
                        elif 600 <= x1 <= 600 + POKUER_WIDTH and 50 <= y1 <= 50 + POKUER_HEIGHT:
                            self.click_poker("Club")
                        elif 800 <= x1 <= 800 + POKUER_WIDTH and 50 <= y1 <= 50 + POKUER_HEIGHT:
                            self.click_poker("Diamond")

    def pve__event_handler(self):
        # 此处可能无法正常关闭,做个标记
        if len(self.bei_group) == 0:
            return
        t_flag = False
        # 电脑回合
        if self.flag:
            place_l = self.place_group.sprites()
            enemy_l = self.enemy_hand.sprites()
            self.computer_times += 1
            if self.computer_times >= 60:
                for el in reversed(enemy_l):
                    if len(place_l) >= 1 and el.suit != place_l[-1].suit or len(place_l) == 0:
                        self.place_group.add(el)
                        self.enemy_hand.remove(el)
                        self.handSort()
                        t_flag = True
                        break
                        # 出牌
                if not t_flag:
                    # 抽牌
                    chou_sound = pygame.mixer.Sound('./music/抽牌.wav')
                    chou_sound.play()
                    self.get_poker()
                    self.handSort()
                self.flag = False
                self.computer_times = 0
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PokerGame.__game_over()
            # 鼠标按下则从牌堆抽牌到放置区
            if not self.flag:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = self.bt1.rect.x, self.bt1.rect.y
                    x1, y1 = pygame.mouse.get_pos()
                    # 按抽牌按钮
                    if x <= x1 <= x + self.bt1.rect.width and y <= y1 <= y + self.bt1.rect.height:
                        chou_sound = pygame.mixer.Sound('./music/抽牌.wav')
                        chou_sound.play()
                        self.Set_poker()
                        self.get_poker()
                        self.handSort()
                        self.flag = True
                    # 按出牌按钮
                    elif self.bt2.rect.x <= x1 <= self.bt2.rect.x + self.bt2.rect.width and self.bt2.rect.y <= y1 <= self.bt2.rect.y + self.bt2.rect.height:
                        temp = self.play_poker()
                        # self.get_poker()
                        self.handSort()
                        self.flag = temp
                    elif 200 <= x1 <= 200 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                        self.click_poker("Spade")
                    elif 400 <= x1 <= 400 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                        self.click_poker("Heart")
                    elif 600 <= x1 <= 600 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                        self.click_poker("Club")
                    elif 800 <= x1 <= 800 + POKUER_WIDTH and 400 <= y1 <= 400 + POKUER_HEIGHT:
                        self.click_poker("Diamond")
                # time.sleep(0.5)
                # if len(self.enemy_hand) == 0:

    def online_play_poker(self):
        if not self.flag:
            hand_l = self.hand_group.sprites()
            for pl in hand_l:
                if pl.flag:
                    break
            if not pl.flag:
                return False
            pl.flag = False
            self.place_group.add(pl)
            self.hand_group.remove(pl)
            operation(self.token, self.uuid, 1, pl.suit+pl.point)
            return True

    # 玩家出牌
    def play_poker(self):
        if not self.flag:
            hand_l = self.hand_group.sprites()
            for pl in hand_l:
                if pl.flag:
                    break
            if not pl.flag:
                return False
            pl.flag = False
            self.place_group.add(pl)
            self.hand_group.remove(pl)
            return True
        else:
            enemy_l = self.enemy_hand.sprites()
            for pl in enemy_l:
                if pl.flag:
                    break
            if not pl.flag:
                return True
            pl.flag = False
            self.place_group.add(pl)
            self.enemy_hand.remove(pl)
            return False

    # 置牌为False状态
    def Set_poker(self):
        hand_l = self.hand_group.sprites()
        for pl in hand_l:
            pl.flag = False
        #
        enemy_l = self.enemy_hand.sprites()
        for pl in enemy_l:
            pl.flag = False

    # 点击扑克事件
    def click_poker(self, suit):
        if not self.flag:
            hand_l = self.hand_group.sprites()
            for pl in reversed(hand_l):
                if pl.suit == suit:
                    if pl.flag:
                        pl.flag = False
                        break
                    else:
                        # 将其他牌点击状态置F
                        self.Set_poker()
                    pl.flag = True
                    pl.rect.y -= 20
                    break
        else:
            enemy_l = self.enemy_hand.sprites()
            for pl in reversed(enemy_l):
                if pl.suit == suit:
                    if pl.flag:
                        pl.flag = False
                        break
                    else:
                        # 将其他牌点击状态置F
                        self.Set_poker()
                    pl.flag = True
                    pl.rect.y -= 20
                    break
    # 抽牌
    def get_poker(self):
        global poker_cur
        pl = place(self.puke[poker_cur].image, self.puke[poker_cur].suit)
        self.place_group.add(pl)
        poker_cur += 1
        back_l = self.bei_group.sprites()
        self.bei_group.remove(back_l[52 - poker_cur])

    def get_online_poker(self):
        global poker_cur
        last_code = operation(self.token, self.uuid, 0).split(' ')
        back_l = self.bei_group.sprites()
        for pl in self.puke:
            if pl.suit[0] == last_code[2][0] and pl.point == last_code[2][1:]:
                temp = place(pl.image, pl.suit)
                temp.set_points(pl.point)
                self.place_group.add(temp)
                self.puke.remove(pl)
                poker_cur += 1
                self.bei_group.remove(back_l[52 - poker_cur])
                break

    # 检测是否同花色
    def handSort(self):
        # 判断同色
        place_l = self.place_group.sprites()
        if len(place_l) > 1:
            if place_l[-1].suit == place_l[-2].suit:
                for pl in self.place_group:
                    if not self.flag:
                        self.hand_group.add(pl)
                    else:
                        self.enemy_hand.add(pl)
                    self.place_group.remove(pl)

    def __check_collide(self):
        # 触碰动画
        for pl in self.hand_group:
            if pl.flag:
                continue
            if pl.suit == 'Spade':
                if pl.rect.x > 200:
                    pl.rect.x -= 20
            elif pl.suit == 'Heart':
                if pl.rect.x > 400:
                    pl.rect.x -= 15
            elif pl.suit == 'Club':
                if pl.rect.x > 600:
                    pl.rect.x -= 10
            elif pl.suit == 'Diamond':
                if pl.rect.x < 800:
                    pl.rect.x += 10
            if pl.rect.y < 400:
                pl.rect.y += 10

        for pl in self.enemy_hand:
            if pl.flag:
                continue
            if pl.suit == 'Spade':
                if pl.rect.x > 200:
                    pl.rect.x -= 20
            elif pl.suit == 'Heart':
                if pl.rect.x > 400:
                    pl.rect.x -= 15
            elif pl.suit == 'Club':
                if pl.rect.x > 600:
                    pl.rect.x -= 10
            elif pl.suit == 'Diamond':
                if pl.rect.x < 800:
                    pl.rect.x += 10
            if pl.rect.y > 50:
                pl.rect.y -= 10
            elif pl.rect.y < 50:
                pl.rect.y += 10


    def bg_music(self):
        pygame.mixer.music.load('./music/bg-music.mp3')
        pygame.mixer.music.play(-1)

    def __update_sprites(self):
        # self.back_group.update()
        self.back_group.draw(self.screen)
        self.bei_group.draw(self.screen)
        self.place_group.update()
        self.place_group.draw(self.screen)
        self.hand_group.draw(self.screen)
        self.enemy_hand.draw(self.screen)
        self.screen.blit(self.bt1.text, (self.bt1.rect.x, self.bt1.rect.y))
        self.screen.blit(self.bt2.text, (self.bt2.rect.x, self.bt2.rect.y))
    # 没有使用对象属性和类属性，所以定义为静态方法
    @staticmethod
    def __game_over():
        print("游戏结束")

        pygame.quit()
        exit()







if __name__ == '__main__':

    #创建游戏对象
    game = PokerGame()

    #启动游戏
    game.start()