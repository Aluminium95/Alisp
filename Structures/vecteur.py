# vecteur.py
#
# Lopez Aliaume
#
# Le vecteur est un tableau
# de taille dynamique plus 
# adapté que celui de python
# pour les petits 
# ajouts et modifications 
#
#
# Implémente itérable

# L'implémentation suit la logique 
# utilisée par Clojure pour son vecteur 
# de même type ... 
#
# Pour le moment c'est un peu fouilli ... 
# il faut le poser sur papier et bien 
# le penser ... 

# -- Les classes -- (types)
class Node:
	def __init__ (self,level,a,b):
		self.level = level
		self.droite = a
		self.gauche = b
	
class Empty:
	pass

class Leaf:
	def __init__ (self, v):
		self.value = v

class Right:
	def __init__ (self,level,a):
		self.level = level
		self.value = a
	
class Left:
	def __init__ (self, level, a):
		self.level = level
		self.value = a
	

def va_droite (n, i):
	if 2 << (n - 1) < i:
		return True
	else:
		return False
	
def suppr_droite (n, i):
	return i - (2 << (n - 1))

def get (tableau, i):
	if isinstance (tableau, Node):
		n = tableau.level
		if va_droite (n, i):
			return get (tableau.gauche, suppr_droite (n,i))
		else:
			return get (tableau.droite, i)
	elif isinstance (tableau, Left):
		get (tableau.value, i)
	elif isinstance (tableau, Right):
		n = tableau.level
		return get (tableau.value, suppr_droite (n,i))
	elif isinstance (tableau,Leaf):
		return tableau.value
	else:
		raise IndexError ("clef inexistante")
	

