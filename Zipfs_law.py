import sys, os
import codecs
import re
import operator
import pymorphy2 as pm
import plotly.plotly as py
import math
from plotly.graph_objs import *
from collections import defaultdict

py.sign_in('Helga-ok', '1qw1a3m2pe')

def tokenize_text(text):
	tokens = re.findall(r'\w+-?\w+|\w+', text.strip())
	return tokens

def create_dictionary(documents):
	morph = pm.MorphAnalyzer()
	dictionary = defaultdict(int)
	for document in documents:
		if(os.path.isfile(document)):
			doc = codecs.open(document, encoding = 'utf-8')
			text = doc.read()
			tokens = tokenize_text(text)
			for token in tokens:
				term = morph.parse(token)[0].normal_form
				dictionary[term] += 1
			doc.close()
		else:
                        print('Something wrong with document.')
                        break
	#print_dict(dictionary)
	return dictionary

def print_dict(dictionary):
	for item in dictionary:
		print(item)

def sum_terms(dictionary):
	sum_of_terms = 0
	for item in dictionary:
		sum_of_terms += dictionary[item]
	return sum_of_terms

def main():
	documents = []
	for i in range(1, len(sys.argv)):
		documents.append(sys.argv[i])
	dictionary = create_dictionary(documents)
	sum_of_terms = sum_terms(dictionary)
	print('Количество слов в тексте: ' + str(sum_of_terms))
	#print_dict(dictionary)
	#sorted_dict = sorted(dictionary.values())
	sorted_dict = sorted(dictionary.items(), key=operator.itemgetter(1))
	sorted_dict.reverse()
	#print(sorted_dict)
	#print_dict(list(sorted_dict))
	data = Data([
			Scatter(
		x = [i for i in range(len(sorted_dict))],
		y = [i[1] for i in sorted_dict],
		marker = Marker(
			maxdisplayed=0,
            		opacity=0.8,
            		size=8,
            		symbol='circle-open'),
		mode = 'markers',
		name = 'Uses of Words',
		opacity = 0.9,
		text = [i[0] for i in sorted_dict],
		textfont=dict(
			color='rgb(102, 102, 102)',
			family='Raleway, sans-serif'
        		),
		)
	],
		Scatter(
			x = [i for i in range(len(sorted_dict))],
			y = [i[1]/30000 for i in sorted_dict],
		line = Line(
			color='rgb(102, 102, 102)',
			width = 2
			),
		name = 'c'
		))
	layout = Layout(
	    autosize=False,
	    height=600,
	    showlegend=False,
	    title="Zipf's Law",
	    width=700,
	    xaxis=XAxis(
		autorange=True,
		range=[-0.20165146139334336, 3.201216949619326],
		showgrid=False,
		showline=True,
		title='rank',
		type='log'
	    ),
	    yaxis=YAxis(
		autorange=True,
		range=[1.1543085111245144, 5.629816444758303],
		showgrid=False,
		showline=True,
		title='frequency',
		type='log'
	    )
	)
	fig = Figure(data=data, layout=layout)
	plot_url = py.plot(fig)
main()
