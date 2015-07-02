#-*-coding:utf8*-
import sys
import bisect

class CliqueCritique:
	def __init__(self, c):
		(X,deltamin,deltamax,tp,td) = c
		self._deltamax=deltamax
		self._deltamin=deltamin
		self._td=td
		self._tp=tp
		self._X = X


	def __eq__(self, other):
		if self._X == other._X and self._td == other._td and self._tp == other._tp and self._deltamin == other._deltamin  and self._deltamax == other._deltamax:
			return True
		else:
			return False

	def __hash__(self):
		return hash((self._X,self._deltamin,self._deltamax,self._deltamin,self._td,self._tp))

	def __str__(self):
		return ','.join(map(str, list(self._X)))  + " " +  str(self._deltamin) + " " + str(self._deltamax) + " " + str(self._td)+ " " + str(self._tp)
