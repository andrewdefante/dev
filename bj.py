"""
write blackjack so we can play it
"""

# import packages
import random


# define pre-existing values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two' : 2, 'Three' : 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True

# define classes

class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank

	def __str__(self): 
		return self.rank + ' of ' + self.suit

	def show(self):
		print("{} of {}".format(self.rank, self.suit))

class Deck:
	def __init__(self):
		self.deck = []
		self.build()

	def build(self):
		for s in suits:
			for r in ranks:
				self.deck.append(Card(s, r))

	def shuffle(self):
		random.shuffle(self.deck)

	def show(self):
		for d in self.deck:
			d.show()

	def deal(self):
		return self.deck.pop()

class Hand:
	def __init__(self):
		self.hand = []
		self.value = 0
		self.aces = 0

	def add_card(self, card):
		self.hand.append(card)
		self.value += values[card.rank]
		if card.rank == 'Ace':
			self.aces += 1 

	def adjust_ace(self):
		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1

class Chips:
	def __init__(self):
		self.total = 100
		self.bet = 0

	def win(self):
		self.total += self.bet*2

	def lose(self):
		self.total -= self.bet*2

# define actions
def place_bet(chips):

	while True:
		try:
			chips.bet = int(input("How many chips you wanna bet?"))
		except ValueError:
			print("Please try again")
		else: 
			if chips.bet > chips.total:
				print("You don't have enough chips :(")
			else:
				break

def hit(deck, hand):
	hand.add_card(deck.deal())
	hand.adjust_ace()

def hit_or_stay(deck, hand):
	global playing 

	while True:
		ask = input("would you like to hit? Please enter 'y' or 'n':")

		if ask[0] == 'y':
			hit(deck, hand)
		elif ask[0] == 'n':
			print("Player stays, dealer keeps playing")
			playing = False
		else:
			print("try again")
			continue
		break

def table_show(player, dealer):
	print("\n Dealer has: ")
	print(dealer.hand[1], "<card hidden>")
	print("\n Player has: ")
	print(*player.hand)

def hand_show(player, dealer):
	print("\n Dealer has: ")
	print(*dealer.hand, dealer.value)
	print("\n Player has: ")
	print(*player.hand, player.value)


# define outcomes

def player_bust(player, dealer, chips):
	print("you busssed")
	chips.lose()

def dealer_bust(player, dealer, chips):
	print("dealer bussed, you win")
	chips.win()

def push(player, dealer, chips):
	print("push, nobody wins")

def player_win(player, dealer, chips):
	print("you win")
	chips.win()

def dealer_win(player, dealer, chips):
	print("you lose")
	chips.lose()

# get to gameplay

while True:

	print("Welcome Cruz Casino Online")

	# shuffle cards
	deck = Deck()
	deck.shuffle()

	# ask and then place bet
	player_chips = Chips()
	place_bet(player_chips)

	# cards get dealt
	player_hand = Hand()
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal())

	dealer_hand = Hand()
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal())

	# show table
	table_show(player_hand, dealer_hand)

	# hit or stay
	while playing:

		hit_or_stay(deck, player_hand)
		table_show(player_hand, dealer_hand)

		if player_hand.value > 21:
			player_busts(player_hand, dealer_hand, player_chips)
			break

	if player_hand.value <= 21:

		while dealer_hand.value < 17:
			hit(deck, dealer_hand)

		hand_show(player_hand, dealer_hand)

		if dealer_hand.value > 21:
			dealer_busts(player_hand, dealer_hand, player_chips)

		elif dealer_hand.value > player_hand.value:
			dealer_win(player_hand, dealer_hand, player_chips)

		elif dealer_hand.value < player_hand.value:
			player_win(player_hand, dealer_hand, player_chips)

		elif dealer_hand.value == player_hand.value:
			push(player_hand, dealer_hand, player_chips)

	print("Player chips stand at:", player_hand.value)

	new_game = input("Would you like to play again? type 'y' or 'n'")
	if new_game[0] == 'y':
		playing = True
		continue
	else:
		break 



