import math
import pygame


'''定义兔子类'''
class BunnySprite(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)  # 调用父类的构造函数初始化精灵对象
        self.image = image  # 设置兔子的图像
        self.rect = self.image.get_rect()  # 获取图像的矩形区域
        self.rect.left, self.rect.top = position  # 设置兔子的初始位置
        self.speed = 5  # 设置兔子的移动速度
        self.rotated_position = position  # 初始化旋转后的位置

    def move(self, screensize, keys):
        """
        移动兔子的方法。

        Parameters:
        - screensize (tuple): 屏幕的尺寸，以元组形式表示宽度和高度。
        - keys (pygame.key.get_pressed()): 按键状态的元组，使用pygame.key.get_pressed()获取。

        Returns:
        - None
        """
        # if keys[pygame.K_a]:
        #     self.rect.left = max(self.rect.left - self.speed, 0)
        # elif keys[pygame.K_d]:
        #     self.rect.left = min(self.rect.left + self.speed, screensize[0])
        # if keys[pygame.K_w]:
        #     self.rect.top = max(self.rect.top - self.speed, 0)
        # elif keys[pygame.K_s]:
        #     self.rect.top = min(self.rect.top + self.speed, screensize[1])

    def draw(self, screen, mouse_pos):

        # 在屏幕上画出兔子的方法。
        # 计算鼠标相对于兔子的位置，得到旋转的角度（弧度制）
        angle = math.atan2(mouse_pos[1] - (self.rect.top + 32), mouse_pos[0] - (self.rect.left + 26))
        #对兔子图像进行旋转，将其旋转到指定角度。57.29 是将弧度转换为角度的系数
        image_rotate = pygame.transform.rotate(self.image, 360 - angle * 57.29)
        # 计算旋转后兔子的新位置，确保旋转中心在原兔子中心位置。
        bunny_pos = (self.rect.left - image_rotate.get_rect().width / 2,
                     self.rect.top - image_rotate.get_rect().height / 2)
        #更新旋转后的位置，用于后续绘制箭头和碰撞检测
        self.rotated_position = bunny_pos
        # 将旋转后的兔子图像绘制到屏幕上的新位置
        screen.blit(image_rotate, bunny_pos)

'''定义子弹类'''
class ArrowSprite(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)  # 调用父类的构造函数初始化精灵对象
        self.angle = position[0]  # 获取子弹的发射角度，这个角度是在发射时由兔子确定的
        self.image = pygame.transform.rotate(image, 360 - position[0] * 57.29)  # 旋转子弹图像
        self.rect = self.image.get_rect()  # 获取图像的矩形区域
        self.mask = pygame.mask.from_surface(self.image)  # 创建图像的遮罩，用于碰撞检测
        self.rect.left, self.rect.top = position[1:]  # 设置子弹的初始位置
        self.speed = 15  # 设置子弹的移动速度

    '''更新子弹'''

    def update(self, screensize):
        velx = math.cos(self.angle) * self.speed  # 根据角度计算水平方向上的速度分量
        vely = math.sin(self.angle) * self.speed  # 根据角度计算垂直方向上的速度分量
        self.rect.left += velx  # 更新子弹的水平位置
        self.rect.top += vely  # 更新子弹的垂直位置
        if (
                self.rect.right < 0
                or self.rect.left > screensize[0]
                or self.rect.top > screensize[1]
                or self.rect.bottom < 0
        ):
            return True  # 如果子弹超出屏幕范围，返回 True，表示需要从精灵组中移除
        return False  # 如果子弹仍在屏幕范围内，返回 False


'''定义地鼠类'''
class BadguySprite(pygame.sprite.Sprite):
    def __init__(self, image, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)  # 调用父类的构造函数初始化精灵对象
        self.image = image  # 地鼠的图像
        self.rect = self.image.get_rect()  # 获取图像的矩形区域
        self.mask = pygame.mask.from_surface(self.image)  # 创建图像的遮罩，用于碰撞检测
        self.rect.left, self.rect.top = position  # 设置地鼠的初始位置
        self.speed = 5  # 设置地鼠的移动速度

    def update(self):
        self.rect.left -= self.speed  # 更新地鼠的水平位置
        if self.rect.left < 64:
            return True  # 如果地鼠超出屏幕左侧，返回 True，表示需要从精灵组中移除
        return False  # 如果地鼠仍在屏幕范围内，返回 False，表示继续保留在精灵组中
