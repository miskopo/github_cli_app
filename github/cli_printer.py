from colorama import Fore
from pprint import pprint


class CLIPrinter:

    @staticmethod
    def out(data_to_print, args):
        if type(data_to_print) == list:
            for i, list_item in enumerate(data_to_print):
                not args.no_numbers and print("{}{}.{}".format(Fore.GREEN, i, Fore.RESET))
                if type(list_item) == list or type(list_item) == tuple:
                    for list_item_sub_item in list_item:
                        list_item_sub_item and print(list_item_sub_item)
                else:
                    print(list_item)
        else:
            pprint(data_to_print)





