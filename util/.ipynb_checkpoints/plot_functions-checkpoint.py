import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
def plot_rainbow(xmin, xmax, ymin=0, ymax=1.02, interval=0.1, alpha_start=0.8, alpha_end=0.3, color=[0,0.4,0.4]):
    mid=0.5*(xmax+xmin)
    span=xmax-xmin
    wing=span/2
    box_num=int(wing/interval)
    alpha=alpha_start
    alpha_interval=(alpha_start-alpha_end)/box_num
    plt.gca().add_patch(Rectangle((mid-interval/2,ymin),interval, ymax,
                    edgecolor='black',
                    facecolor=color,
                    lw=0.0,
                    alpha=alpha))
    
    for i in range(box_num):
        alpha-=alpha_interval
    #     print(alpha)
        x_start=mid-interval/2-(i+1)*interval
        plt.gca().add_patch(Rectangle((x_start,ymin),interval,ymax,
                            edgecolor='black',
                            facecolor=color,
                            lw=0.0,
                            alpha=alpha))

        x_start=mid-interval/2+(i+1)*interval
        plt.gca().add_patch(Rectangle((x_start,ymin),interval,ymax,
                            edgecolor='black',
                            facecolor=color,
                            lw=0.0,
                            alpha=alpha))