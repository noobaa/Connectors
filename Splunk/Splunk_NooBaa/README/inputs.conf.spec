
[noobaa_s3://<name>]
is_secure = whether use secure connection to AWS
host_name = the host name of the S3 service
aws_account = AWS account used to connect to AWS
bucket_name = S3 bucket
key_name = S3 key
recursion_depth = For folder keys, -1 == unconstrained
initial_scan_datetime = Splunk relative time
max_items = Max trackable items.
max_retries = Max number of retry attempts to stream incomplete items.
whitelist = Override regex for blacklist when using a folder key.
blacklist = Keys to ignore when using a folder key.
character_set = The encoding used in your S3 files. Default to 'auto' meaning that file encoding will be detected automatically amoung UTF-8, UTF8 without BOM, UTF-16BE, UTF-16LE, UTF32BE and UTF32LE. Notice that once one specified encoding is set, data input will only handle that encoding.
