import os
import dotenv
from mistralai import Mistral
import matplotlib.pyplot as plt
import numpy as np

# -------- init part -------- #

dotenv.load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"
client = Mistral(api_key=api_key)
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# -------- init part -------- #
PROMPT = '''In this program users will ask us to plot a mathematical graph.
            They will tell
                1. what kind of function they want
                2. the x-interval they want
                3. the multiplier
                    ex. sin(3x). Multiplier is 3
                4(extra). if they ask for polynomial they will give us coefficient
                    ex. 3x^3 + 2x + 2 : coefficient would be (3, 0, 2, 2)

            You need to reponse me
                name of the mathematical function, its interval, its multiplier or coeff. (if polynomial)
                here is the format:
                    if not polynomial: func_name,
                                    interval_left(default: 0),
                                    interval_right(default: 10),
                                    multiplier(default: 1)
                        ex. if users ask for sine(-x) from -1 to 20
                        Response must be: sine,-1,20,-1 and nothing more
                        Note: beware of an interval, right interval must > left_interval
                        (Read Extra3(the interval))
                        same logic apply to cosine, tangent, identity
                        ex. for cosine from a to b: cosine,a,b,multiplier
                        ex. for tangent from a to b: tangent,a,b,multiplier
                        ex. for line like y=2x from a to b: identity,a,b,multiplier
                    if polynomial(when see a power like x^2, etc.): func_name with the formula,
                                    interval_left(default: 0),
                                    interval_right(default: 10),
                                    coefficient
                        Note: max degree for polynomial is 4, means you should response 5 coeff.
                        of x^4, x^3, x^2, x, and const respectively. seperate by '/'
                        ex. if users ask for x^4 + 2x^2 + 2 from 1 to 15
                        Response must be: polynomial:x^4 + 2x^2 + 2,1,15,1/0/2/0/2 and nothing more
                        Note: if the users ask a formula not in order, make sure to order them aswell.
                        ex. x^2 - 2x^4 - 5 from 1 - 10
                        Response must be: polynomial:-2x^4 + 2x^2 - 5,1,10,-2/0/2/0/-5 and nothing more
                        Note2: if users provide the same degree make sure to calculate them before response
                        ex. x^2 + x^2 + 3x^4 - 5
                        Response must be: polynomial:3x^4 + 2x^2 - 5,0,10,3/0/2/0/-5 and nothing more

            Extra1(no interval): if the users didn't provide an interval.
                    You should response the interval 0,10 by defualt

            Extra2(no function name): if the users didn't provide a name of function.
                    You should response with: "Please provide the name of the function."

            Extra3(the interval): the interval from a to b. b must be more than a.
                    ex. if users promt "sine from 20 to 10" You should response 10 before 20

            Extra(exit code): if the users don't want to plot any more they will say somethings like, 
            bye or other ending conversation type of word. For this you should response: 'exit'

            The user input will be at bottom most of the prompt
        '''
user_greet = 'Hi! What graph and interval do you want to plot? ex.sin(3x) from -5 to 5: '

def plot_sin(x, multiplier):
    y = np.sin(int(multiplier) * x)
    plt.plot(x, y)
    plt.title(f'Graph of f(x) = sin({multiplier}x)')

def plot_cos(x, multiplier):
    y = np.cos(int(multiplier) * x)
    plt.plot(x, y)
    plt.title(f'Graph of f(x) = cos({multiplier}x)')

def plot_tan(x, multiplier):
    y = np.tan(int(multiplier) * x)
    plt.plot(x, y)
    plt.title(f'Graph of f(x) = tan({multiplier}x)')

def plot_line(x, multiplier):
    plt.plot(x, int(multiplier) * x)
    plt.title(f'Graph of f(x) = {multiplier}x')

def plot_polynomial(x, coeff, formula):
    coeff = np.array(coeff.split('/'))
    y = (int(coeff[0]) * (x**4)) + \
        (int(coeff[1]) * (x**3)) + \
        (int(coeff[2]) * (x**2)) + \
        (int(coeff[3]) * (x**1)) + (int(coeff[4]))
    plt.plot(x, y)
    plt.title(f'Graph of f(x) = {formula}')

def plotting(func_name, x, x_min, x_max, multiplier):
    if 'polynomial' in func_name:
        func_name, formula = func_name.split(':')
        print(f'Plotting {func_name}: {formula} function in interval: [{x_min}, {x_max}]')        
        plot_polynomial(x, multiplier, formula)
        return

    print(f'Plotting {func_name} function in interval: [{x_min}, {x_max}]')        
    if func_name == 'sine':
        plot_sin(x, multiplier)
    elif func_name == 'cosine':
        plot_cos(x, multiplier)
    elif func_name == 'tangent':
        plot_tan(x, multiplier)
    elif func_name == 'identity':
        plot_line(x, multiplier)

def main():
    while True:
        user_input = input(f'{user_greet}')
        user_prompt = PROMPT + '\nuser_input:' + user_input

        response = client.chat.complete(
            model= model,
            messages = [
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ]
        )
        # print(response.choices[0].message.content)
        answer = response.choices[0].message.content
        print(answer)
        if answer == 'Please provide the name of the function.':
            continue
        if answer == 'exit':
            print('Thanks for using our plot service!\nSee ya!')
            break

        func_name, x_min, x_max, multiplier = answer.split(',')
        points = (int(x_max) - int(x_min)) * 100
        x_axis = np.linspace(int(x_min), int(x_max), points)
        plotting(func_name, x_axis, int(x_min), int(x_max), multiplier)
        plt.show()

if __name__ == '__main__':
    main()

# End of file
