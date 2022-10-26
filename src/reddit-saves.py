import praw, csv, codecs
import hydra
import omegaconf
from pathlib import Path
import pyrootutils
from tqdm import tqdm
import time
import pandas as pd
import collections


def handle(saved_models,path):
    reddit_saved_csv = codecs.open(path, 'w', 'utf-8')  # creating our csv file
    saved_csv_writer = csv.writer(reddit_saved_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    saved_csv_writer.writerow(['Name', 'Subreddit', 'Type', 'URL', 'NoSFW'])  # Column names
    print("Evaluating total number of subs")
    sublist = [models for models in saved_models]
    total_subs = len(sublist)
    with tqdm(total=total_subs,desc ="Subs checked for saved") as pbar:
        for model in sublist:
            subreddit = model.subreddit  # Subreddit model that the Comment/Submission belongs to
            subr_name = subreddit.display_name
            url = reddit_home_url + model.permalink
            try:
                if isinstance(model, praw.models.Submission):  # if the model is a Submission
                    title = model.title
                    noSfw = str(model.over_18)
                    model_type = "Post"
                else:  # if the model is a Comment
                    title = model.submission.title
                    noSfw = str(model.submission.over_18)
                    model_type = "Comment"

                saved_csv_writer.writerow([title, subr_name, model_type, url, noSfw])
                pbar.update(1)
            except:
                print("\nMissed some in r/{0}. Check {1}".format(subr_name, url))
                continue

    reddit_saved_csv.close()



if __name__ == '__main__':
    root = pyrootutils.setup_root(__file__, pythonpath=True)
    cfg = omegaconf.OmegaConf.load(root / "configs"/"reddit.yaml")
    reddit_home_url = cfg.url
    reddit = praw.Reddit(client_id=cfg.client_id,
                         client_secret=cfg.client_secret,
                         user_agent='Saved posts scraper by /u/' + cfg.username,
                         username=cfg.username,
                         password=cfg.password)

    saved_models = reddit.user.me().saved(limit=None)  # models: Comment, Submission
    path = root/"data"/"reddit_saved.csv"
    # CSV writer for better formatting
    start = time.time()
    handle(saved_models,path)
    print("\nCOMPLETED!")
    print("Your saved posts are available in reddit_saved.csv file.")
    print("Time Taken : {}".format(time.time()-start))
