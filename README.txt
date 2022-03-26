			No-GUI-No-Rules Chess Game: A game that doesn't look like one.
READ UNTIL THE END PLEASE.

------------------------------------|
PART ONE: HOW TO PLAY THE GAME      |
PART TWO: WHY THE GAME IS LIKE THAT |
------------------------------------|
w: white | b: black

P: Pawn | N: Knight | B: Bishop | R: Rook | Q: Queen | K: King

PART ONE

The game has to be played from the command-line interface, it needs
an argument, it's either "connect" or "listen". No matter which one you choose,
two TCP streams will be created, the argument is called "initial mode" because
it specifies the order of the connection attempts between the players. 
You either wait for a connection first or connect two someone who's already 
sat up the listener. Then the reverse of the this process will happen. 
Let's assume that white launched the game with "listen"(which means the other
player will write "connect" in the initial mode), then this happens:

1) listen: sets up the listener and waits for a connection attempt
2) Opponent connects
3) You connect to the opponent which his "connect" mode terminated and a
listener is already sat up there for you.

When using "connect", the reverse of everything you've just read happens.
Of course you have to write your IP address and port number and the opponent's
too. You will encounter four input prompts related to connections(two IPs
and two port numbers).

syntax: [PROGRAM_NAME] [INITIAL_MODE]

Now we are done with the connection, let's move on to the chessboard.
A fifth input prompt will be printed for you to choose what character will 
the columns be written in. Then, The board will be shown and depending on
if you're white or black, you will be waiting for a move or it's your turn.

Although when taking a move you will be prompted by the piece type, it's totally
fine to write anything here, because nothing is used to process (handle) the
piece type. This is just a reminder for you to remember what are you moving.
But the current and next location values are critical. They have to take
this syntax: [COLUMN][RANK] (no space between the two).
examples: g8,d4,e1
because it's a No-Rules chess game, whatever location you specify will be used
to overwrite the next location you typed. So if you specify a location that
has no piece and a next location that has a piece, the piece will disappear.
And you can move your opponent's pieces or kill his king and continue, and you
can let the rook jump over pieces, You can do whatever you want, have fun.

If you want to use the game over WAN (Internet), it needs port forwarding on
both ends. This will be your responsibility.

PART TWO

I'm sure you will ask: what's the purpose of such game? or: why not make it
better with GUI and Rules?

The answer is because this project was a practice for me, and the main point of practice is not playing chess, but the logical steps for movement and locating pieces. It's not on my list
of serious automation scripts. But I gained a lot of experience doing it even
though it's just for fun. I'm not even into game development and GUI stuff.
I'm going the exact opposite way, and I chose a chess game because I like chess
more than anyone in the modern world. You can notice that this game can't be 
played without you and your friend chatting and deciding to play. Plus you 
have to exchange public IPs and decide what port numbers will be used. I hope
you read until here, thank you very much and enjoy my weird chess game.
