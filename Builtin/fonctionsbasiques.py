# fonctionsbasiques.py
#
# Lopez Aliaume
#
# Les fonctions de base 
# de Alisp : tout ce qui 
# est vraiment vraiment bas niveau

def bodyRun (contexte, *l):
	"""
		Lance tout les arguments 
		et retourne la valeur du 
		dernier 
	"""
	return l[-1]
	
def createList (contexte, *l):
	""" Crée une liste """
	c = cel.Liste (list (l))
	return c

def createLambda (contexte, args, body):
	""" Crée une fonction ! """
	c = cel.Lambda (cel.Contexte (contexte), args, body)
	return c

def createMacro (contexte, args, body):
	""" Crée une macro """
	return cel.Macro (cel.Contexte (contexte), args, body) # syntaxe spéciale ? quote unquote ?
