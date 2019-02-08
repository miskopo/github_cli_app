from colorama import Fore


class CLIHandler:
    """
    Common class for printing output to and acquiring input from CLI
    """

    @staticmethod
    def out(data_to_print, args):
        if isinstance(data_to_print, list):
            for i, list_item in enumerate(data_to_print):
                if not args.no_numbers:
                    print(f"{Fore.GREEN}{i+1}.{Fore.RESET}")
                if isinstance(list_item, list) or isinstance(list_item, tuple):
                    for list_item_sub_item in list_item:
                        if list_item_sub_item:
                            print(list_item_sub_item)
                else:
                    print(list_item)
        elif isinstance(data_to_print, Exception):
            print(str(data_to_print))
        else:
            print(data_to_print)

    @staticmethod
    def confirm_action(text_query: str = "This action is irreversible, are you sure to continue?") -> bool:
        while True:
            choice = input(f"{text_query} [Y/n] ") or "y"
            if choice.lower() in ['y', 'yes', 'n', 'no']:
                return choice.lower() in ['y', 'yes']
            else:
                CLIHandler.out("Invalid choice, try again", None)







