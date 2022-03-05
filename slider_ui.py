import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


# Load probabilities
with open('probability.pkl', 'rb') as f:
    total_p = pickle.load(f)
n_player = len(total_p)
n_bridge = len(total_p[0])

p0 = int(n_player / 2)
b0 = int(n_bridge / 2)
i0 = 1
pi_step = 1
bi_step = 1

x0 = np.arange(p0) + 1
prob = total_p[p0-1][b0-1][:,-1]

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)
ax.set_ylim([-0.1,1.1])
ax.set_xlim([1,p0])
ax.set_xlabel('player index')
ax.set_title('Live probabilities for each player')

l, = plt.plot(x0, prob, lw=2)
ax.margins(x=0)

axcolor = 'lightgoldenrodyellow'
axcolor2 = 'lightslategray'
axp = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
axb = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axi = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor2)
rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)

sldp = Slider(axp, 'Players', 1, n_player, valinit=p0, valfmt='%d', valstep=pi_step)
sldb = Slider(axb, 'Bridges', 1, n_bridge, valinit=b0, valfmt='%d', valstep=bi_step)
sldi = Slider(axi, 'i-th Players', 1, n_player, valinit=i0, valfmt='%d', valstep=pi_step, slidermax=sldp)
radio = RadioButtons(rax, ('Live', 'Death', 'Reach'), active=0)

sldi.set_active(False)

def update(val):
    pi = sldp.val
    bi = sldb.val
    ii = sldi.val
    if ii > pi:
        sldi.set_val(pi)
        ii = sldi.val
    
    if radio.value_selected == 'Live':
        xi = np.arange(pi) + 1
        prob = total_p[pi-1][bi-1][:,-1]
        ax.set_xlim([1,pi])
        ax.set_ylim([-0.1,1.1])
        ax.set_xlabel('player index')
    elif radio.value_selected == 'Death':
        xi = np.arange(pi) + 1
        prob = 1 - total_p[pi-1][bi-1][:,-1]
        ax.set_xlim([1,pi])
        ax.set_ylim([-0.1,1.1])
        ax.set_xlabel('player index')
    elif radio.value_selected == 'Reach':
        xi = np.arange(bi) + 1
        prob = total_p[pi-1][bi-1][ii-1,:-1]
        ax.set_xlim([1,bi])
        ax.set_ylim([-0.1,0.5])
        ax.set_xlabel('bridge index')
        ax.set_title('Probabilities to reach each bridge for {}-th player'.format(ii))
    l.set_data(xi, prob)
    fig.canvas.draw_idle()


sldp.on_changed(update)
sldb.on_changed(update)
sldi.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def reset(event):
    sldp.reset()
    sldb.reset()
    sldi.reset()
button.on_clicked(reset)

def labelfunc(label):
    update(1)
    if label == 'Reach':
        sldi.set_active(True)
        axi.set_facecolor(axcolor)
    else:
        sldi.set_active(False)
        axi.set_facecolor(axcolor2)
        if label == 'Live':
            ax.set_title('Live probabilities for each player')
        else:
            ax.set_title('Death probabilities for each player')
    fig.canvas.draw_idle()
radio.on_clicked(labelfunc)

# Initialize plot with correct initial active value
labelfunc(radio.value_selected)

plt.show()
