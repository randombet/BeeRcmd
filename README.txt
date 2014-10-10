BeeRcmd is an item-based collaborative filtering recommend system implemented by Python and MySQL.
The webapp is implemented with PHP, JavaScript, MySQL and Ajax.

Data is from Beer Advocate which can be download at https://s3.amazonaws.com/demo-datasets/beer_reviews.tar.gz .


recommsys.py implements the recommend algorithm and output the results to the database.

welcom_message.php servers as the entrance of the web.

getbeer.php gets the recommendation for the user based on their inputs.