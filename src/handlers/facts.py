import csv
import discord
import re

from typing import Dict

from .. import database_module as database
from .. import utils

sydney_metro_depot = "Marrickville"
sydney_metro_set_name = "Sydney Metro"

train_set_names = {
	"A": "Waratah A Set",
	"B": "Waratah B Set",
	"H": "OSCAR H Set",
	"M": "Millennium M Set",
	"T": "Tangara T Set",
	"K": "K Set",
	"N": "Endeavour N Set",
	"J": "Hunter J Set",
	"D": "Mariyung D Set",
	"SM": sydney_metro_set_name,
}

class Train:
	def __init__(self):
		self.train_set_num = ""
		self.train_set_full_name = ""
		self.train_consist = []
		self.train_builder = ""
		self.train_depot = ""
		self.train_notes = ""

class TrainSet:
	def __init__(self, train_set_name):
		self.train_set_name = train_set_name
		self.trains:Dict[str,Train] = {}

train_sets:Dict[str,TrainSet] = {}

def read_csv_train_info():
	with open(utils.csv_file, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) < 2:
				continue

			train = Train()
			train.train_set_num = row[0]  # Set
			set_name = get_set_from_field(train.train_set_num)
			train.train_set_full_name = train_set_names[set_name]
			train.train_consist = [car.strip() for car in row[1].split(" - ")] # Consist
			if len(row) >= 3:
				train.train_builder = row[2] # Builder
				if len(row) >= 4:
					train.train_depot = row[3] # Depot
					if len(row) >= 5:
						train.train_notes = row[4] # Notes

			train_set = train_sets.setdefault(set_name, TrainSet(train.train_set_full_name))
			train_set.trains[train.train_set_num] = train
	generate_metro_sets() # No table needed, these numbers are predictable and can be generated programmatically

def get_set_from_field(set_field:str) -> str:
	match = re.match(r'^[A-Za-z]+', set_field)
	return match.group(0) if match else set_field

def generate_metro_sets():
	suffixes = ["01", "03", "05", "06", "04", "02"]
	for set_num in range(1, 46):
		set_str = f"{set_num:02d}"
		train = Train()
		train.train_set_num = f"SM{set_str}" # Sydney Metro
		set_name = get_set_from_field(train.train_set_num)
		train.train_set_full_name = train_set_names[set_name]
		train.train_consist = [set_str + suffix for suffix in suffixes]
		train.train_builder = "Alstom"
		train.train_depot = sydney_metro_depot
		train_set = train_sets.setdefault(set_name, TrainSet(train.train_set_full_name))
		train_set.trains[train.train_set_num] = train

def find_car(car_num:str):
	'''
		Searches every Train in every TrainSet for a consist entry matching car_num
		(digits only, e.g. "2863" matches consist entry "TE2863").
		Returns a (TrainSet, Train, full_car_number, metro_note) tuple, or None if not found.
		metro_note may be empty if the train is not a metro
	'''
	for train_set in train_sets.values():
		for train in train_set.trains.values():
			for car in train.train_consist:
				if re.sub(r'^\D+', '', car) == car_num:
					if train_set.train_set_name == sydney_metro_set_name:
						return train_set, train, car, get_metro_car_note(car_num)
					return train_set, train, car, None
	return None

def get_metro_car_note(car_num:str) -> str:
	car_num_int = int(car_num) % 100
	closest_end = "Tallawong"
	if car_num_int % 2 == 0:
		closest_end = "Sydenham"

	if car_num_int in [1, 2]:
		return f"This car is at the {closest_end} end of the metro. The metro can be manually driven from here!"
	if car_num_int in [3, 4]:
		other_car = car_num[:3] + '4'
		if car_num_int == 4:
			other_car = car_num[:3] + '3'
		return f"This car is second-closest to {closest_end}, and is one of the two cars that draw in power from the overhead powerlines! The other is car f{other_car}"
	if car_num_int in [5, 6]:
		other_car = car_num[:3] + '5'
		if car_num_int == 5:
			other_car = car_num[:3] + '6'
		return f"This is one of the middle two cars on the metro. This car is one of the four cars with a motor, along with {car_num[:3]}3, {car_num[:3]}4, and {other_car}"

def get_facts(number:int):
	num_fact = get_number_fact(number)
	train_fact = get_train_info(number)

	if len(num_fact) == 0 and len(train_fact) == 0:
		return f"No facts found for {number}.\nYou can find number facts at https://oeis.org/search?q={number}&language=english&go=Search"
	elif len(num_fact) == 0 and len(train_fact) != 0:
		return f"{train_fact}\nNo number fact found for {number}.\nYou can find number facts at https://oeis.org/search?q={number}&language=english&go=Search"
	elif len(num_fact) != 0 and len(train_fact) == 0:
		return f"Number fact for {number}: {num_fact}\nMore number facts can be found at https://oeis.org/search?q={number}&language=english&go=Search"
	else:
		return f"{train_fact}\nNumber fact for {number}: {num_fact}\nMore number facts can be found at https://oeis.org/search?q={number}&language=english&go=Search"

def get_number_fact(number:int) -> str:
	fact = database.get_number_fact(number)
	if fact is None or len(fact) == 0:
		return ""
	else:
		return fact

def get_train_info(number) -> str:
	car_search = find_car(number)
	if car_search:
		train_set, train, full_car_number, metro_note = car_search
		response = f"The train number {full_car_number} is a {train_set.train_set_name} train ({train.train_set_num})."

		train_note = train.train_notes
		if train_set.train_set_name == sydney_metro_set_name and metro_note is not None:
			response += f"\n{metro_note}"
		elif len(train_note) > 0:
			response += f"\n{train_note}"

		return response
	return ""