# Matchify
This project utilizes the Spotify API and Flask to gather user's top artist info and compare this data to user inputted playlist data. Additionally, this project utilizes the user's chosen playlist to create 100 related artists for each of the artists on the playlist. Using each root artist to generate a list of related artists makes it possible to see the correlation between artists that were recommended and their respective genres.
- - - -

## Try it yourself
Install the following libraries:
`pip install requests-cache `
`pip install spotipy`
`pip install boutifulsoup4`
`pip install plotly`
`pip install seaborn`
`pip install networkx`
`pip install flask`

This program uses these libraries for the following capabilities:
* Spotipy: access user data through the Spotify API
* Flask: render user data
* Seaborn: visualize graphics
* Networkx: create artist directed graph network
* Beautiful Soup: scrape the Billboard Top 100 Artist's site
- - - -

## Data Sources
I used the Spotify Developer API to access the data necessary for my application. The API can be accessed here: https://developer.spotify.com/documentation/web-api/. Almost all of the data needed for my application was dynamic, and was not formatted in any file structure type. Caching was used for each API request using the ‘requests_cache’ library with a sqlite backend. 

The data used in my application includes the username of whoever uses the app, their top artists, the playlist of their choosing, and the music data associated with each song on their playlist (i.e., danceability, acoustic-ness, etc.).

When retrieving a user’s top artists the most important fields of the response were the `[‘name’]` fields which contained the artist names. When retrieving a playlist, the most important fields were also the `[‘name’]` in order to compare the user’s top artists with the artist’s on the playlist. When retrieving the music data associated with each track on the playlist, all fields such as `[‘danceability’]`, `[‘acousticness’]`, `[‘energy’]`, etc. were important to develop the graph data structure. 
- - - -

## Data Structure
`models.py` constructs a graph to illustrate the relationships between artists on the top 100 Billboard artists.
- - - -

## Interaction
Upon loading the application in the browser, the user is prompted to authenticate app access via Spotify. After authenticating the user is directed to the home page of the app. The user can then navigate to either the ‘Top Artists’ page or the ‘Blendr’ page. On the ‘Top Artists’ page the user can view their top artists in the last month, last six months, and all time. On the ‘Blender’ page the user can enter a playlist ID into a form and submit the form which will then load a new page showing the user which, if any, of their top artists are on the playlist.

This web application utilizes Flask to render user data. All pages of the application are rendered via HTML templates with CSS styling and user data Is accessed in each Flask route.
- - - -

## Demo
Watch the demo here: LINK
