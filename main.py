import pygame
from pygame.locals import *
import json
import sys
import random

# 設定ファイルのパス
SETTING_FILE_PATH = "setting.json"

# デフォルトの設定
DEFAULT_SETTING = {
    "leftTeam" : "LeftTeam",
    "rightTeam" : "RightTeam",
    "score" : 5,
    "time" : {
        "min" : 2,
        "sec" : 30
    },
    "timerReverse": False,
    "isSwap" : False,
    "key" : {
        "left" : {
            "up" : "w",
            "down" : "s",
            "nup" : "d",
            "ndown" : "a"
        },
        "right" : {
            "up" : "up",
            "down" : "down",
            "nup" : "right",
            "ndown" : "left"
        }
    },
    "resolution" : {
        "width" : 800,
        "height" : 450
    },
    "title" : "共ロボタイマー",
    "font" : "Meiryo"
}


class KyoroboTimer:
    # メンバ変数
    __setting = DEFAULT_SETTING

    __leftTeam = { "name" : "", "score" : 0 }
    __rightTeam = { "name" : "", "score" : 0 }
    __time = { "min" : 0, "sec" : 10 }
    __settingTime = { "min" : 0, "sec" : 0 }
    __setTime = { "min" : 0, "sec" : 0 }

    __icon = None

    __Red = (255, 0, 0)
    __Green = (0, 255, 0)
    __Blue = (0, 0, 255)

    __swap = False

    __cursor = {"x" : 0, "y" : 0}

    __settingFilePath = ""

    __loadFlag = 0

    # x,y,方向,色,速度,半径
    __circleList = [[None,None,False,(147, 247, 255),None,None],
                    [None,None,False,(147, 247, 255),None,None],
                    [None,None,False,(147, 247, 255),None,None],
                    [None,None,False,(147, 247, 255),None,None],
                    [None,None,False,(147, 247, 255),None,None],
                    [None,None,False,(147, 247, 255),None,None],
                    [None,None,False,(255, 249, 132),None,None],
                    [None,None,False,(255, 249, 132),None,None],
                    [None,None,False,(255, 249, 132),None,None],
                    [None,None,False,(255, 249, 132),None,None],
                    [None,None,False,(255, 249, 132),None,None],
                    [None,None,False,(255, 249, 132),None,None],
                    [None,None,False,(187, 180, 250),None,None],
                    [None,None,False,(187, 180, 250),None,None],
                    [None,None,False,(187, 180, 250),None,None],
                    [None,None,False,(187, 180, 250),None,None],
                    [None,None,False,(187, 180, 250),None,None],
                    [None,None,False,(187, 180, 250),None,None],
                    [None,None,False,(200, 255, 200),None,None],
                    [None,None,False,(200, 255, 200),None,None],
                    [None,None,False,(200, 255, 200),None,None],
                    [None,None,False,(200, 255, 200),None,None],
                    [None,None,False,(200, 255, 200),None,None],
                    [None,None,False,(200, 255, 200),None,None]]
                        

    beepHi = None
    beepLo = None

    # 設定ファイルの読み込み
    def loadSetting(self):
        # 設定ファイルの読み込み
        try:
            self.__setting = json.load(open(self.__settingFilePath, "r", encoding="utf-8"))
        except UnicodeDecodeError:
            self.__setting = json.load(open(self.__settingFilePath, "r", encoding="shift-jis"))
        except FileNotFoundError:
            print("setting.jsonが見つかりませんでした。")
        except json.decoder.JSONDecodeError:
            print("setting.jsonが壊れています。")
        except Exception as e:
            print("不明なエラーが発生しました。以下のエラーメッセージを開発者に送ってください。")
            print(e)

        self.__time["min"] = self.__setting["time"]["min"]
        self.__time["sec"] = self.__setting["time"]["sec"]
        self.__leftTeam["name"] = self.__setting["leftTeam"]
        self.__rightTeam["name"] = self.__setting["rightTeam"]

        self.__leftKeys = {
            "up" : pygame.key.key_code(self.__setting["key"]["left"]["up"]),
            "down" : pygame.key.key_code(self.__setting["key"]["left"]["down"]),
            "nup" : pygame.key.key_code(self.__setting["key"]["left"]["nup"]),
            "ndown" : pygame.key.key_code(self.__setting["key"]["left"]["ndown"]),
            "reset" : pygame.key.key_code(self.__setting["key"]["left"]["reset"])
        }
        self.__rightKeys = {
            "up" : pygame.key.key_code(self.__setting["key"]["right"]["up"]),
            "down" : pygame.key.key_code(self.__setting["key"]["right"]["down"]),
            "nup" : pygame.key.key_code(self.__setting["key"]["right"]["nup"]),
            "ndown" : pygame.key.key_code(self.__setting["key"]["right"]["ndown"]),
            "reset" : pygame.key.key_code(self.__setting["key"]["right"]["reset"])
        }
        self.__swapKey = pygame.key.key_code(self.__setting["key"]["swap"])

    # 設定ファイルの保存
    def saveSetting(self):
        try:
            json.dump(self.__setting, open(self.__settingFilePath, "w", encoding="utf-8"), indent=4, ensure_ascii=False)
        except UnicodeEncodeError:
            json.dump(self.__setting, open(self.__settingFilePath, "w", encoding="shift-jis"), indent=4, ensure_ascii=False)
        except Exception as e:
            print("設定ファイルの保存に失敗しました。")
            print(e)

    # 初期化処理
    def __init__(self, setting_file_path):
        pygame.init()
        self.__settingFilePath = setting_file_path

        self.loadSetting()

        # アイコンの読み込み
        try:
            self.__icon = pygame.image.load("img/icon.png")
            pygame.display.set_icon(self.__icon)
        except Exception as e:
            print("アイコンの読み込みに失敗しました。")
            print(e)
        
        # フォントの読み込み
        try:
            with open("font/DSEG7Classic-Bold.ttf", "rb") as f:
                self.__timerFontObject = f.read()
        except Exception as e:
            print("フォントの読み込みに失敗しました。")
            print(e)

        # 効果音の読み込み
        try:
            self.beepLo = pygame.mixer.Sound("sounds/beepLo.wav")
            self.beepHi = pygame.mixer.Sound("sounds/beepHi.wav")
        except Exception as e:
            print("効果音の読み込みに失敗しました。")
            print(e)

        try:
            self.__logo = pygame.image.load("img/logo.png")
        except Exception as e:
            print("ロゴの読み込みに失敗しました。")
            print(e)

        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)

        pygame.display.set_caption("共ロボタイマー")
        
    # デストラクタ
    def __del__(self):
        pygame.quit()

    # メインループ
    def run(self):
        nowFunction = self.title
        
        while True:
            code = nowFunction()

            if code == "exit":
                nowFunction = self.title
                self.__time["min"] = self.__setting["time"]["min"]
                self.__time["sec"] = self.__setting["time"]["sec"]
                self.__leftTeam["score"] = 0
                self.__rightTeam["score"] = 0
            elif code == "timer":
                nowFunction = self.timer
            elif code == "countdown":
                nowFunction = self.countdown
                self.__setTime["min"] = self.__time["min"]
                self.__setTime["sec"] = self.__time["sec"]
                pygame.time.set_timer(USEREVENT, 1000)
                self.__count = 5
            elif code == "setting":
                nowFunction = self.setting
                self.__cursor["y"] = 0
            elif code == "preview":
                nowFunction = self.preview
            elif code == "timerSetting":
                nowFunction = self.timerSetting
                self.__tmpTimeReverse = self.__setting["timerReverse"]
                self.__settingTime["min"] = self.__time["min"]
                self.__settingTime["sec"] = self.__time["sec"]
                self.__cursor["y"] = 0
                self.__cursor["x"] = 0

            pygame.time.wait(30)

            pygame.display.update()

    # タイトル画面
    def title(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                if event.key == K_F11:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                    else:
                        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                if event.key == K_RETURN:
                    return "countdown"
                if event.key == K_LSHIFT or event.key == K_RSHIFT:
                    return "setting"
                
                

        windowsize = pygame.display.get_surface().get_size()

        # 背景の描画
        pygame.draw.rect(self.screen, (255, 255, 255), Rect(0, 0, windowsize[0], windowsize[1]))

        for i in range(len(self.__circleList)):
            if self.__circleList[i][0] == None:
                if random.random() < 0.005:
                    x = random.random()
                    radius = random.uniform(0.5, 1)
                    speed = random.uniform(0.005 / 4, 0.015 / 4)
                    if random.random() < 0.5:
                        self.__circleList[i] = (x, 0 - radius / 5, True, self.__circleList[i][3], speed, radius)
                    else:
                        self.__circleList[i] = (x, 1 + radius / 5, False, self.__circleList[i][3], speed, radius)
                else:
                    continue
            else:
                if self.__circleList[i][2]:
                    self.__circleList[i] = (self.__circleList[i][0], self.__circleList[i][1] + self.__circleList[i][4], True, self.__circleList[i][3], self.__circleList[i][4], self.__circleList[i][5])
                else:
                    self.__circleList[i] = (self.__circleList[i][0], self.__circleList[i][1] - self.__circleList[i][4], False, self.__circleList[i][3], self.__circleList[i][4], self.__circleList[i][5])

                if self.__circleList[i][1] < 0 - self.__circleList[i][5] / 5 or self.__circleList[i][1] > 1 + self.__circleList[i][5] / 5:
                    self.__circleList[i] = (None, None, False, self.__circleList[i][3], None, None)
                else:
                    pygame.draw.circle(self.screen, self.__circleList[i][3], (self.__circleList[i][0] * windowsize[0], self.__circleList[i][1] * windowsize[1]), int(windowsize[0] * self.__circleList[i][5] / 10) )
            


        logoScale = (windowsize[1] / 3) / self.__logo.get_height()

        showLogo = pygame.transform.scale(self.__logo, (int(self.__logo.get_width() * logoScale), int(self.__logo.get_height() * logoScale)))

        self.screen.blit(showLogo, (windowsize[0] / 2 - showLogo.get_width() / 2, windowsize[1] / 2 - showLogo.get_height() / 2))
        
                
        return ""

    # 設定画面
    def setting(self):
        settingElem = ["チーム名", "時間設定", "一度に増やすスコア", "左右入れ替え", "キーコンフィグ", "設定ファイルの再読み込み", "プレビュー", "戻る"]

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F11:
                        if self.screen.get_flags() & pygame.FULLSCREEN:
                            self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                        else:
                            self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                
                if event.key == K_ESCAPE:
                    return "exit"
                if event.key == K_UP:
                    self.__cursor["y"] -= 1
                if event.key == K_DOWN:
                    self.__cursor["y"] += 1
                if event.key == K_RETURN:
                    if self.__cursor["y"] == 7:
                        return "exit"
                    elif self.__cursor["y"] == 6:
                        return "preview"
                    elif self.__cursor["y"] == 5:
                        self.loadSetting()
                        self.__loadFlag = 50
                    elif self.__cursor["y"] == 1:
                        return "timerSetting"
                    else:
                        self.beepLo.play()
        

        if self.__cursor["y"] < 0:
            self.__cursor["y"] = len(settingElem) - 1
        if self.__cursor["y"] > len(settingElem) - 1:
            self.__cursor["y"] = 0


        windowsize = pygame.display.get_surface().get_size()

        # 背景の描画
        pygame.draw.rect(self.screen, (255, 255, 255), Rect(0, 0, windowsize[0], windowsize[1]))


        font = pygame.font.SysFont(self.__setting["font"], int(windowsize[1] / (10 + len(settingElem))))
        textList = []
        for i in range(len(settingElem)):
            text = font.render(settingElem[i], True, (0, 0, 0))
            textList.append(text)
            self.screen.blit(text, (windowsize[0] / 2 - text.get_width() / 2, windowsize[1]* (i + 1.5) / (len(settingElem) + 2)  - text.get_height() / 2))

        pygame.draw.rect(self.screen, self.__Red, Rect(windowsize[0] / 2 - textList[self.__cursor["y"]].get_width() / 2 - 10, windowsize[1]* (self.__cursor["y"] + 1.5) / (len(settingElem) + 2) - textList[self.__cursor["y"]].get_height() / 2, textList[self.__cursor["y"]].get_width() + 20, textList[self.__cursor["y"]].get_height()), 2)
        
        if self.__loadFlag > 0:
            self.__loadFlag -= 1
            font = pygame.font.SysFont(self.__setting["font"], int(windowsize[1] / 10))
            text = font.render("設定を再読み込みしました。", True, (255,0,0))
            self.screen.blit(text, (windowsize[0] / 2 - text.get_width() / 2, windowsize[1] / 2 - text.get_height() / 2))

        return ""

    # カウントダウン画面
    def countdown(self):

        for event in pygame.event.get():
            if event.type == USEREVENT:
                self.__count -= 1
                if self.__count == -1:
                    self.__time["sec"] -= 1
                    return "timer"
                elif self.__count == 0:
                    self.beepHi.play()
                elif self.__count <= 3:
                    self.beepLo.play()
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.time.set_timer(USEREVENT, 0)
                    return "exit"
                if event.key == K_F11:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                    else:
                        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                
            windowsize = pygame.display.get_surface().get_size()

            # 背景の描画
            pygame.draw.rect(self.screen, (0, 0, 0), Rect(0, 0, windowsize[0], windowsize[1]))

            # カウントダウンの描画
            
            if self.__count == 0:
                font = pygame.font.SysFont(self.__setting["font"], int(windowsize[1] / 3))
                text = font.render("START!", True, (255, 255, 255))
            else:
                font = pygame.font.SysFont(self.__setting["font"], int(windowsize[1] / 1 - windowsize[1] / 10))
                text = font.render(str(self.__count), True, (255, 255, 255))
            self.screen.blit(text, (windowsize[0] / 2 - text.get_width() / 2, windowsize[1] / 2 - text.get_height() / 2))

            
        return ""

    # タイマー画面
    def timer(self):
        for event in pygame.event.get():
            if event.type == USEREVENT:
                time = self.__time["min"] * 60 + self.__time["sec"]
                time -= 1
                self.__time["min"] = time // 60
                self.__time["sec"] = time % 60

                if time == 0:
                    self.beepHi.play()
                    pygame.time.set_timer(USEREVENT, 0)
                elif time <= 3:
                    self.beepLo.play()

            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.time.set_timer(USEREVENT, 0)
                    return "exit"


                if event.key == K_F11:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                    else:
                        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

                if event.key == self.__leftKeys["up"]:
                    self.__leftTeam["score"] += 1
                if event.key == self.__leftKeys["down"]:
                    self.__leftTeam["score"] -= 1
                if event.key == self.__leftKeys["nup"]:
                    self.__leftTeam["score"] += self.__setting["score"]
                if event.key == self.__leftKeys["ndown"]:
                    self.__leftTeam["score"] -= self.__setting["score"]
                if event.key == self.__leftKeys["reset"]:
                    self.__leftTeam["score"] = 0

                if event.key == self.__rightKeys["up"]:
                    self.__rightTeam["score"] += 1
                if event.key == self.__rightKeys["down"]:
                    self.__rightTeam["score"] -= 1
                if event.key == self.__rightKeys["nup"]:
                    self.__rightTeam["score"] += self.__setting["score"]
                if event.key == self.__rightKeys["ndown"]:
                    self.__rightTeam["score"] -= self.__setting["score"]
                if event.key == self.__rightKeys["reset"]:
                    self.__rightTeam["score"] = 0

                if event.key == self.__swapKey:
                    self.__swap = not self.__swap
                    self.__leftTeam, self.__rightTeam = self.__rightTeam, self.__leftTeam

        if(self.__leftTeam["score"] < 0):
            self.__leftTeam["score"] = 0
        if(self.__rightTeam["score"] < 0):
            self.__rightTeam["score"] = 0

        windowSise = pygame.display.get_surface().get_size()

        # 背景の描画
        pygame.draw.rect(self.screen, (0, 0, 0), Rect(0, 0, windowSise[0], windowSise[1]))

        if self.__swap:
            leftColor = self.__Red
            rightColor = self.__Blue
        else:
            leftColor = self.__Blue
            rightColor = self.__Red

        pygame.draw.rect(self.screen, leftColor, Rect(0, 0, windowSise[0] / 2, windowSise[1] * 4 / 10))
        pygame.draw.rect(self.screen, rightColor, Rect(windowSise[0] / 2, 0, windowSise[0] / 2, windowSise[1] * 4 / 10))
        pygame.draw.rect(self.screen, (20, 20, 20), Rect(0, windowSise[1] * 4 / 10, windowSise[0], windowSise[1] / 10))

        # タイマーの描画
        if not self.__setting["timerReverse"]:
            now = self.__time["min"] * 60 + self.__time["sec"]
            first = self.__setTime["min"] * 60 + self.__setTime["sec"]
            min = int((first - now) / 60)
            sec = int((first - now) % 60)
            time = str(min).zfill(2) + ":" + str(sec).zfill(2)
        else:
            time = str(self.__time["min"]).zfill(2) + ":" + str(self.__time["sec"]).zfill(2)
        # timerFont = pygame.font.Font(object(self.__timerFontObject), int(windowSise[1] / 2 - windowSise[1] / 10))
        timerFont = pygame.font.Font("font/DSEG7Classic-Bold.ttf", int(windowSise[1] / 2 - windowSise[1] / 10))

        if self.__time["min"] == 0 and self.__time["sec"] == 0:
            timerText = timerFont.render(time, True, self.__Red)
        else:
            timerText = timerFont.render(time, True, (255, 255, 255))
        self.screen.blit(timerText, (windowSise[0] / 2 - timerText.get_width() / 2, windowSise[1] * 3 / 4 - timerText.get_height() / 2))

        # スコアの描画
        scoreFont = pygame.font.SysFont(self.__setting["font"], int(windowSise[1] * 4 / 10))

        leftTeamText = scoreFont.render(str(self.__leftTeam["score"]), True, (255, 255, 255))
        rightTeamText = scoreFont.render(str(self.__rightTeam["score"]), True, (255, 255, 255))
        self.screen.blit(leftTeamText, (windowSise[0] / 4 - leftTeamText.get_width() / 2, windowSise[1] * 4 / 20 - leftTeamText.get_height() / 2))
        self.screen.blit(rightTeamText, (windowSise[0] * 3 / 4 - rightTeamText.get_width() / 2, windowSise[1] * 4 / 20 - rightTeamText.get_height() / 2))

        # チーム名の描画
        font = pygame.font.SysFont(self.__setting["font"], int(windowSise[1] / 10 - (windowSise[1] / 10) / 4))

        leftTeamName = font.render(self.__leftTeam["name"], True, (255, 255, 255))
        rightTeamName = font.render(self.__rightTeam["name"], True, (255, 255, 255))

        if leftTeamName.get_width() > windowSise[0] / 2:
            leftTeamName = pygame.transform.scale(leftTeamName, (int(windowSise[0] / 2), int(leftTeamName.get_height() * (windowSise[0] / 2) / leftTeamName.get_width())))
        if rightTeamName.get_width() > windowSise[0] / 2:
            rightTeamName = pygame.transform.scale(rightTeamName, (int(windowSise[0] / 2), int(rightTeamName.get_height() * (windowSise[0] / 2) / rightTeamName.get_width())))

        self.screen.blit(leftTeamName, (windowSise[0] / 4 - leftTeamName.get_width() / 2, windowSise[1] * 9 / 20 - leftTeamName.get_height() / 2))
        self.screen.blit(rightTeamName, (windowSise[0] * 3 / 4 - rightTeamName.get_width() / 2, windowSise[1] * 9 / 20 - rightTeamName.get_height() / 2))

        return ""

    # プレビュー画面
    def preview(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.__time["min"] = self.__setting["time"]["min"]
                    self.__time["sec"] = self.__setting["time"]["sec"]
                    self.__leftTeam["score"] = 0
                    self.__rightTeam["score"] = 0
                    return "setting"


                if event.key == K_F11:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                    else:
                        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

                if event.key == self.__leftKeys["up"]:
                    self.__leftTeam["score"] += 1
                if event.key == self.__leftKeys["down"]:
                    self.__leftTeam["score"] -= 1
                if event.key == self.__leftKeys["nup"]:
                    self.__leftTeam["score"] += self.__setting["score"]
                if event.key == self.__leftKeys["ndown"]:
                    self.__leftTeam["score"] -= self.__setting["score"]
                if event.key == self.__leftKeys["reset"]:
                    self.__leftTeam["score"] = 0

                if event.key == self.__rightKeys["up"]:
                    self.__rightTeam["score"] += 1
                if event.key == self.__rightKeys["down"]:
                    self.__rightTeam["score"] -= 1
                if event.key == self.__rightKeys["nup"]:
                    self.__rightTeam["score"] += self.__setting["score"]
                if event.key == self.__rightKeys["ndown"]:
                    self.__rightTeam["score"] -= self.__setting["score"]
                if event.key == self.__rightKeys["reset"]:
                    self.__rightTeam["score"] = 0

                if event.key == self.__swapKey:
                    self.__swap = not self.__swap
                    self.__leftTeam, self.__rightTeam = self.__rightTeam, self.__leftTeam

        if(self.__leftTeam["score"] < 0):
            self.__leftTeam["score"] = 0
        if(self.__rightTeam["score"] < 0):
            self.__rightTeam["score"] = 0

        windowSise = pygame.display.get_surface().get_size()

        # 背景の描画
        pygame.draw.rect(self.screen, (0, 0, 0), Rect(0, 0, windowSise[0], windowSise[1]))

        if self.__swap:
            leftColor = self.__Red
            rightColor = self.__Blue
        else:
            leftColor = self.__Blue
            rightColor = self.__Red

        pygame.draw.rect(self.screen, leftColor, Rect(0, 0, windowSise[0] / 2, windowSise[1] * 4 / 10))
        pygame.draw.rect(self.screen, rightColor, Rect(windowSise[0] / 2, 0, windowSise[0] / 2, windowSise[1] * 4 / 10))
        pygame.draw.rect(self.screen, (20, 20, 20), Rect(0, windowSise[1] * 4 / 10, windowSise[0], windowSise[1] / 10))

        # タイマーの描画
        time = str(self.__time["min"]).zfill(2) + ":" + str(self.__time["sec"]).zfill(2)
        # timerFont = pygame.font.Font(object(self.__timerFontObject), int(windowSise[1] / 2 - windowSise[1] / 10))
        timerFont = pygame.font.Font("font/DSEG7Classic-Bold.ttf", int(windowSise[1] / 2 - windowSise[1] / 10))

        if time == "00:00":
            timerText = timerFont.render(time, True, self.__Red)
        else:
            timerText = timerFont.render(time, True, (255, 255, 255))
        self.screen.blit(timerText, (windowSise[0] / 2 - timerText.get_width() / 2, windowSise[1] * 3 / 4 - timerText.get_height() / 2))

        # スコアの描画
        scoreFont = pygame.font.SysFont(self.__setting["font"], int(windowSise[1] * 4 / 10))

        leftTeamText = scoreFont.render(str(self.__leftTeam["score"]), True, (255, 255, 255))
        rightTeamText = scoreFont.render(str(self.__rightTeam["score"]), True, (255, 255, 255))
        self.screen.blit(leftTeamText, (windowSise[0] / 4 - leftTeamText.get_width() / 2, windowSise[1] * 4 / 20 - leftTeamText.get_height() / 2))
        self.screen.blit(rightTeamText, (windowSise[0] * 3 / 4 - rightTeamText.get_width() / 2, windowSise[1] * 4 / 20 - rightTeamText.get_height() / 2))

        # チーム名の描画
        font = pygame.font.SysFont(self.__setting["font"], int(windowSise[1] / 10 - (windowSise[1] / 10) / 4))

        leftTeamName = font.render(self.__leftTeam["name"], True, (255, 255, 255))
        rightTeamName = font.render(self.__rightTeam["name"], True, (255, 255, 255))
        self.screen.blit(leftTeamName, (windowSise[0] / 4 - leftTeamName.get_width() / 2, windowSise[1] * 9 / 20 - leftTeamName.get_height() / 2))
        self.screen.blit(rightTeamName, (windowSise[0] * 3 / 4 - rightTeamName.get_width() / 2, windowSise[1] * 9 / 20 - rightTeamName.get_height() / 2))

        return ""

    # タイマー設定画面
    def timerSetting(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F11:
                        if self.screen.get_flags() & pygame.FULLSCREEN:
                            self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                        else:
                            self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                
                if event.key == K_ESCAPE:
                    return "setting"
                if event.key == K_UP:
                    if self.__cursor["x"] == 0:
                        self.__settingTime["min"] += 10
                    if self.__cursor["x"] == 1:
                        self.__settingTime["min"] += 1
                    if self.__cursor["x"] == 3:
                        self.__settingTime["sec"] += 10
                    if self.__cursor["x"] == 4:
                        self.__settingTime["sec"] += 1
                if event.key == K_DOWN:
                    if self.__cursor["x"] == 0:
                        self.__settingTime["min"] -= 10
                    if self.__cursor["x"] == 1:
                        self.__settingTime["min"] -= 1
                    if self.__cursor["x"] == 3:
                        self.__settingTime["sec"] -= 10
                    if self.__cursor["x"] == 4:
                        self.__settingTime["sec"] -= 1
                if event.key == K_LEFT:
                    self.__cursor["x"] -= 1
                    if self.__cursor["x"] == 2:
                        self.__cursor["x"] -= 1
                if event.key == K_RIGHT:
                    self.__cursor["x"] += 1
                    if self.__cursor["x"] == 2:
                        self.__cursor["x"] += 1
                if event.key == K_RETURN:
                    if self.__cursor["x"] == 6:
                        self.__time = self.__settingTime
                        self.__setting["time"]["min"] = self.__time["min"]
                        self.__setting["time"]["sec"] = self.__time["sec"]
                        self.__setting["timerReverse"] = self.__tmpTimeReverse
                        self.saveSetting()
                        return "setting"
                    if self.__cursor["x"] == 5:
                        self.__tmpTimeReverse = not self.__tmpTimeReverse
        
        if self.__settingTime["min"] < 0:
            self.__settingTime["min"] = 99
        if self.__settingTime["min"] > 99:
            self.__settingTime["min"] = 0
        if self.__settingTime["sec"] < 0:
            self.__settingTime["sec"] = 59
        if self.__settingTime["sec"] > 59:
            self.__settingTime["sec"] = 0
        
                
        if self.__cursor["x"] < 0:
            self.__cursor["x"] = 6
        if self.__cursor["x"] > 6:
            self.__cursor["x"] = 0

        windowSize = pygame.display.get_surface().get_size()

        # 背景の描画
        pygame.draw.rect(self.screen, (255, 255, 255), Rect(0, 0, windowSize[0], windowSize[1]))

        timerFont = pygame.font.Font("font/DSEG7Classic-Bold.ttf", int(windowSize[1] / 2 - windowSize[1] / 5))
        charList = [int(self.__settingTime["min"] / 10), self.__settingTime["min"] % 10, ":", int(self.__settingTime["sec"] / 10), self.__settingTime["sec"] % 10]
        textList = []
        for i in range(len(charList)):
            if i == self.__cursor["x"]:
                text = timerFont.render(str(charList[i]), True, self.__Red)
            else:
                text = timerFont.render(str(charList[i]), True, (0, 0, 0))
            textList.append(text)
            self.screen.blit(text, (windowSize[0] * (i + 2) / 8 - text.get_width() / 2, windowSize[1] / 2 - text.get_height() / 2))
        
        font = pygame.font.SysFont(self.__setting["font"], int(windowSize[1] / 10))
        if self.__cursor["x"] == 6:
            text = font.render("保存", True, (255, 0, 0))
        else:
            text = font.render("保存", True, (0, 0, 0))
        self.screen.blit(text, (windowSize[0] * 3 / 4 - text.get_width() / 2, windowSize[1] * 3 / 4 - text.get_height() / 2))

        reverseText = ""
        if self.__tmpTimeReverse:
            reverseText = "カウントダウン"
        else:
            reverseText = "カウントアップ"

        if self.__cursor["x"] == 5:
            text = font.render(reverseText, True, (255, 0, 0))
        else:
            text = font.render(reverseText, True, (0, 0, 0))
        self.screen.blit(text, (windowSize[0] * 1 / 4 - text.get_width() / 2, windowSize[1] * 3 / 4 - text.get_height() / 2))

        return ""
                
    # チーム名設定画面
    def nameSetting(self):

        return ""

    # キーコンフィグ画面
    def keyConfig(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_F11:
                        if self.screen.get_flags() & pygame.FULLSCREEN:
                            self.screen = pygame.display.set_mode((800, 450), pygame.RESIZABLE)
                        else:
                            self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                
                if event.key == K_ESCAPE:
                    return "setting"
                if event.key == K_UP:
                    self.__cursor["y"] -= 1
                if event.key == K_DOWN:
                    self.__cursor["y"] += 1
                if event.key == K_LEFT:
                    self.__cursor["x"] -= 1
                if event.key == K_RIGHT:
                    self.__cursor["x"] += 1
                if event.key == K_RETURN:
                    return "setting"
                
        if self.__cursor["y"] < 0:
            self.__cursor["y"] = 0
        if self.__cursor["x"] < 0:
            self.__cursor["x"] = 1
        if self.__cursor["x"] > 1:
            self.__cursor["x"] = 0

        # self.__leftKeys = {
        #     "up" : pygame.key.key_code(self.__setting["key"]["left"]["up"]),
        #     "down" : pygame.key.key_code(self.__setting["key"]["left"]["down"]),
        #     "nup" : pygame.key.key_code(self.__setting["key"]["left"]["nup"]),
        #     "ndown" : pygame.key.key_code(self.__setting["key"]["left"]["ndown"]),
        #     "reset" : pygame.key.key_code(self.__setting["key"]["left"]["reset"])
        # }
        # self.__rightKeys = {
        #     "up" : pygame.key.key_code(self.__setting["key"]["right"]["up"]),
        #     "down" : pygame.key.key_code(self.__setting["key"]["right"]["down"]),
        #     "nup" : pygame.key.key_code(self.__setting["key"]["right"]["nup"]),
        #     "ndown" : pygame.key.key_code(self.__setting["key"]["right"]["ndown"]),
        #     "reset" : pygame.key.key_code(self.__setting["key"]["right"]["reset"])
        # }
        # self.__swapKey = pygame.key.key_code(self.__setting["key"]["swap"])


        return ""

# メイン関数
if __name__ == "__main__":
    kyorobo_timer = KyoroboTimer(SETTING_FILE_PATH)
    kyorobo_timer.beepHi = pygame.mixer.Sound("sounds/beepHi.wav")
    kyorobo_timer.beepLo = pygame.mixer.Sound("sounds/beepLo.wav")
    kyorobo_timer.run()
    del kyorobo_timer