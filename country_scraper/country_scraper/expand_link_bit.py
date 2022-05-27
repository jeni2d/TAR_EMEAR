import requests

def expand_link(link):
    headers = {
        'Authorization': 'c7a44e5d86c758c1f7660b3aeb9ac605022108c2',
        'Content-Type': 'application/json',
    }

    data = '{' + '"bitlink_id"' + ':' + '"' + link + '"' + '}'

    response = requests.post('https://api-ssl.bitly.com/v4/expand', headers=headers, data=data)

    return response.json()['long_url']