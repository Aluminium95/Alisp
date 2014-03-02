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

class Vecteur:
	def __init__ (self,arbre = None, l = 0, m = 2):
		self.len = l
		self.max = m
		if arbre == None:
			self.arbre = Node (None,None)
		else:
			self.arbre = arbre

	def insert (self,p,e):
		""" Insère l'élément e à la position 
			i dans le vecteur 
		"""
		if p >= self.max:
			return Vecteur (Node(self.arbre, Partial (p,e)), self.len + 1, self.max * 2)
	
	def append (self,e):
		if self.len == self.max:
			a = Node (self.arbre, Partial (self.max + 1, e))
			v = Vecteur ()
			v.len = self.max + 1
			v.max = self.max * 2
			v.arbre = a
			return v
		else:
			v = Vecteur ()
			v.len = self.len + 1
			v.max = self.max
			a = Node (None,None)
			c = a # pointeur de debug 
			b = self.arbre # variable de parcours 
			i = self.len
			while True:
				if i == 0:
					a.childs = [e, b.get (1)]
					break
				elif i == 1:
					a.childs = [b.get(0),e]
					break
				else:
					if i % 2 == 0: # Gauche
						a.childs[1] = b.childs[1]
						a.childs[0] = Node (None, None)
						a = a.childs[0]
						b = b.childs[0]
					else: # Droite
	 					a.childs[0] = b.childs[0]
	 					a.childs[1] = Node (None, None)
	 					a = a.childs[1]
	 					b = b.childs[1]
					i = i / 2
				print ("{}".format (c))
			v.arbre = a
			return v
	def __repr__ (self):
		return self.arbre.__repr__ ()

class Node: 
	def __init__ (self,a,b):
		self.childs = [a,b]

	def get (self,n):
		if 0 <= n <= 1:
			return self.childs[n]
		else:
			raise IndexError ("Index invalide")
 
	def __repr__ (self):
		return "({}<>{})".format (self.childs[0], self.childs[1])


class Partial:
	def __init__ (self,numero,element):
		self.element = element
		self.numero = numero 

	def __repr__ (self):
		return "[{}@{}]".format (self.numero, self.element)