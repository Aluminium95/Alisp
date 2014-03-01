#-*- coding: utf-8 -*-
# executeur.py
#
# Aliaume Lopez
#
# Réduit un AST
#
# Ce fichier contient les fonctions qui ne sont 
# pas des fonctions de base des classes de Cellules 
# par exemple les principales macros, définition 
# de variable etc ... 
#
# TODO:
#	Trouver un meilleur moyen 
#	d'interfacer le code alisp
#	avec python : comment définir
#	de nouvelles fonctions en python
#	simplement ... 
#
# TODO:
#	Fonctions avec un nombre infini
# 	d'arguments .... Faire que ce soit
# 	possible d'en coder ... 
#
# 	C'est à gérer dans le parser plutôt 
# 	(fun x body) -> x = liste des arguments passés 
# 	(fun (a b . c) body) -> c = liste des arguments restants
# 	Peut-être simplement créer vararg fun (vfun) ? 


import cellule as cel

def varlist (contexte):
	""" Sort la liste des variables 
		et leur valeur dans le contexte 
		actuel (dans un dico)
	"""
	d = cel.Dico ([]) # un dictionnaire vide 
	a = {}
	for i in contexte.bindings:
		a[i] = contexte.get (i)
	
	d.dico = a
	return d
	

def bodyRun (contexte, *l):
	"""
		Lance tout les arguments 
		et retourne la valeur du 
		dernier 
	"""
	return l[-1]

def quote (contexte, e):
	""" 
		Retourne l'expression 
		telle quelle 
	"""
	return e

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

def addToList (contexte, e, l):
	return cel.Liste (l + [e])

def define (contexte, v, e):
	e = eval (e, contexte)
	contexte.set (v, e)
	
def condition (contexte, question, vrai, fausse):
	q = question.eval (contexte)
	if isinstance (q,cel.Erreur):
		return q
	else:			
		if q.vrai ().nom == "true": 
			return vrai.eval (contexte)
		else:
			return fausse.eval (contexte)

def et (contexte, *propositions):
	for i in propositions:
		if i.vrai ().nom == "false":
			return cel.Atome ("false")
	return cel.Atome ("true")

def ou (contexte, *propositions):
	for i in propositions:
		if i.vrai ().nom == "true":
			return cel.Atome ("true")
	return cel.Atome ("false")

def vrai (contexte, a):
	if isinstance (a, cel.Atome):
		return a.vrai ()
	else:
		return cel.Atome ("true")

def faux (contexte, a):
	if isinstance (a, cel.Atome):
		return a.faux ()
	else:
		return cel.Atome ("faux")

def non (contexte, a):
	if isinstance (a, cel.Atome):
		if a.nom == "true":
			return cel.Atome ("false")
		else:
			return cel.Atome ("true")
	else:
		return cel.Erreur ("NotBool", "aurnist")
	
def err (contexte, tp, msg):
	if isinstance (tp, cel.Atome):
		return cel.Erreur (tp, msg)
	else:
		return cel.Erreur (cel.Atome ("InvalidArgument"), cel.String ("..."))

def errtype (contexte, err):
	if isinstance (err, cel.Erreur):
		return err.tp
	else:
		return cel.Erreur (cel.Atome ("InvalidArgument"), cel.String ("..."))

def match (contexte, variable, dico):
	# 
	# ---- Faire un match structurel !
	# 		: permettre des variables 	
	# 		: permettre des 
	variable = variable.eval (contexte)
	
	# une putain de grosse fonction qui fait un match sur des valeurs 
	for i in dico.dico: # pour chaque clef on teste si on matche 
		if variable.__eq__ (i):
			return dico.dico[i]
	return cel.Erreur (cel.Atome ("NoMatch"), variable)

def let (contexte, variable, valeur, body):
	valeur = valeur.eval (contexte)
	ctx = cel.Contexte (contexte) # crée un nouveau contexte
	ctx.set (variable, valeur)
	return body.eval (ctx) 
	
def vareval (contexte, expr):
	return expr.eval (contexte).eval (contexte)
	
def codegen (contexte, expr):
	""" Crée du code à partir d'une 
		expression ... c'est à dire
		retourne la même expression 
		mais en remplaçant les 
		termes qui commencent par 
		un (replace)
		
		euh ... ce code plante quand utilisé 
		de manière récursive ... 
	"""
	if isinstance (expr, cel.Liste):
		if len (expr.liste) > 0:
			if expr.liste[0] == cel.Variable ("@"):
				if len (expr.liste) > 2:
					l = [ i.eval (contexte) for i in expr.liste]
					return cel.Liste (l)
				else:
					return expr.liste[1].eval (contexte)
			else:
				l = [ codegen (contexte, e) for e in expr.liste ]
				return cel.Liste (l)
		else:
			return cel.Liste ([])
	else:
		return expr
		

def codegeneval (contexte, expr):
	a = codegen (contexte, expr)
	return vareval (contexte, a)

def listevide (contexte, expr):
	if isinstance (expr, cel.Liste) and len (expr.liste) == 0:
		return cel.Atome ("true")
	else:
		return cel.Atome ("false")
	
def version (contexte, *expr):
	return cel.Atome ("alpha-1")

def mape (contexte, fonction, liste):
	l = []
	for i in liste.liste:
		l.append (fonction.run (contexte, [i]))
	return cel.Liste (l)

def filtre (contexte, fonction, liste):
	l = []
	for i in liste.liste:
		r = fonction.run (contexte, [i])
		if r.vrai ():
			l.append (i)
	return cel.Liste (l)


# Liste des fonctions 
# avec leur nom attaché !
# C'est pas très joli de le faire comme ça ... il faudrait 
# pouvoir rendre ça dynamique ?
built_in_macros = {
			'fun' : createLambda,			
			'macro' : createMacro,
			'def'  : define,
			'si' : condition,
			'quote' : quote,
			'match' : match,
			'let' : let,
			'eval' : vareval,
			'essai' : cel.Erreur.essai,
			'codegen' : codegen,
			'create' : codegeneval 
		}

built_in_funcs = {
			'liste-variables' : varlist,
			'body' : bodyRun,
			'version' : version,
			'liste' : createList,
			'egal?' : cel.Cellule.egal,
			'tete' : cel.Liste.head,
			'queue' : cel.Liste.tail,
			'ajouter' : cel.Liste.push,
			'concat' : cel.String.append,
			'chaine?' : cel.String.tp,
			'nombre?' : cel.Nombre.tp,
			'erreur?' : cel.Erreur.tp,
			'fun?' : cel.Lambda.tp,
			'atome?' : cel.Atome.tp,
			'liste?' : cel.Liste.tp,
			'null?' : listevide,
			'dico?'  : cel.Dico.tp,
			'variable?' : cel.Variable.tp,
			'+' : cel.Nombre.plus,
			'-' : cel.Nombre.moins,
			'*' : cel.Nombre.mult,
			'/' : cel.Nombre.div,
			'ou' : ou,
			'et' : et,
			'true?' : vrai,
			'false?' : faux,
			'erreur' : err,
			'errtype' : errtype,
			'lever' : cel.Erreur.lever,
			'map' : mape,
			'filter' : filtre
		}

# Ajouter des nouvelles fonctions
# à un contexte ! Les fonctions dont 
# l'utilisateur a besoin !
def addBuiltInFunc (ctx, nom,f):
	ctx.set (cel.Variable (nom), cel.BuiltInLambda (f, nom))

def addBuiltInMacro (ctx, nom,f):
	ctx.set (cel.Variable (nom), cel.BuiltInMacro (f, nom))
	
def addBuiltInMacros (ctx, dictionnaire):
	for i in dictionnaire:
		addBuiltInMacro(ctx, i, dictionnaire[i])
	
def addBuiltInFuncs (ctx, dictionnaire):
	for i in dictionnaire:
		addBuiltInFunc (ctx, i, dictionnaire[i])

def eval (e, contexte):
	return e.eval (contexte)

