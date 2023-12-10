def get_user_name():
    '''Ask user for an username'''
    name = input('What is your user name? ')
    return name


def greet_user(user_name):
    '''Greet user by username'''
    print('Hello', user_name)


if __name__ == '__main__':
    get_user_name()
    greet_user()