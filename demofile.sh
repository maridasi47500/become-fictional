
mkdir templates 
python3 scaffold.py country name
python3 scaffold.py job_or_status name
python3 scaffold.py city name
python3 scaffold.py language name short_name
python3 scaffold.py user phone country_id:references username email password job_or_status_id:references
python3 scaffold.py voyage user_id:references city_id:references country_id:references
python3 scaffold.py post user_id:references language_id:references content
python3 scaffold.py product user_id:references nom description prix product_type image categories
python3 scaffold.py creation_or_activity type name description pic user_id:references
