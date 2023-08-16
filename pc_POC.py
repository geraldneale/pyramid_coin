#Pyramid Coin proof of concept using Python3 before transcribing into Chialisp
AMT = 2000000000000 #in mojos
XCH_ADDRESSES = ["0xdeadbeef0","0xdeadbeef1","0xdeadbeef2","0xdeadbeef3","0xdeadbeef4","0xdeadbeef5","0xdeadbeef6",\
                "0xdeadbeef7","0xdeadbeef8","0xdeadbeef9","0xdeadbeef10","0xdeadbeef11","0xdeadbeef12","0xdeadbeef13",\
                 "0xdeadbeef14","0xdeadbeef15","0xdeadbeef16","0xdeadbeef17","0xdeadbeef18","0xdeadbeef19","0xdeadbeef20",\
                "0xdeadbeef21","0xdeadbeef22","0xdeadbeef23","0xdeadbeef24","0xdeadbeef25","0xdeadbeef26","0xdeadbeef27",\
                "0xdeadbeef28","0xdeadbeef29"]

#functions
def count_addresses(xch_addresses): #How many addresses?
    
    return len(xch_addresses)


def levels_deep(blocks): #How many levels deep? ...in the pyramid
    height = 0
    inlayer = 1
    while inlayer <= blocks:
        height += 1
        #print("height{}: {}".format(i,height))
        blocks -= 2**inlayer
        #print("blocks: {}".format(blocks))
        inlayer += 1
        #print("inlayer: {}\n".format(inlayer))
    return height

def get_position(xch_addresses,address): #one specific position in the pyramid
    
    return xch_addresses.index(address)

def units_per_level(level): #total units in each level. used to calculate payout per unit.
    
    units = 2**level + 1
    return units

def remainder_in_units(total_addresses):  #deepest level will most times not fill every position yet those positions are still used to calculate the payouts
    levels = levels_deep(total_addresses)
    #print("Levels: {}".format(levels))
    if levels == 1:
        remainder = int(3 - total_addresses)
    else:
        accum_units = 0
        for level in range(1,levels+1):
            level_units = units_per_level(level)
            accum_units += level_units     
            #print("Accumulated Units: {}".format(accum_units))
        remainder = accum_units - total_addresses    
    return remainder

def remainder_mojos(amt_level,units_in_level,remainder_units): #remaining units x unit value gives remainder which all goes to the first payout address as a bonus
    
    remainder_mojos = int(amt_level/units_in_level * remainder_units)
    
    return remainder_mojos

print("Total Coin Value: {:,} mojos".format(AMT))
total_addresses = count_addresses(XCH_ADDRESSES)
print("Total Payout Addresses: {}".format(total_addresses))
total_levels = levels_deep(count_addresses(XCH_ADDRESSES))
print("Total Pyramid Levels: {}".format(total_levels))
level_amt = int(AMT/total_levels)
print("Amount Per Level: {:,}".format(level_amt))
remainder = remainder_in_units(total_addresses)
print("Remaining Units: {} of {} in bottom level {}".format(remainder,units_per_level(total_levels),total_levels))
remainder_mojos = remainder_mojos(level_amt,units_per_level(total_levels),remainder) #fix this
print("Remaining Mojos: {}".format(remainder_mojos))
print("\n")
#index postion loop
for address in XCH_ADDRESSES:
    address_position = get_position(XCH_ADDRESSES,address) + 1 # add one to accomodate lisp which has no python list index
    print("Address Position{}: {}".format(address_position,address))
    level = levels_deep(address_position)
    #print("Level: {}".format(level))
    units_in_level = units_per_level(level)
    print("Units on Level {}: {}".format(level,units_in_level))
    unit_value = int(level_amt/units_in_level)
    print("Value Per Unit on Level {}: {}".format(level,unit_value))
    if address_position == 1:
        first_payout = unit_value + remainder_mojos
        usd = first_payout*30/1000000000000
        print("*First Position Payout Value: {:,} Mojos or USD${}".format(first_payout,usd))
        #print("{} = unit value {} plus remainder {}".format(first_payout,unit_value,remainder_mojos))
    else:
        usd = unit_value*30/1000000000000
        print("Payout Level {} Value: {:,} Mojos or USD${}".format(level,unit_value,usd))
    print("\n")
print("*First Position Payout Value = Unit Value + REMAINDER")
