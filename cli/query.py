from datetime import datetime
import get_and_greet_user
import sys
from loader import Loader
from classes import User


stock = Loader(model="stock")
personnel = Loader(model="personnel")


user_name = get_and_greet_user.get_user_name()

# greeting through class method
for position in personnel:
    if position.name_pr == user_name:
        position.greet()
    elif position.head_of_pr:
        for sub_position in position.head_of_pr:
            if user_name == position.name_pr:
                position.greet()
            elif 'head_of' in sub_position:
                for sub_sub_position in sub_position["head_of"]:
                    if user_name == sub_sub_position["user_name"]:
                        position.greet()
                    elif 'head_of' in sub_sub_position:
                        for sub_sub_sub_position in sub_sub_position["head_of"]:
                            if user_name == sub_sub_sub_position["user_name"]:
                                position.greet()
    else:
        user_cl = User(user_name)
        user_cl.greet()
# get_and_greet_user.greet_user(user_name)
log = {'listed': 0, 'searched': set(), 'browsed': set(), 'ordered': set()}
employee_access = False

def get_selected_operation():
    '''Ask user what he/she want to choose from menu'''
    print('\nWhat would you like to do?: \n1. Show list items by warehouse\n2. Search an item and place an order\n3. Browse by category \n4. Quit')
    choice = input('Type the number of the operation: ')
    return choice


def list_items_by_warehouse():
    '''List the items by warehouse'''
    total_items_by_warehouses = {}
    listed_items = 0 # only for log variable

    for warehouse in stock:
        total_items_by_warehouses[int(warehouse.id)] = warehouse.occupancy()
        for item in warehouse.stock_here:
            print(item)
    print('')
    for number in range(1, len(total_items_by_warehouses) + 1):
        listed_items += total_items_by_warehouses[number] # only for log variable
        print(f'Total items in warehouse {number}: ', total_items_by_warehouses[number])

    log['listed'] += listed_items
    termination(user_name)


def search_and_order_item():
    '''Search and order item'''
    desired_product = input(f'\nWhat is the name of the item? ')
    product_quantity_by_locations = {}                    
    bigger_quantity = 0
    bigger_warehouse = 0
    time_now = datetime.now().date()
    location = []
    global employee_access

    # Count products, define warehouse and count days
    for warehouse_iter in stock:
        for item in warehouse_iter.search(desired_product):
            log['searched'].add(str(item)) # add info in log dictionary (at the start of the file) that show info at the end
            time_stored = item.date_of_stock_pr
            time_stored = datetime.strptime(time_stored, "%Y-%m-%d %H:%M:%S").date()
            delta = time_now - time_stored
            if warehouse_iter.id not in product_quantity_by_locations:  # count quantity of items by warehouses
                product_quantity_by_locations[warehouse_iter.id] = 1
            elif warehouse_iter.id in product_quantity_by_locations:
                product_quantity_by_locations[warehouse_iter.id] += 1
            warehouse = warehouse_iter.id
            location.append(f'- Warehouse {warehouse} (in stock for {delta.days} days)')

    '''Count total products in two warehouses'''
    total_quantity = len(location)
    if total_quantity == 0:
        print('Item not found')
        termination(user_name)
    location.sort()

    if total_quantity == 0:
        '''Item not found'''
        print(f'Amount available: {total_quantity}\nLocation: Not in stock')
    else:
        print(f'Amount available: {total_quantity}\nLocation:')

    sorted_product_quantity_by_locations = sorted(product_quantity_by_locations.items(), key=lambda x:x[1], reverse=True)
    new_sorted_product_quantity_by_locations = dict(sorted_product_quantity_by_locations)
    bigger_quantity = list(new_sorted_product_quantity_by_locations.values())[0]
    bigger_warehouse = list(new_sorted_product_quantity_by_locations.keys())[0]

    '''List every item'''
    for item in location:
        print(item)
    print(f'\nMaximum availability: {bigger_quantity} in Warehouse {bigger_warehouse}\n')

    '''ORDER'''

    # ak user does he/she want to order an item
    order_decision = input('Would you like to order this item?(y/n) ') 
    if order_decision == 'n':
        '''Disagree'''
        None
    elif order_decision == 'y':
        '''Agree'''
        if employee_access == False:
            access = user_system(user_name)
            if access == False:
                print("I'm sorry, you are not an employee. Only the employee can make an order. You can try again to login.")
                termination(user_name)
            elif access == True:
                employee_access = True
                order_quantity = int(input('How many would you like? '))
                if order_quantity > total_quantity:
                    message_for_customer(total_quantity)
                    '''Order more than available (accepting and not accepting)'''
                    repeat_order_decision = input('Would you like to order the maximum available?(y/n) ')
                    if repeat_order_decision == 'n':
                        None
                    elif repeat_order_decision == 'y':
                        # add info in log dictionary (at the start of the file) that show info at the end
                        log['ordered'].add(desired_product) 
                        print(f'{total_quantity} {desired_product} have been ordered.')
                    else:
                        print(f'Wrong choice. Please try again!')
                elif order_quantity <= total_quantity:
                    '''Order the available quantity'''
                    # add info in log dictionary (at the start of the file) that show info at the end
                    log['ordered'].add(desired_product) 
                    print(f'{order_quantity} {desired_product} have been ordered.')
                elif order_quantity <= 0:
                    '''Order less than Zero'''
                    print(f'Wrong quantity. Please try again!')
        elif employee_access == True:
            order_quantity = int(input('How many would you like? '))
            if order_quantity > total_quantity:
                message_for_customer(total_quantity)
                '''Order more than available (accepting and not accepting)'''
                repeat_order_decision = input('Would you like to order the maximum available?(y/n) ')
                if repeat_order_decision == 'n':
                    None
                elif repeat_order_decision == 'y':
                    # add info in log dictionary (at the start of the file) that show info at the end
                    log['ordered'].add(desired_product) 
                    print(f'{total_quantity} {desired_product} have been ordered.')
                else:
                    print(f'Wrong choice. Please try again!')
            elif order_quantity <= total_quantity:
                '''Order the available quantity'''
                # add info in log dictionary (at the start of the file) that show info at the end
                log['ordered'].add(desired_product) 
                print(f'{order_quantity} {desired_product} have been ordered.')
            elif order_quantity <= 0:
                '''Order less than Zero'''
                print(f'Wrong quantity. Please try again!')
    else:
        '''Wrong choice'''
        print(f'Wrong choice. Please try again!')
    termination(user_name)


def browse_by_category():
    '''Browse items by category'''
    list_category = []
    dict_category = {}
    '''form category (without quantity of items)'''
    for warehouse in stock:
        for item in warehouse.stock_here:
            if item.category_pr not in list_category:
                list_category.append(item.category_pr)
    print('')
    '''count quantity of items in every category'''
    for i in range(1, len(list_category)+1):
        count = 0
        for warehouse in stock:
            for item in warehouse.stock_here:
                if item.category_pr  == list_category[i-1]:
                    count += 1
        '''print name of every category and its quantity'''
        print(f'{i}. {list_category[i-1]} ({count})')
        '''every created list send to the dictionary as value, and key is ordered number'''
        dict_category[i] = list_category[i-1]

    choice_browse = int(input('Type the number of the category to browse: '))
    if choice_browse in range(1, len(dict_category)+1):
        print(f'\nList of {dict_category[choice_browse]} available: ')
        for key, value in dict_category.items():
            if key == choice_browse:
                for warehouse in stock:
                    for item in warehouse.stock_here:
                        if value == item.category_pr:
                            log["browsed"].add(dict_category[key])
                            print(item.state_pr, item.category_pr +',', 'Warehouse', warehouse.id)
    else:
        print("\nLooks like there isn't this number of category." )
    termination(user_name)


def thanks(user_name):
    '''
    Function thanks user
    and 
    print a list of the actions taken during that session
    '''
    print(f'\nThank you for your visit, {user_name}!')

    print(f'\nIn this session you have:')
    for key, value in log.items():
        if key == 'listed':
            print(f'1. Listed {value} items.')
        elif key == 'searched':
            if len(value) > 0:
                print('2. Searched:')
                for element in value:
                    print('-', element)
            elif len(value) == 0:
                print('2. Searched nothing')
        elif key == 'browsed':
            if len(value) > 0:
                print('3. Browsed:')
                for element in value:
                    print('-', element)
            elif len(value) == 0:
                print('3. Browsed nothing')
        elif key == 'ordered':
            if len(value) > 0:
                print('4. Ordered:')
                for element in value:
                    print('-', element)
            elif len(value) == 0:
                print('4. Browsed nothing')


def termination(user_name):
    '''
    function 
    or sends user to the main menu
    or exits from program
    '''   
    termination_choice = input('\nWould you like to perform another operation? (y/n) ')
    if termination_choice == 'n':
        thanks(user_name)
        sys.exit()
    elif termination_choice == 'y':
        main()
    else:
        valid_operation_message()
        termination(user_name)


def user_system(user_name):
    '''
    ask user to put relevant login and password
    return True if log and pass were matched
    return False if log and pass were matched
    '''
    quit = False
    login = user_name
    while quit == False:
        password = input('Please enter your password: ')
        for position in personnel:
            if login == position.name_pr and password == position.password_pr:
                return True
            elif position.head_of_pr:
                for sub_position in position.head_of_pr:
                    if login == position.name_pr and password == position.password_pr:
                        return True
                    elif 'head_of' in sub_position:
                        for sub_sub_position in sub_position["head_of"]:
                            if login == sub_sub_position["user_name"] and password == sub_sub_position["password"]:
                                return True
                            elif 'head_of' in sub_sub_position:
                                for sub_sub_sub_position in sub_sub_position["head_of"]:
                                    if login == sub_sub_sub_position["user_name"] and password == sub_sub_sub_position["password"]:
                                        return True
        ask_to_continue = input('\nWrong login and password. Would you like to try again:(y/n) ')
        if ask_to_continue == 'n':
            quit = True
            return False
        elif ask_to_continue == 'y':
            login = input('Please enter your name(login): ')
        else:
            print('Ops! Incorrect input. Please try again.')


def decoration(func):
    '''Decorate the message by stars'''
    def inner(*args, **kwargs):
        print('*'*80)
        func(*args, **kwargs)
        print('*'*80)
    return inner


@decoration
def message_for_customer(quantity):
    print(f'There are not this many available. The maximum amount that can be ordered is {quantity}')


@decoration
def valid_operation_message():
    print('Search is not a valid operation.')


def main():


    operation = get_selected_operation()


    if operation == '1':
        list_items_by_warehouse()


    elif operation == '2':
        search_and_order_item()


    elif operation == '3':
        browse_by_category()


    elif operation == '4':
        pass


    else:
        print('')
        valid_operation_message()


if __name__ == '__main__':
    main()
    thanks(user_name)
