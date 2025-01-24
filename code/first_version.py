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
            You need to reponse me only 2 things
                name of the mathematical function along with its interval
                    ex. for sine graph and interval of -1, 2. Response: sine,-1,2
                    for cosine from a to b: cosine,a,b
                    for tangent from a to b: tangent,a,b
                    for line like y=x from a to b: identity,a,b
                    for x^2 from a to b: quadratics,a,b

            Extra1(no interval): if the users didn't provide an interval.
                    You should response the interval 0,10 by defualt

            Extra2(no function name): if the users didn't provide a name of function.
                    You should response with: "Please provide the name of the function."

            Extra3(exit code): if the users don't want to plot any more they will say somethings like, 
            bye or other ending conversation type of word. For this you should response: 'exit'

            Extra4(the interval): the interval from a to b. B must be more than a.
                    ex. if users promt "sine from 20 to 10" You should response 10 before 20

            The user input will be at bottom most of the prompt
        '''
user_greet = 'Hi! What graph and interval do you want to plot? ex.sine from -5 to 5: '

def plot_sin(x):
    y = np.sin(x)
    plt.plot(x, y)
    plt.title('Graph of f(x) = sin(x)')

def plot_cos(x):
    y = np.cos(x)
    plt.plot(x, y)
    plt.title('Graph of f(x) = cos(x)')

def plot_tan(x):
    y = np.tan(x)
    plt.plot(x, y)
    plt.title('Graph of f(x) = tan(x)')

def plot_line(x):
    plt.plot(x, x)
    plt.title('Graph of f(x) = x')

def plot_x_sq(x):
    y = x ** 2
    plt.plot(x, y)
    plt.title('Graph of f(x) = x^2')

def plotting(func_name, x, x_min, x_max):
    print(f'Plotting {func_name} function in interval: [{x_min}, {x_max}]')
    if func_name == 'sine':
        plot_sin(x)
    elif func_name == 'cosine':
        plot_cos(x)
    elif func_name == 'tangent':
        plot_tan(x)
    elif func_name == 'identity':
        plot_line(x)
    elif func_name == 'quadratics':
        plot_x_sq(x)

def main():
    user_input = input(f'{user_greet}')
    user_prompt = PROMPT + '\nuser_input:' + user_input
    while True:
        if user_input is None:
            user_input = input('Provide a formula of next graph if you are ready!: ')
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
        if answer == 'exit':
            print('Thanks for using our plot service!\nSee ya!')
            break
        func_name, x_min, x_max = answer.split(',')
        points = (int(x_max) - int(x_min)) * 100
        x_axis = np.linspace(int(x_min), int(x_max), points)
        plotting(func_name, x_axis, x_min, x_max)
        plt.show()
        user_input = None
if __name__ == '__main__':
    main()

# End of file
