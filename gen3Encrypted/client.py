import socket
from battleship import*
import cryptoWorkspace as cw
PORT = 8080
BUFFER_SIZE = 1024


def socket_to_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(True)
    s.connect(('3.95.242.45', PORT))
    return s


def send(msg):
    msg = cw.encrypt(msg.encode("utf-8"),serv_key)
    s.sendall(msg)


def recieve(bufsize):
    msg = s.recv(bufsize)
    msg = cw.decrypt(msg,priv_key).decode("utf-8")
    return msg


g = Game()
g.set_identity("client")

id = 0 
e_id = 1 # enemy's id
s = socket_to_server()

serv_key = cw.deserialize_key(s.recv(3))
priv_key, pub_key = cw.generate_keys()
s.sendall(cw.serialize_key(pub_key))
print("connected to server")

mess = MESSAGE_ENCODING["waiting"]
while True:
    # add input error/placement success in both client and server.py, include with case my_turn
    # add case "waiting"
    print("prev STATE %s %s" % (mess, MESSAGE_DECODING[int(mess)]))
    print("waiting for server")
    mess = recieve(1)
    print("CURRENT STATE %s %s" % (mess, MESSAGE_DECODING[int(mess)]))
    if mess == MESSAGE_ENCODING['under_fire']:
        move = recieve(3)
        print("recieved move %s under fire" %move)
        g.update_game(move,e_id)
        g.p1.visualize()
        mess = MESSAGE_ENCODING['my_turn']
        print("underfire done")
    elif mess == MESSAGE_ENCODING['you_win']:
        print("You won")
    elif mess == MESSAGE_ENCODING['you_loss']:
        print("YOu loss")
    elif mess == MESSAGE_ENCODING['my_turn']:
        print("my turn lll")
        move = g.get_input_prompt()
        send(move)
        if g.state == STATE['fire']:
            mess = recieve(1) # hear from the server the result of the missle
            if mess == MESSAGE_ENCODING['target_hit']:
                print("hit target")
                print("recieved result mess %s under fire" % MESSAGE_DECODING[int(mess)])
                m = g.parse_input(move)
                g.players[id].enemy_board[m['x']][m['y']] = STATUS['ship']
        g.update_game(move,id)
        print(move,type(move))
        mess = MESSAGE_ENCODING['waiting']
    
s.close()