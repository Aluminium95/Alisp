# macrosbasiques.py
#
# Lopez Aliaume
#
# Contient les macros de base 
# du langage : 
# let/loop/define etc ... 

def define (contexte, v, e):
	e = e.eval (contexte)
	contexte.set (v, e)
	
	
def vareval (contexte, expr):
	return expr.eval (contexte).eval (contexte)

def condition (contexte, question, vrai, fausse):
	q = question.eval (contexte)
	if isinstance (q,cel.Erreur):
		return q
	else:			
		if q.vrai ().nom == "true": 
			return vrai.eval (contexte)
		else:
			return fausse.eval (contexte)

def quote (contexte, e):
	""" 
		Retourne l'expression 
		telle quelle 
	"""
	return e


def whileloop (contexte, pred, body):
	""" Une petite boucle while,
		juste un predicat et un corps
		de boucle ... On ne copie jamais le contexte !
		C'est la l'utilite

		!!! -- Ce code modifie le contexte externe passé
		en argument !!!
	"""
	a = cel.Liste ([])
	p = pred.eval (contexte)

	while isinstance (p, cel.Atome) and p.pVrai () == True:
		# Normalement, on voit ici que les 
		# contextes sont passés par pointeurs 
		# et que le contexte ici peut être 
		# modifié par le body ! (dans un appel 
		# normal de fonction on ferait une copie 
		# de contexte)
		a = body.eval (contexte)
		p = pred.eval (contexte)

	return a
