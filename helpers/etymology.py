import urllib.parse
import ety

def get_etymology(word):
	try:
		state = "Before word url parse"
		url_safe_word = urllib.parse.quote(word)
		etymonline_search = "https://etymonline.com/search?q=" + url_safe_word
		etymonline_result = "https://etymonline.com/word/" + url_safe_word

		state = "Before ety tree"
		ety_result = str(ety.tree(word))

		formatted = f"Etymonline:\nSearch: <{etymonline_search}>\nResult: {etymonline_result}\n\nEty tree:\n{ety_result}"
		return formatted
	except Exception as e:
		return f"Error occured while fetching etymology for {word}.\nState: {state}.\nError: {e}"