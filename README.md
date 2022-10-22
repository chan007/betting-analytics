## Betting analytics

Thesis - There are sure shot ways (can be proven using probability) to make money on betting platforms. Betting platforms get away with this by limiting the bets that successful players can make this or by outright banning them. This is similar to how casinos treat card counting. 
It is possible to make software that lets other people do this effectively. We charge a fee from users for using this software. Players can keep using this software till they get banned.


## Things to try out:
Some way to store historical data from betway and show it in a ui
events -> markets -> outcomes

Figure out how does betting odds algorithm works. Is it similar to google win prediction algorithm?

Algorithm to find positive ev bets


## Design

### Match Winner odds chart
1. Make a scraper for a single url - done
2. Print out the data - done
3. Write it to a db
4. Make a server to read from db and display a graph.

5. Make a crawler so that we don't have to hardcode the urls
6. Scraping other markets other than match winner?

## Setup
1. clone the repo
2. use python 3.7 version
3. make a virtual env (python3.7 -m venv env)
4. activate it (source env/bin/activate) and install dependencies(pip install -r requirements.txt)
5. run script
