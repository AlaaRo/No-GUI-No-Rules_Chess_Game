print("\n\tYOU ARE PLAYING WITH THE BLACK PIECES")
import socket,sys,time
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if len(sys.argv) < 2:
    print("NO CORRECT MODE WAS SPECIFIED, ONLY MODES ARE \"listen\" and \"connect\"\nRead How To Run The Game\n\tEXITING THE GAME")
    time.sleep(20)
    sys.exit()
initial_mode = sys.argv[1]
opponent_ip = input("ENTER THE OPPONENT'S IP\n\t-> ")
opponent_port = int(input("ENTER THE OPPONENT'S PORT NUMBER\n\t-> "))
your_ip = input("ENTER YOUR IP\n\t-> ")
your_port = int(input("ENTER YOUR PORT NUMBER\n\t-> "))
if initial_mode.lower() == "connect":
    try:
        print("TRYING TO CONNECT TO THE OPPONENT")
        clientsocket.connect((opponent_ip,opponent_port))
        print("\nCONNECTED")
        try:
            listener.bind((your_ip,your_port))
            listener.listen(0)
            print("\nWAITING FOR THE OPPONENT TO CONNECT BACK")
            player,address = listener.accept()
            print(address,"CONNECTED",sep="  ")  
        except OSError:
            print("\nWrong Input, Read How To Run the Game. Also Check Network Connection\nEXITING THE GAME")
            player.close()
            clientsocket.close()
            listener.close()
            time.sleep(20)
            sys.exit()
    except ConnectionRefusedError:
        print("\nOpponent Refused the Connection\nCheck the Opponent's IP and Port number or Firewall Rules for you and him/her\nEXITING THE GAME")
        clientsocket.close()
        listener.close()
        time.sleep(20)
        sys.exit()
elif initial_mode.lower() == "listen":
    try:
        listener.bind((your_ip,your_port))
        listener.listen(0)
        print("WAITING FOR THE OPPONENT TO CONNECT")
        player,address = listener.accept()
        print(address,"CONNECTED",sep=" ")
        try:
            print("\nTRYING TO CONNECT TO THE OPPONENT")
            clientsocket.connect((opponent_ip,opponent_port))
            print("\nCONNECTED")
        except ConnectionRefusedError:
            print("Opponent Refused the Connection\nCheck opponent's IP and Port number or Firewall Rules for you and him/her\nEXITING THE GAME")
            player.close()
            clientsocket.close()
            listener.close()
            time.sleep(20)
            sys.exit()
    except OSError:
        print("\nWrong Input, Read How To Run the Game. Also Check Network Connection\nEXITING THE GAME")
        listener.close()
        clientsocket.close()
        time.sleep(20)
        sys.exit()
else:
    print("\nNO CORRECT MODE WAS SPECIFIED, ONLY MODES ARE \"listen\" and \"connect\"\nread how to run the game\n\tEXITING THE GAME")
    player.close()
    listener.close()
    clientsocket.close()
    time.sleep(30)
    sys.exit()
list_chessboard = [     
			["wR","wN","wB","wK","wQ","wB","wN","wR"],

			["wP","wP","wP","wP","wP","wP","wP","wP"],			
                        
			["  ","  ","  ","  ","  ","  ","  ","  "],

			["  ","  ","  ","  ","  ","  ","  ","  "],
                        
			["  ","  ","  ","  ","  ","  ","  ","  "],
                        
			["  ","  ","  ","  ","  ","  ","  ","  "],
                 
			["bP","bP","bP","bP","bP","bP","bP","bP"],
                       
			["bR","bN","bB","bK","bQ","bB","bN","bR"]
		  ]     
copy_list_chessboard = list_chessboard.copy()

file_to_number = ['h','g','f','e','d','c','b','a'] 

rank_translation = [1,2,3,4,5,6,7,8]

class Translator:
    def __init__(self,file,rank):
        self.file = file
        self.rank = rank

promotion_symbol = ""

def movement(currently,future):
    global piece_next_location,promotion_symbol
    if copy_list_chessboard[currently.rank][currently.file] == "bP" and future.rank == 0:
        promotion = input("YOU ARE PROMOTING A PAWN, CHOOSE WHAT PIECE WILL IT BECOME\n(N,B,R,Q) -> ")
        if len(promotion) < 1 or promotion[0].upper() not in ("N","B","R","Q"):
            print("YOU DIDN'T SPECIFY A CORRECT PIECE, YOU WILL BE PUNISHED BY PROMOTING TO A KNIGHT")
            promotion = "N"
            
        copy_list_chessboard[future.rank][future.file] = "b" + promotion[0].upper()
        copy_list_chessboard[currently.rank][currently.file] = "  "
        try:
            promotion_symbol = promotion[0].upper()
        except NameError:
            pass
    else:
        copy_list_chessboard[future.rank][future.file] = copy_list_chessboard[currently.rank][currently.file]
        copy_list_chessboard[currently.rank][currently.file] = "  "
def unfold():
    unfolded = ""
    count = 0
    for row in copy_list_chessboard:
        count += 1 
        unfolded += "\n\t\t-----------------------------------------\n\t\t{} ".format(str(count))
        for piece in row:
            unfolded += piece + " {} ".format(column_shape[0])
    
    return (unfolded+"\n\t\t--h----g----f----e----d----c----b----a---")

try:
    column_shape = input("Choose in what character the columns will be written \nbest are (*,+,|) but you can choose whatever character you want\nNOTE: DEFAULT IS |  -> ")
    if len(column_shape) < 1:
        print("YOU DIDN'T SPECIFY A COLUMN CHARACTER, DEFAULT WILL BE CHOSEN")
        column_shape = "|"
    while True:
        while True:
            try:
                print(unfold())
                print("\n\t\tWAITING FOR WHIITE TO MOVE")
                white_piece_currently = player.recv(2).decode()
                white_piece_future = player.recv(3).decode()
                if len(white_piece_currently) == 0:
                    print("WARNING : RECIEVED AN EMPTY PACKET, CLOSING THE CONNECTIONS")
                    player.close()
                    clientsocket.close()
                    listener.close()
                    time.sleep(15)
                    sys.exit()
                location_currently = Translator(file_to_number.index(white_piece_currently[0]),rank_translation.index(int(white_piece_currently[1])))
                location_future = Translator(file_to_number.index(white_piece_future[0]),rank_translation.index(int(white_piece_future[1])))
                movement(location_currently,location_future)
                try:
                    copy_list_chessboard[location_future.rank][location_future.file] = "w" + white_piece_future[2]
                except IndexError:
                    print("....")
                print(unfold())
                break
            except (IndexError,ValueError):
                print("Wrong Input by Peer")
        while True:
            try:
                print("\n\t\tYOUR MOVE NOW")
                piece_letter = input("\nPiece Type. It doesn't matter what you type here ->  ")
                piece_location = input("Piece Current Location (CRITICAL) ->  ")[:2].lower()
                piece_next_location = input("Where To Move The Piece (CRITICAL) ->  ")[:2].lower()
                black_piece_currently = Translator(file_to_number.index(piece_location[0]),rank_translation.index(int(piece_location[1])))
                black_piece_future = Translator(file_to_number.index(piece_next_location[0]),rank_translation.index(int(piece_next_location[1])))
                movement(black_piece_currently,black_piece_future)
                print(unfold())
                clientsocket.send(piece_location.encode())
                clientsocket.send((piece_next_location + promotion_symbol).encode())
                promotion_symbol = ""
                break
            except (IndexError,ValueError):
                print("Wrong Input")
except ConnectionResetError:
    print("WARNING : CONNECTION RESET : AN EXISTING CONNECTION WAS FORCIBLY CLOSED BY REMOTE HOST\nEXITING THE GAME")
    time.sleep(20)  
    sys.exit()






