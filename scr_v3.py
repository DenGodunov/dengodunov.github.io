# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
#import time
import os.path
from github3 import login
from datetime import datetime


"""
    Main goal of this program is to update values 
    on my static sate dengodunov.github.io with actual 
    values from from open.kattis.com and commit new values 
    via gihub API to site repository.
    This program will run once every day as cron task (using pythonanywhere for creating and running cron task) 
"""

def get_difficulty(html):
    """
        Function takes url for particular problem on open.kattis.com as parameter 
        and return actual 'Diffuculty' of current problem 

        get_difficulty(str)->str

	get_difficulty('https://open.kattis.com/problems/10kindsofpeople')->
	>>>5.2
    """
    html = requests.get(html).text
    soup = BeautifulSoup(html, 'lxml')
    #find <section> with "difficulty" in it
    my_section = soup.findAll("section", {"class": "box clearfix main-content"})[-1]
    #find <div> with "difficulty" in it
    my_div = my_section.find_all("div", {"class": "sidebar-info"})[2]
    #finally find <p> with "difficulty" in it
    my_p = my_div.find_all("p")[3]

    return str(my_p.text.split("  ")[-1])

def title(html):
    """
        Function takes url for particular problem on open.kattis.com as parameter 
        and return actual 'Title' of current problem 
        get_title(str)->str
        get_title('https://open.kattis.com/problems/10kindsofpeople')->
        >>>10 Kinds of People
    """
    html = requests.get(html).text
    soup = BeautifulSoup(html, 'lxml')
    title_div = soup.find("div", {"class": "headline-wrapper"})
    title = soup.find("h1").text
    #print(title)
    return title

def item_to_tr(item):
    """
        Takes tuple as input and return chunk of html in form:
        <tr>
           <td></td>
           <td><a href='%s'>%s</a></td>
           <td>%s</td>
           <td>%s</td>
           <td>%s</td>
        </tr>
        item_to_tr(tuple)-> str
        item_to_tr('https://open.kattis.com/problems/alphabetspam', ['Alphabet Spam', '96%', 1.4, 1.4, 0.0])->
        >>><tr>
               <td></td>
               <td><a href='%s'>%s</a></td>
               <td>%s</td>
               <td>%s</td>
               <td>%s</td>
            </tr>
    """
    formatted_string = """
            <tr>
                <td></td>
                <td><a href='%s'>%s</a></td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
""" % (item[0],    #link to problem
       item[1][0], # problem's Title
       item[1][1], # percent
       item[1][3], # new difficulty value
       item[1][4]  # difference between previous and current values of difficulty
       )
    return formatted_string

def commit_content(c):
    new_content = c
    username = 'DenGodunov'
    token = 'xxx'
    gh = login(username=username, token=token)
    
    repo = gh.repository(username, 'dengodunov.github.io')
    tf = repo.file_contents('/index.html')

    dt = str(datetime.now())
    c = tf.update(dt, new_content.encode('utf-8'))
    c




# first part - gather all rows from table from dengodunov.github.io
html = requests.get('https://dengodunov.github.io').text
soup = BeautifulSoup(html,"lxml")
table = soup.findChildren('table')[0]
rows = table.findChildren(['tr'])

dict_items = {}

# secondly parse all data ain rows and it to dictionary
# in form.. {'link':['https://open.kattis.com/problems/10kindsofpeople', 66%, 5,3], ..} 
for row in range(len(rows)):    
    cells = rows[row].findChildren('td')
    l = []
    for cell in range(len(cells)):
        # case for link
        if cell == 1:
            a = cells[cell].find('a').get('href')
        # case for difficulty
        elif cell == 3:
            value = cells[cell].string
            l.append(float(value))
        # all other cases, percent of users that solved problem for example
        else:
            value = cells[cell].string
            l.append(value)

    #adding Tilte, New difficulty and difference to our list of item properties
    l[0] = title(a)
    prev_difficulty = float(l[-2])
    new_difficulty = float(get_difficulty(a))
    l[3] = new_difficulty
    l.append(round(new_difficulty-prev_difficulty,1))
    #print(l)
    #create item to dictionary key = link and value = list of properties and adding new item to dictionary       
    dict_items[a] = l


#f_out = open('my_file.txt', 'a',encoding='utf-8')

# this loop needed to sort all items by difficulty in descending order
# and for each item it append chunk of html to sourse file/content variable
#
header = """
<!DOCTYPE html>
<html>
<head>
	<title></title>
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
        <link  rel='stylesheet' href='main.css'/>
        <script type="text/javascript" src="https://code.jquery.com/jquery-2.2.4.min.js"></script>
        <script type="text/javascript" src="scripts.js"></script>
</head>
<body> 
<div class="wrap">
<div id=page1>	
<div class="container-fluid">
<h3>My solved problems from <a href='https://open.kattis.com/'>open.kattis.com</a></h3>
  <div class="row">
     <div class="panel panel-default">
        <div class="panel-heading">
                <button id="clickOn" class="btn btn-xs btn-default pull-right">Show all</button>
                <button id="clickOff" class="btn btn-xs btn-default pull-right">Hide</button>
                Solved Puzzles
                <span class="badge">14</span>
       </div>

<table id="openoff" class='off table table-bordered table-striped table-responsive table-hover table-compact'>	

"""
footer = """
	</table>
   			</div>
		</div>
	</div>
</div>
</div>
</body>
</html>
"""
content = header + '\n'
for i in sorted(dict_items.items(), key=lambda e: e[1][3], reverse = True):
    #print(i, i[1][3])
    content += item_to_tr(i)+'\n'
    #time.sleep(4)
content += footer
#f_out.close()
commit_content(content)
        
    

