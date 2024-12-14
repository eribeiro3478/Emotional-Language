import re




precedence = {
   '==': 0, '!=': 0, '<=': 0, '>=': 0, '<': 0, '>': 0,
   '+': 1, '-': 1, '*': 2, '/': 2, '%': 2
}
operators = set(precedence.keys())




def interpret(filename):
   with open(filename) as file:
       s = dict()
       if_stack = [] 
       loop_stack = []
       lines = file.readlines()
       i = 0




       def tokenize(expression):
           """
           Tokenizes an expression, separating numbers, variables, and operators.
           """
           token_specification = [
               ('NUMBER',   r'\d+\.\d+|\d+'),   
               ('BOOL',     r'True|False'),     
               ('OP',       r'==|!=|<=|>=|[<>]=?|[+\-*/%()]'), 
               ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'), 
               ('SKIP',     r'[ \t]+'),         
               ('MISMATCH', r'.'),             
           ]
           tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
           get_token = re.compile(tok_regex).match
           tokens = []
           pos = 0
           mo = get_token(expression, pos)
           while mo is not None:
               kind = mo.lastgroup
               value = mo.group(kind)
               if kind == 'NUMBER':
                   tokens.append(value)
               elif kind == 'BOOL':
                   tokens.append(value)
               elif kind == 'IDENT':
                   tokens.append(value)
               elif kind == 'OP':
                   tokens.append(value)
               elif kind == 'SKIP':
                   pass
               elif kind == 'MISMATCH':
                   print(f'Error: Unexpected character {value}')
                   return []
               pos = mo.end()
               mo = get_token(expression, pos)
           return tokens




       def shunting_yard(tokens):
           """
           Converts the tokenized expression to postfix notation using the shunting-yard algorithm.
           """
           output = []
           stack = []




           for token in tokens:
               if re.match(r'\d+(\.\d+)?', token): 
                   output.append(token)
               elif token in ('True', 'False'): 
                   output.append(token)
               elif re.match(r'[A-Za-z_][A-Za-z0-9_]*', token): 
                   output.append(token)
               elif token in operators:
                   while (stack and stack[-1] in operators and
                          precedence[token] <= precedence[stack[-1]]):
                       output.append(stack.pop())
                   stack.append(token)
               elif token == '(':
                   stack.append(token)
               elif token == ')':
                   while stack and stack[-1] != '(':
                       output.append(stack.pop())
                   if stack and stack[-1] == '(':
                       stack.pop()
                   else:
                       print("Error: Mismatched parentheses")
                       return []
               else:
                   print(f"Error: Unknown token '{token}'")
                   return []
           while stack:
               if stack[-1] == '(' or stack[-1] == ')':
                   print("Error: Mismatched parentheses")
                   return []
               output.append(stack.pop())
           return output




       def evaluate_postfix(postfix):
           """
           Evaluates a postfix expression.
           """
           stack = []




           for token in postfix:
               if token in ('True', 'False'):
                   stack.append(True if token == 'True' else False)
               elif re.match(r'\d+(\.\d+)?', token): 
                   stack.append(float(token))
               elif re.match(r'[A-Za-z_][A-Za-z0-9_]*', token): 
                   if token in s:
                       stack.append(s[token])
                   else:
                       print(f"Error: Variable '{token}' not defined")
                       return None
               elif token in operators:
                   if token in ('+', '-', '*', '/', '%'):
                       if len(stack) < 2:
                           print("Error: Not enough operands")
                           return None
                       b = stack.pop()
                       a = stack.pop()
                       if token == '+':
                           stack.append(a + b)
                       elif token == '-':
                           stack.append(a - b)
                       elif token == '*':
                           stack.append(a * b)
                       elif token == '/':
                           if b == 0:
                               print("Error: Division by zero")
                               return None
                           stack.append(a / b)
                       elif token == '%':
                           stack.append(a % b)
                   elif token in ('==', '!=', '<', '>', '<=', '>='):
                       if len(stack) < 2:
                           print("Error: Not enough operands for comparison")
                           return None
                       b = stack.pop()
                       a = stack.pop()
                       if token == '==':
                           stack.append(a == b)
                       elif token == '!=':
                           stack.append(a != b)
                       elif token == '<':
                           stack.append(a < b)
                       elif token == '>':
                           stack.append(a > b)
                       elif token == '<=':
                           stack.append(a <= b)
                       elif token == '>=':
                           stack.append(a >= b)
               else:
                   print(f"Error: Unknown operator '{token}'")
                   return None
           if len(stack) != 1:
               print("Error: Invalid expression")
               return None
           return stack[0]




       def parse_expression(expr):
           """
           Parse and evaluate a mathematical or boolean expression without eval().
           """
           tokens = tokenize(expr)
           if not tokens:
               return None
           postfix = shunting_yard(tokens)
           if not postfix:
               return None
           return evaluate_postfix(postfix)




       while i < len(lines):
           line = lines[i].strip()
 
         
           if '#' in line:
               line = line.split('#', 1)[0].strip()
 
         
           if line == '':
               i += 1
               continue




         
           execute_line = (all(if_stack) if if_stack else True) and (all(loop['execute'] for loop in loop_stack) if loop_stack else True)




           if line.startswith("if "):
             
               condition = line[3:].strip()
               result = parse_expression(condition)
               if isinstance(result, bool):
                   if_stack.append(result)
                   if not result:
                     
                       nested = 1
                       while nested > 0:
                           i += 1
                           if i >= len(lines):
                               print("Error: IF statement without matching 'end'")
                               return
                           next_line = lines[i].strip()
                           if '#' in next_line:
                               next_line = next_line.split('#', 1)[0].strip()
                           if next_line.startswith("if "):
                               nested += 1
                           elif next_line == "end":
                               nested -= 1
                           elif next_line.startswith(("while ", "for ")):
                               nested += 1
                       if_stack.pop() 
                       i += 1
                       continue
               else:
                   print(f"Error: Invalid condition '{condition}'")
                 
                   nested = 1
                   while nested > 0:
                       i += 1
                       if i >= len(lines):
                           print("Error: IF statement without matching 'end'")
                           return
                       next_line = lines[i].strip()
                       if '#' in next_line:
                           next_line = next_line.split('#', 1)[0].strip()
                       if next_line.startswith("if "):
                           nested += 1
                       elif next_line == "end":
                           nested -= 1
                       elif next_line.startswith(("while ", "for ")):
                           nested += 1
                   i += 1
                   continue
               i += 1
               continue
           elif line == "end":
             
               if loop_stack:
                   loop = loop_stack[-1]
                   if loop['type'] == 'while':
                     
                       result = parse_expression(loop['condition'])
                       if isinstance(result, bool) and result:
                           i = loop['start_line']
                       else:
                           loop_stack.pop()
                           i += 1
                   elif loop['type'] == 'for':
                     
                       s[loop['var']] += loop['step']
                     
                       current_value = s[loop['var']]
                       if ((loop['step'] > 0 and current_value <= loop['end']) or
                           (loop['step'] < 0 and current_value >= loop['end'])):
                           i = loop['start_line']
                       else:
                           loop_stack.pop()
                           i += 1
                   else:
                       print("Error: Unknown loop type")
                       loop_stack.pop()
                       i += 1
               elif if_stack:
                   if_stack.pop()
                   i += 1
               else:
                   print("Error: 'end' without matching 'if', 'while', or 'for'")
                   i += 1
               continue
           elif line.startswith("endure "):
             
               condition = line[6:].strip()
               result = parse_expression(condition)
               if isinstance(result, bool):
                   if result:
                       loop_stack.append({'type': 'while', 'start_line': i + 1, 'condition': condition, 'execute': True})
                       i += 1
                   else:
                     
                       nested = 1
                       while nested > 0:
                           i += 1
                           if i >= len(lines):
                               print("Error: WHILE loop without matching 'end'")
                               return
                           next_line = lines[i].strip()
                           if '#' in next_line:
                               next_line = next_line.split('#', 1)[0].strip()
                           if next_line.startswith("while "):
                               nested += 1
                           elif next_line == "end":
                               nested -= 1
                           elif next_line.startswith(("if ", "for ")):
                               nested += 1
                       i += 1
                   continue
               else:
                   print(f"Error: Invalid condition '{condition}'")
                 
                   nested = 1
                   while nested > 0:
                       i += 1
                       if i >= len(lines):
                           print("Error: WHILE loop without matching 'end'")
                           return
                       next_line = lines[i].strip()
                       if '#' in next_line:
                           next_line = next_line.split('#', 1)[0].strip()
                       if next_line.startswith("while "):
                           nested += 1
                       elif next_line == "end":
                           nested -= 1
                       elif next_line.startswith(("if ", "for ")):
                           nested += 1
                   i += 1
                   continue
           elif line.startswith("persevere "):
             
               for_match = re.match(r'persevere\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s+to\s+(.+?)(\s+step\s+(.+))?$', line)
               if for_match:
                   var = for_match.group(1)
                   start_expr = for_match.group(2)
                   end_expr = for_match.group(3)
                   step_expr = for_match.group(5) if for_match.group(4) else "1"




                   start_value = parse_expression(start_expr)
                   end_value = parse_expression(end_expr)
                   step_value = parse_expression(step_expr)




                   if start_value is None or end_value is None or step_value is None:
                       print(f"Error: Invalid FOR loop expression in line '{line}'")
                     
                       nested = 1
                       while nested > 0:
                           i += 1
                           if i >= len(lines):
                               print("Error: FOR loop without matching 'end'")
                               return
                           next_line = lines[i].strip()
                           if '#' in next_line:
                               next_line = next_line.split('#', 1)[0].strip()
                           if next_line.startswith("for "):
                               nested += 1
                           elif next_line == "end":
                               nested -= 1
                           elif next_line.startswith(("if ", "while ")):
                               nested += 1
                       i += 1
                       continue




                 
                   s[var] = start_value
                   loop_stack.append({
                       'type': 'for',
                       'start_line': i + 1,
                       'var': var,
                       'end': end_value,
                       'step': step_value,
                       'execute': True
                   })
                   i += 1
                   continue
               else:
                   print(f"Error: Invalid FOR loop syntax in line '{line}'")
                   i += 1
                   continue




           if execute_line:
               if line.startswith("mood "):
                 
                   try:
                       definition = line[4:].strip()
                       var, val = definition.split("=", 1)
                       var = var.strip()
                       val = val.strip()
                       result = parse_expression(val)
                       if result is not None:
                           s[var] = result
                       else:
                           print(f"Error: Invalid expression in assignment '{line}'")
                   except ValueError:
                       print(f"Error: Invalid variable assignment '{line}'")
               elif line.startswith("share(") and line.endswith(")"):
                 
                   try:
                       print_content = line[6:-1].strip()
                       if print_content.startswith("\"") and print_content.endswith("\""):
                         
                           print(print_content[1:-1])
                       else:
                           result = parse_expression(print_content)
                           if result is not None:
                               print(result)
                           else:
                               if print_content in s:
                                   print(s[print_content])
                               else:
                                   print(f"Error: Variable '{print_content}' not defined")
                   except Exception as e:
                       print(f"Error: Invalid print statement '{line}'. {e}")
               else:
                   print(f"Error: Unrecognized statement '{line}'")
           i += 1




interpret("program1.emo")


