import numpy as np
import pickle
import matplotlib.pyplot as plt

def calculate_probability(N_PLAYER, N_BRIDGE):
    initial_prob = np.power(0.5, np.arange(1, N_BRIDGE+2, 1))
    initial_prob[-1] = initial_prob[-2]

    mulmat = np.zeros((N_BRIDGE+1, N_BRIDGE+1))
    for i in range(N_BRIDGE):
        for j in range(N_BRIDGE):
            if i > j:
                mulmat[i,j] = np.power(0.5, i-j)
    mulmat[-1] = mulmat[-2]
    mulmat[-1,-2] = 1
    mulmat[-1,-1] = 1

    player_prob = []
    current_prob = initial_prob
    player_prob.append(current_prob)
    for i in range(N_PLAYER-1):
        current_prob = np.matmul(mulmat, current_prob)
        player_prob.append(current_prob)
    player_prob = np.array(player_prob)

    return player_prob

def show_live_prob(player_p):
    n_player, n_bridge = player_p.shape
    p_idx = np.arange(n_player) + 1
    prob = player_p[:,-1]

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(p_idx, prob, linewidth=2)
    ax.set_title('Live probabilities for each player')
    ax.set_xlim([0,n_player+1])
    ax.set_ylim([0,1])
    ax.set_xlabel('player index')
    ax.set_ylabel('probability')
    plt.show()

    pass


def main():
    N_PLAYER = 16
    N_BRIDGE = 18
    player_p = calculate_probability(N_PLAYER, N_BRIDGE)

    show_live_prob(player_p)
    
    # print('t')

    N_PLAYER = 30
    N_BRIDGE = 30
    total = []
    for p in range(1,N_PLAYER+1):
        each_b = []
        for b in range(1,N_BRIDGE+1):
            player_p = calculate_probability(p, b)
            each_b.append(player_p)
        total.append(each_b)

    with open('probability.pkl', 'wb') as f:
        pickle.dump(total, f)

    pass






if __name__ == '__main__':
    main()
