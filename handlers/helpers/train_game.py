import itertools
import copy
import discord

import handlers.helpers.paginator as pagination_module
from handlers.utils import discord_bot, error_message

async def attempt_train_game(interaction:discord.Interaction, number, a, b, c, d, target, use_power, use_modulo):
	try:
		response = get_to_x(target, a, b, c, d, use_power, use_modulo)
		num_of_solutions = len(response)
		if num_of_solutions == 0:
			await interaction.followup.send("There are no solutions for `" + str(number) + "` to get to target " + str(target))
			return
	except Exception as e:
		print(f"Train game: error in get_to_x. {e}")
		await error_message(interaction)
		return
	
	try:
		response_start_title, response_start_subtitle = get_response_start(number, target, num_of_solutions, use_power, use_modulo)
		formatted_list = solve_and_format_solutions(response, target)
	except Exception as e:
		print(f"Train game: error in solving and forming solution list. {e}")
		await error_message(interaction)
		return

	try:
		paginator = pagination_module.Paginator(timeout=None)
		paginator.set(response_start_title, response_start_subtitle, formatted_list)
		await paginator.send(interaction)
	except Exception as e:
		print(f"Train game: error in pagination. {e}")

def get_response_start(number, target, num_of_solutions, use_power, use_modulo):
	title = f"**Results for train game with number {number} and target {target}**"

	subtitle = "\nAll " + str(num_of_solutions) + " solutions"
	if num_of_solutions == 1:
		subtitle = "The only solution"
	elif num_of_solutions == 2:
		subtitle = "Both solutions"
	
	subtitle += " using +-*/"
	if use_power:
		subtitle += "^"
	if use_modulo:
		subtitle += "%"
		
	return title, subtitle

def solve_and_format_solutions(solutions:str, target):
	formatted = []
	try:
		sol_num = 0
		for sol in solutions:
			sol_num += 1
			sol = breakdown_expression(place_brackets(sol), target)
			if sol is None:
				continue
			sol = sol.replace("*", "\*")
			sol = "**" + str(sol_num) + ")** " + sol
			formatted.append(sol)
	except Exception as e:
		print(f"Train game (solve_and_format_solutions): error in solving. {e}")
	return formatted

def place_brackets(expression):
	return "((" + expression[0:3] + ")" + expression[3:5] + ")" + expression[5:]

def breakdown_expression(sol0, target):
	# ((0+9)+0)+1 -> (9+0)+1 -> 9+1 -> 10
	try:
		if len(sol0) != 11:
			print("Somehow got a solution the wrong length (" + str(len(sol0)) + "): " + sol0 + "\nExpected the form (([num] [operation] [num]) [operation] [num]) [operation] [num]")
			return sol0

		so_far = solve(sol0[2], sol0[3], sol0[4])
		sol1 = "(" + str(so_far) + sol0[6:]

		so_far = solve(so_far, sol0[6], sol0[7])
		sol2 = str(so_far) + sol0[9:]

		so_far = solve(so_far, sol0[9], sol0[10])
		sol3 = str(so_far)

		tolerance = 1e-3 # tolerance of ±0.003
		if abs(float(sol3) - float(target)) > tolerance:
			return None

		return sol0 + " -> " + sol1 + " -> " + sol2 + " -> " + sol3
	except Exception as e:
		print(f"Train game (breakdown_expression): error in solving '{sol0}'. {e}")

def solve(num1, op, num2):
	result = 0
	if op == "+":
		result = float(num1) + float(num2)
	elif op == "-":
		result = float(num1) - float(num2)
	elif op == "*":
		result = float(num1) * float(num2)
	elif op == "/":
		result = float(num1) / float(num2)
	elif op == "^":
		result = float(num1) ** float(num2)
	elif op == "%":
		result = float(num1) % float(num2)
	
	if result == int(result):
		return int(result)
	else:
		return float("{:.3f}".format(result))

def get_to_x(x, a, b, c, d, use_power, use_modulo):
	successions = []
	for permutation in itertools.permutations([a, b, c, d]):
		attempt = attempt_get_x(x, permutation, 0, [], use_power, use_modulo)
		if attempt is not None:
			successions.append(attempt)

	for _ in range(0, 4): # the list looks like ass if you don't do this (flatten 4 times cause 4 numbers deep)
		successions = list(itertools.chain.from_iterable(successions))
	
	# turn the list into a set (we need the inner loop because a list isn't hashable and can't be directly added to a set)
	solutions = set()
	for success in successions:
		solution = ""
		for character in success:
			solution += character 
		solutions.add(solution)

	return sorted(solutions)

def attempt_get_x(x, nums, current_total, current_operations:list, use_power, use_modulo):
	successions = []
	if len(nums) < 1 or len(nums) > 4: # something wrong happened
		return successions
	
	# remove the first item cause we're using it now
	current_num = nums[0]
	nums = nums[1:]
	
	if len(nums) == 3: # first number (remember, we took one off)
		attempt = attempt_get_x(x, nums, current_num, [str(current_num)], use_power, use_modulo) # just try the first number by itself
		if attempt is not None:
			successions.append(attempt)
	else:
		# make a new copy of what we've done, so there are no annoying shallow copies
		ops_add = copy.deepcopy(current_operations)
		ops_sub = copy.deepcopy(current_operations)
		ops_mul = copy.deepcopy(current_operations)
		ops_div = copy.deepcopy(current_operations)
		ops_pow = copy.deepcopy(current_operations)
		ops_mod = copy.deepcopy(current_operations)

		# show which operation we're doing
		ops_add.append('+')
		ops_sub.append('-')
		ops_mul.append('*')
		ops_div.append('/')
		ops_pow.append('^')
		ops_mod.append('%')

		# show what number we're doing the operation on
		ops_add.append(str(current_num))
		ops_sub.append(str(current_num))
		ops_mul.append(str(current_num))
		ops_div.append(str(current_num))
		ops_pow.append(str(current_num))
		ops_mod.append(str(current_num))

		# attempt the operation
		attempt_div = None
		attempt_mod = None
		if current_num != 0:
			attempt_div = current_total / current_num
			attempt_mod = current_total % current_num
		attempt_add = current_total + current_num
		attempt_sub = current_total - current_num
		attempt_mul = current_total * current_num
		attempt_pow = current_total ** current_num

		if len(nums) == 0: # last number, no more recursion
			try:
				if attempt_add == int(attempt_add)\
					and attempt_add == x: # addition
						successions.append(ops_add)
			except Exception as e:
				print(f"Train game (attempt_get_x): error in checking if attempts are int for +. {e}")

			try:
				if attempt_sub == int(attempt_sub)\
					and attempt_sub == x: # subtraction
						successions.append(ops_sub)
			except Exception as e:
				print(f"Train game (attempt_get_x): error in checking if attempts are int for -. {e}")

			try:
				if attempt_mul == int(attempt_mul)\
					and attempt_mul == x: # mutiplication
						successions.append(ops_mul)
			except Exception as e:
				print(f"Train game (attempt_get_x): error in checking if attempts are int for *. {e}")

			try:
				if attempt_div is not None\
					and attempt_div == int(attempt_div)\
					and attempt_div == x: # division
						successions.append(ops_div)
			except Exception as e:
				print(f"Train game (attempt_get_x): error in checking if attempts are int for /. {e}")

			try:
				if use_power\
					and attempt_pow == int(attempt_pow)\
					and attempt_pow == x: # exponentiation
						successions.append(ops_pow)
			except Exception as e:
				print(f"Train game (attempt_get_x): error in checking if attempts are int for ^. {e}")

			try:
				if use_modulo\
					and attempt_mod is not None\
					and attempt_mod == int(attempt_mod)\
					and attempt_mod == x: # modulo
						successions.append(ops_pow)
			except Exception as e:
				print(f"Train game (attempt_get_x): error in checking if attempts are int for %. {e}")
		else: # numbers in between
			attempt = attempt_get_x(x, nums, attempt_add, ops_add, use_power, use_modulo) # addition
			if attempt is not None:
				successions.append(attempt)

			attempt = attempt_get_x(x, nums, attempt_sub, ops_sub, use_power, use_modulo) # subtraction
			if attempt is not None:
				successions.append(attempt)

			attempt = attempt_get_x(x, nums, attempt_mul, ops_mul, use_power, use_modulo) # multiplication
			if attempt is not None:
				successions.append(attempt)

			if attempt_div is not None:
				attempt = attempt_get_x(x, nums, attempt_div, ops_div, use_power, use_modulo) # division
				if attempt is not None:
					successions.append(attempt)

			if use_power:
				attempt = attempt_get_x(x, nums, attempt_pow, ops_pow, use_power, use_modulo) # exponentiation
				if attempt is not None:
					successions.append(attempt)

			if use_modulo and attempt_mod is not None:
				attempt = attempt_get_x(x, nums, attempt_mod, ops_mod, use_power, use_modulo) # modulo
				if attempt is not None:
					successions.append(attempt)

	return successions