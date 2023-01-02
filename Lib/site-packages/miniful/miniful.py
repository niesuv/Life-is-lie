from __future__ import print_function
from numpy import array, linspace, ravel, meshgrid
from collections import defaultdict
import sys


class MembershipFunction(object):

	def __init__(self, FS_list=[], concept=""):
		if FS_list==[]:
			print ("ERROR: please specify at least one fuzzy set")
			exit(-2)
		if concept=="":
			print ("ERROR: please specify a concept connected to the MF")
			exit(-3)

		self._FSlist = FS_list
		self._concept = concept

	def get_values(self, v):
		result = {}
		for fs in self._FSlist:
			result[fs._term] = fs.get_value(v)
		return result

	def get_universe_of_discourse(self):
		mins = []
		maxs = []
		for fs in self._FSlist:
			mins.append(min(fs._points.T[0]))
			maxs.append(max(fs._points.T[0]))
		return min(mins), max(maxs)

	def draw(self, TGT):	
		import seaborn as sns
		mi, ma = self.get_universe_of_discourse()
		x = linspace(mi, ma, 1e4)
		for fs in self._FSlist:
			sns.regplot(fs._points.T[0], fs._points.T[1], marker="d", fit_reg=False)
			f = interp1d(fs._points.T[0], fs._points.T[1], bounds_error=False, fill_value=(0,0))
			plot(x, f(x), "--", label=fs._term)
			plot(TGT, f(TGT), "*", ms=10)
		title(self._concept)
		legend(loc="best")
		show()

	def __repr__(self):
		return self._concept


class FuzzySet(object):

	def __init__(self, points=None, term="", high_quality_interpolate=True, verbose=False):
		if len(points)<2: 
			print ("ERROR: more than one point required")
			exit(-1)
		if term=="":
			print ("ERROR: please specify a linguistic term")
			exit(-3)

		self._high_quality_interpolate = high_quality_interpolate
		self._points = array(points)
		self._term = term

	def get_value(self, v):
		#return self.get_value_slow(v)
		if self._high_quality_interpolate:
			return self.get_value_slow(v)
		else:
			return self.get_value_fast(v)

	def _fast_interpolate(self, x0, y0, x1, y1, x):
		return y0 + (x-x0) * ((y1-y0)/(x1-x0))

	def get_value_slow(self, v):		
		from scipy.interpolate import interp1d

		f = interp1d(self._points.T[0], self._points.T[1], 
			bounds_error=False, fill_value=(self._points.T[1][0], self._points.T[1][-1]))
		result = f(v)
		return(result)

	def get_value_fast(self, v):
		x = self._points.T[0]
		y = self._points.T[1]
		N = len(x)
		if v<x[0]: return self._points.T[1][0]
		for i in range(N-1):
			if (x[i]<= v) and (v <= x[i+1]):
				#print (v,  "in (%f, %f)" % (x[i], x[i+1]), i)
				return self._fast_interpolate(x[i], y[i], x[i+1], y[i+1], v)
		return self._points.T[1][-1] # fallback for values outside the Universe of the discourse


def IF(x,y): return (x,y)
def THEN(x,y): return (x,y)
class FuzzyRule(object):

	def __init__(self, antecedent, consequent, comment="", verbose=False):
		self._antecedent = antecedent
		self._consequent = consequent
		self._comment = comment
		if verbose: print ("Rule '%s': IF %s IS %s THEN %s IS %s" % (comment, antecedent[0], antecedent[1], consequent[0], consequent[1]))

	def __repr__(self):
		return self._comment

	def evaluate(self, variables):
		try:
			variable = variables[self._antecedent[0]._concept]
		except KeyError:
			print ("ERROR: variable", self._antecedent[0]._concept, "not initialized")
			exit(-9)
		result = self._antecedent[0].get_values(variable)
		final_result = result[self._antecedent[1]]
		
		try:
			return {'term' : self._consequent[0], 'output' : self._consequent[1], 'weight' : float(final_result)}
		except:
			print (variables)
			print (result); exit()


class FuzzyReasoner(object):

	def __init__(self):
		self._rules = []
		self._mfs = {}
		self._variables = {}

	def set_variable(self, name, value):
		self._variables[name] = value

	def add_rules(self, rules):
		for rule in rules:
			self._rules.append(rule)

	def sugeno(i):
		result = self._rules[i].evaluate(self._variables)
		return result

	def evaluate_rules(self):
		"""Perform Sugeno inference."""

		outputs = defaultdict(list)
		total_rules = len(self._rules)
		for rule in self._rules:
			res = rule.evaluate(self._variables)
			outputs[res['term']].append([res['weight'], res['output']])

		return_values = {}
		for k,v in outputs.items():
			num = sum(map(lambda x: x[0]*x[1], v))
			den = sum([i for i,j in v])
			if den==0: return_values[k] = 0
			else: return_values[k] = num/den

		return return_values

	def plot_surface(self, variables, output, ax, steps=100):

		from mpl_toolkits.mplot3d import Axes3D
		import matplotlib.pyplot as plt
		from matplotlib import cm
		from matplotlib.ticker import LinearLocator, FormatStrFormatter
	
		if len(variables)>2: 
			print ("Unable to plot more than 3 dimensions, aborting.")
			exit(-10)
		
		if len(variables)==2:

			ud1 = variables[0].get_universe_of_discourse()
			ud2 = variables[1].get_universe_of_discourse()
			inter1 = linspace(ud1[0], ud1[1], steps) 
			inter2 = linspace(ud2[0], ud2[1], steps) 

			X, Y = meshgrid(inter1, inter2)

			def wrapper(x,y):
				print (x,y)
				self.set_variable(variables[0]._concept, x)
				self.set_variable(variables[1]._concept, y)
				res = self.evaluate_rules()
				print (res)
				return res[output]
			
			zs = array([wrapper(x,y) for x,y in zip(ravel(X), ravel(Y))])
			Z = zs.reshape(X.shape)

			ax.plot_surface(array(X),array(Y),array(Z), cmap= "CMRmap")
			ax.set_xlabel(variables[0]._concept)
			ax.set_ylabel(variables[1]._concept)
			ax.set_zlabel(output)
			ax.view_init(-90, 0)  # vertical, horizontal
			

	
if __name__=="__main__":
	pass
