# builtin.py
#
# Lopez Aliaume
#
# Fonctions de base dans le langage

def bodyRun (contexte, *l):
	return l[-1]

def createList (contexte, *l):
	c = cel.Liste (list (l))
	return c

def createLambda (contexte, args, body):
	c = cel.Lambda (args, body)

	return c

def addToList (contexte, e, l):
	return cel.Liste (l + [e])

def define (contexte, v, e):
	e = eval (e, contexte)
	contexte.set (v, e)

built_in_macros = {
			'lambda' : createLambda,
			'def'  : define
		}

built_in_funcs = {
			'add' : addToList,
			'list' : createList,
			'body' : bodyRun,
			'head' : cel.Liste.head,
			'tail' : cel.Liste.tail,
			'append' : cel.String.append
		}
