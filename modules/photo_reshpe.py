from PIL import Image

def resize_image(input_path, new_size):
    # 打开图像文件
    image = Image.open(input_path)

    # 调整图像大小
    resized_image = image.resize(new_size)

    # 保存调整大小后的图像，直接覆盖原始文件
    resized_image.save(input_path)

# 指定输入文件路径和新的图像大小
input_image_path = 'resources\images\chengbao.png'
new_size = (109,105)  # 指定新的宽度和高度

# 调用函数进行图像大小调整（将原始文件替换）
resize_image(input_image_path, new_size)
