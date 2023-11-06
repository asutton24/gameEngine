def clearFile(path):
    with open(path, 'w') as file:
        pass

def hello():
    print('hello')

def main():
    running = True
    while running:
        eval(input())

main()