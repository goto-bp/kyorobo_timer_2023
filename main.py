import pygame
from pygame.locals import *
import json
import sys
import random
import pygame._sdl2 as sdl2

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

    __changeColor = 1

    __swap = False

    __cursor = {"x" : 0, "y" : 0}

    __settingFilePath = ""

    __loadFlag = 0

    # x,y,方向,色,速度,半径
    __circleList = []


    __colorList = [(147, 247, 255), (255, 249, 132), (187, 180, 250), (200, 255, 200), (255, 199, 94)]      

    beepHi = None
    beepLo = None

    forcusWindow = "main"

    subFunctionIndex = 0
    subReloadFile = 0
    subChangeSwap = 0

    isShowSetting = True

    tmpScoreSetting = 0

    fullscreenFlag = False

    showCircle = False

    redTeamNameIndex = 0
    blueTeamNameIndex = 0
    redTeamNameList = []
    blueTeamNameList = []

    # イベントの共通部分
    def windowEvent(self, event):
        if event.type == QUIT:
            sys.exit()
        if getattr(event, "window", None) == self.settingWindow:
                if event.type == WINDOWCLOSE:
                    self.settingWindow.hide()
                    self.isShowSetting = False
                if event.type == WINDOWFOCUSGAINED:
                    self.forcusWindow = "sub"
        elif getattr(event, "window", None) == self.mainWindow:
                if event.type == WINDOWCLOSE:
                    sys.exit()
                if event.type == WINDOWFOCUSGAINED:
                    self.forcusWindow = "main"
        if self.forcusWindow == "main":
            if event.type == KEYDOWN:
                if event.key == K_F11:
                    if self.fullscreenFlag:
                        self.mainWindow.set_windowed()
                        self.fullscreenFlag = False
                    else:
                        self.mainWindow.set_fullscreen(True)
                        self.fullscreenFlag = True
                    
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

        self.__swap = self.__setting["isSwap"]

        self.__time["min"] = self.__setting["time"]["min"]
        self.__time["sec"] = self.__setting["time"]["sec"]
        if self.__swap:
            self.__leftTeam["name"] = self.__setting["redTeam"]
            self.__rightTeam["name"] = self.__setting["blueTeam"]
        else:
            self.__leftTeam["name"] = self.__setting["blueTeam"]
            self.__rightTeam["name"] = self.__setting["redTeam"]

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

        self.redTeamNameList = [self.__setting["redTeam"]] + self.__setting["teamNameList"]
        self.blueTeamNameList = [self.__setting["blueTeam"]] + self.__setting["teamNameList"]

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
        for i in range(1,10):
            for j in range(len(self.__colorList)):
                # print(self.__colorList[j][0] + i, self.__colorList[j][1] + i, self.__colorList[j][2] + i)
                self.__colorList.append(
                    (255 if self.__colorList[j][0] + i > 255 else self.__colorList[j][0] + i,
                    255 if self.__colorList[j][1] + i > 255 else self.__colorList[j][1] + i,
                    255 if self.__colorList[j][2] + i > 255 else self.__colorList[j][2] + i)
                )
            

        pygame.init()
        self.__settingFilePath = setting_file_path

        self.loadSetting()

        self.screen = pygame.Surface((800, 450))

        self.mainWindow = sdl2.Window("共ロボタイマー", size=(800, 450), resizable=True)
        self.mainRenderer = sdl2.Renderer(self.mainWindow)

        self.settingWindow = sdl2.Window("設定", size=(400, 225), resizable=True)
        self.settingRenderer = sdl2.Renderer(self.settingWindow)
        self.isShowSetting = False
        self.settingWindow.hide()
        self.settingRenderer.draw_color = (255, 255, 255, 255)

        # アイコンの読み込み
        try:
            self.__icon = pygame.image.load("img/icon.png")
            self.mainWindow.set_icon(self.__icon)
            self.settingWindow.set_icon(self.__icon)
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

    # デストラクタ
    def __del__(self):
        pygame.quit()

    # メインループ
    def run(self):
        nowFunction = self.title
        
        while True:
            self.mainRenderer.clear()
            
            code = nowFunction()

            if code == "exit":
                nowFunction = self.title
                self.__time["min"] = self.__setting["time"]["min"]
                self.__time["sec"] = self.__setting["time"]["sec"]
                self.__leftTeam["score"] = 0
                self.__rightTeam["score"] = 0
                if self.isShowSetting:
                    self.settingWindow.show()
            elif code == "timer":
                nowFunction = self.timer
            elif code == "countdown":
                nowFunction = self.countdown
                self.__setTime["min"] = self.__time["min"]
                self.__setTime["sec"] = self.__time["sec"]
                pygame.time.set_timer(USEREVENT, 1000)
                self.__count = 5
            elif code == "ready":
                nowFunction = self.ready

            tex = sdl2.Texture.from_surface(self.mainRenderer, self.screen)
            tex.draw()
            self.mainRenderer.present()

            pygame.time.wait(30)

    # タイトル画面
    def title(self):

        settingElem = ["チーム名", "時間設定", "一度に増やすスコア", "左右入れ替え", "キーコンフィグ", "設定ファイルの再読み込み", "プレビュー"]

        for event in pygame.event.get():
            
            self.windowEvent(event)

            if self.forcusWindow == "main":
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        sys.exit()
                    if event.key == K_F5:
                        self.loadSetting()
                        self.__changeColor = 2
                    if event.key == K_1:
                        self.__setting["time"]["min"] = 2
                        self.__setting["time"]["sec"] = 30
                        self.__time["min"] = 2
                        self.__time["sec"] = 30
                        self.saveSetting()
                        self.__changeColor = 2
                    if event.key == K_2:
                        self.__setting["time"]["min"] = 5
                        self.__setting["time"]["sec"] = 0
                        self.__time["min"] = 5
                        self.__time["sec"] = 0
                        self.saveSetting()
                        self.__changeColor = 2
                    if event.key == K_RETURN:
                        self.settingWindow.hide()
                        return "ready"
                    if event.key == K_SPACE:
                        self.settingWindow.hide()
                        return "countdown"
                    if event.key == K_RSHIFT or event.key == K_LSHIFT:
                        if not self.isShowSetting:
                            self.settingWindow.show()
                            self.isShowSetting = True
            elif self.forcusWindow == "sub":
                if event.type == KEYDOWN:
                    if self.subFunctionIndex == 0:
                        if event.key == K_ESCAPE:
                            self.settingWindow.hide()
                            self.isShowSetting = False
                        if event.key == K_UP:
                            self.__cursor["y"] -= 1
                        if event.key == K_DOWN:
                            self.__cursor["y"] += 1
                        if event.key == K_RETURN:  
                            if self.__cursor["y"] == 0:
                                self.subFunctionIndex = 2
                            elif self.__cursor["y"] == 1:
                                self.subFunctionIndex = 1
                                self.__tmpTimeReverse = self.__setting["timerReverse"]
                                self.__settingTime["min"] = self.__time["min"]
                                self.__settingTime["sec"] = self.__time["sec"]
                                self.__cursor["y"] = 0
                                self.__cursor["x"] = 0
                            elif self.__cursor["y"] == 2:
                                self.tmpScoreSetting = self.__setting["score"]
                                self.subFunctionIndex = 3
                            elif self.__cursor["y"] == 3:
                                self.__setting["isSwap"] = not self.__setting["isSwap"]
                                self.__swap = self.__setting["isSwap"]
                                self.__rightTeam["name"], self.__leftTeam["name"] = self.__leftTeam["name"], self.__rightTeam["name"]
                                self.saveSetting()
                                self.subChangeSwap = 20
                            elif self.__cursor["y"] == 5:
                                self.loadSetting()
                                self.subReloadFile = 20                        
                            elif self.__cursor["y"] == 6:
                                self.__setTime["min"] = self.__time["min"]
                                self.__setTime["sec"] = self.__time["sec"]
                                self.subFunctionIndex = 4
                            else:
                                self.beepLo.play()
                    elif self.subFunctionIndex == 1:
                        if event.key == K_ESCAPE:
                            self.subFunctionIndex = 0
                            self.__cursor["y"] = 0
                            self.__cursor["x"] = 0
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
                                self.__cursor["y"] = 0
                                self.__cursor["x"] = 0
                                self.subFunctionIndex = 0
                            if self.__cursor["x"] == 5:
                                self.__tmpTimeReverse = not self.__tmpTimeReverse
                    elif self.subFunctionIndex == 2:
                        if event.key == K_ESCAPE:
                            self.subFunctionIndex = 0
                        if event.key == K_UP:
                            self.blueTeamNameIndex -= 1
                        if event.key == K_DOWN:
                            self.blueTeamNameIndex += 1
                        if event.key == K_w:
                            self.redTeamNameIndex -= 1
                        if event.key == K_s:
                            self.redTeamNameIndex += 1
                        if event.key == K_RETURN:
                            self.__setting["redTeam"] = self.redTeamNameList[self.redTeamNameIndex]
                            self.__setting["blueTeam"] = self.blueTeamNameList[self.blueTeamNameIndex]
                            self.__leftTeam["name"] = self.__setting["redTeam"]
                            self.__rightTeam["name"] = self.__setting["blueTeam"]
                            self.saveSetting()
                            self.subFunctionIndex = 0
                    elif self.subFunctionIndex == 3:
                        if event.key == K_ESCAPE:
                            self.subFunctionIndex = 0
                            self.__cursor["y"] = 0
                            self.__cursor["x"] = 0
                        if event.key == K_UP:
                            self.__cursor["x"] -= 1
                        if event.key == K_DOWN:
                            self.__cursor["x"] += 1
                        if self.__cursor["x"] == 0:
                            if event.key == K_RIGHT:
                                self.tmpScoreSetting += 1
                            if event.key == K_LEFT:
                                self.tmpScoreSetting -= 1
                        else:
                            if event.key == K_RETURN:
                                self.__setting["score"] = self.tmpScoreSetting
                                self.saveSetting()
                                self.subFunctionIndex = 0
                                self.__cursor["y"] = 0
                                self.__cursor["x"] = 0
                                self.tmpScoreSetting = 0
                    elif self.subFunctionIndex == 4:
                        if event.key == K_ESCAPE:
                            self.__time["min"] = self.__setting["time"]["min"]
                            self.__time["sec"] = self.__setting["time"]["sec"]
                            self.__leftTeam["score"] = 0
                            self.__rightTeam["score"] = 0
                            self.subFunctionIndex = 0
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

        if self.subFunctionIndex == 0:
            if self.__cursor["y"] < 0:
                self.__cursor["y"] = len(settingElem) - 1
            if self.__cursor["y"] > len(settingElem) - 1:
                self.__cursor["y"] = 0
        elif self.subFunctionIndex == 1:
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
        elif self.subFunctionIndex == 2:
            if self.redTeamNameIndex < 0:
                self.redTeamNameIndex = len(self.redTeamNameList) - 1
            if self.redTeamNameIndex > len(self.redTeamNameList) - 1:
                self.redTeamNameIndex = 0
            if self.blueTeamNameIndex < 0:
                self.blueTeamNameIndex = len(self.blueTeamNameList) - 1
            if self.blueTeamNameIndex > len(self.blueTeamNameList) - 1:
                self.blueTeamNameIndex = 0
        elif self.subFunctionIndex == 3:
            if self.tmpScoreSetting < 0:
                self.tmpScoreSetting = 0
            if self.__cursor["x"] < 0:
                self.__cursor["x"] = 1
            if self.__cursor["x"] > 1:
                self.__cursor["x"] = 0
        elif self.subFunctionIndex == 4:
            if(self.__leftTeam["score"] < 0):
                self.__leftTeam["score"] = 0
            if(self.__rightTeam["score"] < 0):
                self.__rightTeam["score"] = 0

        windowsize = self.mainWindow.size
        self.screen = pygame.Surface(windowsize)


        # 背景の描画
        pygame.draw.rect(self.screen, (255, 255, 255), Rect(0, 0, windowsize[0], windowsize[1]))

        if self.showCircle:
            if random.random() < 0.05 and len(self.__circleList) < 30:
                x = random.random()
                radius = random.uniform(0.5, 1)
                speed = random.uniform(0.005 / 10, 0.015 / 4)
                if random.random() < 0.5:
                    self.__circleList.append((x, 0 - radius / 5, True, self.__colorList[random.randint(0, len(self.__colorList) - 1)], speed, radius))
                else:
                    self.__circleList.append((x, 1 + radius / 5, False, self.__colorList[random.randint(0, len(self.__colorList) - 1)], speed, radius))
                
            destIndex = []
            newCircleList = []

            for i in range(len(self.__circleList)):
                if self.__circleList[i][2]:
                    self.__circleList[i] = (self.__circleList[i][0], self.__circleList[i][1] + self.__circleList[i][4], True, self.__circleList[i][3], self.__circleList[i][4], self.__circleList[i][5])
                else:
                    self.__circleList[i] = (self.__circleList[i][0], self.__circleList[i][1] - self.__circleList[i][4], False, self.__circleList[i][3], self.__circleList[i][4], self.__circleList[i][5])

                if self.__circleList[i][1] < 0 - self.__circleList[i][5] / 5 or self.__circleList[i][1] > 1 + self.__circleList[i][5] / 5:
                    destIndex.append(i)
                else:
                    fixColor = (255 if self.__circleList[i][3][0] * self.__changeColor > 255 else self.__circleList[i][3][0] * self.__changeColor,
                                255 if self.__circleList[i][3][1] * self.__changeColor > 255 else self.__circleList[i][3][1] * self.__changeColor,
                                255 if self.__circleList[i][3][2] * self.__changeColor > 255 else self.__circleList[i][3][2] * self.__changeColor)
                    

                    pygame.draw.circle(self.screen, fixColor, (self.__circleList[i][0] * windowsize[0], self.__circleList[i][1] * windowsize[1]), int(windowsize[0] * self.__circleList[i][5] / 10) )
                    newCircleList.append(self.__circleList[i])
            self.__circleList = newCircleList

        if self.__changeColor > 1:
            self.__changeColor -= 0.1

        logoScale = (windowsize[1] / 4) / self.__logo.get_height()

        showLogo = pygame.transform.scale(self.__logo, (int(self.__logo.get_width() * logoScale), int(self.__logo.get_height() * logoScale)))

        self.screen.blit(showLogo, (windowsize[0] / 2 - showLogo.get_width() / 2, windowsize[1] / 2 - showLogo.get_height() / 2))    

        
        def subSetting():
            subWindowsize = self.settingWindow.size
            
            textureList = []
            for i in range(len(settingElem)):
                font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / (10 + len(settingElem))))
                text = font.render(settingElem[i], True, (0, 0, 0))
                text = sdl2.Texture.from_surface(self.settingRenderer, text)
                textureList.append(text)
                text.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - text.get_rect().width / 2, subWindowsize[1]* (i + 1.5) / (len(settingElem) + 2)  - text.get_rect().height / 2, text.get_rect().width, text.get_rect().height))

            settingSurface = self.settingRenderer.to_surface()
            pygame.draw.rect(settingSurface, self.__Red, Rect(subWindowsize[0] / 2 - textureList[self.__cursor["y"]].get_rect().width / 2 - 10, subWindowsize[1]* (self.__cursor["y"] + 1.5) / (len(settingElem) + 2) - textureList[self.__cursor["y"]].get_rect().height / 2, textureList[self.__cursor["y"]].get_rect().width + 20, textureList[self.__cursor["y"]].get_rect().height), 2)
            tex = sdl2.Texture.from_surface(self.settingRenderer, settingSurface)
            tex.draw()

            if self.subReloadFile > 0:
                self.subReloadFile -= 1
                font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
                text = font.render("設定を再読み込みしました。", True, (255,0,0))
                text = sdl2.Texture.from_surface(self.settingRenderer, text)
                text.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - text.get_rect().width / 2, subWindowsize[1] / 2 - text.get_rect().height / 2, text.get_rect().width, text.get_rect().height))

            if self.subChangeSwap > 0:
                self.subChangeSwap -= 1

                pygame.draw.rect(settingSurface, (255, 255, 255), Rect(subWindowsize[0] / 5, subWindowsize[1] / 5, 
                                                                       subWindowsize[0] * 4 / 5, subWindowsize[1] * 4 / 5))
                tex = sdl2.Texture.from_surface(self.settingRenderer, settingSurface)
                tex.draw()

                text = ""
                font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
                if not self.__setting["isSwap"]:
                    orginText = "左:青　 右:赤"
                    orginText = font.render(orginText, True, (0,0,255))
                    orginText = sdl2.Texture.from_surface(self.settingRenderer, orginText)
                    text1 = "左:"
                    text1 = font.render(text1, True, (255,0,0))
                    text1 = sdl2.Texture.from_surface(self.settingRenderer, text1)
                    text1.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - orginText.get_rect().width / 2,
                                                  subWindowsize[1] / 2 - text1.get_rect().height / 2,
                                                  text1.get_rect().width, text1.get_rect().height))
                    
                    
                    text2 = "青"
                    text2 = font.render(text2, True, (0,0,255))
                    text2 = sdl2.Texture.from_surface(self.settingRenderer, text2)
                    text2.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - orginText.get_rect().width / 2 + text1.get_rect().width,
                                                  subWindowsize[1] / 2 - text2.get_rect().height / 2,
                                                  text2.get_rect().width, text2.get_rect().height))

                    text3 = "　右:赤"
                    text3 = font.render(text3, True, (255,0,0))
                    text3 = sdl2.Texture.from_surface(self.settingRenderer, text3)
                    text3.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - orginText.get_rect().width / 2 + text1.get_rect().width + text2.get_rect().width,
                                                   subWindowsize[1] / 2 - text3.get_rect().height / 2,
                                                   text3.get_rect().width, text3.get_rect().height))
                else:
                    orginText = "左:赤　右:青"
                    orginText = font.render(orginText, True, (255,0,0))
                    orginText = sdl2.Texture.from_surface(self.settingRenderer, orginText)

                    text1 = "左:赤　 右:"
                    text1 = font.render(text1, True, (255,0,0))
                    text1 = sdl2.Texture.from_surface(self.settingRenderer, text1)
                    text1.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - orginText.get_rect().width / 2,
                                                    subWindowsize[1] / 2 - text1.get_rect().height / 2,
                                                    text1.get_rect().width, text1.get_rect().height))
                    
                    text2 = "青"
                    text2 = font.render(text2, True, (0,0,255))
                    text2 = sdl2.Texture.from_surface(self.settingRenderer, text2)
                    text2.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - orginText.get_rect().width / 2 + text1.get_rect().width,
                                                    subWindowsize[1] / 2 - text2.get_rect().height / 2,
                                                    text2.get_rect().width, text2.get_rect().height))
                

                text = "に変更しました"
                text = font.render(text, True, (255,0,0))
                text = sdl2.Texture.from_surface(self.settingRenderer, text)
                text.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - text.get_rect().width / 2, subWindowsize[1] / 2 + text.get_rect().height / 2, text.get_rect().width, text.get_rect().height))

        def subTimerSetting():
            subWindowsize = self.settingWindow.size

            timerFont = pygame.font.Font("font/DSEG7Classic-Bold.ttf", int(subWindowsize[1] / 2 - subWindowsize[1] / 5))
            charList = [int(self.__settingTime["min"] / 10), self.__settingTime["min"] % 10, ":", int(self.__settingTime["sec"] / 10), self.__settingTime["sec"] % 10]
            textList = []
            for i in range(len(charList)):
                if i == self.__cursor["x"]:
                    text = timerFont.render(str(charList[i]), True, (255, 0, 0))
                else:
                    text = timerFont.render(str(charList[i]), True, (0, 0, 0))
                textList.append(text)
                text = sdl2.Texture.from_surface(self.settingRenderer, text)
                text.draw(dstrect=pygame.Rect(subWindowsize[0] * i / 8 + subWindowsize[0] * 3 / 16,
                                              subWindowsize[1] / 2 - text.get_rect().height / 2,
                                              text.get_rect().width,
                                              text.get_rect().height))
                
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
            if self.__cursor["x"] == 6:
                text = font.render("保存", True, (255, 0, 0))
            else:
                text = font.render("保存", True, (0, 0, 0))
            text = sdl2.Texture.from_surface(self.settingRenderer, text)
            text.draw(dstrect=pygame.Rect(subWindowsize[0] * 3 / 4 - text.get_rect().width / 3,
                                          subWindowsize[1] * 3 / 4 - text.get_rect().height / 2,
                                          text.get_rect().width, text.get_rect().height))
            
            reverseText = ""
            if self.__tmpTimeReverse:
                reverseText = "カウントダウン"
            else:
                reverseText = "カウントアップ"

            if self.__cursor["x"] == 5:
                text = font.render(reverseText, True, (255, 0, 0))
            else:
                text = font.render(reverseText, True, (0, 0, 0))
            text = sdl2.Texture.from_surface(self.settingRenderer, text)
            text.draw(dstrect=pygame.Rect(subWindowsize[0] / 4 - text.get_rect().width / 3,
                                          subWindowsize[1] * 3 / 4 - text.get_rect().height / 2,
                                          text.get_rect().width, text.get_rect().height))

        def subTeamNameSetting():

            subWindowsize = self.settingWindow.size 
            subScreen = pygame.Surface(subWindowsize)

            subScreen.fill((255, 255, 255))

            text = "赤チーム"
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
            text = font.render(text, True, (0,0,0))
            subScreen.blit(text, (subWindowsize[0] * 2 / 7 - text.get_rect().width / 2, subWindowsize[1] / 6 - text.get_rect().height / 2))

            text = "青チーム"
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
            text = font.render(text, True, (0,0,0))
            subScreen.blit(text, (subWindowsize[0] * 5 / 7 - text.get_rect().width / 2, subWindowsize[1] / 6 - text.get_rect().height / 2))

            text = self.redTeamNameList[self.redTeamNameIndex]
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
            text = font.render(text, True, (0,0,0))
            subScreen.blit(text, (subWindowsize[0] * 2 / 7 - text.get_rect().width / 2, subWindowsize[1] * 3 / 6 - text.get_rect().height / 2))

            text = self.blueTeamNameList[self.blueTeamNameIndex]
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
            text = font.render(text, True, (0,0,0))
            subScreen.blit(text, (subWindowsize[0] * 5 / 7 - text.get_rect().width / 2, subWindowsize[1] * 3 / 6 - text.get_rect().height / 2))

            text = "保存"
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
            text = font.render(text, True, (0,0,0))
            subScreen.blit(text, (subWindowsize[0] / 2 - text.get_rect().width / 2, subWindowsize[1] * 5 / 6 - text.get_rect().height / 2))

            pygame.draw.rect(subScreen, (0, 0, 0), Rect(subWindowsize[0] / 2 - text.get_rect().width / 2 - 10, subWindowsize[1] * 5 / 6 - text.get_rect().height / 2 - 10, text.get_rect().width + 20, text.get_rect().height + 20), 2)

            tex = sdl2.Texture.from_surface(self.settingRenderer, subScreen)
            tex.draw()

        def subScoreSetting():
            subWindowsize = self.settingWindow.size

            text = "一度に増やすスコア"
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
            text = font.render(text, True, (0,0,0))
            text = sdl2.Texture.from_surface(self.settingRenderer, text)
            text.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - text.get_rect().width / 2,
                                          text.get_rect().height,
                                          text.get_rect().width, text.get_rect().height))
            
            text = str(self.tmpScoreSetting)
            font = pygame.font.Font("font/DSEG7Classic-Bold.ttf", int(subWindowsize[1] / 6))
            if self.__cursor["x"] == 0:
                text = font.render(text, True, (255,0,0))
            else:
                text = font.render(text, True, (0,0,0))
            text = sdl2.Texture.from_surface(self.settingRenderer, text)
            text.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - text.get_rect().width / 2,
                                            subWindowsize[1] / 2 - text.get_rect().height / 2,
                                            text.get_rect().width, text.get_rect().height))

            text = "保存"
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10))
            if self.__cursor["x"] == 1:
                text = font.render(text, True, (255,0,0))
            else:
                text = font.render(text, True, (0,0,0))
            text = sdl2.Texture.from_surface(self.settingRenderer, text)
            text.draw(dstrect=pygame.Rect(subWindowsize[0] / 2 - text.get_rect().width / 2,
                                            subWindowsize[1] / 2 + text.get_rect().height,
                                            text.get_rect().width, text.get_rect().height))
            
            settingSurface = self.settingRenderer.to_surface()

            if self.__cursor["x"] == 0:
                polygonColor = (255,0,0)
            else:
                polygonColor = (0,0,0)

            pygame.draw.polygon(settingSurface, polygonColor, [  (subWindowsize[0] / 2 - subWindowsize[0] / 10, subWindowsize[1] / 2),
                                                            (subWindowsize[0] / 2 - subWindowsize[0] / 20 , subWindowsize[1] / 2  - subWindowsize[0] / 40),
                                                            (subWindowsize[0] / 2 - subWindowsize[0] / 20 , subWindowsize[1] / 2  + subWindowsize[0] / 40)])
            pygame.draw.polygon(settingSurface, polygonColor, [  (subWindowsize[0] / 2 + subWindowsize[0] / 10, subWindowsize[1] / 2),
                                                            (subWindowsize[0] / 2 + subWindowsize[0] / 20 , subWindowsize[1] / 2  - subWindowsize[0] / 40),
                                                            (subWindowsize[0] / 2 + subWindowsize[0] / 20 , subWindowsize[1] / 2  + subWindowsize[0] / 40)])
            tex = sdl2.Texture.from_surface(self.settingRenderer, settingSurface)
            tex.draw()

        def subPreview():
            subWindowsize = self.settingWindow.size
            subScreen = pygame.Surface(subWindowsize)

            if(self.__leftTeam["score"] < 0):
                self.__leftTeam["score"] = 0
            if(self.__rightTeam["score"] < 0):
                self.__rightTeam["score"] = 0

            # 背景の描画
            pygame.draw.rect(subScreen, (0, 0, 0), Rect(0, 0, subWindowsize[0], subWindowsize[1]))

            if self.__swap:
                leftColor = self.__Red
                rightColor = self.__Blue
            else:
                leftColor = self.__Blue
                rightColor = self.__Red

            pygame.draw.rect(subScreen, leftColor, Rect(0, 0, subWindowsize[0] / 2, subWindowsize[1] * 4 / 10))
            pygame.draw.rect(subScreen, rightColor, Rect(subWindowsize[0] / 2, 0, subWindowsize[0] / 2, subWindowsize[1] * 4 / 10))
            pygame.draw.rect(subScreen, (20, 20, 20), Rect(0, subWindowsize[1] * 4 / 10, subWindowsize[0], subWindowsize[1] / 10))

            # タイマーの描画
            if not self.__setting["timerReverse"]:
                now = self.__time["min"] * 60 + self.__time["sec"]
                first = self.__setTime["min"] * 60 + self.__setTime["sec"]
                min = int((first - now) / 60)
                sec = int((first - now) % 60)
                time = str(min) + ":" + str(sec).zfill(2)
            else:
                time = str(self.__time["min"]) + ":" + str(self.__time["sec"]).zfill(2)
            # timerFont = pygame.font.Font(object(self.__timerFontObject), int(subWindowsize[1] / 2 - subWindowsize[1] / 10))
            timerFont = pygame.font.Font("font/DSEG7Classic-Bold.ttf", int(subWindowsize[1] / 2 - subWindowsize[1] / 10))

            if self.__time["min"] == 0 and self.__time["sec"] == 0:
                timerText = timerFont.render(time, True, self.__Red)
            else:
                timerText = timerFont.render(time, True, (255, 255, 255))
            subScreen.blit(timerText, (subWindowsize[0] / 2 - timerText.get_width() / 2, subWindowsize[1] * 3 / 4 - timerText.get_height() / 2))

            # スコアの描画
            scoreFont = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] * 4 / 10))

            leftTeamText = scoreFont.render(str(self.__leftTeam["score"]), True, (255, 255, 255))
            rightTeamText = scoreFont.render(str(self.__rightTeam["score"]), True, (255, 255, 255))
            subScreen.blit(leftTeamText, (subWindowsize[0] / 4 - leftTeamText.get_width() / 2, subWindowsize[1] * 4 / 20 - leftTeamText.get_height() / 2))
            subScreen.blit(rightTeamText, (subWindowsize[0] * 3 / 4 - rightTeamText.get_width() / 2, subWindowsize[1] * 4 / 20 - rightTeamText.get_height() / 2))

            # チーム名の描画
            font = pygame.font.SysFont(self.__setting["font"], int(subWindowsize[1] / 10 - (subWindowsize[1] / 10) / 4))

            leftTeamName = font.render(self.__leftTeam["name"], True, (255, 255, 255))
            rightTeamName = font.render(self.__rightTeam["name"], True, (255, 255, 255))

            if leftTeamName.get_width() > subWindowsize[0] / 2:
                leftTeamName = pygame.transform.scale(leftTeamName, (int(subWindowsize[0] / 2), int(leftTeamName.get_height() * (subWindowsize[0] / 2) / leftTeamName.get_width())))
            if rightTeamName.get_width() > subWindowsize[0] / 2:
                rightTeamName = pygame.transform.scale(rightTeamName, (int(subWindowsize[0] / 2), int(rightTeamName.get_height() * (subWindowsize[0] / 2) / rightTeamName.get_width())))

            subScreen.blit(leftTeamName, (subWindowsize[0] / 4 - leftTeamName.get_width() / 2, subWindowsize[1] * 9 / 20 - leftTeamName.get_height() / 2))
            subScreen.blit(rightTeamName, (subWindowsize[0] * 3 / 4 - rightTeamName.get_width() / 2, subWindowsize[1] * 9 / 20 - rightTeamName.get_height() / 2))

            tex = sdl2.Texture.from_surface(self.settingRenderer, subScreen)
            tex.draw()

        subFunctionList = [subSetting, subTimerSetting, subTeamNameSetting, subScoreSetting, subPreview]

        self.settingRenderer.clear()
        subFunctionList[self.subFunctionIndex]()
        self.settingRenderer.present()

        return ""

    # レディ画面
    def ready(self):
        for event in pygame.event.get():
            
            self.windowEvent(event)
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "exit"
                if event.key == K_RETURN:
                    return "countdown"
                
        windowsize = self.mainWindow.size
        self.screen = pygame.Surface(windowsize)

        # 背景の描画
        pygame.draw.rect(self.screen, (0, 0, 0), Rect(0, 0, windowsize[0], windowsize[1]))

        font = pygame.font.Font("font/DigitalNormal-xO6j.otf", int(windowsize[1] / 2))
        text = font.render("READY", True, (255, 255, 255))
        self.screen.blit(text, (windowsize[0] / 2 - text.get_width() / 2, windowsize[1] / 2 - text.get_height() / 2))
        return ""

    # カウントダウン画面
    def countdown(self):

        for event in pygame.event.get():

            self.windowEvent(event)

            if event.type == USEREVENT:
                self.__count -= 1
                if self.__count == -1:
                    self.__time["sec"] -= 1
                    return "timer"
                elif self.__count == 0:
                    self.beepHi.play()
                elif self.__count <= 3:
                    self.beepLo.play()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.time.set_timer(USEREVENT, 0)
                    return "exit"
                
            windowsize = self.mainWindow.size
            self.screen = pygame.Surface(windowsize)

            # 背景の描画
            pygame.draw.rect(self.screen, (0, 0, 0), Rect(0, 0, windowsize[0], windowsize[1]))

            # カウントダウンの描画
            if self.__count == 0:
                font = pygame.font.Font("font/DigitalNormal-xO6j.otf", int(windowsize[1] / 2))
                text = font.render("START", True, (255, 255, 255))
            else:
                font = pygame.font.Font("font/DSEG7Classic-Bold.ttf", int(windowsize[1] / 1.5 - windowsize[1] / 10))
                text = font.render(str(self.__count), True, (255, 255, 255))
            self.screen.blit(text, (windowsize[0] / 2 - text.get_width() / 2, windowsize[1] / 2 - text.get_height() / 2))

            
        return ""

    # タイマー画面
    def timer(self):
        for event in pygame.event.get():

            self.windowEvent(event)

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

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.time.set_timer(USEREVENT, 0)
                    return "exit"

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

        windowSise = self.mainWindow.size
        self.screen = pygame.Surface(windowSise)

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
            time = str(min) + ":" + str(sec).zfill(2)
        else:
            time = str(self.__time["min"]) + ":" + str(self.__time["sec"]).zfill(2)
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

# メイン関数
if __name__ == "__main__":
    kyorobo_timer = KyoroboTimer(SETTING_FILE_PATH)
    kyorobo_timer.run()
    del kyorobo_timer