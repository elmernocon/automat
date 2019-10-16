from flask import Flask 
from flask import render_template
from flask import request
from automat import Automaton
import re

# initialize the application
app = Flask(__name__)

# create a function to get the grammar
def get_grammar(regex):
	automaton = Automaton.create_from_regex(regex)

	# get the values
	return automaton.get_alphabet(), automaton.states, automaton.start_state, automaton.final_states, automaton.transitions

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == 'POST':
		# get the regex text
		regex = re.sub('\s', '', request.form['textbox'])

		try:
			# require the user to give a valid text input
			if regex == None or regex == "":
				# reload the page with the empty field error
				return render_template('index.html', error="Please input values")
			
			else:
				# initialize the text for final transitions
				final_transition = ""

				# get the values
				alphabet, states, start, final, transitions = get_grammar(regex)

				# extract all transitions
				transitions = [transition for transition in transitions.items()]

				# extract all the final states
				fin_states = [state for state in final]

				# list down all transitions and parse it to text
				for transition in transitions:
					# get the current state
					current_state = transition[0]
					
					# get the next state and the input by extracting the dict
					for key, value in transition[1].items():
						next_state = key
						input_alphabet = value

					# identify if the state is a final state
					if next_state in fin_states:
						next_state = "{}*".format(next_state)

					print("({0}) -- {1} --> ({2})".format(current_state, 
															input_alphabet,
															next_state))

					final_transition += " <br> ({0}) -- {1} --> ({2})".format(current_state, 
															input_alphabet,
															next_state)

				# reload the page with the response values
				return render_template('index.html', input="({})".format(regex), 
										alphabets=alphabet, 
										states=states, 
										start=start, 
										final=final, 
										transitions=final_transition)
		except:
			# reload the page with the error message
			return render_template('index.html', error="You have inputted an invalid value")
			
	else:
		# return the static index page
		return render_template('index.html')

if __name__ == "__main__":
	# start the application
	app.run(debug=True)