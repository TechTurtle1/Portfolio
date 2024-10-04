"""Import modules below this line (starting with unit 6)."""
import string as s
import random as r

"""Write new functions below this line (starting with unit 4)."""

# Makes a new grid
def make_grid():
    list = [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]]
    ship_list = ["mothership", "battleship", "destroyer", "stealth", "patrol"]
    
    # Uploads the ships into ship_list
    # If there is already a ship at the chosen random position choose a different position
    for ship in ship_list:
        if ship == "mothership":
            x = r.randint(1, 8)
            y = r.randint(1, 8)
            list[x][y] = "M"
            list[x-1][y] = "M"
            list[x+1][y] = "M"
            list[x][y-1] = "M"
            list[x][y+1] = "M"
        elif ship == "battleship":
            cont = False
            while not cont:
                x = r.randint(0, 8)
                y = r.randint(0,8)
                if list[x][y] != "M" and list[x + 1][y] != "M" and list[x][y+1] != "M" and list[x+1][y+1] != "M":
                    cont = True
                    list[x][y] = "B"
                    list[x+1][y] = "B"
                    list[x][y+1] = "B"
                    list[x+1][y+1] = "B"
        elif ship == "destroyer":
            cont = False
            while not cont:

                # 0: X ~
                #    X X

                # 1: ~ X
                #    X X

                # 2: X X
                #    X ~

                # 3: X X 
                #    ~ X 

                orientation = r.randint(0, 3)
                x = r.randint(0,8)
                y = r.randint(0,8)
                if orientation == 0:
                    if list[x][y] == "~" and list[x][y+1] == "~" and list[x+1][y+1] == "~":
                        cont = True
                        list[x][y] = "D"
                        list[x][y+1] = "D"
                        list[x+1][y+1] = "D"
                elif orientation == 1:
                    if list[x+1][y] == "~" and list[x][y+1] == "~" and list[x+1][y+1] == "~":
                        cont = True
                        list[x+1][y] = "D"
                        list[x][y+1] = "D"
                        list[x+1][y+1] = "D"
                elif orientation == 2:
                    if list[x+1][y] == "~" and list[x][y] == "~" and list[x][y+1] == "~":
                        cont = True
                        list[x+1][y] = "D"
                        list[x][y+1] = "D"
                        list[x][y] = "D"
                elif orientation == 3:
                    if list[x+1][y] != "~" and list[x+1][y+1] != "~" and list[x][y] != "~":
                        cont = True
                        list[x+1][y] = "D"
                        list[x][y+1] = "D"
                        list[x+1][y] = "D"
        elif ship == "stealth":
            # 0: Vertical
            # 1: Horizontal
            cont = False
            orientation = r.randint(0,1)
            while not cont:
                if orientation == 0:
                    x = r.randint(0,9)
                    y = r.randint(1,8)
                    if list[x][y] == "~" and list[x][y-1] == "~" and list[x][y+1] == "~":
                        cont = True
                        list[x][y] = "S"
                        list[x][y-1] = "S"
                        list[x][y+1] = "S"
                if orientation == 1:
                    x = r.randint(1,8)
                    y = r.randint(0,9)
                    if list[x][y] == "~" and list[x-1][y] == "~" and list[x+1][y] == "~":
                        cont = True
                        list[x][y] = "S"
                        list[x-1][y] = "S"
                        list[x+1][y] = "S"
        elif ship == "patrol":
            # 0: Vertical
            # 1: Horizontal
            cont = False
            orientation = r.randint(0,1)
            while not cont:
                if orientation == 0:
                    x = r.randint(0,9)
                    y = r.randint(0,8)
                    if list[x][y] == "~" and list[x][y+1] == "~":
                        cont = True
                        list[x][y] = "P"
                        list[x][y+1] = "P"
                if orientation == 1:
                    x = r.randint(0,8)
                    y = r.randint(0,9)
                    if list[x][y] == "~" and list[x+1][y] == "~":
                        cont = True
                        list[x][y] = "P"
                        list[x+1][y] = "P"
    return list
                        
# Print the instructions
def print_instructions():
    print("\nInstructions:\n")
    print("Ships are positioned at fixed locations in a 10-by-10\ngrid. The rows of the grid are labeled A through J, and\nthe columns are labeled 0 through 9. Use menu option\n\"2\" to see an example. Target the ships by entering the\nrow and column of the location you wish to shoot. A\nship is destroyed when all of the spaces it fills have\nbeen hit. Try to destroy the fleet with as few shots as\npossible. The fleet consists of the following 5 ships:")
    print("\nSize : Type")
    print("   5 : Mothership")
    print("   4 : Battleship")
    print("   3 : Destroyer")
    print("   3 : Stealth Ship")
    print("   2 : Patrol Ship")

    

def main():
    
    # Whether or not to quit the game
    is_quit = False
    print("\n               ~ Welcome to Battleship! ~               \n")
    print("ChatGPT has gone rogue and commandeered a space strike\nfleet. It's on a mission to take over the world.  We've\nlocated the stolen ships, but we need your superior\nintelligence to help us destroy them before it's too\nlate.")
    while not is_quit:
        file = open("battleship_hof.txt")

        # Read lines 1-10 and stroe it in lines
        lines = file.readlines()[1:11]

        print("\nMenu:")
        print("  1 : Instructions")
        print("  2 : View Example Map")
        print("  3 : New Game")
        print("  4 : Hall of Fame")
        print("  5 : Quit")
        option = input("What would you like to do? ")
        if option == "1":
            print_instructions()
        elif option == "2":
            list = make_grid()

            # The letters and numbers for the grid
            print("\n   0  1  2  3  4  5  6  7  8  9")
            letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
            for index in range(len(list)):
                position = 0
                line = letters[index] + "  "
                for element in list[index]:
                    line += element
                    position += 1
                    if position < len(list[index]):
                        line += "  "
                print(line)
            print()
        elif option == "3":
            list = make_grid()
            cont = True
            letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

            # This is a blank grid
            blank_list = [["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~"]]

            # Number of hits and max health of ships on the board
            hit_list = [0, 0, 0, 0, 0]
            max_hit = [5, 4, 3, 3, 2]
            ship_list = ["Mothership", "Battleship", "Destroyer", "Stealth Ship", "Patrol Ship"]
            hits = 0
            total_shots = 1
            while cont:

                print("\n   0  1  2  3  4  5  6  7  8  9")
                for index in range(len(list)):
                    position = 0
                    line = letters[index] + "  "
                    for element in blank_list[index]:
                        line += element
                        position += 1
                        if position < len(list[index]):
                            line += "  "
                    print(line)
                print()

                quit_flag = False
                while True:
                    coords = input("Where should we target next (q to quit)? ")

                    # If the input is Q or q, then quit
                    if coords.lower() == "q":
                        quit_flag = True
                        break
                    # If the length of the coordinates is not two, or is invalid, prompt the user again
                    if len(coords) != 2:
                        print("Please enter exactly two characters.")
                        continue
                    x = ord(coords[0].lower()) - 97
                    y = ord(coords[1]) - 48
                    #print("X: " + str(x))
                    #print("Y: " + str(y))
                    if x > 9 or x < 0 or y > 9 or y < 0:
                        print("Please enter a location in the form \"G6\".")
                        continue
                    break

                if quit_flag:
                    break
                
                if blank_list[x][y] == "~":
                    if list[x][y] == "~":
                        print("\nmiss")
                        blank_list[x][y] = "o"
                    else:
                        print("\nIT'S A HIT!")
                        hits += 1

                        # Hit number is the index in the hit_list and max_hit
                        hit_number = 0
                        if list[x][y] == "M":
                            hit_number = 0
                        elif list[x][y] == "B":
                            hit_number = 1
                        elif list[x][y] == "D":
                            hit_number = 2
                        elif list[x][y] == "S":
                            hit_number = 3
                        else:
                            hit_number = 4
                        hit_list[hit_number] = hit_list[hit_number] + 1

                        # Check if the ship had been destroyed
                        if hit_list[hit_number] == max_hit[hit_number]:
                            print("The enemy's " + ship_list[hit_number] + " has been destroyed.")
                        blank_list[x][y] = "x"
                        if hits == 17:
                            print("\nYou've destroyed the enemy fleet!\nHumanity has been saved from the threat of AI.\n\nFor now ...\n")

                            # If the file is empty besides the header
                            if len(lines) == 0:
                                print("Congratulations, you have achieved a targeting accuracy\nof " + format((hits / total_shots) * 100, "0.2f") + "% and earned a spot in the Hall of Fame.")
                                name = input("Enter your name: ")

                                # Insert the new score, and write it to the file
                                lines.append(str(name + "," + str(hits) + "," + str(total_shots - hits)) + "\n")
                                file.close()
                                file = open("battleship_hof.txt", "w")
                                file.write("name,hits,misses\n")

                                place = 1
                                print("\n\n~~~~~~~~ Hall of Fame ~~~~~~~~\nRank : Accuracy :  Player Name\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                if len(lines) != 0:
                                    for line in lines:
                                        stripped_line = line.strip("\n").split(",")
                                        if place < 11:
                                            print(format(place, '4.0f') + format((float(stripped_line[1]) / (float(stripped_line[1]) + float(stripped_line[2]))) * 100, '10.2f') + "%" + stripped_line[0].rjust(15))
                                        place += 1
                                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")



                                index = 0
                                for line in lines:
                                    if index < 10:
                                        file.write(line)
                                    index += 1
                            else:

                                # If the file has stats in it already
                                temp_line = lines[len(lines) - 1].strip("\n").split(",")

                                # If accuracy in score of file is less than the current player's accuracy
                                if (float(temp_line[1]) / (float(temp_line[1]) + float(temp_line[2]))) < hits / total_shots or len(lines) < 10:
                                    print("Congratulations, you have achieved a targeting accuracy\nof " + format((hits / total_shots) * 100, "0.2f") + "% and earned a spot in the Hall of Fame.")
                                    name = input("Enter your name: ")
                                    index = 0
                                    for line in lines:
                                        temp_line = line.strip("\n").split(",")
                                        if float(temp_line[1]) / (float(temp_line[1]) + float(temp_line[2])) < hits / total_shots:
                                            break    
                                        index += 1

                                    # Insert the new score, and write it to the file
                                    lines.insert(index, str(name + "," + str(hits) + "," + str(total_shots - hits)) + "\n")
                                    file.close()
                                    file = open("battleship_hof.txt", "w")
                                    file.write("name,hits,misses\n")

                                    place = 1
                                    print("\n\n~~~~~~~~ Hall of Fame ~~~~~~~~\nRank : Accuracy :  Player Name\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                    if len(lines) != 0:
                                        for line in lines:
                                            stripped_line = line.strip("\n").split(",")
                                            if place < 11:
                                                print(format(place, '4.0f') + format((float(stripped_line[1]) / (float(stripped_line[1]) + float(stripped_line[2]))) * 100, '10.2f') + "%" + stripped_line[0].rjust(15))
                                            place += 1
                                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                                    index = 0
                                    for line in lines:
                                        if index < 10:
                                            file.write(line)
                                        index += 1
                                else:
                                    print("Your targeting accuracy was " + format((hits / total_shots) * 100, "0.2f") + "%.")
                            cont = False
                else:
                    print("\nYou've already targeted that location")
                total_shots += 1
                        

                            
        elif option == "4":
            
            place = 1
            print("\n\n~~~~~~~~ Hall of Fame ~~~~~~~~\nRank : Accuracy :  Player Name\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            if len(lines) != 0:
                for line in lines:
                    stripped_line = line.strip("\n").split(",")
                    print(format(place, '4.0f') + format((float(stripped_line[1]) / (float(stripped_line[1]) + float(stripped_line[2]))) * 100, '10.2f') + "%" + stripped_line[0].rjust(15))
                    place += 1
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            file.close()
        elif option == "5":
            print("\nGoodbye\n")
            is_quit = True
            file.close()
        else:
            print("\nInvalid selection.  Please choose a number from the menu.")

                        

            

"""Do not change anything below this line."""
if __name__ == "__main__":
    main()
