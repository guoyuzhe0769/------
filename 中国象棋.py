import pygame
import sys
from PIL import Image, ImageDraw, ImageFont
import os

class 棋子类:
    def __init__(self, 名字, 颜色, 符号, 行, 列):
        self.名字 = 名字
        self.颜色 = 颜色  # 红方或黑方
        self.符号 = 符号
        self.行 = 行
        self.列 = 列

    def is_valid_move(self, 棋盘, 目标行, 目标列):
        pass

class 车(棋子类):
    def is_valid_move(self, 棋盘, 目标行, 目标列):
        if self.行 == 目标行:
            步数 = 目标列 - self.列
            方向 = 1 if 步数 > 0 else -1
            for i in range(1, abs(步数)):
                if 棋盘[self.行][self.列 + i * 方向] is not None:
                    return False
        elif self.列 == 目标列:
            步数 = 目标行 - self.行
            方向 = 1 if 步数 > 0 else -1
            for i in range(1, abs(步数)):
                if 棋盘[self.行 + i * 方向][self.列] is not None:
                    return False
        else:
            return False
        
        return True

class 马(棋子类):
    def is_valid_move(self, 棋盘, 目标行, 目标列):
        行差 = abs(目标行 - self.行)
        列差 = abs(目标列 - self.列)
        
        if (行差 == 1 and 列差 == 2) or (行差 == 2 and 列差 == 1):
            if 行差 == 1:
                中间行 = self.行
                中间列 = (self.列 + 目标列) // 2
            else:
                中间行 = (self.行 + 目标行) // 2
                中间列 = self.列
            
            if 棋盘[中间行][中间列] is None:
                return True
        
        return False

class 相(棋子类):
    def is_valid_move(self, 棋盘, 目标行, 目标列):
        if abs(目标行 - self.行) == 2 and abs(目标列 - self.列) == 2:
            中间行 = (self.行 + 目标行) // 2
            中间列 = (self.列 + 目标列) // 2
            
            if 棋盘[中间行][中间列] is None:
                if (self.颜色 == "红" and 目标行 >= 5) or (self.颜色 == "黑" and 目标行 <= 4):
                    return True
        
        return False

class 仕(棋子类):
    def is_valid_move(self, 棋盘, 目标行, 目标列):
        if abs(目标行 - self.行) == 1 and abs(目标列 - self.列) == 1:
            if (self.颜色 == "红" and 6 <= 目标行 <= 9 and 3 <= 目标列 <= 5) or \
               (self.颜色 == "黑" and 0 <= 目标行 <= 2 and 3 <= 目标列 <= 5):
                return True
        
        return False

class 帅(棋子类):
    def is_valid_move(self, 棋盘, 目标行, 目标列):
        if (abs(目标行 - self.行) + abs(目标列 - self.列) == 1) and \
           ((self.颜色 == "红" and 6 <= 目标行 <= 9 and 3 <= 目标列 <= 5) or \
            (self.颜色 == "黑" and 0 <= 目标行 <= 2 and 3 <= 目标列 <= 5)):
            # 检查是否与对方帅/将处于同一列
            for i in range(self.行 + 1, 10) if self.颜色 == "红" else range(self.行 - 1, -1, -1):
                piece = 棋盘[i][self.列]
                if piece is not None:
                    if isinstance(piece, 帅) and piece.颜色 != self.颜色:
                        return False
                    else:
                        break
            return True
        
        return False

class 炮(棋子类):
    def is_valid_move(self, 棋盘, 目标行, 目标列):
        if self.行 == 目标行:
            步数 = 目标列 - self.列
            方向 = 1 if 步数 > 0 else -1
            跨越棋子数 = 0
            for i in range(1, abs(步数)):
                if 棋盘[self.行][self.列 + i * 方向] is not None:
                    跨越棋子数 += 1
            if (跨越棋子数 == 0 and 棋盘[目标行][目标列] is None) or (跨越棋子数 == 1 and 棋盘[目标行][目标列] is not None):
                return True
        elif self.列 == 目标列:
            步数 = 目标行 - self.行
            方向 = 1 if 步数 > 0 else -1
            跨越棋子数 = 0
            for i in range(1, abs(步数)):
                if 棋盘[self.行 + i * 方向][self.列] is not None:
                    跨越棋子数 += 1
            if (跨越棋子数 == 0 and 棋盘[目标行][目标列] is None) or (跨越棋子数 == 1 and 棋盘[目标行][目标列] is not None):
                return True
        
        return False

class 兵(棋子类):
    def is_valid_move(self, 棋盘, 目标行, 目标列):
        if self.颜色 == "红":
            if self.行 <= 4:  # 未过河
                if 目标行 == self.行 - 1 and 目标列 == self.列:
                    return True
            else:  # 已过河
                if (目标行 == self.行 - 1 and 目标列 == self.列) or \
                   (目标行 == self.行 and abs(目标列 - self.列) == 1):
                    return True
        else:
            if self.行 >= 5:  # 未过河
                if 目标行 == self.行 + 1 and 目标列 == self.列:
                    return True
            else:  # 已过河
                if (目标行 == self.行 + 1 and 目标列 == self.列) or \
                   (目标行 == self.行 and abs(目标列 - self.列) == 1):
                    return True
        
        return False

棋子价值 = {
    "帅": 10000,
    "将": 10000,
    "车": 1000,
    "炮": 500,
    "马": 300,
    "相": 200,
    "象": 200,
    "仕": 200,
    "士": 200,
    "兵": 100,
    "卒": 100
}

class 棋盘类:
    def __init__(self):
        self.棋盘 = [[None for _ in range(9)] for _ in range(10)]
        self.初始化棋盘()
        self.当前回合 = "红"  # 红方先手
        self.人类玩家 = "红"  # 人类玩家控制红方
        self.AI玩家 = "黑"   # AI控制黑方
        
        # macOS 可能的字体路径列表
        可能的字体路径 = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
            "/System/Library/Fonts/华文黑体.ttc",
            "/System/Library/Fonts/华文楷体.ttc",
            "/System/Library/Fonts/华文宋体.ttc"
        ]
        
        # 尝试找到可用的字体
        self.字体路径 = None
        for 路径 in 可能的字体路径:
            if os.path.exists(路径):
                try:
                    ImageFont.truetype(路径, 30)
                    self.字体路径 = 路径
                    print(f"成功加载字体: {路径}")
                    break
                except Exception as e:
                    print(f"尝试加载字体失败 {路径}: {e}")
                    continue
        
        if self.字体路径 is None:
            print("警告: 未找到可用的中文字体，将使用简单图形代替")
    
    def 初始化棋盘(self):
        # 使用Unicode字符
        红方棋子 = {
            (9, 0): 车("车", "红", "車", 9, 0),  # \u8f66
            (9, 1): 马("马", "红", "馬", 9, 1),  # \u9a6c
            (9, 2): 相("相", "红", "相", 9, 2),  # \u76f8
            (9, 3): 仕("仕", "红", "仕", 9, 3),  # \u4ed5
            (9, 4): 帅("帅", "红", "帥", 9, 4),  # \u5e05
            (9, 5): 仕("仕", "红", "仕", 9, 5),
            (9, 6): 相("相", "红", "相", 9, 6),
            (9, 7): 马("马", "红", "馬", 9, 7),
            (9, 8): 车("车", "红", "車", 9, 8),
            (7, 1): 炮("炮", "红", "炮", 7, 1),  # \u70ae
            (7, 7): 炮("炮", "红", "炮", 7, 7),
            (6, 0): 兵("兵", "红", "兵", 6, 0),  # \u5175
            (6, 2): 兵("兵", "红", "兵", 6, 2),
            (6, 4): 兵("兵", "红", "兵", 6, 4),
            (6, 6): 兵("兵", "红", "兵", 6, 6),
            (6, 8): 兵("兵", "红", "兵", 6, 8),
        }
        
        黑方棋子 = {
            (0, 0): 车("车", "黑", "車", 0, 0),
            (0, 1): 马("马", "黑", "馬", 0, 1),
            (0, 2): 相("象", "黑", "象", 0, 2),  # \u8c61
            (0, 3): 仕("士", "黑", "士", 0, 3),  # \u58eb
            (0, 4): 帅("将", "黑", "將", 0, 4),  # \u5c07
            (0, 5): 仕("士", "黑", "士", 0, 5),
            (0, 6): 相("象", "黑", "象", 0, 6),
            (0, 7): 马("马", "黑", "馬", 0, 7),
            (0, 8): 车("车", "黑", "車", 0, 8),
            (2, 1): 炮("炮", "黑", "炮", 2, 1),
            (2, 7): 炮("炮", "黑", "炮", 2, 7),
            (3, 0): 兵("卒", "黑", "卒", 3, 0),  # \u5352
            (3, 2): 兵("卒", "黑", "卒", 3, 2),
            (3, 4): 兵("卒", "黑", "卒", 3, 4),
            (3, 6): 兵("卒", "黑", "卒", 3, 6),
            (3, 8): 兵("卒", "黑", "卒", 3, 8),
        }
        
        # 放置棋子
        for 位置, 棋子 in 红方棋子.items():
            self.棋盘[位置[0]][位置[1]] = 棋子
        for 位置, 棋子 in 黑方棋子.items():
            self.棋盘[位置[0]][位置[1]] = 棋子
    
    def 绘制(self, 屏幕):
        for i in range(10):
            for j in range(9):
                棋子 = self.棋盘[i][j]
                if 棋子 is not None:
                    # 绘制棋子背景
                    pygame.draw.circle(屏幕, (255, 248, 220), (j*60 + 30, i*60 + 30), 25)  # 米色背景
                    pygame.draw.circle(屏幕, (0, 0, 0), (j*60 + 30, i*60 + 30), 25, 2)  # 黑色边框
                    
                    if self.字体路径:
                        try:
                            # 使用PIL创建文字图片
                            字体 = ImageFont.truetype(self.字体路径, 30)
                            img = Image.new('RGBA', (50, 50), (0, 0, 0, 0))
                            draw = ImageDraw.Draw(img)
                            
                            # 设置棋子颜色
                            颜色 = (255, 0, 0) if 棋子.颜色 == "红" else (0, 0, 0)
                            
                            # 获取文字大小
                            bbox = draw.textbbox((0, 0), 棋子.符号, font=字体)
                            文字宽度 = bbox[2] - bbox[0]
                            文字高度 = bbox[3] - bbox[1]
                            
                            # 计算居中位置
                            x = (50 - 文字宽度) // 2
                            y = (50 - 文字高度) // 2
                            
                            # 绘制文字
                            draw.text((x, y), 棋子.符号, 颜色, font=字体)
                            
                            # 转换为Pygame表面
                            文字数据 = img.tobytes()
                            文字表面 = pygame.image.fromstring(文字数据, (50, 50), 'RGBA')
                            
                            # 绘制到屏幕
                            屏幕.blit(文字表面, (j*60 + 5, i*60 + 5))
                        except Exception as e:
                            print(f"渲染棋子 {棋子.符号} 时出错: {e}")
                            # 如果渲染失败，绘制简单的标记
                            颜色 = (255, 0, 0) if 棋子.颜色 == "红" else (0, 0, 0)
                            pygame.draw.circle(屏幕, 颜色, (j*60 + 30, i*60 + 30), 15, 3)
                    else:
                        # 如果没有可用字体，绘制简单的标记
                        颜色 = (255, 0, 0) if 棋子.颜色 == "红" else (0, 0, 0)
                        pygame.draw.circle(屏幕, 颜色, (j*60 + 30, i*60 + 30), 15, 3)
    
    def 获取所有合法移动(self, 颜色):
        合法移动 = []
        for i in range(10):
            for j in range(9):
                棋子 = self.棋盘[i][j]
                if 棋子 is not None and 棋子.颜色 == 颜色:
                    for 目标行 in range(10):
                        for 目标列 in range(9):
                            if 棋子.is_valid_move(self.棋盘, 目标行, 目标列):
                                # 检查目标位置是否有己方棋子
                                目标棋子 = self.棋盘[目标行][目标列]
                                if 目标棋子 is None or 目标棋子.颜色 != 颜色:
                                    合法移动.append((i, j, 目标行, 目标列))
        return 合法移动
    
    def 评估局面(self, 颜色):
        评估值 = 0
        for i in range(10):
            for j in range(9):
                棋子 = self.棋盘[i][j]
                if 棋子 is not None:
                    if 棋子.名字 in 棋子价值:
                        if 棋子.颜色 == 颜色:
                            评估值 += 棋子价值[棋子.名字]
                        else:
                            评估值 -= 棋子价值[棋子.名字]
                    else:
                        print(f"警告: 未知棋子 {棋子.名字}")
        return 评估值
    
    def 极小极大_alpha_beta(self, 深度, 颜色, alpha, beta):
        if 深度 == 0:
            return self.评估局面(颜色)
        
        最佳评估 = float("-inf") if 颜色 == self.AI玩家 else float("inf")
        
        for 起始行, 起始列, 目标行, 目标列 in self.获取所有合法移动(颜色):
            棋子 = self.棋盘[起始行][起始列]
            目标棋子 = self.棋盘[目标行][目标列]
            
            self.棋盘[目标行][目标列] = 棋子
            self.棋盘[起始行][起始列] = None
            
            评估值 = self.极小极大_alpha_beta(深度 - 1, self.人类玩家 if 颜色 == self.AI玩家 else self.AI玩家, alpha, beta)
            
            self.棋盘[起始行][起始列] = 棋子
            self.棋盘[目标行][目标列] = 目标棋子
            
            if 颜色 == self.AI玩家:
                最佳评估 = max(最佳评估, 评估值)
                alpha = max(alpha, 评估值)
                if beta <= alpha:
                    break
            else:
                最佳评估 = min(最佳评估, 评估值)
                beta = min(beta, 评估值)
                if beta <= alpha:
                    break
        
        return 最佳评估
    
    def AI移动(self):
        最佳评估 = float("-inf")
        最佳移动 = None
        
        # 根据游戏阶段调整搜索深度
        搜索深度 = 2
        红方棋子数 = sum(1 for i in range(10) for j in range(9) if self.棋盘[i][j] is not None and self.棋盘[i][j].颜色 == "红")
        黑方棋子数 = sum(1 for i in range(10) for j in range(9) if self.棋盘[i][j] is not None and self.棋盘[i][j].颜色 == "黑")
        总棋子数 = 红方棋子数 + 黑方棋子数
        
        if 总棋子数 <= 8:  # 残局阶段
            搜索深度 = 4
        elif 总棋子数 <= 16:  # 中局阶段
            搜索深度 = 3
        
        for 起始行, 起始列, 目标行, 目标列 in self.获取所有合法移动(self.AI玩家):
            棋子 = self.棋盘[起始行][起始列]
            目标棋子 = self.棋盘[目标行][目标列]
            
            self.棋盘[目标行][目标列] = 棋子
            self.棋盘[起始行][起始列] = None
            
            评估值 = self.极小极大_alpha_beta(搜索深度, self.人类玩家, float("-inf"), float("inf"))
            
            self.棋盘[起始行][起始列] = 棋子
            self.棋盘[目标行][目标列] = 目标棋子
            
            if 评估值 > 最佳评估:
                最佳评估 = 评估值
                最佳移动 = (起始行, 起始列, 目标行, 目标列)
        
        if 最佳移动:
            self.移动棋子(*最佳移动)
            self.当前回合 = self.人类玩家
        else:
            # 如果找不到最佳移动,随机移动一步
            import random
            合法移动 = self.获取所有合法移动(self.AI玩家)
            if 合法移动:
                起始行, 起始列, 目标行, 目标列 = random.choice(合法移动)
                self.移动棋子(起始行, 起始列, 目标行, 目标列)
                self.当前回合 = self.人类玩家
    
    def 移动棋子(self, 起始行, 起始列, 目标行, 目标列):
        if 0 <= 目标行 < 10 and 0 <= 目标列 < 9:
            棋子 = self.棋盘[起始行][起始列]
            if 棋子 is not None and 棋子.is_valid_move(self.棋盘, 目标行, 目标列):
                # 检查是否是当前回合的玩家的棋子
                if 棋子.颜色 == self.当前回合:
                    # 检查目标位置是否有己方棋子
                    目标棋子 = self.棋盘[目标行][目标列]
                    if 目标棋子 is None or 目标棋子.颜色 != 棋子.颜色:
                        self.棋盘[目标行][目标列] = 棋子
                        self.棋盘[起始行][起始列] = None
                        棋子.行 = 目标行
                        棋子.列 = 目标列
                        # 切换回合
                        self.当前回合 = self.AI玩家 if self.当前回合 == self.人类玩家 else self.人类玩家

def 绘制棋盘(屏幕):
    for i in range(10):
        pygame.draw.line(屏幕, (0, 0, 0), (0, i*60), (540, i*60), 2)
    for i in range(9):    
        pygame.draw.line(屏幕, (0, 0, 0), (i*60, 0), (i*60, 600), 2)
        
    # 画九宫格
    pygame.draw.line(屏幕, (0, 0, 0), (180, 0), (360, 180), 2)
    pygame.draw.line(屏幕, (0, 0, 0), (360, 0), (180, 180), 2)
    pygame.draw.line(屏幕, (0, 0, 0), (180, 420), (360, 600), 2)
    pygame.draw.line(屏幕, (0, 0, 0), (360, 420), (180, 600), 2)

def 主程序():
    pygame.init()
    屏幕 = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("中国象棋")
    时钟 = pygame.time.Clock()
    
    游戏棋盘 = 棋盘类()
    选中棋子 = None
    
    while True:
        for 事件 in pygame.event.get():
            if 事件.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif 事件.type == pygame.MOUSEBUTTONDOWN and 游戏棋盘.当前回合 == 游戏棋盘.人类玩家:
                if 选中棋子 is None:
                    x, y = 事件.pos
                    i, j = y // 60, x // 60
                    if 0 <= i < 10 and 0 <= j < 9:
                        棋子 = 游戏棋盘.棋盘[i][j]
                        if 棋子 is not None and 棋子.颜色 == 游戏棋盘.人类玩家:
                            选中棋子 = 棋子
                else:
                    x, y = 事件.pos
                    i, j = y // 60, x // 60
                    游戏棋盘.移动棋子(选中棋子.行, 选中棋子.列, i, j)
                    选中棋子 = None
        
        # AI回合
        if 游戏棋盘.当前回合 == 游戏棋盘.AI玩家:
            游戏棋盘.AI移动()
        
        屏幕.fill((139, 69, 19))  # 棋盘背景色
        绘制棋盘(屏幕)
        游戏棋盘.绘制(屏幕)
        
        pygame.display.flip()
        时钟.tick(60)

if __name__ == "__main__":
    主程序() 