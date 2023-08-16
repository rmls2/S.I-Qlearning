# Aqui vocês irão colocar seu algoritmo de aprendizado
import connection as cn
from random import randint, random
#   V------------ações---------------V
#   [Giro esq, Giro dir, Pulo frente]
q_matrix = []

table_file = open("resultado.txt", "r")
for line in table_file:
    left = float(line.split(' ')[0])
    right = float(line.split(' ')[1])
    jump = float(line.split(' ')[2])
    q_matrix.append([left, right, jump])
table_file.close()

ALFA = 0.1
GAMMA = 0.4
EPSILON = 0.05
skt = cn.connect(2037)

# PASSOS:
# 1) Escolher uma ação e executá-la
# 2) Aplicar a recompensa obtida
# 3) Observar o novo estado s'
# 4) Atualizar o valor de Q(s,a) conforme a regra de aprendizagem


def convert_action(action):
    if(type(action) == int):
        if(action == 0):
            return "left"
        elif(action == 1):
            return "right"
        elif(action == 2):
            return "jump"
    elif(type(action) == str):
        if(action == "left"):
            return 0
        elif(action == "right"):
            return 1
        elif(action == "jump"):
            return 2


def q_update(s: int, new_s: int, a: int, r: int, q: list):
    # Q(s,a) <- Q(s,a) + α[r + γ*max(Q(s', a')) - Q(s,a)]
    global ALFA
    global GAMMA

    # modelo estado: 5bits[plataforma] + 2bits[direção]
    # 00: Norte - 01: Leste - 10: Sul - 11: Oeste
    state_action = q[s][a]

    return state_action + ALFA*(r + GAMMA*max(q[new_s]) - state_action)


def prints(state: int):
    x = state % 4
    if(x == 0):
        way = 'N'
    elif(x == 1):
        way = 'L'
    elif(x == 2):
        way = 'S'
    elif(x == 3):
        way = 'O'
    return str(state//4) + way


old_state = 0  # '0b0000000'
for rept in range(100000):
    # [1]
    if(random() > EPSILON):
        acao = randint(0, 2)
    else:
        acao = q_matrix[old_state].index(max(q_matrix[old_state]))
    # [2] e [3]
    new_state, recompensa = cn.get_state_reward(skt, convert_action(acao))
    new_state = int(new_state, 2)
    # [4]
    q_matrix[old_state][acao] = q_update(
        old_state, new_state, acao, recompensa, q_matrix)
    print(str(rept+1)+':', prints(old_state),
          convert_action(acao), prints(new_state), recompensa)
    old_state = new_state

results = open("resultado.txt", "w")
for line_state in q_matrix:
    line = "{:.5f} {:.5f} {:.5f}\n".format(
        line_state[0], line_state[1], line_state[2])
    results.write(line)
results.close()
