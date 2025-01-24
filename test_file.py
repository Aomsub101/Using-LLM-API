import os
import dotenv
from mistralai import Mistral

# -------- init part -------- #
dotenv.load_dotenv()
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)
# -------- init part -------- #
PROMPT = '''In this program users will ask us to plot a mathematical graph.
            They will tell
                1. what kind of function they want
                2. the x-interval they want
            You need to reponse me only 2 things
                name of the mathematical function along with its interval
                    ex. for sine graph and interval of -1, 2. Response: sine, -1, 2
                    for cosine from a to b: cosine, a, b
                    for tangent from a to b: tangent, a, b
                    for line like y=x from a to b: identity function, a, b
                    for x^2 from a to b: quadratics, a, b
            Extra(no interval): if the users didn't provide an interval.
                    You should response the interval 0, 10 by defualt
            Extra(no function name): if the users didn't provide a name of function.
                    You should response with: "Please provide the name of the function."
            Extra(exit code): if the users don't want to plot any more they will say somethings like, bye
                    or other ending conversation type of word. For this you should response: exit
            Extra(the interval): the interval from a to b. B must be more than a.
                    ex. if users promt "sine from 20 to 10" You should response 10 before 20
            The user input will be at bottom most of the prompt
        '''
user_greet = 'Hi! What graph and interval do you want to plot? ex.sine from -5 to 5: '
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
        print(response.choices[0].message.content)

if __name__ == '__main__':
    main()
# End of file
