#-*- coding: utf-8 -*-
# tokenizer.py
# 
# Aliaume Lopez
#
# Crée les tokens 
# à partir d'une expression
# en Alisp textuelle

# Trouver un super moyen 
# de généraliser les méthodes
# de parsing ... avec de l'héritage ?
# Parce que là c'est beaucoup de code 
# et peu lisible ... 
#
# Ajouter un type variable plutôt
# que garder les chaines nues 
#
# Simplifier le parser est nécessaire ... utiliser une lib ?

# Les différents types de variable nus 
class String:
	def __init__ (self, valeur):
		self.valeur = valeur
	
	def __str__ (self):
		return "String({})".format (self.valeur)
	
class Dict:
	def __init__ (self, liste):
		self.liste = liste 
	
	def __str__ (self):
		return "Dict({})".format (self.liste)

class Liste:
	def __init__ (self, liste):
		self.liste = liste
	
	def __str__ (self):
		return "Liste({})".format (self.liste)

class Atome:
	def  __init__ (self, val):
		self.val = val
	
	def __str__ (self):
		return "Atome({})".format (self.val)

class Nombre:
	def __init__ (self, val):
		self.val = val
	
	def __str__ (self):
		return "Nombre({})".format (self.val)

# Crée les tokens ! 
# On fait une classe pour garder 
# un état global afin de simplifier 
# grandement le système de 
# syntaxes différentes en fonction 
# de modificateurs !

class Tokenizer:
	def __init__ (self):
		self.string = ""
		self.position = 0
		self.buf = ""

	def reset (self):
		""" Reset du tokenizer """
		self.position = 0
		self.string = ""

	def tokenize (self, string):
		self.reset () # reset
		self.string = string # met dans la bonne configuration 

		return self.parseGeneral () # youhou !!!!!
	
	def appendBuf (self, tokens):
		if self.buf != "" and self.buf != " ":
			tokens.append (self.buf)
		self.buf = ""

	def parseGeneral (self):
		self.buf = ""
		tokens = []
		while self.position < len (self.string):
			t = self.string[self.position]
			self.position += 1

			if t == " " and self.buf == "":
				pass
			elif self.buf == "" and t.isdigit ():
				self.appendBuf (tokens)
				self.position -= 1
				tokens.append (self.parseNombre ())
			elif t == "(":
				self.appendBuf (tokens)
				tokens.append (self.parseListe ())
			elif t == "{":
				self.appendBuf (tokens)
				tokens.append (self.parseDict ())
			elif t == "\"":
				self.appendBuf (tokens)
				tokens.append (self.parseString ())
			elif t == ")":
				raise ValueError ("Fermeture de liste en trop")
			elif t == "}":
				raise ValueError ("Fermeture de dictionnaire en trop")
			elif t == ":":
				self.appendBuf (tokens)
				tokens.append (self.parseAtom ())
			elif t == " " and self.buf != "":
				self.appendBuf (tokens)
			else:
				self.buf += t
		if tokens == []:
			return self.buf
		else:
			return tokens 

	def parseString (self):
		self.buf = ""
		while self.position < len (self.string):
			t = self.string[self.position]
			self.position += 1
			if t == "\"":
				s = String (self.buf)
				self.buf = ""
				return s
			else:
				self.buf += t
		raise ValueError ("Chaine de caractère qui n'en finit pas ... ")
	
	def parseNombre (self):
		self.buf = ""
		while self.position < len (self.string):
			t = self.string[self.position]
			self.position += 1
			if t == " ":
				n = float (self.buf)
				self.buf = ""
				return Nombre (n)
			elif t == ")":
				self.position -= 1
				a = Nombre (float (self.buf))
				self.buf = ""
				return a
			elif t == "}":
				self.position -= 1
				a = Nombre (float (self.buf))
				self.buf = ""
				return a
			else:
				self.buf += t
		a = Nombre (float (self.buf))
		self.buf = ""
		return a
	
	def parseAtom (self):
		self.buf = ""
		tokens = []
		while self.position < len (self.string):
			t = self.string[self.position]
			self.position += 1
			if t == " ":
				a = Atome (self.buf)
				self.buf = ""
				return a
			elif t == ")":
				self.position -= 1
				a = Atome (self.buf)
				self.buf = ""
				return a
			elif t == "}":
				self.position -= 1
				a = Atome (self.buf)
				self.buf = ""
				return a
			else:
				self.buf += t
		a = Atome (self.buf)
		self.buf = ""
		return a
	
	def parseListe (self):
		self.buf = ""
		tokens = []
		while self.position < len (self.string): # normal
			t = self.string[self.position] # caractère
			self.position += 1
			
			if t == " " and self.buf == "":
				pass
			elif self.buf == "" and t.isdigit ():
				self.appendBuf (tokens)
				self.position -= 1
				tokens.append (self.parseNombre ())
			elif t == "(": # c'est une ouverture de liste
				self.appendBuf (tokens)
				tokens.append (self.parseListe ())
			elif t == "{":
				self.appendBuf (tokens)
				tokens.append (self.parseDict ())
			elif t == "}":
				raise ValueError ("Fermeture de dictionnaire en trop")
			elif t == "\"":
				self.appendBuf (tokens)
				tokens.append (self.parseString ())
			elif t == ")": # C'est une fermeture de liste 
				self.appendBuf (tokens)
				return Liste (tokens) # fin ... on est bon !
			elif t == ":":
				self.appendBuf (tokens)
				tokens.append (self.parseAtom ())
			elif t == " " and self.buf != "":
				self.appendBuf (tokens)
			else:
				self.buf += t
		raise ValueError ("Liste non terminée ... ")
		
	def parseDict (self):
		self.buf = ""
		tokens = []
		while self.position < len (self.string):
			t = self.string[self.position]
			self.position += 1

			if t == " " and self.buf == "":
				pass
			elif self.buf == "" and t.isdigit ():
				self.appendBuf (tokens)
				self.position -= 1
				tokens.append (self.parseNombre ())
			elif t == "(":
				self.appendBuf (tokens)
				tokens.append (self.parseListe ())
			elif t == "{":
				self.appendBuf (tokens)
				tokens.append (self.parseDict ())
			elif t == "\"":
				self.appendBuf (tokens)
				tokens.append (self.parseString ())
			elif t == ")":
				raise ValueError ("Fermeture de liste en trop ... ")
			elif t == "}":
				self.appendBuf (tokens)
				if len (tokens) % 2 != 0:
					print ("{}".format (tokens))
					raise ValueError ("Le dictionnaire a des clefs sans valeurs ...")
				return Dict (tokens)
			elif t == ":":
				self.appendBuf (tokens)
				tokens.append (self.parseAtom ())
			elif t == " " and self.buf != "":
				self.appendBuf (tokens)
			else:
				self.buf += t
		raise ValueError ("Dictionnaire non terminé ... ")

