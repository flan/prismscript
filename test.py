import prismscript.interpreter
i = prismscript.interpreter.Interpreter(open('quickcall.src').read())
print(i.list_nodes())
print(i.list_functions())

print()

i.execute_node('setup')

print()

print(i._globals)
for l in i.get_log():
    print('\t' + l)
    
