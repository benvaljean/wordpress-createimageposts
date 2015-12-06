# wordpress-createimageposts

Automatically create image and video posts in Wordpress from a directory tree of images and videos.

Specifiy a `MediaRoot` in `createposts.cfg` and for each directory in the text file referenced in `TitlesList` wordpress posts are created, collated by the hour for all pictures and videos found. The post date is taken from the file modified date, the post title from the directory title and the tags and categories from `_tags.txt` and `_cats.txt` files within each directory.

The `TitlesList` file should have directory names once-per-line and wordpress credentials placed in the cfg file. Pictures and videos should already be in a location serviced by `MediaRootURL`/dir-name . Image dimensions are placed in a title element of the http link. Videos are inserted into posts using the `[video]` short-code.

Some assumptions are currently hard-coded, such as the html string used and thumbnail size/suffix.

Requires python 2.x

## Usage

	python createposts.py --site=[all|site-name] --title=[all|dir-name] --date=[all|inc] [--version]

#### --site

Specifiy which wordpress site to post to; references the section in `createposts.cfg`

#### --title

Specify a single directory / title to create posts from, or specificy all in which the list specifcied in `TitlesList` is used.

#### --date

Upload all pictures found regardless of file modified timestamp or upload incrementally from when the script was lastrun.

## Configuration file usage

Configure each site under its own `[section]` , general options are in `[createposts]`

###General options
####Thumbnails

Create thumbnails with the (currently) hard-coded suffix and size of `-150x150`. Aspect ratio is maintained.

####UsePhoton

Sets the thumbnail image link to the image itself, allowing Wordpress to rewrite links to `image.jpg?fit=width%2Cheight` based on your media settings in Settings > Media. Photon must be enabled on your site for this to work correctly.

###Site options

####TitleList

One directory-per-line list of directories to iterate through within the `MediaRoot` location when searching for images to post, each post will use the directory name as the post title.

####WPxmlrpcUrl

xmlrpcul of your wordpress site for creating posts, this must be accessable from the script and enabled.

###WPUser

Wordpress username with author permission or higher.

###WPPass

Wordpress password for the above acc.

###MediaRoot

Media root location to iterate through when searching for images to post, eg. /var/www/example.com/pics/


###MediaRootURL

Media root URL to prefix onto image locations in posts. This url should reference the location in `MediaRoot`, eg. http://www.example.com/pics/

