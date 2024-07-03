from collections import defaultdict, deque

class Formula_Runner:

    def __init__(self) -> None:
        self.pred = {'(': 4, '^': 3, '*': 2, '/': 2, '+': 1, '-': 1}
        self.dependencies = defaultdict(set)
        self.dependent = defaultdict(set)
        self.cell_values = {}


    """
    Set the dependency of the cells if their are multiple cells involved in
    value of the cell 
    """
    def set_cell_value(self, cell, value):
        self.cell_values[cell] = value

        if value.startswith('='):
            dependencies = value[value.index('(') + 1: -1].split(',')
            #I am assuming that that the method has cell refs
            for dependency in dependencies:
                self.dependencies[cell].add(dependency)
                self.dependent[dependency].add(cell)

    """
    Start by evaluating the cell
    """
    def evaluate_cell(self, cell):
        order = self.get_cell_order_exec()
        print(order)
        for node in order:
            cell_val = self.cell_values[node]
            if cell_val.startswith('='):
                func = cell_val[1: cell_val.index("(")]
                args = cell_val[cell_val.index('(') + 1: -1]
                self.cell_values[node] = str(self.convert_to_infix(func, args))
            else:
                #assuming that other than formula the value can only be an integer
                continue

    """
    Converting the infix expression to postfix expression array
    """
    def infix_to_postfix(self, expr):
        post = []
        stack = []
        for i in range(len(expr)):
            if expr[i].isdigit():
                post.append(expr[i])
            elif expr[i] == '(':
                stack.append(expr[i])
            elif expr[i] == ')':
                while stack[-1] != '(':
                    post.append(stack.pop())
            else:
                while stack and self.pred[expr[i]] <= self.pred[stack[-1]]:
                    post.append(stack.pop())
                stack.append(expr[i])
        while stack:
            post.append(stack.pop())        
        
        return post
    
    def evaluate_post(self, postExp):
        stack = []
        for i in range(len(postExp)):
            if postExp[i].isdigit():
                stack.append(int(postExp[i]))
            elif postExp[i] == '+':
                a = stack.pop()
                b = stack.pop()
                stack.append(a + b)
            elif postExp[i] == '-':
                a = stack.pop()
                b = stack.pop()
                stack.append(b-a)
            elif postExp[i] == '*':
                a = stack.pop()
                b = stack.pop()
                stack.append(b*a)
            elif postExp[i] == '/':
                a = stack.pop()
                b = stack.pop()
                stack.append(b/a)
        return stack[0]

    """
    This will convert the it in to infix expression to evaluated
    """
    def convert_to_infix(self, func, args):
        print(func, args)
        if func == 'SUM':
            #the values are comma seperated
            tokens = args.split(',')
            tokens = [self.cell_values[token] for token in tokens]
            expression = '+'.join(tokens)
            post_exp = self.infix_to_postfix(expression)
            return self.evaluate_post(post_exp)

    """
    Get the order of evaluating the cell if multiple cell references are 
    involved
    """
    def get_cell_order_exec(self, node):
        indegree = defaultdict(int)
        for cell in self.cell_values:
            print(cell)
            for _ in self.dependencies[cell]:
                indegree[cell] += 1

        # initialize the queue with 0 indegree edges
        q = deque([node for node in self.cell_values if indegree[node] == 0])

        order = []
        while q:
            cell = q.popleft()
            order.append(cell)
            for dep in self.dependent[cell]:
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    q.append(dep)
            if indegree[node] == 0:
                break
        if indegree[node] == 0:
            return order
        if len(order) != len(self.cell_values):
            raise ValueError('Circular dependency detected')

        return order



fr = Formula_Runner()
fr.set_cell_value('A1', '3')
fr.set_cell_value('A2', '4')
fr.set_cell_value('B1', '=SUM(A1,A2)')
fr.set_cell_value('D1', '=SUM(A2,B1)')

fr.evaluate_cell('D1')
print(fr.cell_values['D1'])
print(fr.cell_values['D1'])
