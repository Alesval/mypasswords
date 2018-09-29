#!/data/data/com.termux/files/usr/bin/python3

from pass_manager import PassManager, PassManagerException
import sys
import getpass
import os

HOMESCREEN = '[add]: add a service-password\n\
[remove]: remove a service-password\n\
[retrieve]: retrieve a password\n\
[services]: get all saved services\n\
[exit]: exit\n{}'


def manage_exit():
    val = input('Continue? [y|n]: ')
    if val != 'y':
        clear_screen()
        sys.exit()


def clear_screen():
    ignore_me = os.system('clear')


#manage the authentication
def auth_access(pass_manager):
    auth_succ = False
    attempts=3
    try:
        while not auth_succ and attempts > 0:
            if attempts < 3:
                print('attempts left: {}'.format(str(attempts)))
            chiave = getpass.getpass('Master key: ')
            try:
                if pass_manager.auth_access(chiave):
                    clear_screen()
                    return
            except PassManagerException as e:
                attempts -= 1
                clear_screen()
                print(e)
        clear_screen()
        print('Exiting')
        sys.exit()
    except KeyboardInterrupt:
        clear_screen()
        sys.exit()


def action_add(pass_manager):
    try:
        try:
            print('Your services:\n'+'\n'.join(pass_manager.get_services()))
        except:
            pass
        service = input('service: ')
        password = getpass.getpass('pass: ')
        if pass_manager.add_pass(service, password):
            print('service/password added succesfully.')
            manage_exit()
            return ''
    except PassManagerException as e:
        return e


def action_retrieve(pass_manager):
    try:
        try:
            print('Your services:\n'+'\n'.join(pass_manager.get_services()))
        except:
            pass
        service = input('service: ')
        passwd = pass_manager.retrieve_pass(service)
        print('Your pass for {} is: {}'.format(service,passwd))
        manage_exit()
        return ''
    except PassManagerException as e:
        return e


def action_services(pass_manager):
    try:
        print('\n'.join(pass_manager.get_services()))
        manage_exit()
        return ''
    except PassManagerException as e:
        return e


def action_remove(pass_manager):
    try:
        try:
            print('Your services:\n'+'\n'.join(pass_manager.get_services()))
        except:
            pass
        service = input('service: ')
        if pass_manager.remove_service(service):
            print('{} removed succesfully'.format(service))
        manage_exit()
        return ''
    except PassManagerException as e:
        return e

def action_exit(pass_manager):
    clear_screen()
    sys.exit()


def main():
    pass_manager = PassManager()
    auth_access(pass_manager)
    msg = ''
    try:
        while True:
            clear_screen()
            print(HOMESCREEN.format(msg))
            msg = ''
            action = input().strip()
            if action == 'add':
                msg = action_add(pass_manager)
            elif action == 'retrieve':
                msg = action_retrieve(pass_manager)
            elif action == 'services':
                msg = action_services(pass_manager)
            elif action == 'remove':
                msg = action_remove(pass_manager)
            elif action == 'exit':
                msg = action_exit(pass_manager)
    except KeyboardInterrupt:
        clear_screen()
        sys.exit()

if __name__ == '__main__':
    main()
