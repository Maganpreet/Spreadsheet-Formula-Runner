from collections import defaultdict
from collections import deque

class formula_runner:

    def __init__(self) -> None:
        self.cell_values = {}
        self.exp = ''
        self.post = []
        self.dependencies = defaultdict(set)        
        self.dependent = defaultdict(set)

    def infix_to_postfix(self):
        pred = {'(': 4, '^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
        stack = []
        num = 0
        for i in range(len(self.exp)):
            """
                if it is a digit then push it post
                else
                    check if stack is not empty and pred[si] > pred[stack[-1]]
                        then push to stack
                    else if stack and s[i] == ')'
                        then pop the elements from stack until stack[-1] == '('
                    else if stack and pred[s[i]] < pred[stack[-1]] #### why do i pop it when the precedence is less cause according to BODMAS multiple/div happens before additon/sub 
                        then pop elements until pred[s[i]] > pred[stack[-1]] or stack empty
                        then push to stack
            """
            if self.exp[i] != ' ':
                 #(1+(2+3)-2)-9+2
                if self.exp[i].isdigit():
                    self.post.append(self.exp[i])
                elif self.exp[i] == ')':
                    while stack and stack[-1] != '(':
                        self.post.append(stack.pop())
                    stack.pop()
                elif stack and pred[self.exp[i]] <= pred[stack[-1]] and stack[-1] != '(':
                    while stack and pred[self.exp[i]] <= pred[stack[-1]] and stack[-1] != '(':
                        self.post.append(stack.pop())
                    stack.append(self.exp[i])
                else:
                    stack.append(self.exp[i]) 
        while stack:
            self.post.append(stack.pop())
        print(self.post)



    def set_cell_values(self, cell, value):
        print(cell, type(value))
        self.cell_values[cell] = value
        print(cell, type(self.cell_values[cell]))
        if value.startswith('='):
            tokens = value[value.index('(') + 1: -1].split(',')
            for token in tokens:
                self.dependencies[cell].add(token)
                self.dependent[token].add(cell)




    def get_cell_exec_order(self):
        indegree = defaultdict(int)

        for cell in self.cell_values:
            for _ in self.dependencies[cell]:
                indegree[cell] += 1
        
        q = deque([cell for cell in self.cell_values if indegree[cell] == 0])
        order = []

        while q:
            cell = q.popleft()
            order.append(cell)
            for dep in self.dependent[cell]:
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    q.append(dep)
        
        return order



    def eval_postfix(self) -> int:
        stack = []
        for i in range(len(self.post)):
            if self.post[i] == '+':
                a = stack.pop()
                b = stack.pop()
                stack.append(int(a)+ int(b))
            elif self.post[i] == '-':
                a = stack.pop()
                b = stack.pop()
                stack.append(int(b)-int(a))
            elif self.post[i] == '/':
                a = stack.pop()
                b = stack.pop()
                stack.append(int(b) / int(a))
            elif self.post[i] == '*':
                a = stack.pop()
                b = stack.pop()
                stack.append(int(b) * int(a))
            else: stack.append(self.post[i])
        return stack.pop()
    
    def convert_to_infix(self, func, cell_val):
        if func == 'SUM':
            tokens = cell_val.split(',')
            tokens = [self.cell_values[tokens[i]] for i in range(len(tokens))]
            print(type(tokens[0]), cell_val)
            self.exp = '+'.join(tokens)
            print(self.exp)
        self.infix_to_postfix()
        return self.eval_postfix()
    
    def eval_cell(self, cell):
        if self.cell_values[cell][0] == '=':
            func = self.cell_values[cell][1: self.cell_values[cell].index('(')]
            cell_val = self.cell_values[cell][self.cell_values[cell].index('(') + 1: -1]
            return self.convert_to_infix(func, cell_val)    
        else:
            if self.cell_values[cell].isdigit():
                return self.cell_values[cell]


    def run(self) -> int:       
        order = self.get_cell_exec_order()
        for cell in order:
            self.cell_values[cell] = self.eval_cell(cell)





if __name__ == "__main__":

    fr = formula_runner()
    fr.set_cell_values('C2', '=SUM(B1,B2,C1)')
    fr.set_cell_values('B1', '2')
    fr.set_cell_values('B2', '2')
    fr.set_cell_values('C1', '9')

    fr.run()

    print(fr.cell_values['C2'])

    """
    fr0 = formula_runner('1 + ( 2 + 3 ) - 2')
    fr1 = formula_runner('( 1 + ( 2 + 3 ) - 2 ) - 9 + 2') #-4
    fr2 = formula_runner('1 + (6 - 2 + 3 - 5) - 2') #1
    fr3 = formula_runner('2 * ( 4 / 2 * 8 ) + 8 / 2') #1
    print('executing the expression')
    print(fr0.run())
    print(fr1.run())
    #print(fr1.post)
    print(fr2.run())
    print(fr3.run())
    """