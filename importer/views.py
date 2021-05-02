from django.shortcuts import render, redirect
import importlib, json, os, requests
from pathlib import Path
# from login.models import User
from .models import Book, Author, Narrator, Genre
# core merge logic:
from .merge_cli import *
from django.contrib import messages

rootdir = f"{str(Path.home())}/input"

def importer(request):
	folder_arr = []
	for path in Path(rootdir).iterdir():
		base = os.path.basename(path)
		full = path
		folder_arr.append(base)

	context = {
		"this_dir": folder_arr,
	}
	return render(request, "importer.html", context)

def dir_selection(request):
	request.session['input_dir'] = request.POST['input_dir']

	return redirect('/import/match')

def match(request):
	context = {
		"this_input": request.session['input_dir']
	}
	
	return render(request, "match.html", context)

def make_models(asin, input_data):
	
	metadata = audible_parser(asin)
	m4b_data(input_data, metadata, output)

	# Book DB entry
	#TODO: fix long_desc
	if 'subtitle' in metadata:
		base_title = metadata['title']
		base_subtitle = metadata['subtitle']
		title = f'{base_title} - {base_subtitle}'
	else:
		title = metadata['title']

	new_book = Book.objects.create(
		title=metadata['title'], 
		asin=asin, short_desc=metadata['summary'], 
		long_desc="", 
		release_date=metadata['release_date'], 
		converted=True, 
		src_path=input_data[0], 
		dest_path=f"""
		\"
		{output}/
		{metadata['authors'][0]}/
		{metadata['title']}/
		{title}.m4b
		\"
		"""
		)

	# Only add in series if it exists
	if 'series' in metadata:
		new_book.series = metadata['series']

	new_book.save()

	# # Author DB entry
	# # Need check if author exists
	# new_author = Author.objects.create(short_desc="", long_desc="")
	# new_author.save()

	# # Need check if narrator exists
	# # Narrator DB entry
	# new_narrator = Narrator.objects.create()
	# new_narrator.save()

def api_auth(request):
	return render(request, "authenticate.html")

def get_auth(request):
	audible_login(
		USERNAME=request.POST['aud_email'], 
		PASSWORD=request.POST['aud_pass'])
	return redirect('/import/match)

def get_asin(request):
	#check that user is signed into audible api
	auth_file = Path(dir_path, ".aud_auth.txt")
	if not auth_file.exists():
		return redirect('/import/api_auth')

	asin = request.POST['asin']
	input_data = get_directory(
		f"{rootdir}/{request.session['input_dir']}"
		)
	# Check for validation errors
	errors = Book.objects.book_asin_validator(request.POST)
	if len(errors) > 0:
		for k, v in errors.items():
			messages.error(request, v)
		return redirect('/import/match')
	else:
		# Check that asin actually returns data from audible
		check = requests.get(f"https://www.audible.com/pd/{asin}")
		if check.status_code == 200:
			make_models(asin, input_data)
			return redirect(f'/import/{asin}/confirm')
		else:
			print(f'Got http error: {check.status_code}')
			return redirect('/import/match')

def finish(request, asin):
	context = {
		"this_book": Book.objects.get(asin=asin)
	}
	
	return render(request, "finish.html", context)