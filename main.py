import os
import math
import random
import pygame
from modules.Sprites import *
from modules.interfaces import *

#设置游戏帧率
FPS = 100
# 屏幕大小
SCREENSIZE = (800,500)
# 游戏图片路径
IMAGE_PATHS = {
                'rabbit': os.path.join(os.getcwd(), 'resources/images/dude.png'),
                'grass': os.path.join(os.getcwd(), 'resources/images/grass.png'),
                'castle': os.path.join(os.getcwd(), 'resources/images/chengbao.png'),
                'arrow': os.path.join(os.getcwd(), 'resources/images/bullet.png'),
                'badguy': os.path.join(os.getcwd(), 'resources/images/badguy.png'),
                'healthbar': os.path.join(os.getcwd(), 'resources/images/healthbar.png'),
                'health': os.path.join(os.getcwd(), 'resources/images/health.png'),
                'gameover': os.path.join(os.getcwd(), 'resources/images/gameover.png'),
                'youwin': os.path.join(os.getcwd(), 'resources/images/youwin.png')
            }
# 游戏声音路径
SOUNDS_PATHS = {
                'hit': os.path.join(os.getcwd(), 'resources/audio/explode.wav'),
                'enemy': os.path.join(os.getcwd(), 'resources/audio/enemy.wav'),
                'shoot': os.path.join(os.getcwd(), 'resources/audio/shoot.wav'),
                'moonlight': os.path.join(os.getcwd(), 'resources/audio/moonlight.wav')
            }

# 保存和读取游戏状态信息的文件路径]
GAME_STATE_FILE = 'game_state.txt'
def save_game_state(accuracy):
    """
    保存游戏状态（准确率）到文件中。
    Parameters:
    - accuracy (float): 要保存的准确率值。
    Returns:
    - None
    Raises:
    - Exception: 如果在保存过程中发生错误，将打印错误信息。
    """
    try:
        with open(GAME_STATE_FILE, 'w') as file:
            file.write(str(accuracy))
    except Exception as e:
        print(f"Error saving game state: {e}")

def load_game_state():
    """
    从文件中加载游戏状态（准确率）。

    Returns:
    - float: 加载的准确率值。

    Raises:
    - FileNotFoundError: 如果文件不存在，将打印相应的提示信息。
    - Exception: 如果在加载过程中发生错误，将打印错误信息。
    """
    accuracy = 0.0
    try:
        with open(GAME_STATE_FILE, 'r') as file:
            accuracy = float(file.read())
    except FileNotFoundError:
        print("Game state file not found. Starting with default values.")
    except Exception as e:
        print(f"Error loading game state: {e}")
    return accuracy

'''游戏初始化'''
def initGame():
    """
    初始化游戏，设置展示窗口，并加载必要的游戏素材（图片和声音）。

    Returns:
    - pygame.Surface: 游戏窗口的 Surface 对象。
    - dict: 包含游戏图片的字典，键为图像类型，值为对应的 Surface 对象。
    - dict: 包含游戏声音的字典，键为声音类型，值为对应的 pygame.mixer.Sound 对象。
    """
    # 初始化pygame, 设置展示窗口
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('保卫晶石-守卫家园')

    # 加载必要的游戏素材
    game_images = {}
    for key, value in IMAGE_PATHS.items():
        game_images[key] = pygame.image.load(value)
    game_sounds = {}
    for key, value in SOUNDS_PATHS.items():
        if key != 'moonlight':
            game_sounds[key] = pygame.mixer.Sound(value)

    return screen, game_images, game_sounds

'''主函数'''
def main():
	# 初始化
	screen, game_images, game_sounds = initGame()
	# 播放背景音乐
	pygame.mixer.music.load(SOUNDS_PATHS['moonlight'])
	pygame.mixer.music.play(-1, 0.0)
	# 字体加载
	font = pygame.font.Font(None, 24)
	# 定义兔子
	bunny = BunnySprite(image=game_images.get('rabbit'), position=(180,250))
	# 跟踪玩家的精度变量, 记录了射出的箭头数和被击中的獾的数量.
	acc_record = [0., 0.]
	# 生命值
	healthvalue = 194
	# 子弹
	arrow_sprites_group = pygame.sprite.Group()
	# 地鼠
	badguy_sprites_group = pygame.sprite.Group()
	badguy = BadguySprite(game_images.get('badguy'), position=(640, 100))
	badguy_sprites_group.add(badguy)
	# 定义了一个定时器, 使得游戏里经过一段时间后就新建一支獾
	badtimer = 100
	badtimer1 = 0
	# 游戏主循环, running变量会跟踪游戏是否结束, exitcode变量会跟踪玩家是否胜利.
	running, exitcode = True, False
	clock = pygame.time.Clock()

	# 加载准确率
	accuracy = load_game_state()
	while running:
		# --在给屏幕画任何东西之前用黑色进行填充
		screen.fill(0)
		# --添加的风景也需要画在屏幕上
		for x in range(SCREENSIZE[0]//game_images['grass'].get_width()+1):
        #cfg.SCREENSIZE[0] 表示取 SCREENSIZE 属性中的第一个元素，即屏幕的宽度
			for y in range(SCREENSIZE[1]//game_images['grass'].get_height()+1):
				#将草地图案绘制到屏幕上，每个草地的大小为(100, 100)
				screen.blit(game_images['grass'], (x*100, y*100))
		#绘制城堡的图案，共有四个城堡，位于屏幕左上角，垂直间隔为 105 像素
		for i in range(4): screen.blit(game_images['castle'], (0, 30+105*i))

		# --按键检测
		# keys = pygame.key.get_pressed()
		# bunny.move(cfg.SCREENSIZE, keys)

		# --倒计时信息
		# 返回当前程序运行的毫秒数
		countdown_text = font.render(str((90000-pygame.time.get_ticks())//60000)+":"+str(
			(90000-pygame.time.get_ticks())//1000%60).zfill(2), True, (0, 0, 0))
		#计算了剩余的毫秒数，然后通过除以 60000 得到分钟数
		#%60 求余操作，得到剩余秒数对 60 取余的结果，表示不足一分钟的秒数
		countdown_rect = countdown_text.get_rect()
		countdown_rect.topright = [635, 5]
		screen.blit(countdown_text, countdown_rect)
		# --按键检测
		# ----退出与射击
		for event in pygame.event.get():#遍历所有的pygame事件
			if event.type == pygame.QUIT:#检测是否有退出事件，如果是，退出游戏
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:#检测是否有鼠标按下事件
				game_sounds['shoot'].play()  # 播放射击音效
				acc_record[1] += 1  # 记录射击次数
				mouse_pos = pygame.mouse.get_pos()  # 获取鼠标点击位置
				angle = math.atan2(mouse_pos[1] - (bunny.rotated_position[1] + 32),
								   mouse_pos[0] - (bunny.rotated_position[0] + 26))
				# 计算子弹的发射角度
				arrow = ArrowSprite(game_images.get('arrow'), (angle,
															   bunny.rotated_position[0] + 32,
															   bunny.rotated_position[1] + 26))
				# 创建ArrowSprite对象，表示一发子弹，并设置其初始位置和发射角度
				arrow_sprites_group.add(arrow)  # 将箭添加到箭的精灵组中

		# ----移动兔子
		# key_pressed = pygame.key.get_pressed()
		# if key_pressed[pygame.K_w]:
		# 	bunny.move(cfg.SCREENSIZE, 'up')
		# elif key_pressed[pygame.K_s]:
		# 	 bunny.move(cfg.SCREENSIZE, 'down')
		# elif key_pressed[pygame.K_a]:
		# 	bunny.move(cfg.SCREENSIZE, 'left')
		# elif key_pressed[pygame.K_d]:
		# 	bunny.move(cfg.SCREENSIZE, 'right')
		# --更新弓箭
		for arrow in arrow_sprites_group:
			if arrow.update(SCREENSIZE):
				arrow_sprites_group.remove(arrow)
		# --更新地鼠
		if badtimer == 0:
			badguy = BadguySprite(game_images.get('badguy'), position=(640, random.randint(50, 430)))
			badguy_sprites_group.add(badguy)
			badtimer = 100 - (badtimer1 * 2)
			badtimer1 = 20 if badtimer1>=20 else badtimer1+2
		badtimer -= 1
		for badguy in badguy_sprites_group:
			if badguy.update():#如果返回 True，表示敌人已经越过屏幕左侧，需要处理玩家的生命值减少
				game_sounds['hit'].play()#播放命中音效
				healthvalue -= random.randint(4, 8)#随机减少玩家的生命值
				badguy_sprites_group.remove(badguy)#移除该敌人，因为它已经越过屏幕
		# --碰撞检测
		for arrow in arrow_sprites_group:
			for badguy in badguy_sprites_group:
				if pygame.sprite.collide_mask(arrow, badguy):
					game_sounds['enemy'].play()  # 播放敌人被击中的音效
					arrow_sprites_group.remove(arrow)  # 从子弹精灵组中移除碰撞的子弹
					badguy_sprites_group.remove(badguy)  # 从地鼠精灵组中移除碰撞的地鼠
					acc_record[0] += 1  # 记录击中的敌人数量

		# --画出子弹
		arrow_sprites_group.draw(screen)
		# --画出地鼠
		badguy_sprites_group.draw(screen)
		# --画出兔子（pygame.mouse.get_pos() 返回当前鼠标的位置，是一个包含 x 和 y 坐标的元组）
		bunny.draw(screen, pygame.mouse.get_pos())
		# --画出城堡健康值, 首先画了一个全红色的生命值条, 然后根据城堡的生命值往生命条里面添加绿色.
		screen.blit(game_images.get('healthbar'), (5, 5))
		for i in range(healthvalue):
			screen.blit(game_images.get('health'), (i+8, 8))
		# --判断游戏是否结束
		if pygame.time.get_ticks() >= 90000:
			running, exitcode = False, True
		if healthvalue <= 0:
			running, exitcode = False, False
		# --更新屏幕
		pygame.display.flip()
		clock.tick(FPS)
	# 计算准确率
	accuracy = acc_record[0] / acc_record[1] * 100 if acc_record[1] > 0 else 0
	accuracy = '%.2f' % accuracy
	showEndGameInterface(screen, exitcode, accuracy, game_images)
	# 保存游戏准确率
	save_game_state(float(accuracy))


'''运行程序'''
if __name__ == '__main__':
	main()
