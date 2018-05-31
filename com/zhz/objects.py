import pygame
import config
import os
from random import randrange


class SquishSprite(pygame.sprite.Sprite):
    """
    游戏Squish所有精灵(sprite)的超类.构造函数加载一副图像，
    设置精灵的外接矩形和移动范围。移动范围取决于屏幕尺寸和边距
    """
    def __init__(self, image):
        super().__init__()
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        shrink = -config.margin * 2
        self.area = screen.get_rect().inflate(shrink, shrink)


class Weight(SquishSprite):
    """
    从天而降的铅锤。它使用SquishSprite的构造函数来设置表示铅锤的图像,
    并以其构造函数的一个参数指定的速度下降
    """
    def __init__(self, speed):
        super().__init__(config.weight_image)
        self.speed = speed
        self.reset()

    def reset(self):
        """
        将铅锤移动到屏幕顶端，使其刚好看不到），并放在一个随机的水平位置
        :return:
        """
        x = randrange(self.area.left, self.area.right)
        self.rect.midbottom = x, 0

    def update(self):
        """
        根据铅锤的速度垂直向下移动相应的距离，同时，
        根据铅锤是否已到达屏幕底部相应地设置属性landed
        :return:
        """
        self.rect.top += self.speed
        self.landed = self.rect.top >= self.area.bottom


class Banana(SquishSprite):
    """
    绝望的香蕉，它使用SquishSprite的构造函数来设置香蕉图像，
    并停留在屏幕底部附近，且水平位置由鼠标的当前位置决定（有一定的限制)
    """
    def __init__(self):
        super().__init__(config.banana_image)
        self.rect.bottom = self.area.bottom
        # 这些内边距表示图像中不属于香蕉的部分
        # 如果铅锤进入了这些区域，并不认为它砸到了香蕉:

        self.pad_top = config.banana_pad_top
        self.pad_side = config.banana_pad_size

    def update(self):
        """
        将香蕉中心的x坐标设置为鼠标当前的x坐标，
        再使用矩形的方法clamp确保香蕉位于允许移动的范围内
        :return:
        """
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect = self.rect.clamp(self.area)

    def touches(self, other):
        """
        判断香蕉是否与另一个精灵（如铅锤）发生了碰撞。
        这里没有直接使用矩形的方法colliderect,而是先使用矩形的方法inflat
        以及pad_size和pad_top计算出一个新的矩形，这个矩形不包含香蕉图像顶部
        和两边的“空白”区域
        :param other:
        :return:
        """
        # 通过剔除内边距来计算bounds
        bounds = self.rect.inflate(-self.pad_side, -self.pad_top)
        # 将bounds 移动到与香蕉底部对齐：
        bounds.bottom = self.rect.bottom
        # 检查bounds 是否与另一个对象的rect重叠
        return bounds.colliderect(other.rect)

