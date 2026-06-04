import requests
def Aiprocess(command):
    prompt = f"Answer in 1-2 lines. If it's a coding task, provide only the code without explanation: {command}"
    
    response = requests.get(f"https://text.pollinations.ai/{prompt}?model=openai")
    return response.text

print(Aiprocess("Write a Python function to calculate the factorial of a number."))