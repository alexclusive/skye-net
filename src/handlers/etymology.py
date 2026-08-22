import bs4
import requests
import urllib.parse

from .. import logger

word_classes = ["adj.", "adv.", "conj.", "n.", "prep.", "pron.", "v."]

def get_etymology(word):
	logger.log(logger.LOG_DETAIL, f"Getting etymology for {word}")
	try:
		url_safe_word = urllib.parse.quote(word)
		etymonline_url = "https://etymonline.com/word/" + url_safe_word
		etymonline_result = "No definition found"
		images = []

		
		logger.log(logger.LOG_DETAIL, f"Fetching from url {etymonline_url}")
		response = requests.get(etymonline_url)
		if response.status_code == 200:
			soup = bs4.BeautifulSoup(response.text, "html.parser")
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
			logger.log(logger.LOG_DETAIL, "No connection made")

		formatted = f"Etymology for '{word}'\n"
		formatted += f"<{etymonline_url}>\n\n{etymonline_result}\n"
		if len(images) > 0:
			formatted += "\n".join(images)
		
		return formatted
	except Exception as e:
		logger.log(logger.LOG_INFO, f"Error getting etymology: {e}")
		return f"Error occurred while fetching etymology for {word}.\nError: {e}"