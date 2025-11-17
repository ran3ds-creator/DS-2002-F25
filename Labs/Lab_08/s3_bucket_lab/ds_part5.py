import urllib.request
import boto3
import sys

def main():
    file_url = "https://media.giphy.com/media/fUYhyT9IjftxrxJXcE/giphy.gif"
    object_name = "lab8.gif"

    bucket_name = sys.argv[1]
    expires_in = int(sys.argv[2])

    urllib.request.urlretrieve(file_url, object_name)

    s3 = boto3.client("s3", region_name="us-east-1")

    s3.upload_file(object_name, bucket_name, object_name)

    response = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": object_name},
        ExpiresIn=expires_in
    )

    print(response)

if __name__ == "__main__":
    main()

