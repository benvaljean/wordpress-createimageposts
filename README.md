# wordpress-createimageposts

Automatically create image posts in Wordpress from a directory tree of images

Specifiy a `MediaRoot` in `createposts.cfg` and for each directory in the text file referenced in `TitlesList` wordpress posts are created, collated by the hour for all pictures found. The post date is taken from the file modified date, the post title from the directory title and the tags and categories from `_tags.txt` and `_cats.txt` files with in each directory.

This first public release makes many other assumptions that are hard-coded, such as the html string used and thumbnail suffix used. The script also assumes that the thumbnails already exist - it does not create them. All these features will be added in future releases.

## Usage

	python createposts.py --site=[all|site-name] --title=[all|dir-name] --date=[all|inc] [--version]

#### --site

Specifiy which wordpress site to post to; references the section in `createposts.cfg`

#### --title

Specify a single directory / title to create posts from, or specificy all in which the list specifcied in `TitlesList` is used.

#### --date

Upload all pictures found regardless of file modified timestamp or upload incrementally from when the script was lastrun.
