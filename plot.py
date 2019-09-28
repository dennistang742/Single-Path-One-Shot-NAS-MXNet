import matplotlib.pyplot as plt
import numpy as np
import argparse
import re


def plot():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log-file', default='condensed_shufflenas_supernet.log', help='log file')
    parser.add_argument('--mode', type=str, default='accuracy', help='the mode of plotting')
    # parser.add_argument('--log-file', default='search_supernet_SinglePathOneShot.log', help='log file')
    # parser.add_argument('--mode', type=str, default='subnet', help='the mode of plotting')
    args = vars(parser.parse_args())

    rows = open(args['log_file']).readlines()

    if args['mode'] == 'accuracy':
        train_acc_list = []
        val_acc_list = []

        for row in rows:
            if row[0] != '[':
                continue
            epoch = int(row[row.find(' ') + 1: row.find(']')])

            if 'training' in row:
                train_acc = float(row[row.find('=') + 1:])
                train_acc_list.append((epoch, train_acc))

            if 'validation' in row:
                val_acc = float(row[row.find('=') + 1: row.find('=') + 9])
                val_acc_list.append((epoch, 1 - val_acc))

        # plot the accuracies
        plt.style.use("ggplot")
        plt.figure()
        plt.plot(np.arange(0, len(train_acc_list)), [item[1] for item in train_acc_list], label="train_top1")
        plt.plot(np.arange(0, len(val_acc_list)), [item[1] for item in val_acc_list], label="val_top1")
        plt.title("Accuracy plot for supernet")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.legend(loc="lower right")
        plt.savefig('supernet_accuracy.png')
        plt.show()
    elif args['mode'] == 'subnet':
        score_list = []
        val_acc_list = []

        for i, row in enumerate(rows):
            if 'score' in row:
                score = float(row[row.find(':') + 1: row.rfind('.')])
                if 'Val' not in rows[i + 1]:
                    continue
                score_list.append(2 - score)
            if 'Val' in row:
                val_acc = float(row[row.find(':') + 1: row.find('\n')])
                if val_acc < 0.1:
                    score_list.pop()
                    continue
                val_acc_list.append(val_acc)

        plt.style.use("ggplot")
        plt.figure()
        plt.scatter(score_list, val_acc_list, alpha=0.8, c='steelblue', s=150, label='subnet')
        plt.title("Subnet Val-acc vs. score difference")
        plt.xlabel("Normalized score difference (larger is better)")
        plt.ylabel("Accuracy")
        plt.legend(loc="lower right")
        plt.savefig('subnet_scatter.png')
        plt.show()


if __name__ == '__main__':
    plot()