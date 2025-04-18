import urllib.parse
import ety
import requests
import bs4
from bs4 import BeautifulSoup

word_classes = ["adj.", "adv.", "conj.", "n.", "prep.", "pron.", "v."]

def get_etymology(word):
	try:
		url_safe_word = urllib.parse.quote(word)
		etymonline_url = "https://etymonline.com/word/" + url_safe_word
		etymonline_result = "No definition found"
		images = []

		# Fetch the etymonline page
		response = requests.get(etymonline_url)
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, "html.parser")
			text_result:bs4.element.ResultSet = soup.find_all("div", {"class": "space-y-2"})
			if text_result:
				main_results = set() # sometimes get duplicates somehow
				for result in set(text_result):
					text = result.get_text(strip=False)
					text = text.split("\n")[0]
					if not text.startswith(f"{word}"):
						# throw away anything that isn't the first paragraph of the word
						continue
					word_class_start = text.find("(") + 1
					word_class_end = text.find(")")
					word_class = text[word_class_start:word_class_end].strip()
					if word_class not in word_classes:
						# throw away anything that doesn't show a word class (i.e. won't be the paragraph we want)
						continue
					_, paragraph = text.split(")", 1)
					paragraph = paragraph.strip().replace("*", "\*")
					formatted = f"**{word}** ({word_class})\n{paragraph}"
					main_results.add(formatted)
				etymonline_result = "\n\n".join(main_results)

			image_result:bs4.element.ResultSet = soup.find_all("img", {"alt": f"{word}"})
			if image_result:
				for result in image_result:
					images.append(result.get("src"))
		else:
			etymonline_result = "No result found (404 or other error)"

		# # Get ety tree
		# ety_tree = str(ety.tree(word))
		# if len(ety_tree) == 0:
		# 	ety_tree = "No tree found"

		# Format the result
		formatted = f"Etymology for '{word}'\n"
		formatted += f"<{etymonline_url}>\n\n{etymonline_result}\n"
		if len(images) > 0:
			formatted += "\n".join(images)
		
		return formatted
	except Exception as e:
		return f"Error occurred while fetching etymology for {word}.\nError: {e}"
