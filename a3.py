import tkinter as tk
from tkinter import filedialog # For masters task
from typing import Callable, Union, Optional
from a3_support import *
from model import *
from constants import *

#additional constants
map_file = 'maps/map1.txt'          #NOTE make so that it takes the user input, that way the map file can be changed.
TOTAL_WIDTH = FARM_WIDTH + INVENTORY_WIDTH
TOTAL_LENGTH = BANNER_HEIGHT + FARM_WIDTH + INFO_BAR_HEIGHT + 35
FARM_SIZE = (FARM_WIDTH, FARM_WIDTH)                                         #NOTE farm size

# Implement your classes here
class FarmView(AbstractGrid):
    def __init__(self, 
                 master: tk.Tk | tk.Frame, 
                 dimensions: tuple[int, int], 
                 size: tuple[int, int], 
                 **kwargs) -> None: 
        """Sets up the FarmView to be an AbstractGrid with the appropriate 
        dimensions and size, and creates an instance attribute of an empty
        dictionary to be used as an image cache.
        """
        super().__init__(master, dimensions, size, **kwargs)
        
        # self._master = master
        self.img_cache = {} 
        self._img_size = self.get_cell_size()
        self._dimensions = dimensions

        #ground images
        self._G_img = get_image('images/grass.png', self._img_size, self.img_cache)
        self._S_img = get_image('images/soil.png', self._img_size, self.img_cache)
        self._U_img = get_image('images/untilled_soil.png', self._img_size, self.img_cache)

        #player images
        self._facing_W_img = get_image('images/player_w.png', self._img_size, self.img_cache)
        self._facing_A_img = get_image('images/player_a.png', self._img_size, self.img_cache)
        self._facing_S_img = get_image('images/player_s.png', self._img_size, self.img_cache)
        self._facing_D_img = get_image('images/player_d.png', self._img_size, self.img_cache)

        #plant images                                                                                          NOTE make more pythonic NOTE

    def redraw(self, 
               ground: list[str], 
               plants: dict[tuple[int, int], 'Plant'], 
               player_position: tuple[int, int], 
               player_direction: str) -> None:
        """Clears the farm view, then creates (on the FarmView instance)
           the images for the ground, then the plants, then the player. 
           That is, the player and plants should render in front of the ground, 
           and the player should render in front of the plants. You must use 
           the get image function from a3 support.py to create your images.
        """  
        self.clear()

        for row_idx, row in enumerate(ground):
            for column_idx, marker in enumerate(row):
                # self.create_rectangle(self.get_bbox((row_idx, column_idx)))
                # self.annotate_position((row_idx, column_idx), marker)
                midpoint = self.get_midpoint((row_idx, column_idx))
                
        #ground
                if marker == GRASS:
                    self.create_image(midpoint, image= self._G_img)
                elif marker == SOIL:
                    self.create_image(midpoint, image= self._S_img)
                elif marker == UNTILLED:
                    self.create_image(midpoint, image= self._U_img)
                
        #plants
        # plants = (position : Plant)
                for pos, plant in plants.items():
                    if pos == (row_idx, column_idx):
                        self.create_image(midpoint, image= get_image(f'images/{get_plant_image_name(plant)}', self._img_size, self.img_cache))  
                                #NOTE make a function that inputs the plant and returns the filepath with images/

        #player
                if player_position == (row_idx, column_idx):
                    if player_direction == UP:
                        self.create_image(midpoint, image= self._facing_W_img)
                    elif player_direction == DOWN:
                        self.create_image(midpoint, image= self._facing_S_img)
                    elif player_direction == LEFT:
                        self.create_image(midpoint, image= self._facing_A_img)
                    elif player_direction == RIGHT:
                        self.create_image(midpoint, image= self._facing_D_img)

#NOTE make the next day button dynamic
class InfoBar(AbstractGrid):
    def __init__(self, master: tk.Tk | tk.Frame) -> None:
        """Sets up this InfoBar to be an AbstractGrid with the appropriate 
        number of rows and columns, and the appropriate width and height 
        (see constants.py).
        """
        super().__init__(master, dimensions=(2, 3), size=(700, INFO_BAR_HEIGHT))
        self._master = master

    def redraw(self, day: int, money: int, energy: int) -> None:
        """Clears the InfoBar and redraws it to display the provided day, 
        money, and energy. E.g. in Figure 3, this method was called with 
        day = 1, money = 0, and energy = 100
        """
        self.clear()

        # day 
        self.annotate_position((0, 0), text= 'Day:', font= HEADING_FONT)
        self.annotate_position((1, 0), text= f"{day}", font= ('Helvetica', 15))

        # money 
        self.annotate_position((0, 1), text= 'Money:', font= HEADING_FONT)
        self.annotate_position((1, 1), text= f'${money}', font= ('Helvetica', 15))

        # energy 
        self.annotate_position((0, 2), text= 'Energy:', font= HEADING_FONT)
        self.annotate_position((1, 2), text= f'{energy}', font= ('Helvetica', 15))

#NOTE FIX THE LAYOUT, IS ANNOYING ASF
class ItemView(tk.Frame):
   
    item_id = 0 

    def __init__(self, 
                 master: tk.Frame, 
                 item_name: str, 
                 amount: int, 
                 select_command: Optional[Callable[[str], None]] = None, 
                 sell_command: Optional[Callable[[str], None]] = None, 
                 buy_command: Optional[Callable[[str], None]] = None) -> None:
        """Sets up ItemView to operate as a tk.Frame, and creates all internal 
        widgets. Sets the commands for the buy and sell buttons to the buy 
        command and sell command each called with the appropriate item name 
        respectively. Binds the select command to be called with the 
        appropriate item name when either the ItemView frame or label is left 
        clicked. Note: The three callbacks are type-hinted as Optional to allow 
        you to pass in None if you have not yet implemented these callbacks 
        (i.e. when developing, just pass None to begin with, and hook up the 
        functionality once you’ve completed the rest of the tasks; see Section 5).
        """

        self._item_name = item_name

        self.item_price = 0
        self.item_cost = 'N/A'

        self.id = ItemView.item_id
        ItemView.item_id += 1
        
        #check if item with name exists within SELL_PRICES
        if SELL_PRICES.get(self._item_name) != None:    
            self.item_price = SELL_PRICES.get(self._item_name) 

        #check if item with name exists within BUY_PRICES
        if BUY_PRICES.get(self._item_name) != None:
            self.item_cost = BUY_PRICES.get(self._item_name)

        #set local global color variables
        self.outline = INVENTORY_OUTLINE_COLOUR
        self.selected = INVENTORY_SELECTED_COLOUR

        if amount != 0:
            self.frame_colour = INVENTORY_COLOUR
        else: 
            self.frame_colour = INVENTORY_EMPTY_COLOUR

        #frame to store label and buttons.
        tk.Frame.__init__(self, 
                          master, 
                          width= INVENTORY_WIDTH, 
                          bg= self.frame_colour, 
                          relief= 'ridge', 
                          border= 1)

        self._item_info = tk.Label(self, 
                                   text= f"{self._item_name}: {amount}\nSell price: ${self.item_price}\nBuy price: ${self.item_cost}",
                                   bg= self.frame_colour
                                   ).pack(side= 'left')
        
        # NOTE tutors advice on editing the label and frame
        #use 3 labels, store in a list to access each later on 
        # store frames in a list to acces later on 
        # write return methods for the frame and list indivudally 
        

        #buy and sell buttons 
        if self._item_name[-4:] == 'Seed':
            tk.Button(self, 
                    text= 'Buy', 
                    bg= 'white', 
                    command= buy_command).pack(side= 'left', padx= 10)

        tk.Button(self, 
                text= 'Sell', 
                bg= 'white',
                command= sell_command).pack(side= 'left', padx= 10)
               
        #bindings
        master.bind('<Button-1>', select_command) # select an item

        self.pack(side= 'top', fill= 'x')

    def update(self, amount: int, selected: bool = False) -> None:
        """Updates the text on the label, and the colour of this ItemView 
        appropriately. See Figure 5 for more details on how these are 
        presented. Note: you should configure the existing widgets in this 
        method. You must not destroy and recreate the internal widgets
        """
        if selected:
            self.config(bg = INVENTORY_SELECTED_COLOUR)
            # self._item_info.config(bg = INVENTORY_SELECTED_COLOUR)
            
        # self._item_info.config(text= f'{self._item_name}: {self._amount - amount}')
            
#NOTE Controller class
class FarmGame():
    def __init__(self, master: tk.Tk, map_file: str) -> None:
        
        # master frame
        master.title('Farm Game')
        master.geometry(f'{TOTAL_WIDTH}x{TOTAL_LENGTH}')
        
        # image
        header_img = get_image('images/header.png', (TOTAL_WIDTH, BANNER_HEIGHT))
        header_lbl = tk.Label(master, image= header_img)
        header_lbl.image = header_img

        #Infobar
        self._info_bar = InfoBar(master)

        #farm view
        self._farm_model = FarmModel(map_file)
        self._farm_map = self._farm_model.get_map()
        self._farm = FarmView(master, self._farm_model.get_dimensions(), FARM_SIZE)

        #player 
        self._character = self._farm_model.get_player()

        #next day btn
        next_day = tk.Button(master, 
                             text= "Next day", 
                             font= ('Helvetica', 12), 
                             command= self.btn_func)
        
        #pack heierarchy
        header_lbl.pack()
        next_day.pack(side= 'bottom')
        self._info_bar.pack(side= 'bottom')
        self._farm.pack(side= 'left')

        #list to append all items to so that can be accessed later
        self.all_items = []

        for item in ITEMS:
            in_inventory = 1
            for item_owned in self._character.get_inventory().keys():
                if item_owned == item:
                    item = ItemView(master, 
                            item, 
                            self._character.get_inventory().get(item), 
                            select_command= lambda event: self.select_item(event.widget._item_name),
                            buy_command= lambda event: self.buy_item(event.widget._item_name), 
                            sell_command= lambda event: self.sell_item(event.widget._item_name))
                    in_inventory = 0
                    self.all_items.append(item)
                    break
            if in_inventory:
                in_inventory = 1
                item = ItemView(master, 
                            item, 
                            0, 
                            select_command= lambda event: self.select_item(event.widget._item_name),
                            buy_command= lambda event: self.buy_item(event.master.widget._item_name), 
                            sell_command= lambda event: self.sell_item(event.master.widget._item_name))
                self.all_items.append(item)
            print(self.all_items)                                                                          #NOTE NOTE remove when finished NOTE NOTE

        # Redraw
        self.redraw()

        #bindings
        master.bind('<Key>', self.handle_keypress) #move character
    
    def btn_func(self):
        
        self._farm_model.new_day()
        self.redraw()

    def redraw(self) -> None: 
        """Redraws the entire game based on the current model state
        """
        self._farm.redraw(ground= self._farm_map,
                          plants= self._farm_model.get_plants(),
                          player_position= self._character.get_position(),
                          player_direction= self._character.get_direction())
        self._info_bar.redraw(day= self._farm_model.get_days_elapsed(), 
                              money= self._character.get_money(), 
                              energy= self._character.get_energy())

    def handle_keypress(self, event: tk.Event) -> None:
        #player_position
        player_pos = self._character.get_position()
        
        # print key pressed     NOTE for debugging NOTE
        # print(f'key = {event.char}, pos = {self._character.get_position()}, new_pos = {new_pos}')
        # print(event)

        if event.char == 'w':   #move up
            self._farm_model.move_player(UP)
            self.redraw()

        elif event.char == 'a': #move left
            self._farm_model.move_player(LEFT)
            self.redraw()
        
        elif event.char == 's': #move down
            self._farm_model.move_player(DOWN)
            self.redraw()

        elif event.char == 'd': #move right
            self._farm_model.move_player(RIGHT)
            self.redraw()
            
        elif event.char == 'p':
            pos_x, pos_y = self._character.get_position()

            if self._farm_model.get_map()[pos_x][pos_y] == SOIL:
                self._farm_model.add_plant(position= player_pos, plant= PotatoPlant())      #NOTE NOTE change the plant NOTE NOTE
                self.redraw()

            #make so that you cannot plant on soil and grass ('G', 'S')

        elif event.char == 'h': 
            print('Attempt to harvest plant from players current position')
            self._farm_model.harvest_plant(player_pos)
            self.redraw()
            print(self._character.get_inventory())


        elif event.char == 'r':
            print('attempt to remove the plant from the players current position.')
            self._farm_model.remove_plant(player_pos)
            self.redraw()

        elif event.char == 't':
            self._farm_model.till_soil(player_pos)
            self.redraw()

        elif event.char == 'u':
            self._farm_model.untill_soil(player_pos)
            self.redraw()

    def select_item(self, item_name: str) -> None:
        # self._character.select_item(item_name)
        print(f'selected: {item_name}')


        #NOTE figure out how to update the item views so that their backgound colour changes, also change the ItemView
        # self.all_items[0].update(self, amount= 0, selected= True)

    def buy_item(self, item_name: str) -> None:
        """The callback to be given to each ItemView for buying items. 
        This method should cause the player to attempt to buy the item with the
        given item name, at the price specified in BUY PRICES, 
        and then redraw the view
        """
        price = [item for item in BUY_PRICES if item[0] == item_name]
        # self._character.buy(item_name, price= BUY_PRICES.get(item_name))
        print(f'bought item: {item_name} for ${price}')


    def sell_item(self, item_name: str) -> None: 
        """The callback to be given to each ItemView for selling items. 
        This method should cause the player to attempt to sell the item with 
        the given item name, at the price specified in SELL PRICES, 
        and then redraw the view
        """
        # self._character.sell(item_name, price= ?)
        print(f'sell item: {item_name}')

def play_game(root: tk.Tk, map_file: str) -> None:
    game = FarmGame(root, map_file)
 
    # run
    root.mainloop()

def main() -> None:
    #initialize
    root = tk.Tk()

    play_game(root, map_file)

if __name__ == '__main__':
    main()

