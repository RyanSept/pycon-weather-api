Upload secret configs to S3 bucket for use by `$ aws s3 cp env.json s3://weather-api-bucket`

Set env.json configs to env vars `eval "$(jq -r '. | to_entries | .[] | "export " + .key + "=\"" + .value + "\""' env.json)"`
