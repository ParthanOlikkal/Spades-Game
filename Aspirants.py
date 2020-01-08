"""
Team Aspirants

Parthan 
Raghav
Saad
Nishanjan

"""
import numpy as np
import pandas as pd
#import random

# Helper functions    #Saad

class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []  # Holds Agent's current cards
        self.players = []  # Holds the current players name
        # Stores the game data as Pandas dataframe
        self.data = pd.DataFrame(columns=['lead', 'winner', 'trick'])
        self.cardsplayed = {}
    
    def parse_trick(self, trick):
    #print('Parsing',trick)
        card_dict = {'A': 14, 'K':13,'Q':12,'J':11 ,'T':10} # Assigning the face cards with numbers for comparison
        card_nums = [i[:-1] for i in trick] # Removing the suite characters to extract the card value
        #print(trick, card_nums)
        card_nums_ = [int(i) if i.isdigit() else card_dict[i] for i in card_nums ] # Extracting the card value
        return card_nums_

    def analyse_hand(self,hand): # Modification over Nishan's code. 
    # Create the dictionary which calculates the number of cards of each suit
        suit_list = {'C','D','H','S'}
        suit_totals = {}
        for suit in suit_list:
            sum = 0
            for card in hand:
                if card[-1] == suit:
                    sum += 1
                    if sum == 0:
                        continue
                    suit_totals[suit] = sum
        return suit_totals 

    def get_name(self):
        """
        Returns a string of the agent's name
        """
        return str(self.name)

    def get_hand(self):
        """
        Returns a list of two character strings reprsenting cards in the agent's hand
        """
        return self.hand

    def new_hand(self, names):
        """
        Takes a list of names of all agents in the game in clockwise playing order
        and returns nothing. This method is also responsible for clearing any data
        necessary for your agent to start a new round.
        """
        self.players = names  # Setting the names of players to the agent
        self.hand = []  # Resetting the hand of the agent
        # Resetting the dataframe
        self.data = pd.DataFrame(columns=['lead', 'winner', 'trick'])

    def add_cards_to_hand(self, cards):
        """
        Takes a list of two character strings representing cards as an argument
        and returns nothing.
        This list can be any length.
        """
        self.hand = cards
        
    
    def trackingCards(self, suite = None):
        Spades = ["2S","3S","4S","5S","6S","7S","8S","9S","TS","JS","QS","KS","AS"]
        Hearts = ["2H","3H","4H","5H","6H","7H","8H","9H","TH","JH","QH","KH","AH"]
        Clubs = ["2C","3C","4C","5C","6C","7C","8C","9C","TC","JC","QC","KC","AC"]
        Diamonds = ["2D","3D","4D","5D","6D","7D","8D","9D","TD","JD","QD","KD","AD"]
        #opponents cards are tracked
        opp_cards = [Spades,Hearts,Clubs,Diamonds]
        
        track_cards = [Clubs[-1],Diamonds[-1],Hearts[-1],Spades[-1]]
        for cards in self.data["trick"]:
            for card in cards:
                if card[-1] == "C":
                    Clubs.remove(card)
                    track_cards[0] = Clubs[-1]        #argmax of np can be used
                    
                elif card[-1] == "S":
                    Spades.remove(card)
                    track_cards[3] = Spades[-1]
                    
                elif card[-1] == "H":
                    Hearts.remove(card)
                    track_cards[2] = Hearts[-1]
                    
                elif card[-1] == "D":
                    Diamonds.remove(card)
                    track_cards[1] = Diamonds[-1]
        #after the iteration track_card look at the highest whereas opp_cards will have the list of all the cards            
        return track_cards, opp_cards
        
    def select_card(self,trick,available_actions,oponent_hand = None):  
        action_num = self.parse_trick(available_actions) # Converting agent's available actions to numerical values
        print(action_num)
        game_len = len(trick) # How many hands has been passed in the trick
        if game_len == 2: ## Case 3 Agent is the third player 
            temp_trick = trick # Storing trick in a temporary variable
            evals = []
            for action in available_actions:
                temp_trick.append(action)
                oponent_card = self.select_card(temp_trick,oponent_hand)
                temp_trick.append(oponent_card)
                utility = self.evaluate(temp_trick,3)
                evals.append(utility)
                #print(temp_trick)
                temp_trick = temp_trick[:-2] # Popping the last two element.
                eval_sum = np.sum(evals)
#             print(evals)
            if eval_sum == 0:
                indx = np.argmin(action_num)        # returns the minimum value in the axis = 0
                selected_card = available_actions[indx]
            else:
                indx = list(np.flatnonzero(evals)) # Getting the index of non zero elements
                valid_actions = [available_actions[i] for i in indx]
                valid_actions_num = [action_num[i] for i in indx] # Numerical represtation of valid actions
                indx = np.argmin(valid_actions_num)
                selected_card = valid_actions[indx]
            #print(selected_card)
            return selected_card

        elif game_len == 3: ## Case 4 Agent is the final player
            temp_trick = trick # Storing trick in a temporary variable
            evals = []
            for action in available_actions:  
                temp_trick.append(action)
#                 print(temp_trick)
                utility = self.evaluate(temp_trick,4)
                evals.append(utility)
                temp_trick.pop(-1) # Popping the last element.
#             print(evals)          
            eval_sum = np.sum(evals)
            if eval_sum == 0:
                indx = np.argmin(action_num)
                selected_card = available_actions[indx]  
            else:
                indx = list(np.flatnonzero(evals)) # Getting the index of non zero elements
                valid_actions = [available_actions[i] for i in indx]
                valid_actions_num = [action_num[i] for i in indx] # Numerical represtation of valid actions
                indx = np.argmin(valid_actions_num)
                selected_card = valid_actions[indx]
            #print(selected_card)
            return selected_card
    
    def play_card(self, lead, trick):
        """
        Takes a a string of the name of the player who lead the trick and
        a list of cards in the trick so far as arguments.

        Returns a two character string from the agents hand of the card to be played
        into the trick.
        """
        # Version 2 created by Nishan
        # Starting a game with 2 of clubs
        game_len=len(trick)
        if game_len==0:
            available_actions = self.get_hand()
            action_num = self.parse_trick(available_actions) # Converting agent's available actions to numerical values
            
        #if game_len == 0: ## Case 1 Agent is the first player
            # 2 different cases
            # case 1: when we have 2C
            track = self.trackingCards()
            print(action_num)
            if '2C' in available_actions:       #Checking inhand if we have 2C
                selected_card = '2C'
                track.remove('2C')         #remove 2C from trackingCards
                #print(selected_card)
            
            #case 2: playing highest 
            elif '2C' not in available_actions:
                highest_lead_card = track
                highest_lead_card_num = self.parse_trick(highest_lead_card)
                if max(action_num) in highest_lead_card_num:
                    selected_card_indx = np.argmax(action_num)
                    selected_card = available_actions[selected_card_indx]
                    #Need to remove the selected card from trackingCard
                else:
                    #Need to remove the selected card from trackingCard
                    selected_card_indx = np.argmin(action_num)
                    selected_card = available_actions[selected_card_indx]
                    #Need to remove the selected card from trackingCard
                    
                self.trackingCards(selected_card[-1])
                    
        
        elif game_len == 1:     
            available_actions = self.get_hand()
            trick_suite = trick[0][-1]
            available_cards = [i for i in available_actions if i[-1] == trick_suite] # Getiing all cards with the selected suite from agent's hand
            action_num = self.parse_trick(available_actions) # Converting agent's available actions to numerical values
            
        #if game_len == 0: ## Case 1 Agent is the first player
            # 2 different cases
            # case 1: when we have 2C
            track = self.trackingCards(None)
            print(action_num)
            highest_lead_card = track
            highest_lead_card_num = self.parse_trick(highest_lead_card)
            
            if len(available_cards) == 0:
                self.burn_card()
            
            elif max(action_num) in highest_lead_card_num:
                selected_card_indx = np.argmax(action_num)
                selected_card = available_actions[selected_card_indx]
            else:
                selected_card_indx = np.argmin(action_num)
                selected_card = available_actions[selected_card_indx]
                    
            #self.trackingCard(selected_card[-1])
                
        elif game_len == 2 or game_len == 3:
            available_actions = self.get_hand()
            trick_suite = trick[0][-1]
            available_cards = [i for i in available_actions if i[-1] == trick_suite] # Getiing all cards with the selected suite from agent's hand
            action_num = self.parse_trick(available_actions) # Converting agent's available actions to numerical values
            opponent_cards = [] # Have to figure out
            if len(available_cards) == 0:
                self.burn_card()
            
            elif len(available_cards) == 1:
                selected_card = available_cards[0]
            
            else:
                self.select_card(trick, available_cards, opponent_cards)            
            
        # remove the selected card from the hand and return that card
        self.hand.remove(selected_card)
        return selected_card
        
    def collect_trick(self, lead, winner, trick):
        """
        Takes three arguements. Lead is the name of the player who led the trick.
        Winner is the name of the player who won the trick. And trick is a four card
        list of the trick that was played. Should return nothing.
        """
        temp_dict = {'lead': lead, 'winner': winner, 'trick': [trick]}  # Passing all data as list, so 'pandas' see this as a single row of data
        temp_df = pd.DataFrame(temp_dict)
        # Appending the new data to Agent's data
        self.data = self.data.append(temp_df, ignore_index=True)

    def score(self):
        """
        Calculates and returns the score for the game being played.
        """
        winners = list(self.data['winner'])  # Getting the list of the trick winners
        player_name = self.get_name()  # Getting the agent's name
        wins = winners.count(player_name)  # Counting the number of wins
        return wins

	
    def burn_card(self):
    	hand = self.get_hand() # Getting Aget's current hand
    	suit_total = self.analyse_hand(hand) # Computing how many cards from each suite is present
    	suits = [i[0] for i in suit_total] # Seperating the suites from suit_total dictionary
    	num_cards = [i for i in suit_total.values()] # Seperating the numbers from suit_total dictionary
    	# Logic for determining which suite the agent going to burn
    	possible_burn = []
    	for i,nums in enumerate(num_cards):
    		if nums == 1: # If only one card is present for any suite, append that suite
    			possible_burn.append(suits[i])
    	sorted_suit_total = sorted(suit_total.items(),key = lambda x:x[1]) # Sorting the suit_total to find the suite with highest number of cards
    	high_card_suite = sorted_suit_total[-1][0] 
    	possible_burn.append(high_card_suite) # Adding the suit with highest number of cards for possible burn
    	available_cards = [i for selected_suite in possible_burn for i in hand if i[-1] == selected_suite] # Getiing all cards with the selected suite from agent's hand
    	available_cards_num = self.parse_trick(available_cards) # Converting the cards into numerals for comparison
    	card_indx = np.argmin(available_cards_num) # Getting the index of the lowest card
    	selected_card = available_cards[card_indx] # Getting the lowest card for burn
    	return selected_card
    
    
if __name__ == "__main__":
# Some testcases
    """
    player = Player('Bluffmaster')
    print(player.trackingCards())
    player.collect_trick('Sam', 'Bob', ['10C', 'AC', 'KC', 'QC'])
    player.collect_trick('Sam', 'Bob', ['5D', '8D', 'AD', 'QD'])
    player.collect_trick('Sam', 'Bob', ['9H', 'AH', 'KH', 'QH'])
    player.collect_trick('Sam', 'Bob', ['8H', 'JH', '7H', 'JC'])
    trick1 = []
    available_actions = ['5D', '3S', '10C', 'AH']
    print(player.trackingCards())
    """