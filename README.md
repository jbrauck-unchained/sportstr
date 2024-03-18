# Introducing Sportstr
### A python script based solution to getting sports RSS feeds into my nostr feed.

I am sports junkie and even though I a bitcoiner I am also still the guy at the barbecue asking if you caught the game last night.

In this repo you will find a variety of identical repos all essentially doing the same thing. It fetches an rss feed from one source, then right after fetches all posts from the account in question from the last two days. Using text pre-processing and a cosine similarity scoring mechanism, it decides how similar this is to recent headlines. If this score cracks an 80% similarity threshold, then it will choose not to post the article. This in hopes to expanding to multiple sources for each category and stopping those sources from posting duplicates.

If an article looks new and unique, it fires it off from the post_note.py script.

Lastly, the way this is currently working is its running on a cron job every 30 min from my home server. I hope to modify this so it kicks off on a custom schedule whenever an rss feed is updated.

All in all this a fun project for my own entertainment, and all zaps on posts will be donated to opensats (I expect this to be a pretty low amount lol)


## Installation 
To install the required packages for this project, make sure you have Python installed on your system. Then, follow these steps: 
1. Clone this repository to your local machine
2. Navigate to the project directory
3. Install the required packages using `pip` and the `requirements.txt` file

This will install all the necessary dependencies for the project.

## Usage

Now you can choose to modify these scripts or run them yourself. You will just have to use your own nsec for a nostr account.
They each get kicked off from the `fetch_xx_rss.py`files.

## Contributing

If you would like to contribute to this project, please reach out to me on nostr and we can discuss a path forward for this.

Rudy Nutstink (rnutstink@nostrplebs.com)
npub125q2n8m6ml7rr2e8n7kp9rdmexxfpm6d3jgsr44hl5lr294cjvsqc052n4

## License

This project is licensed under the [MIT License](LICENSE).
(Maybe this is true, idk all the cool projects say it)



