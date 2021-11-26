def is_number_func(str):
    """
    Check if entered string is a number
    :param str: string to check
    :return: bool value (it is a number - True, else - False)
    """
    try:
        float(str)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    print('''
    This is a prorgam for temperature convertation into different units!
    Available T units: celsius, kelvin, fahrenheit
    Units input: T units you have
    Units output: T units you want to get
    Value to convert: T value to convert from units unput to units output\n
    If you want to exit program, just enter "exit" in any line.\n
    ''')
    available_units = {'celsius', 'kelvin', 'fahrenheit'}
    units_abbr = {'celsius': 'C', 'kelvin': 'K', 'fahrenheit': 'F'}
    while True:
        units_input = input('Units input: ')
        if units_input == 'exit':
            break
        units_output = input('Units output: ')
        if units_output == 'exit':
            break
        while not all([unit in available_units for unit in (units_input, units_output)]):
            print('Unavailable units!')
            print('List of available units: celsius, kelvin, fahrenheit\n')
            units_input = input('Units input: ')
            if units_output == 'exit':
                break
            units_output = input('Units output: ')
            if units_output == 'exit':
                break
        value = input('Value to convert: ')
        if value == 'exit':
            break
        while not is_number_func(value):
            print('{value} is not a number! Try again!\n'.format(value=value))
            value = input('Value to convert: ')
            if value == 'exit':
                break
        value = float(value)
        if units_input == 'celsius' and value < -273.15:
            print('''
            WARNING: Convertation still will be done
            But please note that T cannot be less than -273.15 C!\n''')
        elif units_input == 'kelvin' and value < 0:
            print('''
            WARNING: Convertation still will be done
            But please note that T cannot be less than 0 K!\n''')
        elif units_input == 'fahrenheit' and value < -459.67:
            print('''
            WARNING: Convertation still will be done
            But please note that T cannot be less than -459.67 F!\n''')
        if units_input == 'celsius':
            if units_output == 'kelvin':
                res = value + 273.15
            elif units_output == 'fahrenheit':
                res = value*(9 / 5) + 32
        elif units_input == 'kelvin':
            if units_output == 'celsius':
                res = value - 273.15
            elif units_output == 'fahrenheit':
                res = (value - 273.15)*(9 / 5) + 32
        else:
            if units_output == 'celsius':
                res = round((value-32)*5/9, 4)
            elif units_output == 'kelvin':
                res = (value-32)*5/9+273.15
        print('T: {value} {units_input} = {res} {units_output}\n'.format(value=value,
                                                                         units_input=units_abbr[units_input],
                                                                         res=round(res, 3),
                                                                         units_output=units_abbr[units_output]))
