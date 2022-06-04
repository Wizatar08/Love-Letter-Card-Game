
# Imports
import colorama
from colorama import Fore
import random
import time

import helperFunctions as helper

# Create global variables
PLAYERS = []
DECK = []
CURRENT_PLAYER_INDEX = 0;

# Card class - stores the main functions of the card subclass
class Card(object):

  # Initialize card attributes (name and strength)
  def __init__(self, name, strength):
    self.name = name; 
    self.strength = strength;

  # Superclass 'play' - will run when a player plays a card
  def play(self, player, playerList):
    pass;

  # Superclass 'onDiscard' - will run when a player discards the card
  def onDiscard(self, player):
    pass;

  # Superclass 'mustBePlayed' - will run before a player's turn to see if the card must be played
  def mustBePlayed(self, player):
    return False;

  # GETTER FUNCTIONS - Get the object's attributes
  def getStrength(self):
    return self.strength;

  def getName(self):
    return self.name

# Guard - subclass of Card
class Guard(Card):

  def __init__(self):
    super().__init__('Guard', 1); # Initialize

  def play(self, player, playerList):
    playerList.remove(player); # Remove this player from playerList

    # Initialize targeting variables
    targetPlayer = '';
    guessStrength = '';
    targetCard = '';
    if len(playerList) > 0: # If there are targetable players
      if player.isAI: # If the player is a computer
        memory = player.getMemory(); # Get the computer's memory
        if len(memory) > 0: # If there is something in memory
          for loopPlayer, loopCard in memory.items(): # Loop through memory
            if not loopPlayer.isImmune() and loopCard.getStrength() != 1: # If the player is targetable and they don't have a Guard
              targetPlayer = loopPlayer; # Target that player and their card
              targetCard = loopCard;
              guessStrength = targetCard.getStrength();
          if targetPlayer != '': # After looping through memory, if there is a target
            player.forget(targetPlayer) # Remove that player from memory
        if targetPlayer == '': # Randomly choose a player if there is no target up to this point
          targetPlayer = random.choice(playerList);
          guessStrength = random.randint(2, 8);
      else: # If the player is a human
        print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
        for i in range(len(playerList)): # Loop through playerList, listing players that can be targeted
          print('[%s] ==> %s' % (i + 1, playerList[i].getName()))
        targetPlayerNum = input("Please enter your target (type in one of the numbers specified for each opponent): ") # Ask user for input
        allowedValues = []
        for i in range(len(playerList)): # Allow user to input a number based on the amount of players available for targeting
          allowedValues.append(str(i + 1))
        while not helper.checkInput(targetPlayerNum, allowedValues): # if player did not enter a valid input, ask again
          targetPlayerNum = input("Invalid input. Please enter your target: ")
        targetPlayer = playerList[int(targetPlayerNum) - 1]; # Set the target player to the user input
        print('[2] --> Priest\n[3] --> Baron\n[4] --> Handmaid\n[5] --> Prince\n[6] --> King\n[7] --> Countess\n[8] --> Princess') # Print the available card options
        guessStrength = input("What card do you think %s has? " % (targetPlayer.getName())); # Get card guess from user
        while not helper.checkInput(guessStrength, ['2', '3', '4', '5', '6', '7', '8']): # Check if user input is valid, if not, continue asking
          guessStrength = input("Invalid input. What card do you think %s has? " % (targetPlayer.getName()));
        
        guessStrength = int(guessStrength);
      print("Player %s targeted %s and guessed that they have a %s in their hand." % (player.getName(), targetPlayer.getName(), str(guessStrength))) # Print message
      actualCardStrength = targetPlayer.getHand()[0].getStrength(); # Get the strength of the targeted player's hand
      if actualCardStrength == guessStrength: # Is the targeted player's card the same as the guessed card?
        targetPlayer.removeFromRound(); # Remove the player from the round
      else: # Otherwise
        print("%s failed to guess %s's hand." % (player.getName(), targetPlayer.getName())); # Print that the player failed to guess the target's hand
    else: # If there are no available player's to target
      print("You cannot choose any players (all remaining opponents are immune to effects)"); # Print that the player cannot target anyone

# Priest - subclass of Card
class Priest(Card):

  def __init__(self):
    super().__init__('Priest', 2);

  def play(self, player, playerList):
    playerList.remove(player); # Remove this player from playerList
    if len(playerList) > 0: # If there are available players to target
      if player.isAI: # If this player is a computer
        targetPlayer = random.choice(playerList); # Randomly target a player
        card = targetPlayer.getHand()[0]; # Get their card
        player.remember(targetPlayer, card) # Add the player and the card to the player's memory
        print('%s looked at %s\'s hand' % (player.getName(), targetPlayer.getName())) # Print their actions to the console
      else: # if this player is a human
        print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
        for i in range(len(playerList)): # Print the available targets to the console
          print('[%s] ==> %s' % (i + 1, playerList[i].getName()))
        targetPlayerNum = input("Please enter a target to see their hand (type in one of the numbers specified for each opponent): ") # Ask the user for a target
        allowedValues = []
        for i in range(len(playerList)): # Add the targetable players into a list of indexes
          allowedValues.append(str(i + 1)) 
        while not helper.checkInput(targetPlayerNum, allowedValues): # Check if the user inputted a correct value, if not, ask again
          targetPlayerNum = input("Invalid input. Please enter your target: ")
        targetPlayer = playerList[int(targetPlayerNum) - 1]; # Use the inputted number to target teh appropriate player
        print('%s\'s card is a %s (Strength: %s)' % (targetPlayer.getName(), targetPlayer.getHand()[0].getName(), targetPlayer.getHand()[0].getStrength())) # Print the targeted player's card to the console
    else: # If there are no targetable players
      print("You cannot choose any players (all remaining opponents are immune to effects)"); # Print to the console

# Baron - subclass of Card
class Baron(Card):

  def __init__(self):
    super().__init__('Baron', 3);

  def play(self, player, playerList):
    playerList.remove(player); # Remove this player from playerList
    if len(playerList) > 0: # if there are targetable players
      targetPlayer = '' # Initialize local variables
      yourStrength = 0;
      for card in player.getHand(): # Get the other card in your hand's strength
        if card != self:
          yourStrength = card.getStrength();
      if player.isAI: # If the player is a computer
        memory = player.getMemory(); # Get the memory of the player
        if len(memory) > 0: # If there is something in the player's memory
          for playerLoop, card in memory.items(): # Loop through everything in the player's memory
            if not playerLoop.isImmune() and card.getStrength() < yourStrength: # If the player is targetable and their card strength is less than your card strength
              targetPlayer = playerLoop; # Target that player
        if targetPlayer == '': # If a player has not been chosen at this point
          targetPlayer = random.choice(playerList); # Select a random player
      else: # If the player is a human
        print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
        for i in range(len(playerList)): # Print the targetable players into the console
          print('[%s] ==> %s' % (i + 1, playerList[i].getName()))
        targetPlayerNum = input("Please enter your target to compare hands (type in one of the numbers specified for each opponent): ") # Ask user to target a user
        allowedValues = []
        for i in range(len(playerList)): # Create list of allowed inputs the user can input, based on the amount of targetable players
          allowedValues.append(str(i + 1))
        while not helper.checkInput(targetPlayerNum,allowedValues): # Check if the user inputted a valid value, if not ask user for input again
          targetPlayerNum = input("Invalid input. Please enter your target: ")
        targetPlayer = playerList[int(targetPlayerNum) - 1]; # Set the targeted player to a player from the playerList based on the user inputted index
      print('%s targeted %s' % (player.getName(), targetPlayer.getName())) # Print the user's actions
      if yourStrength > targetPlayer.getHand()[0].getStrength(): # If your strength is greater than the targeted player's strength, eliminate the targeted player, otherwise, if their strength is greater than your's, eliminate yourself. If strengths are tied, nothing happens
        targetPlayer.removeFromRound();
      elif yourStrength < targetPlayer.getHand()[0].getStrength():
        player.removeFromRound();
    else: # Print to the console if there are no targetable players
      print("You cannot choose any players (all remaining opponents are immune to effects)");

# Handmaid - subclass of Card
class Handmaid(Card):

  def __init__(self):
    super().__init__("Handmaid", 4);

  def play(self, player, playerList):
    player.setImmunity(True); # Make the player immune and print to the console
    print('%s is now immune to all effects until their next turn' % (player.getName()))

class Prince(Card):
  
  def __init__(self):
    super().__init__("Prince", 5);

  def play(self, player, playerList):
    targetPlayer = '' # Initialize targetPlayer
    if player.isAI: # If this player is a computer
      memory = player.getMemory(); # Get player memory
      if len(memory) > 0: # If the computer remembers something
        for loopPlayer, card in memory.items(): # Loop through all it's memories
          if not loopPlayer.isImmune() and card.getStrength() == 8: # If the computer thinks a player has the princess and is not immune to effects
            targetPlayer = loopPlayer; # Target that player
      if targetPlayer == '': # If the computer did not choose anyone
        for card in player.getHand(): # If the player holds the princess, make sure the computer does not pick itself to target
          if card.getStrength() == 8:
            playerList.remove(player);
        if len(playerList) > 0: # At this point, if there are targetable players, choose one randomly
          targetPlayer = random.choice(playerList);
      else:
        player.forget(targetPlayer); # Forget the player from the computer's memory
    else:
      print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
      for i in range(len(playerList)): # Print targetable players to the console
        print('[%s] ==> %s' % (i + 1, playerList[i].getName()))
      targetPlayerNum = input("Please enter your target, which includes yourself, to forcefully discard their hand (type in one of the numbers specified for each opponent): ") # Ask player for target
      allowedValues = []
      for i in range(len(playerList)): # Create list of targetable players
        allowedValues.append(str(i + 1))
      while not helper.checkInput(targetPlayerNum, allowedValues): # If the player did not input a valid value, ask again
        targetPlayerNum = input("Invalid input. Please enter your target: ")
      targetPlayer = playerList[int(targetPlayerNum) - 1]; # Set the target to the user-inputted index
    print('%s forced %s to discard their hand and draw a new card. They discarded a %s.' % (player.getName(), targetPlayer.getName(), targetPlayer.getHand()[0].getName())) # Print to console
    targetPlayer.removeCard(targetPlayer.getHand()[0], True) # Discard the target player's hand
    
    if targetPlayer.inRound: # If the target is not eliminated, give them another card
      givePlayerCard(targetPlayer);

class King(Card):

  def __init__(self):
    super().__init__("King", 6)

  def play(self, player, playerList):
    playerList.remove(player); # Remove the current player from the targetable players list
    if len(playerList) > 0: # If there is a targetable player
      targetPlayer = ''; # Init variable
      if player.isAI: # If player is a computer
        memory = player.getMemory(); # Get the player's memory
        if len(memory) > 0: # If there is something in the player's memory
          for playerLoop, card in memory.items(): # Loop through memory
            if not playerLoop.isImmune() and card.getStrength() == 1: # If it finds a player with a guard and the player is targetable
              targetPlayer = playerLoop; # Set the target player to that player
        if targetPlayer == '': # If the computer did not target anyone yet
          targetPlayer = random.choice(playerList); # Randomly choose a player
      else: # If player is human
        print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
        for i in range(len(playerList)): # Print available targets to the console
          print('[%s] ==> %s' % (i + 1, playerList[i].getName()))
        targetPlayerNum = input("Please enter your target to swap hands with (type in one of the numbers specified for each opponent): ") # Ask user for input
        allowedValues = []
        for i in range(len(playerList)): # Create list of targetable players
          allowedValues.append(str(i + 1))
        while not helper.checkInput(targetPlayerNum, allowedValues): # If the player did not input a valid input, ask again
          targetPlayerNum = input("Invalid input. Please enter your target: ")
        targetPlayer = playerList[int(targetPlayerNum) - 1]; # Set target to the user-inputted index
      print('%s swapped hands with %s' % (player.getName(), targetPlayer.getName())) # Print to console

      # Get the hands of the player and the target
      currPlayerHand = player.getHand(); 
      targetPlayerHand = targetPlayer.getHand();

      # Swap hands by giving the player the target's card and giving the target the player's card, then removing the original cards from both players
      player.addToHand(targetPlayerHand[0]);
      targetPlayer.addToHand(currPlayerHand[0]);
      targetPlayer.removeCard(targetPlayerHand[0], False);
      player.removeCard(currPlayerHand[0], False);
      if player.isAI: # If the player is a computer, remember what they just had under the target
        player.remember(targetPlayer, targetPlayer.getHand()[0])    
    else: # If there are no targetable players, print to the console
      print("You cannot choose any players (all remaining opponents are immune to effects)");

class Countess(Card):

  def __init__(self):
    super().__init__("Countess", 7);

  def mustBePlayed(self, player):
    hasRequiredCards = False; # Init variable
    for card in player.getHand(): # Loop through player's hand
      if card.getStrength() == 6 or card.getStrength() == 5: # If the player holds a King or Prince
        hasRequiredCards = True; # Set the playing requirement to True
    return hasRequiredCards; # Return

class Princess(Card):

  def __init__(self):
    super().__init__("Princess", 8);

  def onDiscard(self, player):
    player.removeFromRound(); # If the player discards this card in any way, eliminate them from the round


# Player object - what makes and controls all players
class Player(object):

  def __init__(self, name, isAI):
    # Initiate local variables
    self.name = name;
    self.isAI = isAI;
    self.hand = [];
    self.inRound = True;
    self.favor = 0;
    self.immunity = False;
    self.cardMemory = {};
    self.discardedCards = [];

  def addToHand(self, card): # Add card to hand
    self.hand.append(card) # Add card to player's hand

  def removeCard(self, card, discardEffect): # Remove card from hand
    if discardEffect: # If a discard effect should be played
      self.discardedCards.append(card); # Add it to the discarded cards list
      card.onDiscard(self); # Play discard effect
    if card in self.hand: # If the card is in player's hand (used to avoid errors)
      self.hand.remove(card); # Remove from hand

  def removeFromRound(self): # Eliminate player
    global PLAYERS;
    print(Fore.RED + colorama.Style.BRIGHT + '%s was eliminated from this round!' % (self.name) + colorama.Style.RESET_ALL) # Print to console
    print(Fore.YELLOW + "%s discarded a %s" % (self.name, self.hand[0].getName() + Fore.RESET)); # Print discarded card to console
    self.inRound = False; # Set matching variable to false
    for player in PLAYERS: # Make all the AI players forget the player
      if self in player.getMemory():
        player.forget(self);

  def gainFavor(self): # Give player a favor token
    self.favor = self.favor + 1;
        
  def setImmunity(self, setImmune): # Set player's immunity to the passed in boolean
    self.immunity = setImmune;

  def remember(self, playerObject, cardObject): # Add a player and card to AI player's memory
    self.cardMemory[playerObject] = cardObject;

  def forget(self, playerObject): # Remove a player and card from AI player's memory
    self.cardMemory.pop(playerObject);

  def resetOnNewRound(self): # Reset variables and clear lists when a new round starts
    self.immunity = False; 
    self.cardMemory.clear();
    self.discardedCards.clear();
    self.hand.clear();
    self.inRound = True;

  # GETTER FUNCTIONS:
  
  def getHand(self):
    return self.hand;

  def inRound(self):
    return self.inRound;

  def getFavor(self):
    return self.favor;

  def isAI(self):
    return self.isAI;

  def isImmune(self):
    return self.immunity;

  def getMemory(self):
    return self.cardMemory;

  def getDiscardedCards(self):
    return self.discardedCards;

  def getName(self):
    return self.name;

  def __repr__(self):
    return 'Player(%s)' % (self.name)


# MAIN GAME FUNCTIONS:

def getRemainingPlayers(): # Get all players still in the round
  global PLAYERS;
  remainingPlayers = [] # Make an empty list
  for player in PLAYERS: # Loop through all players
    if player.inRound: # If the player is still in the round
      remainingPlayers.append(player) # Add to list
  return remainingPlayers; # Return the list

def getApplicablePlayers(playerList): # GEt all targetable players from list
  applicablePlayers = [];
  for player in playerList: # Loop through all players
    if not player.isImmune(): # If the player is not immune (from handmaid effect)
      applicablePlayers.append(player); # Add to list
  return applicablePlayers; # Return list

def givePlayerCard(player): # Give a player a card
  global DECK;
  if len(DECK) > 0: # If there is something in the main deck
    player.addToHand(DECK[0]) # Give player the top card
    DECK.pop(0); # Remove top card from deck

def endGame(winningPlayer): # Called when the game is ending
  global PLAYERS;
  print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
  print('Congratulations %s, you have won the game!' % (winningPlayer.getName())); # Display to console who won the game
  print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
  mainMenu(); # Display the main menu

def endRound(remainingPlayerList): # Called when the round is ending
  global PLAYERS;
  print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
  if len(remainingPlayerList) == 1: # If only one player is still in the round
    remainingPlayerList[0].gainFavor(); # Give that playera favor token
    print(Fore.LIGHTBLUE_EX + remainingPlayerList[0].getName() + Fore.RESET + ' is the last person remaining and gained attention from the princess. They have gained one favor token.') # Print the console
  else: # If there are multiple players still in the round
    print(Fore.YELLOW + 'The deck has run out!' + Fore.RESET) # Print that te deck ran out
    strongestPlayer = remainingPlayerList[0]; # Set a new variable, set it to the first player in the list of reaining players
    for player in remainingPlayerList: # Loop throgh the remaining players
      if len(player.getHand()) > 0: # If there is something in the player's hand
        if player.getHand()[0].getStrength() > strongestPlayer.getHand()[0].getStrength(): # If the looped player has a greater strength that the strongest player
          strongestPlayer = player; # Set the strongest player to the looped player
    strongestPlayer.gainFavor(); # GIve the strongest player a favor token
    print(Fore.LIGHTBLUE_EX + strongestPlayer.getName() + Fore.RESET + ' has the best card out of the remaining players. They have gained one favor token.') # Print the console
  mostFavoredPlayer = PLAYERS[0] # Create a new variable which will store the most favored player
  for player in PLAYERS: # Loop through players
    if player.getFavor() > mostFavoredPlayer.getFavor(): # If the looped player has more favor than the most favored player, set the most favored player to the looped player
      mostFavoredPlayer = player;
  print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
  print(Fore.CYAN + 'FINAL PLAYER HANDS:') # Print list header to console
  for player in PLAYERS: # Loop through all players
    if player.inRound: # If the player is still in the round
      if len(player.getHand()) > 0: # If there is something in their hand
        print('%s: %s' % (player.getName(), player.getHand()[0].getName())); # Print the player and their hand to the console
      else: # If there is nothing in their hand
        print('%s: N/A' % (player.getName())); # Print the player to the console, and print that they have nothing in their hand
    else: # If the player is not in the round
      print('%s: ELIMINATED' % (player.getName())) # Display that to the console
  print(Fore.LIGHTYELLOW_EX + "\nCURRENT STANDINGS:") # Print list header
  for player in PLAYERS: # Loop through all players
    print('%s: %s' % (player.getName(), player.getFavor())) # Print the player and their favor to the console
  print(Fore.RESET)
  if (len(PLAYERS) == 4 and mostFavoredPlayer.getFavor() >= 4) or (len(PLAYERS) == 3 and mostFavoredPlayer.getFavor() >= 5) or (len(PLAYERS) == 2 and mostFavoredPlayer.getFavor() >= 7): # If the most favored player has the required amount of favor to win the game
    endGame(mostFavoredPlayer); # End the game, passing in the winning player
  else: # If there needs to be another round
    input("Press ENTER to continue.") # Ask user to contine
    setupRound(); # Make another round

def playTurn(player): # Function run when it is a player's turn
  print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET);
  print("It is %s's turn! " % (player.getName()))
  global PLAYERS, DECK, CURRENT_PLAYER_INDEX;
  print(Fore.YELLOW)
  print('%s picked up a card. There are now %s cards left in the deck!' % (player.getName(), str(len(DECK) - 1))) # Print the amount of cards still in the deck
  print(Fore.RESET)
  player.setImmunity(False); # Set the player's immunity to False
  givePlayerCard(player); # Give the player a new card
  targetCard = '' # Init variable targetCard
  for card in player.getHand(): # For each card, make sure the card does not need to be played. If a card must be played, set the targetCard to that
    if card.mustBePlayed(player):
      targetCard = card;
  if targetCard == '': # If a card is not needed to be played
    if player.isAI: # If the player is an AI
      targetCard = random.choice(player.getHand()); # Randomly select a card from hand
      while targetCard.getStrength() == 8: # Choose another card if they choose the princess
        targetCard = random.choice(player.getHand())
    else: # if the player is human
      for i in range(len(player.getHand())): # Print the cards to the console
        print('[%s] ==> %s (%s)' % (i + 1, player.getHand()[i].getName(), player.getHand()[i].getStrength()));
      playerChoice = input("Please select which card you would like to play: "); # Get player to input the card they want to play
      while not helper.checkInput(playerChoice, ['1', '2']): # WHile the player did not input a valid input, make them choose again
        playerChoice = input("Invalid input. Please select which card you would like to play: ");
      targetCard = player.getHand()[int(playerChoice) - 1]; # Set the target card to the player's choice
  print("%s played a %s" % (player.getName(), targetCard.getName())) # Print to console
  player.removeCard(targetCard, True); # Discard the card
  targetCard.play(player, getApplicablePlayers(getRemainingPlayers())) # Play the card
  if len(getRemainingPlayers()) == 1 or len(DECK) == 0: # If there is one player left or the deck has run out, end the round
    endRound(getRemainingPlayers())
  else: # Otherwise
    foundPlayer = False; # Init variables
    player = '';
    while not foundPlayer: # Loop through playerList until the next non-eliminated player is found
      CURRENT_PLAYER_INDEX += 1;
      if CURRENT_PLAYER_INDEX >= len(PLAYERS): # If the index exceeds the size of the list, bring it back to 0
        CURRENT_PLAYER_INDEX = 0;
      if PLAYERS[CURRENT_PLAYER_INDEX].inRound: # IF the looped player is not eliminated
        player = PLAYERS[CURRENT_PLAYER_INDEX] # Set the player to that
        foundPlayer = True;
    time.sleep(5) # Wait 5 seconds
    playTurn(player); # Play the next player's turn

def setupRound(): # When a round is about to begin, run this code
  global PLAYERS, DECK, CURRENT_PLAYER_INDEX
  DECK = createDeck(); # Create the deck
  continueShuffling = True; # Initialize variable - determines whether the deck should be shffled
  while continueShuffling: # If the deck should continue to be shuffled
    shouldShuffle = input('Would you like to shuffle the deck? (Type Y or N) ') # Ask user if the deck should be shuffled
    while not helper.checkInput(shouldShuffle, ['Y', 'N']): # If the user inputs an invalid input, keep asking
      shouldShuffle = input("Invalid input. Would you like to shuffle the deck? ")
    if shouldShuffle == 'Y': # If the user wants to shuffle, shuffle the deck
      DECK = shuffleDeck(DECK);
    else: # If the user does not want to shuffle, break the loop
      continueShuffling = False;
  for player in PLAYERS: # Reset the stats for all players and give them each a card
    player.resetOnNewRound();
    givePlayerCard(player);
  CURRENT_PLAYER_INDEX = 0; # Start with the first player
  playTurn(PLAYERS[0]); # Play the first player's turn
  
def createDeck(): # Create the deck
  deck = []; # Make a new empty list

  # Add 5 guards, 2 priests, 2 barons, 2 handmaids, 2 princes, a king, a countess and a princess to the deck
  for i in range(5):
    deck.append(Guard());
  for i in range(2):
    deck.append(Priest());
  for i in range(2):
    deck.append(Baron());
  for i in range(2):
    deck.append(Handmaid());
  for i in range(2):
    deck.append(Prince())
  deck.append(King())
  deck.append(Countess())
  deck.append(Princess())
  return deck; # Return the deck

def shuffleDeck(deck): # Shuffle the deck
  shuffledDeck = []; # Create new empty list
  currDeck = deck; # Create new list with values from 'deck' passed through
  while len(currDeck) > 0: # While currDeck has items inside
    ind = random.randint(0, len(currDeck) - 1); # Pick a random number between 0 and the length of currDeck-1
    card = currDeck[ind]; # Get the card corresponding to the index
    shuffledDeck.append(card); # Add this card to shuffledDeck
    currDeck.pop(ind); # Remove this card from currDeck
  return shuffledDeck; # Return shuffledDeck

def setupGame(): # Set up the game
  global PLAYERS;
  PLAYERS = [] # Make list of players
  
  players = input("How many players will be in the game? (Choose a number between 2 and 4) "); # Ask how many players will play
  while not helper.checkInput(players, ['2', '3', '4']): # If the input is not 2, 3 or 4, ask again
    players = input("Invalid input. How many players will be in the game?")
  username = input("What would you like to be known as? "); # Ask what the player user should be called
  PLAYERS.append(Player(username, False)) # Add this as a human player
  for i in range(int(players) - 1): # Add the rest of the players as AI players
    PLAYERS.append(Player("AI player " + str(i + 1), True));
  setupRound() # Set up the first round

def printInstructions(): # Print the rules of the game
  print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
  print(Fore.RED + '❤️  Love Letter Card Game ❤️\n' + Fore.RESET);
  print('Love Letter is a classic card game, where the players try to get the attention of a princess who locked herself in a tower. Players play cards to gain as much favor from the princess while also limiting your opponents to do the same. This program will replicate this game, with a single player playing against 1 to 3 AI players.\n\n')
  print(Fore.RED + '❤️  Playing the Game ❤️\n' + Fore.RESET);
  print('You will always have one card in your hand, and your opponents will also have one card in their hand. The cards are all initially hidden from you. All players will start with 0 favor tokens. Upon winning a round, a player will receive a favor token. Once a player has a set amount of favor tokens, they will the game.\n\n')
  print(Fore.RED + ' ==> Setup Instructions:\n' + Fore.RESET);
  print('When you press the Play the Game option from the main menu, the game will ask you how many players that you want to play against. This is the total amount of players, not the AI players. Type a number between 2 and 4. Then, the console will ask for your username. Type in what you want to be known as. Afterwards, you can shuffle the deck. You can shuffle the deck as many times as you would like, however, it is recommended that you shuffle it at least once. Afterwards, the game will be set up. The game will begin on your turn, followed by the AI players.\n\n')
  print(Fore.RED + ' ==> On Your Turn:\n' + Fore.RESET);
  print('The first thing you do on your turn is to draw a card from the main deck. You then must play one card. Each card you play will have a different effect, which will be listed below. The card you play will then be discarded and will be known to the other players. The next player will then play their turn.')
  print('Cards will have various effects, from looking, comparing or trading hands with other players, eliminating other players from the round or forcing other players or yourself to take certain actions.\n\n')
  print(Fore.RED + ' ==> If You Are Eliminated:\n' + Fore.RESET);
  print('Some cards will eliminate you from the round. If this happens, you discard your hand and let the other players know what the card is. You cannot play any turns if you are eliminated from the round, though you do rejoin when a new round starts.\n\n')
  print(Fore.RED + ' ==> When is a Round Over?\n' + Fore.RESET);
  print('A round is over when there is only one player left in the round who is not eliminated or the deck runs out.');
  print('If there is one player left, they gain a favor token and a new round begins.');
  print('If the deck runs out, all remaining players compare hands. The player with the highest strength card will gain a favor token. A new round will then begin.\n\n');
  print(Fore.RED + ' ==> When Does the Game End?\n' + Fore.RESET);
  print('The game ends when a player reaches the required amount of favor tokens. In a four player game, the first player to reach 4 favor tokens wins the game. In a three player game, the first player to reach 5 favor tokens wins the game. In a two player game, the first player to reach 7 favor tokens wins the game.\n\n')
  print(Fore.RED + '❤️  Cards ❤️\n' + Fore.RESET);
  print('In each deck, there are 16 cards: 5 Guards, 2 Priests, 2 Barons, 2 Handmaids, 2 Princes, a King, a Countess and a Princess. All these cards have their own effect and their own strength.\n\n')
  print(Fore.RED + ' ==> Card appendix:\n' + Fore.RESET);
  print('''Guard [Str: 1]: The player who played this card must choose a player (if applicable) and guess a card other than a guard that is in the player's hand. If the chosen player has that card, they are eliminated from the round.
        
Priest [Str: 2]: The player who played this card must choose a player (if applicable). That player can see the chosen player's hand.
        
Baron [Str: 3]: The player who played this card must choose a player (if applicable). The current player sees the strength of the chosen player's card. Whoever has the weaker card is eliminated from the round.
        
Handmaid [Str: 4]: The player who played this card cannot be targeted by any players until their next turn.
        
Prince [Str: 5]: The player who played this card must choose any player including themselves to discard their card and draw a new one.
        
King [Str: 6]: The player who played this card must choose any player (if applicable). Both players trade their hands with each other.
        
Countess [Str: 7]: The card does nothing when played. However, if the player also has a Prince or King, this card must be played.
        
Princess [Str: 8]: The strongest card in the game. If you discard this card in any way, you are eliminated from the round.
        ''')
  mainMenu(); # Show the main menu

def mainMenu(): # Show main game options and process user input
  print(Fore.LIGHTBLACK_EX + "=================================================" + Fore.RESET)
  print("Main menu:\n[1] ==> Play the game\n[2] ==> Print instructions\n[3] ==> Quit the game") # Print menu
  playerInput = input("What would you like to do? ") # Ask user what they want to do
  while not helper.checkInput(playerInput, ['1', '2', '3']): # If the user inputted an invalid input, ask again
    playerInput = input("Invalid input. What would you like to do? ")
  if playerInput == '1': # Start the game if player inputs 1
    setupGame();
  elif playerInput == '2': # Print rules if player inputs 2
    printInstructions();
  elif playerInput == '3': # Quit the game if player inputs 3
    print("Thanks for playing, goodbye!")

mainMenu(); # Print the main menu for the first time