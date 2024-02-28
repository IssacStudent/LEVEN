
import matplotlib.pyplot as plt
import numpy as np


def read_losses(file_path):
    """
    读取损失值文件并返回损失值列表。
    """
    with open(file_path, 'r') as file:
        losses = [float(line.strip()) for line in file]
    return losses


def plot_losses(losses):
    """
    绘制损失值的对数图表。
    """
    # 对损失值取自然对数
    losses = np.log(losses)

    plt.plot(losses)
    plt.title('Log of Loss over Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Log of Loss')
    plt.show()


def main():
    # 替换成你的文件路径
    file_path = './saved_20240131/loss_list.txt'

    # 读取损失值并绘图
    losses = read_losses(file_path)
    plot_losses(losses)
    print(losses.__len__())

if __name__ == "__main__":
    main()
