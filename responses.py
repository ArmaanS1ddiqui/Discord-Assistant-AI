from random import choice , randint
from datetime import datetime


def get_response(user_input: str) -> str:

    command = user_input.lower().strip()

    if command == '':
        return 'Well You\'re awfully silent....'
    elif command == 'hello' or command == 'hi':
        return 'Hello There!'
    elif command == "how are you?" or command == "whats up?":
        return 'I am doing well. how about you?'
    elif command == 'bye':
        return 'Bye, hit me up if you need anything'
    elif command == "roll dice":
        return f'you rolled: {randint(1,6)}'    
    
    elif command == "What time is it?" or command == "Whats the Time":
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
    elif command == "flip a coin":
        return f'You Got:{choice(["Heads","Tails"])}!'
    elif command == "math" or command == "solve":
        try:
            result = eval(user_input.replace("$solve","").replace("$math","").strip())
            return f"The answer is {result}"
        except Exception as e:
            return "Sorry i couldnt solve that.. please try again"
    
    else:
        return choice(['I do not understand... i am in early stages of development so my communication is a work in progress \n **Try using $help**',
                       'what are you talking about?.... i am in early stages of development so my communication is a work in progress \n **Try using $help**',
                       'Do you mind rephrasing that?... i am in early stages of development so my communication is a work in progress \n **Try using $help**'])