from random import random
from matplotlib import pyplot as plt
import numpy as np
import math

### random()  ##Random float:  0.0 <= x < 1.0
import seaborn as sns

# settings for seaborn plotting style
sns.set(color_codes=True)
# settings for seaborn plot sizes
sns.set(rc={"figure.figsize": (5, 5)})

import imageio  ## conda install -c conda-forge imageio
import glob
import os

choice = 1


class Bertrand:
    def __init__(self):
        ## creates a figure and an Axes object(the plotting area)
        self.fig, self.ax = plt.subplots()
        ## side/length of the equilateral triangle
        self.triangle_len = 0

    def distance(self, point1, point2):
        ## point consists of (x,y)
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def draw_circle(self, radius, center=(0, 0)):
        self.ax.set_xlim((-radius - 0.2, radius + 0.2)), self.ax.set_ylim((-radius - 0.2, radius + 0.2))
        self.ax.set_xlabel("x"), self.ax.set_ylabel("y")

        centerx, centery = center
        circle = plt.Circle((centerx, centery), radius, color="black", fill=False)
        ## Artist: a standard graphical object, knows how to use the renderer to paint it
        self.ax.add_artist(circle)
        self.ax.set_aspect("equal")

    def draw_triangle(self, OneEndPoint, center=(0, 0)):
        x, y = OneEndPoint
        Tricenterx, Tricentery = center
        ## stack arrays in sequence horizontally (column wise)
        points = np.hstack([x, y])
        self.ax.plot(x, y, color="cyan", marker="*")  ##, label='P'

        # calculate the other 2 points of the equilateral triangle
        # rotate OneEndPoint by 120, -120 degrees => A, B points
        angle = np.deg2rad(120)
        xA = (
            Tricenterx
            + (x - Tricenterx) * np.cos(angle)
            - (y - Tricentery) * np.sin(angle)
        )
        yA = (
            Tricentery
            + (x - Tricenterx) * np.sin(angle)
            + (y - Tricentery) * np.cos(angle)
        )
        A = (xA, yA)
        points = np.vstack([points, [xA, yA]])
        self.ax.plot(xA, yA, color="cyan", marker="*")

        angle = np.deg2rad(-120)
        xB = (
            Tricenterx
            + (x - Tricenterx) * np.cos(angle)
            - (y - Tricentery) * np.sin(angle)
        )
        yB = (
            Tricentery
            + (x - Tricenterx) * np.sin(angle)
            + (y - Tricentery) * np.cos(angle)
        )
        B = (xB, yB)

        self.triangle_len = self.distance(A, B)
        points = np.vstack([points, [xB, yB]])
        self.ax.plot(xB, yB, color="cyan", marker="*")
        points = np.vstack([points, [x, y]])
        self.ax.plot(
            points[:, 0], points[:, 1], linewidth=2, color="blue"
        )  ##, label='equilateral triangle'

    def first_method(self):
        global choice
        r = float(input("radius = "))
        n = int(input("sample population = "))

        self.fig.suptitle("Bertrand paradox (random two points)")
        self.draw_circle(r, center=(0, 0))

        ## get a fixed P point on the circumference
        alpha = random() * (2 * np.pi)  ##Random float:  0.0 <= x < 1.0
        x0, y0 = 0 + r * np.cos(alpha), 0 + r * np.sin(alpha)  ## here (0,0) is the center
        P = (x0, y0)
        self.draw_triangle(P, center=(0, 0))

        center_points = []
        fav = 0  ## Sample number that great than sqrt(3)*r
        ## generate random points on the circumference
        for i in range(n):
            alpha = np.random.uniform(low=0, high=2 * np.pi)  ##[low, high)
            x, y = 0 + r * np.cos(alpha), 0 + r * np.sin(alpha)
            ## the new point
            M1 = (x, y)

            alpha = np.random.uniform(low=0, high=2 * np.pi)  ##[low, high)
            x, y = 0 + r * np.cos(alpha), 0 + r * np.sin(alpha)
            M2 = (x, y)

            # self.ax.plot((M1[0]+M2[0])/2, (M1[1]+M2[1])/2, color='orange', marker='.') ## middle point
            center_points.append([(M1[0] + M2[0]) / 2, (M1[1] + M2[1]) / 2])

            plt.draw()
            self.ax.plot(x, y, color="black", marker=".")
            if self.distance(M2, M1) > self.triangle_len:
                self.ax.plot([M1[0], M2[0]], [M1[1], M2[1]], color="green")
                fav += 1
            else:
                self.ax.plot([M1[0], M2[0]], [M1[1], M2[1]], color="red")

            plt.pause(0.001)
            print("Sample {}".format(i + 1), end="\r")
            self.draw_triangle(P, center=(0, 0))
            plt.savefig(f"./pictures/{choice}/{i}.png")
            self.ax.plot([M1[0], M2[0]], [M1[1], M2[1]], color="gray")

        print(
            "The probability for the length of chord is greater than sqrt(3)*r is: {}/{} = {}".format(fav, n, fav / n)
        )

        plt.grid()
        plt.show()

        #### plot the middle points of the chords distribution with the circle
        center_points = np.array(center_points)
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Bertrand paradox (random two points)")
        self.draw_circle(r, center=(0, 0))
        self.ax.scatter(
            center_points[:, 0], center_points[:, 1], color="orange", marker="."
        )
        self.draw_triangle(P, center=(0, 0))
        circle = plt.Circle((0, 0), r / 2, color="grey", fill=False)
        self.ax.add_artist(circle)
        plt.grid()
        plt.show()

    def second_method(self):
        global choice
        centerx = 0
        centery = 0
        r = float(input("radius = "))
        n = int(input("sample population = "))
        self.fig.suptitle("Bertrand paradox (random middle point in circle)")
        self.draw_circle(r, center=(centerx, centery))

        ## get a fixed P point on the circumference
        alpha = random() * (2 * np.pi)  ##Random float:  0.0 <= x < 1.0
        x0, y0 = centerx + r * np.cos(alpha), centery + r * np.sin(alpha)
        P = (x0, y0)
        self.draw_triangle(P, center=(centerx, centery))

        ## draw a smaller circle
        circle = plt.Circle((centerx, centery), r / 2, color="grey", fill=False)
        self.ax.add_artist(circle)
        center_points = []

        fav = 0  ## Sample number that great than sqrt(3)*r
        for i in range(n):
            ## generate a new point within the circle
            alpha = np.random.uniform(low=0, high=2 * np.pi)
            rand_r = math.sqrt(np.random.uniform(low=0, high=r))  ### area change is const
            x, y = centerx + rand_r * np.cos(alpha), centery + rand_r * np.sin(alpha)

            # self.ax.plot(x, y, color='orange', marker='.') ## middle point
            center_points.append([x, y])
            beta = alpha - np.pi / 2
            ## cord half length
            length = math.sqrt(pow(r, 2) - pow(rand_r, 2))
            x1, y1 = centerx + x + length * np.cos(beta), centery + y + length * np.sin(beta)
            x2, y2 = centerx + x - length * np.cos(beta), centery + y - length * np.sin(beta)
            ## the new point
            M = (x, y)
            plt.draw()
            if rand_r < r / 2:
                # plt.plot(x, y, color='green', marker='.')
                self.ax.plot([x1, x2], [y1, y2], color="green")
                fav += 1
            else:
                # plt.plot(x, y, color='red', marker='.')
                self.ax.plot([x1, x2], [y1, y2], color="red")

            plt.pause(0.001)
            print("Sample {}".format(i + 1), end="\r")
            # plt.plot(x, y, color='gray', marker='.')
            self.draw_triangle(P, center=(0, 0))
            plt.savefig(f"./pictures/{choice}/{i}.png")
            self.ax.plot([x1, x2], [y1, y2], color="gray")

        print(
            "The probability for the length of chord is greater than sqrt(3)*r is: {}/{} = {}".format(fav, n, fav / n)
        )

        plt.grid()
        plt.show()

        #### plot the middle points of the chords distribution with the circle
        center_points = np.array(center_points)
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Bertrand paradox (random middle point in circle)")
        self.draw_circle(r, center=(0, 0))
        self.ax.scatter(
            center_points[:, 0], center_points[:, 1], color="orange", marker="."
        )
        self.draw_triangle(P, center=(0, 0))
        circle = plt.Circle((centerx, centery), r / 2, color="grey", fill=False)
        self.ax.add_artist(circle)
        plt.grid()
        plt.show()

    def third_method(self):
        global choice
        centerx = 0
        centery = 0
        r = float(input("radius = "))
        n = int(input("sample population = "))
        self.fig.suptitle("Bertrand paradox (random middle point in a radius)")
        self.draw_circle(r, center=(centerx, centery))

        ## get a fixed P point on the circumference
        alpha0 = random() * (2 * np.pi)
        x0, y0 = centerx + r * np.cos(alpha0), centery + r * np.sin(alpha0)
        P = (x0, y0)
        self.draw_triangle(P, center=(centerx, centery))

        center_points = []

        fav = 0
        for i in range(n):
            ### random point on a random radius
            alpha = np.random.uniform(low=0, high=2 * np.pi)
            m = np.random.uniform(low=0, high=r)
            x, y = m * np.cos(alpha), m * np.sin(alpha)
            M = (x, y)
            plt.draw()
            # self.ax.plot(x, y, color='orange', marker='.') ## middle point
            center_points.append([x, y])
            ## perpendicular line to the radius in the generated point
            beta = alpha - np.pi / 2
            ## cord half length
            length = math.sqrt(pow(r, 2) - pow(m, 2))
            x1, y1 = centerx + x + length * np.cos(beta), centery + y + length * np.sin(beta)
            x2, y2 = centerx + x - length * np.cos(beta), centery + y - length * np.sin(beta)
            if m < r / 2:
                self.ax.plot([x1, x2], [y1, y2], color="green")
                fav += 1
            else:
                self.ax.plot([x1, x2], [y1, y2], color="red")

            plt.pause(0.001)
            print("Sample {}".format(i + 1), end="\r")

            self.draw_triangle(P, center=(0, 0))
            plt.savefig(f"./pictures/{choice}/{i}.png")
            self.ax.plot([x1, x2], [y1, y2], color="gray")

        print(
            "The probability for the length of chord is greater than sqrt(3)*r is: {}/{} = {}".format(fav, n, fav / n)
        )
        plt.grid()
        plt.show()

        #### plot the middle points of the chords distribution with the circle
        center_points = np.array(center_points)
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Bertrand paradox (random middle point in a radius)")
        self.draw_circle(r, center=(0, 0))
        self.ax.scatter(
            center_points[:, 0], center_points[:, 1], color="orange", marker="."
        )
        self.draw_triangle(P, center=(0, 0))
        circle = plt.Circle((centerx, centery), r / 2, color="grey", fill=False)
        self.ax.add_artist(circle)
        plt.grid()
        plt.show()


def main():
    global choice
    print("choose from the 3 methods (1|2|3):")
    print("\t1 (random two points in the circumference)")
    print("\t2 (random middile point inside the circle)")
    print("\t3 (random middle point along the radius)") 

    choice = int(input("choice = "))

    print("Delete files...")
    for f in glob.glob(f"./pictures/{choice}/*"):
        os.remove(f)

    bert = Bertrand()
    if choice == 1:
        bert.first_method()
    elif choice == 2:
        bert.second_method()
    elif choice == 3:
        bert.third_method()
    else:
        print("Input choice is invalid")


def distribution_plot(data, xname):
    ax = sns.distplot(
        data,
        bins=1000,
        kde=True,
        color="skyblue",
        hist_kws={"linewidth": 15, "alpha": 1},
    )
    ax.set(xlabel=xname, ylabel="Frequency")
    plt.show()


if __name__ == "__main__":
    """
    ### https://www.datacamp.com/tutorial/probability-distributions-python
    ### https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
    ### https://github.com/Fengtao22/Bertrand-paradox-Python_simulation/blob/main/bertrands.py
    random_test = []
    for i in range(10000):
            random_test.append(random())
    distribution_plot(random_test, 'random() Distribution')

    random_test = []
    for i in range(10000):
            random_test.append(np.random.uniform(0,1))
    distribution_plot(random_test, 'uniform() Distribution')

    from scipy.stats import uniform
    data_uniform = uniform.rvs(size=10000, loc = 0, scale=1)
    distribution_plot(data_uniform, 'scipy.stats.uniform Distribution')
    """

    main()

    images = []
    filenames = [image for image in glob.glob(f"./pictures/{choice}/*.png")]
    filenames = sorted(filenames, key=len)

    for filename in filenames:
        images.append(imageio.v2.imread(filename))
    imageio.mimsave(f"gifs/{choice}/Method{choice}.gif", images)
