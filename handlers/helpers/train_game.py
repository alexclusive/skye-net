import itertools
import discord

import handlers.helpers.train_info as train_info_module
import handlers.helpers.paginator as pagination_module

async def train_game(interaction:discord.Interaction, number, a, b, c, d, target, strict_mode):
	solutions = set()

	if strict_mode:
		permutations = [(a, b, c, d)] # Just one permutation for strict mode
	else:
		permutations = list(itertools.permutations([a, b, c, d]))

	def attempt(remaining_digits, current_total, expression):
		if len(remaining_digits) == 0:
			if current_total == target:
				solutions.add(expression)
			return

		current_num = remaining_digits[0]
		next_digits = remaining_digits[1:]

		attempt(next_digits, current_total + current_num, expression + "+" + str(current_num))
		attempt(next_digits, current_total - current_num, expression + "-" + str(current_num))
		attempt(next_digits, current_total * current_num, expression + "*" + str(current_num))

		if current_num != 0:
			attempt(next_digits, current_total / current_num, expression + "/" + str(current_num))
			if not strict_mode:
				attempt(next_digits, current_total % current_num, expression + "%" + str(current_num))

		if not strict_mode:
			attempt(next_digits, current_total ** current_num, expression + "^" + str(current_num))
	
	for permutation in permutations:
		if len(permutation) == 0:
			continue
		attempt(permutation[1:], permutation[0], str(permutation[0]))

	response = sorted(solutions)
	num_of_solutions = len(response)
	if num_of_solutions == 0:
		await interaction.followup.send("There are no solutions for `" + number + "` to get to target " + str(target))
		await show_train_info(interaction, number)
		return

	try:
		formatted_list = solve_and_format(response, target)
	except Exception as e:
		print(f"Train game: error in solving and forming solution list. {e}")
		await interaction.followup.send("Sorry! Unable to compute.")
		return
	
	try:
		paginator = pagination_module.Paginator(timeout=None)
		response_title, response_subtitle = get_response_start(number, target, num_of_solutions, strict_mode)
		paginator.set(response_title, response_subtitle, formatted_list)
		await paginator.send(interaction)
		await show_train_info(interaction, number)
	except Exception as e:
		print(f"Train game: error in pagination. {e}")
		await interaction.followup.send("Sorry! Something went wrong while displaying the results.")

async def show_train_info(interaction:discord.Interaction, number):
	car_search = train_info_module.find_car(number)
	if car_search:
		train_set, train, full_car_number = car_search

		response = f"The train number {full_car_number} is a set {train_set.train_set_name} train ({train.train_set_num})."

		train_note = train.train_notes
		if train_set.train_set_name == "Sydney Metro":
			response += f"\n{train_info_module.get_metro_car_note(number)}"
		elif len(train_note) > 0:
			response += f"\n{train_note}"

		await interaction.followup.send(response)

def get_response_start(number, target, num_of_solutions, strict_mode):
	title = f"**Results for train game with number {number} and target {target}**"

	subtitle = "\nAll " + str(num_of_solutions) + " solutions"
	if num_of_solutions == 1:
		subtitle = "The only solution"
	elif num_of_solutions == 2:
		subtitle = "Both solutions"
	
	subtitle += " using +-*/"
	if strict_mode:
		subtitle += " with no permutations"
	else:
		subtitle += "^% with permutations"
		
	return title, subtitle

def solve_and_format(solutions, target):
	formatted = []
	for i, expression in enumerate(solutions, start=1):
		solved = solve(place_brackets(expression), target)
		if solved is not None:
			solved = solved.replace("*", r"\*")
			formatted.append(f"**{i})** {solved}")
	return formatted

def place_brackets(expression):
	return "((" + expression[0:3] + ")" + expression[3:5] + ")" + expression[5:]

def solve(expression, target):
	# ((7+1)+1)+1 -> (8+1)+1 -> 9+1 -> 10
	if len(expression) != 11:
		print("Somehow got a solution the wrong length (" + str(len(expression)) + "): " + expression + "\nExpected the form (([num] [operation] [num]) [operation] [num]) [operation] [num]")
		return expression
	
	try:
		step_one = compute(expression[2], expression[3], expression[4])
		step_two = compute(step_one, expression[6], expression[7])
		step_three = compute(step_two, expression[9], expression[10])

		tolerance = 1e-3 # tolerance of ±0.003
		if abs(float(step_three) - float(target) > tolerance):
			return None # incorrect solution
	except Exception as e:
		print(f"Train game (breakdown_expression): error in solving '{expression}'. {e}")
		return None
	
	step_one_text = "(" + str(step_one) + expression[6:]
	step_two_text = str(step_two) + expression[9:]
	step_three_text = str(step_three)
	return expression + " -> " + step_one_text + " -> " + step_two_text + " -> " + step_three_text

def compute(num1, op, num2):
	operations = {
		"+": lambda a, b: float(a) + float(b),
		"-": lambda a, b: float(a) - float(b),
		"*": lambda a, b: float(a) * float(b),
		"/": lambda a, b: float(a) / float(b),
		"^": lambda a, b: float(a) ** float(b),
		"%": lambda a, b: float(a) % float(b)
	}
	if op not in operations:
		# throw error to show this didnt work
		pass

	result = operations[op](num1, num2)
	if result == int(result):
		return int(result)
	else:
		return float("{:.3f}".format(result))