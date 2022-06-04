<h1>Love Letter Card Game</h1>
<p>Love Letter is a classic card game, where the players try to get the attention of a princess who locked herself in a tower. Players play cards to gain as much favor from the princess while also limiting your opponents to do the same. This program will replicate this game, with a single player playing against 1 to 3 AI players.</p>

<h2>Running the Program</h2>
<p>Running is really simple. On repl.it, hit the green 'run' button at the top of the window. The game is played via strings and messages, so open the console and follow the play instructions.</p>

<h3>The Main Menu</h3>
<p>The first thing you will see is a menu with three options: Play the game, print instructions, and quit thr game. Each option will have a number beside it. To use the desired option, type in the number beside the option and press 'enter'. Make sure you type it in correctly, otherwise you will be prompted to give a valid option.</p>
<p>The play game option will begin the game. Before playing, you will be asked to enter a series of options to set up the game, which are listed below.</p>
<p>The Print Instructions option will print out the basic rules of the game and the card functions, which are also stated on this file.</p>
<p>Finally, the Quit the Game function will end the program and print a message to the user.</p>

<h2>Playing the Game</h2>
<p>You will always have one card in your hand, and your opponents will also have one card in their hand. The cards are all initially hidden from you. All players will start with 0 favor tokens. Upon winning a round, a player will receive a favor token. Once a player has a set amount of favor tokens, they will the game.</p>
<h3>Setup Instructions</h3>
<p>When you press the Play the Game option from the main menu, the game will ask you how many players that you want to play against. This is the total amount of players, not the AI players. Type a number between 2 and 4. Then, the console will ask for your username. Type in what you want to be known as. Afterwards, you can shuffle the deck. You can shuffle the deck as many times as you would like, however, it is recommended that you shuffle it at least once. Afterwards, the game will be set up. The game will begin on your turn, followed by the AI players.</p>
<h3>On Your Turn</h3>
<p>The first thing you do on your turn is to draw a card from the main deck. You then must play one card. Each card you play will have a different effect, which will be listed below. The card you play will then be discarded and will be known to the other players. The next player will then play their turn.</p>
<p>Cards will have various effects, from looking, comparing or trading hands with other players, eliminating other players from the round or forcing other players or yourself to take certain actions.</p>
<h3>If you are eliminated</h3>
<p>Some cards will eliminate you from the round. If this happens, you discard your hand and let the other players know what the card is. You cannot play any turns if you are eliminated from the round, though you do rejoin when a new round starts.</p>
<h3>When is a round over?</h3>
<p>A round is over when there is only one player left in the round who is not eliminated or the deck runs out.</p>
<p>If there is one player left, they gain a favor token and a new round begins.</p>
<p>If the deck runs out, all remaining players compare hands. The player with the highest strength card will gain a favor token. A new round will then begin.</p>
<h3>When does the game end?</h3>
<p>The game ends when a player reaches the required amount of favor tokens. In a four player game, the first player to reach 4 favor tokens wins the game. In a three player game, the first player to reach 5 favor tokens wins the game. In a two player game, the first player to reach 7 favor tokens wins the game.</p>

<h2>Cards</h2>
<p>In each deck, there are 16 cards: 5 Guards, 2 Priests, 2 Barons, 2 Handmaids, 2 Princes, a King, a Countess and a Princess. All these cards have their own effect and their own strength.</p>
<h3>Card Appendix</h3>
<p>Below are the type of cards, their strength's, and their abilities.</p>
<ul>
  <li><strong>Guard [Str: 1]: </strong>The player who played this card must choose a player (if applicable) and guess a card other than a guard that is in the player's hand. If the chosen player has that card, they are eliminated from the round.</li>
  <li><strong>Priest [Str: 2]: </strong>The player who played this card must choose a player (if applicable). That player can see the chosen player's hand.</li>
  <li><strong>Baron [Str: 3]: </strong>The player who played this card must choose a player (if applicable). The current player sees the strength of the chosen player's card. Whoever has the weaker card is eliminated from the round.</li>
  <li><strong>Handmaid [Str: 4]: </strong>The player who played this card cannot be targeted by any players until their next turn.</li>
  <li><strong>Prince [Str: 5]: </strong>The player who played this card must choose any player including themselves to discard their card and draw a new one.</li>
  <li><strong>King [Str: 6]: </strong>The player who played this card must choose any player (if applicable). Both players trade their hands with each other.</li>
  <li><strong>Countess [Str: 7]: </strong>The card does nothing when played. However, if the player also has a Prince or King, this card must be played.</li>
  <li><strong>Princess [Str: 8]: </strong>The strongest card in the game. If you discard this card in any way, you are eliminated from the round.</li>
</ul>