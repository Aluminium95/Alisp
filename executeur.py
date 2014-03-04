#-*- coding: utf-8 -*-
# executeur.py
#
# Aliaume Lopez
#
# Réduit un AST : IE celui qui exécute le code 
# il servira de base pour la machine virtuelle
# même si pour des raisons de simplification 
# beaucoup de code d'évaluation est réparti
# dans les classes de Cellule 
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
#	simplement ... Et respecter le typage ?
# 	ainsi que le nombre d'arguments 
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
#
# 

import cellule as cel

# import des fonctions et macros de base 
from Builtin.fonctionsbasiques import *
from Builtin.macrosbasiques import *
from Builtin.macrosavancees import * 

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
	
def let (contexte, variable, valeur, body):
	valeur = valeur.eval (contexte)
	ctx = cel.Contexte (contexte) # crée un nouveau contexte
	ctx.set (variable, valeur)
	return body.eval (ctx)

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

def listevide (contexte, expr):
	if isinstance (expr, cel.Liste) and len (expr.liste) == 0:
		return cel.Atome ("true")
	else:
		return cel.Atome ("false")
	
def version (contexte, *expr):
	return cel.Atome ("alpha-2")

# TODO : ne pas faire ces fonctions sur 
# des listes mais sur des éléments itérables 
# et retourner des générateurs ! (économies 
# de ressources)
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
			'tantque' : whileloop,
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
			'assoc' : cel.Dico.assoc,
			'dissoc' : cel.Dico.dessoc,
			'variable?' : cel.Variable.tp,
			'+' : cel.Nombre.plus,
			'-' : cel.Nombre.moins,
			'*' : cel.Nombre.mult,
			'/' : cel.Nombre.div,
			'ou' : ou,
			'et' : et,
			'non' : non,
			'true?' : vrai,
			'false?' : faux,
			'erreur' : err,
			'errtype' : errtype,
			'lever' : cel.Erreur.lever,
			'map' : mape,
			'filter' : filtre,
			'<' : cel.Nombre.inf,
			'>' : cel.Nombre.sup,
			'<=' : cel.Nombre.infeg,
			'>=' : cel.Nombre.supeg
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

# La grosse fonction !
def eval (e, contexte):
	return e.eval (contexte)

