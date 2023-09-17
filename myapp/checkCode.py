from PIL import Image, ImageDraw, ImageFont
import random

from scipy.fftpack import fft
import numpy as np


def generate_captcha_image(width, height, code_length, font_path, output_path):
    # 创建空白图像
    image = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建 ImageDraw 对象
    draw = ImageDraw.Draw(image)

    # 定义验证码的字符集
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

    # 生成随机验证码字符串
    code = ''.join(random.choice(characters) for _ in range(code_length))

    # 定义验证码的字体和大小
    font = ImageFont.truetype(font_path, int(width/3))

    # 在图像上绘制验证码文本
    draw.text((10, 10), code, font=font, fill=(0, 0, 0))

    # 添加干扰线
    # 添加干扰点
    for _ in range(100):
        x = random.randint(0, width)
        y = random.randint(0, height)
        point_size = 0#random.randint(1, 5)  # 干扰点大小范围为 1 到 5
        draw.rectangle((x, y, x + point_size, y + point_size), fill=(0, 0, 0))

    # 保存图像到文件
    image.save(output_path)

    # 返回生成的验证码字符串
    return code
def FFT(Fs, data):
    """
    对输入信号进行FFT
    :param Fs:  采样频率
    :param data:待FFT的序列
    :return:
    """
    L = len(data)  # 信号长度
    N = np.power(2, np.ceil(np.log2(L)))  # 下一个最近二次幂，也即N个点的FFT
    result = np.abs(fft(x=data, n=int(N))) / L * 2  # N点FFT
    axisFreq = np.arange(int(N / 2)) * Fs / N  # 频率坐标
    result = result[range(int(N / 2))]  # 因为图形对称，所以取一半
    return axisFreq, result
