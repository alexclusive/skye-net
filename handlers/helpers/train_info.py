import csv
import os
import re
from typing import Dict # need this so i can do type hints

from bs4 import BeautifulSoup

helpers_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(helpers_dir, "database", "train_info.csv")
html_file = os.path.join(helpers_dir, "database", "train_info.html")

class Train:
	def __init__(self):
		self.train_set_num = ""
		self.train_consist = []
		self.train_builder = ""
		self.train_depot = ""
		self.train_notes = ""

class TrainSet:
	def __init__(self, train_set_name):
		self.train_set_name = train_set_name
		self.trains:Dict[str,Train] = {}

train_sets:Dict[str,TrainSet] = {}

def find_car(car_num:str):
	'''
		Searches every Train in every TrainSet for a consist entry matching car_num
		(digits only, e.g. "2863" matches consist entry "TE2863").
		Returns a (TrainSet, Train, full_car_number) tuple, or None if not found.
	'''
	for train_set in train_sets.values():
		for train in train_set.trains.values():
			for car in train.train_consist:
				if re.sub(r'^\D+', '', car) == car_num:
					return train_set, train, car
	return None

def print_all_train_set_names():
	for train_set in train_sets.values():
		print(train_set.train_set_name)
		if train_set.train_set_name == "Sydney Metro":
			for train in train_set.trains.values():
				print(f"  {train.train_set_num}: {train.train_consist}")

def get_set_from_field(set_field:str) -> str:
	match = re.match(r'^[A-Za-z]+', set_field)
	return match.group(0) if match else set_field

def read_csv_into_trains():
	with open(csv_file, 'r', encoding='utf-8') as f:
		reader = csv.reader(f)
		for row in reader:
			if len(row) < 2:
				continue

			train = Train()
			train.train_set_num = row[0]  # Set
			train.train_consist = [car.strip() for car in row[1].split(" - ")]  # Consist
			if len(row) >= 3:
				train.train_builder = row[2]  # Builder
				if len(row) >= 4:
					train.train_depot = row[3]  # Depot
					if len(row) >= 5:
						train.train_notes = row[4]  # Notes

			set_name = get_set_from_field(train.train_set_num)
			train_set = train_sets.setdefault(set_name, TrainSet(set_name))
			train_set.trains[train.train_set_num] = train
	generate_metro_sets() # No table needed, these numbers are predictable and can be generated programmatically

def generate_metro_sets():
	suffixes = ["01", "03", "05", "06", "04", "02"]
	for set_num in range(1, 46):
		set_str = f"{set_num:02d}"
		train = Train()
		train.train_set_num = f"SM{set_str}" # Sydney Metro
		train.train_consist = [set_str + suffix for suffix in suffixes]
		train.train_builder = "Alstom"
		train.train_depot = "Marrickville"
		train_set = train_sets.setdefault("Sydney Metro", TrainSet("Sydney Metro"))
		train_set.trains[train.train_set_num] = train

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

def convert_html_to_csv():
	'''
		Code taken from https://gist.github.com/erd0s/2d0593332c88bfb13dadbaa87d26cd9d
		Translated from js to py and modified a lot for what I wanted. Other converters didn't take rowspan into account and ended up with misaligned cells
		To set up: Copy the html table from https://nswtrains.fandom.com/wiki/List_of_Sydney_Trains/NSW_TrainLink_fleets and put into train_info.html
	'''
	source_file_path = html_file
	dest_file_path = csv_file

	def clean_text(cell):
		return " ".join(cell.get_text(" ", strip=True).replace("\u00a0", " ").split())

	with open(source_file_path, 'r', encoding='utf-8') as source_file:
		soup = BeautifulSoup(source_file.read(), 'html.parser')

	rows = [row for row in soup.select("table.wikitable > tbody > tr") if not row.select("th")]
	records = []

	# A <td rowspan="N"> "belongs" to its column for the next N-1 rows too, so
	# those rows won't have a <td> of their own for that column. carried_over
	# tracks, per column, how many rows are still owed that cell's text.
	carried_over = {}  # col -> [rows_left, text]

	for i, row in enumerate(rows):
		cells = iter(row.select("td"))
		record = []
		col = 0

		while True:
			if col in carried_over:
				rows_left, text = carried_over[col]
				if rows_left == 1:
					del carried_over[col]
				else:
					carried_over[col][0] -= 1
			else:
				cell = next(cells, None)
				if cell is None:
					break  # no carried-over cell and no more <td>s: row is done
				text = clean_text(cell)
				rowspan = int(cell.get('rowspan', 1))
				if rowspan > 1:
					carried_over[col] = [rowspan - 1, text]

			record.append(text)
			col += 1

		# Pad rows that are shorter than the expected column count so the CSV stays aligned.
		while len(record) < 5:
			record.append('')

		records.append(record)

	with open(dest_file_path, 'w', encoding='utf-8', newline='') as dest_file:
		writer = csv.writer(dest_file, lineterminator='\n')
		for record in records:
			while record and record[-1] == '':
				record.pop()
			writer.writerow(record)