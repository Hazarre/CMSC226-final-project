import socket
from battleship import*
from common import *
#import cryptoWorkspace as cw

def socket_to_server():
    #connects to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(True)
    s.connect(('3.95.242.45', PORT))
    return s

def handle_flag(flag):
    # prints out flag messages 
    for mes in FLAGS: 
        if flag == FLAGS[mes] and flag != FLAGS["wait"]:
            print(mes)

def process_input(s):
    # convert command line input into format for function call on battleship.py
    l = s.split()
    if len(s) == 3:
        return MSG_TYPE['ship placement'] + " " + s
    elif len(s) == 2:
        return MSG_TYPE['fire'] + " " + s
    else: 
        print("input error")


g = Game() # start game
g.set_identity("client")
p = g.players[0] #player 
o = g.players[1] #opponent 
o.nships_to_place = 0
s = socket_to_server()
print("connected to server")

def make_move():
    # asks user for move input and updates game for both at local and the server
    move = g.get_input_prompt()
    g.update_game(move, 0)
    print("making move %s" % move)
    s.sendall(move.encode("utf-8"))

while True:
    mes = s.recv(BUFFER_SIZE).decode("UTF-8").split()
    mes_type = mes[0]

    if mes_type == MSG_TYPE['flag']:
        if mes[1] == FLAGS["my turn"]:
            make_move()
        else: 
            handle_flag(mes[1])
    
    elif mes_type == MSG_TYPE['fire result']:
        x, y = int(mes[2]), int(mes[3])
        if mes[1] == RESULT['hit']:
            p.enemy_board[x][y] = STATUS["hit"]
            print("target hit at (%s,%s)" % (mes[2], mes[3]))
        else:
            p.enemy_board[x][y] = STATUS["miss"]
            print("target missed at (%s,%s)" % (mes[2], mes[3]))
        p.visualize()

    elif mes_type == MSG_TYPE['under fire']:
        if p.take_missle(int(mes[1]),int(mes[2])) == STATUS["hit"]:
            print("got hit at (%s,%s)" % (mes[1], mes[2]))
        else:
            print("got lucky at (%s,%s)" % (mes[1], mes[2]))
        p.visualize()
        make_move()

s.close()