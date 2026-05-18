class MenuRenderer:
    def __init__(self):
        pass

    def renderMenu(self, menu):
        options = menu.options
        hovering = menu.hovering
        header = menu.header

        if header:
            for row in menu.getHeader():
                print(row)

        for i, option in enumerate(options):
            option = '->' + option if i == hovering else '  ' + option 
            print(option.rjust(25 + len(option)))
