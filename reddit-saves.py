import praw, csv, codecs
import hydra
import omegaconf
import pyrootutils



def handle(saved_models):
    count = 1
    for model in saved_models:
        subreddit = model.subreddit  # Subreddit model that the Comment/Submission belongs to
        subr_name = subreddit.display_name
        url = reddit_home_url + model.permalink

        if isinstance(model, praw.models.Submission):  # if the model is a Submission
            title = model.title
            noSfw = str(model.over_18)
            model_type = "#Post"
        else:  # if the model is a Comment
            title = model.submission.title
            noSfw = str(model.submission.over_18)
            model_type = "#Comment"

        print('Model number ' + str(count) + ' is written to csv file.')
        saved_csv_writer.writerow([str(count), title, subr_name, model_type, url, noSfw])

        count += 1



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

    reddit_saved_csv = codecs.open('reddit_saved.csv', 'w', 'utf-8')  # creating our csv file

    # CSV writer for better formatting
    saved_csv_writer = csv.writer(reddit_saved_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    saved_csv_writer.writerow(['ID', 'Name', 'Subreddit', 'Type', 'URL', 'NoSFW'])  # Column names
    handle(saved_models)
    reddit_saved_csv.close()

    print("\nCOMPLETED!")
    print("Your saved posts are available in reddit_saved.csv file.")
