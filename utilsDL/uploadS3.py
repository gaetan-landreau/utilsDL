import boto3
import os
import tqdm
class UploadSynthiaS3Bucket():
        def __init__(self, indir, s3BucketName = "datasets.research.rd.meero.com"):

                self.s3BucketName = s3BucketName
                self.indir = indir

                self.bucket = self.initS3()
                print('--> Bucket init. went fine.')

        def initS3(self):
                """
                Allow to init the right Bucket on S3 to further download weight file used in RetinaFace for face detection. 
                Returns:
                        [s3bucket]: Return the models Bucket from S3.
                """
                s3 = boto3.resource("s3")
                bucket = s3.Bucket(self.s3BucketName)
                return bucket

        def uploadToS3(self,uploadAll=False,onlyResizedImgs=True):
                synthiaDirsName = [l for l in os.listdir(self.indir) if not l.startswith('.')]

                for synthiaDir in tqdm.tqdm(synthiaDirsName):
                        print(f'Processed directory: {synthiaDir}')
                        synthiaCompletePath = os.path.join(self.indir,synthiaDir)
                        if uploadAll:
                                return
                        if onlyResizedImgs:

                                # Upload RGB images. 
                                imgsResizedDirPath = os.path.join(synthiaCompletePath,'RGB_rescaled_x4')
                                for subdir, dirs, files in os.walk(imgsResizedDirPath):
                                        for file in files:

                                                localPath = os.path.join(subdir, file)
                                                s3Path = 'Synthia' + localPath.replace(self.indir,'')

                                                self.bucket.upload_file(localPath,\
                                                                                                s3Path)
                                # Upload .json files. 
                                localPathJsonTrain = os.path.join(synthiaCompletePath,'transformsSorted_train.json')
                                localPathJsonTest = os.path.join(synthiaCompletePath,'transformsSorted_test.json')
                                self.bucket.upload_file(localPathJsonTrain,\
                                                                                'Synthia/' + synthiaDir + '/transforms_train.json')
                                self.bucket.upload_file(localPathJsonTest,\
                                                                                'Synthia/' + synthiaDir + '/transforms_test.json')



if __name__ == "__main__":
        uploaderSynthia = UploadSynthiaS3Bucket(indir='/data/datasets/Synthia', s3BucketName = "datasets.research.rd.meero.com")

        uploaderSynthia.uploadToS3(uploadAll=False,onlyResizedImgs=True)
