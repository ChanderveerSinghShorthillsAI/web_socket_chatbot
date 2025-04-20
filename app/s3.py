class S3Manager:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name

    def get_presigned_urls(self, folder: str, filenames: list[str]) -> list[str]:
        """
        Generate presigned URLs for accessing files in an S3 bucket.

        Args:
            folder (str): The folder path within the S3 bucket.
            filenames (list[str]): A list of filenames to generate URLs for.

        Returns:
            list[str]: A list of presigned URLs for the specified files.
        """
        return [
            f"https://{self.bucket_name}.s3.amazonaws.com/{folder}/{filename}"
            for filename in filenames
        ]
