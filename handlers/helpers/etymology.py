import urllib.parse
import ety

def get_etymology(word):
	try:
		url_safe_word = urllib.parse.quote(word)

		etymonline_search = "https://etymonline.com/search?q=" + url_safe_word
		etymonline_result = "https://etymonline.com/word/" + url_safe_word

		ety_result = str(ety.tree(word))
		if len(ety_result) == 0:
			ety_result = "No tree found"

		formatted = f"Etymology for '{word}'\n\nEtymonline:\nSearch: <{etymonline_search}>\nResult: {etymonline_result}\n\nEty tree:\n{ety_result}"
		return formatted
	except Exception as e:
		return f"Error occured while fetching etymology for {word}.\nError: {e}"
