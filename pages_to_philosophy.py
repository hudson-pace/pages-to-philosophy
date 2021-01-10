import urllib.request

def find_first_link(content):
    link_start = 0
    while True:
        if content.find('(') < content.find('<a href=') and content.find('(') != -1:
            depth = 1
            start_paren = content.find('(')
            current_pos = start_paren + 1
            while depth > 0:
                if content.find('(', current_pos) < content.find(')', current_pos) and content.find('(', current_pos) != -1:
                    depth += 1
                    current_pos = content.find('(', current_pos) + 1
                else:
                    depth -= 1
                    current_pos = content.find(')', current_pos) + 1
                    end_paren = current_pos
            else:
                content = content[end_paren : ]
        else:
            break
    while True:
        link_start = content.find('<a href=', link_start)
        link_start = content.find('"', link_start + 1)
        link_end = content.find('"', link_start + 1)
        if link_start == -1:
            return None
        if content[link_start + 1 : link_start + 6] == '/wiki':
            if content[link_start + 1 : link_start + 11] != '/wiki/Help' and content[link_start + 1 : link_start + 11] != '/wiki/File':
                break
    return content[link_start + 1 : link_end]

def get_first_paragraph(content):
    paragraph_start = content.find('<p>')
    paragraph_end = content.find('</p>', paragraph_start)
    if paragraph_start == -1:
        return None
    if find_first_link(content[paragraph_start : paragraph_end]) != None:
        if '<p><b>' in content[paragraph_start : paragraph_end]:
            return content[paragraph_start : paragraph_end]
        if '<p><span' not in content[paragraph_start : paragraph_end]:
            if '<a href=' in content[paragraph_start : paragraph_end]:
                return content[paragraph_start : paragraph_end]
    return get_first_paragraph(content[paragraph_end : ])
def get_first_list_item(content):
    list_start = content.find('<li>')
    list_end = content.find('</li>', list_start)
    if '<a href=' in content[list_start : list_end]:
        return content[list_start : list_end]
    if list_start == -1:
        return None
    return get_first_list_item(content[list_end :])

def next_page(next_url):
    return 'https://en.wikipedia.org/wiki/' + next_url

def cut_out_tables(content):
    while True:
        table_start = content.find('<table')
        table_end = content.find('</table', table_start)
        if table_start == -1:
            return content
        else:
            content = content[: table_start] + content[table_end :]

def get_page_url(content):
    url_start = content.find('<link rel="canonical" href="https://en.wikipedia.org/wiki/')
    url_end = content.find('>', url_start)
    return content[url_start + 58 : url_end - 2]

def find_pages_to_philosophy(user_input):
    number_of_steps = 0
    pages_so_far = []
    stuck_in_a_loop = False
    url = 'https://en.wikipedia.org/wiki/' + user_input
    valid_input = True
    try:
        page = urllib.request.urlopen(url)
        url = page.geturl()
        pages_so_far.append(url)
        page = str(page.read())
    except:
        valid_input = False
    while url != 'https://en.wikipedia.org/wiki/Philosophy' and stuck_in_a_loop == False and valid_input == True:
        page = cut_out_tables(page)
        if (get_first_paragraph(page) == None):
            page = get_first_list_item(page)
        else:
            page = get_first_paragraph(page)
        url = find_first_link(page)
        url = 'https://en.wikipedia.org' + url
        if url == 'https://en.wikipedia.org/wiki/Philosophical':
            url = 'https://en.wikipedia.org/wiki/Philosophy'
        try:
            page = urllib.request.urlopen(url)
            page = str(page.read())
        except:
            print('Oh snappity-snap! Something was wrong with your input!')
        print(url[30 :])
        if url in pages_so_far:
            print ("\nUh-oh! You're caught in a loop! It will keep looping through:")
            for item in range(pages_so_far.index(url), len(pages_so_far)):
                print(pages_so_far[item][30 :])
                stuck_in_a_loop = True
        else:
            pages_so_far.append(url)
        number_of_steps += 1
    else:
        if (valid_input == False):
            print('Oh snappity-snap! Something was wrong with your input!')
        elif (stuck_in_a_loop == False):
            print('It took {} steps to get to philosophy!'.format(number_of_steps))



def run_program():
    running = True
    while running == True:
        user_input = input('\nWhat page should I start on? ')
        if (user_input == 'Q' or user_input == 'Quit' or user_input == 'q' or user_input == 'quit'):
            running = False
        else:
            find_pages_to_philosophy(user_input)


run_program()
